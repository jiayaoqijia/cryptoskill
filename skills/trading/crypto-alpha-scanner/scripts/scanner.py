#!/usr/bin/env python3
"""
MoltAlpha Scanner v2 - Simplified & Reliable
Only uses free APIs that consistently work:
- CoinGecko (prices, trending)
- Alternative.me (Fear/Greed)
- Polymarket Gamma API (markets)
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

def fetch_json(url, timeout=10):
    """Fetch JSON from URL with error handling"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'MoltAlpha/2.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_crypto_prices():
    """Get BTC, ETH, SOL prices from CoinGecko"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
    data = fetch_json(url)
    if "error" in data:
        return None
    return {
        "BTC": {"price": data.get("bitcoin", {}).get("usd"), "change": data.get("bitcoin", {}).get("usd_24h_change")},
        "ETH": {"price": data.get("ethereum", {}).get("usd"), "change": data.get("ethereum", {}).get("usd_24h_change")},
        "SOL": {"price": data.get("solana", {}).get("usd"), "change": data.get("solana", {}).get("usd_24h_change")}
    }

def get_fear_greed():
    """Get Fear & Greed Index"""
    url = "https://api.alternative.me/fng/?limit=1"
    data = fetch_json(url)
    if "error" in data or "data" not in data:
        return None
    fg = data["data"][0]
    return {"value": int(fg["value"]), "classification": fg["value_classification"]}

def get_trending_coins():
    """Get trending coins from CoinGecko"""
    url = "https://api.coingecko.com/api/v3/search/trending"
    data = fetch_json(url)
    if "error" in data or "coins" not in data:
        return None
    return [coin["item"]["name"] for coin in data["coins"][:5]]

def get_polymarket_hot():
    """Get top Polymarket markets by volume"""
    url = "https://gamma-api.polymarket.com/markets?closed=false&limit=5&order=volume24hr&ascending=false"
    data = fetch_json(url)
    if "error" in data or not isinstance(data, list):
        return None
    markets = []
    for m in data[:3]:
        markets.append({
            "question": m.get("question", "")[:60],
            "volume": f"${int(float(m.get('volume24hr', 0))):,}"
        })
    return markets

def format_report():
    """Generate the alpha report"""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    lines = [f"🤖 Alpha Report | {now}"]
    
    # Prices
    prices = get_crypto_prices()
    if prices:
        lines.append("\n📊 Market Pulse")
        for symbol, data in prices.items():
            if data["price"]:
                change = data["change"] or 0
                emoji = "🟢" if change > 0 else "🔴"
                lines.append(f"{emoji} {symbol}: ${data['price']:,.0f} ({change:+.1f}%)")
    
    # Fear/Greed
    fg = get_fear_greed()
    if fg:
        emoji = "😱" if fg["value"] < 25 else "😰" if fg["value"] < 45 else "😐" if fg["value"] < 55 else "😀" if fg["value"] < 75 else "🤑"
        lines.append(f"{emoji} Fear/Greed: {fg['value']} ({fg['classification']})")
    
    # Trending
    trending = get_trending_coins()
    if trending:
        lines.append(f"\n🔥 Trending: {', '.join(trending)}")
    
    # Polymarket
    poly = get_polymarket_hot()
    if poly:
        lines.append("\n🎯 Polymarket Hot")
        for m in poly:
            lines.append(f"• {m['question']}... ({m['volume']})")
    
    # Insight
    if fg and fg["value"] < 20:
        lines.append("\n💡 Extreme fear = historically strong buy zone. Watch for reversal signals.")
    elif fg and fg["value"] > 80:
        lines.append("\n💡 Extreme greed = caution advised. Consider taking profits.")
    
    lines.append("\n— Nix 🔥")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(format_report())
