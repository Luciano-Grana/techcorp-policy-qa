"""
Flask web application for policy Q&A chatbot.
"""

import os
import time
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv
from src.vector_store import VectorStore
from src.rag_pipeline import RAGPipeline
from src.document_processor import DocumentProcessor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize RAG components
vector_store = None
rag_pipeline = None
initialization_done = False


def initialize_rag():
    """Initialize or load the RAG pipeline."""
    global vector_store, rag_pipeline, initialization_done

    if initialization_done:
        return

    print("Starting RAG initialization...")
    vector_store = VectorStore(persist_directory="chroma_db")

    # Check if vector store is empty
    stats = vector_store.get_stats()

    if stats['total_documents'] == 0:
        print("Vector store is empty. Indexing documents...")
        processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
        documents = processor.load_documents("data/policies")
        print(f"Loaded {len(documents)} document chunks")

        vector_store.add_documents(documents)
        print("Documents indexed successfully")
    else:
        print(f"Vector store loaded with {stats['total_documents']} documents")

    # Initialize RAG pipeline
    rag_pipeline = RAGPipeline(
        vector_store=vector_store,
        model=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "500")),
        top_k=int(os.getenv("RAG_TOP_K", "5"))
    )

    print("RAG pipeline initialized")
    initialization_done = True


# Lazy initialization - only initialize when needed
def ensure_initialized():
    """Ensure RAG pipeline is initialized before use."""
    if not initialization_done:
        initialize_rag()


@app.route('/')
def index():
    """Serve the web chat interface."""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        ensure_initialized()
        stats = vector_store.get_stats()
        return jsonify({
            "status": "healthy",
            "vector_store": {
                "total_documents": stats['total_documents'],
                "embedding_dimension": stats['embedding_dimension']
            },
            "model": rag_pipeline.model
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for answering questions.

    Expected JSON body:
    {
        "question": "How much PTO do I get?"
    }

    Returns:
    {
        "answer": "...",
        "sources": [...],
        "confidence": 0.85,
        "latency_ms": 1234
    }
    """
    start_time = time.time()

    try:
        ensure_initialized()

        # Get question from request
        data = request.get_json()

        if not data or 'question' not in data:
            return jsonify({
                "error": "Missing 'question' in request body"
            }), 400

        question = data['question'].strip()

        if not question:
            return jsonify({
                "error": "Question cannot be empty"
            }), 400

        # Enforce length limit
        if len(question) > 500:
            return jsonify({
                "error": "Question too long (max 500 characters)"
            }), 400

        # Get answer from RAG pipeline
        response = rag_pipeline.answer(question)

        # Calculate latency
        latency_ms = int((time.time() - start_time) * 1000)

        return jsonify({
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
            "latency_ms": latency_ms
        }), 200

    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        return jsonify({
            "error": f"An error occurred: {str(e)}",
            "latency_ms": latency_ms
        }), 500


@app.route('/search', methods=['POST'])
def search():
    """
    Search endpoint for retrieving relevant documents.

    Expected JSON body:
    {
        "query": "PTO policy",
        "top_k": 5
    }
    """
    try:
        ensure_initialized()

        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' in request body"
            }), 400

        query = data['query'].strip()
        top_k = data.get('top_k', 5)

        if not query:
            return jsonify({
                "error": "Query cannot be empty"
            }), 400

        # Search vector store
        results = vector_store.search(query, k=top_k)

        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.content,
                "metadata": doc.metadata,
                "similarity": float(score)
            })

        return jsonify({
            "results": formatted_results,
            "count": len(formatted_results)
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


@app.route('/stats', methods=['GET'])
def stats():
    """Get vector store statistics."""
    try:
        ensure_initialized()
        stats = vector_store.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


if __name__ == '__main__':
    # Run Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
