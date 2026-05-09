import PyPDF2
import numpy as np
import google.generativeai as genai
import re
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")
genai.configure(api_key=GEMINI_API_KEY)

# Retry configuration for rate limiting
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def chunk_text(text, chunk_size=50):
    """Split text into chunks of specified word size."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def get_embeddings(texts):
    """Generate embeddings for a list of texts using Gemini API with retry logic."""
    embeddings = []
    for text in texts:
        embedding = _get_embedding_with_retry(text, task_type="retrieval_document")
        embeddings.append(embedding)
    return embeddings


def _get_embedding_with_retry(text, task_type="retrieval_document"):
    """Get embedding with exponential backoff retry logic for rate limiting."""
    for attempt in range(MAX_RETRIES):
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type=task_type
            )
            return result['embedding']
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a rate limit error (429)
            if "429" in error_msg or "RATE_LIMIT_EXCEEDED" in error_msg:
                if attempt < MAX_RETRIES - 1:
                    retry_delay = INITIAL_RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    print(f"Rate limited. Retrying in {retry_delay}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"⚠️ Rate limit exceeded after {MAX_RETRIES} retries. Using fallback vector.")
                    return [0.0] * 768  # text-embedding-004 uses 768 dimensions
            
            # For other errors, log and return fallback
            print(f"Error generating embedding: {e}")
            return [0.0] * 768

def load_embeddings(npy_file):
    """Load chunks and embeddings from an NPY file."""
    try:
        data = np.load(npy_file, allow_pickle=True).item()
        return data["chunks"], data["embeddings"]
    except (FileNotFoundError, ValueError):
        return [], []

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors, handling zero norms."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    # Handle zero vectors (avoid division by zero)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return np.dot(a, b) / (norm_a * norm_b)

def get_query_embedding(query):
    """Generate embedding for a single query text with retry logic."""
    return _get_embedding_with_retry(query, task_type="retrieval_query")

def retrieve_relevant_chunks(query_emb, embeddings, chunks, top_k=3):
    """Retrieve top-k relevant chunks based on query embedding."""
    if not embeddings or not chunks:
        return "No document context available."
    similarities = [cosine_similarity(query_emb, emb) for emb in embeddings]
    indices = np.argsort(similarities)[-top_k:][::-1]
    retrieved = [chunks[i] for i in indices]
    return "\n".join(retrieved)

def clean_html_response(text):
    """Clean and validate HTML response."""
    if not text:
        return text
    
    # Remove any markdown code block syntax
    text = re.sub(r'```[\w]*\n?', '', text)
    text = re.sub(r'```\n?$', '', text)
    
    # Remove any remaining backticks
    text = text.strip('`')
    
    # Clean up extra whitespace but preserve HTML structure
    text = text.strip()
    
    return text

def generate_answer(messages, model="gemini-1.5-flash"):
    """Generate an answer using the Gemini chat API with retry logic for rate limiting."""
    
    for attempt in range(MAX_RETRIES):
        try:
            # Convert messages format to work with Gemini
            gemini_model = genai.GenerativeModel(
                model_name=model,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            # Extract system prompt and conversation history
            system_prompt = ""
            conversation_history = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                elif msg["role"] == "user":
                    conversation_history.append(f"User: {msg['content']}")
                elif msg["role"] == "assistant":
                    conversation_history.append(f"Assistant: {msg['content']}")
            
            # Combine system prompt with conversation
            full_prompt = f"{system_prompt}\n\nConversation:\n" + "\n".join(conversation_history)
            
            # Add explicit instruction to avoid code blocks
            full_prompt += "\n\nIMPORTANT: Respond with clean HTML content only. Do NOT use code blocks (```html) or any markdown formatting. Provide the HTML directly."
            
            response = gemini_model.generate_content(full_prompt)
            
            # Clean the response
            cleaned_response = clean_html_response(response.text)
            
            return cleaned_response
            
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a rate limit error (429)
            if "429" in error_msg or "RATE_LIMIT_EXCEEDED" in error_msg:
                if attempt < MAX_RETRIES - 1:
                    retry_delay = INITIAL_RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    print(f"⚠️ Rate limited. Retrying in {retry_delay}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"⚠️ Rate limit exceeded after {MAX_RETRIES} retries. Check your Gemini API quota.")
                    return '<div class="text-sm text-red-600"><p>⚠️ API quota exceeded. Please check your Google Gemini API quota and try again later.</p></div>'
            
            # For other errors, log and return error message
            print(f"Error generating answer: {e}")
            return f'<div class="text-sm text-red-600"><p>Error: {str(e)[:100]}</p></div>'