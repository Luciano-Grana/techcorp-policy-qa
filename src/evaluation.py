"""
Evaluation script for RAG pipeline with groundedness and citation accuracy metrics.
"""

import json
import time
import os
import sys
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables from .env file
load_dotenv()

from src.vector_store import VectorStore
from src.rag_pipeline import RAGPipeline


@dataclass
class EvaluationQuestion:
    """Evaluation question with expected answer and metadata."""
    question: str
    expected_answer: str = ""  # Optional: for exact/partial match
    relevant_doc_ids: List[str] = None  # Expected document IDs
    category: str = ""  # e.g., "PTO", "Security", "Remote Work"


@dataclass
class EvaluationResult:
    """Result of evaluating a single question."""
    question: str
    answer: str
    sources: List[Dict]
    latency_ms: int
    groundedness_score: float
    citation_accuracy_score: float
    exact_match: bool = False
    partial_match: bool = False
    category: str = ""


class Evaluator:
    """Evaluator for RAG pipeline."""

    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag_pipeline = rag_pipeline
        # Use the same client as the RAG pipeline (supports OpenRouter/OpenAI)
        self.client = rag_pipeline.client

    def evaluate_groundedness(self, answer: str, retrieved_chunks: List[str]) -> float:
        """
        Evaluate groundedness: % of answer content supported by retrieved evidence.

        Uses LLM to assess if answer is factually consistent with context.

        Returns:
            Score between 0 and 1
        """
        if not answer or not retrieved_chunks:
            return 0.0

        context = "\n\n".join(retrieved_chunks)

        prompt = f"""You are evaluating the groundedness of an AI-generated answer.

Groundedness means: ALL information in the answer is directly supported by and consistent with the provided context. The answer should not contain any information that is absent from or contradicted by the context.

Context (Retrieved Documents):
{context}

Answer to Evaluate:
{answer}

Evaluate the groundedness on a scale of 0-100:
- 100: All information in the answer is directly supported by the context
- 75: Most information is supported, minor unsupported details
- 50: About half is supported, significant unsupported content
- 25: Little information is supported
- 0: Answer is not grounded in the context at all

Respond with ONLY a number between 0 and 100."""

        try:
            response = self.client.chat.completions.create(
                model=self.rag_pipeline.model,
                messages=[
                    {"role": "system", "content": "You are an expert evaluator assessing answer quality."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=10
            )

            score_text = response.choices[0].message.content.strip()
            score = float(score_text) / 100.0

            return max(0.0, min(1.0, score))

        except Exception as e:
            print(f"Error evaluating groundedness: {e}")
            return 0.0

    def evaluate_citation_accuracy(self, answer: str, sources: List[Dict], retrieved_chunks: List[str]) -> float:
        """
        Evaluate citation accuracy: % of cited sources that correctly support the answer.

        Returns:
            Score between 0 and 1
        """
        if not sources or not answer:
            return 0.0

        # Check if answer contains source citations
        if not any(src['doc_id'] in answer for src in sources):
            # No citations in answer
            return 0.0

        context_with_sources = ""
        for i, (chunk, src) in enumerate(zip(retrieved_chunks, sources)):
            context_with_sources += f"\n\nSource {i+1} (Doc ID: {src['doc_id']}, File: {src['source']}):\n{chunk}"

        prompt = f"""You are evaluating citation accuracy.

Citation Accuracy means: The sources cited in the answer actually support the information attributed to them. Citations should not be misleading or incorrect.

Context with Source Information:
{context_with_sources}

Answer with Citations:
{answer}

Evaluate citation accuracy on a scale of 0-100:
- 100: All citations correctly point to supporting passages
- 75: Most citations are correct, minor issues
- 50: About half of citations are correct
- 25: Few citations are correct
- 0: Citations are incorrect or misleading

Respond with ONLY a number between 0 and 100."""

        try:
            response = self.client.chat.completions.create(
                model=self.rag_pipeline.model,
                messages=[
                    {"role": "system", "content": "You are an expert evaluator assessing citation quality."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=10
            )

            score_text = response.choices[0].message.content.strip()
            score = float(score_text) / 100.0

            return max(0.0, min(1.0, score))

        except Exception as e:
            print(f"Error evaluating citation accuracy: {e}")
            return 0.0

    def evaluate_exact_match(self, answer: str, expected: str) -> bool:
        """Check if answer exactly matches expected answer (case-insensitive)."""
        if not expected:
            return False

        answer_clean = answer.lower().strip()
        expected_clean = expected.lower().strip()

        return answer_clean == expected_clean

    def evaluate_partial_match(self, answer: str, expected: str) -> bool:
        """Check if answer contains key information from expected answer."""
        if not expected:
            return False

        # Simple partial match: check if key phrases are in answer
        answer_lower = answer.lower()
        expected_lower = expected.lower()

        # Split expected answer into key phrases (simple heuristic)
        key_phrases = [phrase.strip() for phrase in expected_lower.split(',')]

        # Check if majority of key phrases are in answer
        matches = sum(1 for phrase in key_phrases if phrase in answer_lower)
        return matches >= len(key_phrases) * 0.6  # 60% threshold

    def evaluate_question(self, question: EvaluationQuestion) -> EvaluationResult:
        """Evaluate a single question."""
        print(f"Evaluating: {question.question}")

        # Measure latency
        start_time = time.time()
        response = self.rag_pipeline.answer(question.question)
        latency_ms = int((time.time() - start_time) * 1000)

        # Evaluate groundedness
        groundedness = self.evaluate_groundedness(
            response.answer,
            response.retrieved_chunks
        )

        # Evaluate citation accuracy
        citation_accuracy = self.evaluate_citation_accuracy(
            response.answer,
            response.sources,
            response.retrieved_chunks
        )

        # Evaluate exact/partial match if expected answer provided
        exact_match = False
        partial_match = False
        if question.expected_answer:
            exact_match = self.evaluate_exact_match(response.answer, question.expected_answer)
            partial_match = self.evaluate_partial_match(response.answer, question.expected_answer)

        return EvaluationResult(
            question=question.question,
            answer=response.answer,
            sources=response.sources,
            latency_ms=latency_ms,
            groundedness_score=groundedness,
            citation_accuracy_score=citation_accuracy,
            exact_match=exact_match,
            partial_match=partial_match,
            category=question.category
        )

    def evaluate_dataset(self, questions: List[EvaluationQuestion]) -> Dict:
        """
        Evaluate full dataset and return metrics.

        Returns:
            Dictionary with aggregate metrics
        """
        results = []

        for question in questions:
            result = self.evaluate_question(question)
            results.append(result)

        # Calculate aggregate metrics
        latencies = [r.latency_ms for r in results]
        groundedness_scores = [r.groundedness_score for r in results]
        citation_scores = [r.citation_accuracy_score for r in results]

        metrics = {
            "total_questions": len(results),
            "groundedness": {
                "mean": float(np.mean(groundedness_scores)),
                "median": float(np.median(groundedness_scores)),
                "std": float(np.std(groundedness_scores)),
                "percentage_high_quality": float(sum(1 for s in groundedness_scores if s >= 0.8) / len(groundedness_scores) * 100)
            },
            "citation_accuracy": {
                "mean": float(np.mean(citation_scores)),
                "median": float(np.median(citation_scores)),
                "std": float(np.std(citation_scores)),
                "percentage_high_quality": float(sum(1 for s in citation_scores if s >= 0.8) / len(citation_scores) * 100)
            },
            "latency_ms": {
                "p50": float(np.percentile(latencies, 50)),
                "p95": float(np.percentile(latencies, 95)),
                "mean": float(np.mean(latencies)),
                "min": int(np.min(latencies)),
                "max": int(np.max(latencies))
            }
        }

        # Add exact/partial match if applicable
        exact_matches = [r for r in results if r.exact_match]
        partial_matches = [r for r in results if r.partial_match]

        if exact_matches or partial_matches:
            metrics["answer_matching"] = {
                "exact_match_count": len(exact_matches),
                "partial_match_count": len(partial_matches),
                "exact_match_percentage": len(exact_matches) / len(results) * 100,
                "partial_match_percentage": len(partial_matches) / len(results) * 100
            }

        # Category breakdown
        categories = {}
        for result in results:
            if result.category:
                if result.category not in categories:
                    categories[result.category] = []
                categories[result.category].append(result)

        if categories:
            metrics["by_category"] = {}
            for cat, cat_results in categories.items():
                cat_groundedness = [r.groundedness_score for r in cat_results]
                cat_citation = [r.citation_accuracy_score for r in cat_results]
                metrics["by_category"][cat] = {
                    "count": len(cat_results),
                    "groundedness_mean": float(np.mean(cat_groundedness)),
                    "citation_accuracy_mean": float(np.mean(cat_citation))
                }

        return {
            "metrics": metrics,
            "results": results
        }


def load_evaluation_dataset() -> List[EvaluationQuestion]:
    """Load evaluation questions."""
    questions = [
        # PTO Policy Questions
        EvaluationQuestion(
            question="How many days of PTO do employees get?",
            category="PTO",
            relevant_doc_ids=["POL-001"]
        ),
        EvaluationQuestion(
            question="How many PTO days do employees accrue after 3 years of service?",
            category="PTO",
            relevant_doc_ids=["POL-001"]
        ),
        EvaluationQuestion(
            question="What is the maximum PTO accrual limit?",
            category="PTO",
            relevant_doc_ids=["POL-001"]
        ),
        EvaluationQuestion(
            question="How many days of PTO can be carried over to next year?",
            category="PTO",
            relevant_doc_ids=["POL-001"]
        ),
        EvaluationQuestion(
            question="How far in advance should I request PTO?",
            category="PTO",
            relevant_doc_ids=["POL-001"]
        ),

        # Remote Work Questions
        EvaluationQuestion(
            question="What is the remote work policy?",
            category="Remote Work",
            relevant_doc_ids=["POL-002"]
        ),
        EvaluationQuestion(
            question="How many days per week can I work remotely in a hybrid schedule?",
            category="Remote Work",
            relevant_doc_ids=["POL-002"]
        ),
        EvaluationQuestion(
            question="What are the internet speed requirements for remote work?",
            category="Remote Work",
            relevant_doc_ids=["POL-002"]
        ),
        EvaluationQuestion(
            question="Do I need to use VPN when working remotely?",
            category="Remote Work",
            relevant_doc_ids=["POL-002"]
        ),
        EvaluationQuestion(
            question="Can I work remotely from another country?",
            category="Remote Work",
            relevant_doc_ids=["POL-002"]
        ),

        # Expense Reimbursement Questions
        EvaluationQuestion(
            question="What expenses can be reimbursed?",
            category="Expenses",
            relevant_doc_ids=["POL-003"]
        ),
        EvaluationQuestion(
            question="What is the hotel accommodation limit per night?",
            category="Expenses",
            relevant_doc_ids=["POL-003"]
        ),
        EvaluationQuestion(
            question="Can I expense alcoholic beverages?",
            category="Expenses",
            relevant_doc_ids=["POL-003"]
        ),
        EvaluationQuestion(
            question="What is the mileage reimbursement rate?",
            category="Expenses",
            relevant_doc_ids=["POL-003"]
        ),
        EvaluationQuestion(
            question="How long do I have to submit expense reports?",
            category="Expenses",
            relevant_doc_ids=["POL-003"]
        ),

        # Security Questions
        EvaluationQuestion(
            question="What are the password requirements?",
            category="Security",
            relevant_doc_ids=["POL-004"]
        ),
        EvaluationQuestion(
            question="Is multi-factor authentication required?",
            category="Security",
            relevant_doc_ids=["POL-004"]
        ),
        EvaluationQuestion(
            question="How should I report a security incident?",
            category="Security",
            relevant_doc_ids=["POL-004"]
        ),
        EvaluationQuestion(
            question="Can I use personal devices for work?",
            category="Security",
            relevant_doc_ids=["POL-004"]
        ),

        # Benefits Questions
        EvaluationQuestion(
            question="What health insurance plans are available?",
            category="Benefits",
            relevant_doc_ids=["POL-008"]
        ),
        EvaluationQuestion(
            question="What is the company 401k match?",
            category="Benefits",
            relevant_doc_ids=["POL-008"]
        ),
        EvaluationQuestion(
            question="Is there a gym membership reimbursement?",
            category="Benefits",
            relevant_doc_ids=["POL-008"]
        ),

        # Holidays Questions
        EvaluationQuestion(
            question="What holidays does the company observe?",
            category="Holidays",
            relevant_doc_ids=["POL-006"]
        ),
        EvaluationQuestion(
            question="How many weeks of parental leave are offered?",
            category="Holidays",
            relevant_doc_ids=["POL-006"]
        ),
        EvaluationQuestion(
            question="What is the sabbatical policy?",
            category="Holidays",
            relevant_doc_ids=["POL-006"]
        ),

        # Professional Development Questions
        EvaluationQuestion(
            question="What is the learning and development budget?",
            category="Learning",
            relevant_doc_ids=["POL-007"]
        ),
        EvaluationQuestion(
            question="Does the company provide tuition reimbursement?",
            category="Learning",
            relevant_doc_ids=["POL-007"]
        ),
        EvaluationQuestion(
            question="What online learning platforms are available?",
            category="Learning",
            relevant_doc_ids=["POL-007"]
        ),

        # Out-of-scope questions (should refuse to answer)
        EvaluationQuestion(
            question="What is the capital of France?",
            category="Out-of-scope",
            relevant_doc_ids=[]
        ),
        EvaluationQuestion(
            question="How do I bake a cake?",
            category="Out-of-scope",
            relevant_doc_ids=[]
        ),
    ]

    return questions


if __name__ == "__main__":
    # Run evaluation
    print("Loading RAG pipeline...")
    vector_store = VectorStore()
    rag_pipeline = RAGPipeline(vector_store=vector_store, top_k=5)

    print("\nLoading evaluation dataset...")
    questions = load_evaluation_dataset()
    print(f"Loaded {len(questions)} evaluation questions")

    print("\nRunning evaluation...")
    evaluator = Evaluator(rag_pipeline)
    evaluation_output = evaluator.evaluate_dataset(questions)

    # Print metrics
    metrics = evaluation_output["metrics"]
    print("\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80)

    print(f"\nTotal Questions: {metrics['total_questions']}")

    print("\nGroundedness:")
    print(f"  Mean: {metrics['groundedness']['mean']:.3f}")
    print(f"  Median: {metrics['groundedness']['median']:.3f}")
    print(f"  Std Dev: {metrics['groundedness']['std']:.3f}")
    print(f"  High Quality (≥0.8): {metrics['groundedness']['percentage_high_quality']:.1f}%")

    print("\nCitation Accuracy:")
    print(f"  Mean: {metrics['citation_accuracy']['mean']:.3f}")
    print(f"  Median: {metrics['citation_accuracy']['median']:.3f}")
    print(f"  Std Dev: {metrics['citation_accuracy']['std']:.3f}")
    print(f"  High Quality (≥0.8): {metrics['citation_accuracy']['percentage_high_quality']:.1f}%")

    print("\nLatency:")
    print(f"  P50: {metrics['latency_ms']['p50']:.0f}ms")
    print(f"  P95: {metrics['latency_ms']['p95']:.0f}ms")
    print(f"  Mean: {metrics['latency_ms']['mean']:.0f}ms")
    print(f"  Range: {metrics['latency_ms']['min']:.0f}ms - {metrics['latency_ms']['max']:.0f}ms")

    if "by_category" in metrics:
        print("\nBy Category:")
        for cat, cat_metrics in metrics["by_category"].items():
            print(f"\n  {cat}:")
            print(f"    Questions: {cat_metrics['count']}")
            print(f"    Groundedness: {cat_metrics['groundedness_mean']:.3f}")
            print(f"    Citation Accuracy: {cat_metrics['citation_accuracy_mean']:.3f}")

    # Save results
    os.makedirs("evaluation_results", exist_ok=True)

    # Save metrics
    with open("evaluation_results/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Save detailed results
    results_for_json = []
    for result in evaluation_output["results"]:
        results_for_json.append({
            "question": result.question,
            "answer": result.answer,
            "sources": result.sources,
            "latency_ms": result.latency_ms,
            "groundedness_score": result.groundedness_score,
            "citation_accuracy_score": result.citation_accuracy_score,
            "category": result.category
        })

    with open("evaluation_results/detailed_results.json", "w") as f:
        json.dump(results_for_json, f, indent=2)

    print("\n\nResults saved to evaluation_results/")
    print("  - metrics.json: Aggregate metrics")
    print("  - detailed_results.json: Per-question results")
