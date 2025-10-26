"""
Embedding generation using free-tier models.
"""

from typing import List
import os
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """Wrapper for embedding models."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model.

        Args:
            model_name: Name of the sentence-transformers model to use
                       Default is a good free model with 384 dimensions
        """
        self.model_name = model_name
        # Load model with memory optimization for low-RAM environments
        self.model = SentenceTransformer(model_name, device='cpu')
        # Reduce memory footprint
        self.model.max_seq_length = 256  # Reduce from default 512
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,  # Disable progress bar to save memory
            convert_to_numpy=True,
            batch_size=8  # Smaller batch size for low memory
        )
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a single query.

        Args:
            query: Query text to embed

        Returns:
            Embedding vector
        """
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding.tolist()


# Alternative: Cohere embeddings (free tier)
# Uncomment if you prefer to use Cohere
"""
import cohere

class CohereEmbedding:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        self.client = cohere.Client(self.api_key)
        self.embedding_dim = 1024  # embed-english-light-v3.0

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embed(
            texts=texts,
            model="embed-english-light-v3.0",
            input_type="search_document"
        )
        return response.embeddings

    def embed_query(self, query: str) -> List[float]:
        response = self.client.embed(
            texts=[query],
            model="embed-english-light-v3.0",
            input_type="search_query"
        )
        return response.embeddings[0]
"""


if __name__ == "__main__":
    # Test embeddings
    embedder = EmbeddingModel()
    print(f"Using model: {embedder.model_name}")
    print(f"Embedding dimension: {embedder.embedding_dim}")

    # Test single query embedding
    query = "What is the PTO policy?"
    query_embedding = embedder.embed_query(query)
    print(f"\nQuery embedding shape: {len(query_embedding)}")

    # Test document embeddings
    docs = [
        "Employees receive 15-25 days of PTO per year",
        "Remote work is available to eligible employees",
        "Health insurance coverage begins on first day"
    ]
    doc_embeddings = embedder.embed_documents(docs)
    print(f"Document embeddings shape: {len(doc_embeddings)} x {len(doc_embeddings[0])}")
