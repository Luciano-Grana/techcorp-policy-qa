# Deploy to Render - Step-by-Step Guide

This guide walks you through deploying your RAG application to Render using GitHub.

## Prerequisites

✅ All deployment files are ready:
- `Procfile` - Tells Render how to start the app
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Lists all dependencies
- `.gitignore` - Excludes unnecessary files
- `.env.example` - Template for environment variables

## Deployment Steps

### Step 1: Create GitHub Repository

1. **Go to GitHub** and create a new repository:
   - Visit https://github.com/new
   - Repository name: `techcorp-policy-qa` (or your preferred name)
   - Description: "RAG-based policy Q&A assistant using ChromaDB and OpenRouter"
   - Visibility: **Public** (for free Render tier) or Private (requires paid Render plan)
   - **DO NOT** initialize with README (we already have one)

2. **Copy the repository URL** (you'll need it in Step 2)
   - Format: `https://github.com/YOUR_USERNAME/techcorp-policy-qa.git`

### Step 2: Initialize Git and Push to GitHub

Run these commands in your terminal from the project directory:

```bash
# 1. Initialize git repository
git init

# 2. Configure git (if not done already)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 3. Add all files
git add .

# 4. Create first commit
git commit -m "Initial commit: RAG policy Q&A application

- Custom RAG pipeline with ChromaDB
- 8 policy documents (~70 pages)
- Flask web interface
- Evaluation framework with 88.3% groundedness, 91.7% citation accuracy
- OpenRouter API integration (free tier)
- Ready for production deployment"

# 5. Add remote repository (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/techcorp-policy-qa.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Create Render Account

1. **Go to Render**: https://render.com
2. **Sign up** using your GitHub account (easiest option)
3. **Authorize Render** to access your GitHub repositories

### Step 4: Create Web Service on Render

1. **Dashboard** → Click **"New +"** → **"Web Service"**

2. **Connect Repository**:
   - Select your `techcorp-policy-qa` repository
   - Click **"Connect"**

3. **Configure Web Service**:

   | Setting | Value |
   |---------|-------|
   | **Name** | `techcorp-policy-qa` (or your choice) |
   | **Region** | Choose closest to you |
   | **Branch** | `main` |
   | **Root Directory** | Leave empty |
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2` |
   | **Instance Type** | **Free** |

4. **Click "Advanced"** to expand advanced settings

### Step 5: Add Environment Variables

In the **Environment Variables** section, add:

| Key | Value |
|-----|-------|
| `OPENROUTER_API_KEY` | `YOUR_OPENROUTER_API_KEY_HERE` |
| `LLM_MODEL` | `meta-llama/llama-3.1-8b-instruct:free` |
| `LLM_TEMPERATURE` | `0.1` |
| `LLM_MAX_TOKENS` | `500` |
| `RAG_TOP_K` | `5` |
| `FLASK_DEBUG` | `False` |
| `PYTHON_VERSION` | `3.10.12` |

### Step 6: Deploy

1. **Click "Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies (~5 minutes)
   - Build the application
   - Start the web server
   - Index documents on first startup

3. **Watch the logs** for:
   ```
   Loading policy documents...
   ✓ Loaded 8 policy documents
   Indexing documents...
   ✓ Indexed 125 chunks
   Starting Gunicorn server...
   ```

4. **Wait for deployment** to complete (~5-10 minutes)

### Step 7: Test Your Deployment

1. **Get your URL**: Render will provide a URL like:
   ```
   https://techcorp-policy-qa.onrender.com
   ```

2. **Visit the URL** in your browser

3. **Test the chatbot**:
   - Ask: "How much PTO do employees get?"
   - Ask: "What is the remote work policy?"
   - Ask: "How do I submit an expense report?"

4. **Verify health endpoint**:
   ```
   https://techcorp-policy-qa.onrender.com/health
   ```

## Post-Deployment

### Update Your README

Add your deployment URL to the README.md:

```bash
# Edit README.md and update the "Live Demo" line
git add README.md
git commit -m "Add production URL to README"
git push
```

Render will **auto-deploy** on every push to main!

### Enable Auto-Deploy (Optional)

Render automatically deploys when you push to GitHub. To disable:
- Go to your service settings
- Navigate to "Deploy" section
- Toggle "Auto-Deploy"

### Monitor Your Application

**Render Dashboard** provides:
- Real-time logs
- CPU/Memory usage
- Request metrics
- Deploy history

Access at: https://dashboard.render.com

## Troubleshooting

### Build Fails: ChromaDB Installation Error

**Error**: `Building wheel for chroma-hnswlib: finished with status 'error'`

**Fix**: Already handled! Your `requirements.txt` uses `chromadb>=0.4.24` which works on Render.

### Application Crashes: "Vector store is empty"

**Cause**: Documents not indexed on startup

**Fix**: The app automatically indexes documents on first run. Check logs for:
```
✓ Indexed 125 chunks
```

### Slow Cold Starts

**Issue**: Free tier services sleep after 15 minutes of inactivity

**Solution**: First request after sleep takes 30-60 seconds. Paid tier ($7/month) keeps service running.

### Out of Memory

**Issue**: Free tier has 512MB RAM limit

**Fix**: Already optimized:
- Using local embeddings (no API calls)
- 2 Gunicorn workers
- Efficient ChromaDB storage

### API Rate Limits

**OpenRouter Free Tier Limits**:
- ~20 requests/minute for `llama-3.1-8b-instruct:free`
- Requests may queue during high traffic

**Solution**: Upgrade to OpenRouter paid tier ($5 credit minimum) for higher limits

## Free Tier Limitations

Render Free Tier:
- ✅ 750 hours/month
- ✅ Custom domain support
- ✅ Auto-deploy from GitHub
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ 512MB RAM
- ⚠️ Shared CPU

**Good for**: Portfolio projects, demos, course projects
**Upgrade when**: Production traffic, need 24/7 uptime

## Upgrading to Paid Tier

**Render Starter** ($7/month):
- No sleep
- 2GB RAM
- Priority support

To upgrade:
1. Go to service settings
2. Change instance type to "Starter"
3. Add payment method

## Security Best Practices

### Protect Your API Key

1. **Never commit .env** (already in .gitignore ✓)
2. **Use environment variables** on Render (already configured ✓)
3. **Rotate keys periodically**

### Update Dependencies

```bash
# Check for security updates
pip list --outdated

# Update requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies for security"
git push
```

Render auto-deploys the updates!

## Next Steps

After successful deployment:

1. ✅ Test all features in production
2. ✅ Update project documentation with live URL
3. ✅ Add URL to your resume/portfolio
4. 🎯 (Optional) Set up custom domain
5. 🎯 (Optional) Add monitoring/analytics
6. 🎯 (Optional) Implement CI/CD tests with GitHub Actions

## Support Resources

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **OpenRouter Docs**: https://openrouter.ai/docs
- **Your Project Issues**: https://github.com/YOUR_USERNAME/techcorp-policy-qa/issues

---

## Quick Reference

```bash
# Push updates to production
git add .
git commit -m "Your update message"
git push

# View logs
# Visit: https://dashboard.render.com → Your Service → Logs

# Check deployment status
# Visit: https://dashboard.render.com → Your Service → Events
```

Good luck with your deployment! 🚀
