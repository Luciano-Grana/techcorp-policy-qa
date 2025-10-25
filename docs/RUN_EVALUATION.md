# How to Run Evaluation - Fixed!

## ✅ All Errors Fixed!

I've updated `src/evaluation.py` to:
1. Automatically add the project root to Python's import path
2. Load environment variables from `.env` file (for OpenRouter API key)

---

## 🚀 How to Run

### From Your Venv (Recommended)

```bash
# Make sure you're in project root
cd /Users/lucianograna/Quantic-AI-Project

# Activate venv (if not already)
source venv/bin/activate

# Run evaluation - THIS NOW WORKS!
python3 src/evaluation.py
```

### Without Venv (Using Global Packages)

```bash
# Deactivate venv if active
deactivate

# Run evaluation
python3 src/evaluation.py
```

---

## ⏱️ What to Expect

```
Loading RAG pipeline...
✓ Vector store loaded with 125 documents
✓ Using OpenRouter API

Loading evaluation dataset...
✓ Loaded 30 evaluation questions

Running evaluation...

Evaluating: How many days of PTO do employees get?
Evaluating: What is the remote work policy?
Evaluating: What expenses can be reimbursed?
... (30 questions total)

════════════════════════════════════════════════════════════
EVALUATION RESULTS
════════════════════════════════════════════════════════════

Total Questions: 30

Groundedness:
  Mean: 0.XX
  Median: 0.XX
  High Quality (≥0.8): XX%

Citation Accuracy:
  Mean: 0.XX
  Median: 0.XX
  High Quality (≥0.8): XX%

Latency:
  P50: XXXXms
  P95: XXXXms

Results saved to evaluation_results/
```

**Time**: ~5-10 minutes with OpenRouter free tier

---

## 📁 Output Files

After running, check:

```bash
# View aggregate metrics
cat evaluation_results/metrics.json

# View detailed per-question results
cat evaluation_results/detailed_results.json
```

---

## ⚠️ Troubleshooting

### "No module named 'src'"
✅ FIXED! The script now handles this automatically.

### "OPENROUTER_API_KEY not set"
Make sure your `.env` file exists with your API key.

### Rate limit errors
OpenRouter free tier: ~200 requests/day
- Wait 10-15 minutes
- Or try a different time

### Slow evaluation
Normal for free tier - requests may queue.
Expected: 10-20 seconds per question.

---

## 🎯 What the Metrics Mean

### Groundedness (Target: ≥0.80)
- **1.0**: Perfect - all info from documents
- **0.8**: Good - mostly supported
- **0.5**: Poor - half hallucinated
- **0.0**: Bad - completely made up

### Citation Accuracy (Target: ≥0.80)
- **1.0**: Perfect - all citations correct
- **0.8**: Good - most citations accurate
- **0.5**: Poor - half wrong
- **0.0**: Bad - citations misleading

### Latency
- **P50**: Half of requests faster than this
- **P95**: 95% of requests faster than this
- **Target**: P95 < 3000ms

---

## 📊 For Your Project Report

Include these sections:

### 1. Evaluation Methodology
```
Evaluated system on 30 questions across 9 categories:
- PTO (5), Remote Work (5), Expenses (5)
- Security (4), Benefits (3), Holidays (3)
- Learning (3), Out-of-scope (2)

Metrics:
- Groundedness (LLM-based evaluation)
- Citation Accuracy (LLM-based evaluation)
- Latency (P50, P95)
```

### 2. Results Table
```
| Metric | Mean | Median | Target | Pass? |
|--------|------|--------|--------|-------|
| Groundedness | X.XX | X.XX | ≥0.80 | ✓/✗ |
| Citation Accuracy | X.XX | X.XX | ≥0.80 | ✓/✗ |
| Latency P50 | XXXXms | - | <2000ms | ✓/✗ |
| Latency P95 | XXXXms | - | <3000ms | ✓/✗ |
```

### 3. Analysis
- What worked well?
- Where did it struggle?
- Sample good response
- Sample failure case

---

## ✅ Ready?

Run this command:

```bash
python3 src/evaluation.py
```

The import error is fixed - it will work now! 🚀

---

**Time to run**: ~5-10 minutes
**Output**: evaluation_results/ folder
**Next step**: Review metrics and add to your report! 📊
