---
name: spoon-agent-development
description: Build AI agents with SpoonReactMCP. Use when creating custom agents, configuring tool chains, designing system prompts, or implementing concurrent agent patterns.
---

# Agent Development

Build AI agents using the Spoon AI ReAct framework.

## Agent Hierarchy

```
SpoonReactSkill  → Skills + x402 Payments
    ↓
SpoonReactMCP   → MCP Tool Integration
    ↓
SpoonReactAI    → Base ReAct + Tool Calling
    ↓
ToolCallAgent   → Tool Execution
    ↓
BaseAgent       → Pydantic Foundation
```

## Quick Start

```python
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from spoon_ai.tools.mcp_tool import MCPTool

# Create agent with MCP tool
agent = SpoonReactMCP(
    name="my_agent",
    llm=ChatBot(model_name="gpt-4o"),
    tools=ToolManager([MCPTool(...)]),
    max_steps=15
)

await agent.initialize()
result = await agent.run("Your query here")
```

## Scripts

| Script | Purpose |
|--------|---------|
| [basic_agent.py](scripts/basic_agent.py) | Simple SpoonReactAI agent |
| [mcp_agent.py](scripts/mcp_agent.py) | MCP-enabled agent |
| [custom_tool.py](scripts/custom_tool.py) | Custom BaseTool implementation |
| [concurrent_agents.py](scripts/concurrent_agents.py) | Multi-agent parallel execution |

## References

| Reference | Content |
|-----------|---------|
| [prompts.md](references/prompts.md) | System prompt templates |
| [mcp_config.md](references/mcp_config.md) | MCP configuration options |

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | "spoon_react" | Agent identifier |
| `max_steps` | int | 10 | Max ReAct iterations |
| `tool_choice` | str | "required" | "auto", "required", "none" |
| `system_prompt` | str | None | Custom system prompt |

## Best Practices

1. Pre-load MCP tool parameters before use
2. Use concurrent execution for independent tools
3. Implement retry with exponential backoff
4. Keep system prompts focused and specific
5. Never hardcode API keys
