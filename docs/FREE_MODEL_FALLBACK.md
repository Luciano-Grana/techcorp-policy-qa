# Free Model Fallback Strategy

When OpenRouter free models hit rate limits, try these in order:

## Current Free Models (October 2025)

Try in this order until one works:

1. **DeepSeek R1**
   ```
   LLM_MODEL=deepseek/deepseek-r1:free
   ```

2. **DeepSeek R1 Distill Llama**
   ```
   LLM_MODEL=deepseek/deepseek-r1-distill-llama-70b:free
   ```

3. **DeepSeek R1 Distill Qwen**
   ```
   LLM_MODEL=deepseek/deepseek-r1-distill-qwen-14b:free
   ```

4. **Google Gemini 2.0 Flash**
   ```
   LLM_MODEL=google/gemini-2.0-flash-exp:free
   ```

5. **Google Gemini 2.5 Flash**
   ```
   LLM_MODEL=google/gemini-2.5-flash-image-preview:free
   ```

## How to Switch Models

### Locally
Edit `.env`:
```bash
nano .env
# Change LLM_MODEL to one of the models above
# Save and restart app
```

### On Render
1. Go to Environment tab
2. Edit `LLM_MODEL` variable
3. Save and redeploy

## Rate Limit Strategy

If you get **429 errors**:
1. Wait 15-30 minutes
2. Try a different model from the list above
3. OR add $5 credit to OpenRouter for reliable access

## Paid Alternative (Recommended for Production)

Add $5 to OpenRouter and use:
```
LLM_MODEL=openai/gpt-3.5-turbo
```

Cost: ~$0.001 per question (5,000 questions for $5)
