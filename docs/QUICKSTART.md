# Quick Start Guide - Chatbot Backend v2.0

## 🚀 Get Running in 3 Minutes

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Configure API Keys
```powershell
# The .env file is already set up with your keys
# Just verify it contains:
# GEMINI_API_KEY=your_key
# SERPER_API_KEY=your_key
```

### Step 3: Start the Server
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
✅ Loaded 150 chunks from embeddings file
```

---

## 🧪 Test the API

### Option 1: Interactive API Docs (Recommended)
```
Open browser: http://localhost:8000/docs
```
- Try endpoints directly
- See request/response formats
- View all available operations

### Option 2: Python Client
```powershell
python
```

```python
from client_sdk import ChatbotAPIClient

with ChatbotAPIClient() as client:
    # Test connection
    health = client.health_check()
    print(f"✅ API Status: {health['status']}")
    
    # Send a query
    response = client.query("What is GYWS?", user_id="test_user")
    print(f"Answer: {response.answer}")
    print(f"Time: {response.processing_time}s")
```

### Option 3: cURL
```powershell
curl -X POST http://localhost:8000/v1/query `
  -H "Content-Type: application/json" `
  -d '{
    "query": "What is GYWS?",
    "user_id": "test_user",
    "use_web_search": true
  }'
```

### Option 4: PowerShell
```powershell
$body = @{
    query = "What is GYWS?"
    user_id = "test_user"
    use_web_search = $true
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/v1/query" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

---

## 📊 What's New in v2.0

### Before (v1.0) - Polling Based
```
POST /query/          → get request_id
GET /status/{id}      → poll status
GET /result/{id}/{uid} → get answer
(3+ API calls, slow)
```

### Now (v2.0) - Direct Response
```
POST /v1/query → get answer immediately
(1 API call, fast)
```

### New Features
✅ **Synchronous API** - Get answers directly  
✅ **Batch Processing** - Process 50+ queries at once  
✅ **WebSocket Support** - Real-time updates  
✅ **Python Client SDK** - Easy integration  
✅ **Better Error Handling** - Clear error messages  
✅ **Service Status** - Monitor active users  

---

## 💻 Integration Examples

### JavaScript/Node.js
```javascript
// Simple fetch example
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

### Python
```python
import requests

response = requests.post("http://localhost:8000/v1/query", json={
    "query": "What is GYWS?",
    "user_id": "user123",
    "use_web_search": True
})

data = response.json()
print(data["answer"])
```

### C# / .NET
```csharp
using System.Net.Http;
using System.Text.Json;

var client = new HttpClient();
var payload = new {
    query = "What is GYWS?",
    user_id = "user123",
    use_web_search = true
};

var content = new StringContent(
    JsonSerializer.Serialize(payload),
    System.Text.Encoding.UTF8,
    "application/json"
);

var response = await client.PostAsync(
    "http://localhost:8000/v1/query",
    content
);

var result = JsonSerializer.Deserialize<JsonElement>(
    await response.Content.ReadAsStringAsync()
);
```

---

## 🛠️ Common Commands

### Run Server (Development)
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Server (Production)
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Check API Status
```powershell
curl http://localhost:8000/
```

### Get Service Status
```powershell
curl http://localhost:8000/v1/status
```

### View Conversation History
```powershell
curl "http://localhost:8000/v1/conversation/user123?limit=10"
```

### Clear Conversation
```powershell
curl -X DELETE http://localhost:8000/v1/conversation/user123
```

---

## 📁 Project Structure

```
Chatbot-backend-main/
├── main.py                   # ← Main FastAPI application (v2.0)
├── utils.py                  # Utility functions
├── client_sdk.py             # ← Python client library (NEW)
├── requirements.txt          # Dependencies
├── .env                       # Configuration (git ignored)
├── .env.example              # Configuration template
├── .gitignore                # Git ignore rules
├── README.md                 # Main documentation
├── ARCHITECTURE.md           # ← System design (NEW)
├── INTEGRATION_GUIDE.md      # ← Integration examples (NEW)
├── UPGRADE_SUMMARY.md        # ← v1→v2 changes (NEW)
└── embeddings.npy            # Pre-generated embeddings
```

---

## 🔍 Debugging

### Check Embeddings
```powershell
curl http://localhost:8000/v1/embeddings/info
```

**Response:**
```json
{
  "status": "loaded",
  "chunks_count": 150,
  "embedding_dimension": 768,
  "file": "embeddings.npy"
}
```

### View Server Logs
```powershell
# Terminal where server is running shows logs
# Look for:
# - Request timestamps
# - Processing times
# - Errors (if any)
```

### Test with Python
```python
from client_sdk import ChatbotAPIClient
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

client = ChatbotAPIClient()
response = client.query("Test", "user123")
print(response)
```

---

## ⚠️ Troubleshooting

### Issue: "Module not found" error
```powershell
# Solution: Install missing package
pip install -r requirements.txt
```

### Issue: "Connection refused"
```powershell
# Solution: Check if server is running
# Terminal 1:
uvicorn main:app --reload

# Terminal 2:
curl http://localhost:8000/
```

### Issue: "Embeddings file not found"
```powershell
# Solution: Generate embeddings
# (Note: You need an index.py file to do this)
# For now, place your embeddings.npy in project root
```

### Issue: API returns 500 error
```powershell
# Solution: Check server logs for details
# Look at terminal running the server
# Common causes:
# - Missing API keys in .env
# - Embeddings file missing
# - Invalid query format
```

---

## 📚 Documentation Index

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Main docs with all endpoints |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & patterns |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | Code examples |
| [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md) | What's new in v2.0 |
| [client_sdk.py](client_sdk.py) | Python client library |

---

## 🎯 Next Steps

### For Development
1. ✅ Server running locally
2. 📖 Review `INTEGRATION_GUIDE.md` for examples
3. 🧪 Test with your frontend
4. 📊 Monitor with `/v1/status` endpoint

### For Production
1. 📋 Review `ARCHITECTURE.md`
2. 🔐 Add authentication/rate limiting
3. 💾 Set up database for persistence
4. 📊 Add monitoring & alerts
5. 🚀 Deploy with multiple workers

### For Integration
1. 📚 Check `INTEGRATION_GUIDE.md`
2. 📦 Use `client_sdk.py` from Python
3. 🔗 Or integrate with any language via HTTP
4. ✅ Test thoroughly before deployment

---

## 📞 API Reference

```
GET  /                           → Health check
POST /v1/query                   → Process single query
POST /v1/query/batch             → Process multiple queries
WS   /ws/query/{user_id}         → WebSocket connection
GET  /v1/conversation/{user_id}  → Get history
POST /v1/conversation/{user_id}/message → Add message
DEL  /v1/conversation/{user_id}  → Clear history
GET  /v1/status                  → Service status
GET  /v1/embeddings/info         → Embeddings info
```

For detailed docs, visit: **http://localhost:8000/docs**

---

## ✅ Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with API keys
- [ ] `embeddings.npy` file exists
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Test query works
- [ ] Read documentation files
- [ ] Ready for integration

---

## 🎉 You're Ready!

Your Chatbot Backend v2.0 is now ready for:
- 🌐 Web applications
- 📱 Mobile backends
- 🔗 Microservice integration
- 💬 Chat applications
- 📊 Batch processing

**Happy coding! 🚀**

For support, check the documentation or review code comments.

---

**Version**: 2.0.0 (May 2026)  
**Status**: Production Ready
