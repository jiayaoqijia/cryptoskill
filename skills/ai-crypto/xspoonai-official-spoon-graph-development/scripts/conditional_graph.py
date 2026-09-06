#!/usr/bin/env python3
"""Conditional routing in StateGraph."""

import asyncio
from typing import TypedDict, Literal
from spoon_ai.graph import StateGraph, END


class RouterState(TypedDict):
    input: str
    category: str
    result: str


async def classify_node(state: RouterState) -> dict:
    """Classify input to determine routing."""
    input_text = state["input"].lower()

    if "price" in input_text or "cost" in input_text:
        category = "price"
    elif "news" in input_text or "update" in input_text:
        category = "news"
    else:
        category = "general"

    return {"category": category}


async def price_handler(state: RouterState) -> dict:
    """Handle price-related queries."""
    return {"result": f"Price info for: {state['input']}"}


async def news_handler(state: RouterState) -> dict:
    """Handle news-related queries."""
    return {"result": f"News results for: {state['input']}"}


async def general_handler(state: RouterState) -> dict:
    """Handle general queries."""
    return {"result": f"General response for: {state['input']}"}


def route_by_category(state: RouterState) -> Literal["price", "news", "general"]:
    """Router function for conditional edges."""
    return state["category"]


def build_graph() -> StateGraph:
    graph = StateGraph(RouterState)

    # Add nodes
    graph.add_node("classify", classify_node)
    graph.add_node("price", price_handler)
    graph.add_node("news", news_handler)
    graph.add_node("general", general_handler)

    # Set entry point
    graph.set_entry_point("classify")

    # Add conditional routing
    graph.add_conditional_edges(
        "classify",
        route_by_category,
        {
            "price": "price",
            "news": "news",
            "general": "general"
        }
    )

    # All handlers go to END
    graph.add_edge("price", END)
    graph.add_edge("news", END)
    graph.add_edge("general", END)

    return graph


async def main():
    graph = build_graph()
    app = graph.compile()

    # Test different inputs
    queries = [
        "What's the price of Bitcoin?",
        "Latest news about Ethereum",
        "How does blockchain work?"
    ]

    for query in queries:
        result = await app.invoke({
            "input": query,
            "category": "",
            "result": ""
        })
        print(f"Query: {query}")
        print(f"Category: {result['category']}")
        print(f"Result: {result['result']}\n")


if __name__ == "__main__":
    asyncio.run(main())
