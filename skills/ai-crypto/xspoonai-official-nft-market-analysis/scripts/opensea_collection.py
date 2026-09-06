#!/usr/bin/env python3
"""
OpenSea Collection Data Script
Fetches collection data from OpenSea API
"""

import json
import sys
import os
import urllib.request
import urllib.error

OPENSEA_API_V2 = "https://api.opensea.io/api/v2"


def fetch_json(url: str, api_key: str = None) -> dict:
    """Fetch JSON from URL with optional API key"""
    headers = {
        "Accept": "application/json",
        "User-Agent": "NFT-Skill/1.0"
    }

    if api_key:
        headers["X-API-KEY"] = api_key

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise ValueError("Invalid or missing OpenSea API key")
        elif e.code == 404:
            raise ValueError("Collection not found")
        raise ConnectionError(f"API error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def get_collection_stats(collection_slug: str, api_key: str = None) -> dict:
    """Get collection statistics from OpenSea"""
    url = f"{OPENSEA_API_V2}/collections/{collection_slug}/stats"
    data = fetch_json(url, api_key)

    if not data:
        raise ValueError(f"No stats found for collection: {collection_slug}")

    return data


def get_collection_info(collection_slug: str, api_key: str = None) -> dict:
    """Get collection information from OpenSea"""
    url = f"{OPENSEA_API_V2}/collections/{collection_slug}"
    data = fetch_json(url, api_key)

    if not data:
        raise ValueError(f"Collection not found: {collection_slug}")

    return data


def get_collection_data(collection_slug: str, chain: str = "ethereum") -> dict:
    """Get comprehensive collection data"""
    api_key = os.getenv("OPENSEA_API_KEY")

    # Fetch collection info
    try:
        info = get_collection_info(collection_slug, api_key)
    except Exception as e:
        # Try without API key for public data
        info = get_collection_info(collection_slug)

    # Fetch collection stats
    try:
        stats = get_collection_stats(collection_slug, api_key)
    except Exception:
        stats = {}

    # Parse and format data
    total_stats = stats.get("total", {})
    intervals = stats.get("intervals", [])

    # Get 24h stats if available
    day_stats = {}
    for interval in intervals:
        if interval.get("interval") == "one_day":
            day_stats = interval
            break

    return {
        "success": True,
        "collection": {
            "name": info.get("name", collection_slug),
            "slug": collection_slug,
            "description": (info.get("description", "")[:500] + "...") if info.get("description") else "N/A",
            "image_url": info.get("image_url", "N/A"),
            "banner_image_url": info.get("banner_image_url", "N/A"),
            "external_url": info.get("project_url", "N/A"),
            "discord_url": info.get("discord_url", "N/A"),
            "twitter_username": info.get("twitter_username", "N/A"),
            "contracts": info.get("contracts", []),
            "created_date": info.get("created_date", "N/A"),
            "owner": info.get("owner", "N/A"),
            "category": info.get("category", "N/A"),
            "is_safelist_request_status": info.get("safelist_request_status", "N/A"),
            "total_supply": info.get("total_supply", 0)
        },
        "stats": {
            "floor_price": {
                "value": total_stats.get("floor_price", 0),
                "currency": total_stats.get("floor_price_symbol", "ETH")
            },
            "total_volume": total_stats.get("volume", 0),
            "total_sales": total_stats.get("sales", 0),
            "num_owners": total_stats.get("num_owners", 0),
            "average_price": total_stats.get("average_price", 0),
            "market_cap": total_stats.get("market_cap", 0)
        },
        "day_stats": {
            "volume": day_stats.get("volume", 0),
            "volume_change": day_stats.get("volume_change", 0),
            "sales": day_stats.get("sales", 0),
            "sales_change": day_stats.get("sales_change", 0),
            "average_price": day_stats.get("average_price", 0)
        },
        "chain": chain,
        "marketplace": "OpenSea",
        "analysis": {
            "listing_ratio": "N/A",  # Would need additional API call
            "holder_concentration": "N/A",  # Would need on-chain data
            "liquidity_score": calculate_liquidity_score(total_stats, day_stats)
        }
    }


def calculate_liquidity_score(total_stats: dict, day_stats: dict) -> str:
    """Calculate a simple liquidity score based on volume and sales"""
    daily_volume = day_stats.get("volume", 0)
    daily_sales = day_stats.get("sales", 0)

    if daily_sales >= 100 and daily_volume >= 10:
        return "HIGH"
    elif daily_sales >= 20 and daily_volume >= 2:
        return "MEDIUM"
    elif daily_sales >= 5:
        return "LOW"
    else:
        return "VERY LOW"


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        collection = input_data.get("collection")
        chain = input_data.get("chain", "ethereum")

        if not collection:
            print(json.dumps({"error": "Missing required parameter: collection"}))
            sys.exit(1)

        result = get_collection_data(collection, chain)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
