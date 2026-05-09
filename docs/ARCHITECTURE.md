# GYWS Chatbot API - Architecture & Integration Guide

## Architecture Overview

### System Design
```
┌─────────────────────────────────────────────────────────┐
│                    Client Applications                   │
│     (Web Frontend, Mobile, Other Services)               │
└────────────────┬──────────────────────────────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
  HTTP/REST   WebSocket   Batch API
     │           │           │
┌────┴───────────┴───────────┴────────────────────────────┐
│              FastAPI Application (main.py)              │
│                                                         │
│  ├─ /v1/query        (Synchronous - Main Endpoint)    │
│  ├─ /v1/query/batch  (Batch Processing)               │
│  ├─ /ws/query/{id}   (WebSocket - Real-time)          │
│  ├─ /v1/conversation (History Management)             │
│  ├─ /v1/status       (Service Monitoring)             │
│  └─ /docs            (API Documentation)              │
└────┬──────────────────────────────────────────────────┬─┘
     │                                                  │
     └──────────────────┬───────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    ┌───▼────┐    ┌─────▼─────┐  ┌─────▼────┐
    │  Utils │    │ Embeddings│  │   LLM    │
    │ Module │    │   (RAG)   │  │ (Gemini) │
    └────────┘    └───────────┘  └──────────┘
        │               │              │
        └───────────────┼──────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    ┌───▼────────┐ ┌───▼──────┐  ┌──────▼────┐
    │  PDF Text  │ │Embeddings│  │ Web Search│
    │ Processing │ │ Storage  │  │  (Serper) │
    └────────────┘ └──────────┘  └───────────┘
```

## Improved API Design

### Why v2.0 API is Better for Service Integration

#### Problem with v1.0 (Old)
```
POST /query/  → Returns request_id
     ↓
GET /status/{request_id}  → Poll repeatedly
     ↓
GET /result/{request_id}/{user_id}  → Get answer
```
**Issues:**
- Requires polling (inefficient)
- 3 separate API calls
- Coupling between endpoints
- Difficult to monitor

#### Solution in v2.0 (New)
```
POST /v1/query  → Returns answer directly
```
**Benefits:**
- Single synchronous call
- Immediate response
- Decoupled operations
- Easy to integrate

---

## API Usage Patterns

### Pattern 1: Simple Query (Recommended)
**Best for:** Web applications, chatbots, direct user interaction

```python
# Single synchronous request
response = requests.post(
    "http://api:8000/v1/query",
    json={
        "query": "What is GYWS?",
        "user_id": "user123",
        "use_web_search": True
    }
)
answer = response.json()["answer"]
```

### Pattern 2: Batch Processing
**Best for:** Bulk operations, data processing, reports

```python
queries = [
    {"query": "Q1", "user_id": "u1", "use_web_search": True},
    {"query": "Q2", "user_id": "u2", "use_web_search": False},
    # ... more queries
]

response = requests.post(
    "http://api:8000/v1/query/batch",
    json=queries
)

for result in response.json():
    print(result["answer"])
    print(f"Time: {result['processing_time']}s")
```

### Pattern 3: Real-time WebSocket
**Best for:** Chat applications, live updates, streaming

```javascript
const ws = new WebSocket("ws://api:8000/ws/query/user123");

ws.onmessage = (event) => {
  const { status, answer, processing_time } = JSON.parse(event.data);
  updateUI(answer);
  console.log(`Processed in ${processing_time}s`);
};

ws.send(JSON.stringify({ query: "...", use_web_search: true }));
```

### Pattern 4: Conversation Management
**Best for:** Multi-turn conversations, context preservation

```python
# Get conversation history
history = requests.get(
    f"http://api:8000/v1/conversation/user123?limit=20"
).json()

# Process new query (automatically added to history)
response = requests.post(
    "http://api:8000/v1/query",
    json={"query": "...", "user_id": "user123"}
)

# Clear when done
requests.delete(f"http://api:8000/v1/conversation/user123")
```

---

## Integration Scenarios

### Scenario 1: Web Frontend Integration
```
┌──────────────┐
│ React/Vue.js │
└──────┬───────┘
       │ fetch("/v1/query")
       ↓
┌──────────────────┐
│ Chatbot API      │
│ (FastAPI)        │
└──────┬───────────┘
       │ JSON response with answer
       ↓
┌──────────────────┐
│ Display HTML     │
│ (Tailwind CSS)   │
└──────────────────┘
```

**Implementation:**
```javascript
async function sendQuery(query, userId) {
  const response = await fetch('/v1/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      user_id: userId,
      use_web_search: true
    })
  });
  
  const { answer, processing_time, status } = await response.json();
  
  if (status === 'success') {
    document.getElementById('answer').innerHTML = answer;
    document.getElementById('time').textContent = `${processing_time.toFixed(2)}s`;
  }
}
```

### Scenario 2: Microservices Integration
```
┌─────────────────────────────────────┐
│ Main Application                    │
│                                     │
│ ┌──────────────┐   ┌──────────────┐│
│ │ User Service │──▶│Query Handler ││
│ └──────────────┘   └────────┬─────┘│
└────────────────────────────┬────────┘
                             │ HTTP POST /v1/query
                             ↓
                    ┌──────────────────┐
                    │ Chatbot API      │
                    │ (FastAPI)        │
                    └──────────────────┘
```

**Implementation:**
```python
from typing import Dict
import httpx

class ChatbotService:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
    
    async def ask(self, query: str, user_id: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/v1/query",
                json={
                    "query": query,
                    "user_id": user_id,
                    "use_web_search": True
                }
            )
            return response.json()
```

### Scenario 3: Monitoring & Analytics
```
┌──────────────────┐
│ Chatbot API      │
│ (with metrics)   │
└────────┬─────────┘
         │
    ┌────┴─────────────────┐
    │                      │
    ▼                      ▼
┌─────────────┐  ┌──────────────────┐
│ Prometheus  │  │ ELK Stack / Logs │
│ (Metrics)   │  │ (Tracing)        │
└─────────────┘  └──────────────────┘
    │                      │
    └────────┬─────────────┘
             ▼
    ┌──────────────────┐
    │ Dashboard        │
    │ (Grafana)        │
    └──────────────────┘
```

**Metrics to Track:**
- Response time per query
- Active users
- Error rate
- Web search usage
- Embedding cache hits

### Scenario 4: Load Balancing
```
┌────────────────────────────────────┐
│ Load Balancer (Nginx/HAProxy)      │
└──────────┬───────────────┬─────────┘
           │               │
    ┌──────▼──────┐  ┌─────▼──────┐
    │ API Instance 1   │ API Instance 2   │
    └──────┬──────┘  └─────┬──────┘
           │               │
           └───────┬───────┘
                   │ Shared Embeddings
                   ▼
           ┌────────────────┐
           │ Embeddings DB  │
           └────────────────┘
```

---

## Configuration for Production

### Environment Variables
```env
# API Configuration
GEMINI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
PORT=8000

# Optional: for database integration
DATABASE_URL=postgresql://user:pass@host/db
REDIS_URL=redis://host:6379

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/chatbot-api.log

# Performance
MAX_WORKERS=4
REQUEST_TIMEOUT=30
```

### Running Multiple Workers
```bash
# Production setup with 4 workers
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --loop uvloop \
  --http httptools
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Error Handling & Resilience

### Standard Error Response
```json
{
  "error": "Error description",
  "status_code": 500,
  "timestamp": "2026-05-10T10:30:45.123456Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Recommended Client-Side Handling
```python
import time
from typing import Optional

def query_with_retry(
    query: str,
    user_id: str,
    max_retries: int = 3,
    backoff_factor: float = 1.0
) -> Optional[str]:
    """Query with exponential backoff retry logic."""
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "http://api:8000/v1/query",
                json={"query": query, "user_id": user_id},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["answer"]
            elif response.status_code == 429:  # Rate limit
                wait_time = backoff_factor ** attempt
                time.sleep(wait_time)
            else:
                return None
                
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = backoff_factor ** attempt
            time.sleep(wait_time)
    
    return None
```

---

## Performance Optimization

### 1. Connection Pooling
```python
import httpx

# Reuse connection pool
client = httpx.Client(base_url="http://api:8000")

# Multiple requests use same connections
for i in range(100):
    response = client.post("/v1/query", json=data)
```

### 2. Request Caching
```python
from functools import lru_cache
from hashlib import md5

@lru_cache(maxsize=1000)
def cached_query(query_hash: str) -> str:
    """Cache responses for identical queries."""
    pass

query_hash = md5(query.encode()).hexdigest()
```

### 3. Batch Operations
```python
# Instead of 100 individual requests
queries = [{"query": q, "user_id": f"u{i}"} for i, q in enumerate(queries)]
responses = requests.post("/v1/query/batch", json=queries)
```

---

## Monitoring & Debugging

### Health Check Implementation
```python
import requests
from datetime import datetime

def health_check():
    """Monitor API health."""
    try:
        response = requests.get("http://api:8000/", timeout=5)
        data = response.json()
        
        print(f"✅ Status: {data['status']}")
        print(f"📊 Embeddings: {data['embeddings_count']} chunks")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

# Run periodically
while True:
    health_check()
    time.sleep(60)
```

### Service Status Monitoring
```python
response = requests.get("http://api:8000/v1/status")
status = response.json()

print(f"Active Users: {status['active_users']}")
print(f"Total Conversations: {status['total_conversations']}")
print(f"WebSocket Connections: {status['active_websockets']}")
```

---

## Migration from v1.0 to v2.0

### Breaking Changes
| v1.0 | v2.0 | Migration |
|------|------|-----------|
| `POST /query/` returns `request_id` | `POST /v1/query` returns answer directly | Remove polling logic |
| `GET /status/{request_id}` | `GET /v1/status` (service-wide) | Update monitoring |
| `GET /result/{request_id}/{user_id}` | Included in `/v1/query` response | Simplify retrieval |

### Migration Example
```python
# Old v1.0 code
request_id = requests.post("/query/", json=data).json()["request_id"]
while True:
    status = requests.get(f"/status/{request_id}").json()
    if status["completed"]:
        result = requests.get(f"/result/{request_id}/{user_id}").json()
        break

# New v2.0 code
result = requests.post("/v1/query", json=data).json()
answer = result["answer"]
```

---

## Support & Documentation

- **API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Source Code**: See `main.py`
- **Configuration**: Update `.env` file

**Version**: 2.0.0 (May 2026)
