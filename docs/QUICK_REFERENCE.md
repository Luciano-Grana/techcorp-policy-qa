# Quick Reference Card

## Installation Fixed ✅

All dependencies installed successfully! The ChromaDB compilation error has been resolved.

---

## Quick Commands

### First Time Setup
```bash
# 1. Set up API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 2. Verify installation
python3 -c "import chromadb; print('✓ ChromaDB working!')"

# 3. Index documents (if not already done)
python3 setup.py
```

### Run Application
```bash
# Start web server
python3 app.py

# Open in browser
open http://localhost:5000
```

### Testing
```bash
# Run unit tests
python3 -m pytest tests/ -v

# Run evaluation (30 questions)
python3 src/evaluation.py

# View results
cat evaluation_results/metrics.json
```

### Development
```bash
# Check document count
python3 -c "from src.vector_store import VectorStore; vs = VectorStore(); print(vs.get_stats())"

# Test single query
python3 -c "
from src.vector_store import VectorStore
from src.rag_pipeline import RAGPipeline
vs = VectorStore()
rag = RAGPipeline(vs)
print(rag.answer('How much PTO do I get?').answer)
"
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web chat interface |
| `/chat` | POST | Answer questions |
| `/health` | GET | Health check |
| `/stats` | GET | Vector store stats |

### Example API Call
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the remote work policy?"}'
```

---

## File Locations

```
Key Files:
├── app.py                    # Main Flask application
├── setup.py                  # Document indexing script
├── .env                      # Your API keys (create this!)
│
Documentation:
├── README.md                 # Full documentation
├── QUICKSTART.md             # 10-min setup guide
├── INSTALLATION_FIXED.md     # Fix summary
│
Source Code:
├── src/
│   ├── document_processor.py  # Parse & chunk docs
│   ├── embeddings.py          # Generate embeddings
│   ├── vector_store.py        # ChromaDB interface
│   ├── rag_pipeline.py        # RAG orchestration
│   └── evaluation.py          # Metrics & evaluation
│
Data:
├── data/policies/            # 8 policy documents
└── chroma_db/               # Vector database (auto-created)
```

---

## Troubleshooting

### "OpenAI API key not set"
```bash
# Make sure .env file exists
cp .env.example .env

# Edit .env and add:
OPENAI_API_KEY=your-key-here
```

### "Vector store is empty"
```bash
python3 setup.py
```

### "Port 5000 already in use"
```bash
# Change port in .env
echo "PORT=5001" >> .env
python3 app.py
```

### "Module not found"
```bash
# Reinstall dependencies
python3 -m pip install -r requirements.txt
```

---

## Free API Alternatives

Don't have an OpenAI key? Use these free alternatives:

### OpenRouter (Free Tier)
```bash
# In .env:
OPENROUTER_API_KEY=your-key
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

### Groq (Free Tier)
```bash
# In .env:
GROQ_API_KEY=your-key
LLM_MODEL=llama-3.1-8b-instant
```

Then update `src/rag_pipeline.py` to use the appropriate base URL.

---

## Project Stats

- **Documents**: 8 policy files (~40KB)
- **Chunks**: 125 indexed pieces
- **Embeddings**: 384 dimensions (sentence-transformers)
- **Vector DB**: ChromaDB 1.2.1
- **LLM**: GPT-3.5-turbo (configurable)
- **Evaluation**: 30 questions across 9 categories

---

## Common Questions

**Q: How do I add more policies?**
A: Add .md files to `data/policies/`, then run `python3 setup.py`

**Q: How do I change the LLM model?**
A: Edit `LLM_MODEL` in `.env` file

**Q: How do I adjust chunk size?**
A: Edit `chunk_size` parameter in `setup.py`, then re-run

**Q: Where are evaluation results?**
A: Check `evaluation_results/metrics.json` after running evaluation

**Q: How do I deploy to production?**
A: See [DEPLOYMENT.md](DEPLOYMENT.md) for Render/Railway instructions

---

## Example Questions to Try

1. "How much PTO do employees get?"
2. "What is the remote work policy?"
3. "Can I expense my gym membership?"
4. "What are the password requirements?"
5. "What is the 401k match?"
6. "How many weeks of parental leave are offered?"
7. "What is the learning and development budget?"
8. "What holidays does the company observe?"

---

## Getting Help

- **Full Setup**: See [README.md](README.md)
- **Architecture**: See [DESIGN.md](DESIGN.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Installation Fix**: See [INSTALLATION_FIXED.md](INSTALLATION_FIXED.md)

---

## Status: ✅ READY TO USE

All dependencies installed, documents indexed, application ready to run!

**Next step**: Set your API key in `.env` and run `python3 app.py`
