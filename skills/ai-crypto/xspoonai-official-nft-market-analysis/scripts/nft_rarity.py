#!/usr/bin/env python3
"""
NFT Rarity Calculator Script
Calculates rarity scores based on trait distribution
"""

import json
import sys
import os
import urllib.request
import urllib.error
import math

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
        raise ConnectionError(f"API error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def calculate_trait_rarity(trait_count: int, total_supply: int) -> float:
    """Calculate rarity score for a single trait"""
    if total_supply == 0 or trait_count == 0:
        return 0

    # Rarity percentage
    rarity_pct = trait_count / total_supply

    # Score using log scale (rarer = higher score)
    # Max score of 10 for 0.1% rarity
    score = -math.log10(rarity_pct + 0.001) * 2.5
    return min(max(score, 0), 10)


def calculate_statistical_rarity(traits: list, total_supply: int) -> dict:
    """Calculate statistical rarity based on trait frequencies"""
    if not traits:
        return {"score": 0, "rank": "Unknown", "traits": []}

    total_score = 0
    trait_scores = []

    for trait in traits:
        trait_type = trait.get("trait_type", "Unknown")
        trait_value = trait.get("value", "Unknown")
        trait_count = trait.get("trait_count", total_supply)

        rarity_pct = (trait_count / total_supply * 100) if total_supply > 0 else 100
        score = calculate_trait_rarity(trait_count, total_supply)
        total_score += score

        trait_scores.append({
            "trait_type": trait_type,
            "value": str(trait_value),
            "count": trait_count,
            "rarity_pct": round(rarity_pct, 2),
            "score": round(score, 2)
        })

    # Sort by score (highest first)
    trait_scores.sort(key=lambda x: x["score"], reverse=True)

    # Normalize total score to 100
    num_traits = len(traits)
    max_possible = num_traits * 10
    normalized_score = (total_score / max_possible * 100) if max_possible > 0 else 0

    return {
        "total_score": round(normalized_score, 2),
        "raw_score": round(total_score, 2),
        "num_traits": num_traits,
        "traits": trait_scores,
        "rarity_tier": get_rarity_tier(normalized_score)
    }


def get_rarity_tier(score: float) -> str:
    """Get rarity tier based on score"""
    if score >= 90:
        return "LEGENDARY"
    elif score >= 75:
        return "EPIC"
    elif score >= 50:
        return "RARE"
    elif score >= 25:
        return "UNCOMMON"
    else:
        return "COMMON"


def get_nft_metadata(collection: str, token_id: str, api_key: str = None) -> dict:
    """Fetch NFT metadata from OpenSea"""
    # This is a simplified version - OpenSea API v2 structure
    chain = "ethereum"
    url = f"{OPENSEA_API_V2}/chain/{chain}/contract/{collection}/nfts/{token_id}"

    try:
        data = fetch_json(url, api_key)
        return data.get("nft", {})
    except Exception:
        # Fallback: try as slug
        url = f"{OPENSEA_API_V2}/collections/{collection}"
        collection_data = fetch_json(url, api_key)
        contracts = collection_data.get("contracts", [])
        if contracts:
            contract_addr = contracts[0].get("address", "")
            if contract_addr:
                url = f"{OPENSEA_API_V2}/chain/{chain}/contract/{contract_addr}/nfts/{token_id}"
                data = fetch_json(url, api_key)
                return data.get("nft", {})

    raise ValueError(f"NFT not found: {collection} #{token_id}")


def calculate_rarity(collection: str, token_id: str) -> dict:
    """Calculate rarity for a specific NFT"""
    api_key = os.getenv("OPENSEA_API_KEY")

    # Get NFT metadata
    nft_data = get_nft_metadata(collection, token_id, api_key)

    if not nft_data:
        raise ValueError(f"NFT not found: {collection} #{token_id}")

    # Extract traits
    traits = nft_data.get("traits", [])

    # Get collection total supply (estimate from metadata if not available)
    # In production, this would come from collection stats
    total_supply = 10000  # Default assumption

    # Calculate rarity
    rarity_result = calculate_statistical_rarity(traits, total_supply)

    return {
        "success": True,
        "nft": {
            "collection": collection,
            "token_id": token_id,
            "name": nft_data.get("name", f"#{token_id}"),
            "description": nft_data.get("description", "")[:200] if nft_data.get("description") else "N/A",
            "image_url": nft_data.get("image_url", "N/A"),
            "owner": nft_data.get("owners", [{}])[0].get("address", "N/A") if nft_data.get("owners") else "N/A"
        },
        "rarity": {
            "score": rarity_result["total_score"],
            "tier": rarity_result["rarity_tier"],
            "num_traits": rarity_result["num_traits"],
            "trait_breakdown": rarity_result["traits"][:10]  # Top 10 traits
        },
        "analysis": {
            "rarest_trait": rarity_result["traits"][0] if rarity_result["traits"] else None,
            "most_common_trait": rarity_result["traits"][-1] if rarity_result["traits"] else None,
            "recommendation": get_recommendation(rarity_result["total_score"], rarity_result["rarity_tier"])
        }
    }


def get_recommendation(score: float, tier: str) -> str:
    """Get investment recommendation based on rarity"""
    if tier == "LEGENDARY":
        return "Extremely rare NFT. High collector value. Expect significant premium over floor."
    elif tier == "EPIC":
        return "Very rare traits. Should command premium over floor price. Good long-term hold."
    elif tier == "RARE":
        return "Above average rarity. Moderate premium expected. Solid mid-tier choice."
    elif tier == "UNCOMMON":
        return "Slightly above average. May trade near floor with small premium."
    else:
        return "Common traits. Likely to trade at or near floor price. Consider for floor sweeping."


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        collection = input_data.get("collection")
        token_id = input_data.get("token_id")

        if not collection or not token_id:
            print(json.dumps({"error": "Missing required parameters: collection, token_id"}))
            sys.exit(1)

        result = calculate_rarity(collection, str(token_id))
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
