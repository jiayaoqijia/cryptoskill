#!/usr/bin/env python3
"""
Crypto Price Query Tool
使用 CoinGecko API 查询加密货币价格
API 文档: https://www.coingecko.com/api/documentation
"""

import sys
import json
import urllib.request
import urllib.error
from urllib.parse import quote

API_BASE = "https://api.coingecko.com/api/v3"

def fetch_json(url, timeout=10):
    """获取 JSON 数据"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (OpenClaw crypto-price skill)"
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return {"error": "API 请求过于频繁，请稍后再试"}
        return {"error": f"HTTP 错误: {e.code}"}
    except Exception as e:
        return {"error": f"请求失败: {str(e)}"}

def search_coins(query):
    """搜索加密货币"""
    url = f"{API_BASE}/search?query={quote(query)}"
    return fetch_json(url)

def get_simple_price(coin_id, currency="usd"):
    """获取简单价格"""
    url = f"{API_BASE}/simple/price?ids={coin_id}&vs_currencies={currency}&include_24hr_change=true&include_last_updated_at=true"
    return fetch_json(url)

def get_top_coins(limit=10, currency="usd"):
    """获取市值排名前列的加密货币"""
    url = f"{API_BASE}/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={limit}&page=1&sparkline=false&price_change_percentage=24h"
    return fetch_json(url)

def format_price(price, currency="usd"):
    """格式化价格"""
    if price is None:
        return "N/A"
    symbol = {"usd": "$", "cny": "¥", "eur": "€", "jpy": "¥", "gbp": "£", "krw": "₩"}.get(currency, "$")
    if price >= 1000:
        return f"{symbol}{price:,.2f}"
    elif price >= 1:
        return f"{symbol}{price:,.4f}"
    else:
        return f"{symbol}{price:.8f}"

def format_percent(value):
    """格式化百分比"""
    if value is None:
        return "N/A"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"

def main():
    if len(sys.argv) < 2:
        print("用法: crypto-price <command> [args]")
        print("")
        print("命令:")
        print("  crypto-price search <关键词>     搜索加密货币")
        print("  crypto-price get <coin_id> [货币] 获取指定币种价格")
        print("  crypto-price top [数量] [货币]    查看市值排行")
        print("")
        print("货币代码: usd, cny, eur, jpy, gbp, krw, ...")
        print("")
        print("示例:")
        print("  crypto-price search bitcoin")
        print("  crypto-price get bitcoin cny")
        print("  crypto-price top 10 usd")
        return 1

    command = sys.argv[1]

    if command == "search":
        if len(sys.argv) < 3:
            print("错误: 请提供搜索关键词")
            return 1
        query = sys.argv[2]
        data = search_coins(query)
        
        if "error" in data:
            print(f"错误: {data['error']}")
            return 1
        
        coins = data.get("coins", [])[:10]
        if not coins:
            print(f"未找到与 '{query}' 相关的加密货币")
            return 0
        
        print(f"找到 {len(coins)} 个结果:\n")
        for coin in coins:
            symbol = coin.get("symbol", "N/A").upper()
            name = coin.get("name", "N/A")
            coin_id = coin.get("id", "N/A")
            print(f"  {symbol} - {name}")
            print(f"    ID: {coin_id}")
            print()

    elif command == "get":
        if len(sys.argv) < 3:
            print("错误: 请提供币种 ID")
            return 1
        coin_id = sys.argv[2]
        currency = sys.argv[3] if len(sys.argv) > 3 else "usd"
        
        data = get_simple_price(coin_id, currency)
        
        if "error" in data:
            print(f"错误: {data['error']}")
            return 1
        
        if coin_id not in data:
            print(f"错误: 未找到币种 '{coin_id}'")
            print("提示: 使用 'crypto-price search <关键词>' 查找正确的 ID")
            return 1
        
        coin_data = data[coin_id]
        price = coin_data.get(currency)
        change_key = f"{currency}_24h_change"
        change = coin_data.get(change_key)
        last_updated = coin_data.get("last_updated_at")
        
        print(f"\n💰 {coin_id.upper()}")
        print(f"价格: {format_price(price, currency)}")
        if change is not None:
            change_str = format_percent(change)
            emoji = "🟢" if change > 0 else "🔴"
            print(f"24h 涨跌: {emoji} {change_str}")
        print()

    elif command == "top":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 10
        currency = sys.argv[3] if len(sys.argv) > 3 else "usd"
        
        if limit > 100:
            limit = 100
        
        coins = get_top_coins(limit, currency)
        
        if isinstance(coins, dict) and "error" in coins:
            print(f"错误: {coins['error']}")
            return 1
        
        if not coins:
            print("获取数据失败")
            return 1
        
        currency_upper = currency.upper()
        print(f"\n🏆 市值排行前 {limit} 名 ({currency_upper})\n")
        print(f"{'排名':<4} {'币种':<15} {'价格':<18} {'24h涨跌':<12}")
        print("-" * 55)
        
        for i, coin in enumerate(coins, 1):
            symbol = coin.get("symbol", "N/A").upper()
            name = coin.get("name", "N/A")[:12]
            price = coin.get("current_price")
            change = coin.get("price_change_percentage_24h")
            
            price_str = format_price(price, currency)
            change_str = format_percent(change)
            
            print(f"{i:<4} {symbol} {name:<13} {price_str:<18} {change_str}")
        print()

    else:
        print(f"未知命令: {command}")
        print("使用 'crypto-price' 查看帮助")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
