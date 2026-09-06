#!/usr/bin/env python3
"""MCP-enabled SpoonReactMCP agent example."""

import os
import asyncio
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from spoon_ai.tools.mcp_tool import MCPTool


# NPX-based MCP tool
tavily_search = MCPTool(
    name="tavily-search",
    description="Search the web for current information",
    mcp_config={
        "command": "npx",
        "args": ["-y", "tavily-mcp"],
        "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")},
        "timeout": 30,
        "max_retries": 3,
    },
)

# Python-based MCP tool
python_tool = MCPTool(
    name="data-analysis",
    description="Analyze data with custom Python MCP server",
    mcp_config={
        "command": "python",
        "args": ["path/to/mcp_server.py"],
        "env": {"DATA_PATH": "/data"}
    }
)

# URL-based MCP tool (SSE)
sse_tool = MCPTool(
    name="remote-service",
    description="Connect to remote MCP service",
    mcp_config={
        "url": "https://mcp.example.com/sse",
        "transport": "sse"
    }
)


async def main():
    # Create agent with MCP tools
    agent = SpoonReactMCP(
        name="research_agent",
        llm=ChatBot(model_name="gpt-4o", llm_provider="openai"),
        tools=ToolManager([tavily_search]),
        max_steps=15
    )

    # Pre-load MCP tool parameters (important for schema discovery)
    await tavily_search.ensure_parameters_loaded()

    # Initialize agent
    await agent.initialize()

    # Execute query
    result = await agent.run("Find the latest news about Ethereum ETF approval")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
