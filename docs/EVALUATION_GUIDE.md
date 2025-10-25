# Evaluation Guide

## 📊 What Gets Evaluated

Your RAG system will be tested on **30 questions** measuring:

### 1. Information Quality Metrics (Required)

**Groundedness**
- Definition: % of answer content fully supported by retrieved documents
- Method: LLM evaluates if answer is factually consistent with context
- Target: Mean ≥ 0.80 (80%)

**Citation Accuracy**
- Definition: % of cited sources that correctly support the answer
- Method: LLM verifies citations point to correct passages
- Target: Mean ≥ 0.80 (80%)

### 2. System Metrics (Required)

**Latency**
- P50 (median): Typical response time
- P95 (95th percentile): Worst-case response time
- Target: P95 < 3000ms

### 3. Test Dataset

30 questions across 9 categories:
- PTO Policy (5 questions)
- Remote Work (5 questions)
- Expenses (5 questions)
- Security (4 questions)
- Benefits (3 questions)
- Holidays (3 questions)
- Learning (3 questions)
- Out-of-scope (2 questions) - tests refusal behavior

---

## 🚀 Running Evaluation

### Full Evaluation (30 questions)

```bash
python3 src/evaluation.py
```

**Time**: ~5-10 minutes with OpenRouter free tier
**Output**:
- `evaluation_results/metrics.json` - Aggregate metrics
- `evaluation_results/detailed_results.json` - Per-question results

### Quick Test (3 questions)

For faster testing, you can modify the script to test fewer questions.

---

## 📈 Expected Results

### Good Performance
```
Groundedness: ≥0.80 (80%)
Citation Accuracy: ≥0.80 (80%)
Latency P50: ~1500ms
Latency P95: <3000ms
```

### Sample Output
```
EVALUATION RESULTS
==================

Total Questions: 30

Groundedness:
  Mean: 0.87
  Median: 0.90
  High Quality (≥0.8): 83.3%

Citation Accuracy:
  Mean: 0.85
  Median: 0.88
  High Quality (≥0.8): 80.0%

Latency:
  P50: 1456ms
  P95: 2789ms
  Mean: 1678ms
```

---

## 🔍 Understanding the Metrics

### Groundedness Score

**1.0 (100%)**: All information in answer is directly from context
**0.8 (80%)**: Most information supported, minor unsupported details
**0.5 (50%)**: Half supported, significant hallucination
**0.0 (0%)**: Completely made up, not from documents

### Citation Accuracy Score

**1.0 (100%)**: All citations correctly point to supporting text
**0.8 (80%)**: Most citations correct
**0.5 (50%)**: Half of citations are wrong
**0.0 (0%)**: Citations are misleading or incorrect

### Latency

**P50 (Median)**: Half of requests faster, half slower
**P95 (95th percentile)**: 95% of requests faster than this
**Good**: P50 < 2s, P95 < 3s

---

## 📂 Output Files

### metrics.json
```json
{
  "total_questions": 30,
  "groundedness": {
    "mean": 0.87,
    "median": 0.90,
    "std": 0.12,
    "percentage_high_quality": 83.3
  },
  "citation_accuracy": {
    "mean": 0.85,
    "median": 0.88,
    "percentage_high_quality": 80.0
  },
  "latency_ms": {
    "p50": 1456,
    "p95": 2789,
    "mean": 1678
  },
  "by_category": {
    "PTO": {...},
    "Remote Work": {...}
  }
}
```

### detailed_results.json
Per-question breakdown with:
- Question text
- Generated answer
- Sources cited
- Latency
- Groundedness score
- Citation accuracy score

---

## ⚠️ Important Notes

### With OpenRouter Free Tier

- **May be slower**: Free tier can queue requests
- **Rate limits**: ~200 requests/day
- **Evaluation uses ~60 API calls**: 30 for Q&A + 30 for evaluation
- **If you hit limits**: Wait or use different free model

### Evaluation Uses LLM-as-Judge

- Uses the same OpenRouter model to evaluate answers
- Pros: Automated, repeatable, nuanced
- Cons: LLM judge may have biases
- Alternative: Manual human evaluation (more accurate but time-consuming)

---

## 🐛 Troubleshooting

### "Rate limit exceeded"
- OpenRouter free tier limit hit
- Wait 10-15 minutes
- Or switch model in .env

### Very slow evaluation
- Normal for free tier (may queue)
- Consider reducing test set size
- Or run during off-peak hours

### Low scores
- Check if documents cover the topics
- Review prompt engineering in src/rag_pipeline.py
- Adjust top_k or chunk_size
- Check retrieval quality

---

## 📝 For Your Project Report

Include these sections:

### Evaluation Methodology
- 30 questions across 9 categories
- Groundedness and citation accuracy (LLM-based)
- Latency metrics (P50, P95)

### Results
- Copy metrics from metrics.json
- Create charts/tables
- Compare to targets

### Analysis
- What worked well?
- Where did it struggle?
- What would improve it?

### Sample Responses
- Include 2-3 good examples
- Include 1-2 failure cases
- Show how system handles out-of-scope questions

---

## 🎯 Assignment Rubric

Your evaluation should demonstrate:

✅ Groundedness measurement (required)
✅ Citation accuracy measurement (required)
✅ Latency metrics (required)
✅ Test set of 15-30 questions (required)
✅ Results documented (required)

Optional enhancements:
- Exact/partial match metrics
- Category-wise breakdown
- Ablation studies (different k, chunk size)
- Error analysis

---

## Next Steps

1. **Run evaluation**: `python3 src/evaluation.py`
2. **Review results**: Check `evaluation_results/`
3. **Analyze**: Look for patterns in errors
4. **Iterate**: Improve prompts, chunking, or k
5. **Document**: Add results to your project report

---

**Ready to evaluate?** Run `python3 src/evaluation.py` now! 🚀
