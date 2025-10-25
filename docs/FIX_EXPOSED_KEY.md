# Fix Exposed API Key - Complete Guide

## What Happened

Your OpenRouter API key was accidentally committed to GitHub in documentation files. OpenRouter detected this and disabled the key for security.

**Files affected**:
- `docs/OPENROUTER_SETUP.md`
- `docs/DEPLOY_TO_RENDER.md`

**Status**: ✅ Keys removed from documentation files

---

## Step-by-Step Fix

### Step 1: Get a New OpenRouter API Key (2 minutes)

1. **Go to OpenRouter**: https://openrouter.ai/keys

2. **Sign in** with your existing account

3. **Delete the old key** (ending in `...a0de`)
   - Click the trash icon next to the compromised key
   - Confirm deletion

4. **Create a new key**:
   - Click "Create Key"
   - Name it: "TechCorp Policy QA - Production"
   - Click "Create"
   - **Copy the key** (starts with `sk-or-v1-...`)

5. **⚠️ IMPORTANT**: Save this key securely - you'll need it for the next steps

---

### Step 2: Update Your Local .env File (1 minute)

```bash
# Edit your .env file
nano .env

# Replace the old key with your new key:
OPENROUTER_API_KEY=sk-or-v1-YOUR_NEW_KEY_HERE
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=500
RAG_TOP_K=5
FLASK_DEBUG=False
PORT=5000

# Save and exit (Ctrl+O, Enter, Ctrl+X)
```

---

### Step 3: Clean Git History (5 minutes)

The exposed key is in your GitHub repository history. We need to remove it completely.

**Option A: Force Push with Amended History (Recommended for new repos)**

```bash
# 1. Check current status
git status

# 2. Stage the fixed documentation files
git add docs/OPENROUTER_SETUP.md docs/DEPLOY_TO_RENDER.md

# 3. Commit the security fix
git commit -m "security: Remove exposed API keys from documentation

- Replace actual API keys with placeholders
- Add instructions to obtain keys from OpenRouter
- Ensure .env remains in .gitignore"

# 4. Force push to overwrite history
git push origin main --force
```

**Option B: Delete and Recreate Repository (Cleanest option)**

```bash
# 1. Go to GitHub: https://github.com/YOUR_USERNAME/techcorp-policy-qa
# 2. Settings → Scroll down → Delete this repository
# 3. Confirm deletion

# 4. Create a new repository with the same name

# 5. Remove old git history and start fresh
rm -rf .git
git init
git add .
git commit -m "Initial commit: RAG policy Q&A application (secure)"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/techcorp-policy-qa.git
git push -u origin main
```

**⚠️ Note**: Option B is cleaner but you'll lose commit history and GitHub stars/forks

---

### Step 4: Verify Key is Not in Repository (1 minute)

```bash
# Search for any remaining keys in your codebase
grep -r "sk-or-v1-" . --exclude-dir=venv --exclude-dir=.git --exclude-dir=chroma_db

# Expected output: Only find it in .env (which is in .gitignore)
./.env:OPENROUTER_API_KEY=sk-or-v1-YOUR_NEW_KEY_HERE

# Verify .env is in .gitignore
cat .gitignore | grep ".env"
# Should show: .env
```

---

### Step 5: Test Locally (2 minutes)

```bash
# Test that your new key works
python3 app.py

# You should see:
# ✓ Using OpenRouter API
# ✓ Vector store loaded with 125 documents
# ✓ RAG pipeline initialized
```

Visit http://localhost:5000 and test the chatbot.

---

### Step 6: Deploy to Render (10 minutes)

Now that your repo is clean, deploy to Render:

1. **Go to Render**: https://dashboard.render.com

2. **Create New Web Service**:
   - Connect your GitHub repository
   - Select `techcorp-policy-qa`

3. **Configure Service**:
   - Name: `techcorp-policy-qa`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2`

4. **⚠️ CRITICAL: Add Environment Variables**:

   | Key | Value |
   |-----|-------|
   | `OPENROUTER_API_KEY` | Your **NEW** API key (sk-or-v1-...) |
   | `LLM_MODEL` | `meta-llama/llama-3.1-8b-instruct:free` |
   | `LLM_TEMPERATURE` | `0.1` |
   | `LLM_MAX_TOKENS` | `500` |
   | `RAG_TOP_K` | `5` |
   | `FLASK_DEBUG` | `False` |
   | `PYTHON_VERSION` | `3.10.12` |

5. **Click "Create Web Service"**

6. **Wait for deployment** (~10 minutes)

7. **Test your production URL**

---

## Prevention: Never Commit Keys Again

### ✅ What's Already Protected

Your repository is already set up with:

1. **`.gitignore`** includes `.env` ✓
2. **`.env.example`** has placeholders only ✓
3. **Documentation** now uses placeholders ✓

### 🛡️ Additional Protection (Optional)

Install `git-secrets` to prevent accidental commits:

```bash
# Install git-secrets (macOS)
brew install git-secrets

# Initialize in your repo
cd /Users/lucianograna/Quantic-AI-Project
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'sk-or-v1-[a-zA-Z0-9]+'
git secrets --add 'OPENROUTER_API_KEY=[a-zA-Z0-9-]+'

# Test it works
echo "sk-or-v1-test123" > test.txt
git add test.txt
git commit -m "test"
# Should block the commit!
```

---

## Checklist

Before deploying, verify:

- [ ] Got new OpenRouter API key
- [ ] Updated local `.env` with new key
- [ ] Tested app locally with new key
- [ ] Removed exposed key from docs (✅ Already done)
- [ ] Cleaned Git history (force push OR delete/recreate repo)
- [ ] Verified `.env` is in `.gitignore`
- [ ] Searched repo for any remaining keys
- [ ] Deployed to Render with new key in environment variables

---

## Security Best Practices

### ✅ DO:
- Store keys in `.env` file (gitignored)
- Use environment variables on Render
- Use `.env.example` with placeholders
- Rotate keys periodically

### ❌ DON'T:
- Commit `.env` to Git
- Put keys in documentation
- Put keys in code files
- Share keys in screenshots
- Put keys in commit messages

---

## What About the Old Key?

The old key (ending in `...a0de`) has been **disabled by OpenRouter** and cannot be used. You don't need to do anything else - it's dead.

---

## Need Help?

If you run into issues:

1. **OpenRouter API Issues**: Check https://openrouter.ai/docs
2. **Git Issues**: See https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
3. **Render Issues**: Check https://render.com/docs

---

## Summary

1. ✅ Documentation cleaned (keys removed)
2. 🔑 Get new OpenRouter API key
3. 📝 Update local `.env`
4. 🗑️ Clean Git history (force push or recreate repo)
5. ✅ Verify no keys in repo
6. 🚀 Deploy to Render with new key

**Total time**: ~20 minutes

Your app will be secure and deployed! 🎉
