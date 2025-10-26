# AI Code Tools Usage

## Overview

This document describes the AI code tools used during the development of the TechCorp Policy Q&A Assistant and how they were applied throughout the project lifecycle.

---

## AI Tools Used

### 1. Claude Code (Primary Development Assistant)

**Tool**: Anthropic Claude (Sonnet 4.5) via Claude Code extension in VSCode

**Usage Scope**: Extensive use throughout the entire project for:
- Architecture design and implementation
- Code generation and refactoring
- Documentation writing
- Debugging and troubleshooting
- Deployment configuration
- CI/CD pipeline setup

#### Specific Applications

**a) Initial Project Architecture**
- **What**: Designed modular RAG system architecture
- **How**: Discussed requirements and received design recommendations for component separation
- **Output**: Module structure (DocumentProcessor, EmbeddingModel, VectorStore, RAGPipeline, Evaluator)
- **Human Role**: Provided requirements, reviewed designs, made final decisions

**b) Core Component Implementation**
- **What**: Implemented RAG pipeline components from scratch
- **How**: Iterative development with Claude generating code and explaining design choices
- **Files Generated**:
  - `src/document_processor.py` - Document parsing and chunking
  - `src/embeddings.py` - Sentence Transformers integration
  - `src/vector_store.py` - ChromaDB wrapper
  - `src/rag_pipeline.py` - Retrieval and generation orchestration
  - `src/evaluation.py` - Automated evaluation framework
  - `app.py` - Flask web application
- **Human Role**: Specified functional requirements, tested components, validated behavior

**c) Prompt Engineering**
- **What**: Developed prompts for answer generation and guardrails
- **How**: Iteratively refined prompts to improve groundedness and citation quality
- **Example**: System prompt instructing LLM to cite sources and refuse out-of-scope questions
- **Human Role**: Tested prompts with edge cases, provided feedback on answer quality

**d) Evaluation Framework**
- **What**: Built automated evaluation system with LLM-as-judge
- **How**: Claude generated evaluation pipeline, test set structure, and metrics calculation
- **Files**:
  - `evaluate_rag.py` - Main evaluation script
  - `evaluation/test_set.json` - 30-question test set
  - `evaluation_results/` - Metrics and detailed results
- **Human Role**: Designed test cases, validated metrics, interpreted results

**e) Debugging and Troubleshooting**
- **What**: Diagnosed and fixed issues throughout development
- **Examples**:
  - Memory errors during Render deployment (resolved by switching to Railway)
  - OpenRouter API rate limiting (resolved by purchasing credits)
  - Railway CI wait configuration (resolved by implementing develop→main workflow)
  - GitHub Actions permissions (resolved by adding write permissions)
- **How**: Claude analyzed error logs, proposed solutions, implemented fixes
- **Human Role**: Provided error messages, tested solutions, validated fixes

**f) Documentation**
- **What**: Generated comprehensive project documentation
- **How**: Claude wrote markdown documentation based on implementation
- **Files Created**:
  - `README.md` - Project overview and setup instructions
  - `docs/DESIGN.md` - Architecture and design decisions
  - `docs/QUICKSTART.md` - 10-minute setup guide
  - `docs/DEPLOYMENT.md` - Production deployment instructions
  - `docs/PROJECT_SUMMARY.md` - Requirements checklist
  - `docs/CI_CD_SETUP.md` - CI/CD pipeline documentation
  - `docs/DEVELOPMENT_WORKFLOW.md` - Git workflow guide
  - `design-and-evaluation.md` - This document
  - `ai-use.md` - This AI usage documentation
- **Human Role**: Reviewed documentation, requested clarifications, validated accuracy

**g) Deployment Configuration**
- **What**: Configured deployment infrastructure
- **How**: Claude generated configuration files and deployment instructions
- **Files**:
  - `Procfile` - Gunicorn web server configuration
  - `railway.json` - Railway deployment settings
  - `.github/workflows/ci-cd.yml` - CI/CD pipeline
  - Environment variable configuration
- **Human Role**: Created accounts (Railway, OpenRouter), configured secrets, tested deployments

**h) CI/CD Pipeline**
- **What**: Implemented automated testing and deployment workflow
- **How**: Claude designed and implemented GitHub Actions workflow with develop→main auto-merge strategy
- **Iterations**:
  1. Initial CI/CD with Railway "Wait for CI" (didn't work)
  2. Branch protection approach (blocked direct pushes)
  3. Webhook/API approach (Railway lacks webhook)
  4. Final: develop→main auto-merge after CI passes ✅
- **Human Role**: Tested workflow, reported issues, approved final approach

**i) Git Operations**
- **What**: Managed version control and repository organization
- **How**: Claude executed git commands for commits, pushes, file moves
- **Examples**:
  - Moving markdown files to `docs/` directory
  - Creating develop branch
  - Crafting commit messages with co-authorship
- **Human Role**: Approved changes, reviewed commits, managed GitHub repository settings

---

## How AI Was Used

### Development Workflow Pattern

The typical workflow for using Claude Code was:

1. **Human describes requirement or problem**
   - Example: "I need to implement a RAG pipeline that retrieves policy documents and generates answers"

2. **Claude proposes solution**
   - Explains approach
   - Suggests architecture
   - Provides code implementation

3. **Human reviews and tests**
   - Runs code locally
   - Tests edge cases
   - Identifies issues

4. **Iterative refinement**
   - Claude fixes bugs
   - Improves implementation
   - Adds features

5. **Human validates final solution**
   - Confirms functionality
   - Approves for deployment

### Code Generation vs. Code Review

**Code Generated by AI**: ~95% of codebase
- All Python modules (src/, app.py, evaluate_rag.py)
- All configuration files (Procfile, railway.json, .github/workflows/ci-cd.yml)
- All documentation (docs/, README.md, etc.)
- Test set (evaluation/test_set.json)

**Code Written by Human**: ~5%
- Policy documents (data/*.md) - provided as project input
- Environment variables (.env) - configured with API keys
- Railway/GitHub settings - configured via web interfaces

**Code Reviewed by Human**: 100%
- All generated code was reviewed, tested, and validated
- Final decisions on architecture and approach made by human
- Edge cases and requirements specified by human

### AI Limitations Encountered

**1. Deployment Platform Knowledge**
- **Issue**: Claude assumed Railway had webhook/API deployment triggers
- **Reality**: Railway's "Wait for CI" feature works differently
- **Resolution**: Human tested Railway settings, Claude adapted to develop→main workflow

**2. Error Message Interpretation**
- **Issue**: Some errors required multiple iterations to diagnose
- **Example**: GitHub Actions permission errors needed permission block addition
- **Resolution**: Human provided detailed logs, Claude proposed fixes iteratively

**3. External Service Behavior**
- **Issue**: Claude couldn't predict exact behavior of external APIs (OpenRouter rate limits)
- **Resolution**: Human experienced errors in production, reported them, Claude proposed solutions

**4. Project Requirements**
- **Issue**: AI needed clear specifications to generate appropriate solutions
- **Resolution**: Human provided detailed requirements, reviewed outputs, requested changes

---

## Benefits of AI Usage

### 1. Development Speed
- **Estimate**: 10x faster development compared to manual coding
- **Example**: RAG pipeline implementation (2 hours vs. estimated 20+ hours manually)
- **Reason**: Instant code generation, no syntax lookup, immediate documentation

### 2. Code Quality
- **Modular Design**: AI suggested clean separation of concerns
- **Error Handling**: Comprehensive try-catch blocks and error messages
- **Type Hints**: Consistent use of Python type annotations
- **Documentation**: Inline comments and docstrings generated automatically

### 3. Learning Value
- **Explanations**: Claude explained design decisions and trade-offs
- **Best Practices**: Generated code followed Python conventions
- **Architecture**: Learned RAG system design patterns
- **Debugging**: Learned systematic troubleshooting approaches

### 4. Documentation Completeness
- **Coverage**: Comprehensive docs for all components
- **Consistency**: Uniform formatting and structure
- **Examples**: Concrete usage examples in all docs
- **Maintenance**: Easy to update as code changed

### 5. Reduced Context Switching
- **Seamless Flow**: Ask questions and get code without leaving IDE
- **Iterative Development**: Quick feedback loop for refinement
- **Multi-task Handling**: Generate code, docs, config simultaneously

---

## Human Contributions

While AI generated most code, human contributions were essential:

### 1. Project Vision and Requirements
- Defined goal: RAG-based policy Q&A system
- Specified evaluation criteria (groundedness, citations, latency)
- Chose deployment constraints (low cost, simple infrastructure)

### 2. Domain Knowledge
- Provided policy documents (data/*.md)
- Designed test questions covering realistic scenarios
- Validated answer quality against actual policies

### 3. Decision Making
- Technology choices (ChromaDB, Railway, OpenRouter)
- Architecture approval (modular design, custom RAG vs. LangChain)
- Trade-off evaluation (local embeddings vs. OpenAI embeddings)

### 4. Testing and Validation
- Tested all components locally
- Ran evaluation on test set
- Validated deployment in production
- Verified CI/CD pipeline behavior

### 5. Infrastructure Setup
- Created accounts (GitHub, Railway, OpenRouter)
- Configured secrets and environment variables
- Managed repository settings (branches, permissions)
- Purchased API credits

### 6. Quality Assurance
- Reviewed all generated code
- Tested edge cases
- Validated documentation accuracy
- Ensured project met academic requirements

---

## Transparency and Attribution

### Code Attribution
All code commits include co-authorship attribution:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Documentation Attribution
Documentation acknowledges AI generation:
```
🤖 Generated with Claude Code
```

### Academic Integrity
- **Tool Purpose**: AI used as development accelerator, not replacement for learning
- **Human Oversight**: All code reviewed, tested, and understood by human
- **Learning Outcomes**: Project demonstrates understanding of RAG systems, not just code generation
- **Evaluation**: System evaluated against objective metrics (groundedness, citations, latency)

---

## Lessons Learned

### What Worked Well
1. **Iterative Development**: Quick feedback loop enabled rapid refinement
2. **Modular Architecture**: Claude's suggested design was clean and maintainable
3. **Documentation**: AI-generated docs were comprehensive and consistent
4. **Debugging**: Systematic troubleshooting with error log analysis
5. **Code Generation**: High-quality, idiomatic Python code

### What Required Human Intervention
1. **External Services**: Testing Railway, OpenRouter, GitHub Actions behavior
2. **Requirements Clarification**: Specifying edge cases and constraints
3. **Decision Making**: Choosing between alternative approaches
4. **Infrastructure Setup**: Creating accounts, configuring secrets
5. **Quality Validation**: Testing against real user needs

### Future Improvements
1. **Earlier Production Testing**: Test deployment earlier to catch platform limitations
2. **More Explicit Requirements**: Specify constraints upfront (cost, latency targets)
3. **Incremental Commits**: Commit more frequently during development
4. **Test-Driven Development**: Write tests before implementation
5. **Code Review Checklist**: Systematic review process for AI-generated code

---

## Conclusion

AI tools, specifically Claude Code, were instrumental in developing this RAG application efficiently while maintaining high code quality. The key to successful AI usage was:

1. **Clear Requirements**: Providing specific, detailed requirements to the AI
2. **Human Oversight**: Reviewing, testing, and validating all AI outputs
3. **Iterative Refinement**: Using feedback loops to improve solutions
4. **Decision Authority**: Keeping humans in control of architecture and approach
5. **Transparency**: Clearly attributing AI contributions

The project demonstrates that AI can dramatically accelerate development while preserving learning value, provided the human maintains active involvement in design, testing, and validation.

---

**Project**: TechCorp Policy Q&A Assistant
**Author**: Luciano Grana
**Institution**: Quantic School of Business and Technology
**Course**: Master of Science in Software Engineering - AI Engineering
**Primary AI Tool**: Claude Code (Anthropic Claude Sonnet 4.5)
**Date**: October 2025
