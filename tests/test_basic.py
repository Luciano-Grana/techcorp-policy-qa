"""
Basic smoke tests for the RAG application.
"""

import pytest
from src.document_processor import DocumentProcessor, Document
from src.embeddings import EmbeddingModel


def test_document_processor_initialization():
    """Test that DocumentProcessor can be initialized."""
    processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    assert processor.chunk_size == 1000
    assert processor.chunk_overlap == 200


def test_embedding_model_initialization():
    """Test that EmbeddingModel can be initialized."""
    embedder = EmbeddingModel()
    assert embedder.embedding_dim > 0


def test_document_creation():
    """Test Document object creation."""
    doc = Document(
        content="Test content",
        metadata={"source": "test.md", "doc_id": "TEST-001"}
    )
    assert doc.content == "Test content"
    assert doc.metadata["source"] == "test.md"
    assert doc.id is not None


def test_embed_single_query():
    """Test embedding a single query."""
    embedder = EmbeddingModel()
    query = "What is the PTO policy?"
    embedding = embedder.embed_query(query)

    assert isinstance(embedding, list)
    assert len(embedding) == embedder.embedding_dim
    assert all(isinstance(x, float) for x in embedding)


def test_embed_multiple_documents():
    """Test embedding multiple documents."""
    embedder = EmbeddingModel()
    docs = [
        "First document about PTO",
        "Second document about remote work",
        "Third document about expenses"
    ]
    embeddings = embedder.embed_documents(docs)

    assert len(embeddings) == 3
    assert all(len(emb) == embedder.embedding_dim for emb in embeddings)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
