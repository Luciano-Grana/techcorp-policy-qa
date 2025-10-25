"""
RAG pipeline for question answering over policy documents.
"""

import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from openai import OpenAI
from src.vector_store import VectorStore
from src.document_processor import Document


@dataclass
class RAGResponse:
    """Response from RAG pipeline."""
    answer: str
    sources: List[Dict[str, str]]
    retrieved_chunks: List[str]
    confidence: float = 0.0


class RAGPipeline:
    """RAG pipeline for policy Q&A."""

    def __init__(
        self,
        vector_store: VectorStore,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.1,
        max_tokens: int = 500,
        top_k: int = 5
    ):
        """
        Initialize RAG pipeline.

        Args:
            vector_store: VectorStore instance
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: LLM model to use
            temperature: Temperature for generation
            max_tokens: Maximum tokens in response
            top_k: Number of documents to retrieve
        """
        self.vector_store = vector_store
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_k = top_k

        # Initialize LLM client - supports OpenRouter, OpenAI, or Groq
        # Check for OpenRouter first, then OpenAI
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set OPENROUTER_API_KEY or OPENAI_API_KEY environment variable.")

        # Create OpenAI client for OpenRouter or OpenAI
        if os.getenv("OPENROUTER_API_KEY"):
            # Use OpenRouter with proper client initialization
            self.client = OpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://github.com/Luciano-Grana/techcorp-policy-qa",
                    "X-Title": "TechCorp Policy Q&A"
                }
            )
            print("Using OpenRouter API")
        else:
            # Use OpenAI
            self.client = OpenAI(api_key=self.api_key)
            print("Using OpenAI API")

        # System prompt for the LLM
        self.system_prompt = """You are a helpful assistant that answers questions about TechCorp company policies.

IMPORTANT GUIDELINES:
1. ONLY answer questions based on the provided policy documents
2. If the answer is not in the provided context, say "I can only answer questions about our company policies. This information is not available in the policy documents I have access to."
3. Always cite your sources using the Document ID and source filename
4. Be concise and direct in your answers
5. If you're unsure, say so rather than making up information
6. Include specific details like numbers, dates, and requirements when available in the context

When answering:
- Start with a direct answer to the question
- Provide relevant details from the policy documents
- End with citations in the format: [Source: document_name, Doc ID: POL-XXX]
"""

    def retrieve(self, query: str) -> List[Tuple[Document, float]]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: User query

        Returns:
            List of (Document, similarity_score) tuples
        """
        return self.vector_store.search(query, k=self.top_k)

    def _format_context(self, documents: List[Tuple[Document, float]]) -> str:
        """Format retrieved documents as context for LLM."""
        context_parts = []

        for i, (doc, score) in enumerate(documents):
            context_parts.append(f"""
Document {i+1}:
Source: {doc.metadata['source']}
Document ID: {doc.metadata['doc_id']}
Section: {doc.metadata.get('heading', 'N/A')}
Similarity: {score:.3f}

Content:
{doc.content}
""")

        return "\n---\n".join(context_parts)

    def _extract_sources(self, documents: List[Tuple[Document, float]]) -> List[Dict[str, str]]:
        """Extract source information from documents."""
        sources = []
        seen = set()

        for doc, score in documents:
            source_key = f"{doc.metadata['doc_id']}:{doc.metadata['source']}"
            if source_key not in seen:
                sources.append({
                    "doc_id": doc.metadata['doc_id'],
                    "source": doc.metadata['source'],
                    "heading": doc.metadata.get('heading', ''),
                    "similarity": f"{score:.3f}"
                })
                seen.add(source_key)

        return sources

    def _is_policy_related(self, query: str) -> bool:
        """
        Check if query is related to company policies.
        This is a simple heuristic - could be improved with a classifier.
        """
        policy_keywords = [
            'policy', 'pto', 'vacation', 'leave', 'remote', 'work from home',
            'expense', 'reimbursement', 'security', 'password', 'benefit',
            'insurance', 'holiday', '401k', 'retirement', 'parental', 'sick',
            'bereavement', 'jury', 'sabbatical', 'development', 'training',
            'conference', 'code of conduct', 'harassment', 'discrimination',
            'techcorp', 'company', 'employee', 'manager', 'hr'
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in policy_keywords)

    def answer(self, query: str) -> RAGResponse:
        """
        Answer a question using RAG.

        Args:
            query: User question

        Returns:
            RAGResponse object
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(query)

        # Check if any relevant documents were found
        if not retrieved_docs or retrieved_docs[0][1] < 0.3:  # Similarity threshold
            return RAGResponse(
                answer="I can only answer questions about our company policies. This information is not available in the policy documents I have access to.",
                sources=[],
                retrieved_chunks=[],
                confidence=0.0
            )

        # Format context
        context = self._format_context(retrieved_docs)

        # Create prompt
        user_prompt = f"""Based on the following policy documents, please answer this question:

Question: {query}

Policy Documents:
{context}

Remember to cite your sources and only use information from the provided documents."""

        # Call LLM
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            answer = response.choices[0].message.content

            # Extract sources
            sources = self._extract_sources(retrieved_docs)

            # Extract retrieved chunks
            chunks = [doc.content for doc, _ in retrieved_docs]

            # Calculate confidence based on similarity scores
            avg_similarity = sum(score for _, score in retrieved_docs) / len(retrieved_docs)

            return RAGResponse(
                answer=answer,
                sources=sources,
                retrieved_chunks=chunks,
                confidence=avg_similarity
            )

        except Exception as e:
            return RAGResponse(
                answer=f"An error occurred while generating the answer: {str(e)}",
                sources=[],
                retrieved_chunks=[],
                confidence=0.0
            )

    def answer_with_reranking(self, query: str) -> RAGResponse:
        """
        Answer with optional re-ranking (simple implementation).

        This could be enhanced with a dedicated re-ranking model.
        """
        # For now, just use the standard answer method
        # In a production system, you might use a cross-encoder for re-ranking
        return self.answer(query)


if __name__ == "__main__":
    # Test RAG pipeline
    import sys

    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    # Initialize vector store
    store = VectorStore()

    # Initialize RAG pipeline
    rag = RAGPipeline(
        vector_store=store,
        model="gpt-3.5-turbo",
        top_k=5
    )

    # Test questions
    test_queries = [
        "How much PTO do employees get?",
        "What is the remote work policy?",
        "Can I expense my gym membership?",
        "What are the security requirements for passwords?",
    ]

    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Question: {query}")
        print(f"{'='*80}")

        response = rag.answer(query)

        print(f"\nAnswer:\n{response.answer}")
        print(f"\nConfidence: {response.confidence:.3f}")
        print(f"\nSources:")
        for source in response.sources:
            print(f"  - {source['source']} (Doc ID: {source['doc_id']}, Section: {source['heading']})")
