#!/usr/bin/env python3
"""Detect arbitrage opportunities across DEXes using real price data"""
import json
import argparse
import sys
import urllib.request
from datetime import datetime


def format_success(data):
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error, details=None):
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def fetch_coingecko_price(token_id):
    """Fetch real token price from CoinGecko API."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            if token_id in data and "usd" in data[token_id]:
                return data[token_id]["usd"]
            return None
    except Exception as e:
        return None


def get_token_id(token_symbol):
    """Map token symbols to CoinGecko IDs."""
    mapping = {
        "WETH": "ethereum",
        "ETH": "ethereum",
        "USDC": "usd-coin",
        "USDT": "tether",
        "DAI": "dai",
        "WBTC": "wrapped-bitcoin",
        "BTC": "bitcoin",
        "BNB": "binancecoin",
        "UNI": "uniswap",
        "AAVE": "aave",
    }
    return mapping.get(token_symbol.upper())


def detect_arbitrage(params):
    """Detect arbitrage opportunities with real price data."""
    token_pair = params.get("token_pair")
    dexes = params.get("dexes")
    prices = params.get("prices")
    min_profit_percentage = params.get("min_profit_percentage", 0.5)
    use_live = params.get("use_live_prices", False)
    
    if not token_pair or not isinstance(token_pair, list) or len(token_pair) != 2:
        raise ValueError("token_pair must be array of 2 tokens")
    
    if not dexes or not isinstance(dexes, list) or len(dexes) == 0:
        raise ValueError("dexes must be non-empty array")
    
    # Use live prices if enabled, otherwise use provided prices
    if use_live:
        prices = {}
        base_price = None
        for token in token_pair:
            token_id = get_token_id(token)
            if token_id:
                price = fetch_coingecko_price(token_id)
                if price:
                    if base_price is None:
                        base_price = price
                    prices[token_id] = price
        
        if not prices or len(prices) < 2:
            raise ValueError("Could not fetch live prices. Provide prices parameter.")
    
    if not prices or not isinstance(prices, dict):
        raise ValueError("prices must be object with DEX prices")
    
    # Validate all DEXes have prices
    for dex in dexes:
        if dex not in prices:
            raise ValueError(f"Missing price for DEX: {dex}")
    
    if not isinstance(min_profit_percentage, (int, float)) or min_profit_percentage < 0:
        raise ValueError("min_profit_percentage must be non-negative number")
    
    # Find arbitrage opportunities
    opportunities = []
    
    for i, buy_dex in enumerate(dexes):
        for sell_dex in dexes[i+1:]:
            buy_price = float(prices[buy_dex])
            sell_price = float(prices[sell_dex])
            
            profit_pct = ((sell_price - buy_price) / buy_price) * 100
            
            if abs(profit_pct) >= min_profit_percentage:
                opportunities.append({
                    "buy_dex": buy_dex if profit_pct > 0 else sell_dex,
                    "sell_dex": sell_dex if profit_pct > 0 else buy_dex,
                    "buy_price": round(buy_price if profit_pct > 0 else sell_price, 8),
                    "sell_price": round(sell_price if profit_pct > 0 else buy_price, 8),
                    "profit_percentage": round(abs(profit_pct), 4),
                    "spread_basis_points": round(abs(profit_pct) * 100, 2)
                })
    
    result = {
        "token_pair": token_pair,
        "dexes_scanned": dexes,
        "min_profit_percentage": min_profit_percentage,
        "opportunities_found": len(opportunities),
        "opportunities": sorted(opportunities, key=lambda x: x["profit_percentage"], reverse=True),
        "price_source": "live" if use_live else "provided",
        "scan_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Detect arbitrage opportunities across DEXes')
    parser.add_argument('--params', type=str, required=True, help='JSON parameters with token_pair, dexes, and prices')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
        result = detect_arbitrage(params)
        print(format_success(result))
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
