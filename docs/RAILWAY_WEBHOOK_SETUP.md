# Railway Webhook Setup - Deploy After CI Passes

This guide configures Railway to deploy ONLY after GitHub Actions CI passes.

## The Solution

**Disable Railway auto-deploy** and trigger deployment via webhook from GitHub Actions after tests pass.

## Step-by-Step Setup

### Step 1: Disable Railway Auto-Deploy

1. **Go to Railway**: https://railway.app
2. **Select your service**: `techcorp-policy-qa`
3. **Settings** → **Source** section
4. **Option A**: Click "Disconnect" next to GitHub repo (recommended)
5. **Option B**: Settings → Deploy → Toggle OFF "Automatic Deployments"

This stops Railway from deploying immediately on push.

### Step 2: Get Railway Deployment Webhook

Railway provides a webhook URL to trigger deployments:

**Option A: Deployment Webhook (Simple)**
1. Railway Dashboard → Your service
2. Settings → scroll to find "Webhooks" or "Deploy Hooks"
3. Look for "Deployment Webhook URL"
4. Copy the URL

**Option B: Use Railway API (More Control)**
You'll need:
- Railway API Token
- Service ID
- Environment ID

To get these:
1. Railway Dashboard → Account Settings → Tokens
2. Create new token, copy it
3. Your service URL shows IDs: `railway.app/project/{PROJECT_ID}/service/{SERVICE_ID}`

### Step 3: Add Secrets to GitHub

**Go to**: https://github.com/Luciano-Grana/techcorp-policy-qa/settings/secrets/actions

**Add these secrets**:

**For Webhook Method** (simpler):
- **Name**: `RAILWAY_WEBHOOK_URL`
- **Value**: The webhook URL from Step 2

**For API Method** (more reliable):
- **Name**: `RAILWAY_TOKEN`
- **Value**: Your Railway API token

- **Name**: `RAILWAY_SERVICE_ID`
- **Value**: Your service ID (from URL)

- **Name**: `RAILWAY_ENVIRONMENT_ID`
- **Value**: Your environment ID (usually `production`)

### Step 4: Test the Setup

The workflow is already updated! Now test it:

```bash
# Make a small change
echo "# Test webhook deployment" >> README.md

# Commit and push
git add README.md
git commit -m "test: Verify webhook deployment after CI"
git push origin main
```

### Step 5: Verify It Works

**GitHub Actions** (~2-3 minutes):
1. Go to: https://github.com/Luciano-Grana/techcorp-policy-qa/actions
2. Watch the workflow run
3. `build-and-test` job completes
4. `deploy` job triggers Railway webhook
5. Should see: "✅ Tests passed! Triggering Railway deployment..."

**Railway** (after GitHub Actions completes):
1. Go to: https://railway.app → Deployments
2. Should see NEW deployment starting AFTER CI completes
3. Not immediate like before!

## Expected Flow

```
1. Push to main
   ↓
2. GitHub Actions starts (~2-3 min)
   - Install dependencies
   - Run smoke tests
   - Check formatting
   ↓
3. Tests PASS ✅
   ↓
4. Deploy job triggers Railway webhook
   ↓
5. Railway starts building (~5-7 min)
   ↓
6. Deployment complete ✅

Total time: ~8-10 minutes
Railway only deploys if CI passes!
```

## Troubleshooting

### Railway Still Auto-Deploys

**Issue**: Railway deploys immediately, webhook also triggers

**Solution**:
- Make sure you disconnected GitHub in Railway settings
- Or disabled "Automatic Deployments"

### Webhook Returns Error

**Issue**: Webhook URL doesn't work

**Solution**:
- Try the API method instead
- Ensure webhook URL is correct
- Check Railway documentation for current webhook format

### No Deployment Triggered

**Issue**: Tests pass but Railway doesn't deploy

**Solution**:
- Check GitHub Actions logs for webhook call
- Verify secret `RAILWAY_WEBHOOK_URL` is set correctly
- Try using Railway API method instead

## Current Configuration

Your `.github/workflows/ci-cd.yml` now has TWO deployment methods:

**Method 1: Webhook** (tries first if `RAILWAY_WEBHOOK_URL` exists)
```yaml
curl -X POST "$RAILWAY_WEBHOOK_URL" -H "Content-Type: application/json" -d '{"branch": "main"}'
```

**Method 2: API** (fallback if `RAILWAY_TOKEN` and `RAILWAY_SERVICE_ID` exist)
```yaml
curl -X POST https://backboard.railway.app/graphql/v2 ...
```

Set up whichever secrets you have available!

## Benefits

✅ Railway ONLY deploys after CI passes
✅ Prevents broken code from reaching production
✅ Professional CI/CD workflow
✅ Full control over deployment timing
✅ Works with Railway hobby tier

## Summary

1. ✅ Disable Railway auto-deploy
2. ✅ Get webhook URL or API token
3. ✅ Add to GitHub secrets
4. ✅ Workflow updated (already done)
5. ✅ Test with a push
6. ✅ Verify Railway deploys AFTER CI passes

This is the proper way to ensure CI gates deployment on Railway!
