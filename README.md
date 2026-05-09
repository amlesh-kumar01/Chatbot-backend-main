# Chatbot Backend - GYWS Query Assistant

A modern, service-oriented FastAPI-based chatbot backend using Retrieval-Augmented Generation (RAG) and web search to provide intelligent answers about GYWS and IIT Kharagpur.

## 🎯 Key Features

- ⚡ **Synchronous API** - Get answers directly without polling
- 🚀 **Batch Processing** - Process multiple queries efficiently
- 🔄 **Real-time WebSocket** - Bidirectional streaming communication
- 📚 **RAG Integration** - Context-aware responses using document embeddings
- 🌐 **Web Search** - Real-time information retrieval
- 💾 **Conversation Memory** - Per-user conversation history with pagination
- 📊 **Service Monitoring** - Track active users and system status
- 🐍 **Python SDK** - Easy integration with built-in client library
- 📖 **Full Documentation** - Complete API docs with examples

## 📚 Documentation Guide

**Start here based on your role:**

| Role | Start With | Purpose |
|------|-----------|---------|
| **Quick Start** | [QUICKSTART.md](QUICKSTART.md) | Get server running in 3 minutes |
| **Developer** | [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | Code examples for your language |
| **Architect** | [ARCHITECTURE.md](ARCHITECTURE.md) | System design & patterns |
| **Upgrading** | [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md) | What's new in v2.0 |
| **API Details** | [API Section](#api-endpoints-v20---service-oriented) below | Full endpoint reference |
| **Python User** | [client_sdk.py](client_sdk.py) | Ready-to-use client library |

## 🚀 Quick Start

### 1. Install & Run (30 seconds)
```powershell
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test the API
```powershell
# Visit interactive docs:
http://localhost:8000/docs
```

### 3. First Query
```python
from client_sdk import ChatbotAPIClient

client = ChatbotAPIClient()
response = client.query("What is GYWS?", "user123")
print(response.answer)
```

📖 **Full setup guide:** [QUICKSTART.md](QUICKSTART.md)

## 🏗️ Architecture

The API v2.0 is built for service integration:

```
Client App → POST /v1/query → API (processes immediately) → Returns answer
                              ↓
                    (Conversation history)
                              ↓
                    (Performance metrics)
```

**Improvements from v1.0:**
- ✅ Single synchronous call vs. 3+ polling requests
- ✅ Direct answers vs. async with status polling
- ✅ Better error handling and standardized responses
- ✅ WebSocket support for real-time apps
- ✅ Batch processing for bulk operations

📖 **Full architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)

## 💻 Integration Examples

### Python
```python
import requests

response = requests.post("http://localhost:8000/v1/query", json={
    "query": "What is GYWS?",
    "user_id": "user123",
    "use_web_search": True
})

answer = response.json()["answer"]
```

### JavaScript
```javascript
const response = await fetch("http://localhost:8000/v1/query", {
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

### cURL
```bash
curl -X POST http://localhost:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is GYWS?",
    "user_id": "user123",
    "use_web_search": true
  }'
```

📖 **More examples:** [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **AI Models**: 
  - Google Generative AI (Gemini) - embeddings & text generation
  - Mistral AI - optional integration
- **Data**: NumPy, PyPDF2
- **APIs**: Serper (Google Search)

## Project Structure

```
Chatbot-backend-main/
├── main.py                 # ← FastAPI application (v2.0)
├── utils.py               # Utility functions for RAG
├── client_sdk.py          # ← Python client library (NEW)
├── requirements.txt       # Dependencies
├── .env                   # Configuration (secret)
├── .env.example          # Configuration template
├── .gitignore            # Git ignore rules
├── embeddings.npy        # Pre-generated embeddings
│
├── README.md             # This file
├── QUICKSTART.md         # ← Start here (NEW)
├── ARCHITECTURE.md       # System design (NEW)
├── INTEGRATION_GUIDE.md  # Code examples (NEW)
└── UPGRADE_SUMMARY.md    # v1→v2 changes (NEW)
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API Keys:
  - [Google Generative AI](https://makersuite.google.com/app/apikey)
  - [Serper API](https://serper.dev)

## Installation & Setup

### Step 1: Clone Repository

```bash
cd e:\PRODIGY\Chatbot-backend-main
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment

1. Your `.env` file already has API keys configured
2. Verify both keys are present:
   - `GEMINI_API_KEY`
   - `SERPER_API_KEY`

### Step 5: Prepare Embeddings

The app requires `embeddings.npy`. Make sure it exists in the project root.

If you need to generate it:
1. Use `index.py` (create if needed)
2. Run: `python index.py`

### Step 6: Run the Server

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Loaded 150 chunks from embeddings file
```

## How It Works

1. **User submits a query** with their unique user_id
2. **System generates embeddings** for the query
3. **Retrieves relevant chunks** from documents using RAG
4. **Optionally performs web search** for real-time information
5. **Generates answer** using Gemini API with context
6. **Returns clean HTML response** styled with Tailwind CSS
7. **Stores conversation history** for context awareness

## Configuration

### Environment Variables

Create `.env` file with:
```
GEMINI_API_KEY=your_api_key
SERPER_API_KEY=your_api_key
```

Use `.env.example` as template for team members.

### Server Settings

Edit `main.py` to modify:
- `EMBEDDINGS_FILE` - Path to embeddings (default: `embeddings.npy`)
- `PORT` - Server port (default: 8000)
- CORS settings - Currently allows all origins

## API Endpoints (v2.0 - Service-Oriented)

### Base URL
```
http://localhost:8000
```

### Health Check
```
GET /
```
Returns server status with embeddings information.

**Response:**
```json
{
  "status": "healthy",
  "service": "GYWS Chatbot API",
  "version": "2.0.0",
  "embeddings_loaded": true,
  "embeddings_count": 150
}
```

---

### Query (Synchronous - Recommended)
```
POST /v1/query
```
Process a query synchronously and get the answer immediately. **Perfect for service-to-service integration.**

**Request Body:**
```json
{
  "query": "What is GYWS?",
  "user_id": "user123",
  "use_web_search": true,
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "answer": "<div class=\"text-sm\"><p>GYWS is...</p></div>",
  "timestamp": "2026-05-10T10:30:45.123456Z",
  "processing_time": 2.34
}
```

**Status Codes:**
- `200`: Success
- `500`: Error (check `detail` field)

---

### Batch Query
```
POST /v1/query/batch
```
Process multiple queries in a single request.

**Request Body:**
```json
[
  {
    "query": "What is GYWS?",
    "user_id": "user123",
    "use_web_search": true
  },
  {
    "query": "Tell me about IIT Kharagpur",
    "user_id": "user124",
    "use_web_search": false
  }
]
```

**Response:**
```json
[
  {
    "request_id": "...",
    "status": "success",
    "answer": "<div>...</div>",
    "timestamp": "2026-05-10T10:30:45.123456Z",
    "processing_time": 2.34
  },
  // ... more results
]
```

---

### WebSocket (Real-time)
```
WebSocket /ws/query/{user_id}
```
Establish a WebSocket connection for real-time query processing.

**Connect:**
```javascript
const ws = new WebSocket("ws://localhost:8000/ws/query/user123");
```

**Send Query:**
```json
{
  "query": "What is GYWS?",
  "use_web_search": true
}
```

**Receive Response:**
```json
{
  "status": "success",
  "answer": "<div>...</div>",
  "processing_time": 2.34,
  "timestamp": "2026-05-10T10:30:45.123456Z"
}
```

---

### Get Conversation History
```
GET /v1/conversation/{user_id}?skip=0&limit=10
```
Retrieve conversation history with pagination.

**Query Parameters:**
- `skip`: Number of messages to skip (default: 0)
- `limit`: Number of messages to return (default: 10, max: 100)

**Response:**
```json
{
  "user_id": "user123",
  "messages": [
    {
      "role": "user",
      "content": "What is GYWS?",
      "timestamp": "2026-05-10T10:30:40.123456Z"
    },
    {
      "role": "assistant",
      "content": "<div>...</div>",
      "timestamp": "2026-05-10T10:30:45.123456Z"
    }
  ],
  "total_messages": 25
}
```

---

### Clear Conversation
```
DELETE /v1/conversation/{user_id}
```
Clear all conversation history for a user.

---

### Service Status
```
GET /v1/status
```
Get detailed service status.

**Response:**
```json
{
  "service": "GYWS Chatbot API",
  "status": "operational",
  "active_users": 42,
  "total_conversations": 156,
  "active_websockets": 5,
  "timestamp": "2026-05-10T10:30:45.123456Z"
}
```

---

### Embeddings Info
```
GET /v1/embeddings/info
```
Get information about loaded embeddings.

---

## Error Handling

### Standard Error Response
```json
{
  "error": "Error description",
  "status_code": 500,
  "timestamp": "2026-05-10T10:30:45.123456Z",
  "request_id": "optional-request-id"
}
```

---

## Common Issues & Solutions

### ModuleNotFoundError: No module named 'google'
**Solution**: Install google-generativeai
```powershell
pip install google-generativeai==0.6.0
```

### GEMINI_API_KEY not found
**Solution**: Create `.env` file with your API key (see Configuration section)

### embeddings.npy not found
**Solution**: Generate embeddings using `index.py` or place existing file in project root

### API returns 500 error
**Solution**: Check server logs for details. Common causes:
- Missing API keys in `.env`
- Embeddings file not found
- Network connectivity issues

---

## Deployment

### Development Setup
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Production Setup
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Security Notes

⚠️ **Important:**
- Never commit `.env` file (it's in `.gitignore`)
- Keep API keys private and secure
- Use `.env.example` as template for team members
- For production, use environment variable services

---

## Monitoring & Debugging

### Health Check
```bash
curl http://localhost:8000/
```

### Service Status
```bash
curl http://localhost:8000/v1/status
```

### Embeddings Info
```bash
curl http://localhost:8000/v1/embeddings/info
```

---

## License

All rights reserved. Proprietary project for GYWS/IIT Kharagpur.

---

## Support & Documentation

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Architecture Guide**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Integration Examples**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Upgrade Notes**: [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)

---

## Version History

- **v2.0.0** (May 2026): Redesigned API - Synchronous, batch processing, WebSocket support
- **v1.0.0** (Earlier): Initial release with async polling

---

**Last Updated**: May 10, 2026  
**Status**: Production Ready ✅

## Project Structure

```
Chatbot-backend-main/
├── main.py                 # FastAPI application and endpoints
├── utils.py               # Utility functions for embeddings and text processing
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── .env.example          # Template for environment variables
├── embeddings.npy        # Pre-generated embeddings file (not in repo)
└── README.md            # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (optional but recommended)

## Installation & Setup

### Step 1: Clone the Repository

```bash
cd e:\PRODIGY\Chatbot-backend-main
```

### Step 2: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file with your API keys:

```
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**How to get API keys:**

1. **Gemini API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy and paste into `.env`

2. **Serper API Key**:
   - Go to [Serper.dev](https://serper.dev)
   - Sign up and get your API key
   - Add to `.env`

### Step 5: Prepare Embeddings

The app requires a pre-generated embeddings file (`embeddings.npy`). If you don't have one:

1. Place your PDF files in the project directory
2. Create an `index.py` file to generate embeddings (or use an existing one)
3. Run: `python index.py` to generate `embeddings.npy`

## Running the Application

### Start the Server

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access Points

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/
- **API Base URL**: http://localhost:8000

## API Endpoints (v2.0 - Service-Oriented)

### Base URL
```
http://localhost:8000
```

### 1. Health Check
```
GET /
```
Returns server status with embeddings information.

**Response:**
```json
{
  "status": "healthy",
  "service": "GYWS Chatbot API",
  "version": "2.0.0",
  "embeddings_loaded": true,
  "embeddings_count": 150
}
```

---

### 2. Query (Synchronous - Recommended for Service Integration)
```
POST /v1/query
```
Process a query synchronously and get the answer immediately. Perfect for service-to-service integration.

**Request Body:**
```json
{
  "query": "What is GYWS?",
  "user_id": "user123",
  "use_web_search": true,
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "answer": "<div class=\"text-sm\"><p>GYWS is...</p></div>",
  "timestamp": "2026-05-10T10:30:45.123456Z",
  "processing_time": 2.34
}
```

**Status Codes:**
- `200`: Success
- `500`: Error (check `detail` field)

---

### 3. Batch Query
```
POST /v1/query/batch
```
Process multiple queries in a single request.

**Request Body:**
```json
[
  {
    "query": "What is GYWS?",
    "user_id": "user123",
    "use_web_search": true
  },
  {
    "query": "Tell me about IIT Kharagpur",
    "user_id": "user124",
    "use_web_search": false
  }
]
```

**Response:**
```json
[
  {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "success",
    "answer": "<div>...</div>",
    "timestamp": "2026-05-10T10:30:45.123456Z",
    "processing_time": 2.34
  },
  {
    "request_id": "550e8400-e29b-41d4-a716-446655440001",
    "status": "success",
    "answer": "<div>...</div>",
    "timestamp": "2026-05-10T10:30:46.123456Z",
    "processing_time": 2.45
  }
]
```

---

### 4. WebSocket (Real-time Query - Optional)
```
WebSocket /ws/query/{user_id}
```
Establish a WebSocket connection for real-time query processing and responses.

**Connect:**
```javascript
const ws = new WebSocket("ws://localhost:8000/ws/query/user123");

ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  console.log(response);
};
```

**Send Query:**
```json
{
  "query": "What is GYWS?",
  "use_web_search": true
}
```

**Receive Response:**
```json
{
  "status": "success",
  "answer": "<div>...</div>",
  "processing_time": 2.34,
  "timestamp": "2026-05-10T10:30:45.123456Z"
}
```

---

### 5. Get Conversation History
```
GET /v1/conversation/{user_id}?skip=0&limit=10
```
Retrieve conversation history for a user with pagination.

**Query Parameters:**
- `skip`: Number of messages to skip (default: 0)
- `limit`: Number of messages to return (default: 10, max: 100)

**Response:**
```json
{
  "user_id": "user123",
  "messages": [
    {
      "role": "user",
      "content": "What is GYWS?",
      "timestamp": "2026-05-10T10:30:40.123456Z"
    },
    {
      "role": "assistant",
      "content": "<div>...</div>",
      "timestamp": "2026-05-10T10:30:45.123456Z"
    }
  ],
  "total_messages": 25
}
```

---

### 6. Add Message to Conversation
```
POST /v1/conversation/{user_id}/message
```
Manually add a message to conversation history (useful for integrations).

**Request Body:**
```json
{
  "role": "user",
  "content": "Custom message"
}
```

**Response:**
```json
{
  "message": "Message added",
  "user_id": "user123",
  "timestamp": "2026-05-10T10:30:45.123456Z"
}
```

---

### 7. Clear Conversation
```
DELETE /v1/conversation/{user_id}
```
Clear all conversation history for a user.

**Response:**
```json
{
  "message": "Conversation cleared",
  "user_id": "user123",
  "timestamp": "2026-05-10T10:30:45.123456Z"
}
```

---

### 8. Service Status
```
GET /v1/status
```
Get detailed service status including active users and connections.

**Response:**
```json
{
  "service": "GYWS Chatbot API",
  "status": "operational",
  "active_users": 42,
  "total_conversations": 156,
  "active_websockets": 5,
  "timestamp": "2026-05-10T10:30:45.123456Z"
}
```

---

### 9. Embeddings Info
```
GET /v1/embeddings/info
```
Get information about loaded embeddings.

**Response:**
```json
{
  "status": "loaded",
  "chunks_count": 150,
  "embedding_dimension": 768,
  "file": "embeddings.npy",
  "timestamp": "2026-05-10T10:30:45.123456Z"
}
```

---

## API Response Standards

### Success Response
```json
{
  "request_id": "unique-id",
  "status": "success",
  "answer": "Response content",
  "timestamp": "ISO-8601 timestamp",
  "processing_time": 2.34
}
```

### Error Response
```json
{
  "error": "Error description",
  "status_code": 500,
  "timestamp": "ISO-8601 timestamp",
  "request_id": "optional-request-id"
}
```

---

## Service Integration Examples

### Python Example (Synchronous)
```python
import requests

url = "http://localhost:8000/v1/query"
payload = {
    "query": "What is GYWS?",
    "user_id": "user123",
    "use_web_search": True
}

response = requests.post(url, json=payload)
result = response.json()

print(result["answer"])
print(f"Processing time: {result['processing_time']}s")
```

### JavaScript/Node.js Example
```javascript
const response = await fetch("http://localhost:8000/v1/query", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "What is GYWS?",
    user_id: "user123",
    use_web_search: true
  })
});

const result = await response.json();
console.log(result.answer);
```

### WebSocket Example
```javascript
const ws = new WebSocket("ws://localhost:8000/ws/query/user123");

ws.onopen = () => {
  ws.send(JSON.stringify({
    query: "What is GYWS?",
    use_web_search: true
  }));
};

ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  console.log(result.answer);
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};
```

---

## Key Improvements in v2.0

✅ **Synchronous API** - `/v1/query` returns answer directly (no polling)
✅ **Batch Processing** - Process multiple queries at once
✅ **WebSocket Support** - Real-time bidirectional communication
✅ **Better Pagination** - Conversation history with skip/limit
✅ **Service Status** - Monitor active users and connections
✅ **Timestamps** - All responses include ISO-8601 timestamps
✅ **Processing Time** - Track query processing duration
✅ **Proper Error Handling** - Consistent error response format
✅ **API Versioning** - All endpoints under `/v1/` for future compatibility
✅ **OpenAPI Documentation** - Full Swagger docs at `/docs`

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Generative AI API key | Yes |
| `SERPER_API_KEY` | Serper (Google Search) API key | Yes |

### Server Settings

Edit `main.py` to modify:
- `EMBEDDINGS_FILE`: Path to embeddings file (default: `embeddings.npy`)
- CORS settings (currently allows all origins)
- Port number (default: 8000)

## How It Works

1. **Query Processing**:
   - User submits a query with unique `user_id`
   - System generates embedding for the query
   - Retrieves relevant document chunks using cosine similarity
   - Optionally performs web search
   - Generates answer using Gemini API with context

2. **Response Format**:
   - Returns clean HTML styled with Tailwind CSS
   - Maintains conversation history per user
   - Avoids markdown code blocks in output

3. **Special Features**:
   - If query contains "mrinal da" → responds with "ask other question"
   - Focuses on GYWS and IIT Kharagpur information
   - Preserves conversation context across multiple queries

## Common Issues & Solutions

### ModuleNotFoundError: No module named 'google'
**Solution**: Install google-generativeai
```powershell
pip install google-generativeai==0.6.0
```

### GEMINI_API_KEY not found
**Solution**: Create `.env` file with your API key (see Configuration section)

### ModuleNotFoundError: No module named 'dotenv'
**Solution**: Install python-dotenv
```powershell
pip install python-dotenv==1.0.0
```

### embeddings.npy not found
**Solution**: Generate embeddings using `index.py` or place existing file in project root

## Development

### Activate Debug Mode
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### View API Documentation
Access http://localhost:8000/docs while server is running

### Check Logs
Monitor the terminal for real-time processing logs and errors

## Deployment

### Production Setup
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Remove `--reload` flag in production.

## Security Notes

⚠️ **Important**: 
- Never commit `.env` file to version control (it's in `.gitignore`)
- Keep API keys private and secure
- Use `.env.example` as template for team members
- Consider using environment variable services in production

## Troubleshooting

### Server won't start
1. Check if port 8000 is available: `netstat -ano | findstr :8000`
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Check `.env` file exists with valid API keys

### Slow responses
1. Check embeddings file size
2. Verify API rate limits with Gemini and Serper
3. Consider caching frequent queries

### Incorrect responses
1. Verify embeddings were generated from correct documents
2. Check RAG context quality
3. Review system prompt in `main.py`

## License

All rights reserved. Proprietary project for GYWS/IIT Kharagpur.

## Support

For issues or questions, contact the development team.

## Version History

- **v1.0.0** (May 2026): Initial release with RAG and web search support

---

**Last Updated**: May 10, 2026
