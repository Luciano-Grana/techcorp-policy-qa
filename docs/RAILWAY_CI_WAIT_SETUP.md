# Railway "Wait for CI" Configuration Guide

Railway can wait for GitHub Actions to pass before deploying, but it needs to know which check to wait for.

## The Problem

By default, Railway deploys immediately on push without waiting for tests to complete.

## The Solution

Configure Railway to wait for the `build-and-test` check from GitHub Actions.

## Setup Steps

### Option 1: Configure in Railway (Preferred)

1. **Go to Railway Dashboard**: https://railway.app
2. **Select your service**: `techcorp-policy-qa`
3. **Settings** → **Deploy** section
4. **Toggle "Wait for CI"**: ON ✅
5. **If there's a "Check Name" field**: Enter `build-and-test`
6. **Save settings**

### Option 2: Set Required Check in GitHub (Alternative)

If Railway doesn't have a specific check name field, make `build-and-test` a required check:

1. **Go to GitHub repository**: https://github.com/Luciano-Grana/techcorp-policy-qa
2. **Settings** → **Branches** → **Add branch protection rule**
3. **Branch name pattern**: `main`
4. **Enable**: ✅ Require status checks to pass before merging
5. **Select status checks**: `build-and-test`
6. **Enable**: ✅ Require branches to be up to date before merging
7. **Create** or **Save changes**

Once configured, Railway will automatically wait for this required check.

## How to Verify It's Working

### Test the Configuration:

1. **Make a small change** (e.g., update a comment in code)
2. **Commit and push** to `main` branch
3. **Watch Railway dashboard** → Deployments tab

**Expected behavior**:
```
GitHub Actions           Railway Deployment
    ⏳ Running       →   ⏸️  Waiting for CI
    (2-3 min)
        ↓
    ✅ Passed        →   ⏳ Building
                         (5-7 min)
                             ↓
                         ✅ Deployed
```

**If Railway starts building immediately** (before GitHub Actions completes):
- ❌ Wait for CI is not properly configured
- Check the settings again

**If Railway shows "Waiting for CI"**:
- ✅ Configuration is correct!
- Railway will deploy after GitHub Actions passes

## Understanding the GitHub Check Name

From `.github/workflows/ci-cd.yml`:

```yaml
jobs:
  build-and-test:    # ← This is the check name
    runs-on: ubuntu-latest
    steps:
      ...
```

The job name `build-and-test` becomes the GitHub check that Railway monitors.

## Troubleshooting

### Railway Still Deploys Immediately

**Possible causes**:
1. "Wait for CI" toggle is OFF
2. Check name not configured (if Railway requires it)
3. No required checks set in GitHub branch protection

**Solution**:
- Verify toggle is ON in Railway settings
- Set up branch protection in GitHub (Option 2 above)
- Contact Railway support if issue persists

### Railway Never Deploys (Stuck on "Waiting")

**Possible causes**:
1. GitHub Actions workflow is failing
2. Wrong check name configured
3. GitHub permissions issue

**Solution**:
- Check GitHub Actions results (should show green checkmark)
- Verify check name is exactly `build-and-test`
- Ensure Railway has proper GitHub OAuth permissions

### How to Check Current Status

**GitHub Actions**:
- Go to: https://github.com/Luciano-Grana/techcorp-policy-qa/actions
- See if workflow is passing (green ✅) or failing (red ❌)

**Railway**:
- Go to: https://railway.app → Deployments
- See deployment status and logs

## Best Practice

**Always use "Wait for CI"** for production deployments:
- ✅ Prevents broken code from reaching production
- ✅ Ensures tests pass before deployment
- ✅ Professional CI/CD workflow
- ✅ Catches errors early

## Current Configuration

For this project:
- **GitHub Actions workflow**: `.github/workflows/ci-cd.yml`
- **Check name to wait for**: `build-and-test`
- **Required for**: Pushes to `main` branch
- **Expected wait time**: 2-3 minutes (for tests to complete)

Once properly configured, every deployment to `main` will:
1. Run automated tests first
2. Wait for tests to pass
3. Only deploy if tests succeed
4. Provide safe, reliable deployments

---

**Note**: If you're still having issues after following these steps, the simplest solution is to set up GitHub branch protection (Option 2). This makes the check "required" and Railway will definitely respect it.
