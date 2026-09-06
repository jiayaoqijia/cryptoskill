---
name: spoon-tool-development
description: Develop tools for SpoonOS agents. Use when creating custom tools, MCP servers, toolkit extensions, or configuring tool managers.
---

# Tool Development

Build tools for SpoonOS agents using BaseTool and FastMCP.

## Tool Types

| Type | Use Case |
|------|----------|
| `BaseTool` | Local Python tools |
| `MCPTool` | External MCP servers |
| `FastMCP` | Build MCP servers |

## Quick Start

```python
from spoon_ai.tools.base import BaseTool
from pydantic import Field

class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "Tool description"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "param": {"type": "string"}
        },
        "required": ["param"]
    })

    async def execute(self, param: str) -> str:
        return f"Result: {param}"
```

## Scripts

| Script | Purpose |
|--------|---------|
| [base_tool.py](scripts/base_tool.py) | BaseTool implementation |
| [mcp_tool.py](scripts/mcp_tool.py) | MCPTool configuration |
| [fastmcp_server.py](scripts/fastmcp_server.py) | FastMCP server |
| [tool_manager.py](scripts/tool_manager.py) | ToolManager usage |

## References

| Reference | Content |
|-----------|---------|
| [error_handling.md](references/error_handling.md) | Error patterns |
| [testing.md](references/testing.md) | Testing tools |

## ToolManager Methods

| Method | Description |
|--------|-------------|
| `add_tool(tool)` | Add single tool |
| `remove_tool(name)` | Remove by name |
| `execute(name, input)` | Execute tool |
| `to_params()` | Get OpenAI specs |

## Best Practices

1. Use async for all I/O operations
2. Return ToolResult/ToolFailure
3. Validate inputs before execution
4. Implement proper error handling
5. Use environment variables for secrets
