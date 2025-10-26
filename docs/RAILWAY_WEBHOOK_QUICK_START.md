# Railway Webhook Setup - Quick Checklist

## What You Need to Do Right Now

Your GitHub Actions workflow is already configured! You just need to configure Railway and add secrets to GitHub.

### ✅ Step 1: Disable Railway Auto-Deploy (2 minutes)

1. Go to https://railway.app
2. Select your project → `techcorp-policy-qa` service
3. Click **Settings**
4. Scroll to **Source** section
5. Click **Disconnect** next to your GitHub repository

This stops Railway from deploying on every push.

### ✅ Step 2: Get Railway Webhook URL (1 minute)

**Easiest method:**

1. Still in Settings
2. Scroll down to find **Webhooks** or **Deploy Hooks** section
3. Look for **Deployment Webhook URL**
4. Copy the entire URL (looks like: `https://backboard.railway.app/webhook/...`)

### ✅ Step 3: Add Secret to GitHub (1 minute)

1. Go to https://github.com/Luciano-Grana/techcorp-policy-qa/settings/secrets/actions
2. Click **New repository secret**
3. Name: `RAILWAY_WEBHOOK_URL`
4. Value: Paste the webhook URL from Step 2
5. Click **Add secret**

### ✅ Step 4: Test the Setup (2 minutes)

Make a small change to trigger the workflow:

```bash
cd /Users/lucianograna/Quantic-AI-Project

# Make a small change
echo "" >> README.md

# Commit and push
git add README.md
git commit -m "test: Verify webhook deployment after CI passes"
git push origin main
```

### ✅ Step 5: Verify It Works

**Watch GitHub Actions** (https://github.com/Luciano-Grana/techcorp-policy-qa/actions):
1. Workflow starts immediately
2. `build-and-test` job runs (~2-3 minutes)
3. Tests pass ✅
4. `deploy` job runs
5. You should see: "✅ Tests passed! Triggering Railway deployment..."

**Watch Railway** (https://railway.app):
1. NO deployment should start immediately
2. Deployment should start ONLY after GitHub Actions completes
3. This is the correct behavior!

## Expected Timeline

```
Push to main
   ↓
GitHub Actions starts (2-3 min)
   ↓
Tests PASS ✅
   ↓
Webhook triggered
   ↓
Railway deployment starts (5-7 min)
   ↓
Done! ✅

Total: ~8-10 minutes
```

## Troubleshooting

### If Railway Still Auto-Deploys
- Make sure you clicked **Disconnect** in Step 1
- Check that GitHub connection is removed from Railway Settings

### If No Deployment Happens
- Verify secret `RAILWAY_WEBHOOK_URL` is set in GitHub
- Check GitHub Actions logs for webhook call
- Make sure webhook URL is complete and correct

### If You Can't Find Webhook URL
Use the API method instead (see [RAILWAY_WEBHOOK_SETUP.md](./RAILWAY_WEBHOOK_SETUP.md) for details).

## What's Already Done

✅ GitHub Actions workflow updated with webhook deployment
✅ Workflow only triggers deploy after tests pass
✅ Documentation created

## What You Need to Do

⏳ Disconnect Railway from GitHub
⏳ Get webhook URL
⏳ Add to GitHub secrets
⏳ Test with a push

**Time required: ~6 minutes**

---

Once this is working, Railway will ONLY deploy after your tests pass! 🎉
