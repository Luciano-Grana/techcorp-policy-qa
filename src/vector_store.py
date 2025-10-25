"""
Vector store using ChromaDB for document retrieval.
"""

import os
from typing import List, Dict, Tuple
import chromadb
from chromadb.config import Settings
from src.document_processor import Document
from src.embeddings import EmbeddingModel


class VectorStore:
    """Vector store for document embeddings and retrieval."""

    def __init__(self, persist_directory: str = "chroma_db", collection_name: str = "policies"):
        """
        Initialize vector store.

        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )

        # Initialize embedding model
        self.embedder = EmbeddingModel()

    def add_documents(self, documents: List[Document]):
        """
        Add documents to the vector store.

        Args:
            documents: List of Document objects to add
        """
        if not documents:
            return

        # Extract texts and metadata
        texts = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = [doc.id for doc in documents]

        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} documents...")
        embeddings = self.embedder.embed_documents(texts)

        # Add to collection in batches (ChromaDB has batch size limits)
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]

            self.collection.add(
                documents=batch_texts,
                metadatas=batch_metadatas,
                ids=batch_ids,
                embeddings=batch_embeddings
            )

        print(f"Added {len(texts)} documents to vector store")

    def search(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """
        Search for similar documents.

        Args:
            query: Query text
            k: Number of results to return

        Returns:
            List of (Document, similarity_score) tuples
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_query(query)

        # Search collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )

        # Convert results to Document objects
        documents = []
        for i in range(len(results['documents'][0])):
            doc = Document(
                content=results['documents'][0][i],
                metadata=results['metadatas'][0][i]
            )
            # Convert distance to similarity score (cosine distance to similarity)
            # ChromaDB returns squared L2 distance for cosine space
            similarity = 1 - results['distances'][0][i]
            documents.append((doc, similarity))

        return documents

    def reset(self):
        """Reset the vector store (delete all documents)."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        count = self.collection.count()
        return {
            "total_documents": count,
            "collection_name": self.collection_name,
            "embedding_dimension": self.embedder.embedding_dim
        }


if __name__ == "__main__":
    # Test vector store
    from src.document_processor import DocumentProcessor

    # Process documents
    processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    docs = processor.load_documents("data/policies")

    print(f"Processed {len(docs)} document chunks")

    # Create vector store
    store = VectorStore()

    # Reset if needed (for testing)
    # store.reset()

    # Add documents
    store.add_documents(docs)

    # Show stats
    stats = store.get_stats()
    print(f"\nVector store stats: {stats}")

    # Test search
    query = "How much PTO do employees get?"
    results = store.search(query, k=3)

    print(f"\nSearch results for: '{query}'\n")
    for i, (doc, score) in enumerate(results):
        print(f"Result {i+1} (score: {score:.3f})")
        print(f"Source: {doc.metadata['source']}")
        print(f"Doc ID: {doc.metadata['doc_id']}")
        print(f"Content: {doc.content[:200]}...")
        print()
