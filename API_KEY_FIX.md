# 🔐 API Key Leaked + Model Not Found - FIX GUIDE

## 🚨 **CRITICAL: Your API Key is Compromised!**

Your Gemini API key has been reported as leaked. This means someone may have access to your account.

### **Action Required (RIGHT NOW):**

1. **Revoke the old API key immediately:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Find and **DELETE** your current API key
   - This prevents anyone from using it

2. **Create a NEW API key:**
   - In Google Cloud Console: APIs & Services → Credentials
   - Click: **+ Create Credentials** → **API Key**
   - Copy the NEW key

3. **Update your `.env` file:**
   ```
   GEMINI_API_KEY=your_new_api_key_here_without_quotes
   SERPER_API_KEY=your_serper_api_key
   ```

4. **Restart your server:**
   ```powershell
   # Stop current server (Ctrl+C)
   uvicorn main:app --reload
   ```

---

## 📌 **About the Embedding Model Error**

### **What the Error Means:**
```
404 models/text-embedding-004 is not found for API version v1beta
```

This means:
- ❌ Model name `text-embedding-004` doesn't exist in your API version
- ✅ The correct model is: `models/embedding-001`

### **What I Fixed:**
Changed in `utils.py`:
```python
# ❌ WRONG (doesn't exist):
model="models/text-embedding-004"

# ✅ CORRECT (exists):
model="models/embedding-001"
```

---

## 🔧 **Available Embedding Models**

| Model Name | Status | Use Case |
|------------|--------|----------|
| `models/embedding-001` | ✅ Available | Standard embeddings (768 dimensions) |
| `models/text-embedding-004` | ❌ Not Available | Don't use (v1beta doesn't support) |
| Latest models | ⚠️ May vary | Check Google's API docs |

---

## ✅ **What I Fixed in Your Code**

### **File: `utils.py`**

#### **Change 1: Embedding Function**
```python
# BEFORE (❌ Wrong model):
result = genai.embed_content(
    model="models/text-embedding-004",
    content=text,
    task_type=task_type
)

# AFTER (✅ Correct model):
result = genai.embed_content(
    model="models/embedding-001",
    content=text,
    task_type=task_type
)
```

**Location:** Line ~47 in `_get_embedding_with_retry()` function

---

## 🚀 **Quick Fix Steps**

### **Step 1: Get New API Key (5 minutes)**
```
1. Visit: https://console.cloud.google.com/apis/credentials
2. Delete old key
3. Create new key
4. Copy the key
```

### **Step 2: Update .env File (1 minute)**
```
Edit: .env
Change: GEMINI_API_KEY=your_new_key_here
```

### **Step 3: Restart Server (1 minute)**
```powershell
# Kill current server (Ctrl+C)
uvicorn main:app --reload
```

### **Step 4: Test (2 minutes)**
```bash
curl -X POST http://localhost:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is GYWS?",
    "user_id": "test_user",
    "use_web_search": false
  }'
```

---

## 🔍 **How to Verify the Fix**

### **In Swagger UI:**
1. Visit: http://localhost:8000/docs
2. Try: POST `/v1/query` endpoint
3. Should return answer ✅

### **In Terminal:**
```powershell
# Should NOT see these errors:
# ❌ 403 Your API key was reported as leaked
# ❌ 404 models/text-embedding-004 is not found
# ❌ Error generating embedding
```

---

## 🎯 **Root Causes Explained**

### **Why: "API key was reported as leaked"**
- Your API key was exposed somewhere (GitHub, logs, etc.)
- Google's security system detected it
- You need a new key

### **Why: "models/text-embedding-004 not found"**
- Google's API has multiple versions (v1, v1beta, v2, etc.)
- Each version supports different models
- Your v1beta doesn't have `text-embedding-004`
- Use `embedding-001` instead (stable & available)

---

## 🛡️ **Security Best Practices**

### **Never Do:**
```
❌ Commit .env to Git
❌ Share API keys in messages
❌ Hardcode keys in source files
❌ Log API keys
```

### **Always Do:**
```
✅ Use .env for sensitive data
✅ Add .env to .gitignore
✅ Use environment variables
✅ Rotate keys regularly
✅ Monitor usage in Google Cloud Console
```

---

## 📋 **Checklist**

### **Security (Do First):**
- [ ] Visit Google Cloud Console
- [ ] Delete old/compromised API key
- [ ] Create new API key
- [ ] Copy new key
- [ ] Update `.env` file with new key
- [ ] Save `.env` file
- [ ] Verify `.env` is in `.gitignore`

### **Code Fix (Done):**
- [x] Changed embedding model from `text-embedding-004` to `embedding-001`
- [x] Updated `utils.py` line ~47

### **Testing:**
- [ ] Restart server: `uvicorn main:app --reload`
- [ ] Test with Swagger: http://localhost:8000/docs
- [ ] Make test query (with `use_web_search: false`)
- [ ] Verify response is returned ✅

---

## 🆘 **If You Still Get Errors**

### **Error: "403 Your API key was reported as leaked"**
→ You forgot to update `.env` with new key
→ **Fix:** Replace GEMINI_API_KEY with new key from Google Cloud

### **Error: "404 models/embedding-001 not found"**
→ Your API version doesn't support this model
→ **Fix:** Check Google's API docs for your API version
→ Try: `models/embedding-001` first, then `models/text-embedding-004`

### **Error: "429 Quota exceeded"**
→ You've exceeded free tier quota
→ **Fix:** Request higher quota or enable billing

### **Error: "invalid API key"**
→ Key is wrong or expired
→ **Fix:** Create new key from Google Cloud Console

---

## 🔗 **Useful Links**

| Link | Purpose |
|------|---------|
| https://console.cloud.google.com/apis/credentials | Manage API keys |
| https://ai.google.dev/models | View available models |
| https://cloud.google.com/docs/authentication | Auth documentation |
| https://cloud.google.com/docs/quotas | Quota management |

---

## 📞 **Quick Reference**

### **Key Models to Remember:**
```
Embedding:    models/embedding-001
Text Gen:     models/gemini-1.5-flash (or gemini-pro)
```

### **Test Command:**
```bash
curl -X POST http://localhost:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query":"test","user_id":"user1","use_web_search":false}'
```

### **Key Locations:**
```
API Key:     .env (GEMINI_API_KEY)
Code Fix:    utils.py line ~47
Server:      http://localhost:8000
Docs:        http://localhost:8000/docs
```

---

## ✨ **Summary**

1. **Got new API key?** ✅ Required (old one is compromised)
2. **Updated .env?** ✅ Required (with new key)
3. **Code fixed?** ✅ Done (embedding-001 model)
4. **Server restarted?** ✅ Required (to load new .env)
5. **Tested?** → Next step

---

**Your Turn:** Get a new API key and update `.env`, then restart! 🚀
