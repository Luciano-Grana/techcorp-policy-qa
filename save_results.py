"""
Quick script to save the evaluation results you already have.
Just copy-paste your metrics into this file and run it.
"""

import json
import os

# Your evaluation results from the terminal output
metrics = {
    "total_questions": 30,
    "groundedness": {
        "mean": 0.883,
        "median": 1.000,
        "std": 0.301,
        "percentage_high_quality": 83.3
    },
    "citation_accuracy": {
        "mean": 0.917,
        "median": 1.000,
        "std": 0.253,
        "percentage_high_quality": 86.7
    },
    "latency_ms": {
        "p50": 991,
        "p95": 2100,
        "mean": 1122,
        "min": 31,
        "max": 2374
    },
    "by_category": {
        "PTO": {
            "count": 5,
            "groundedness_mean": 0.900,
            "citation_accuracy_mean": 0.950
        },
        "Remote Work": {
            "count": 5,
            "groundedness_mean": 1.000,
            "citation_accuracy_mean": 0.950
        },
        "Expenses": {
            "count": 5,
            "groundedness_mean": 1.000,
            "citation_accuracy_mean": 1.000
        },
        "Security": {
            "count": 4,
            "groundedness_mean": 1.000,
            "citation_accuracy_mean": 1.000
        },
        "Benefits": {
            "count": 3,
            "groundedness_mean": 1.000,
            "citation_accuracy_mean": 1.000
        },
        "Holidays": {
            "count": 3,
            "groundedness_mean": 0.667,
            "citation_accuracy_mean": 1.000
        },
        "Learning": {
            "count": 3,
            "groundedness_mean": 1.000,
            "citation_accuracy_mean": 1.000
        },
        "Out-of-scope": {
            "count": 2,
            "groundedness_mean": 0.000,
            "citation_accuracy_mean": 0.000
        }
    }
}

# Save to file
os.makedirs("evaluation_results", exist_ok=True)

with open("evaluation_results/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("✓ Saved metrics to evaluation_results/metrics.json")
print("\nYour RAG system performance:")
print(f"  Groundedness: {metrics['groundedness']['mean']:.1%} (Target: ≥80%) ✅")
print(f"  Citation Accuracy: {metrics['citation_accuracy']['mean']:.1%} (Target: ≥80%) ✅")
print(f"  Latency P95: {metrics['latency_ms']['p95']}ms (Target: <3000ms) ✅")
print("\n🎉 All targets exceeded!")
