#!/usr/bin/env python3
"""
Protocol Risk Scorer
Evaluates DeFi protocol safety using TVL data from DeFiLlama,
audit history, and exploit records.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import urllib.request
import urllib.error
import re

DEFILLAMA_API = "https://api.llama.fi"
GOPLUS_API = "https://api.gopluslabs.io/api/v1"

CHAIN_IDS = {
    "ethereum": "1",
    "eth": "1",
    "bsc": "56",
    "bnb": "56",
    "polygon": "137",
    "matic": "137",
    "arbitrum": "42161",
    "arb": "42161",
    "base": "8453",
    "optimism": "10",
    "op": "10",
    "avalanche": "43114",
    "avax": "43114",
}

SUPPORTED_CHAINS = sorted(set(CHAIN_IDS.keys()))

# Known audited protocols and their audit firms
KNOWN_AUDITED = {
    "aave": ["Trail of Bits", "OpenZeppelin", "SigmaPrime", "Certora"],
    "uniswap": ["Trail of Bits", "ABDK"],
    "compound": ["Trail of Bits", "OpenZeppelin"],
    "makerdao": ["Trail of Bits", "Runtime Verification"],
    "lido": ["Quantstamp", "MixBytes", "Statemind"],
    "curve-dex": ["Trail of Bits", "Quantstamp"],
    "convex-finance": ["MixBytes"],
    "rocket-pool": ["Sigma Prime", "Consensys Diligence"],
    "frax": ["Trail of Bits"],
    "instadapp": ["OpenZeppelin"],
    "yearn-finance": ["Trail of Bits", "MixBytes"],
    "balancer-v2": ["Trail of Bits", "OpenZeppelin"],
    "sushi": ["Quantstamp", "Peckshield"],
    "pancakeswap": ["Peckshield", "SlowMist"],
    "gmx": ["ABDK", "Guardian Audits"],
    "dydx": ["Peckshield"],
    "1inch-network": ["OpenZeppelin", "Chainsulting"],
    "stargate": ["Quantstamp", "Zellic"],
    "eigenlayer": ["Sigma Prime", "Consensys Diligence"],
    "pendle": ["Ackee Blockchain", "Dingbats"],
    "morpho": ["Spearbit"],
    "euler": ["Sherlock", "Zellic"],
}

# Known hacks/exploits
KNOWN_EXPLOITS = {
    "euler": [{"date": "2023-03-13", "loss": "$197M", "type": "Flash loan attack", "recovered": True}],
    "curve-dex": [{"date": "2023-07-30", "loss": "$73.5M", "type": "Vyper reentrancy", "recovered": "Partial"}],
    "balancer-v2": [{"date": "2023-08-22", "loss": "$2.1M", "type": "Rate provider vulnerability", "recovered": False}],
    "harvest-finance": [{"date": "2020-10-26", "loss": "$34M", "type": "Flash loan manipulation", "recovered": False}],
    "beanstalk": [{"date": "2022-04-17", "loss": "$182M", "type": "Governance exploit", "recovered": False}],
    "ronin": [{"date": "2022-03-23", "loss": "$625M", "type": "Validator compromise", "recovered": "Partial"}],
    "wormhole": [{"date": "2022-02-02", "loss": "$326M", "type": "Signature verification bypass", "recovered": True}],
    "nomad": [{"date": "2022-08-01", "loss": "$190M", "type": "Message verification flaw", "recovered": "Partial"}],
    "mango-markets": [{"date": "2022-10-11", "loss": "$114M", "type": "Oracle manipulation", "recovered": "Partial"}],
}


def fetch_json(url: str, timeout: int = 20) -> dict:
    """Fetch JSON data from a URL with error handling."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "DeFiSafetyShield/1.0",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise ConnectionError(
                "Rate limit exceeded. Please wait 1-2 minutes before retrying."
            )
        if e.code == 404:
            return None
        raise ConnectionError(f"API error (HTTP {e.code})")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Connection failed: {e.reason}")


def normalize_slug(protocol: str) -> str:
    """Normalize a protocol name to DeFiLlama slug format."""
    return protocol.strip().lower().replace(" ", "-")


def find_protocol(query: str) -> dict:
    """Find a protocol by name or slug from DeFiLlama."""
    query_lower = query.strip().lower()

    # Try direct slug match first
    slug = normalize_slug(query)
    data = fetch_json(f"{DEFILLAMA_API}/protocol/{slug}")
    if data and data.get("name"):
        return data

    # If direct match fails, search through all protocols
    all_protocols = fetch_json(f"{DEFILLAMA_API}/protocols")
    if not all_protocols or not isinstance(all_protocols, list):
        raise ConnectionError("Could not fetch protocol list from DeFiLlama.")

    # Try exact name match
    for p in all_protocols:
        if p.get("name", "").lower() == query_lower or p.get("slug", "").lower() == query_lower:
            # Fetch full data
            full = fetch_json(f"{DEFILLAMA_API}/protocol/{p['slug']}")
            return full if full else p

    # Try partial match
    matches = []
    for p in all_protocols:
        name = p.get("name", "").lower()
        slug_val = p.get("slug", "").lower()
        if query_lower in name or query_lower in slug_val:
            matches.append(p)

    if len(matches) == 1:
        full = fetch_json(f"{DEFILLAMA_API}/protocol/{matches[0]['slug']}")
        return full if full else matches[0]
    elif len(matches) > 1:
        # Return best match (highest TVL)
        best = max(matches, key=lambda x: float(x.get("tvl", 0) or 0))
        full = fetch_json(f"{DEFILLAMA_API}/protocol/{best['slug']}")
        return full if full else best

    raise ValueError(
        f"Protocol '{query}' not found on DeFiLlama. "
        "Check the protocol name or try its DeFiLlama slug."
    )


def analyze_tvl(protocol_data: dict) -> dict:
    """Analyze TVL trends for risk indicators."""
    current_tvl = float(protocol_data.get("tvl") or protocol_data.get("currentChainTvls", {}).get("total", 0) or 0)

    tvl_history = protocol_data.get("tvl") if isinstance(protocol_data.get("tvl"), list) else []
    # DeFiLlama returns tvl as a list of {date, totalLiquidityUSD} for /protocol/{slug}
    if not tvl_history:
        chain_tvls = protocol_data.get("chainTvls", {})
        for chain_data in chain_tvls.values():
            if isinstance(chain_data, dict) and "tvl" in chain_data:
                tvl_history = chain_data["tvl"]
                break

    analysis = {
        "current_tvl": current_tvl,
        "current_tvl_formatted": format_usd(current_tvl),
        "tvl_trend": "unknown",
        "tvl_change_7d": None,
        "tvl_change_30d": None,
        "risk_indicators": [],
    }

    if isinstance(tvl_history, list) and len(tvl_history) >= 2:
        # Get recent TVL values
        recent = tvl_history[-1].get("totalLiquidityUSD", 0) if isinstance(tvl_history[-1], dict) else 0

        # 7-day change
        if len(tvl_history) >= 7:
            week_ago = tvl_history[-7].get("totalLiquidityUSD", 0) if isinstance(tvl_history[-7], dict) else 0
            if week_ago > 0:
                change_7d = ((recent - week_ago) / week_ago) * 100
                analysis["tvl_change_7d"] = round(change_7d, 2)
                if change_7d < -30:
                    analysis["risk_indicators"].append({
                        "severity": "CRITICAL",
                        "indicator": f"TVL dropped {abs(change_7d):.1f}% in 7 days",
                        "detail": "Rapid TVL decline may indicate a security incident, loss of confidence, or exit scam.",
                    })
                elif change_7d < -15:
                    analysis["risk_indicators"].append({
                        "severity": "HIGH",
                        "indicator": f"TVL dropped {abs(change_7d):.1f}% in 7 days",
                        "detail": "Significant TVL outflows detected. Investigate the cause.",
                    })

        # 30-day change
        if len(tvl_history) >= 30:
            month_ago = tvl_history[-30].get("totalLiquidityUSD", 0) if isinstance(tvl_history[-30], dict) else 0
            if month_ago > 0:
                change_30d = ((recent - month_ago) / month_ago) * 100
                analysis["tvl_change_30d"] = round(change_30d, 2)
                if change_30d < -50:
                    analysis["risk_indicators"].append({
                        "severity": "CRITICAL",
                        "indicator": f"TVL dropped {abs(change_30d):.1f}% in 30 days",
                        "detail": "Massive TVL exodus over the past month. Protocol may be dying or compromised.",
                    })

        # Determine trend
        if analysis.get("tvl_change_7d") is not None:
            if analysis["tvl_change_7d"] > 5:
                analysis["tvl_trend"] = "growing"
            elif analysis["tvl_change_7d"] < -5:
                analysis["tvl_trend"] = "declining"
            else:
                analysis["tvl_trend"] = "stable"

    # TVL size risk
    if current_tvl < 100_000:
        analysis["risk_indicators"].append({
            "severity": "HIGH",
            "indicator": f"Very low TVL: {format_usd(current_tvl)}",
            "detail": "Extremely low TVL suggests the protocol is untested, abandoned, or a scam.",
        })
    elif current_tvl < 1_000_000:
        analysis["risk_indicators"].append({
            "severity": "MEDIUM",
            "indicator": f"Low TVL: {format_usd(current_tvl)}",
            "detail": "Low TVL means less battle-testing and potentially higher risk.",
        })

    return analysis


def format_usd(value: float) -> str:
    """Format USD value with appropriate suffix."""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.2f}K"
    else:
        return f"${value:.2f}"


def get_audit_info(slug: str) -> dict:
    """Get audit information for a protocol."""
    slug_lower = slug.lower()
    auditors = KNOWN_AUDITED.get(slug_lower, [])
    return {
        "has_known_audits": len(auditors) > 0,
        "auditors": auditors,
        "audit_count": len(auditors),
    }


def get_exploit_history(slug: str) -> dict:
    """Get known exploit history for a protocol."""
    slug_lower = slug.lower()
    exploits = KNOWN_EXPLOITS.get(slug_lower, [])
    return {
        "has_known_exploits": len(exploits) > 0,
        "exploits": exploits,
        "exploit_count": len(exploits),
    }


def score_protocol(protocol: str, chain: str = "ethereum") -> dict:
    """Score a DeFi protocol's risk level."""
    # Find protocol data
    protocol_data = find_protocol(protocol)

    name = protocol_data.get("name", protocol)
    slug = protocol_data.get("slug", normalize_slug(protocol))
    category = protocol_data.get("category", "Unknown")
    chains = protocol_data.get("chains", [])
    url = protocol_data.get("url", "")

    # Analyze TVL
    tvl_analysis = analyze_tvl(protocol_data)

    # Get audit info
    audit_info = get_audit_info(slug)

    # Get exploit history
    exploit_info = get_exploit_history(slug)

    # Calculate risk score
    score = 0
    factors = []

    # TVL-based scoring
    current_tvl = tvl_analysis.get("current_tvl", 0)
    if current_tvl < 100_000:
        score += 3
        factors.append({
            "factor": "Very low TVL",
            "impact": "+3",
            "detail": f"TVL is only {tvl_analysis['current_tvl_formatted']}",
        })
    elif current_tvl < 1_000_000:
        score += 2
        factors.append({
            "factor": "Low TVL",
            "impact": "+2",
            "detail": f"TVL is {tvl_analysis['current_tvl_formatted']}",
        })
    elif current_tvl < 10_000_000:
        score += 1
        factors.append({
            "factor": "Moderate TVL",
            "impact": "+1",
            "detail": f"TVL is {tvl_analysis['current_tvl_formatted']}",
        })
    else:
        factors.append({
            "factor": "Strong TVL",
            "impact": "0 (positive)",
            "detail": f"TVL is {tvl_analysis['current_tvl_formatted']}",
        })

    # TVL trend scoring
    change_7d = tvl_analysis.get("tvl_change_7d")
    if change_7d is not None:
        if change_7d < -30:
            score += 3
            factors.append({
                "factor": "Severe TVL decline (7d)",
                "impact": "+3",
                "detail": f"TVL dropped {abs(change_7d):.1f}% in the past week",
            })
        elif change_7d < -15:
            score += 2
            factors.append({
                "factor": "Significant TVL decline (7d)",
                "impact": "+2",
                "detail": f"TVL dropped {abs(change_7d):.1f}% in the past week",
            })
        elif change_7d < -5:
            score += 1
            factors.append({
                "factor": "TVL declining (7d)",
                "impact": "+1",
                "detail": f"TVL dropped {abs(change_7d):.1f}% in the past week",
            })

    # Audit scoring
    if not audit_info["has_known_audits"]:
        score += 2
        factors.append({
            "factor": "No known audits",
            "impact": "+2",
            "detail": "No reputable security audits found in our database",
        })
    elif audit_info["audit_count"] >= 3:
        score = max(0, score - 1)
        factors.append({
            "factor": "Multiple audits",
            "impact": "-1 (positive)",
            "detail": f"Audited by {', '.join(audit_info['auditors'][:3])}",
        })
    else:
        factors.append({
            "factor": "Has audits",
            "impact": "0 (positive)",
            "detail": f"Audited by {', '.join(audit_info['auditors'])}",
        })

    # Exploit history scoring
    if exploit_info["has_known_exploits"]:
        recent_exploits = [
            e for e in exploit_info["exploits"]
            if not e.get("recovered")
        ]
        if recent_exploits:
            score += 2
            factors.append({
                "factor": "Previous exploits (unrecovered)",
                "impact": "+2",
                "detail": f"{len(recent_exploits)} exploit(s) with unrecovered funds",
            })
        else:
            score += 1
            factors.append({
                "factor": "Previous exploits (recovered)",
                "impact": "+1",
                "detail": f"{exploit_info['exploit_count']} exploit(s), funds recovered",
            })

    # Chain diversity (more chains = more tested)
    if len(chains) >= 5:
        factors.append({
            "factor": "Multi-chain deployment",
            "impact": "0 (positive)",
            "detail": f"Deployed on {len(chains)} chains: {', '.join(chains[:5])}",
        })
    elif len(chains) == 1:
        score += 1
        factors.append({
            "factor": "Single chain",
            "impact": "+1",
            "detail": f"Only deployed on {chains[0] if chains else 'unknown'}",
        })

    # Cap score
    score = min(score, 10)

    if score >= 8:
        level = "CRITICAL"
    elif score >= 6:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    elif score >= 2:
        level = "LOW"
    else:
        level = "SAFE"

    # Generate summary
    if score >= 8:
        summary = (
            f"CRITICAL RISK: {name} has severe risk indicators including "
            f"{'exploits, ' if exploit_info['has_known_exploits'] else ''}"
            f"{'no audits, ' if not audit_info['has_known_audits'] else ''}"
            f"and {'very low TVL' if current_tvl < 1_000_000 else 'significant concerns'}. "
            "Avoid depositing funds."
        )
    elif score >= 6:
        summary = (
            f"HIGH RISK: {name} has notable concerns. "
            "Review findings carefully before committing significant funds."
        )
    elif score >= 4:
        summary = (
            f"MEDIUM RISK: {name} has some risk factors to consider. "
            "Protocol appears functional but warrants caution."
        )
    elif score >= 2:
        summary = (
            f"LOW RISK: {name} appears generally safe with minor concerns. "
            "Well-established protocol with good fundamentals."
        )
    else:
        summary = (
            f"SAFE: {name} is a well-established protocol with strong TVL, "
            "multiple audits, and no major known issues."
        )

    # Recommendations
    recommendations = []
    if not audit_info["has_known_audits"]:
        recommendations.append(
            "No known audits - consider waiting for the protocol to be audited"
        )
    if exploit_info["has_known_exploits"]:
        recommendations.append(
            "Protocol has been exploited before - review how the team handled the incident"
        )
    if current_tvl < 1_000_000:
        recommendations.append(
            "Low TVL - start with small amounts and monitor closely"
        )
    if change_7d is not None and change_7d < -15:
        recommendations.append(
            "TVL is declining rapidly - investigate the cause before depositing"
        )
    if score <= 3:
        recommendations.append(
            "Protocol appears solid, but always diversify across protocols"
        )
    recommendations.append(
        "Monitor the protocol's official channels for security updates"
    )
    recommendations.append(
        "Never deposit more than you can afford to lose in any single protocol"
    )

    return {
        "success": True,
        "scan_type": "protocol_risk",
        "protocol": {
            "name": name,
            "slug": slug,
            "category": category,
            "url": url,
            "chains": chains,
        },
        "tvl": {
            "current": tvl_analysis["current_tvl_formatted"],
            "current_raw": current_tvl,
            "trend": tvl_analysis["tvl_trend"],
            "change_7d_percent": tvl_analysis.get("tvl_change_7d"),
            "change_30d_percent": tvl_analysis.get("tvl_change_30d"),
        },
        "audits": audit_info,
        "exploits": exploit_info,
        "risk_score": score,
        "risk_level": level,
        "summary": summary,
        "risk_factors": factors,
        "recommendations": recommendations,
    }


def main() -> None:
    """Main entry point. Reads JSON from stdin."""
    try:
        input_data = json.loads(sys.stdin.read())

        protocol = input_data.get("protocol", "")
        chain = input_data.get("chain", "ethereum")

        if not protocol:
            print(json.dumps({
                "error": "Missing required parameter: 'protocol'",
                "usage": {
                    "protocol": "aave (protocol name or DeFiLlama slug)",
                    "chain": "ethereum (optional, default: ethereum)",
                },
                "examples": [
                    {"protocol": "aave"},
                    {"protocol": "uniswap"},
                    {"protocol": "curve-dex"},
                    {"protocol": "gmx"},
                ],
            }))
            sys.exit(1)

        result = score_protocol(protocol, chain)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input. Send valid JSON via stdin."}))
        sys.exit(1)
    except (ValueError, ConnectionError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {type(e).__name__}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
