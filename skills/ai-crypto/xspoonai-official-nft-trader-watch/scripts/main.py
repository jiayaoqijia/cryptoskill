#!/usr/bin/env python3
"""Track NFT trader activity and patterns with real API data"""
import json
import argparse
import sys
import urllib.request
import urllib.error
from datetime import datetime
from collections import defaultdict


# OpenSea API configuration
OPENSEA_API_BASE = "https://api.opensea.io/api/v2"
OPENSEA_API_KEY = "test"  # Can be obtained from OpenSea for free tier

# CoinGecko API for ETH price
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Popular NFT collections
NFT_COLLECTIONS = {
    "bored_ape": "0xBC4CA0EdA7647A8aB7C2061c2E2ad9D2d6d2eEDE",
    "cryptopunks": "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",
    "pudgy_penguins": "0xBd3531dA5DD0A74fb411a9b847beAeC30DC5511B",
    "cool_cats": "0x1A92de1e5EC850f0385d3a010937198afb8b5AAF",
    "art_blocks": "0xa7d8d9ef8D8Ce8992Df33D8b8f37e3a930B5CFfD",
}


def format_success(data):
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error, details=None):
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def fetch_eth_price():
    """Fetch current ETH price from CoinGecko."""
    try:
        url = f"{COINGECKO_API}/simple/price?ids=ethereum&vs_currencies=usd"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get("ethereum", {}).get("usd", 1850)
    except:
        return 1850  # Default fallback price


def fetch_collection_sales(collection_slug):
    """Fetch recent sales from OpenSea API."""
    url = f"{OPENSEA_API_BASE}/events"
    params = {
        "collection_slug": collection_slug,
        "event_type": "sale",
        "limit": 100,
        "occurred_after": int(datetime.utcnow().timestamp()) - 86400  # Last 24h
    }
    
    try:
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        req = urllib.request.Request(
            f"{url}?{query_string}",
            headers={"X-API-KEY": OPENSEA_API_KEY}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("asset_events", [])
    except:
        # Return empty if API fails, skill still works with parameter mode
        return []


def detect_trader_flips(sales_data):
    """Detect flipping activity from sales data."""
    trader_buys = defaultdict(list)
    trader_sells = defaultdict(list)
    
    # Group sales by trader
    for sale in sales_data:
        buyer = sale.get("buyer", {}).get("address", "unknown")
        seller = sale.get("seller", {}).get("address", "unknown")
        price_eth = float(sale.get("payment", {}).get("quantity", 0)) / 1e18
        timestamp = sale.get("created_date", datetime.utcnow().isoformat())
        nft_id = sale.get("asset", {}).get("token_id", "unknown")
        
        # Record buys
        if buyer != "unknown":
            trader_buys[buyer].append({
                "nft_id": nft_id,
                "price_eth": price_eth,
                "timestamp": timestamp,
                "type": "buy"
            })
        
        # Record sells
        if seller != "unknown":
            trader_sells[seller].append({
                "nft_id": nft_id,
                "price_eth": price_eth,
                "timestamp": timestamp,
                "type": "sell"
            })
    
    # Detect flips (same NFT bought and sold)
    flips = []
    for trader, sells in trader_sells.items():
        for sell in sells:
            nft_id = sell["nft_id"]
            # Check if trader also bought this NFT
            if trader in trader_buys:
                for buy in trader_buys[trader]:
                    if buy["nft_id"] == nft_id:
                        profit_eth = sell["price_eth"] - buy["price_eth"]
                        if profit_eth > 0:
                            flips.append({
                                "trader": trader[:10] + "..." + trader[-4:],
                                "nft_id": nft_id,
                                "buy_price_eth": round(buy["price_eth"], 4),
                                "sell_price_eth": round(sell["price_eth"], 4),
                                "profit_eth": round(profit_eth, 4),
                                "profit_pct": round((profit_eth / buy["price_eth"] * 100), 2)
                            })
    
    return flips, trader_buys, trader_sells


def analyze_trader_activity_api(params):
    """Analyze NFT trader activity with real or custom data."""
    network = params.get("network", "ethereum")
    collection = params.get("collection")
    collection_slug = params.get("collection_slug", "")
    min_volume = params.get("min_volume", 5)
    use_api = params.get("use_api", True)
    
    if not collection:
        raise ValueError("collection address or identifier required")
    
    eth_price = fetch_eth_price()
    
    if use_api:
        # Attempt to fetch from OpenSea API
        if not collection_slug:
            # Try to resolve collection slug from known collections
            for key, addr in NFT_COLLECTIONS.items():
                if addr.lower() == collection.lower():
                    collection_slug = key
                    break
        
        if collection_slug:
            sales_data = fetch_collection_sales(collection_slug)
        else:
            sales_data = []
        
        if sales_data:
            # Analyze real API data
            flips, trader_buys, trader_sells = detect_trader_flips(sales_data)
            
            # Calculate trader stats
            traders_data = []
            for trader in set(list(trader_buys.keys()) + list(trader_sells.keys())):
                buys = trader_buys.get(trader, [])
                sells = trader_sells.get(trader, [])
                buy_vol = sum(t["price_eth"] for t in buys)
                sell_vol = sum(t["price_eth"] for t in sells)
                
                if len(buys) + len(sells) >= min_volume:
                    profit = sell_vol - buy_vol
                    traders_data.append({
                        "trader": trader[:10] + "..." + trader[-4:],
                        "buys": len(buys),
                        "sells": len(sells),
                        "buy_volume_eth": round(buy_vol, 4),
                        "sell_volume_eth": round(sell_vol, 4),
                        "profit_eth": round(profit, 4),
                        "profit_usd": round(profit * eth_price, 2)
                    })
            
            # Sort by profit
            traders_data.sort(key=lambda x: x["profit_eth"], reverse=True)
            
            result = {
                "source": "opensea_api",
                "network": network,
                "collection": collection,
                "eth_price": round(eth_price, 2),
                "total_traders": len(traders_data),
                "flips_detected": len(flips),
                "traders": traders_data[:10],
                "top_flips": sorted(flips, key=lambda x: x["profit_eth"], reverse=True)[:5],
                "analysis_timestamp": datetime.utcnow().isoformat() + "Z"
            }
        else:
            # API failed, use parameter mode
            result = analyze_trader_from_params(params, eth_price)
    else:
        # Parameter mode - analyze provided trades
        result = analyze_trader_from_params(params, eth_price)
    
    return result


def analyze_trader_from_params(params, eth_price):
    """Analyze trader data from parameters."""
    collection = params.get("collection")
    trades = params.get("trades", [])
    
    buys = [t for t in trades if t.get("type") == "buy"]
    sells = [t for t in trades if t.get("type") == "sell"]
    
    total_bought_eth = sum(t.get("price_eth", 0) for t in buys)
    total_sold_eth = sum(t.get("price_eth", 0) for t in sells)
    profit_eth = total_sold_eth - total_bought_eth
    
    avg_buy = (total_bought_eth / len(buys)) if buys else 0
    avg_sell = (total_sold_eth / len(sells)) if sells else 0
    
    # Detect flips from parameter data
    flips = []
    buys_by_nft = defaultdict(list)
    sells_by_nft = defaultdict(list)
    
    for trade in trades:
        nft_id = trade.get("nft_id", "")
        if trade.get("type") == "buy":
            buys_by_nft[nft_id].append(trade)
        else:
            sells_by_nft[nft_id].append(trade)
    
    for nft_id, sell_list in sells_by_nft.items():
        if nft_id in buys_by_nft:
            for buy in buys_by_nft[nft_id]:
                for sell in sell_list:
                    profit = sell.get("price_eth", 0) - buy.get("price_eth", 0)
                    if profit > 0:
                        flips.append({
                            "nft_id": nft_id,
                            "buy_price_eth": buy.get("price_eth", 0),
                            "sell_price_eth": sell.get("price_eth", 0),
                            "profit_eth": round(profit, 4),
                            "profit_pct": round((profit / buy.get("price_eth", 1) * 100), 2)
                        })
    
    result = {
        "source": "parameters",
        "collection": collection,
        "eth_price": round(eth_price, 2),
        "total_trades": len(trades),
        "buys": len(buys),
        "sells": len(sells),
        "total_volume_eth": round(total_bought_eth + total_sold_eth, 4),
        "total_volume_usd": round((total_bought_eth + total_sold_eth) * eth_price, 2),
        "profit_eth": round(profit_eth, 4),
        "profit_usd": round(profit_eth * eth_price, 2),
        "avg_buy_price_eth": round(avg_buy, 4),
        "avg_sell_price_eth": round(avg_sell, 4),
        "flips_detected": len(flips),
        "flips": flips,
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Track NFT trader activity')
    parser.add_argument('--params', type=str, required=True, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
        result = analyze_trader_activity_api(params)
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
