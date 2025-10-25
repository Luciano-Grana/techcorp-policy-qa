# Virtual Environment Fix

## Issue
You're running from a virtual environment (`venv`) but the packages are installed globally, not inside the venv.

**Error**: `ModuleNotFoundError: No module named 'flask'`

---

## ✅ Solution

You have **two options**:

### Option 1: Install in Virtual Environment (Recommended)

Run these commands in your terminal (while venv is activated):

```bash
# Make sure you're in the project directory
cd /Users/lucianograna/Quantic-AI-Project

# Your venv should already be activated (you see "(venv)" in prompt)
# If not activated, run:
source venv/bin/activate

# Install all requirements in the venv
pip install -r requirements.txt
```

This will take 2-3 minutes. Then run:

```bash
python app.py
```

---

### Option 2: Deactivate Virtual Environment (Quick Fix)

If you want to use the globally installed packages:

```bash
# Deactivate the virtual environment
deactivate

# Now run with python3 (uses global packages)
python3 app.py
```

---

## ✅ Recommended: Use Virtual Environment

Virtual environments are best practice because they:
- Keep project dependencies isolated
- Prevent conflicts between projects
- Make deployment easier
- Match production environment

---

## Step-by-Step: Install in Venv

```bash
# 1. Make sure venv is activated (you should see "(venv)" in prompt)
source venv/bin/activate

# 2. Upgrade pip in venv
pip install --upgrade pip

# 3. Install requirements
pip install -r requirements.txt

# This will install:
# - Flask
# - ChromaDB
# - OpenAI
# - sentence-transformers
# - All other dependencies
```

**Installation time**: ~2-3 minutes

---

## Verify Installation

After installation, verify:

```bash
# Check Flask is installed in venv
python -c "import flask; print('✓ Flask installed')"

# Check ChromaDB
python -c "import chromadb; print('✓ ChromaDB installed')"

# Check OpenAI
python -c "import openai; print('✓ OpenAI installed')"
```

You should see all three checkmarks.

---

## Then Run the App

```bash
# With venv activated
python app.py

# Or
python3 app.py
```

Both should work once packages are installed in venv.

---

## Why This Happened

When I ran the installation earlier, I used `python3` which installed packages globally (system-wide). But when you run from inside a venv, Python looks for packages in the venv first, not the global installation.

---

## Quick Commands

```bash
# Activate venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run app
python app.py

# When done (to exit venv)
deactivate
```

---

## Troubleshooting

### "pip: command not found" in venv
Try: `python -m pip install -r requirements.txt`

### Installation is slow
This is normal - ChromaDB and sentence-transformers are large packages.

### Out of space error
Need ~2GB free space for all dependencies.

### Still getting import errors
Make sure you're running from the project directory where `requirements.txt` is.

---

## What to Do Now

1. **Activate venv**: `source venv/bin/activate`
2. **Install packages**: `pip install -r requirements.txt`
3. **Wait 2-3 minutes** for installation
4. **Run app**: `python app.py`
5. **Open browser**: http://localhost:5000

---

That's it! Once packages are installed in your venv, everything will work. 🚀
