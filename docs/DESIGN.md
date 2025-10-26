# Design Documentation

## TechCorp Policy Q&A Assistant - Architecture & Design Decisions

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Component Design](#component-design)
3. [Design Decisions](#design-decisions)
4. [Data Flow](#data-flow)
5. [Evaluation Strategy](#evaluation-strategy)
6. [Trade-offs](#trade-offs)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    (Web Browser / API Client)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask Web Application                       │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Routes     │  │  Chat API    │  │   Health     │         │
│  │  (/, /chat)  │  │   Endpoint   │  │   Check      │         │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘         │
└─────────┼──────────────────┼──────────────────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                        RAG Pipeline                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Query Processing                                      │  │
│  │     - Input validation                                    │  │
│  │     - Query embedding generation                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. Retrieval (Vector Search)                            │  │
│  │     - Similarity search in ChromaDB                       │  │
│  │     - Top-k document retrieval                            │  │
│  │     - Optional re-ranking                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. Context Formatting                                    │  │
│  │     - Format retrieved chunks                             │  │
│  │     - Add source metadata                                 │  │
│  │     - Build prompt with guardrails                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  4. Generation (LLM)                                      │  │
│  │     - Send to OpenAI API                                  │  │
│  │     - Generate answer with citations                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer                                    │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   ChromaDB   │  │  Embeddings  │  │   Policy     │         │
│  │ Vector Store │  │    Model     │  │  Documents   │         │
│  │              │  │              │  │              │         │
│  │ - Embeddings │  │ - MiniLM-L6  │  │ - 8 MD files │         │
│  │ - Metadata   │  │ - 384 dims   │  │ - ~70 pages  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| **Frontend** | HTML/CSS/JavaScript | Simple, no-framework chat interface |
| **Backend** | Flask | Lightweight, easy deployment, good for APIs |
| **Vector DB** | ChromaDB | Free, persistent, good for small-medium datasets |
| **Embeddings** | sentence-transformers | Free, local, fast (no API costs) |
| **LLM** | OpenAI GPT-3.5-turbo | Good quality/speed/cost balance |
| **Deployment** | Render/Railway | Free tier, easy GitHub integration |
| **CI/CD** | GitHub Actions | Free, integrated with GitHub |

---

## Component Design

### 1. Document Processing (`document_processor.py`)

**Purpose**: Parse and chunk policy documents for indexing

**Key Design Decisions**:

#### Chunking Strategy
- **Method**: Heading-based chunking with size limits
- **Parameters**:
  - Chunk size: 1000 characters (~250 tokens)
  - Overlap: 200 characters (20%)

**Rationale**:
- Markdown documents have natural semantic boundaries (headings)
- Preserving sections keeps related information together
- 1000 chars fits well in LLM context windows (~8k tokens total for 5 chunks)
- Overlap prevents information loss at boundaries

**Alternative Approaches Considered**:
1. **Fixed-size chunking**: Simpler but breaks semantic units
2. **Sentence-based chunking**: More granular but loses document structure
3. **Recursive character splitting**: LangChain's approach, more complex
4. **Semantic chunking**: Would use embeddings, slower and more complex

**Trade-offs**:
- ✅ Preserves document structure
- ✅ Good semantic coherence
- ❌ Variable chunk sizes (but capped at 1.5x limit)
- ❌ Heading-dependent (works for markdown, not plain text)

#### File Format Support
Supports: Markdown, PDF, HTML, TXT

**Implementation**:
- Markdown: Parse with `markdown` library, preserve headings
- PDF: Extract text with `pypdf`
- HTML: Parse with BeautifulSoup, extract text
- TXT: Direct reading

### 2. Embeddings (`embeddings.py`)

**Purpose**: Generate vector embeddings for semantic search

**Model Choice**: `all-MiniLM-L6-v2`

**Specifications**:
- Dimensions: 384
- Max sequence length: 256 tokens
- Speed: ~1000 docs/sec on CPU
- Size: ~80MB

**Rationale**:
1. **Free & Local**: No API costs, works offline
2. **Good Quality**: Trained on 1B+ sentence pairs
3. **Fast**: Optimized for inference
4. **Compact**: 384 dims (vs 768/1536 for larger models)

**Alternatives Considered**:

| Model | Dimensions | Quality | Speed | Cost |
|-------|-----------|---------|-------|------|
| **all-MiniLM-L6-v2** ✓ | 384 | Good | Fast | Free |
| all-mpnet-base-v2 | 768 | Better | Slower | Free |
| Cohere embed-light | 1024 | Better | Fast | API |
| OpenAI text-embed-3-small | 1536 | Best | Fast | $0.02/1M |

**Trade-offs**:
- ✅ Zero cost
- ✅ No API dependency
- ✅ Good enough for policy Q&A
- ❌ Lower quality than commercial models
- ❌ No fine-tuning for domain

### 3. Vector Store (`vector_store.py`)

**Purpose**: Store and retrieve document embeddings

**Choice**: ChromaDB (persistent, local)

**Configuration**:
- Similarity metric: Cosine similarity
- Persistence: Disk storage (`chroma_db/`)
- Index: HNSW (Hierarchical Navigable Small World)

**Rationale**:
1. **Free & Open Source**: No costs, self-hosted
2. **Persistent**: Survives app restarts (important for deployment)
3. **Simple API**: Easy to use, minimal boilerplate
4. **Good Performance**: Sub-second retrieval for <10k docs
5. **Local**: No network latency, works offline

**Alternatives Considered**:

| Vector Store | Pros | Cons |
|--------------|------|------|
| **ChromaDB** ✓ | Free, persistent, simple | Limited scale |
| Pinecone | Fast, scalable, managed | Costs, API dependency |
| Weaviate | Feature-rich, hybrid search | Complex setup |
| FAISS | Very fast, Facebook-built | No persistence, manual setup |
| Qdrant | Modern, fast | Less mature ecosystem |

**Trade-offs**:
- ✅ Zero cost
- ✅ Easy setup
- ✅ Good for <100k docs
- ❌ Not optimized for massive scale
- ❌ No distributed deployment

### 4. RAG Pipeline (`rag_pipeline.py`)

**Purpose**: Orchestrate retrieval and generation

**Key Parameters**:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `top_k` | 5 | Balances context quality vs. noise |
| `temperature` | 0.1 | Low temp for factual accuracy |
| `max_tokens` | 500 | Concise answers, lower cost |
| `model` | gpt-3.5-turbo | Good quality/speed/cost |

**Prompt Engineering**:

1. **System Prompt**: Sets behavior and guardrails
   - Scope limitation: "ONLY answer from documents"
   - Citation requirement: Must cite sources
   - Refusal handling: Out-of-scope message
   - Tone: Professional, concise

2. **User Prompt Template**:
   ```
   Question: {query}

   Policy Documents:
   {formatted_context_with_sources}

   Remember: cite sources, only use provided info
   ```

**Guardrails**:
1. **Scope Control**: Refuse non-policy questions
2. **Length Limit**: Max 500 tokens
3. **Citation Enforcement**: Always include doc IDs
4. **Similarity Threshold**: Filter low-quality retrievals (<0.3)

**Trade-offs**:
- ✅ Strong guardrails prevent hallucination
- ✅ Citations enable verification
- ❌ May refuse valid but creatively-worded questions
- ❌ Limited to context window (can't synthesize across many docs)

### 5. Evaluation (`evaluation.py`)

**Purpose**: Measure system quality and performance

**Metrics Implemented**:

#### Information Quality Metrics

1. **Groundedness** (LLM-based)
   - Definition: Answer content fully supported by evidence
   - Method: GPT-3.5 evaluates factual consistency
   - Scale: 0-1 (0% to 100%)
   - Target: Mean ≥ 0.8

2. **Citation Accuracy** (LLM-based)
   - Definition: Cited sources correctly support claims
   - Method: GPT-3.5 verifies citation correctness
   - Scale: 0-1
   - Target: Mean ≥ 0.8

3. **Exact/Partial Match** (optional)
   - Definition: Answer matches expected response
   - Method: String matching (exact) or overlap (partial)
   - Target: ≥60% partial match

#### System Metrics

1. **Latency**
   - P50 (median): Typical response time
   - P95: Worst-case (95th percentile)
   - Target: P95 < 3000ms

**Dataset**: 30 evaluation questions across 9 categories
- PTO: 5 questions
- Remote Work: 5 questions
- Expenses: 5 questions
- Security: 4 questions
- Benefits: 3 questions
- Holidays: 3 questions
- Learning: 3 questions
- Out-of-scope: 2 questions

**Trade-offs**:
- ✅ LLM-based evaluation is flexible and nuanced
- ✅ Automated, repeatable
- ❌ LLM evaluation costs money (but small dataset)
- ❌ LLM judges may have biases

---

## Design Decisions

### 1. Why ChromaDB over Pinecone?

**Decision**: Use ChromaDB for vector storage

**Factors**:
- **Cost**: Free vs. paid (Pinecone free tier limited)
- **Deployment**: Self-hosted vs. managed service
- **Dataset size**: <100 docs, ChromaDB is sufficient
- **Learning**: Students can run locally

**When to reconsider**: If scaling to >100k documents or need distributed deployment

### 2. Why Heading-Based Chunking?

**Decision**: Chunk by markdown headings instead of fixed-size

**Factors**:
- Policy documents have clear section structure
- Preserves semantic coherence (keeps related info together)
- Better citation (can cite specific sections)
- Avoids splitting mid-paragraph

**When to reconsider**: For unstructured text (e.g., articles without headings)

### 3. Why GPT-3.5-turbo over GPT-4?

**Decision**: Default to GPT-3.5-turbo

**Factors**:
- **Cost**: ~20x cheaper ($0.50/M vs $10/M tokens)
- **Speed**: ~2-3x faster response
- **Quality**: Sufficient for policy Q&A (not complex reasoning)
- **Configurable**: Can swap to GPT-4 via env var

**When to reconsider**: If answers lack nuance or struggle with complex policies

### 4. Why Low Temperature (0.1)?

**Decision**: Set temperature to 0.1 instead of default 0.7

**Factors**:
- **Factual accuracy**: Policies require precise information
- **Consistency**: Same question should give same answer
- **Hallucination risk**: Higher temp increases creativity (bad for facts)
- **Citations**: Need deterministic source selection

**When to reconsider**: Never for policy Q&A (factual domain)

### 5. Why Top-k = 5?

**Decision**: Retrieve 5 chunks per query

**Analysis**:
- 5 chunks × ~250 tokens = ~1250 tokens of context
- Leaves room for system prompt (~300 tokens) and response (500 tokens)
- Total: ~2050 tokens (well under 4k context limit)

**Alternatives tested**:
- k=3: Sometimes misses relevant context
- k=7: Adds noise, slows generation
- k=10: Token limit issues, dilutes quality

**When to reconsider**: If using longer context models (GPT-4-turbo, Claude)

### 6. Why Flask over FastAPI?

**Decision**: Use Flask for web framework

**Factors**:
- **Simplicity**: Minimal boilerplate for simple API
- **Familiarity**: Widely known, good for educational project
- **Deployment**: Render/Railway have good Flask support
- **Sufficient**: No need for async (single LLM call per request)

**When to reconsider**: If adding async features (streaming, concurrent requests)

### 7. Why LLM-Based Evaluation?

**Decision**: Use GPT-3.5 to evaluate groundedness and citations

**Alternatives**:
- **Human evaluation**: Gold standard but expensive and slow
- **Rule-based**: Fast but brittle, misses nuance
- **Metrics (BLEU, ROUGE)**: Don't capture semantic accuracy

**Rationale**:
- LLMs can assess factual consistency
- Automated and repeatable
- Correlates well with human judgments
- Reasonable cost for 30 questions (~$0.10)

**When to reconsider**: If evaluation budget is very limited (use rule-based) or if highest accuracy needed (human eval)

---

## Data Flow

### Indexing Flow (One-Time Setup)

```
1. Load Documents
   data/policies/*.md → DocumentProcessor

2. Parse & Chunk
   DocumentProcessor → List[Document]
   - Extract metadata (doc ID, headings)
   - Split by headings
   - Add overlap

3. Generate Embeddings
   List[Document] → EmbeddingModel → List[Vector]
   - Batch processing (100 docs at a time)
   - 384-dimensional vectors

4. Store in Vector DB
   List[Vector] + Metadata → ChromaDB
   - Persist to disk (chroma_db/)
   - Build HNSW index
```

### Query Flow (Runtime)

```
1. User Question
   "How much PTO do I get?" → Flask /chat endpoint

2. Generate Query Embedding
   Question → EmbeddingModel → Query Vector (384-dim)

3. Vector Search
   Query Vector → ChromaDB → Top-5 Similar Documents
   - Cosine similarity
   - Returns: content + metadata + scores

4. Format Context
   Top-5 Docs → Context String
   - Add source information
   - Format for LLM prompt

5. Generate Answer
   Context + Question → OpenAI API → Answer + Citations
   - Temperature: 0.1
   - Max tokens: 500
   - System prompt enforces guardrails

6. Return Response
   Answer + Sources + Latency → JSON → User
```

---

## Evaluation Strategy

### Why These Metrics?

#### Groundedness
- **Critical for RAG**: Ensures no hallucination
- **Measurable**: LLM can assess factual consistency
- **Actionable**: Low scores indicate retrieval or prompt issues

#### Citation Accuracy
- **Enables verification**: Users can check sources
- **Builds trust**: Correct citations = credible system
- **Detects errors**: Wrong citations indicate context confusion

#### Latency
- **User experience**: Slow responses hurt usability
- **System health**: Degradation indicates issues
- **Trade-off metric**: Balance quality vs speed

### Evaluation Dataset Design

**Coverage**:
- All 8 policy documents represented
- Mix of difficulty (simple facts vs. complex policies)
- Edge cases (out-of-scope questions)

**Size**: 30 questions
- Large enough for statistical significance
- Small enough to run frequently (for CI/CD)
- Cost-effective for LLM-based eval (~$0.10/run)

**Categories**:
- Policy-specific questions (28)
- Out-of-scope questions (2)
- Tests refusal behavior

---

## Trade-offs

### Quality vs. Cost

| Choice | Quality Impact | Cost Impact | Decision |
|--------|---------------|-------------|----------|
| GPT-4 vs GPT-3.5 | +20% accuracy | +20x cost | GPT-3.5 ✓ |
| Cohere embed vs MiniLM | +10% retrieval | $0.10/M docs | MiniLM ✓ |
| Re-ranking | +15% precision | +500ms latency | Skip (v1) |
| Top-k=10 vs 5 | +5% recall | +50% cost | k=5 ✓ |

### Simplicity vs. Features

| Feature | Complexity | Value | Decision |
|---------|-----------|-------|----------|
| Conversation memory | Medium | Medium | Skip (v1) |
| Re-ranking | Medium | High | Skip (v1) |
| Hybrid search | High | Medium | Skip |
| Streaming | Low | High | Future |
| User feedback | Medium | High | Future |

### Development Speed vs. Production Readiness

| Aspect | V1 Approach | Production Approach |
|--------|------------|---------------------|
| Auth | None | OAuth 2.0 |
| Caching | None | Redis |
| Monitoring | Basic logs | Datadog/Sentry |
| Rate limiting | None | Per-user limits |
| Database | Local ChromaDB | Managed Pinecone |

**Decision**: Focus on core functionality for V1, iterate based on feedback

---

## Future Improvements

### Short-term (Next Sprint)
1. **Re-ranking**: Add cross-encoder for better Top-5 selection
2. **Streaming**: Stream LLM responses for better UX
3. **Caching**: Cache common queries (reduce cost/latency)

### Medium-term (Next Quarter)
1. **Conversation memory**: Track multi-turn conversations
2. **Feedback loop**: Collect user ratings, retrain
3. **Hybrid search**: Combine semantic + keyword search
4. **Advanced chunking**: Implement semantic chunking

### Long-term (Future Versions)
1. **Fine-tuned embeddings**: Train on policy domain
2. **Multi-modal**: Support images in policies (diagrams, charts)
3. **Personalization**: Tailor answers to user role/department
4. **Analytics dashboard**: Track usage, popular questions

---

## Conclusion

This design prioritizes:
1. **Simplicity**: Easy to understand, deploy, and maintain
2. **Cost-effectiveness**: Free-tier components where possible
3. **Quality**: Good-enough accuracy for policy Q&A
4. **Measurability**: Clear metrics for evaluation
5. **Reproducibility**: Deterministic, testable system

The architecture is intentionally minimal for an educational project while demonstrating production RAG concepts.

---

**Version**: 1.0
**Last Updated**: January 2025
**Author**: Luciano Grana
