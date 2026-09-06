#!/usr/bin/env python3
"""
Jupiter Quote Script
Gets swap quotes from Jupiter aggregator
"""

import json
import sys
import urllib.request
import urllib.error
from typing import Dict, Optional

# Note: Jupiter API v6 was deprecated Sept 2025. Use the current API endpoint.
JUPITER_API = "https://api.jup.ag/swap/v1"

# Common token mints
TOKEN_MINTS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "WSOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "MSOL": "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So",
    "JITOSOL": "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn",
    "RAY": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
    "ORCA": "orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE",
    "PYTH": "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3"
}

# Token decimals
TOKEN_DECIMALS = {
    "So11111111111111111111111111111111111111112": 9,
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": 6,
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": 6,
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": 6,
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": 5,
    "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So": 9,
    "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn": 9
}


def resolve_mint(token: str) -> str:
    """Resolve token symbol or mint to mint address"""
    upper = token.upper()
    if upper in TOKEN_MINTS:
        return TOKEN_MINTS[upper]

    # Check if already a mint address
    if len(token) >= 32 and len(token) <= 44:
        return token

    raise ValueError(f"Unknown token: {token}")


def get_decimals(mint: str) -> int:
    """Get decimals for a token mint"""
    return TOKEN_DECIMALS.get(mint, 9)  # Default to 9


def fetch_json(url: str) -> dict:
    """Fetch JSON from URL"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JupiterQuote/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def get_jupiter_quote(input_mint: str, output_mint: str, amount: int, slippage_bps: int = 50) -> Dict:
    """Get swap quote from Jupiter"""
    url = f"{JUPITER_API}/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippageBps={slippage_bps}"

    data = fetch_json(url)

    if not data or "error" in data:
        raise ValueError(data.get("error", "Failed to get quote"))

    return data


def format_quote(quote: dict, input_symbol: str, output_symbol: str) -> Dict:
    """Format quote data for display"""
    input_mint = quote.get("inputMint", "")
    output_mint = quote.get("outputMint", "")

    in_decimals = get_decimals(input_mint)
    out_decimals = get_decimals(output_mint)

    in_amount = int(quote.get("inAmount", 0)) / (10 ** in_decimals)
    out_amount = int(quote.get("outAmount", 0)) / (10 ** out_decimals)
    other_amount_threshold = int(quote.get("otherAmountThreshold", 0)) / (10 ** out_decimals)

    # Calculate price impact
    price_impact_pct = float(quote.get("priceImpactPct", 0)) * 100

    # Get route info
    route_plan = quote.get("routePlan", [])
    route_summary = []
    for step in route_plan:
        swap_info = step.get("swapInfo", {})
        amm_label = swap_info.get("label", "Unknown")
        route_summary.append(amm_label)

    return {
        "success": True,
        "quote": {
            "input": {
                "mint": input_mint,
                "symbol": input_symbol,
                "amount": round(in_amount, 9)
            },
            "output": {
                "mint": output_mint,
                "symbol": output_symbol,
                "amount": round(out_amount, 9),
                "minimum_received": round(other_amount_threshold, 9)
            },
            "exchange_rate": round(out_amount / in_amount, 6) if in_amount > 0 else 0,
            "price_impact_pct": round(price_impact_pct, 4),
            "slippage_bps": quote.get("slippageBps", 50)
        },
        "route": {
            "steps": len(route_plan),
            "path": " → ".join(route_summary) if route_summary else "Direct",
            "dexes_used": route_summary
        },
        "fees": {
            "platform_fee_bps": quote.get("platformFee", {}).get("feeBps", 0),
            "estimated_fee_sol": 0.000005 * len(route_plan)  # Approximate
        },
        "warnings": get_quote_warnings(price_impact_pct, in_amount, input_symbol)
    }


def get_quote_warnings(price_impact: float, amount: float, symbol: str) -> list:
    """Generate warnings based on quote"""
    warnings = []

    if price_impact > 1:
        warnings.append(f"High price impact: {price_impact:.2f}%. Consider smaller trade size.")
    if price_impact > 5:
        warnings.append("VERY HIGH price impact. Strongly recommend splitting order.")

    if symbol in ["SOL", "WSOL"] and amount > 1000:
        warnings.append("Large SOL trade. Consider using Jito for MEV protection.")

    return warnings


def get_swap_quote(input_token: str, output_token: str, amount: float, slippage_bps: int = 50) -> Dict:
    """Get formatted swap quote"""
    # Resolve mints
    input_mint = resolve_mint(input_token)
    output_mint = resolve_mint(output_token)

    # Get decimals
    in_decimals = get_decimals(input_mint)

    # Convert amount to raw units
    amount_raw = int(amount * (10 ** in_decimals))

    # Get quote
    quote = get_jupiter_quote(input_mint, output_mint, amount_raw, slippage_bps)

    # Format response
    return format_quote(quote, input_token.upper(), output_token.upper())


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        input_token = input_data.get("input_mint") or input_data.get("input_token", "SOL")
        output_token = input_data.get("output_mint") or input_data.get("output_token", "USDC")
        amount = input_data.get("amount")
        slippage_bps = int(input_data.get("slippage_bps", 50))

        if not amount:
            print(json.dumps({"error": "Missing required parameter: amount"}))
            sys.exit(1)

        # Handle if amount is already in raw units (large number)
        amount_float = float(amount)
        if amount_float > 1e9:
            # Assume it's already in raw units, convert based on SOL decimals
            amount_float = amount_float / 1e9

        result = get_swap_quote(input_token, output_token, amount_float, slippage_bps)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
