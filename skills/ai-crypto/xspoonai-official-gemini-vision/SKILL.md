---
name: gemini-vision
description: Analyze images using Google Gemini 2.0 Flash with proxy support, retry logic, and mock mode.
version: 1.0.0
author: Moxan <namemoxan@gmail.com>
tags: [ai, vision, gemini, image-analysis]
---

# Gemini Vision Analyzer

A robust SpoonOS skill for analyzing images using Google's Gemini 2.0 Flash model. It is designed for production environments with built-in support for HTTP proxies, automatic retries for rate limits, and a mock mode for testing without API costs.

## Quick Start

```python
from spoon.skills.gemini_vision import vision_analyze

# Analyze an image
with open("image.jpg", "rb") as f:
    image_bytes = f.read()

result = await vision_analyze(
    image=image_bytes, 
    prompt="Describe this image"
)
print(result)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [main.py](scripts/main.py) | Main implementation of the vision analysis logic |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key |
| `HTTPS_PROXY` | No | Proxy URL (e.g., `http://127.0.0.1:7890`) |
| `MOCK_VISION` | No | Set to `true` to enable mock mode |
| `GEMINI_MODEL` | No | Model name (default: `gemini-2.5-flash`) |

## Best Practices

1. **Use Mock Mode for Dev**: Set `MOCK_VISION=true` during development to save API quota.
2. **Handle Proxies**: If you are in a region where Google API is restricted, ensure `HTTPS_PROXY` is set.
3. **Structured Prompts**: The skill automatically appends JSON formatting instructions, so focus your prompt on *what* to analyze.
