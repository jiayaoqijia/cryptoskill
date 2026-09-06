#!/usr/bin/env python3
"""FastMCP server example."""

from fastmcp import FastMCP
from pydantic import BaseModel, Field


# Create MCP server
mcp = FastMCP(name="MyToolsServer")


# Define input schemas
class PriceInput(BaseModel):
    symbol: str = Field(..., description="Token symbol (e.g., BTC, ETH)")
    currency: str = Field("usd", description="Target currency")


class AnalysisInput(BaseModel):
    data: str = Field(..., description="Data to analyze")
    format: str = Field("json", pattern="^(json|csv|text)$")


@mcp.tool()
async def get_price(input: PriceInput) -> str:
    """Get cryptocurrency price."""
    # Replace with actual implementation
    return f"Price of {input.symbol}: $50000 {input.currency.upper()}"


@mcp.tool()
async def analyze_data(input: AnalysisInput) -> str:
    """Analyze data in various formats."""
    return f"Analysis result for {input.format} data"


@mcp.resource("config://settings")
async def get_settings() -> str:
    """Get server configuration."""
    return '{"version": "1.0.0", "supported_chains": ["ethereum", "polygon"]}'


if __name__ == "__main__":
    mcp.run()
