#!/usr/bin/env python3
"""
Bridge Routes Script
Finds optimal bridging routes including multi-hop options
"""

import json
import sys
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Chain connectivity graph
BRIDGE_GRAPH = {
    "ethereum": {
        "polygon": ["stargate", "wormhole", "across", "hop", "native"],
        "arbitrum": ["stargate", "wormhole", "across", "hop", "native"],
        "optimism": ["stargate", "wormhole", "across", "hop", "native"],
        "base": ["stargate", "wormhole", "across", "native"],
        "bsc": ["stargate", "wormhole"],
        "avalanche": ["stargate", "wormhole"],
        "solana": ["wormhole"]
    },
    "polygon": {
        "ethereum": ["stargate", "wormhole", "across", "hop", "native"],
        "arbitrum": ["stargate", "wormhole", "across"],
        "optimism": ["stargate", "wormhole"],
        "base": ["stargate", "wormhole"],
        "bsc": ["stargate", "wormhole"],
        "avalanche": ["stargate", "wormhole"]
    },
    "arbitrum": {
        "ethereum": ["stargate", "wormhole", "across", "hop", "native"],
        "polygon": ["stargate", "wormhole", "across"],
        "optimism": ["stargate", "wormhole", "across"],
        "base": ["stargate", "wormhole"],
        "bsc": ["stargate", "wormhole"]
    },
    "optimism": {
        "ethereum": ["stargate", "wormhole", "across", "hop", "native"],
        "polygon": ["stargate", "wormhole"],
        "arbitrum": ["stargate", "wormhole", "across"],
        "base": ["stargate", "wormhole"]
    },
    "base": {
        "ethereum": ["stargate", "wormhole", "across", "native"],
        "polygon": ["stargate", "wormhole"],
        "arbitrum": ["stargate", "wormhole"],
        "optimism": ["stargate", "wormhole"]
    },
    "bsc": {
        "ethereum": ["stargate", "wormhole"],
        "polygon": ["stargate", "wormhole"],
        "arbitrum": ["stargate", "wormhole"]
    },
    "avalanche": {
        "ethereum": ["stargate", "wormhole"],
        "polygon": ["stargate", "wormhole"]
    },
    "solana": {
        "ethereum": ["wormhole"]
    }
}

# Bridge cost estimates (fee + gas in USD equivalent)
BRIDGE_COSTS = {
    "stargate": {"cost": 5, "time": 2, "reliability": 0.95},
    "wormhole": {"cost": 10, "time": 15, "reliability": 0.90},
    "across": {"cost": 4, "time": 5, "reliability": 0.92},
    "hop": {"cost": 6, "time": 10, "reliability": 0.88},
    "native": {"cost": 10, "time": 15, "reliability": 0.99}
}


def find_direct_routes(source: str, dest: str) -> List[Dict]:
    """Find direct bridge routes"""
    source = source.lower()
    dest = dest.lower()

    routes = []

    if source in BRIDGE_GRAPH and dest in BRIDGE_GRAPH.get(source, {}):
        bridges = BRIDGE_GRAPH[source][dest]
        for bridge in bridges:
            cost_info = BRIDGE_COSTS.get(bridge, BRIDGE_COSTS["stargate"])
            routes.append({
                "type": "direct",
                "hops": 1,
                "path": [{"from": source, "to": dest, "bridge": bridge}],
                "total_cost_estimate_usd": cost_info["cost"],
                "total_time_minutes": cost_info["time"],
                "reliability": cost_info["reliability"],
                "bridges_used": [bridge]
            })

    return routes


def find_multi_hop_routes(source: str, dest: str, max_hops: int = 2) -> List[Dict]:
    """Find multi-hop bridge routes"""
    source = source.lower()
    dest = dest.lower()

    routes = []

    if source not in BRIDGE_GRAPH:
        return routes

    # Find all chains reachable from source
    for intermediate in BRIDGE_GRAPH.get(source, {}).keys():
        if intermediate == dest:
            continue

        # Check if intermediate can reach destination
        if dest in BRIDGE_GRAPH.get(intermediate, {}):
            # Found a 2-hop route
            first_bridges = BRIDGE_GRAPH[source][intermediate]
            second_bridges = BRIDGE_GRAPH[intermediate][dest]

            # Use best bridge for each hop
            for first_bridge in first_bridges[:1]:  # Best option
                for second_bridge in second_bridges[:1]:  # Best option
                    first_cost = BRIDGE_COSTS.get(first_bridge, BRIDGE_COSTS["stargate"])
                    second_cost = BRIDGE_COSTS.get(second_bridge, BRIDGE_COSTS["stargate"])

                    total_cost = first_cost["cost"] + second_cost["cost"]
                    total_time = first_cost["time"] + second_cost["time"]
                    reliability = first_cost["reliability"] * second_cost["reliability"]

                    routes.append({
                        "type": "multi-hop",
                        "hops": 2,
                        "path": [
                            {"from": source, "to": intermediate, "bridge": first_bridge},
                            {"from": intermediate, "to": dest, "bridge": second_bridge}
                        ],
                        "total_cost_estimate_usd": total_cost,
                        "total_time_minutes": total_time,
                        "reliability": round(reliability, 3),
                        "bridges_used": [first_bridge, second_bridge],
                        "intermediate_chain": intermediate
                    })

    return routes


def find_optimal_routes(source: str, dest: str, token: str, amount: float, optimize_for: str = "cost") -> Dict:
    """Find optimal bridging routes"""
    source = source.lower()
    dest = dest.lower()

    # Find all routes
    direct_routes = find_direct_routes(source, dest)
    multi_hop_routes = find_multi_hop_routes(source, dest)

    all_routes = direct_routes + multi_hop_routes

    if not all_routes:
        return {
            "success": False,
            "error": f"No routes found from {source} to {dest}",
            "suggestion": "Try using Wormhole through Ethereum as an intermediate"
        }

    # Sort routes based on optimization criteria
    if optimize_for == "cost":
        all_routes.sort(key=lambda x: x["total_cost_estimate_usd"])
    elif optimize_for == "time":
        all_routes.sort(key=lambda x: x["total_time_minutes"])
    elif optimize_for == "reliability":
        all_routes.sort(key=lambda x: x["reliability"], reverse=True)

    # Calculate estimated receive amounts
    for route in all_routes:
        # Simple fee estimation based on cost
        fee_pct = route["total_cost_estimate_usd"] / (amount if token.upper() in ["USDC", "USDT", "DAI"] else amount * 2500)
        route["estimated_receive"] = round(amount * (1 - min(fee_pct, 0.05)), 6)

    return {
        "success": True,
        "timestamp": datetime.utcnow().isoformat(),
        "request": {
            "source": source,
            "destination": dest,
            "token": token,
            "amount": amount,
            "optimize_for": optimize_for
        },
        "routes_found": len(all_routes),
        "recommended_route": all_routes[0] if all_routes else None,
        "all_routes": all_routes[:5],  # Top 5 routes
        "analysis": {
            "direct_routes_available": len(direct_routes),
            "multi_hop_routes_available": len(multi_hop_routes),
            "fastest_route": min(all_routes, key=lambda x: x["total_time_minutes"]) if all_routes else None,
            "cheapest_route": min(all_routes, key=lambda x: x["total_cost_estimate_usd"]) if all_routes else None,
            "most_reliable_route": max(all_routes, key=lambda x: x["reliability"]) if all_routes else None
        }
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        source_chain = input_data.get("source_chain", "ethereum")
        dest_chain = input_data.get("dest_chain", "arbitrum")
        token = input_data.get("token", "USDC")
        amount = float(input_data.get("amount", 1000))
        optimize_for = input_data.get("optimize_for", "cost")

        result = find_optimal_routes(source_chain, dest_chain, token, amount, optimize_for)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
