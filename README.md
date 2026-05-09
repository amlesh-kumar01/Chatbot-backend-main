# Chatbot Backend - GYWS Query Assistant

A FastAPI-based chatbot backend that uses Retrieval-Augmented Generation (RAG) combined with web search to answer questions about GYWS (Green Yellow White Society) and IIT Kharagpur.

## Features

- **RAG (Retrieval-Augmented Generation)**: Uses document embeddings for context-aware responses
- **Web Search Integration**: Fetches real-time information using Serper API
- **Conversation History**: Maintains per-user conversation context
- **Async Processing**: Non-blocking query processing with status tracking
- **HTML Responses**: Generates clean HTML responses styled with Tailwind CSS
- **CORS Support**: Configured for cross-origin requests

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **AI Models**: 
  - Google Generative AI (Gemini) for embeddings and text generation
  - Mistral AI integration support
- **Data Processing**: NumPy, PyPDF2
- **API Integration**: Serper (Google Search API)

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

## API Endpoints

### 1. Health Check
```
GET /
```
Returns server status.

**Response:**
```json
{
  "message": "Chatbot API is running!",
  "status": "healthy"
}
```

### 2. Submit Query
```
POST /query/
```
Start processing a query asynchronously.

**Request Body:**
```json
{
  "query": "What is GYWS?",
  "user_id": "user123",
  "use_web_search": true
}
```

**Response:**
```json
{
  "message": "Query processing started",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. Get Processing Status
```
GET /status/{request_id}
```
Check the status of a query being processed.

**Response:**
```json
{
  "status": "Generating answer...",
  "completed": false
}
```

### 4. Get Query Result
```
GET /result/{request_id}/{user_id}
```
Retrieve the final answer once processing is complete.

**Response:**
```json
{
  "answer": "<div class=\"text-sm\"><p>GYWS is...</p></div>",
  "completed": true
}
```

### 5. Clear Conversation History
```
DELETE /conversation/{user_id}
```
Clear all conversation history for a specific user.

**Response:**
```json
{
  "message": "Conversation cleared"
}
```

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
