#!/usr/bin/env python3
"""Concurrent agent execution patterns."""

import asyncio
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.tools import ToolManager


async def execute_tools_concurrently(manager: ToolManager, tasks: list):
    """Execute multiple tool calls concurrently."""

    async def execute_single(task):
        name, inputs = task["name"], task["inputs"]
        try:
            result = await manager.execute(name=name, tool_input=inputs)
            return {"name": name, "success": True, "result": result}
        except Exception as e:
            return {"name": name, "success": False, "error": str(e)}

    results = await asyncio.gather(
        *[execute_single(task) for task in tasks],
        return_exceptions=True
    )
    return results


async def run_agents_concurrently(agents: list, queries: list):
    """Run multiple agents concurrently with different queries."""

    async def run_single(agent, query):
        try:
            await agent.initialize()
            result = await agent.run(query)
            return {"agent": agent.name, "success": True, "result": result}
        except Exception as e:
            return {"agent": agent.name, "success": False, "error": str(e)}

    if len(agents) != len(queries):
        raise ValueError("Number of agents must match number of queries")

    results = await asyncio.gather(
        *[run_single(agent, query) for agent, query in zip(agents, queries)],
        return_exceptions=True
    )
    return results


async def main():
    # Create specialized agents
    research_agent = SpoonReactMCP(name="researcher", max_steps=10)
    analysis_agent = SpoonReactMCP(name="analyst", max_steps=10)
    summary_agent = SpoonReactMCP(name="summarizer", max_steps=5)

    # Run concurrently
    results = await run_agents_concurrently(
        agents=[research_agent, analysis_agent, summary_agent],
        queries=[
            "Find latest DeFi trends",
            "Analyze BTC price movements",
            "Summarize today's crypto news"
        ]
    )

    for result in results:
        print(f"{result['agent']}: {result.get('result', result.get('error'))}")


if __name__ == "__main__":
    asyncio.run(main())
