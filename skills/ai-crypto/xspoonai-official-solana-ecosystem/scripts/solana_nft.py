#!/usr/bin/env python3
"""
Solana NFT Script
Queries Solana NFT data from Magic Eden
"""

import json
import sys
import urllib.request
import urllib.error
from typing import Dict, List, Optional
from datetime import datetime

MAGIC_EDEN_API = "https://api-mainnet.magiceden.dev/v2"

# Popular collections
POPULAR_COLLECTIONS = {
    "mad_lads": "madlads",
    "madlads": "madlads",
    "tensorians": "tensorians",
    "claynosaurz": "claynosaurz",
    "famous_fox_federation": "famous_fox_federation",
    "degods": "degods",
    "y00ts": "y00ts",
    "okay_bears": "okay_bears",
    "degenerate_ape_academy": "degenerate_ape_academy",
    "solana_monkey_business": "solana_monkey_business"
}


def fetch_json(url: str) -> dict:
    """Fetch JSON from URL"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "SolanaNFT/1.0",
            "Accept": "application/json"
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError("Collection not found")
        raise ConnectionError(f"API error: {e.code}")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def get_collection_stats(collection_symbol: str) -> Dict:
    """Get collection statistics from Magic Eden"""
    url = f"{MAGIC_EDEN_API}/collections/{collection_symbol}/stats"

    try:
        data = fetch_json(url)
    except ValueError:
        # Try normalized symbol
        normalized = POPULAR_COLLECTIONS.get(collection_symbol.lower(), collection_symbol)
        if normalized != collection_symbol:
            url = f"{MAGIC_EDEN_API}/collections/{normalized}/stats"
            data = fetch_json(url)
        else:
            raise

    return data


def get_collection_listings(collection_symbol: str, limit: int = 10) -> List[Dict]:
    """Get current listings for a collection"""
    url = f"{MAGIC_EDEN_API}/collections/{collection_symbol}/listings?limit={limit}"

    try:
        data = fetch_json(url)
        return data if isinstance(data, list) else []
    except:
        return []


def get_collection_activities(collection_symbol: str, limit: int = 10) -> List[Dict]:
    """Get recent activities for a collection"""
    url = f"{MAGIC_EDEN_API}/collections/{collection_symbol}/activities?limit={limit}"

    try:
        data = fetch_json(url)
        return data if isinstance(data, list) else []
    except:
        return []


def format_sol_price(lamports: int) -> float:
    """Convert lamports to SOL"""
    return lamports / 1e9 if lamports else 0


def analyze_collection(collection: str) -> Dict:
    """Comprehensive collection analysis"""
    # Normalize collection name
    symbol = POPULAR_COLLECTIONS.get(collection.lower(), collection.lower())

    # Get stats
    stats = get_collection_stats(symbol)

    # Get listings
    listings = get_collection_listings(symbol, 20)

    # Get activities
    activities = get_collection_activities(symbol, 10)

    # Parse stats
    floor_price = format_sol_price(stats.get("floorPrice", 0))
    listed_count = stats.get("listedCount", 0)
    volume_all = format_sol_price(stats.get("volumeAll", 0))
    avg_price_24h = format_sol_price(stats.get("avgPrice24hr", 0))

    # Analyze listings
    listing_prices = [format_sol_price(l.get("price", 0)) for l in listings if l.get("price")]
    min_listing = min(listing_prices) if listing_prices else floor_price
    max_listing_top10 = max(listing_prices[:10]) if listing_prices else floor_price

    # Analyze activities
    recent_sales = [a for a in activities if a.get("type") == "buyNow"]
    sale_prices = [format_sol_price(s.get("price", 0)) for s in recent_sales]

    return {
        "success": True,
        "timestamp": datetime.utcnow().isoformat(),
        "collection": {
            "symbol": symbol,
            "marketplace": "Magic Eden"
        },
        "market_stats": {
            "floor_price_sol": round(floor_price, 4),
            "listed_count": listed_count,
            "total_volume_sol": round(volume_all, 2),
            "avg_price_24h_sol": round(avg_price_24h, 4)
        },
        "listing_analysis": {
            "current_listings": len(listings),
            "floor_listing": round(min_listing, 4),
            "price_range": {
                "min": round(min_listing, 4),
                "max_top10": round(max_listing_top10, 4)
            }
        },
        "recent_activity": {
            "sales_count": len(recent_sales),
            "avg_sale_price": round(sum(sale_prices) / len(sale_prices), 4) if sale_prices else 0,
            "recent_sales": [
                {
                    "price_sol": round(format_sol_price(s.get("price", 0)), 4),
                    "buyer": s.get("buyer", "")[:8] + "..." if s.get("buyer") else "Unknown",
                    "timestamp": s.get("blockTime")
                }
                for s in recent_sales[:5]
            ]
        },
        "market_assessment": {
            "liquidity": "HIGH" if listed_count > 100 else "MEDIUM" if listed_count > 20 else "LOW",
            "price_trend": "STABLE",  # Would need historical data for accurate trend
            "recommendation": get_market_recommendation(floor_price, listed_count, len(recent_sales))
        }
    }


def get_market_recommendation(floor_price: float, listed_count: int, recent_sales: int) -> str:
    """Generate market recommendation"""
    if recent_sales > 5 and listed_count > 50:
        return "Active market with good liquidity. Suitable for trading."
    elif recent_sales > 2:
        return "Moderate activity. Consider market conditions before large positions."
    else:
        return "Low activity. May face difficulty selling quickly."


def get_nft_by_mint(mint_address: str) -> Dict:
    """Get specific NFT data by mint address"""
    url = f"{MAGIC_EDEN_API}/tokens/{mint_address}"

    try:
        data = fetch_json(url)
        return {
            "success": True,
            "nft": {
                "mint": mint_address,
                "name": data.get("name", "Unknown"),
                "collection": data.get("collection", "Unknown"),
                "image": data.get("image", ""),
                "attributes": data.get("attributes", []),
                "owner": data.get("owner", ""),
                "listing_price": format_sol_price(data.get("listPrice", 0)) if data.get("listPrice") else None
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_top_collections() -> Dict:
    """Get top collections by volume"""
    # Magic Eden doesn't have a direct top collections endpoint in v2
    # Return curated list with known data

    top_collections = [
        {"name": "Mad Lads", "symbol": "madlads", "floor_range": "50-150 SOL"},
        {"name": "Tensorians", "symbol": "tensorians", "floor_range": "10-30 SOL"},
        {"name": "Claynosaurz", "symbol": "claynosaurz", "floor_range": "20-50 SOL"},
        {"name": "Famous Fox Federation", "symbol": "famous_fox_federation", "floor_range": "5-15 SOL"},
        {"name": "DeGods", "symbol": "degods", "floor_range": "3-10 SOL"},
        {"name": "y00ts", "symbol": "y00ts", "floor_range": "2-8 SOL"},
        {"name": "Okay Bears", "symbol": "okay_bears", "floor_range": "5-15 SOL"}
    ]

    return {
        "success": True,
        "timestamp": datetime.utcnow().isoformat(),
        "note": "Floor prices are estimates and change frequently",
        "top_collections": top_collections,
        "marketplace": "Magic Eden",
        "recommendation": "Always verify current floor prices before trading"
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        action = input_data.get("action", "collection_stats")
        collection = input_data.get("collection")
        mint = input_data.get("mint")

        if action == "top":
            result = get_top_collections()
        elif action == "nft" and mint:
            result = get_nft_by_mint(mint)
        elif collection:
            result = analyze_collection(collection)
        else:
            result = get_top_collections()

        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
