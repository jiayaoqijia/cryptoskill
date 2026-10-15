# Pika MCP Plugin for GenTech Agent Kit

Video generation and creative content skills for AI agents via Pika.

## Architecture

Two integration paths:

### 1. Pika MCP Server (Recommended)
Pika hosts an MCP server at `https://mcp.pika.me/api/mcp` (or `https://experiment-mcp.pika.art/api/mcp`). Connect any MCP-compatible client:

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  pika:
    url: "https://mcp.pika.me/api/mcp"
    timeout: 300
    connect_timeout: 120
```

One-time OAuth required. Supports 14+ models: Pika Video, Sora, Veo 3, Kling, MiniMax, ElevenLabs, Whisper.

### 2. Fal.ai API Client (Programmatic)
Standalone Python client for the Pika API via Fal.ai. Requires `FAL_KEY`:

```python
from pika_client import PikaClient

client = PikaClient(api_key="your-fal-key")
result = client.text_to_video(prompt="A cat dancing on a rainbow")
print(result.video_url)
```

## Available MCP Tools

| Tool | Description | Price |
|------|-------------|-------|
| `pika_text_to_video` | Generate video from text | Pika credits |
| `pika_image_to_video` | Animate a starting image | Pika credits |
| `pika_health` | Check API configuration | Free |

## Pika Skills (Slash Commands)

Pika's MCP server also provides pre-built skills activated via slash commands:

| Skill | Command | Use Case |
|-------|---------|----------|
| 4K VFX | `/4k-vfx` | Turn clips into VFX shots |
| App Sizzle | `/app-sizzle` | 15s launch video from repo/URL |
| Build-a-Brand | `/build-a-brand` | Full brand guidelines |
| Explainer | `/explainer` | URL → narrated explainer |
| Founder Video | `/founder-product-video` | Talking-head avatar |
| UGC Ads | `/ugc-ads` | UGC-style ad variants |
| Podcast | `/podcast` | AI-hosted podcast video |
| Viral Hook | `/viral-hook` | Scroll-stopping shorts |
| Persona Builder | `/persona-builder` | Content playbook |

## Setup

```bash
# Install plugin dependencies
pip install -r requirements.txt

# Run MCP server (stdio transport)
python -m server

# Run tests
python -m pytest tests/ -v
```

## Files

```
plugins/pika-mcp/
├── __init__.py         # Package init
├── pika_client.py      # Fal.ai Pika API client
├── server.py           # MCP server (stdio transport)
├── requirements.txt    # Dependencies
├── README.md           # This file
└── tests/
    ├── __init__.py
    └── test_server.py  # 17 tests
```
