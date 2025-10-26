# Development Workflow

## Branch Strategy

This project uses a simple two-branch workflow to ensure Railway only deploys code that passes CI tests.

### Branches

- **`develop`**: Development branch - push your changes here
- **`main`**: Production branch - automatically updated by CI after tests pass, triggers Railway deployment

### How It Works

```
You push to develop
   ↓
GitHub Actions runs CI (~2-3 min)
   ↓
Tests PASS ✅
   ↓
GitHub Actions auto-merges develop → main
   ↓
Railway detects main branch update
   ↓
Railway deploys (~5-7 min)
   ↓
Live at: https://web-production-19d49a.up.railway.app
```

## Development Process

### 1. Make Changes on Develop Branch

```bash
# Make sure you're on develop
git checkout develop

# Make your changes to code
# ... edit files ...

# Stage and commit
git add .
git commit -m "feat: your feature description"

# Push to develop
git push origin develop
```

### 2. CI Runs Automatically

GitHub Actions will automatically:
- ✅ Install dependencies
- ✅ Run smoke tests (import validation)
- ✅ Check code formatting
- ✅ Run any unit tests (if available)

### 3. Auto-Merge to Main

If all tests pass:
- GitHub Actions automatically merges `develop` → `main`
- Merge commit includes `[skip ci]` to avoid re-running tests
- You'll see the merge commit in the `main` branch

### 4. Railway Deploys

- Railway is configured to deploy from the `main` branch only
- When `main` is updated, Railway automatically builds and deploys
- No "Wait for CI" configuration needed - main only updates after CI passes!

## Why This Works

**Problem**: Railway's "Wait for CI" feature doesn't reliably prevent immediate deployments.

**Solution**: Separate branches ensure Railway only sees updates to `main` AFTER tests pass:
1. You never push directly to `main`
2. CI runs on `develop` branch
3. Only passing code gets merged to `main`
4. Railway only deploys from `main`
5. Therefore, Railway only deploys tested code ✅

## Viewing CI Status

Check GitHub Actions: https://github.com/Luciano-Grana/techcorp-policy-qa/actions

You'll see:
1. `build-and-test` job running (~2-3 min)
2. If tests pass, `merge-to-main` job runs (~30 sec)
3. Green checkmarks indicate successful deployment

## Configuration Files

- [.github/workflows/ci-cd.yml](../.github/workflows/ci-cd.yml) - CI/CD pipeline configuration
- Railway Settings → Source → Deploy from `main` branch only

## Troubleshooting

### If CI Fails

Tests failed - merge to `main` is blocked:
1. Check GitHub Actions logs to see what failed
2. Fix the issue in your local `develop` branch
3. Push the fix - CI runs again
4. Only when tests pass will code reach `main` and deploy

### If You Need to Push Directly to Main

Emergency fixes only:
```bash
git checkout main
# Make fix
git add .
git commit -m "hotfix: critical issue [skip ci]"
git push origin main
```

Note: Use `[skip ci]` to prevent CI from running on `main` (since CI already ran on `develop`).

### Syncing Branches

If `develop` falls behind `main`:
```bash
git checkout develop
git merge main
git push origin develop
```

## Best Practices

1. **Always develop on `develop` branch**
2. **Never push directly to `main`** (except emergencies)
3. **Let CI handle the merge** - it's automatic!
4. **Monitor GitHub Actions** to ensure tests pass
5. **Check Railway logs** after deployment completes

---

**Key Takeaway**: Push to `develop` → CI tests → Auto-merge to `main` → Railway deploys ✅
