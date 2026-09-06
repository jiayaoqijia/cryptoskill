"""
OpenClaw MCP Bridge for Gold API Feed
Integrates with TBN Ops Center's OpenClaw system
"""

import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from price_feed import GoldAPIFeed, get_price_sync


def handle_mcp_request(request: dict) -> dict:
    """
    Handle MCP (Model Context Protocol) requests from OpenClaw

    Request format:
    {
        "tool": "get_price",
        "params": {"symbol": "XAU"}
    }
    """
    tool = request.get("tool")
    params = request.get("params", {})

    if tool == "get_price":
        symbol = params.get("symbol", "XAU")
        data = get_price_sync(symbol)

        if data:
            return {
                "success": True,
                "result": {
                    "symbol": data.symbol,
                    "name": data.name,
                    "price": data.price,
                    "currency": data.currency,
                    "updated": data.updated_readable
                }
            }
        else:
            return {
                "success": False,
                "error": f"Failed to fetch price for {symbol}"
            }

    elif tool == "get_all_prices":
        from price_feed import get_all_prices_sync
        prices = get_all_prices_sync()

        return {
            "success": True,
            "result": {
                symbol: {
                    "name": data.name,
                    "price": data.price,
                    "updated": data.updated_readable
                }
                for symbol, data in prices.items()
            }
        }

    elif tool == "get_gold_price":
        data = get_price_sync("XAU")
        if data:
            return {
                "success": True,
                "result": {
                    "price": data.price,
                    "formatted": f"${data.price:,.2f}"
                }
            }

    elif tool == "get_bitcoin_price":
        data = get_price_sync("BTC")
        if data:
            return {
                "success": True,
                "result": {
                    "price": data.price,
                    "formatted": f"${data.price:,.2f}"
                }
            }

    return {
        "success": False,
        "error": f"Unknown tool: {tool}"
    }


def main():
    """
    Main entry point for OpenClaw MCP bridge
    Reads JSON from stdin, writes JSON to stdout
    """
    print("Gold API Feed MCP Bridge started", file=sys.stderr)

    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = handle_mcp_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "success": False,
                "error": f"Invalid JSON: {str(e)}"
            }), flush=True)
        except Exception as e:
            print(json.dumps({
                "success": False,
                "error": str(e)
            }), flush=True)


if __name__ == "__main__":
    main()
