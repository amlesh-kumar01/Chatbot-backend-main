# GYWS Chatbot API - Quick Integration Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Choose Your Integration Method

#### Option A: Using Python Client SDK (Recommended)
```python
from client_sdk import ChatbotAPIClient

with ChatbotAPIClient("http://api-server:8000") as client:
    response = client.query("What is GYWS?", user_id="user123")
    print(response.answer)
```

#### Option B: Using HTTP Requests
```python
import requests

response = requests.post("http://api-server:8000/v1/query", json={
    "query": "What is GYWS?",
    "user_id": "user123",
    "use_web_search": True
})

answer = response.json()["answer"]
print(answer)
```

#### Option C: Using cURL
```bash
curl -X POST http://api-server:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is GYWS?",
    "user_id": "user123",
    "use_web_search": true
  }'
```

#### Option D: Using JavaScript/Fetch
```javascript
const response = await fetch("http://api-server:8000/v1/query", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "What is GYWS?",
    user_id: "user123",
    use_web_search: true
  })
});

const data = await response.json();
console.log(data.answer);
```

---

## 📋 Integration Scenarios

### Scenario 1: Web Chat Application

```html
<!-- HTML -->
<form id="queryForm">
  <input type="text" id="queryInput" placeholder="Ask about GYWS...">
  <button type="submit">Send</button>
</form>
<div id="response"></div>

<script>
// JavaScript
document.getElementById('queryForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const query = document.getElementById('queryInput').value;
  
  const response = await fetch("/api/v1/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: query,
      user_id: getCurrentUserId(),
      use_web_search: true
    })
  });
  
  const data = await response.json();
  document.getElementById('response').innerHTML = data.answer;
});
</script>
```

### Scenario 2: Python Flask Backend Integration

```python
from flask import Flask, request, jsonify
from client_sdk import ChatbotAPIClient

app = Flask(__name__)
chatbot = ChatbotAPIClient("http://localhost:8000")

@app.route("/chat/query", methods=["POST"])
def query():
    data = request.json
    
    try:
        response = chatbot.query(
            query=data["query"],
            user_id=data["user_id"],
            use_web_search=data.get("use_web_search", True)
        )
        
        return jsonify({
            "status": response.status,
            "answer": response.answer,
            "time": response.processing_time
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
```

### Scenario 3: Async FastAPI Integration

```python
from fastapi import FastAPI
from client_sdk import AsyncChatbotAPIClient

app = FastAPI()
chatbot = AsyncChatbotAPIClient("http://localhost:8000")

@app.post("/query")
async def process_query(query: str, user_id: str):
    response = await chatbot.query(query, user_id)
    return {
        "answer": response.answer,
        "processing_time": response.processing_time
    }
```

### Scenario 4: Microservice Communication

```python
import httpx
import asyncio

async def call_chatbot_service(query: str, user_id: str):
    """Call chatbot service from another microservice"""
    
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "http://chatbot-api:8000/v1/query",
            json={
                "query": query,
                "user_id": user_id,
                "use_web_search": True
            }
        )
        
        data = response.json()
        return data["answer"]

# Usage
answer = asyncio.run(call_chatbot_service("What is GYWS?", "user123"))
```

### Scenario 5: Batch Processing

```python
from client_sdk import ChatbotAPIClient

client = ChatbotAPIClient()

# Prepare batch of queries
queries = [
    {"query": "What is GYWS?", "user_id": "user1", "use_web_search": True},
    {"query": "Tell me about events", "user_id": "user2", "use_web_search": True},
    {"query": "How to join?", "user_id": "user3", "use_web_search": False},
]

# Process in bulk
responses = client.batch_query(queries)

# Handle responses
for resp in responses:
    if resp.status == "success":
        print(f"✅ Answer: {resp.answer[:100]}...")
    else:
        print(f"❌ Error: {resp.answer}")
```

### Scenario 6: Conversation Context

```python
from client_sdk import ChatbotAPIClient

client = ChatbotAPIClient()
user_id = "user123"

# First query
q1 = client.query("What is GYWS?", user_id)
print(f"Q1: {q1.answer[:100]}...")

# Follow-up query (context is preserved)
q2 = client.query("What are their activities?", user_id)
print(f"Q2: {q2.answer[:100]}...")

# Get full conversation
history = client.get_conversation(user_id)
print(f"Total messages: {history['total_messages']}")

for msg in history['messages']:
    print(f"{msg['role']}: {msg['content']}")

# Clear when done
client.clear_conversation(user_id)
```

---

## 🔧 Configuration by Use Case

### Development (Local)
```python
client = ChatbotAPIClient("http://localhost:8000")
```

### Staging
```python
client = ChatbotAPIClient("http://staging-api.example.com:8000")
```

### Production
```python
import os
api_url = os.getenv("CHATBOT_API_URL", "http://localhost:8000")
client = ChatbotAPIClient(api_url)
```

### With Authentication (Future)
```python
import httpx

client = httpx.Client(
    base_url="http://api-server:8000",
    headers={"Authorization": f"Bearer {token}"}
)

response = client.post("/v1/query", json=data)
```

---

## 📊 Error Handling

### Basic Error Handling
```python
from client_sdk import ChatbotAPIClient

client = ChatbotAPIClient()

try:
    response = client.query("What is GYWS?", "user123")
    if response.status == "success":
        print(response.answer)
    else:
        print(f"API Error: {response.answer}")
except httpx.HTTPError as e:
    print(f"Connection Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

### Retry Logic
```python
import time
from client_sdk import ChatbotAPIClient

def query_with_retry(query: str, user_id: str, max_retries: int = 3):
    client = ChatbotAPIClient()
    
    for attempt in range(max_retries):
        try:
            return client.query(query, user_id)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
            time.sleep(wait_time)

response = query_with_retry("What is GYWS?", "user123")
```

---

## 📈 Performance Tips

### 1. Connection Pooling
```python
# Good: Reuse client connection
client = ChatbotAPIClient()
for i in range(100):
    response = client.query(f"Query {i}", f"user{i}")

# Bad: Creating new client each time
for i in range(100):
    client = ChatbotAPIClient()  # ❌ Don't do this
    response = client.query(f"Query {i}", f"user{i}")
```

### 2. Async for High Concurrency
```python
from client_sdk import AsyncChatbotAPIClient
import asyncio

async def process_many():
    async with AsyncChatbotAPIClient() as client:
        tasks = [
            client.query(f"Query {i}", f"user{i}")
            for i in range(100)
        ]
        responses = await asyncio.gather(*tasks)
        return responses
```

### 3. Batch Processing for Multiple Queries
```python
# Efficient: Single batch request
queries = [{"query": f"Q{i}", "user_id": f"u{i}"} for i in range(50)]
responses = client.batch_query(queries)

# Less efficient: 50 individual requests
for i in range(50):
    client.query(f"Q{i}", f"u{i}")
```

### 4. Response Caching
```python
from functools import lru_cache
from client_sdk import ChatbotAPIClient

class CachedChatbot:
    def __init__(self):
        self.client = ChatbotAPIClient()
        self.cache = {}
    
    def query(self, query: str, user_id: str):
        cache_key = f"{user_id}:{query}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = self.client.query(query, user_id)
        self.cache[cache_key] = response
        return response
```

---

## 🧪 Testing

### Unit Test Example
```python
import pytest
from client_sdk import ChatbotAPIClient

@pytest.fixture
def client():
    return ChatbotAPIClient("http://localhost:8000")

def test_query(client):
    response = client.query("What is GYWS?", "test_user")
    
    assert response.status == "success"
    assert response.answer is not None
    assert response.processing_time > 0

def test_batch_query(client):
    queries = [
        {"query": "Q1", "user_id": "u1"},
        {"query": "Q2", "user_id": "u2"}
    ]
    
    responses = client.batch_query(queries)
    
    assert len(responses) == 2
    assert all(r.status == "success" for r in responses)
```

### Integration Test Example
```python
def test_conversation_flow(client):
    user_id = "test_user"
    
    # First query
    q1 = client.query("What is GYWS?", user_id)
    assert q1.status == "success"
    
    # Second query
    q2 = client.query("Tell me more", user_id)
    assert q2.status == "success"
    
    # Check history
    history = client.get_conversation(user_id)
    assert history['total_messages'] >= 4  # 2 user + 2 assistant
    
    # Cleanup
    client.clear_conversation(user_id)
```

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Connection refused | Check if API is running on correct host:port |
| Timeout errors | Increase timeout: `ChatbotAPIClient(timeout=60)` |
| Embeddings not loaded | Run `python index.py` to generate embeddings |
| Rate limiting | Use batch processing instead of individual calls |
| Memory issues | Use async client for high concurrency |

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Architecture Guide**: See `ARCHITECTURE.md`
- **Client SDK**: See `client_sdk.py`
- **Main API Code**: See `main.py`
- **Utils**: See `utils.py`

---

## 🎯 Best Practices Checklist

- ✅ Use `ChatbotAPIClient` context manager for proper cleanup
- ✅ Implement retry logic for production deployments
- ✅ Cache responses for frequently asked questions
- ✅ Monitor API health with `/` endpoint
- ✅ Use async client for high-concurrency scenarios
- ✅ Implement proper error handling
- ✅ Log all API calls for debugging
- ✅ Test API integration before deployment
- ✅ Keep API keys in environment variables
- ✅ Monitor processing time metrics

---

**Version**: 2.0.0 (May 2026)

For support or questions, refer to the main README.md or check the API documentation at `/docs`.
