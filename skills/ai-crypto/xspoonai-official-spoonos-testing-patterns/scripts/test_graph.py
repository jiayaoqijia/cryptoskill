#!/usr/bin/env python3
"""Example tests for StateGraph workflows."""

import pytest
from typing import TypedDict
from spoon_ai.graph import StateGraph, END


class TestState(TypedDict):
    value: int
    processed: bool


def increment(state: TestState) -> dict:
    return {"value": state["value"] + 1}


def double(state: TestState) -> dict:
    return {"value": state["value"] * 2}


def mark_processed(state: TestState) -> dict:
    return {"processed": True}


@pytest.fixture
def simple_graph():
    """Create a simple test graph."""
    graph = StateGraph(TestState)
    graph.add_node("increment", increment)
    graph.add_node("double", double)
    graph.add_node("mark", mark_processed)
    graph.set_entry_point("increment")
    graph.add_edge("increment", "double")
    graph.add_edge("double", "mark")
    graph.add_edge("mark", END)
    return graph.compile()


@pytest.mark.asyncio
async def test_graph_execution(simple_graph):
    """Test graph executes all nodes."""
    result = await simple_graph.invoke({
        "value": 5,
        "processed": False
    })

    # 5 + 1 = 6, 6 * 2 = 12
    assert result["value"] == 12
    assert result["processed"] == True


@pytest.mark.asyncio
async def test_graph_streaming(simple_graph):
    """Test graph streaming output."""
    outputs = []

    async for event in simple_graph.astream({
        "value": 1,
        "processed": False
    }):
        outputs.append(event)

    assert len(outputs) == 3  # One per node


def should_continue(state: TestState) -> str:
    if state["value"] > 100:
        return "end"
    return "continue"


@pytest.fixture
def conditional_graph():
    """Graph with conditional routing."""
    graph = StateGraph(TestState)
    graph.add_node("double", double)
    graph.add_node("finish", mark_processed)
    graph.set_entry_point("double")
    graph.add_conditional_edges(
        "double",
        should_continue,
        {"continue": "double", "end": "finish"}
    )
    graph.add_edge("finish", END)
    return graph.compile()


@pytest.mark.asyncio
async def test_conditional_loop(conditional_graph):
    """Test conditional edge routing."""
    result = await conditional_graph.invoke({
        "value": 10,
        "processed": False
    })

    # 10 -> 20 -> 40 -> 80 -> 160 (> 100, stop)
    assert result["value"] == 160
    assert result["processed"] == True
