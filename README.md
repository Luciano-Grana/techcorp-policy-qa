# TechCorp Policy Q&A Assistant

A Retrieval-Augmented Generation (RAG) application for answering questions about company policies using LLMs and vector search.

**Live Demo**: [Your deployment URL here]

**Project for**: Master of Science in Software Engineering - AI Engineering Course

## Overview

This application provides an intelligent chatbot that answers questions about TechCorp company policies. It uses:

- **Document Processing**: Parses and chunks policy documents (Markdown, PDF, HTML, TXT)
- **Vector Search**: ChromaDB for semantic search over policy content
- **RAG Pipeline**: Retrieves relevant context and generates accurate answers
- **Web Interface**: Flask-based chat interface
- **Evaluation**: Automated metrics for groundedness, citation accuracy, and latency

## Features

- Natural language Q&A over 8 company policy documents (~70 pages)
- Source citation for all answers
- Guardrails to refuse out-of-scope questions
- Comprehensive evaluation framework
- CI/CD pipeline with GitHub Actions
- Production deployment on Render/Railway

## Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key (or alternative: OpenRouter, Groq)
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Quantic-AI-Project
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Running Locally

1. **Index documents** (first time only):
   ```bash
   python src/vector_store.py
   ```

2. **Start the web application**:
   ```bash
   python app.py
   ```

3. **Open in browser**:
   ```
   http://localhost:5000
   ```

### Running Evaluation

```bash
python src/evaluation.py
```

Results will be saved to `evaluation_results/`:
- `metrics.json`: Aggregate metrics
- `detailed_results.json`: Per-question results

## Project Structure

```
Quantic-AI-Project/
├── data/
│   └── policies/              # Company policy documents (8 files)
├── src/
│   ├── document_processor.py  # Document parsing and chunking
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # ChromaDB vector store
│   ├── rag_pipeline.py        # RAG question answering
│   └── evaluation.py          # Evaluation metrics
├── templates/
│   └── index.html             # Web chat interface
├── tests/
│   └── test_basic.py          # Smoke tests
├── docs/                      # Documentation and guides
│   ├── ARCHITECTURE_EXPLAINED.md   # Technical deep dive
│   ├── EVALUATION_GUIDE.md         # Evaluation framework details
│   ├── RUN_EVALUATION.md           # How to run evaluation
│   ├── INSTALLATION_FIXED.md       # Installation troubleshooting
│   ├── OPENROUTER_SETUP.md         # OpenRouter API setup
│   ├── OPENROUTER_FIX.md           # OpenRouter compatibility fixes
│   ├── VENV_FIX.md                 # Virtual environment setup
│   ├── FILE_INDEX.md               # Complete file reference
│   └── QUICK_REFERENCE.md          # Common commands
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline
├── app.py                     # Flask web application
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── Procfile                   # Deployment configuration
├── README.md                  # This file
├── DESIGN.md                  # Architecture and design decisions
├── QUICKSTART.md              # Quick start guide
├── DEPLOYMENT.md              # Deployment guide
└── PROJECT_SUMMARY.md         # Project overview
```

## API Endpoints

### `GET /`
Web chat interface

### `POST /chat`
Answer questions about policies

**Request**:
```json
{
  "question": "How much PTO do employees get?"
}
```

**Response**:
```json
{
  "answer": "Employees receive 15-25 days of PTO per year...",
  "sources": [
    {
      "doc_id": "POL-001",
      "source": "pto_policy.md",
      "heading": "Accrual Rates",
      "similarity": "0.892"
    }
  ],
  "confidence": 0.85,
  "latency_ms": 1234
}
```

### `GET /health`
Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "vector_store": {
    "total_documents": 42,
    "embedding_dimension": 384
  },
  "model": "gpt-3.5-turbo"
}
```

### `GET /stats`
Vector store statistics

## Policy Documents

The application includes 8 synthetic policy documents covering:

1. **PTO Policy** (POL-001): Paid time off accrual, usage, carryover
2. **Remote Work** (POL-002): Remote work eligibility, equipment, security
3. **Expense Reimbursement** (POL-003): Travel, meals, office supplies
4. **Information Security** (POL-004): Passwords, data classification, incidents
5. **Code of Conduct** (POL-005): Ethics, harassment, conflicts of interest
6. **Holidays and Leave** (POL-006): Holidays, parental leave, sabbaticals
7. **Professional Development** (POL-007): L&D budget, certifications, conferences
8. **Benefits Overview** (POL-008): Health insurance, 401k, perks

**Total**: ~70 pages, ~42 document chunks after processing

## Evaluation Metrics

### Success Metrics

The application is evaluated on 30 questions across policy categories:

#### Information Quality Metrics

1. **Groundedness** (required):
   - Definition: % of answers whose content is factually consistent with retrieved evidence
   - Evaluation: LLM-based assessment (GPT-3.5-turbo)
   - Target: ≥80% mean score

2. **Citation Accuracy** (required):
   - Definition: % of answers with correct source citations
   - Evaluation: LLM-based verification
   - Target: ≥80% mean score

3. **Exact/Partial Match** (optional):
   - Definition: % of answers matching expected responses
   - Target: ≥60% partial match

#### System Metrics

1. **Latency** (required):
   - P50 (median response time)
   - P95 (95th percentile response time)
   - Target: P95 < 3000ms

### Running Evaluation

```bash
# Full evaluation on 30 questions
python src/evaluation.py

# Results location
cat evaluation_results/metrics.json
```

### Sample Results

```json
{
  "groundedness": {
    "mean": 0.87,
    "percentage_high_quality": 83.3
  },
  "citation_accuracy": {
    "mean": 0.85,
    "percentage_high_quality": 80.0
  },
  "latency_ms": {
    "p50": 1456,
    "p95": 2789
  }
}
```

## Design Decisions

### Embedding Model
**Choice**: `sentence-transformers/all-MiniLM-L6-v2`

**Justification**:
- Free and locally runnable (no API costs)
- Good balance of quality vs. speed (384 dimensions)
- Well-suited for semantic search tasks
- Fast inference for real-time retrieval

**Alternatives considered**:
- Cohere `embed-english-light-v3.0`: Higher quality but API dependency
- OpenAI `text-embedding-3-small`: Good quality but costs per request

### Chunking Strategy
**Choice**: Heading-based chunking with 1000 character limit and 200 character overlap

**Justification**:
- Preserves semantic coherence (keeps sections together)
- 1000 characters ≈ 250 tokens, fits well in LLM context
- 200 character overlap prevents information loss at boundaries
- Markdown headings provide natural semantic boundaries

**Alternatives considered**:
- Fixed-size chunking: Simpler but breaks semantic units
- Recursive character splitting: More complex, similar results

### Vector Store
**Choice**: ChromaDB (persistent, local storage)

**Justification**:
- Free and open source
- Easy local development and testing
- Persistent storage (survives restarts)
- Good performance for small-medium datasets (<10k docs)
- Supports cosine similarity

**Alternatives considered**:
- Pinecone: Better for scale but requires API key and costs
- FAISS: Faster but no persistence without extra work

### Retrieval Parameters
**Choice**: Top-k = 5, cosine similarity

**Justification**:
- 5 chunks provide sufficient context (~1250 tokens) without overwhelming LLM
- Cosine similarity works well for semantic search
- Similarity threshold of 0.3 filters low-quality results

### LLM Model
**Choice**: GPT-3.5-turbo (default), configurable

**Justification**:
- Good balance of quality, speed, and cost
- Fast inference (typically <2s for responses)
- Strong instruction following for guardrails
- Can be swapped for GPT-4, Claude, or open-source models

**Free alternatives**:
- OpenRouter free tier models
- Groq (llama-3.1-8b, mixtral)

### Prompt Design
**Choice**: System prompt with explicit guardrails and citation requirements

**Key elements**:
1. Scope limitation: "ONLY answer based on provided documents"
2. Out-of-scope handling: Explicit refusal message
3. Citation requirement: Always include source document IDs
4. Conciseness: Keep answers direct and focused

### Temperature
**Choice**: 0.1 (low temperature)

**Justification**:
- Factual accuracy is critical for policy Q&A
- Low temperature reduces hallucination risk
- Ensures consistent, deterministic answers

## Deployment

### Deploy to Render

1. **Create account** at [render.com](https://render.com)

2. **Create new Web Service**:
   - Connect your GitHub repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

3. **Add environment variables**:
   - `OPENAI_API_KEY`: Your API key
   - `PYTHON_VERSION`: 3.10.12

4. **Set up deploy hook** (optional):
   - Copy deploy hook URL from Render dashboard
   - Add to GitHub secrets as `RENDER_DEPLOY_HOOK_URL`

### Deploy to Railway

1. **Create account** at [railway.app](https://railway.app)

2. **Create new project**:
   - Connect GitHub repository
   - Railway auto-detects Python and uses Procfile

3. **Add environment variables**:
   - `OPENAI_API_KEY`: Your API key

4. **Deploy**: Automatic on push to main branch

### Environment Variables

Required:
- `OPENAI_API_KEY`: OpenAI API key (or alternative LLM provider)

Optional:
- `LLM_MODEL`: Model name (default: gpt-3.5-turbo)
- `LLM_TEMPERATURE`: Temperature 0-1 (default: 0.1)
- `LLM_MAX_TOKENS`: Max response tokens (default: 500)
- `RAG_TOP_K`: Number of chunks to retrieve (default: 5)
- `PORT`: Server port (default: 5000)

## CI/CD Pipeline

GitHub Actions workflow runs on push and PR:

1. **Build and Test**:
   - Install dependencies
   - Verify imports (smoke test)
   - Run pytest (if tests exist)
   - Check code formatting

2. **Deploy** (on push to main):
   - Trigger deployment to Render/Railway

### Setting up CI/CD

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Add secrets** (GitHub Settings > Secrets):
   - `RENDER_DEPLOY_HOOK_URL`: Deploy hook from Render
   - Or `RAILWAY_TOKEN`: Railway API token

3. **Workflow runs automatically** on push

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Formatting

```bash
pip install black
black src/ app.py
```

### Indexing New Documents

Add documents to `data/policies/`, then:

```bash
python -c "from src.vector_store import VectorStore; from src.document_processor import DocumentProcessor; vs = VectorStore(); vs.reset(); dp = DocumentProcessor(); docs = dp.load_documents('data/policies'); vs.add_documents(docs)"
```

## Ablation Studies (Optional)

Test different configurations:

### Vary Top-k

```python
# In src/rag_pipeline.py
rag = RAGPipeline(vector_store=store, top_k=3)  # Try 3, 5, 7, 10
```

### Vary Chunk Size

```python
# In src/document_processor.py
processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)  # Try different sizes
```

### Vary Prompt Format

Edit system prompt in `src/rag_pipeline.py` to test different instruction styles.

## Documentation

For detailed guides and troubleshooting, see the [docs/](docs/) folder:

- [ARCHITECTURE_EXPLAINED.md](docs/ARCHITECTURE_EXPLAINED.md) - Technical deep dive into the RAG pipeline
- [EVALUATION_GUIDE.md](docs/EVALUATION_GUIDE.md) - Evaluation framework details
- [RUN_EVALUATION.md](docs/RUN_EVALUATION.md) - How to run evaluation
- [INSTALLATION_FIXED.md](docs/INSTALLATION_FIXED.md) - Installation troubleshooting
- [OPENROUTER_SETUP.md](docs/OPENROUTER_SETUP.md) - OpenRouter API setup guide
- [VENV_FIX.md](docs/VENV_FIX.md) - Virtual environment setup
- [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) - Common commands

## Troubleshooting

### Quick Fixes

#### "OpenAI API key not set"
- Ensure `.env` file exists with `OPENROUTER_API_KEY=your_key` or `OPENAI_API_KEY=your_key`
- Or set environment variable: `export OPENROUTER_API_KEY=your_key`

#### "Vector store is empty"
- Run indexing: `python src/vector_store.py`
- Check that `data/policies/` contains documents

#### "No module named 'src'"
- Ensure you're in project root directory
- Verify `src/__init__.py` exists

#### Slow response times
- Check network connection to OpenAI/OpenRouter API
- Consider using faster model (gpt-3.5-turbo or llama-3.1-8b)
- Reduce `top_k` parameter

For more troubleshooting help, see [docs/](docs/)

## Future Improvements

1. **Re-ranking**: Add cross-encoder for better retrieval precision
2. **Hybrid search**: Combine semantic + keyword search
3. **Conversation memory**: Track multi-turn conversations
4. **Feedback loop**: Collect user feedback to improve responses
5. **Advanced chunking**: Implement semantic chunking
6. **Caching**: Cache common queries for faster responses
7. **Streaming**: Stream LLM responses for better UX
8. **Authentication**: Add user authentication and access control

## License

This project is for educational purposes as part of an AI Engineering course.

## Contact

**Student**: Luciano Grana
**Course**: Master of Science in Software Engineering
**Institution**: [Your institution]

## Acknowledgments

- Company policy templates inspired by real-world HR policies
- Built with LangChain, ChromaDB, Flask, and OpenAI
- Deployed on Render/Railway free tier
