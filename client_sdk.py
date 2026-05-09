"""
GYWS Chatbot API - Python Client SDK
Easy-to-use Python client for integrating with the Chatbot API
"""

from typing import Optional, List, Dict
import httpx
import asyncio
from datetime import datetime
from dataclasses import dataclass


@dataclass
class QueryResponse:
    """Response from a query operation"""
    request_id: str
    status: str
    answer: Optional[str] = None
    timestamp: str = ""
    processing_time: Optional[float] = None
    
    def __repr__(self):
        return f"QueryResponse(status={self.status}, time={self.processing_time}s)"


@dataclass
class ConversationMessage:
    """Message in conversation history"""
    role: str
    content: str
    timestamp: str


class ChatbotAPIClient:
    """
    Synchronous client for GYWS Chatbot API
    
    Example:
        client = ChatbotAPIClient("http://localhost:8000")
        response = client.query("What is GYWS?", "user123")
        print(response.answer)
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client
        
        Args:
            base_url: Base URL of the API (default: http://localhost:8000)
        """
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)
    
    def health_check(self) -> Dict:
        """Check API health status
        
        Returns:
            dict: Health status including embeddings info
        """
        response = self.client.get("/")
        response.raise_for_status()
        return response.json()
    
    def query(
        self,
        query: str,
        user_id: str,
        use_web_search: bool = True,
        session_id: Optional[str] = None
    ) -> QueryResponse:
        """Send a query to the API
        
        Args:
            query: The user's question
            user_id: Unique user identifier
            use_web_search: Enable web search (default: True)
            session_id: Optional session identifier
        
        Returns:
            QueryResponse: API response with answer
        
        Raises:
            httpx.HTTPError: If request fails
        """
        payload = {
            "query": query,
            "user_id": user_id,
            "use_web_search": use_web_search,
        }
        if session_id:
            payload["session_id"] = session_id
        
        response = self.client.post("/v1/query", json=payload)
        response.raise_for_status()
        data = response.json()
        
        return QueryResponse(
            request_id=data["request_id"],
            status=data["status"],
            answer=data.get("answer"),
            timestamp=data["timestamp"],
            processing_time=data.get("processing_time")
        )
    
    def batch_query(self, queries: List[Dict]) -> List[QueryResponse]:
        """Process multiple queries at once
        
        Args:
            queries: List of query dictionaries with 'query', 'user_id', etc.
        
        Returns:
            list: List of QueryResponse objects
        """
        response = self.client.post("/v1/query/batch", json=queries)
        response.raise_for_status()
        data = response.json()
        
        return [
            QueryResponse(
                request_id=item["request_id"],
                status=item["status"],
                answer=item.get("answer"),
                timestamp=item["timestamp"],
                processing_time=item.get("processing_time")
            )
            for item in data
        ]
    
    def get_conversation(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10
    ) -> Dict:
        """Get conversation history for a user
        
        Args:
            user_id: User identifier
            skip: Number of messages to skip
            limit: Maximum messages to return
        
        Returns:
            dict: Conversation history with metadata
        """
        response = self.client.get(
            f"/v1/conversation/{user_id}",
            params={"skip": skip, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    
    def add_message(self, user_id: str, role: str, content: str) -> Dict:
        """Manually add a message to conversation history
        
        Args:
            user_id: User identifier
            role: Message role ("user" or "assistant")
            content: Message content
        
        Returns:
            dict: Confirmation response
        """
        response = self.client.post(
            f"/v1/conversation/{user_id}/message",
            json={"role": role, "content": content}
        )
        response.raise_for_status()
        return response.json()
    
    def clear_conversation(self, user_id: str) -> Dict:
        """Clear conversation history for a user
        
        Args:
            user_id: User identifier
        
        Returns:
            dict: Confirmation response
        """
        response = self.client.delete(f"/v1/conversation/{user_id}")
        response.raise_for_status()
        return response.json()
    
    def get_service_status(self) -> Dict:
        """Get detailed service status
        
        Returns:
            dict: Service status including active users and connections
        """
        response = self.client.get("/v1/status")
        response.raise_for_status()
        return response.json()
    
    def get_embeddings_info(self) -> Dict:
        """Get information about loaded embeddings
        
        Returns:
            dict: Embeddings metadata
        """
        response = self.client.get("/v1/embeddings/info")
        response.raise_for_status()
        return response.json()
    
    def close(self):
        """Close the HTTP client"""
        self.client.close()
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.close()


class AsyncChatbotAPIClient:
    """
    Asynchronous client for GYWS Chatbot API
    
    Example:
        async with AsyncChatbotAPIClient("http://localhost:8000") as client:
            response = await client.query("What is GYWS?", "user123")
            print(response.answer)
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the async client
        
        Args:
            base_url: Base URL of the API (default: http://localhost:8000)
        """
        self.base_url = base_url.rstrip("/")
        self.client: Optional[httpx.AsyncClient] = None
    
    async def _ensure_client(self):
        """Ensure async client is initialized"""
        if self.client is None:
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0
            )
    
    async def health_check(self) -> Dict:
        """Check API health status"""
        await self._ensure_client()
        response = await self.client.get("/")
        response.raise_for_status()
        return response.json()
    
    async def query(
        self,
        query: str,
        user_id: str,
        use_web_search: bool = True,
        session_id: Optional[str] = None
    ) -> QueryResponse:
        """Send a query to the API (async)"""
        await self._ensure_client()
        
        payload = {
            "query": query,
            "user_id": user_id,
            "use_web_search": use_web_search,
        }
        if session_id:
            payload["session_id"] = session_id
        
        response = await self.client.post("/v1/query", json=payload)
        response.raise_for_status()
        data = response.json()
        
        return QueryResponse(
            request_id=data["request_id"],
            status=data["status"],
            answer=data.get("answer"),
            timestamp=data["timestamp"],
            processing_time=data.get("processing_time")
        )
    
    async def batch_query(self, queries: List[Dict]) -> List[QueryResponse]:
        """Process multiple queries asynchronously"""
        await self._ensure_client()
        
        response = await self.client.post("/v1/query/batch", json=queries)
        response.raise_for_status()
        data = response.json()
        
        return [
            QueryResponse(
                request_id=item["request_id"],
                status=item["status"],
                answer=item.get("answer"),
                timestamp=item["timestamp"],
                processing_time=item.get("processing_time")
            )
            for item in data
        ]
    
    async def get_conversation(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10
    ) -> Dict:
        """Get conversation history (async)"""
        await self._ensure_client()
        
        response = await self.client.get(
            f"/v1/conversation/{user_id}",
            params={"skip": skip, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    
    async def get_service_status(self) -> Dict:
        """Get service status (async)"""
        await self._ensure_client()
        
        response = await self.client.get("/v1/status")
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the async client"""
        if self.client:
            await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager support"""
        await self._ensure_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager cleanup"""
        await self.close()


# ==================== Example Usage ====================

if __name__ == "__main__":
    # Example 1: Synchronous query
    print("=" * 50)
    print("Example 1: Simple Synchronous Query")
    print("=" * 50)
    
    with ChatbotAPIClient() as client:
        # Health check
        health = client.health_check()
        print(f"✅ API Status: {health['status']}")
        print(f"📊 Embeddings loaded: {health['embeddings_count']} chunks\n")
        
        # Send query
        response = client.query(
            query="What is GYWS?",
            user_id="example_user",
            use_web_search=True
        )
        
        print(f"Status: {response.status}")
        print(f"Processing time: {response.processing_time}s")
        print(f"Answer: {response.answer[:100]}...\n")
    
    # Example 2: Batch processing
    print("=" * 50)
    print("Example 2: Batch Query Processing")
    print("=" * 50)
    
    with ChatbotAPIClient() as client:
        queries = [
            {"query": "What is GYWS?", "user_id": "user1", "use_web_search": True},
            {"query": "Tell me about IIT Kharagpur", "user_id": "user2", "use_web_search": False},
        ]
        
        responses = client.batch_query(queries)
        
        for i, resp in enumerate(responses):
            print(f"Query {i+1}: {resp.status} ({resp.processing_time}s)")
    
    # Example 3: Conversation history
    print("\n" + "=" * 50)
    print("Example 3: Conversation History")
    print("=" * 50)
    
    with ChatbotAPIClient() as client:
        # Get conversation
        history = client.get_conversation("example_user", limit=5)
        print(f"Messages: {history['total_messages']}")
        
        for msg in history["messages"]:
            print(f"  {msg['role']}: {msg['content'][:50]}...")
    
    # Example 4: Async usage
    print("\n" + "=" * 50)
    print("Example 4: Async Query Processing")
    print("=" * 50)
    
    async def async_example():
        async with AsyncChatbotAPIClient() as client:
            response = await client.query(
                "What is GYWS?",
                "async_user"
            )
            print(f"✅ Async Response: {response.status}")
            print(f"⏱️  Time: {response.processing_time}s")
    
    # Run async example
    asyncio.run(async_example())
    
    print("\n✅ All examples completed!")
