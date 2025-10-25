"""
Setup script for initializing the RAG application.
"""

import os
import sys
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore


def setup_vector_store():
    """Initialize and populate the vector store."""
    print("="*80)
    print("TechCorp Policy Q&A - Setup")
    print("="*80)

    # Check for documents
    policies_dir = "data/policies"
    if not os.path.exists(policies_dir):
        print(f"\nError: {policies_dir} directory not found!")
        print("Please ensure policy documents are in the data/policies/ directory.")
        sys.exit(1)

    policy_files = [f for f in os.listdir(policies_dir) if f.endswith('.md')]
    if not policy_files:
        print(f"\nError: No policy documents found in {policies_dir}!")
        print("Please add policy documents (.md files) to the data/policies/ directory.")
        sys.exit(1)

    print(f"\nFound {len(policy_files)} policy documents:")
    for f in policy_files:
        print(f"  - {f}")

    # Process documents
    print("\n" + "-"*80)
    print("Step 1: Processing and chunking documents...")
    print("-"*80)

    processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    documents = processor.load_documents(policies_dir)

    print(f"\nProcessed {len(documents)} document chunks")

    # Show sample
    if documents:
        print("\nSample chunk:")
        sample = documents[0]
        print(f"  Source: {sample.metadata['source']}")
        print(f"  Doc ID: {sample.metadata['doc_id']}")
        print(f"  Heading: {sample.metadata.get('heading', 'N/A')}")
        print(f"  Length: {len(sample.content)} chars")
        print(f"  Preview: {sample.content[:150]}...")

    # Initialize vector store
    print("\n" + "-"*80)
    print("Step 2: Initializing vector store...")
    print("-"*80)

    store = VectorStore(persist_directory="chroma_db")

    # Check if already populated
    stats = store.get_stats()
    if stats['total_documents'] > 0:
        print(f"\nVector store already contains {stats['total_documents']} documents.")
        response = input("Reset and re-index? (y/N): ")
        if response.lower() == 'y':
            print("Resetting vector store...")
            store.reset()
        else:
            print("Keeping existing index.")
            print("\nSetup complete!")
            return

    # Add documents to vector store
    print("\n" + "-"*80)
    print("Step 3: Generating embeddings and indexing...")
    print("-"*80)
    print("\nThis may take a few minutes for first-time setup...")

    store.add_documents(documents)

    # Show final stats
    final_stats = store.get_stats()
    print("\n" + "="*80)
    print("Setup Complete!")
    print("="*80)
    print(f"\nVector Store Statistics:")
    print(f"  Total documents: {final_stats['total_documents']}")
    print(f"  Embedding dimension: {final_stats['embedding_dimension']}")
    print(f"  Storage location: {store.persist_directory}")

    print("\nNext steps:")
    print("  1. Set up your .env file with API keys (copy from .env.example)")
    print("  2. Run the application: python app.py")
    print("  3. Open http://localhost:5000 in your browser")

    print("\n" + "="*80)


if __name__ == "__main__":
    try:
        setup_vector_store()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
