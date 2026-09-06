#!/usr/bin/env python3
"""Pytest fixtures for SpoonOS testing."""

import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_chatbot():
    """Create a mock ChatBot that returns predefined responses."""
    from spoon_ai.chat import ChatBot

    chatbot = MagicMock(spec=ChatBot)

    async def mock_chat(messages, tools=None, **kwargs):
        last_message = messages[-1]["content"]

        if "price" in last_message.lower():
            return MagicMock(
                content="I'll check the price for you.",
                tool_calls=[{
                    "id": "call_123",
                    "function": {
                        "name": "get_price",
                        "arguments": '{"coin_id": "bitcoin"}'
                    }
                }]
            )
        else:
            return MagicMock(
                content="I don't understand that request.",
                tool_calls=None
            )

    chatbot.chat = AsyncMock(side_effect=mock_chat)
    return chatbot


@pytest.fixture
def mock_tool_response():
    """Fixture for mocking tool execution."""
    async def _mock_response(tool_name, expected_result):
        tool = MagicMock()
        tool.execute = AsyncMock(return_value=expected_result)
        return tool
    return _mock_response


@pytest.fixture(scope="session")
def real_agent():
    """Create a real agent for integration tests."""
    from spoon_ai.agents import SpoonReactMCP
    from spoon_ai.chat import ChatBot
    from spoon_ai.tools import ToolManager

    return SpoonReactMCP(
        name="test_agent",
        llm=ChatBot(model_name="gpt-4o-mini"),
        tools=ToolManager([]),
        max_steps=5
    )


@pytest.fixture
def isolated_agent(real_agent):
    """Get agent with fresh state."""
    real_agent.reset()
    return real_agent
