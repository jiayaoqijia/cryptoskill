#!/usr/bin/env python3
"""
Route Optimizer
Find the optimal cross-chain bridge route between two blockchains.
Ranks available bridges by a composite score weighted by user priority
(cost, speed, or safety).

Uses the DeFiLlama Bridges API for real-time bridge data and a curated
security/design database for risk assessment.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional, Tuple

BRIDGES_API = "https://bridges.llama.fi/bridges?includeChains=true"

USER_AGENT = "BridgeAnalyzer/1.0"

# Chain name normalization mapping
CHAIN_ALIASES: Dict[str, str] = {
    "ethereum": "Ethereum",
    "eth": "Ethereum",
    "mainnet": "Ethereum",
    "arbitrum": "Arbitrum",
    "arb": "Arbitrum",
    "optimism": "Optimism",
    "op": "Optimism",
    "polygon": "Polygon",
    "matic": "Polygon",
    "bsc": "BSC",
    "bnb": "BSC",
    "binance": "BSC",
    "base": "Base",
    "avalanche": "Avalanche",
    "avax": "Avalanche",
    "solana": "Solana",
    "sol": "Solana",
    "fantom": "Fantom",
    "ftm": "Fantom",
    "gnosis": "Gnosis",
    "xdai": "Gnosis",
    "linea": "Linea",
    "zksync": "zkSync Era",
    "zksync era": "zkSync Era",
    "scroll": "Scroll",
    "mantle": "Mantle",
    "metis": "Metis",
    "celo": "Celo",
    "moonbeam": "Moonbeam",
    "kava": "Kava",
    "aurora": "Aurora",
    "harmony": "Harmony",
    "cronos": "Cronos",
    "polygon zkevm": "Polygon zkEVM",
    "era": "zkSync Era",
    "blast": "Blast",
    "manta": "Manta",
    "mode": "Mode",
}

# --- Curated Security Database ---

BRIDGE_SECURITY: Dict[str, Dict[str, Any]] = {
    "Multichain": {
        "exploits": [{"date": "2023-07", "amount": 126000000, "type": "exploit"}],
        "audits": [],
        "status": "compromised",
        "risk_modifier": 5,
    },
    "Ronin": {
        "exploits": [{"date": "2022-03", "amount": 624000000, "type": "hack"}],
        "audits": [],
        "status": "recovered",
        "risk_modifier": 2,
    },
    "Wormhole": {
        "exploits": [{"date": "2022-02", "amount": 320000000, "type": "hack"}],
        "audits": ["Neodyme", "Kudelski"],
        "status": "recovered",
        "risk_modifier": 2,
    },
    "Nomad": {
        "exploits": [{"date": "2022-08", "amount": 190000000, "type": "exploit"}],
        "audits": ["Quantstamp"],
        "status": "compromised",
        "risk_modifier": 4,
    },
    "Harmony": {
        "exploits": [{"date": "2022-06", "amount": 100000000, "type": "hack"}],
        "audits": [],
        "status": "compromised",
        "risk_modifier": 4,
    },
    "Stargate": {"exploits": [], "audits": ["Quantstamp", "Zokyo"], "status": "active", "risk_modifier": 0},
    "Across": {"exploits": [], "audits": ["OpenZeppelin"], "status": "active", "risk_modifier": 0},
    "Hop": {"exploits": [], "audits": ["OpenZeppelin"], "status": "active", "risk_modifier": 0},
    "Celer": {
        "exploits": [{"date": "2022-08", "amount": 240000, "type": "exploit"}],
        "audits": ["CertiK", "SlowMist"],
        "status": "active",
        "risk_modifier": 1,
    },
    "Synapse": {"exploits": [], "audits": ["Halborn"], "status": "active", "risk_modifier": 0},
    "Orbiter": {"exploits": [], "audits": [], "status": "active", "risk_modifier": 0},
    "Connext": {"exploits": [], "audits": ["Consensys Diligence"], "status": "active", "risk_modifier": 0},
    "deBridge": {"exploits": [], "audits": ["Halborn", "Neodyme"], "status": "active", "risk_modifier": 0},
    "LayerZero": {"exploits": [], "audits": ["Zellic", "Trail of Bits"], "status": "active", "risk_modifier": 0},
}

BRIDGE_DESIGN: Dict[str, str] = {
    "Stargate": "liquidity-pool",
    "Across": "optimistic-relay",
    "Hop": "liquidity-pool",
    "Wormhole": "message-passing",
    "LayerZero": "message-passing",
    "Celer": "liquidity-pool",
    "Synapse": "liquidity-pool",
    "Multichain": "lock-and-mint",
    "Connext": "liquidity-pool",
    "deBridge": "liquidity-pool",
    "Orbiter": "maker-model",
    "Ronin": "validator-set",
    "Nomad": "lock-and-mint",
    "Harmony": "validator-set",
}

# Design type attributes for scoring
DESIGN_ATTRIBUTES: Dict[str, Dict[str, Any]] = {
    "optimistic-relay": {"risk": 2.0, "speed": "fast", "cost_efficiency": "high"},
    "liquidity-pool": {"risk": 3.0, "speed": "fast", "cost_efficiency": "medium"},
    "maker-model": {"risk": 2.5, "speed": "fast", "cost_efficiency": "high"},
    "message-passing": {"risk": 3.5, "speed": "medium", "cost_efficiency": "medium"},
    "lock-and-mint": {"risk": 5.0, "speed": "medium", "cost_efficiency": "low"},
    "validator-set": {"risk": 4.0, "speed": "slow", "cost_efficiency": "low"},
    "unknown": {"risk": 5.0, "speed": "unknown", "cost_efficiency": "unknown"},
}

# Speed scoring (lower = faster = better for speed priority)
SPEED_SCORES: Dict[str, float] = {
    "fast": 1.0,
    "medium": 5.0,
    "slow": 8.0,
    "unknown": 6.0,
}

# Cost efficiency scoring (lower = cheaper = better for cost priority)
COST_SCORES: Dict[str, float] = {
    "high": 1.0,
    "medium": 4.0,
    "low": 7.0,
    "unknown": 5.0,
}

VALID_PRIORITIES = {"safety", "cost", "speed"}


def _fetch_json(url: str, max_retries: int = 3, timeout: int = 20) -> Dict[str, Any]:
    """Fetch JSON from URL with retry logic and 429 handling."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            _error_exit(f"HTTP error {e.code} fetching {url}")
        except urllib.error.URLError as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            _error_exit(f"URL error: {e.reason}")
        except Exception as e:
            _error_exit(f"Unexpected error: {str(e)}")
    _error_exit("Max retries exceeded")


def _error_exit(message: str) -> None:
    """Print error JSON and exit."""
    output = {
        "success": False,
        "error": message,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    print(json.dumps(output, indent=2))
    sys.exit(1)


def _normalize_chain(chain: str) -> str:
    """Normalize a chain name to DeFiLlama format."""
    lower = chain.strip().lower()
    if lower in CHAIN_ALIASES:
        return CHAIN_ALIASES[lower]
    return chain.strip().title()


def _find_security_entry(bridge_name: str) -> Optional[Dict[str, Any]]:
    """Find security database entry for a bridge (fuzzy match)."""
    name_lower = bridge_name.lower()
    for key, entry in BRIDGE_SECURITY.items():
        if key.lower() in name_lower or name_lower in key.lower():
            return entry
    return None


def _find_design_type(bridge_name: str) -> str:
    """Find bridge design type from curated database."""
    name_lower = bridge_name.lower()
    for key, design in BRIDGE_DESIGN.items():
        if key.lower() in name_lower or name_lower in key.lower():
            return design
    return "unknown"


def _compute_risk_score(bridge: Dict[str, Any], all_volumes: List[float]) -> float:
    """Compute a simplified risk score for route ranking.

    Args:
        bridge: Bridge data from DeFiLlama.
        all_volumes: All bridge volumes for percentile comparison.

    Returns:
        Risk score 0-10.
    """
    name = bridge.get("name", "Unknown")
    volume_24h = float(bridge.get("volumePrevDay", 0) or 0)
    chains_count = len(bridge.get("chains", []))

    security = _find_security_entry(name)
    design_type = _find_design_type(name)

    # Volume score
    if all_volumes and max(all_volumes) > 0:
        sorted_vols = sorted(all_volumes)
        rank = sum(1 for v in sorted_vols if volume_24h >= v)
        percentile = rank / len(sorted_vols)
        if percentile >= 0.9:
            vol_score = 0.5
        elif percentile >= 0.75:
            vol_score = 1.5
        elif percentile >= 0.5:
            vol_score = 3.0
        elif percentile >= 0.25:
            vol_score = 5.0
        else:
            vol_score = 7.0
    else:
        vol_score = 5.0

    # Security score
    sec_score = 4.0
    if security:
        if security.get("status") == "compromised":
            sec_score = 10.0
        elif security.get("exploits"):
            total_lost = sum(e.get("amount", 0) for e in security["exploits"])
            sec_score = min(3.0 + security.get("risk_modifier", 0), 10.0)
            if total_lost > 100_000_000:
                sec_score = max(sec_score, 6.0)
        else:
            sec_score = 0.5

    # Design score
    design_attrs = DESIGN_ATTRIBUTES.get(design_type, DESIGN_ATTRIBUTES["unknown"])
    design_score = design_attrs["risk"]

    # Audit score
    audit_score = 5.0
    if security:
        audits = security.get("audits", [])
        if len(audits) >= 2:
            audit_score = 0.5
        elif len(audits) == 1:
            audit_score = 2.0

    # Weighted composite
    composite = (
        vol_score * 0.25
        + sec_score * 0.35
        + design_score * 0.20
        + audit_score * 0.20
    )
    return round(min(composite, 10.0), 1)


def _classify_risk(score: float) -> str:
    """Classify risk score into a named level."""
    if score <= 1.0:
        return "SAFE"
    elif score <= 3.0:
        return "LOW"
    elif score <= 5.0:
        return "MEDIUM"
    elif score <= 7.0:
        return "HIGH"
    else:
        return "CRITICAL"


def _compute_composite_score(
    bridge: Dict[str, Any],
    risk_score: float,
    all_volumes: List[float],
    priority: str,
) -> Tuple[float, str]:
    """Compute a composite route score based on user priority.

    Returns a score 0-100 (higher is better) and a recommendation string.

    Args:
        bridge: Bridge data from DeFiLlama.
        risk_score: Pre-computed risk score.
        all_volumes: All volumes for comparison.
        priority: User priority (safety, cost, speed).

    Returns:
        Tuple of (composite score 0-100, recommendation text).
    """
    name = bridge.get("name", "Unknown")
    display_name = bridge.get("displayName", name)
    volume_24h = float(bridge.get("volumePrevDay", 0) or 0)
    design_type = _find_design_type(name)
    design_attrs = DESIGN_ATTRIBUTES.get(design_type, DESIGN_ATTRIBUTES["unknown"])

    # Safety score (invert risk: 0 risk = 100 safety)
    safety_score = max(0, (10.0 - risk_score) * 10.0)

    # Volume/liquidity score (higher volume = better cost/less slippage)
    if all_volumes and max(all_volumes) > 0:
        max_vol = max(all_volumes)
        liquidity_score = min((volume_24h / max_vol) * 100.0, 100.0)
    else:
        liquidity_score = 50.0

    # Speed score
    speed_raw = SPEED_SCORES.get(design_attrs["speed"], 6.0)
    speed_score = max(0, (10.0 - speed_raw) * 10.0)

    # Cost score
    cost_raw = COST_SCORES.get(design_attrs["cost_efficiency"], 5.0)
    cost_score = max(0, (10.0 - cost_raw) * 10.0)

    # Weight by priority
    if priority == "safety":
        composite = safety_score * 0.50 + liquidity_score * 0.25 + speed_score * 0.15 + cost_score * 0.10
        rec_focus = "safety"
    elif priority == "cost":
        composite = cost_score * 0.35 + liquidity_score * 0.30 + safety_score * 0.25 + speed_score * 0.10
        rec_focus = "cost efficiency"
    elif priority == "speed":
        composite = speed_score * 0.40 + safety_score * 0.25 + liquidity_score * 0.20 + cost_score * 0.15
        rec_focus = "speed"
    else:
        composite = safety_score * 0.40 + liquidity_score * 0.30 + speed_score * 0.15 + cost_score * 0.15
        rec_focus = "balanced"

    composite = round(min(composite, 100.0), 1)

    # Generate recommendation
    risk_level = _classify_risk(risk_score)
    if risk_level in ("CRITICAL", "HIGH"):
        recommendation = f"Not recommended -- {risk_level} risk level"
    elif composite >= 80:
        recommendation = f"Top pick for {rec_focus} -- {design_type} design with strong metrics"
    elif composite >= 60:
        recommendation = f"Good option for {rec_focus} -- solid {design_type} bridge"
    elif composite >= 40:
        recommendation = f"Acceptable for {rec_focus} -- some trade-offs with {design_type} design"
    else:
        recommendation = f"Below average for {rec_focus} -- consider alternatives"

    return composite, recommendation


def find_routes(
    all_bridges: List[Dict[str, Any]],
    source_chain: str,
    dest_chain: str,
    priority: str = "safety",
) -> Dict[str, Any]:
    """Find and rank bridge routes between two chains.

    Args:
        all_bridges: All bridge data from DeFiLlama.
        source_chain: Normalized source chain name.
        dest_chain: Normalized destination chain name.
        priority: Ranking priority (safety, cost, speed).

    Returns:
        Routes result dictionary.
    """
    all_volumes = [float(b.get("volumePrevDay", 0) or 0) for b in all_bridges]

    # Find bridges that support both chains
    candidates = []
    for bridge in all_bridges:
        chains = bridge.get("chains", [])
        chains_lower = [c.lower() for c in chains]
        if source_chain.lower() in chains_lower and dest_chain.lower() in chains_lower:
            candidates.append(bridge)

    if not candidates:
        return {
            "source_chain": source_chain,
            "destination_chain": dest_chain,
            "priority": priority,
            "routes": [],
            "total_routes": 0,
            "message": f"No bridges found supporting both {source_chain} and {dest_chain}.",
        }

    # Score and rank each candidate
    routes = []
    for bridge in candidates:
        name = bridge.get("name", "Unknown")
        display_name = bridge.get("displayName", name)
        volume_24h = float(bridge.get("volumePrevDay", 0) or 0)
        design_type = _find_design_type(name)
        risk_score = _compute_risk_score(bridge, all_volumes)
        risk_level = _classify_risk(risk_score)

        composite, recommendation = _compute_composite_score(
            bridge, risk_score, all_volumes, priority
        )

        security = _find_security_entry(name)
        audits = security.get("audits", []) if security else []
        status = security.get("status", "unknown") if security else "unknown"

        routes.append({
            "bridge": display_name,
            "bridge_id": bridge.get("id"),
            "design_type": design_type,
            "volume_24h": round(volume_24h, 2),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "composite_score": composite,
            "recommendation": recommendation,
            "audits": audits,
            "status": status,
        })

    # Sort by composite score descending (higher is better)
    routes.sort(key=lambda r: r["composite_score"], reverse=True)

    # Assign ranks
    for idx, route in enumerate(routes):
        route["rank"] = idx + 1

    return {
        "source_chain": source_chain,
        "destination_chain": dest_chain,
        "priority": priority,
        "routes": routes,
        "total_routes": len(routes),
    }


def validate_input(data: Dict[str, Any]) -> Optional[str]:
    """Validate input parameters.

    Args:
        data: Parsed input JSON.

    Returns:
        Error message or None if valid.
    """
    if "source_chain" not in data:
        return "Missing required parameter 'source_chain'."
    if "destination_chain" not in data:
        return "Missing required parameter 'destination_chain'."

    if not isinstance(data["source_chain"], str) or not data["source_chain"].strip():
        return "'source_chain' must be a non-empty string."
    if not isinstance(data["destination_chain"], str) or not data["destination_chain"].strip():
        return "'destination_chain' must be a non-empty string."

    source = _normalize_chain(data["source_chain"])
    dest = _normalize_chain(data["destination_chain"])
    if source.lower() == dest.lower():
        return "Source and destination chains must be different."

    priority = data.get("priority", "safety")
    if priority not in VALID_PRIORITIES:
        return f"'priority' must be one of: {', '.join(sorted(VALID_PRIORITIES))}."

    return None


def main() -> None:
    """Main entry point. Reads JSON from stdin and outputs optimized routes."""
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            _error_exit("No input provided. Send JSON via stdin.")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        _error_exit(f"Invalid JSON input: {str(e)}")
        return

    error = validate_input(data)
    if error:
        _error_exit(error)
        return

    source_chain = _normalize_chain(data["source_chain"])
    dest_chain = _normalize_chain(data["destination_chain"])
    priority = data.get("priority", "safety")

    # Fetch bridge data
    api_data = _fetch_json(BRIDGES_API)
    all_bridges = api_data.get("bridges", [])

    if not all_bridges:
        _error_exit("No bridge data returned from DeFiLlama API.")
        return

    result = find_routes(all_bridges, source_chain, dest_chain, priority)
    result["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    print(json.dumps({"success": True, "data": result}, indent=2))


if __name__ == "__main__":
    main()
