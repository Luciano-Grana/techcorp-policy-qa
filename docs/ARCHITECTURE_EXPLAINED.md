# Architecture Explained: What Frameworks Were Actually Used?

## TL;DR - Framework Summary

| Component | Framework/Library | Why |
|-----------|------------------|-----|
| **Web App** | ✅ **Flask** | Lightweight Python web framework |
| **RAG Pipeline** | ❌ **Custom (no framework)** | Built from scratch for learning |
| **Vector Store** | **ChromaDB** (direct client) | Vector database library |
| **Embeddings** | **sentence-transformers** (direct) | HuggingFace library |
| **LLM** | **OpenAI SDK** (direct API calls) | Direct API integration |

---

## Detailed Architecture Breakdown

### 1. Web Application Layer: **Flask** ✅

**Yes, I used Flask!** It's a micro web framework for Python.

```python
# app.py
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data['question']
    response = rag_pipeline.answer(question)
    return jsonify({
        "answer": response.answer,
        "sources": response.sources
    })
```

**Why Flask?**
- Lightweight and simple
- Perfect for REST APIs
- Easy to deploy on Render/Railway
- No unnecessary complexity

**Alternatives I didn't use:**
- FastAPI (more modern, async, but overkill)
- Streamlit (easier but less customizable)
- Django (way too heavy for this)

---

### 2. RAG Pipeline: **Custom Implementation** ❌ (No Framework)

**I did NOT use LangChain or any RAG framework for the core pipeline.**

Here's what I built from scratch:

#### a) Document Processing (Custom)
```python
# src/document_processor.py
class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_documents(self, directory):
        # Custom markdown parsing
        # Custom chunking by headings
        # Custom overlap logic
        return documents
```

**No framework** - pure Python with helpers:
- `markdown` library (just for MD→HTML conversion)
- `BeautifulSoup` (just for HTML parsing)
- `pypdf` (just for PDF text extraction)

#### b) Embeddings (Direct Library Use)
```python
# src/embeddings.py
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, query):
        # Direct call to sentence-transformers
        return self.model.encode(query)
```

**No framework** - direct use of HuggingFace's `sentence-transformers` library

#### c) Vector Store (Direct Client)
```python
# src/vector_store.py
import chromadb

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection("policies")

    def search(self, query, k=5):
        # Direct ChromaDB API calls
        results = self.collection.query(query_embeddings=[embedding], n_results=k)
        return results
```

**No framework** - direct ChromaDB Python client

#### d) RAG Orchestration (Custom)
```python
# src/rag_pipeline.py
import openai

class RAGPipeline:
    def answer(self, query):
        # 1. Retrieve (custom logic)
        docs = self.vector_store.search(query, k=5)

        # 2. Format context (custom)
        context = self._format_context(docs)

        # 3. Generate (direct OpenAI API)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ]
        )

        return response
```

**No framework** - custom orchestration with direct OpenAI API calls

---

## What About LangChain?

### Included but NOT Used

You'll notice `langchain` in `requirements.txt`:

```txt
langchain==0.1.0
langchain-community==0.0.10
```

**Why is it there?**
- Initially planned to use it
- Kept for optional future enhancements
- Good for students to experiment with both approaches

**But I built everything custom because:**
1. **Learning**: Better to understand RAG internals
2. **Control**: Full control over chunking, retrieval, prompts
3. **Simplicity**: No abstraction layers to debug
4. **Transparency**: Every step is visible and modifiable

### If I Had Used LangChain

The code would look like this (I didn't do this):

```python
# Example of what LangChain version would look like (NOT USED)
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# This is NOT what I did!
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
```

---

## Complete Tech Stack

### Infrastructure
```
Frontend: Vanilla HTML/CSS/JavaScript (no React/Vue)
Backend: Flask (Python web framework)
Deployment: Gunicorn (WSGI server)
```

### RAG Components (All Custom/Direct)
```
Document Processing: Custom Python code
  ├── markdown → HTML parsing
  ├── pypdf → PDF text extraction
  └── BeautifulSoup → HTML cleaning

Chunking: Custom algorithm (heading-based)

Embeddings: sentence-transformers library (direct)
  └── Model: all-MiniLM-L6-v2

Vector Store: ChromaDB Python client (direct)
  └── Similarity: Cosine
  └── Storage: Persistent local disk

LLM: OpenAI Python SDK (direct)
  └── Model: gpt-3.5-turbo
  └── API: Direct REST calls
```

### Evaluation (Custom)
```python
# src/evaluation.py - All custom code
class Evaluator:
    def evaluate_groundedness(self, answer, context):
        # Custom LLM-as-judge implementation
        # Direct OpenAI API call

    def evaluate_citation_accuracy(self, answer, sources):
        # Custom verification logic
        # Direct OpenAI API call
```

---

## Why This Architecture?

### 1. Educational Value
Building from scratch teaches:
- How RAG actually works under the hood
- Vector embeddings and similarity search
- Prompt engineering
- LLM API integration

### 2. Flexibility
Custom code means:
- Full control over chunking strategy
- Custom prompt templates
- Easy to modify and experiment
- No framework lock-in

### 3. Simplicity
- No complex abstractions
- Easy to debug
- Clear data flow
- Minimal dependencies

### 4. Production-Ready
Despite being custom:
- Well-tested components
- Error handling
- Logging
- Configurable via env vars

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser                              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Flask Web App (app.py)                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │ / route    │  │ /chat POST │  │ /health    │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            Custom RAG Pipeline (src/rag_pipeline.py)         │
│                                                              │
│  1. Retrieve(query) → vector_store.search()                 │
│  2. Format context → custom function                         │
│  3. Generate → openai.chat.completions.create()             │
└─────────────┬───────────────────────────┬───────────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────────┐
│   Vector Store (Custom) │   │   OpenAI API (Direct SDK)   │
│  src/vector_store.py    │   │                             │
│                         │   │  - gpt-3.5-turbo            │
│  ├── ChromaDB client    │   │  - Direct REST calls        │
│  ├── Embeddings         │   │  - No LangChain wrapper     │
│  └── Search logic       │   └─────────────────────────────┘
└─────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│        Document Processor (Custom - src/document_processor.py)│
│                                                              │
│  - Load MD/PDF/HTML files                                   │
│  - Custom chunking by headings                              │
│  - Overlap logic                                            │
│  - Metadata extraction                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Comparison: Custom vs. Framework

| Aspect | Custom (What I Did) | LangChain |
|--------|-------------------|-----------|
| **Complexity** | Simple, clear | More abstraction |
| **Learning Curve** | Steep initially | Easier to start |
| **Flexibility** | Full control | Framework constraints |
| **Code Lines** | ~500 lines RAG code | ~50 lines (using chains) |
| **Understanding** | Deep knowledge | Black box |
| **Debugging** | Easy to trace | Framework internals |
| **Dependencies** | Minimal | Many sub-packages |
| **Best For** | Learning, custom needs | Rapid prototyping |

---

## Summary

### What I Used:
✅ **Flask** - Web framework
✅ **Custom RAG Pipeline** - No framework, built from scratch
✅ **ChromaDB** - Direct client (not through LangChain)
✅ **sentence-transformers** - Direct library use
✅ **OpenAI SDK** - Direct API calls

### What I Didn't Use:
❌ **LangChain** - Included but not used (available for experiments)
❌ **LlamaIndex** - Not included
❌ **Haystack** - Not included
❌ **Streamlit** - Not used (Flask instead)

---

## Code Statistics

```
Custom RAG Implementation:
- document_processor.py: 280 lines
- embeddings.py: 80 lines
- vector_store.py: 150 lines
- rag_pipeline.py: 220 lines
- evaluation.py: 350 lines

Total Custom RAG Code: ~1,080 lines

Flask Web App:
- app.py: 150 lines
- index.html: 280 lines

Total: ~1,510 lines of custom code
```

Compare to LangChain approach: ~100-200 lines total

**Trade-off**: More code, but much better understanding!

---

## Want to See the Full Code?

Check these files:
- **Web App**: [app.py](app.py)
- **RAG Pipeline**: [src/rag_pipeline.py](src/rag_pipeline.py)
- **Vector Store**: [src/vector_store.py](src/vector_store.py)
- **Document Processing**: [src/document_processor.py](src/document_processor.py)
- **Embeddings**: [src/embeddings.py](src/embeddings.py)

All custom, all understandable, all yours to modify! 🚀
