#!/usr/bin/env python3
"""Basic StateGraph workflow example."""

import asyncio
from typing import TypedDict
from spoon_ai.graph import StateGraph, END


class AnalysisState(TypedDict):
    query: str
    research: str
    analysis: str
    result: str


async def research_node(state: AnalysisState) -> dict:
    """Research phase - gather information."""
    query = state["query"]
    return {"research": f"Research findings for: {query}"}


async def analyze_node(state: AnalysisState) -> dict:
    """Analysis phase - process research."""
    research = state["research"]
    return {"analysis": f"Analysis of: {research}"}


async def summarize_node(state: AnalysisState) -> dict:
    """Summary phase - produce final result."""
    analysis = state["analysis"]
    return {"result": f"Summary: {analysis}"}


def build_graph() -> StateGraph:
    """Build the analysis workflow graph."""
    graph = StateGraph(AnalysisState)

    # Add nodes
    graph.add_node("research", research_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("summarize", summarize_node)

    # Set entry point
    graph.set_entry_point("research")

    # Add edges (linear flow)
    graph.add_edge("research", "analyze")
    graph.add_edge("analyze", "summarize")
    graph.add_edge("summarize", END)

    return graph


async def main():
    graph = build_graph()
    app = graph.compile()

    initial_state = {
        "query": "Bitcoin market trends",
        "research": "",
        "analysis": "",
        "result": ""
    }

    result = await app.invoke(initial_state)
    print(f"Final result: {result['result']}")


if __name__ == "__main__":
    asyncio.run(main())
