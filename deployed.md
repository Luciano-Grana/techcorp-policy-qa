# Deployed Application

## Live Demo

The TechCorp Policy Q&A Assistant is deployed and accessible at:

**https://web-production-19d49a.up.railway.app**

## Deployment Platform

- **Platform**: Railway (https://railway.app)
- **Pricing Model**: Pay-as-you-go (Hobby Plan - $5/month usage-based)
- **Deployment Method**: Automated deployment from `main` branch via CI/CD pipeline
- **Build System**: Nixpacks (automatic detection)

## Application Details

- **Application Type**: Flask web application with RAG-based Q&A chatbot
- **LLM**: OpenAI GPT-3.5 Turbo (via OpenRouter API)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2, local)
- **Vector Database**: ChromaDB (persistent storage)
- **Documents**: 8 company policy documents (~70 pages)

## Deployment Status

The application automatically deploys when:
1. Code is pushed to the `develop` branch
2. GitHub Actions CI tests pass successfully
3. CI automatically merges `develop` → `main`
4. Railway detects the update to `main` and deploys

You can monitor the CI/CD pipeline status:

![CI/CD Status](https://github.com/Luciano-Grana/techcorp-policy-qa/actions/workflows/ci-cd.yml/badge.svg)

## Features Available

- Interactive chat interface for policy questions
- Source citations for all answers
- Guardrails to refuse out-of-scope questions
- Persistent conversation history during session
- Responsive web design

## Testing the Deployment

Try asking questions like:
- "What is the remote work policy?"
- "How many vacation days do employees get?"
- "What are the security requirements for passwords?"
- "Tell me about the code review process"

## Technical Infrastructure

- **Runtime**: Python 3.10
- **Web Server**: Gunicorn (production WSGI server)
- **Port**: Dynamically assigned by Railway
- **Environment Variables**: Securely managed via Railway dashboard
- **Persistent Storage**: Vector database persists across deployments

## Cost Analysis

- **LLM API**: ~$0.001 per question (OpenRouter + GPT-3.5 Turbo)
- **Hosting**: ~$5/month (Railway Hobby Plan)
- **Total Monthly Cost**: ~$5-10/month for moderate usage

## Repository

- **GitHub**: https://github.com/Luciano-Grana/techcorp-policy-qa
- **Branch Structure**:
  - `develop` - Development branch (push here)
  - `main` - Production branch (auto-updated by CI)

## Support

For issues or questions:
1. Check the GitHub repository for documentation
2. Review logs in Railway dashboard
3. Contact: Luciano Grana

---

**Project for**: Master of Science in Software Engineering - AI Engineering Course
**Institution**: Quantic School of Business and Technology
**Author**: Luciano Grana
**Deployed**: October 2025
