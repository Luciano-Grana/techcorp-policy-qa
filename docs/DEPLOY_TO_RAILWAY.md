# Deploy to Railway - Free Alternative

Railway's free tier offers better RAM limits than Render (up to 1GB vs 512MB).

## Quick Setup (10 minutes)

### Step 1: Sign Up
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Authorize Railway to access your GitHub
4. Select `techcorp-policy-qa` repository

### Step 3: Configure Environment Variables

Railway will auto-detect your Python app. Add these variables:

Click "Variables" tab and add:

```
OPENROUTER_API_KEY=your_new_api_key_here
LLM_MODEL=openai/gpt-3.5-turbo
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=500
RAG_TOP_K=5
FLASK_DEBUG=False
PYTHON_VERSION=3.10.12
TOKENIZERS_PARALLELISM=false
OMP_NUM_THREADS=1
MKL_NUM_THREADS=1
PORT=8080
```

### Step 4: Configure Build

Railway should auto-detect from `Procfile`, but if needed:

**Build Command**: (leave blank, uses requirements.txt)
**Start Command**:
```
gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --worker-class sync --max-requests 1000 --max-requests-jitter 50 --preload --worker-tmp-dir /dev/shm
```

### Step 5: Deploy

Railway will automatically deploy. Watch the logs:

```
==> Building...
==> Installing dependencies...
==> Starting application...
==> Deployment successful!
```

You'll get a URL like: `https://techcorp-policy-qa-production.up.railway.app`

## Railway Free Tier

**Limits**:
- $5 free credit per month
- 500 hours execution time
- ~1GB RAM (better than Render's 512MB)
- 1GB disk

**Good for**:
- Portfolio projects
- Demos
- Low traffic apps

## Comparison

| Feature | Render Free | Railway Free | Render Starter |
|---------|-------------|--------------|----------------|
| **RAM** | 512MB ❌ | ~1GB ✅ | 2GB ✅ |
| **Cost** | Free | Free ($5 credit) | $7/month |
| **Sleep** | After 15min | No | No |
| **Hours** | 750/month | 500/month | Unlimited |

## If Railway Also Runs Out of Memory

Then you'll need to:
1. Upgrade Railway to paid tier (~$5-10/month)
2. OR upgrade Render to Starter ($7/month)
3. OR switch to API-based embeddings (code changes required)

Railway's free tier should work for this project though!
