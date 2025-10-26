# Deployment Guide

Step-by-step instructions for deploying to Render or Railway.

---

## Option 1: Deploy to Render (Recommended)

Render offers a generous free tier with automatic deployments from GitHub.

### Step 1: Prepare Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: RAG policy Q&A application"
   ```

2. **Push to GitHub**:
   ```bash
   # Create a new repository on GitHub first
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up using your GitHub account
3. Authorize Render to access your repositories

### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**

2. **Connect Repository**:
   - Select your `Quantic-AI-Project` repository
   - Click **"Connect"**

3. **Configure Service**:
   ```
   Name: techcorp-policy-assistant
   Region: Oregon (US West) [or closest to you]
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   Instance Type: Free
   ```

4. **Add Environment Variables**:
   Click **"Advanced"** → **"Add Environment Variable"**

   Required:
   ```
   OPENAI_API_KEY = your_openai_api_key_here
   PYTHON_VERSION = 3.10.12
   ```

   Optional (for tuning):
   ```
   LLM_MODEL = gpt-3.5-turbo
   LLM_TEMPERATURE = 0.1
   RAG_TOP_K = 5
   ```

5. Click **"Create Web Service"**

### Step 4: Wait for Deployment

- Render will build and deploy your app (~5-10 minutes for first deploy)
- Watch the logs for any errors
- Once complete, you'll get a URL like: `https://techcorp-policy-assistant.onrender.com`

### Step 5: Test Deployment

```bash
# Health check
curl https://YOUR_APP_URL.onrender.com/health

# Test chat
curl -X POST https://YOUR_APP_URL.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How much PTO do I get?"}'
```

### Step 6: Set Up Auto-Deploy (Optional)

Render automatically deploys on push to `main` branch.

To trigger manual deploys:
1. Go to your service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Option 2: Deploy to Railway

Railway also offers free hosting with automatic GitHub integration.

### Step 1: Prepare Repository

Same as Render (see above).

### Step 2: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Authorize Railway

### Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `Quantic-AI-Project` repository

### Step 4: Configure

Railway automatically detects Python and uses `Procfile`.

**Add Environment Variables**:
1. Click on your service
2. Go to **"Variables"** tab
3. Add:
   ```
   OPENAI_API_KEY = your_api_key_here
   ```

### Step 5: Deploy

- Railway deploys automatically
- Get your URL from the **"Settings"** → **"Domains"** tab
- Railway provides a URL like: `https://your-app.up.railway.app`

### Step 6: Test

Same as Render testing steps.

---

## CI/CD Setup with GitHub Actions

Automate deployments when you push code.

### For Render

1. **Get Deploy Hook**:
   - Go to Render dashboard → Your service
   - Click **"Settings"** → scroll to **"Deploy Hook"**
   - Copy the webhook URL

2. **Add to GitHub Secrets**:
   - Go to GitHub repository → **"Settings"** → **"Secrets and variables"** → **"Actions"**
   - Click **"New repository secret"**
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Value: Your webhook URL
   - Click **"Add secret"**

3. **GitHub Actions will now**:
   - Run tests on every push/PR
   - Auto-deploy to Render on push to `main`

### For Railway

1. **Get API Token**:
   - Railway dashboard → **"Account Settings"** → **"Tokens"**
   - Create new token
   - Copy the token

2. **Add to GitHub Secrets**:
   - Name: `RAILWAY_TOKEN`
   - Value: Your token

3. **Update GitHub Actions**:
   Uncomment the Railway deployment section in `.github/workflows/ci-cd.yml`

---

## Free Tier Limits

### Render Free Tier
- ✅ 750 hours/month (enough for one app)
- ✅ Automatic HTTPS
- ✅ Auto-deploy from Git
- ❌ Spins down after 15 min inactivity (first request slow)
- ❌ 512 MB RAM limit

**Tip**: Keep app awake with UptimeRobot pinging `/health` every 5 minutes.

### Railway Free Tier
- ✅ $5 free credit/month
- ✅ No sleep/spin-down
- ✅ 512 MB RAM, 1 GB disk
- ❌ Credits run out (~500 hours depending on usage)

---

## Troubleshooting Deployment

### "Application failed to start"

**Check logs** for errors:
- Render: Dashboard → Logs tab
- Railway: Service → Deployments → View logs

Common issues:
1. **Missing dependencies**: Ensure `requirements.txt` is complete
2. **Missing environment variables**: Check `OPENAI_API_KEY` is set
3. **Port binding**: Make sure app uses `$PORT` env var

### "Out of memory"

Free tier: 512 MB RAM

**Solutions**:
1. Reduce batch size in embeddings
2. Use smaller model (MiniLM vs mpnet)
3. Upgrade to paid tier

### "ChromaDB persistence errors"

Render/Railway free tiers have ephemeral filesystems.

**Solutions**:
1. Re-index on startup (app.py already does this)
2. Use cloud vector store (Pinecone, Weaviate)
3. Store ChromaDB in persistent volume (paid tier)

### "Slow cold starts"

Render spins down after inactivity.

**Solutions**:
1. Use UptimeRobot to ping `/health` every 5 minutes
2. Upgrade to paid tier (no spin-down)
3. Accept 30s first-request delay

### Vector store empty on deploy

**Issue**: ChromaDB not persisting between deploys

**Solution**: App auto-indexes on startup if empty (see `app.py` line ~30)

**Verify**:
```bash
curl https://your-app.onrender.com/stats
```

Should show `total_documents > 0`

---

## Production Checklist

Before going live:

- [ ] Environment variables set correctly
- [ ] API keys secured (not in code)
- [ ] `.gitignore` includes `.env`, `chroma_db/`, etc.
- [ ] Health endpoint returns 200 OK
- [ ] Test queries work via `/chat` endpoint
- [ ] Vector store has documents (`/stats` endpoint)
- [ ] CI/CD pipeline passes
- [ ] Logs show no errors
- [ ] Response times acceptable (< 3s)

---

## Monitoring

### Health Checks

Set up external monitoring:

**UptimeRobot** (free):
1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Add monitor:
   - Type: HTTP(s)
   - URL: `https://your-app.onrender.com/health`
   - Interval: 5 minutes
3. Get alerts if app goes down

### Logs

**Render**:
- Dashboard → Service → Logs tab
- Real-time log streaming
- Download logs for analysis

**Railway**:
- Service → Deployments → Latest → Logs
- Can filter by severity

### Metrics

Track via `/stats` endpoint:
```bash
curl https://your-app.onrender.com/stats
```

Monitor:
- Document count (should be ~42)
- Response times (add to evaluation)

---

## Scaling Considerations

When you outgrow free tier:

### Vector Store
- **Current**: ChromaDB local (ephemeral on free tier)
- **Upgrade to**: Pinecone, Weaviate Cloud (managed, persistent)

### Compute
- **Current**: Free tier (512 MB RAM, shared CPU)
- **Upgrade to**: Render/Railway paid (~$7-15/month, dedicated resources)

### LLM
- **Current**: OpenAI API (pay-per-use)
- **Optimize**: Use GPT-3.5-turbo, cache responses, rate limit users

### Caching
- **Add**: Redis for query caching
- **Benefit**: Reduce LLM costs, faster responses

---

## Cost Estimates

### Free Tier (Month 1)
```
Render: Free
OpenAI API: ~$2-5 (100-500 queries)
Total: $2-5/month
```

### Production (at scale)
```
Render/Railway: $7-15/month
Pinecone: $0-70/month (free tier -> starter)
OpenAI API: $10-50/month (1k-5k queries)
Total: $20-135/month
```

---

## Next Steps After Deployment

1. **Test thoroughly**: Run full evaluation suite
2. **Monitor usage**: Check logs daily for first week
3. **Gather feedback**: Share with classmates/users
4. **Iterate**: Improve based on metrics
5. **Document**: Update README with live URL

---

## Support

Deployment issues?

1. Check Render/Railway status page
2. Review deployment logs
3. Test locally first (`python app.py`)
4. Verify environment variables
5. Check GitHub Actions logs

---

**Deployed successfully?** Update your README with the live URL! 🎉
