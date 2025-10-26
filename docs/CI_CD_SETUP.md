# CI/CD Pipeline Documentation

This project uses GitHub Actions for continuous integration and continuous deployment (CI/CD).

## Pipeline Overview

The CI/CD pipeline automatically runs on:
- **Push to `main` branch**: Runs tests and deploys to Railway
- **Push to `develop` branch**: Runs tests only (no deployment)
- **Pull requests to `main`**: Runs tests to verify changes

## Workflow Stages

### 1. Build and Test

Located at: `.github/workflows/ci-cd.yml`

**Steps**:
1. **Checkout code**: Gets latest code from repository
2. **Set up Python 3.10**: Installs Python environment
3. **Cache dependencies**: Speeds up builds by caching pip packages
4. **Install dependencies**: Runs `pip install -r requirements.txt`
5. **Smoke tests**: Verifies all modules can be imported
6. **Run pytest** (if tests exist): Executes test suite
7. **Code formatting check**: Validates code style with `black`

**Smoke Tests Include**:
```python
✓ App imports successful
✓ DocumentProcessor imports successful
✓ EmbeddingModel imports successful
✓ VectorStore imports successful
✓ RAGPipeline imports successful
✓ Evaluator imports successful
```

### 2. Deploy (Main Branch Only)

**Trigger**: Only runs when code is pushed to `main` branch

**Deployment Target**: Railway (auto-deploy from GitHub)

Railway automatically deploys when:
- Code is pushed to `main` branch
- GitHub Actions build succeeds
- Railway detects changes via GitHub webhook

## Current Status

### ✅ What's Working

- Automated testing on every push
- Import validation (smoke tests)
- Code formatting checks
- Automatic deployment to Railway on `main` branch push

### 📊 Build Status

You can see the build status in your GitHub repository:
- Go to: https://github.com/Luciano-Grana/techcorp-policy-qa/actions
- Latest runs show build and test results
- Green checkmark = passing, red X = failing

## Railway Integration

Railway automatically deploys from GitHub without requiring additional GitHub Actions steps.

**How it works**:
1. You push code to `main` branch
2. GitHub Actions runs tests
3. If tests pass, Railway detects the push
4. Railway automatically rebuilds and deploys

**No secrets required** - Railway uses OAuth with GitHub

### Optional: Railway Token (Advanced)

If you want explicit deployment triggers from GitHub Actions:

1. **Get Railway Token**:
   - Go to https://railway.app/account/tokens
   - Create new token
   - Copy token value

2. **Add to GitHub Secrets**:
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `RAILWAY_TOKEN`
   - Value: Your Railway token
   - Click "Add secret"

3. **Update workflow** (already configured in `ci-cd.yml`)

## Test Suite

### Existing Tests

Located at: `tests/test_basic.py`

**Current tests**:
- `test_document_processor_initialization()`: Validates DocumentProcessor setup
- `test_embedding_model_initialization()`: Validates EmbeddingModel setup
- `test_document_creation()`: Validates Document objects
- `test_embed_single_query()`: Tests single query embedding
- `test_embed_multiple_documents()`: Tests batch embedding

### Running Tests Locally

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_basic.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term
```

### Adding More Tests

To add more tests, create files in `tests/` following the pattern:

```python
# tests/test_rag_pipeline.py
import pytest
from src.rag_pipeline import RAGPipeline
from src.vector_store import VectorStore

def test_rag_pipeline_initialization():
    """Test RAG pipeline can be initialized."""
    store = VectorStore()
    rag = RAGPipeline(vector_store=store)
    assert rag.vector_store is not None
    assert rag.model is not None
```

## Code Quality Checks

### Black Formatting

The pipeline checks code formatting with `black`:

```bash
# Check formatting locally
black --check src/ app.py

# Auto-format code
black src/ app.py
```

**Configuration**: Uses default Black settings (88 char line length)

### Adding More Checks (Optional)

You can add additional quality checks:

**Pylint** (linting):
```yaml
- name: Run pylint
  run: |
    pip install pylint
    pylint src/ --fail-under=8.0
```

**MyPy** (type checking):
```yaml
- name: Run mypy
  run: |
    pip install mypy
    mypy src/
```

## Viewing Build Results

### GitHub Actions Dashboard

1. Go to your repository on GitHub
2. Click "Actions" tab
3. See all workflow runs
4. Click on any run to see detailed logs

### Build Badges (Optional)

Add a build status badge to your README:

```markdown
![CI/CD](https://github.com/Luciano-Grana/techcorp-policy-qa/actions/workflows/ci-cd.yml/badge.svg)
```

Shows: ![CI/CD](https://github.com/Luciano-Grana/techcorp-policy-qa/actions/workflows/ci-cd.yml/badge.svg)

## Troubleshooting

### Build Fails on Dependency Installation

**Issue**: `pip install` fails or times out

**Solutions**:
- Check `requirements.txt` for version conflicts
- Ensure all packages are available on PyPI
- Add `--timeout 300` to pip install command

### Tests Pass Locally But Fail in CI

**Common causes**:
- Missing environment variables (CI doesn't have `.env`)
- File path differences (use relative paths)
- Dependencies not in `requirements.txt`

**Solution**: Make tests independent of local environment

### Railway Not Deploying After Push

**Check**:
1. Railway dashboard shows the push
2. Railway build logs for errors
3. GitHub webhook is configured in Railway settings

**Fix**: Go to Railway → Settings → check GitHub connection

## Best Practices

### ✅ Do:
- Keep tests fast (<30 seconds total)
- Test core functionality, not external APIs
- Use mocks for external dependencies
- Commit working code to `main`
- Review test failures before merging

### ❌ Don't:
- Test with real API keys in CI
- Commit breaking changes to `main`
- Skip tests by forcing pushes
- Test deployment-specific features in unit tests

## Future Enhancements

Potential improvements to the CI/CD pipeline:

1. **Add coverage reporting**: Track test coverage over time
2. **Security scanning**: Use tools like `bandit` or `safety`
3. **Performance testing**: Benchmark RAG pipeline speed
4. **Preview deployments**: Deploy PRs to temporary URLs
5. **Slack/Discord notifications**: Alert on build failures
6. **Semantic versioning**: Auto-tag releases

## Summary

✅ **Continuous Integration**: Automated tests on every push
✅ **Continuous Deployment**: Automatic Railway deployment from `main`
✅ **Code Quality**: Format checking with Black
✅ **Fast Builds**: Cached dependencies (~2-3 minutes)
✅ **Minimal Configuration**: Works out of the box

Your CI/CD pipeline ensures code quality and automatic deployment with minimal manual intervention.
