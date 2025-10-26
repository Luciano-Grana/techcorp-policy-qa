# Quick Start Guide

Get the TechCorp Policy Q&A Assistant running in under 10 minutes!

## Prerequisites

- Python 3.10 or higher
- OpenAI API key (or free alternative: OpenRouter, Groq)
- Git (for deployment)

## 5-Minute Setup

### 1. Install Dependencies (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt
```

### 2. Configure API Key (1 minute)

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=sk-your-key-here
```

**Don't have an OpenAI key?** Use free alternatives:

- **OpenRouter**: https://openrouter.ai/ (free tier available)
- **Groq**: https://console.groq.com/ (free tier available)

For OpenRouter/Groq, update `app.py` or `rag_pipeline.py` to point to their base URLs.

### 3. Index Documents (2 minutes)

```bash
# Run setup script
python setup.py
```

This will:
- Load policy documents from `data/policies/`
- Chunk documents into ~1000 character pieces
- Generate embeddings using sentence-transformers
- Store in ChromaDB vector database

### 4. Start Application (<1 minute)

```bash
python app.py
```

Open browser to: **http://localhost:5000**

## Testing the Application

Try these example questions:

1. "How much PTO do employees get?"
2. "What is the remote work policy?"
3. "What expenses can I reimburse?"
4. "What are the password requirements?"
5. "What is the 401k match?"

## Running Evaluation

```bash
# Run full evaluation suite (30 questions)
python src/evaluation.py

# View results
cat evaluation_results/metrics.json
```

## Common Issues

### "OpenAI API key not set"
- Make sure `.env` file exists in project root
- Check that `OPENAI_API_KEY` is set correctly
- Try: `export OPENAI_API_KEY=your-key` (temporary)

### "Vector store is empty"
- Run: `python setup.py`
- Make sure `data/policies/` contains .md files

### "No module named 'src'"
- Ensure you're in the project root directory
- Check that `src/__init__.py` exists

### Slow responses
- First query is always slower (model loading)
- Check your internet connection
- Consider using a faster LLM model

## Project Structure

```
Quantic-AI-Project/
├── app.py                  # Flask web application
├── setup.py               # Setup script (run first)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
│
├── data/
│   └── policies/         # Policy documents (8 .md files)
│
├── src/
│   ├── document_processor.py  # Document parsing & chunking
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # ChromaDB vector store
│   ├── rag_pipeline.py        # RAG orchestration
│   └── evaluation.py          # Evaluation metrics
│
├── templates/
│   └── index.html        # Web chat interface
│
├── tests/
│   └── test_basic.py     # Unit tests
│
└── chroma_db/            # Vector database (created by setup)
```

## API Usage

### Chat Endpoint

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How much PTO do I get?"}'
```

Response:
```json
{
  "answer": "Employees receive 15-25 days of PTO per year based on tenure...",
  "sources": [
    {
      "doc_id": "POL-001",
      "source": "pto_policy.md",
      "heading": "Accrual Rates"
    }
  ],
  "confidence": 0.87,
  "latency_ms": 1456
}
```

### Health Check

```bash
curl http://localhost:5000/health
```

## Next Steps

### Deploy to Production

See [README.md](README.md#deployment) for deployment instructions:
- Deploy to Render (recommended)
- Deploy to Railway
- Configure CI/CD with GitHub Actions

### Customize

1. **Add your own policies**: Place .md files in `data/policies/`
2. **Adjust chunking**: Modify `chunk_size` in `setup.py`
3. **Change LLM model**: Edit `LLM_MODEL` in `.env`
4. **Tune retrieval**: Adjust `RAG_TOP_K` in `.env`

### Improve Quality

1. **Run evaluation**: `python src/evaluation.py`
2. **Review results**: Check `evaluation_results/metrics.json`
3. **Iterate on prompt**: Edit system prompt in `src/rag_pipeline.py`
4. **Experiment with chunk size**: Re-run setup with different sizes

## Using Free-Tier APIs

### OpenRouter (Recommended for Free Tier)

```python
# In src/rag_pipeline.py, modify OpenAI client initialization:
import openai

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENROUTER_API_KEY")

# Use free models: "meta-llama/llama-3.1-8b-instruct:free"
```

### Groq (Fast & Free)

```python
# Install Groq SDK
pip install groq

# In src/rag_pipeline.py:
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Use: "llama-3.1-8b-instant" (free tier)
```

## Troubleshooting

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Vector Store Issues
```bash
# Reset vector store
rm -rf chroma_db/
python setup.py
```

### Port Already in Use
```bash
# Change port in .env
echo "PORT=5001" >> .env
python app.py
```

## Learn More

- [README.md](../README.md) - Full documentation
- [DESIGN.md](DESIGN.md) - Architecture & design decisions
- [evaluation_results/](../evaluation_results/) - Evaluation metrics

## Support

Questions or issues? Check:
1. README.md for full documentation
2. GitHub Issues (if repository is public)
3. Course discussion forum

---

**Ready to go?** Run `python setup.py` and start chatting! 🚀
