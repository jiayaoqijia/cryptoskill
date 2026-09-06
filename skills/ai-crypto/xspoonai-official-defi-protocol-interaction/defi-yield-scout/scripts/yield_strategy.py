#!/usr/bin/env python3
"""
DeFi Yield Strategy Recommender - Personalized yield strategy recommendations.

Generates tailored DeFi yield strategies based on capital, risk tolerance,
preferred chains, stablecoin preferences, and investment timeframe. Fetches
real-time pool data from DeFiLlama to recommend specific protocols and pools.

Input (JSON via stdin):
{
    "capital_usd": 10000,
    "risk_tolerance": "medium",
    "preferred_chains": ["ethereum", "arbitrum"],
    "stablecoin_preference": true,
    "timeframe": "6m"
}

Output (JSON via stdout):
{
    "success": true,
    "strategies": [...],
    "portfolio_summary": {...}
}

API: https://yields.llama.fi/pools (free, no API key)
"""

import json
import sys
import urllib.request
import urllib.error
import time
import math
from typing import Any, Dict, List, Optional, Tuple


# DeFiLlama API
DEFILLAMA_POOLS_URL = "https://yields.llama.fi/pools"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2.0

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
    "linea": "Linea",
    "scroll": "Scroll",
    "zksync": "zkSync Era",
    "mantle": "Mantle",
    "blast": "Blast",
}

# Timeframe to days mapping
TIMEFRAME_DAYS: Dict[str, int] = {
    "1m": 30,
    "3m": 90,
    "6m": 180,
    "1y": 365,
    "2y": 730,
}

# Blue-chip protocols considered safe for conservative strategies
BLUE_CHIP_PROTOCOLS = {
    "aave-v3", "aave-v2", "compound-v3", "compound", "lido", "maker",
    "makerdao", "spark", "rocket-pool", "sky",
}

# Established protocols for balanced strategies
ESTABLISHED_PROTOCOLS = BLUE_CHIP_PROTOCOLS | {
    "curve-dex", "curve", "uniswap-v3", "uniswap-v2", "balancer-v2",
    "balancer", "convex-finance", "yearn-finance", "morpho",
    "frax", "frax-ether", "instadapp",
}

# Risk tolerance configuration
RISK_CONFIGS: Dict[str, Dict] = {
    "low": {
        "allocations": [
            {"name": "Conservative Foundation", "pct": 70, "type": "conservative"},
            {"name": "Moderate Growth", "pct": 30, "type": "balanced"},
        ],
        "max_apy_threshold": 20,
        "min_tvl": 50_000_000,
        "prefer_stablecoins": True,
        "max_il_risk": "low",
    },
    "medium": {
        "allocations": [
            {"name": "Conservative Foundation", "pct": 50, "type": "conservative"},
            {"name": "Balanced Growth", "pct": 35, "type": "balanced"},
            {"name": "Opportunistic Alpha", "pct": 15, "type": "aggressive"},
        ],
        "max_apy_threshold": 50,
        "min_tvl": 10_000_000,
        "prefer_stablecoins": False,
        "max_il_risk": "moderate",
    },
    "high": {
        "allocations": [
            {"name": "Stable Base", "pct": 25, "type": "conservative"},
            {"name": "Growth Engine", "pct": 40, "type": "balanced"},
            {"name": "Aggressive Alpha", "pct": 35, "type": "aggressive"},
        ],
        "max_apy_threshold": 200,
        "min_tvl": 1_000_000,
        "prefer_stablecoins": False,
        "max_il_risk": "high",
    },
}

# Strategy type to pool selection criteria
STRATEGY_CRITERIA: Dict[str, Dict] = {
    "conservative": {
        "min_tvl": 100_000_000,
        "max_apy": 15,
        "stablecoin_preferred": True,
        "single_asset_preferred": True,
        "allowed_il": "none",
        "target_risk_score": 1.5,
        "description": "Blue-chip lending and liquid staking with established protocols",
    },
    "balanced": {
        "min_tvl": 10_000_000,
        "max_apy": 40,
        "stablecoin_preferred": False,
        "single_asset_preferred": False,
        "allowed_il": "moderate",
        "target_risk_score": 4.0,
        "description": "Mix of lending, LP positions, and L2 opportunities",
    },
    "aggressive": {
        "min_tvl": 1_000_000,
        "max_apy": 200,
        "stablecoin_preferred": False,
        "single_asset_preferred": False,
        "allowed_il": "high",
        "target_risk_score": 6.5,
        "description": "High-APY farms, newer protocols, and volatile pairs",
    },
}

# Protocol risk scores for quick assessment
PROTOCOL_RISK_SCORES: Dict[str, float] = {
    "aave-v3": 1.0, "aave-v2": 1.0, "compound-v3": 1.0, "compound": 1.0,
    "lido": 1.0, "maker": 1.0, "makerdao": 1.0, "spark": 1.5, "sky": 1.0,
    "rocket-pool": 1.5, "curve-dex": 2.0, "curve": 2.0,
    "uniswap-v3": 2.0, "uniswap-v2": 2.0, "balancer-v2": 2.5, "balancer": 2.5,
    "convex-finance": 3.0, "yearn-finance": 2.5, "morpho": 2.5,
    "frax": 3.0, "frax-ether": 3.0, "instadapp": 3.0,
    "pendle": 4.0, "gmx": 4.0, "eigenlayer": 3.5,
    "pancakeswap": 3.5, "sushiswap": 3.5, "stargate": 3.5,
    "venus": 4.0, "benqi": 4.0, "radiant-v2": 5.0,
}

DEFAULT_PROTOCOL_RISK = 6.0


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


def _normalize_chain(chain: str) -> str:
    """Normalize chain name to DeFiLlama format."""
    return CHAIN_ALIASES.get(chain.lower(), chain.title())


def _get_il_risk(pool: Dict) -> str:
    """Get IL risk level for a pool."""
    if pool.get("stablecoin", False):
        return "none"

    symbol = pool.get("symbol", "")
    if "-" not in symbol and "/" not in symbol:
        return "none"

    stables = {"USDC", "USDT", "DAI", "BUSD", "FRAX", "LUSD", "TUSD"}
    tokens = [t.strip().upper() for t in symbol.replace("/", "-").split("-")]
    stable_count = sum(1 for t in tokens if t in stables)

    if stable_count == len(tokens):
        return "low"
    elif stable_count >= 1:
        return "moderate"

    # Check correlated pairs
    correlated = [
        ("ETH", "STETH"), ("ETH", "WSTETH"), ("ETH", "RETH"), ("ETH", "CBETH"),
        ("BTC", "WBTC"), ("BTC", "TBTC"),
    ]
    for a, b in correlated:
        if a in tokens and b in tokens:
            return "low"

    return "high"


def _get_protocol_risk(project: str) -> float:
    """Get risk score for a protocol."""
    project_lower = project.lower()
    for key, score in PROTOCOL_RISK_SCORES.items():
        if key in project_lower or project_lower in key:
            return score
    return DEFAULT_PROTOCOL_RISK


def _pool_matches_criteria(pool: Dict, criteria: Dict, chain_filter: Optional[List[str]]) -> bool:
    """Check if a pool matches the strategy criteria.

    Args:
        pool: Pool data.
        criteria: Strategy criteria dict.
        chain_filter: Optional list of normalized chain names.

    Returns:
        True if pool matches.
    """
    apy = _safe_float(pool.get("apy"))
    tvl = _safe_float(pool.get("tvlUsd"))

    # Basic filters
    if apy <= 0 or apy > criteria["max_apy"]:
        return False
    if tvl < criteria["min_tvl"]:
        return False

    # Skip unreasonable APYs
    if apy > 10000:
        return False

    # Chain filter
    if chain_filter:
        if pool.get("chain", "") not in chain_filter:
            return False

    # IL risk filter
    il_risk = _get_il_risk(pool)
    allowed_il = criteria["allowed_il"]
    il_order = {"none": 0, "low": 1, "moderate": 2, "high": 3}
    if il_order.get(il_risk, 3) > il_order.get(allowed_il, 3):
        return False

    # Stablecoin preference
    if criteria["stablecoin_preferred"] and not pool.get("stablecoin", False):
        # Allow single-asset pools even if not stablecoin (e.g., stETH)
        symbol = pool.get("symbol", "")
        if "-" in symbol or "/" in symbol:
            return False

    # Single asset preference
    if criteria["single_asset_preferred"]:
        symbol = pool.get("symbol", "")
        if "-" in symbol or "/" in symbol:
            # Allow stablecoin-stablecoin pairs
            if not pool.get("stablecoin", False):
                return False

    return True


def _select_pools_for_strategy(
    pools: List[Dict],
    strategy_type: str,
    chain_filter: Optional[List[str]],
    allocation_usd: float,
    max_positions: int = 3,
) -> List[Dict]:
    """Select the best pools for a strategy type.

    Args:
        pools: All available pools.
        strategy_type: "conservative", "balanced", or "aggressive".
        chain_filter: Optional chain filter.
        allocation_usd: USD to allocate.
        max_positions: Maximum number of positions.

    Returns:
        List of selected position dicts.
    """
    criteria = STRATEGY_CRITERIA[strategy_type]

    # Filter matching pools
    candidates = []
    for pool in pools:
        if _pool_matches_criteria(pool, criteria, chain_filter):
            # Prefer blue-chip for conservative
            project = pool.get("project", "").lower()
            if strategy_type == "conservative":
                is_blue_chip = any(bc in project for bc in BLUE_CHIP_PROTOCOLS)
                if not is_blue_chip:
                    continue

            risk = _get_protocol_risk(pool.get("project", ""))
            apy = _safe_float(pool.get("apy"))
            tvl = _safe_float(pool.get("tvlUsd"))

            # Score: higher APY is better, lower risk is better, higher TVL is better
            # Weighted scoring to balance risk and return
            if strategy_type == "conservative":
                score = apy * 0.3 + (10 - risk) * 0.5 + math.log10(max(tvl, 1)) * 0.2
            elif strategy_type == "balanced":
                score = apy * 0.4 + (10 - risk) * 0.3 + math.log10(max(tvl, 1)) * 0.3
            else:
                score = apy * 0.6 + (10 - risk) * 0.2 + math.log10(max(tvl, 1)) * 0.2

            candidates.append({
                "pool": pool,
                "score": score,
                "risk": risk,
            })

    if not candidates:
        return []

    # Sort by score descending
    candidates.sort(key=lambda c: c["score"], reverse=True)

    # Deduplicate by protocol (avoid putting everything in one protocol)
    seen_protocols = set()
    selected = []
    for candidate in candidates:
        project = candidate["pool"].get("project", "").lower()
        # Allow max 1 position per protocol per strategy
        base_project = project.split("-")[0] if "-" in project else project
        if base_project in seen_protocols:
            continue
        seen_protocols.add(base_project)
        selected.append(candidate)
        if len(selected) >= max_positions:
            break

    # If we couldn't get enough unique protocols, fill with duplicates
    if len(selected) < max_positions:
        for candidate in candidates:
            if candidate not in selected:
                selected.append(candidate)
                if len(selected) >= max_positions:
                    break

    # Allocate capital evenly across positions, weighted slightly by score
    positions = []
    total_score = sum(s["score"] for s in selected) if selected else 1
    remaining = allocation_usd

    for i, sel in enumerate(selected):
        pool = sel["pool"]
        if i == len(selected) - 1:
            amount = remaining  # Give remainder to last position
        else:
            weight = sel["score"] / total_score
            amount = round(allocation_usd * weight, 2)
            remaining -= amount

        positions.append({
            "protocol": pool.get("project", "Unknown"),
            "chain": pool.get("chain", "Unknown"),
            "pool": pool.get("symbol", "Unknown"),
            "apy": round(_safe_float(pool.get("apy")), 2),
            "apy_base": round(_safe_float(pool.get("apyBase")), 2),
            "apy_reward": round(_safe_float(pool.get("apyReward")), 2),
            "tvl_display": _format_tvl(_safe_float(pool.get("tvlUsd"))),
            "amount_usd": round(amount, 2),
            "il_risk": _get_il_risk(pool),
            "risk_score": round(sel["risk"], 1),
        })

    return positions


def _validate_input(params: Dict) -> Tuple[Dict, Optional[str]]:
    """Validate and normalize input parameters.

    Args:
        params: Raw input parameters.

    Returns:
        Tuple of (normalized_params, error_string).
    """
    normalized = {}

    # Capital
    capital = _safe_float(params.get("capital_usd", 10000))
    if capital <= 0:
        return {}, "capital_usd must be positive"
    normalized["capital_usd"] = capital

    # Risk tolerance
    risk = params.get("risk_tolerance", "medium")
    if isinstance(risk, str):
        risk = risk.lower().strip()
    if risk not in RISK_CONFIGS:
        return {}, f"risk_tolerance must be one of: {', '.join(RISK_CONFIGS.keys())}"
    normalized["risk_tolerance"] = risk

    # Preferred chains
    chains = params.get("preferred_chains", ["all"])
    if isinstance(chains, str):
        chains = [chains]
    if not isinstance(chains, list):
        return {}, "preferred_chains must be a list of chain names"

    if "all" in [c.lower() for c in chains] or not chains:
        normalized["preferred_chains"] = None
    else:
        normalized["preferred_chains"] = [_normalize_chain(c) for c in chains]

    # Stablecoin preference
    normalized["stablecoin_preference"] = bool(params.get("stablecoin_preference", False))

    # Timeframe
    timeframe = params.get("timeframe", "6m")
    if isinstance(timeframe, str):
        timeframe = timeframe.lower().strip()
    if timeframe not in TIMEFRAME_DAYS:
        return {}, f"timeframe must be one of: {', '.join(TIMEFRAME_DAYS.keys())}"
    normalized["timeframe"] = timeframe
    normalized["holding_days"] = TIMEFRAME_DAYS[timeframe]

    return normalized, None


def _generate_risk_warnings(strategies: List[Dict], params: Dict) -> List[str]:
    """Generate risk warnings based on the strategy portfolio.

    Args:
        strategies: List of strategy dicts.
        params: Input parameters.

    Returns:
        List of warning strings.
    """
    warnings = []

    # Check if any position has high APY
    for strategy in strategies:
        for pos in strategy.get("positions", []):
            if pos.get("apy", 0) > 50:
                warnings.append(
                    f"Position in {pos['protocol']} ({pos['pool']}) has {pos['apy']}% APY. "
                    f"Very high APYs may not be sustainable."
                )
                break

    # Check IL exposure
    high_il_count = sum(
        1 for s in strategies
        for p in s.get("positions", [])
        if p.get("il_risk") in ("moderate", "high")
    )
    if high_il_count > 0:
        warnings.append(
            f"{high_il_count} position(s) have moderate-to-high impermanent loss risk. "
            f"Use the IL calculator to assess potential losses."
        )

    # Capital-specific warnings
    capital = params.get("capital_usd", 0)
    if capital < 1000:
        warnings.append(
            "With capital under $1,000, gas fees on Ethereum mainnet may significantly "
            "eat into yields. Consider L2 chains (Arbitrum, Base, Optimism) instead."
        )
    elif capital < 5000:
        warnings.append(
            "With smaller capital, prefer L2 chains to minimize gas fee impact on returns."
        )

    # General DeFi warnings
    warnings.append(
        "DeFi yields are variable and can change rapidly. Monitor positions regularly "
        "and rebalance as needed."
    )
    warnings.append(
        "Smart contract risk exists for all DeFi protocols. Consider using the "
        "Smart Contract Auditor skill for additional due diligence."
    )

    return warnings


def recommend_strategies(params: Dict) -> Dict:
    """Generate personalized yield strategy recommendations.

    Args:
        params: Validated input parameters.

    Returns:
        Result dict with strategies and portfolio summary.
    """
    # Fetch pool data
    data, error = _fetch_json(DEFILLAMA_POOLS_URL)
    if error:
        return {
            "success": False,
            "error": f"Failed to fetch pool data: {error}",
            "suggestion": "DeFiLlama API may be temporarily unavailable. Try again shortly.",
        }

    pools = data.get("data", [])
    if not pools:
        return {"success": False, "error": "No pool data available from DeFiLlama"}

    risk_tolerance = params["risk_tolerance"]
    capital = params["capital_usd"]
    chain_filter = params["preferred_chains"]
    stablecoin_pref = params["stablecoin_preference"]
    holding_days = params["holding_days"]

    risk_config = RISK_CONFIGS[risk_tolerance]
    allocations = risk_config["allocations"]

    # If stablecoin preference, bias strategies toward stablecoins
    if stablecoin_pref:
        for alloc in allocations:
            if alloc["type"] in ("conservative", "balanced"):
                # Override criteria for stablecoin preference
                pass  # Criteria already handle this through pool filtering

    strategies = []
    all_positions = []

    for alloc in allocations:
        alloc_usd = capital * (alloc["pct"] / 100.0)
        strategy_type = alloc["type"]
        criteria = STRATEGY_CRITERIA[strategy_type]

        # Adjust criteria for stablecoin preference
        effective_criteria = dict(criteria)
        if stablecoin_pref and strategy_type != "aggressive":
            effective_criteria["stablecoin_preferred"] = True

        positions = _select_pools_for_strategy(
            pools, strategy_type, chain_filter, alloc_usd,
            max_positions=3 if strategy_type != "aggressive" else 2,
        )

        if not positions:
            # Fallback: create a placeholder recommendation
            positions = [{
                "protocol": "N/A",
                "chain": "N/A",
                "pool": f"No matching {strategy_type} pools found",
                "apy": 0,
                "apy_base": 0,
                "apy_reward": 0,
                "tvl_display": "N/A",
                "amount_usd": alloc_usd,
                "il_risk": "none",
                "risk_score": 0,
            }]

        # Calculate strategy-level metrics
        total_alloc = sum(p["amount_usd"] for p in positions)
        if total_alloc > 0:
            weighted_apy = sum(
                p["apy"] * (p["amount_usd"] / total_alloc)
                for p in positions
                if p["apy"] > 0
            )
            weighted_risk = sum(
                p["risk_score"] * (p["amount_usd"] / total_alloc)
                for p in positions
                if p["risk_score"] > 0
            )
        else:
            weighted_apy = 0
            weighted_risk = 0

        # Determine risk level
        if weighted_risk <= 1:
            risk_level = "SAFE"
        elif weighted_risk <= 3:
            risk_level = "LOW"
        elif weighted_risk <= 5:
            risk_level = "MEDIUM"
        elif weighted_risk <= 7:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"

        # Determine IL exposure
        il_risks = [p["il_risk"] for p in positions if p["il_risk"] != "none"]
        if not il_risks:
            il_exposure = "none"
        elif "high" in il_risks:
            il_exposure = "high"
        elif "moderate" in il_risks:
            il_exposure = "moderate"
        else:
            il_exposure = "low"

        # Expected earnings
        expected_earnings = alloc_usd * (weighted_apy / 100) * (holding_days / 365)

        strategy = {
            "name": alloc["name"],
            "allocation_pct": alloc["pct"],
            "allocation_usd": round(alloc_usd, 2),
            "expected_apy": round(weighted_apy, 2),
            "expected_apy_range": _format_apy_range(positions),
            "risk_score": round(weighted_risk, 1),
            "risk_level": risk_level,
            "il_exposure": il_exposure,
            "description": criteria["description"],
            "expected_earnings": round(expected_earnings, 2),
            "positions": positions,
        }
        strategies.append(strategy)
        all_positions.extend(positions)

    # Portfolio summary
    total_capital = sum(s["allocation_usd"] for s in strategies)
    if total_capital > 0:
        portfolio_weighted_apy = sum(
            s["expected_apy"] * (s["allocation_usd"] / total_capital)
            for s in strategies
        )
        portfolio_weighted_risk = sum(
            s["risk_score"] * (s["allocation_usd"] / total_capital)
            for s in strategies
        )
    else:
        portfolio_weighted_apy = 0
        portfolio_weighted_risk = 0

    expected_annual_yield = capital * (portfolio_weighted_apy / 100)
    expected_period_yield = expected_annual_yield * (holding_days / 365)

    # Unique protocols and chains
    unique_protocols = set(
        p["protocol"] for p in all_positions if p["protocol"] != "N/A"
    )
    unique_chains = set(
        p["chain"] for p in all_positions if p["chain"] != "N/A"
    )

    portfolio_summary = {
        "total_capital": round(capital, 2),
        "weighted_apy": round(portfolio_weighted_apy, 2),
        "weighted_risk_score": round(portfolio_weighted_risk, 1),
        "expected_annual_yield": round(expected_annual_yield, 2),
        "expected_period_yield": round(expected_period_yield, 2),
        "holding_period": params["timeframe"],
        "holding_days": holding_days,
        "num_strategies": len(strategies),
        "num_positions": len([p for p in all_positions if p["protocol"] != "N/A"]),
        "unique_protocols": len(unique_protocols),
        "unique_chains": len(unique_chains),
        "diversification_score": _calc_diversification_score(all_positions),
    }

    # Risk warnings
    warnings = _generate_risk_warnings(strategies, params)

    return {
        "success": True,
        "profile": {
            "capital_usd": capital,
            "risk_tolerance": risk_tolerance,
            "preferred_chains": params["preferred_chains"] or ["all"],
            "stablecoin_preference": stablecoin_pref,
            "timeframe": params["timeframe"],
        },
        "strategies": strategies,
        "portfolio_summary": portfolio_summary,
        "warnings": warnings,
        "metadata": {
            "data_source": "DeFiLlama",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "pools_analyzed": len(pools),
        },
    }


def _format_apy_range(positions: List[Dict]) -> str:
    """Format the APY range across positions.

    Args:
        positions: List of position dicts.

    Returns:
        Formatted string like "3-8%".
    """
    apys = [p["apy"] for p in positions if p["apy"] > 0]
    if not apys:
        return "N/A"
    if len(apys) == 1:
        return f"{apys[0]:.1f}%"
    return f"{min(apys):.1f}-{max(apys):.1f}%"


def _calc_diversification_score(positions: List[Dict]) -> str:
    """Calculate a simple diversification score.

    Args:
        positions: All positions across strategies.

    Returns:
        Diversification rating string.
    """
    valid = [p for p in positions if p["protocol"] != "N/A"]
    if not valid:
        return "none"

    unique_protocols = len(set(p["protocol"] for p in valid))
    unique_chains = len(set(p["chain"] for p in valid))

    total = unique_protocols + unique_chains
    if total >= 8:
        return "excellent"
    elif total >= 5:
        return "good"
    elif total >= 3:
        return "moderate"
    else:
        return "low"


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
                "description": "Get personalized DeFi yield strategy recommendations",
                "example_input": {
                    "capital_usd": 10000,
                    "risk_tolerance": "medium",
                    "preferred_chains": ["ethereum", "arbitrum"],
                    "stablecoin_preference": False,
                    "timeframe": "6m",
                },
            },
        }
        print(json.dumps(result, indent=2))
        return

    if not isinstance(params, dict):
        result = {"success": False, "error": "Input must be a JSON object"}
        print(json.dumps(result, indent=2))
        return

    # Validate input
    validated, error = _validate_input(params)
    if error:
        result = {"success": False, "error": f"Input validation failed: {error}"}
        print(json.dumps(result, indent=2))
        return

    # Generate strategies
    result = recommend_strategies(validated)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
