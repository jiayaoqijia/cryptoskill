#!/usr/bin/env python3

import json
import argparse
import sys
import re
from datetime import datetime
from typing import Dict, Any, List


# All available skills across tracks
SKILL_CATALOG = {
    "ai-productivity": [
        {"name": "api-webhook-signer", "track": "ai-productivity", "keywords": ["webhook", "signing", "security", "hmac"]},
        {"name": "db-sql-runner", "track": "ai-productivity", "keywords": ["database", "sql", "query", "execution"]},
        {"name": "email-ses-sender", "track": "ai-productivity", "keywords": ["email", "sending", "ses", "notifications"]},
        {"name": "logfile-alerts", "track": "ai-productivity", "keywords": ["logging", "alerts", "monitoring", "files"]},
        {"name": "messaging-slack-notify", "track": "ai-productivity", "keywords": ["slack", "messaging", "notifications", "chat"]}
    ],
    "enterprise-skills": [
        {"name": "api-contract-diff", "track": "enterprise-skills", "keywords": ["api", "contract", "diff", "validation"]},
        {"name": "code-review-basics", "track": "enterprise-skills", "keywords": ["code review", "quality", "standards"]},
        {"name": "doc-changelog-writer", "track": "enterprise-skills", "keywords": ["documentation", "changelog", "versioning"]},
        {"name": "license-audit", "track": "enterprise-skills", "keywords": ["license", "audit", "compliance", "dependencies"]},
        {"name": "security-deps-audit", "track": "enterprise-skills", "keywords": ["security", "audit", "vulnerabilities", "dependencies"]}
    ],
    "web3": [
        {"name": "erc20-allowance-manager", "track": "web3-core", "keywords": ["erc20", "token", "allowance", "ethereum"]},
        {"name": "nft-metadata-pinner", "track": "web3-core", "keywords": ["nft", "metadata", "ipfs", "pinning"]},
        {"name": "wallet-multisend", "track": "web3-core", "keywords": ["wallet", "multisend", "batch", "transactions"]},
        {"name": "dex-arb-detector", "track": "web3-data", "keywords": ["dex", "arbitrage", "trading", "opportunities"]},
        {"name": "whale-tracker", "track": "web3-data", "keywords": ["whale", "tracking", "large transactions", "monitoring"]}
    ]
}


def format_success(data):
    """Format successful JSON response."""
    return json.dumps({"ok": True, "data": data})


def format_error(error):
    """Format error JSON response."""
    return json.dumps({"ok": False, "error": error})


def calculate_relevance_score(query, skill):
    """Calculate relevance score for skill against query."""
    query_lower = query.lower()
    score = 0
    
    # Exact name match (+50)
    if query_lower == skill["name"].lower():
        score += 50
    # Name substring match (+30)
    elif query_lower in skill["name"].lower():
        score += 30
    
    # Keyword matches (+10 per match)
    keywords = skill.get("keywords", [])
    for keyword in keywords:
        if keyword.lower() in query_lower:
            score += 10
    
    # Wildcard matching (partial keyword match, +5)
    query_words = query_lower.split()
    for word in query_words:
        if len(word) > 3:  # Only match words > 3 chars to avoid noise
            for keyword in keywords:
                if word in keyword.lower():
                    score += 5
                    break
    
    return score


def route_skill(query, catalog=None):
    """Route query to matching skills."""
    if catalog is None:
        catalog = SKILL_CATALOG
    
    if not query or not query.strip():
        return {"error": "Query cannot be empty", "matches": []}
    
    # Flatten all skills
    all_skills = []
    for track, skills in catalog.items():
        all_skills.extend(skills)
    
    # Score each skill
    scored_skills = []
    for skill in all_skills:
        score = calculate_relevance_score(query, skill)
        if score > 0:
            scored_skills.append({
                "name": skill["name"],
                "track": skill["track"],
                "relevance_score": score,
                "keywords_matched": [k for k in skill["keywords"] if k.lower() in query.lower()]
            })
    
    # Sort by relevance score desc
    scored_skills.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Get top 5 matches
    top_matches = scored_skills[:5]
    
    return {
        "query": query,
        "matches_found": len(top_matches),
        "total_skills_in_catalog": len(all_skills),
        "matches": top_matches,
        "routing_status": "found" if top_matches else "no_matches"
    }


def execute_routing(params):
    """Execute skill routing with parameters."""
    query = params.get("query", "")
    
    if not query:
        return format_error("query parameter is required")
    
    result = route_skill(query)
    return format_success(result)


def demo_routing():
    """Run demo routing examples."""
    demo_queries = [
        "webhook signing",
        "email notifications",
        "security audit",
        "nft tokens",
        "transaction tracking"
    ]
    
    routing_results = []
    for query in demo_queries:
        result = route_skill(query)
        routing_results.append({
            "query": query,
            "top_match": result["matches"][0]["name"] if result["matches"] else None,
            "matches_count": result["matches_found"],
            "relevance_score_of_top": result["matches"][0]["relevance_score"] if result["matches"] else 0
        })
    
    demo_data = {
        "demo": True,
        "timestamp": datetime.now().isoformat(),
        "routing_demonstration": {
            "catalog_skills": len([s for skills in SKILL_CATALOG.values() for s in skills]),
            "catalog_tracks": list(SKILL_CATALOG.keys()),
            "sample_queries": len(demo_queries),
            "routing_results": routing_results,
            "routing_success_rate": (sum(1 for r in routing_results if r["matches_count"] > 0) / len(routing_results)) * 100
        },
        "detailed_results": [route_skill(q) for q in demo_queries]
    }
    
    return format_success(demo_data)


def main():
    parser = argparse.ArgumentParser(description="Route queries to appropriate skills")
    parser.add_argument("--demo", action="store_true", help="Run demo routing")
    parser.add_argument("--params", type=str, help="JSON parameters with query")
    parser.add_argument("--query", type=str, help="Query string to route")
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            print(demo_routing())
        elif args.params:
            params = json.loads(args.params)
            print(execute_routing(params))
        elif args.query:
            print(execute_routing({"query": args.query}))
        else:
            print(demo_routing())
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
