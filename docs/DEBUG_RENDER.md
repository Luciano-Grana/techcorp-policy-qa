# Debug Render Deployment

## Current Issue: "The string did not match the expected pattern"

This error means Render is still using the old model configuration.

## Step-by-Step Debug Process

### 1. Check Render Environment Variables

Go to **Render Dashboard** → **Environment** tab

**Verify EXACT values:**
```
OPENROUTER_API_KEY = sk-or-v1-YOUR_NEW_KEY_HERE  (NOT the old ...a0de key!)
LLM_MODEL = openai/gpt-3.5-turbo  (NOT deepseek or llama!)
```

**Common mistakes:**
- ❌ Old API key still set
- ❌ Model name has typo
- ❌ Model name still has `:free` suffix
- ❌ Forgot to click "Save Changes"

### 2. Check Render Logs for Actual Error

The logs you shared don't show the error. Look for:

```
# In Render Logs tab, search for:
"error"
"Error code: 404"
"Error code: 429"
"string did not match"
```

**To see the full error:**
1. Click "Logs" tab in Render
2. Ask a question in the chatbot
3. Look for the error traceback
4. Copy the full error message

### 3. Force Redeploy After Changing Environment

After changing environment variables:

**Option A: Automatic**
- Render should show "Environment updated, redeploy?"
- Click "Yes, redeploy"

**Option B: Manual**
- Go to top right
- Click "Manual Deploy"
- Select "Clear build cache & deploy"
- This ensures new environment variables are loaded

### 4. Check What Model Render is Using

Look in Render logs for:
```
Using OpenRouter API
✓ Using model: openai/gpt-3.5-turbo
```

If it shows a different model, the environment variable didn't update.

### 5. Verify Your New API Key is Active

Test your new key locally:
```bash
curl https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer YOUR_NEW_KEY_HERE"
```

Should return:
```json
{
  "data": {
    "label": "...",
    "limit": null,
    "usage": 0.000XX
  }
}
```

## Common Render Issues

### Issue 1: Environment Variable Not Saved
**Symptoms**: "string did not match" error
**Fix**:
1. Go to Environment tab
2. Click "Add Environment Variable" if LLM_MODEL doesn't exist
3. Or click "Edit" if it exists
4. Set to: `openai/gpt-3.5-turbo`
5. **Click "Save Changes"**
6. When prompted, click "Redeploy"

### Issue 2: Using Old Deployment
**Symptoms**: App works but uses old model
**Fix**:
1. Click "Manual Deploy"
2. Select "Clear build cache & deploy"
3. Wait for full rebuild

### Issue 3: Old API Key Still Set
**Symptoms**: 401 Unauthorized or old key errors
**Fix**:
1. Go to Environment tab
2. Find OPENROUTER_API_KEY
3. Click Edit
4. Paste NEW key (should start with sk-or-v1-...)
5. Save and redeploy

## Quick Verification Checklist

Before asking for more help, verify:

- [ ] Updated `LLM_MODEL` to `openai/gpt-3.5-turbo` on Render
- [ ] Updated `OPENROUTER_API_KEY` to NEW key on Render
- [ ] Clicked "Save Changes" after editing
- [ ] Clicked "Redeploy" or manually deployed
- [ ] Waited for deployment to complete (shows "Live")
- [ ] Checked logs for "Using model: openai/gpt-3.5-turbo"
- [ ] Tested chatbot after redeployment

## Get Full Error Details

To get the exact error from Render:

1. **In Render Logs**, click the filter icon
2. **Search for**: `Error`
3. **Copy the full error** including:
   - Error message
   - Stack trace
   - Any HTTP response codes

Share that full error for more specific help.

## Expected Success Logs

After fixing, you should see:

```
==> Starting service...
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000

# After first request:
Starting RAG initialization...
Vector store loaded with 125 documents
Using OpenRouter API
✓ RAG pipeline initialized
✓ Using model: openai/gpt-3.5-turbo

# After asking a question:
127.0.0.1 - - [date] "POST /chat HTTP/1.1" 200 543
```

**No errors, clean 200 response!**
