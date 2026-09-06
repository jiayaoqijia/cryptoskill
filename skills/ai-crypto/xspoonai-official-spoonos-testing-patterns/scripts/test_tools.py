#!/usr/bin/env python3
"""Example unit tests for SpoonOS tools."""

import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_price_tool_success():
    """Test successful price fetch."""
    from spoon_ai.tools.base import BaseTool

    # Mock tool implementation
    class PriceTool(BaseTool):
        name = "get_price"

        async def execute(self, coin_id: str, currency: str = "usd"):
            return f"{coin_id.upper()}: $50,000 {currency.upper()}"

    tool = PriceTool()
    result = await tool.execute(coin_id="bitcoin", currency="usd")

    assert "50,000" in result
    assert "BTC" in result or "BITCOIN" in result


@pytest.mark.asyncio
async def test_price_tool_with_mock():
    """Test with mocked HTTP response."""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "bitcoin": {"usd": 50000, "usd_24h_change": 2.5}
        })
        mock_get.return_value.__aenter__.return_value = mock_response

        # Your actual tool test here
        assert True  # Replace with actual assertions


def test_tool_parameters_schema():
    """Verify tool parameter schema."""
    from spoon_ai.tools.base import BaseTool
    from pydantic import Field

    class TestTool(BaseTool):
        name = "test_tool"
        parameters: dict = Field(default={
            "type": "object",
            "properties": {
                "param1": {"type": "string"}
            },
            "required": ["param1"]
        })

        async def execute(self, param1: str):
            return param1

    tool = TestTool()
    params = tool.parameters

    assert params["type"] == "object"
    assert "param1" in params["properties"]
    assert "param1" in params["required"]
