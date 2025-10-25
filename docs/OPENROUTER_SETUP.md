# OpenRouter Setup Guide

## ✅ Your API Key is Configured!

Your OpenRouter API key has been set up and the application is ready to use.

---

## What is OpenRouter?

OpenRouter is a unified API that gives you access to multiple LLM providers (OpenAI, Anthropic, Meta, Google, etc.) through a single interface. It offers **free tier models** perfect for development and testing.

**Website**: https://openrouter.ai/

---

## Configuration

### ✅ Already Done

Your `.env` file should be configured with:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

**Get your API key from**: https://openrouter.ai/keys

### Available Free Models

OpenRouter offers several free models you can use:

| Model | Name | Description |
|-------|------|-------------|
| **Llama 3.1 8B** | `meta-llama/llama-3.1-8b-instruct:free` | Meta's latest, great for general tasks |
| **Gemma 2 9B** | `google/gemma-2-9b-it:free` | Google's efficient model |
| **Mistral 7B** | `mistralai/mistral-7b-instruct:free` | Fast and capable |

To change models, edit `LLM_MODEL` in your `.env` file.

---

## How It Works

The application has been modified to automatically detect and use OpenRouter:

```python
# In src/rag_pipeline.py
if os.getenv("OPENROUTER_API_KEY"):
    openai.api_key = os.getenv("OPENROUTER_API_KEY")
    openai.api_base = "https://openrouter.ai/api/v1"
    print("Using OpenRouter API")
```

OpenRouter uses the OpenAI-compatible API, so no major code changes were needed!

---

## Running the Application

### 1. Start the Server

```bash
python3 app.py
```

You should see:
```
Using OpenRouter API
Vector store loaded with 125 documents
RAG pipeline initialized
 * Running on http://0.0.0.0:5000
```

### 2. Open Browser

Navigate to: **http://localhost:5000**

### 3. Ask Questions!

Try these example questions:
- "How much PTO do employees get?"
- "What is the remote work policy?"
- "Can I expense gym memberships?"
- "What are the password requirements?"

---

## Advantages of OpenRouter

### ✅ Free Tier
- No credit card required for free models
- Generous rate limits for development
- Multiple model options

### ✅ Easy Switching
Change models by editing `.env`:
```bash
# Try different models
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free
# or
LLM_MODEL=google/gemma-2-9b-it:free
# or
LLM_MODEL=mistralai/mistral-7b-instruct:free
```

### ✅ OpenAI Compatible
Uses the same API format as OpenAI, so the code works with minimal changes.

### ✅ Fallback Support
The app also supports:
- OpenAI (set `OPENAI_API_KEY`)
- Groq (modify `api_base` to Groq endpoint)

---

## Model Comparison

### Llama 3.1 8B (Current Default)
- **Best for**: General Q&A, policy questions
- **Speed**: Fast (~1-2s per response)
- **Quality**: Very good for most tasks
- **Context**: 8K tokens

### Gemma 2 9B
- **Best for**: Detailed explanations
- **Speed**: Fast
- **Quality**: Excellent reasoning
- **Context**: 8K tokens

### Mistral 7B
- **Best for**: Quick, concise answers
- **Speed**: Very fast
- **Quality**: Good
- **Context**: 8K tokens

---

## Monitoring Usage

OpenRouter provides a dashboard to monitor your usage:
1. Go to https://openrouter.ai/
2. Sign in with your account
3. View "Usage" to see request history

---

## Rate Limits (Free Tier)

Free tier limits vary by model but are generous for development:
- ~200 requests per day for free models
- Rate limiting is per-model
- Switch models if you hit a limit

---

## Troubleshooting

### "Invalid API key"
- Check that your API key is correct in `.env`
- Make sure there are no extra spaces
- Verify the key is active at https://openrouter.ai/keys

### "Rate limit exceeded"
- Wait a few minutes
- Switch to a different free model
- Check usage dashboard

### "Model not found"
- Verify model name in `.env`
- Check available models at https://openrouter.ai/models
- Ensure you're using `:free` suffix for free models

### Slow responses
- First request is always slower (model loading)
- Free tier may have occasional queueing
- Try a different free model
- Response time: typically 1-3 seconds

---

## Testing

### Quick Test

```bash
# Test with a simple question
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How much PTO do employees get?"}'
```

### Run Full Evaluation

```bash
python3 src/evaluation.py
```

Note: Evaluation with OpenRouter free models may take longer (~5-10 minutes for 30 questions).

---

## Switching Back to OpenAI

If you want to use OpenAI instead:

1. Edit `.env`:
```bash
# Comment out OpenRouter
# OPENROUTER_API_KEY=...

# Add OpenAI key
OPENAI_API_KEY=your-openai-key-here
LLM_MODEL=gpt-3.5-turbo
```

2. Restart the app

The code automatically detects which API to use based on environment variables.

---

## Best Practices

### For Development
✅ Use free tier models (Llama 3.1 8B recommended)
✅ Test locally before deploying
✅ Monitor usage dashboard

### For Production
- Consider paid tier for better rate limits
- Use models with longer context windows
- Set up error handling for rate limits
- Monitor costs via OpenRouter dashboard

---

## OpenRouter vs OpenAI

| Feature | OpenRouter (Free) | OpenAI |
|---------|------------------|---------|
| **Cost** | Free | $0.50/M tokens (GPT-3.5) |
| **Setup** | No credit card | Credit card required |
| **Models** | Multiple options | OpenAI only |
| **Speed** | Fast | Very fast |
| **Rate Limits** | ~200/day | Pay as you go |
| **Best For** | Development, learning | Production |

---

## Additional Resources

- **OpenRouter Docs**: https://openrouter.ai/docs
- **Model Comparison**: https://openrouter.ai/models
- **API Keys**: https://openrouter.ai/keys
- **Usage Dashboard**: https://openrouter.ai/activity

---

## Summary

✅ **OpenRouter is configured and ready!**

Your application will:
1. Use your OpenRouter API key automatically
2. Route requests to Llama 3.1 8B (free tier)
3. Work exactly like the OpenAI version
4. Cost you $0 for development

**Next Step**: Run `python3 app.py` and start asking questions! 🚀

---

**Questions?** Check the [main README](README.md) or OpenRouter documentation.
