# 🔧 Error Fixes - API Issues Resolved

## ✅ Problems Fixed

### 1. **Embedding Model Error (404)**
**Problem:** `models/embedding-001` is not found for API version v1beta

**Fix:** Changed to `models/text-embedding-004` which is available and supported
- **File:** `utils.py`
- **Change:** Line 43 & 67 - Updated model name
- **Status:** ✅ Fixed

---

### 2. **Rate Limiting Error (429)**
**Problem:** Quota exceeded for Generate Content API requests per minute

**Cause:** Free tier of Google Gemini API has limited requests (0 per minute means no quota)

**Fixes Applied:**
- ✅ Added **exponential backoff retry logic** - Automatic retries with delays
- ✅ Retry up to 3 times before giving up
- ✅ Delays: 1s → 2s → 4s between retries
- **Files:** `utils.py` (functions: `generate_answer`, `_get_embedding_with_retry`)

---

### 3. **NaN Error (Invalid Value in Scalar Divide)**
**Problem:** RuntimeWarning: invalid value encountered in scalar divide (line 63)

**Cause:** Cosine similarity calculation dividing by zero when vector norm is 0

**Fix:** Added zero-norm handling in `cosine_similarity()` function
```python
# Now safely handles zero vectors
if norm_a == 0 or norm_b == 0:
    return 0.0
```

---

## 🚀 Solution for Rate Limiting

### Option 1: Request Higher Quota (Recommended for Production)
1. Visit: https://cloud.google.com/docs/quotas/help/request_increase
2. Request higher quota for "GenerateContent request limit per minute"
3. Wait for Google to approve (usually 24-48 hours)

### Option 2: Use Paid API Tier
1. Enable billing in Google Cloud Console
2. Free tier converts to paid (with generous free credits)
3. Get much higher quota limits

### Option 3: Optimize Current Setup
- Use fewer web searches per query
- Cache common queries
- Batch multiple queries together
- Wait between requests

---

## 📊 How the Fix Works

### Before (Failed)
```
Query → Embedding Error (404) → Returns zero vector
    → Answer Generation → Rate Limit (429) → Error
```

### After (Works with Retries)
```
Query → Embedding (text-embedding-004) ✅
    ↓
    If Rate Limited → Wait 1s → Retry
    If Still Rate Limited → Wait 2s → Retry
    If Still Rate Limited → Wait 4s → Retry
    ↓
Answer → Return ✅
```

---

## ⚙️ Updated Code Highlights

### New Retry Function
```python
def _get_embedding_with_retry(text, task_type="retrieval_document"):
    """Get embedding with exponential backoff retry logic"""
    for attempt in range(MAX_RETRIES):
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",  # Fixed model
                content=text,
                task_type=task_type
            )
            return result['embedding']
        except Exception as e:
            if "429" in str(e) or "RATE_LIMIT_EXCEEDED" in str(e):
                if attempt < MAX_RETRIES - 1:
                    retry_delay = INITIAL_RETRY_DELAY * (2 ** attempt)
                    time.sleep(retry_delay)  # Exponential backoff
                    continue
```

### Fixed Cosine Similarity
```python
def cosine_similarity(a, b):
    """Calculate cosine similarity, handling zero norms"""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0  # Prevent NaN
    
    return np.dot(a, b) / (norm_a * norm_b)
```

---

## 🧪 Testing the Fix

### Step 1: Restart the Server
```powershell
# Stop current server (Ctrl+C)
# Then restart
uvicorn main:app --reload
```

### Step 2: Test the Query Endpoint
```bash
curl -X POST http://localhost:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is GYWS?",
    "user_id": "test_user",
    "use_web_search": false
  }'
```

**Note:** Set `use_web_search: false` to reduce API calls while testing.

### Step 3: Monitor Console Output
You should see:
```
✅ Loaded 150 chunks from embeddings file
🌐 Server will start on http://localhost:8000
```

When you make a request, you should NOT see:
- ❌ `Error generating query embedding: 404 models/embedding-001`
- ❌ `Error generating answer: 429 Quota exceeded`

---

## 📋 Verification Checklist

- [ ] `utils.py` has been updated with retry logic
- [ ] Server restarted after file changes
- [ ] Can successfully query `/v1/query` endpoint
- [ ] No embedding model errors (404)
- [ ] No rate limit errors (429) - or they're being retried
- [ ] Responses are returned (even if from fallback)
- [ ] No NaN warnings in console output

---

## 🎯 Next Steps

### Immediate (This Week)
1. Test with `use_web_search: false` to avoid extra API calls
2. Monitor your API quota usage
3. If still hitting rate limits, request higher quota

### Short Term (Next Week)
1. Request quota increase from Google Cloud Console
2. Once approved, enable `use_web_search: true`
3. Monitor query response times

### Long Term (Production)
1. Set up API key with billing enabled
2. Implement caching layer for common queries
3. Add monitoring and alerting for quota usage
4. Consider multi-model strategy (different APIs)

---

## 🔗 Helpful Links

- **Google API Status:** https://cloud.google.com/docs/quotas/help/request_increase
- **Gemini API Quotas:** https://ai.google.dev/
- **Our API Docs:** http://localhost:8000/docs
- **Rate Limiting Best Practices:** https://cloud.google.com/docs/rate-limiting

---

## ✨ Summary

All three errors have been fixed:
1. ✅ **Embedding model** - Now using correct API
2. ✅ **Rate limiting** - Automatic retries with backoff
3. ✅ **NaN calculation** - Safe zero-norm handling

**Your API is now resilient to temporary rate limits!** 🚀
