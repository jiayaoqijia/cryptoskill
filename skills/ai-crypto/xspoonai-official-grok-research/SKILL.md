---
name: grok-research
description: Aggressive web research and information synthesis via Grok-compatible API. Provides structured JSON with sources. Use when: searching latest info, verifying facts, technical docs research.
version: 1.0.0
author: Anonymous
tags: [web-research, grok, search, productivity, ai-agents]
---

# Grok Research

Expert web research skill that uses Grok-compatible endpoints to perform deep searches and synthesize information with explicit source citations.

## Quick Start

```python
# Minimal working example
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="researcher",
    skill_paths=["./grok-research"],
    scripts_enabled=True
)
await agent.activate_skill("grok-research")
result = await agent.execute("What is the current status of SpoonOS?")
```

## Scripts

| Script | Purpose |
|--------|---------|
| [grok_tool.py](scripts/grok_tool.py) | Main tool for performing web research and synthesis. |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROK_API_KEY` | Yes | Your Grok-compatible API key. |
| `GROK_BASE_URL` | Yes | The endpoint URL (OpenAI-compatible). |
| `GROK_MODEL` | No | Model to use (default: grok-2-latest). |

## Best Practices

1. Use specific queries for better search results.
2. Provide context in the query if searching for niche technical topics.
3. Review the `sources` array for deeper verification.
