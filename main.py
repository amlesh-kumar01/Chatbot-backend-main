from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import numpy as np
import requests
import json
import uuid
import re
import os
import asyncio
from datetime import datetime
from typing import Optional, List, Dict
from dotenv import load_dotenv
from utils import load_embeddings, get_query_embedding, retrieve_relevant_chunks, generate_answer

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="GYWS Chatbot API",
    description="A RAG-based chatbot service for GYWS and IIT Kharagpur queries",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API keys from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY not found in environment variables. Please set it in .env file.")

EMBEDDINGS_FILE = "embeddings.npy"

# In-memory storage (in production, use a database)
conversation_store: Dict[str, List[Dict]] = {}
active_websockets: Dict[str, List[WebSocket]] = {}

# ==================== Pydantic Models ====================

class Message(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    query: str
    user_id: str
    use_web_search: bool = True
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    request_id: str
    status: str
    answer: Optional[str] = None
    timestamp: str
    processing_time: Optional[float] = None

class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: str

class ConversationHistory(BaseModel):
    user_id: str
    messages: List[ConversationMessage]
    total_messages: int

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    embeddings_loaded: bool
    embeddings_count: int

class ErrorResponse(BaseModel):
    error: str
    status_code: int
    timestamp: str
    request_id: Optional[str] = None

# ==================== Utility Functions ====================

def clean_response(text):
    """Remove code block markers and clean the response."""
    if not text:
        return text
    
    text = re.sub(r'```[\w]*\n?', '', text)
    text = re.sub(r'```\n?$', '', text)
    text = text.strip('`')
    text = text.strip()
    
    return text

def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"

async def process_query_sync(query: str, user_id: str, use_web_search: bool) -> tuple[str, float]:
    """Process query synchronously and return answer with processing time."""
    import time
    start_time = time.time()
    
    try:
        history = conversation_store.get(user_id, [])
        chunks, embeddings = load_embeddings(EMBEDDINGS_FILE)
        
        query_embedding = get_query_embedding(query)
        context = retrieve_relevant_chunks(query_embedding, embeddings, chunks, top_k=3)
        web_search_context = web_search(query) if use_web_search else ""
        
        formatted_messages = [{
            "role": "system",
            "content": (
                f"RAG Context:\n{context}\n\n"
                f"Web_Search_Context: {web_search_context}\n\n"
                """You are a helpful chatbot for GYWS queries. Your response should be clean HTML content styled with Tailwind CSS.

                IMPORTANT FORMATTING RULES:
                - Do NOT wrap your response in code blocks (```html or ```)
                - Provide clean HTML content directly without any markdown formatting
                - Use Tailwind CSS classes for styling
                - Keep the content well-structured and readable
                - Use appropriate HTML tags like <p>, <ul>, <li>, <strong>, <em> etc.

                CONTENT RULES:
                - Answer user queries directly and concisely
                - If a user's query contains "mrinal da" (case-insensitive), respond only with: "ask other question"
                - Focus on GYWS and IIT Kharagpur related information
                - Do not reveal internal processing steps"""
            )
        }]
        
        for msg in history:
            formatted_messages.append({"role": msg["role"], "content": msg["content"]})
        formatted_messages.append({"role": "user", "content": query})
        
        raw_answer = generate_answer(formatted_messages)
        cleaned_answer = clean_response(raw_answer)
        
        history.append({"role": "user", "content": query, "timestamp": get_timestamp()})
        history.append({"role": "assistant", "content": cleaned_answer, "timestamp": get_timestamp()})
        conversation_store[user_id] = history
        
        processing_time = time.time() - start_time
        return cleaned_answer, processing_time
        
    except Exception as e:
        raise Exception(f"Error processing query: {str(e)}")

def web_search(query):
    """Perform a web search using the Serper API."""
    try:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": f"{query} in the context of GYWS, IIT Kharagpur"})
        headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        return response.text if response.status_code == 200 else ""
    except Exception as e:
        print(f"Web search error: {e}")
        return ""

# ==================== API Endpoints ====================

@app.get("/", tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint with service status."""
    try:
        chunks, embeddings = load_embeddings(EMBEDDINGS_FILE)
        embeddings_count = len(chunks) if chunks else 0
        embeddings_loaded = embeddings_count > 0
    except:
        embeddings_loaded = False
        embeddings_count = 0
    
    return HealthResponse(
        status="healthy",
        service="GYWS Chatbot API",
        version="2.0.0",
        embeddings_loaded=embeddings_loaded,
        embeddings_count=embeddings_count
    )

@app.post("/v1/query", response_model=QueryResponse, tags=["Query"])
async def query_sync(request: QueryRequest) -> QueryResponse:
    """
    Process a query synchronously and return the answer immediately.
    Perfect for service-to-service integration.
    
    **Request Body:**
    - `query`: The user's question
    - `user_id`: Unique user identifier for conversation history
    - `use_web_search`: Enable/disable web search (default: true)
    - `session_id`: Optional session identifier for tracking
    """
    request_id = str(uuid.uuid4())
    
    try:
        answer, processing_time = await process_query_sync(
            request.query, 
            request.user_id, 
            request.use_web_search
        )
        
        return QueryResponse(
            request_id=request_id,
            status="success",
            answer=answer,
            timestamp=get_timestamp(),
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "request_id": request_id,
                "timestamp": get_timestamp()
            }
        )

@app.post("/v1/query/batch", tags=["Query"])
async def batch_query(queries: List[QueryRequest]) -> List[QueryResponse]:
    """
    Process multiple queries in batch.
    Useful for bulk processing.
    """
    results = []
    for req in queries:
        try:
            answer, processing_time = await process_query_sync(
                req.query,
                req.user_id,
                req.use_web_search
            )
            results.append(QueryResponse(
                request_id=str(uuid.uuid4()),
                status="success",
                answer=answer,
                timestamp=get_timestamp(),
                processing_time=processing_time
            ))
        except Exception as e:
            results.append(QueryResponse(
                request_id=str(uuid.uuid4()),
                status="error",
                answer=str(e),
                timestamp=get_timestamp()
            ))
    return results

@app.websocket("/ws/query/{user_id}")
async def websocket_query(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time query processing.
    Allows streaming responses and real-time communication.
    
    Send: {"query": "your question", "use_web_search": true}
    """
    await websocket.accept()
    
    if user_id not in active_websockets:
        active_websockets[user_id] = []
    active_websockets[user_id].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)
            query = request_data.get("query")
            use_web_search = request_data.get("use_web_search", True)
            
            if not query:
                await websocket.send_json({"error": "Query is required"})
                continue
            
            try:
                answer, processing_time = await process_query_sync(query, user_id, use_web_search)
                await websocket.send_json({
                    "status": "success",
                    "answer": answer,
                    "processing_time": processing_time,
                    "timestamp": get_timestamp()
                })
            except Exception as e:
                await websocket.send_json({
                    "status": "error",
                    "error": str(e),
                    "timestamp": get_timestamp()
                })
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_websockets[user_id].remove(websocket)
        if not active_websockets[user_id]:
            del active_websockets[user_id]

@app.get("/v1/conversation/{user_id}", response_model=ConversationHistory, tags=["Conversation"])
async def get_conversation(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
) -> ConversationHistory:
    """
    Retrieve conversation history for a user with pagination.
    
    **Parameters:**
    - `user_id`: Unique user identifier
    - `skip`: Number of messages to skip (pagination)
    - `limit`: Maximum number of messages to return
    """
    history = conversation_store.get(user_id, [])
    
    messages = [
        ConversationMessage(
            role=msg.get("role"),
            content=msg.get("content"),
            timestamp=msg.get("timestamp", get_timestamp())
        )
        for msg in history[skip:skip + limit]
    ]
    
    return ConversationHistory(
        user_id=user_id,
        messages=messages,
        total_messages=len(history)
    )

@app.delete("/v1/conversation/{user_id}", tags=["Conversation"])
async def clear_conversation(user_id: str):
    """Clear all conversation history for a user."""
    if user_id in conversation_store:
        conversation_store[user_id] = []
    
    return {
        "message": "Conversation cleared",
        "user_id": user_id,
        "timestamp": get_timestamp()
    }

@app.post("/v1/conversation/{user_id}/message", tags=["Conversation"])
async def add_message(user_id: str, message: Message):
    """
    Manually add a message to conversation history.
    Useful for integrating external messages.
    """
    if user_id not in conversation_store:
        conversation_store[user_id] = []
    
    conversation_store[user_id].append({
        "role": message.role,
        "content": message.content,
        "timestamp": get_timestamp()
    })
    
    return {
        "message": "Message added",
        "user_id": user_id,
        "timestamp": get_timestamp()
    }

@app.get("/v1/status", tags=["Service"])
async def service_status():
    """Get detailed service status including active users and conversations."""
    return {
        "service": "GYWS Chatbot API",
        "status": "operational",
        "active_users": len(conversation_store),
        "total_conversations": sum(len(v) for v in conversation_store.values()),
        "active_websockets": sum(len(v) for v in active_websockets.values()),
        "timestamp": get_timestamp()
    }

@app.get("/v1/embeddings/info", tags=["Service"])
async def embeddings_info():
    """Get information about loaded embeddings."""
    try:
        chunks, embeddings = load_embeddings(EMBEDDINGS_FILE)
        return {
            "status": "loaded",
            "chunks_count": len(chunks),
            "embedding_dimension": len(embeddings[0]) if embeddings else 0,
            "file": EMBEDDINGS_FILE,
            "timestamp": get_timestamp()
        }
    except Exception as e:
        return {
            "status": "not_loaded",
            "error": str(e),
            "timestamp": get_timestamp()
        }

# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            status_code=exc.status_code,
            timestamp=get_timestamp()
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=str(exc),
            status_code=500,
            timestamp=get_timestamp()
        ).dict()
    )

# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Chatbot API Server v2.0...")
    print("📊 Checking embeddings file...")
    
    if os.path.exists(EMBEDDINGS_FILE):
        chunks, embeddings = load_embeddings(EMBEDDINGS_FILE)
        print(f"✅ Loaded {len(chunks)} chunks from embeddings file")
    else:
        print("❌ No embeddings file found. Please run 'python index.py' first!")
    
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Server will start on http://localhost:{port}")
    print(f"📚 API Documentation available at: http://localhost:{port}/docs")
    print("🔄 Starting server...")
    
    uvicorn.run(app, host="0.0.0.0", port=port)