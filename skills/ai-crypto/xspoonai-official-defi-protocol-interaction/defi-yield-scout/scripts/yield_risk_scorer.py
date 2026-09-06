#!/usr/bin/env python3
"""
DeFi Yield Risk Scorer - Quantitatively risk-score DeFi yield opportunities.

Analyzes individual yield opportunities across multiple risk dimensions:
protocol maturity, TVL stability, APY sustainability, impermanent loss exposure,
chain security, and audit history. Uses DeFiLlama data and a curated audit database.

Input (JSON via stdin):
{
    "pool_id": "pool-id-here",       # option 1: direct pool ID lookup
    "protocol": "aave-v3",            # option 2: search by attributes
    "chain": "ethereum",
    "symbol": "USDC"
}

Output (JSON via stdout):
{
    "success": true,
    "risk_score": 1.5,
    "risk_level": "SAFE",
    "risk_breakdown": {...}
}

APIs:
- https://yields.llama.fi/pools (pool data)
- https://api.llama.fi/protocols (protocol metadata)
"""

import json
import sys
import urllib.request
import urllib.error
import time
import math
from typing import Any, Dict, List, Optional, Tuple


# API endpoints
DEFILLAMA_POOLS_URL = "https://yields.llama.fi/pools"
DEFILLAMA_PROTOCOLS_URL = "https://api.llama.fi/protocols"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2.0

# Risk score boundaries
RISK_LEVELS = {
    "SAFE": (0, 1),
    "LOW": (2, 3),
    "MEDIUM": (4, 5),
    "HIGH": (6, 7),
    "CRITICAL": (8, 10),
}

# Risk dimension weights (must sum to 1.0)
RISK_WEIGHTS = {
    "protocol_risk": 0.25,
    "tvl_risk": 0.20,
    "apy_sustainability": 0.25,
    "il_risk": 0.15,
    "chain_risk": 0.15,
}

# Curated audit database for major protocols
AUDITED_PROTOCOLS: Dict[str, Dict] = {
    "aave-v3": {"audits": ["Trail of Bits", "OpenZeppelin"], "score": 9},
    "aave-v2": {"audits": ["Trail of Bits", "OpenZeppelin"], "score": 9},
    "compound-v3": {"audits": ["OpenZeppelin", "ChainSecurity"], "score": 9},
    "compound": {"audits": ["OpenZeppelin", "Trail of Bits"], "score": 9},
    "lido": {"audits": ["Sigma Prime", "Quantstamp"], "score": 9},
    "curve-dex": {"audits": ["Trail of Bits", "Quantstamp"], "score": 8},
    "curve": {"audits": ["Trail of Bits", "Quantstamp"], "score": 8},
    "uniswap-v3": {"audits": ["Trail of Bits"], "score": 9},
    "uniswap-v2": {"audits": ["dapp.org"], "score": 8},
    "maker": {"audits": ["Trail of Bits", "Runtime Verification"], "score": 9},
    "makerdao": {"audits": ["Trail of Bits", "Runtime Verification"], "score": 9},
    "convex-finance": {"audits": ["MixBytes"], "score": 7},
    "yearn-finance": {"audits": ["Trail of Bits", "MixBytes"], "score": 8},
    "morpho": {"audits": ["Spearbit", "Trail of Bits"], "score": 8},
    "rocket-pool": {"audits": ["Sigma Prime", "Consensys Diligence"], "score": 8},
    "frax": {"audits": ["Trail of Bits", "ABDK"], "score": 7},
    "frax-ether": {"audits": ["Trail of Bits", "ABDK"], "score": 7},
    "pendle": {"audits": ["Ackee Blockchain"], "score": 7},
    "eigenlayer": {"audits": ["Sigma Prime"], "score": 7},
    "gmx": {"audits": ["ABDK", "Quantstamp"], "score": 7},
    "balancer-v2": {"audits": ["Trail of Bits", "OpenZeppelin"], "score": 8},
    "balancer": {"audits": ["Trail of Bits", "OpenZeppelin"], "score": 8},
    "pancakeswap": {"audits": ["PeckShield", "SlowMist"], "score": 7},
    "sushiswap": {"audits": ["PeckShield", "Quantstamp"], "score": 7},
    "instadapp": {"audits": ["MixBytes", "Dedaub"], "score": 7},
    "spark": {"audits": ["ChainSecurity"], "score": 8},
    "stargate": {"audits": ["Quantstamp", "Zokyo"], "score": 7},
    "venus": {"audits": ["Certik", "PeckShield"], "score": 7},
    "benqi": {"audits": ["Halborn"], "score": 7},
    "radiant-v2": {"audits": ["PeckShield", "BlockSec"], "score": 6},
    "sky": {"audits": ["Trail of Bits", "Runtime Verification"], "score": 9},
}

# Chain risk scores (lower = safer)
CHAIN_RISK_SCORES: Dict[str, float] = {
    "Ethereum": 1.0,
    "BSC": 3.0,
    "Polygon": 2.5,
    "Arbitrum": 2.0,
    "Base": 2.0,
    "Optimism": 2.0,
    "Avalanche": 2.5,
    "Solana": 2.5,
    "Fantom": 4.0,
    "Gnosis": 3.0,
    "Celo": 3.5,
    "Moonbeam": 4.0,
    "Cronos": 4.0,
    "Metis": 3.5,
    "Linea": 3.0,
    "Scroll": 3.0,
    "zkSync Era": 3.0,
    "Mantle": 3.5,
    "Blast": 3.5,
    "Manta": 3.5,
    "Mode": 4.0,
}

# Default chain risk for unknown chains
DEFAULT_CHAIN_RISK = 5.0

# Chain name normalization
CHAIN_ALIASES: Dict[str, str] = {
    "ethereum": "Ethereum",
    "eth": "Ethereum",
    "bsc": "BSC",
    "binance": "BSC",
    "polygon": "Polygon",
    "matic": "Polygon",
    "arbitrum": "Arbitrum",
    "arb": "Arbitrum",
    "base": "Base",
    "optimism": "Optimism",
    "op": "Optimism",
    "avalanche": "Avalanche",
    "avax": "Avalanche",
    "solana": "Solana",
    "sol": "Solana",
    "fantom": "Fantom",
    "ftm": "Fantom",
    "gnosis": "Gnosis",
}


def _fetch_json(url: str, timeout: int = 25) -> Tuple[Optional[Any], Optional[str]]:
    """Fetch JSON from URL with retry logic and 429 handling.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        Tuple of (data, error_string).
    """
    headers = {
        "User-Agent": "DeFiYieldScout/1.0",
        "Accept": "application/json",
    }

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                return data, None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = RETRY_DELAY_BASE * (2 ** attempt)
                time.sleep(wait_time)
                continue
            return None, f"HTTP {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            return None, f"URL error: {str(e.reason)}"
        except json.JSONDecodeError as e:
            return None, f"JSON decode error: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    return None, "Max retries exceeded (rate limited)"


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _format_tvl(tvl: float) -> str:
    """Format TVL as human-readable string."""
    if tvl >= 1_000_000_000:
        return f"${tvl / 1_000_000_000:.2f}B"
    elif tvl >= 1_000_000:
        return f"${tvl / 1_000_000:.2f}M"
    elif tvl >= 1_000:
        return f"${tvl / 1_000:.2f}K"
    else:
        return f"${tvl:.2f}"


def _normalize_chain(chain: str) -> Optional[str]:
    """Normalize chain name to DeFiLlama format."""
    if not chain:
        return None
    return CHAIN_ALIASES.get(chain.lower(), chain.title())


def _find_pool(pools: List[Dict], params: Dict) -> Optional[Dict]:
    """Find a specific pool from the pools list.

    Args:
        pools: All pools from DeFiLlama.
        params: Search parameters (pool_id, protocol, chain, symbol).

    Returns:
        Matching pool dict or None.
    """
    pool_id = params.get("pool_id")
    if pool_id:
        for pool in pools:
            if pool.get("pool") == pool_id:
                return pool
        return None

    protocol = params.get("protocol", "").lower()
    chain = params.get("chain")
    symbol = params.get("symbol", "").upper()

    candidates = []
    for pool in pools:
        # Protocol match
        if protocol and protocol not in pool.get("project", "").lower():
            continue

        # Chain match
        if chain:
            normalized = _normalize_chain(chain)
            if normalized and pool.get("chain", "").lower() != normalized.lower():
                continue

        # Symbol match
        if symbol and symbol not in pool.get("symbol", "").upper():
            continue

        candidates.append(pool)

    if not candidates:
        return None

    # Return the candidate with the highest TVL (most likely the one the user wants)
    candidates.sort(key=lambda p: _safe_float(p.get("tvlUsd")), reverse=True)
    return candidates[0]


def _score_protocol_risk(pool: Dict, protocol_meta: Optional[Dict]) -> Dict:
    """Score protocol risk based on audit history and maturity.

    Args:
        pool: Pool data.
        protocol_meta: Protocol metadata from DeFiLlama protocols endpoint.

    Returns:
        Dict with score and reason.
    """
    project = pool.get("project", "").lower()

    # Check audit database
    audit_info = None
    for key, info in AUDITED_PROTOCOLS.items():
        if key in project or project in key:
            audit_info = info
            break

    if audit_info:
        audit_score = audit_info["score"]
        auditors = audit_info["audits"]
        # High audit score = low risk
        risk = max(0, 10 - audit_score)
        return {
            "score": round(risk, 1),
            "reason": f"Audited by {', '.join(auditors)} (audit score: {audit_score}/10)",
            "audited": True,
            "auditors": auditors,
            "audit_score": audit_score,
        }

    # Unknown protocol - check if we have metadata
    if protocol_meta:
        # Use TVL as a proxy for maturity
        protocol_tvl = _safe_float(protocol_meta.get("tvl", 0))
        if protocol_tvl > 1_000_000_000:
            return {
                "score": 3.0,
                "reason": f"No audit data found, but protocol has ${protocol_tvl/1e9:.1f}B TVL suggesting maturity",
                "audited": False,
            }
        elif protocol_tvl > 100_000_000:
            return {
                "score": 4.0,
                "reason": f"No audit data found, protocol has ${protocol_tvl/1e6:.0f}M TVL",
                "audited": False,
            }
        else:
            return {
                "score": 6.0,
                "reason": "No audit data found and relatively small protocol TVL",
                "audited": False,
            }

    return {
        "score": 7.0,
        "reason": "Unknown protocol with no audit data or metadata available",
        "audited": False,
    }


def _score_tvl_risk(pool: Dict) -> Dict:
    """Score TVL risk based on pool size and trends.

    Args:
        pool: Pool data.

    Returns:
        Dict with score and reason.
    """
    tvl = _safe_float(pool.get("tvlUsd"))
    pct_7d = pool.get("tvlPct7D")
    pct_30d = pool.get("tvlPct30D")

    # Base score from TVL size
    if tvl >= 1_000_000_000:
        base_score = 0.5
        size_desc = "Extremely high TVL"
    elif tvl >= 500_000_000:
        base_score = 1.0
        size_desc = "Very high TVL"
    elif tvl >= 100_000_000:
        base_score = 1.5
        size_desc = "High TVL"
    elif tvl >= 50_000_000:
        base_score = 2.5
        size_desc = "Moderate-high TVL"
    elif tvl >= 10_000_000:
        base_score = 3.5
        size_desc = "Moderate TVL"
    elif tvl >= 1_000_000:
        base_score = 5.0
        size_desc = "Low TVL"
    elif tvl >= 100_000:
        base_score = 7.0
        size_desc = "Very low TVL"
    else:
        base_score = 9.0
        size_desc = "Minimal TVL"

    # Adjust for trends
    trend_adj = 0
    trend_desc = ""
    if pct_7d is not None:
        pct_7d_val = _safe_float(pct_7d)
        if pct_7d_val < -20:
            trend_adj += 2.0
            trend_desc = "severe TVL decline (7d)"
        elif pct_7d_val < -10:
            trend_adj += 1.0
            trend_desc = "significant TVL decline (7d)"
        elif pct_7d_val > 20:
            trend_adj -= 0.5
            trend_desc = "strong TVL growth (7d)"

    if pct_30d is not None:
        pct_30d_val = _safe_float(pct_30d)
        if pct_30d_val < -30:
            trend_adj += 1.5
            trend_desc += (", " if trend_desc else "") + "severe decline (30d)"
        elif pct_30d_val < -15:
            trend_adj += 0.5
            trend_desc += (", " if trend_desc else "") + "declining (30d)"

    final_score = min(10, max(0, base_score + trend_adj))
    tvl_display = _format_tvl(tvl)

    reason = f"{size_desc} ({tvl_display})"
    if trend_desc:
        reason += f" with {trend_desc}"

    return {
        "score": round(final_score, 1),
        "reason": reason,
        "tvl_usd": tvl,
        "tvl_display": tvl_display,
    }


def _score_apy_sustainability(pool: Dict) -> Dict:
    """Score APY sustainability risk.

    Very high APYs are often unsustainable and signal risk.

    Args:
        pool: Pool data.

    Returns:
        Dict with score and reason.
    """
    apy = _safe_float(pool.get("apy"))
    apy_base = _safe_float(pool.get("apyBase"))
    apy_reward = _safe_float(pool.get("apyReward"))
    is_stablecoin = pool.get("stablecoin", False)

    # Adjust thresholds for stablecoin vs volatile
    if is_stablecoin:
        # Stablecoin lending: sustainable range is 1-10%
        if apy <= 8:
            score = 1.0
            reason = f"APY of {apy:.1f}% is within sustainable range for stablecoin lending"
        elif apy <= 15:
            score = 3.0
            reason = f"APY of {apy:.1f}% is above average for stablecoins, monitor sustainability"
        elif apy <= 30:
            score = 5.0
            reason = f"APY of {apy:.1f}% is high for stablecoins, likely from temporary incentives"
        elif apy <= 50:
            score = 7.0
            reason = f"APY of {apy:.1f}% is very high for stablecoins, likely unsustainable"
        else:
            score = 9.0
            reason = f"APY of {apy:.1f}% is extremely high for stablecoins, almost certainly unsustainable"
    else:
        # Volatile pairs: higher APY is more common
        if apy <= 15:
            score = 1.5
            reason = f"APY of {apy:.1f}% is conservative for volatile assets"
        elif apy <= 30:
            score = 3.0
            reason = f"APY of {apy:.1f}% is moderate, check reward token sustainability"
        elif apy <= 60:
            score = 5.0
            reason = f"APY of {apy:.1f}% is elevated, partially driven by token incentives"
        elif apy <= 100:
            score = 7.0
            reason = f"APY of {apy:.1f}% is very high, likely from heavy token emissions"
        else:
            score = 9.0
            reason = f"APY of {apy:.1f}% is extremely high, almost certainly unsustainable"

    # Penalize if most APY comes from rewards (less sustainable)
    if apy > 0 and apy_reward > 0:
        reward_ratio = apy_reward / apy
        if reward_ratio > 0.8:
            score = min(10, score + 1.5)
            reason += f". {reward_ratio*100:.0f}% of APY from token rewards (less sustainable)"
        elif reward_ratio > 0.5:
            score = min(10, score + 0.5)
            reason += f". {reward_ratio*100:.0f}% of APY from token rewards"

    # Check APY trend (apyPct1D, apyPct7D, apyPct30D)
    apy_pct_30d = pool.get("apyPct30D")
    if apy_pct_30d is not None:
        apy_trend = _safe_float(apy_pct_30d)
        if apy_trend < -50:
            score = min(10, score + 1.0)
            reason += ". APY has dropped significantly over 30 days"

    return {
        "score": round(min(10, max(0, score)), 1),
        "reason": reason,
        "apy_total": round(apy, 2),
        "apy_base": round(apy_base, 2),
        "apy_reward": round(apy_reward, 2),
    }


def _score_il_risk(pool: Dict) -> Dict:
    """Score impermanent loss risk.

    Args:
        pool: Pool data.

    Returns:
        Dict with score and reason.
    """
    is_stablecoin = pool.get("stablecoin", False)
    il_risk_flag = pool.get("ilRisk", "")
    symbol = pool.get("symbol", "")

    # Single-asset pools (lending, staking)
    if "-" not in symbol and "/" not in symbol:
        return {
            "score": 0.0,
            "reason": "Single-asset pool (lending/staking), no impermanent loss risk",
            "il_type": "none",
        }

    # All-stablecoin pairs
    if is_stablecoin:
        return {
            "score": 0.5,
            "reason": "Stablecoin pool, minimal impermanent loss risk from depegs only",
            "il_type": "minimal",
        }

    # Check if it's flagged as no IL risk
    if il_risk_flag == "no":
        return {
            "score": 0.5,
            "reason": "Pool flagged as no IL risk by DeFiLlama",
            "il_type": "none",
        }

    # Multi-asset volatile pair
    stables = {"USDC", "USDT", "DAI", "BUSD", "FRAX", "LUSD", "TUSD", "GUSD", "USDP"}
    tokens = [t.strip() for t in symbol.replace("/", "-").split("-")]
    stable_count = sum(1 for t in tokens if t.upper() in stables)

    if stable_count == len(tokens) - 1:
        # One volatile + one or more stables
        return {
            "score": 4.0,
            "reason": f"Volatile-stable pair ({symbol}), moderate IL risk from price movement",
            "il_type": "moderate",
        }
    elif stable_count == 0:
        # All volatile
        correlated_pairs = [
            ("ETH", "STETH"), ("ETH", "WSTETH"), ("ETH", "RETH"), ("ETH", "CBETH"),
            ("BTC", "WBTC"), ("BTC", "TBTC"),
        ]
        token_upper = [t.upper() for t in tokens]
        for a, b in correlated_pairs:
            if a in token_upper and b in token_upper:
                return {
                    "score": 1.5,
                    "reason": f"Correlated pair ({symbol}), low IL risk as assets track each other",
                    "il_type": "low",
                }
        return {
            "score": 7.0,
            "reason": f"Volatile-volatile pair ({symbol}), high IL risk from uncorrelated price movement",
            "il_type": "high",
        }

    return {
        "score": 5.0,
        "reason": f"Mixed pair ({symbol}), moderate IL risk",
        "il_type": "moderate",
    }


def _score_chain_risk(pool: Dict) -> Dict:
    """Score chain risk based on network maturity.

    Args:
        pool: Pool data.

    Returns:
        Dict with score and reason.
    """
    chain = pool.get("chain", "Unknown")
    score = CHAIN_RISK_SCORES.get(chain, DEFAULT_CHAIN_RISK)

    maturity_map = {
        (0, 1.5): "Most battle-tested blockchain",
        (1.5, 2.5): "Well-established network with strong security",
        (2.5, 3.5): "Established network, moderate track record",
        (3.5, 4.5): "Newer or less-proven network",
        (4.5, 10): "Less mature network, higher risk",
    }

    desc = "Unknown chain maturity"
    for (low, high), description in maturity_map.items():
        if low <= score < high:
            desc = description
            break

    return {
        "score": round(score, 1),
        "reason": f"{chain}: {desc}",
        "chain": chain,
    }


def _get_risk_level(score: float) -> str:
    """Get risk level label from numeric score.

    Args:
        score: Risk score 0-10.

    Returns:
        Risk level string.
    """
    if score <= 1:
        return "SAFE"
    elif score <= 3:
        return "LOW"
    elif score <= 5:
        return "MEDIUM"
    elif score <= 7:
        return "HIGH"
    else:
        return "CRITICAL"


def _generate_recommendation(risk_score: float, risk_level: str, breakdown: Dict) -> str:
    """Generate a human-readable recommendation.

    Args:
        risk_score: Overall risk score.
        risk_level: Risk level string.
        breakdown: Risk breakdown dict.

    Returns:
        Recommendation string.
    """
    if risk_level == "SAFE":
        return "Excellent low-risk yield opportunity. Suitable for large conservative allocations."
    elif risk_level == "LOW":
        return "Good risk-adjusted yield. Suitable for core portfolio positions with regular monitoring."
    elif risk_level == "MEDIUM":
        recs = ["Moderate risk opportunity. Limit allocation to 20-30% of DeFi portfolio."]
        if breakdown.get("apy_sustainability", {}).get("score", 0) > 5:
            recs.append("APY may not be sustainable long-term.")
        if breakdown.get("il_risk", {}).get("score", 0) > 4:
            recs.append("Consider impermanent loss before entering.")
        return " ".join(recs)
    elif risk_level == "HIGH":
        recs = ["Significant risks detected. Only allocate 5-10% of portfolio."]
        if breakdown.get("protocol_risk", {}).get("score", 0) > 5:
            recs.append("Protocol lacks sufficient audit coverage.")
        if breakdown.get("apy_sustainability", {}).get("score", 0) > 6:
            recs.append("APY appears unsustainable.")
        return " ".join(recs)
    else:
        return "Critical risk level. Avoid this opportunity or limit to speculative micro-allocations only."


def _find_protocol_metadata(protocols: List[Dict], project_name: str) -> Optional[Dict]:
    """Find protocol metadata from DeFiLlama protocols list.

    Args:
        protocols: Protocol list from DeFiLlama.
        project_name: Project name to search for.

    Returns:
        Protocol metadata dict or None.
    """
    project_lower = project_name.lower()
    for proto in protocols:
        slug = proto.get("slug", "").lower()
        name = proto.get("name", "").lower()
        if slug == project_lower or project_lower in slug or project_lower in name:
            return proto
    return None


def score_yield_risk(params: Dict) -> Dict:
    """Main function to risk-score a yield opportunity.

    Args:
        params: Input parameters.

    Returns:
        Result dict with risk scores and breakdown.
    """
    # Fetch pool data
    pools_data, error = _fetch_json(DEFILLAMA_POOLS_URL)
    if error:
        return {
            "success": False,
            "error": f"Failed to fetch pool data: {error}",
        }

    pools = pools_data.get("data", [])
    if not pools:
        return {"success": False, "error": "No pool data available"}

    # Find the target pool
    pool = _find_pool(pools, params)
    if not pool:
        search_desc = []
        if params.get("pool_id"):
            search_desc.append(f"pool_id={params['pool_id']}")
        if params.get("protocol"):
            search_desc.append(f"protocol={params['protocol']}")
        if params.get("chain"):
            search_desc.append(f"chain={params['chain']}")
        if params.get("symbol"):
            search_desc.append(f"symbol={params['symbol']}")
        return {
            "success": False,
            "error": f"Pool not found matching: {', '.join(search_desc)}",
            "suggestion": "Try broadening your search or check the protocol/chain names.",
        }

    # Fetch protocol metadata
    protocols_data, proto_error = _fetch_json(DEFILLAMA_PROTOCOLS_URL)
    protocol_meta = None
    if not proto_error and isinstance(protocols_data, list):
        project_name = pool.get("project", "")
        protocol_meta = _find_protocol_metadata(protocols_data, project_name)

    # Score each risk dimension
    protocol_risk = _score_protocol_risk(pool, protocol_meta)
    tvl_risk = _score_tvl_risk(pool)
    apy_sustainability = _score_apy_sustainability(pool)
    il_risk = _score_il_risk(pool)
    chain_risk = _score_chain_risk(pool)

    breakdown = {
        "protocol_risk": protocol_risk,
        "tvl_risk": tvl_risk,
        "apy_sustainability": apy_sustainability,
        "il_risk": il_risk,
        "chain_risk": chain_risk,
    }

    # Calculate weighted overall score
    weighted_score = (
        protocol_risk["score"] * RISK_WEIGHTS["protocol_risk"]
        + tvl_risk["score"] * RISK_WEIGHTS["tvl_risk"]
        + apy_sustainability["score"] * RISK_WEIGHTS["apy_sustainability"]
        + il_risk["score"] * RISK_WEIGHTS["il_risk"]
        + chain_risk["score"] * RISK_WEIGHTS["chain_risk"]
    )
    weighted_score = round(min(10, max(0, weighted_score)), 1)
    risk_level = _get_risk_level(weighted_score)

    # Build audit info
    project = pool.get("project", "").lower()
    audit_info = {"audited": False, "auditors": [], "audit_score": 0}
    for key, info in AUDITED_PROTOCOLS.items():
        if key in project or project in key:
            audit_info = {
                "audited": True,
                "auditors": info["audits"],
                "audit_score": info["score"],
            }
            break

    recommendation = _generate_recommendation(weighted_score, risk_level, breakdown)

    return {
        "success": True,
        "pool": {
            "symbol": pool.get("symbol", "Unknown"),
            "pool_id": pool.get("pool", ""),
            "chain": pool.get("chain", "Unknown"),
            "protocol": pool.get("project", "Unknown"),
            "apy": round(_safe_float(pool.get("apy")), 2),
            "apy_base": round(_safe_float(pool.get("apyBase")), 2),
            "apy_reward": round(_safe_float(pool.get("apyReward")), 2),
            "tvl_usd": round(_safe_float(pool.get("tvlUsd")), 2),
            "tvl_display": _format_tvl(_safe_float(pool.get("tvlUsd"))),
            "stablecoin": pool.get("stablecoin", False),
        },
        "risk_score": weighted_score,
        "risk_level": risk_level,
        "risk_breakdown": breakdown,
        "audit_info": audit_info,
        "recommendation": recommendation,
        "metadata": {
            "risk_weights": RISK_WEIGHTS,
            "data_source": "DeFiLlama",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
    }


def main() -> None:
    """Entry point: read JSON from stdin, process, write JSON to stdout."""
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            params = {}
        else:
            params = json.loads(raw_input)
    except json.JSONDecodeError as e:
        result = {
            "success": False,
            "error": f"Invalid JSON input: {str(e)}",
            "usage": {
                "option_1": "Search by pool ID: {\"pool_id\": \"pool-id-here\"}",
                "option_2": "Search by attributes: {\"protocol\": \"aave-v3\", \"chain\": \"ethereum\", \"symbol\": \"USDC\"}",
            },
        }
        print(json.dumps(result, indent=2))
        return

    if not isinstance(params, dict):
        result = {"success": False, "error": "Input must be a JSON object"}
        print(json.dumps(result, indent=2))
        return

    # Require at least one search parameter
    if not any(params.get(k) for k in ("pool_id", "protocol", "chain", "symbol")):
        result = {
            "success": False,
            "error": "At least one search parameter required (pool_id, protocol, chain, or symbol)",
            "usage": {
                "option_1": "Search by pool ID: {\"pool_id\": \"pool-id-here\"}",
                "option_2": "Search by attributes: {\"protocol\": \"aave-v3\", \"chain\": \"ethereum\", \"symbol\": \"USDC\"}",
            },
        }
        print(json.dumps(result, indent=2))
        return

    result = score_yield_risk(params)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
