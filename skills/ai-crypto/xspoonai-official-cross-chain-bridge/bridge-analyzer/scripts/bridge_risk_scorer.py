#!/usr/bin/env python3
"""
Bridge Risk Scorer
Comprehensive risk scoring for cross-chain bridge protocols using
real-time metrics from DeFiLlama and a curated security intelligence
database covering exploits, audits, and design classifications.

Risk scoring scale: 0-10
  SAFE     (0-1): No significant risks, strong track record
  LOW      (2-3): Minor concerns, generally safe
  MEDIUM   (4-5): Proceed with caution
  HIGH     (6-7): Significant risks, not recommended
  CRITICAL (8-10): Known exploits or compromised, avoid

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

# --- Curated Security Database ---

BRIDGE_SECURITY: Dict[str, Dict[str, Any]] = {
    "Multichain": {
        "exploits": [
            {"date": "2023-07", "amount": 126000000, "type": "exploit",
             "detail": "Infrastructure exploit, CEO arrested, funds unrecoverable"}
        ],
        "audits": [],
        "status": "compromised",
        "risk_modifier": 5,
    },
    "Ronin": {
        "exploits": [
            {"date": "2022-03", "amount": 624000000, "type": "hack",
             "detail": "Validator key compromise via social engineering"}
        ],
        "audits": [],
        "status": "recovered",
        "risk_modifier": 2,
    },
    "Wormhole": {
        "exploits": [
            {"date": "2022-02", "amount": 320000000, "type": "hack",
             "detail": "Signature verification bypass in smart contract"}
        ],
        "audits": ["Neodyme", "Kudelski"],
        "status": "recovered",
        "risk_modifier": 2,
    },
    "Nomad": {
        "exploits": [
            {"date": "2022-08", "amount": 190000000, "type": "exploit",
             "detail": "Initialization bug allowed anyone to drain funds"}
        ],
        "audits": ["Quantstamp"],
        "status": "compromised",
        "risk_modifier": 4,
    },
    "Harmony": {
        "exploits": [
            {"date": "2022-06", "amount": 100000000, "type": "hack",
             "detail": "Validator key compromise, 2-of-5 multisig"}
        ],
        "audits": [],
        "status": "compromised",
        "risk_modifier": 4,
    },
    "Stargate": {
        "exploits": [],
        "audits": ["Quantstamp", "Zokyo"],
        "status": "active",
        "risk_modifier": 0,
    },
    "Across": {
        "exploits": [],
        "audits": ["OpenZeppelin"],
        "status": "active",
        "risk_modifier": 0,
    },
    "Hop": {
        "exploits": [],
        "audits": ["OpenZeppelin"],
        "status": "active",
        "risk_modifier": 0,
    },
    "Celer": {
        "exploits": [
            {"date": "2022-08", "amount": 240000, "type": "exploit",
             "detail": "DNS hijack on cBridge front-end"}
        ],
        "audits": ["CertiK", "SlowMist"],
        "status": "active",
        "risk_modifier": 1,
    },
    "Synapse": {
        "exploits": [],
        "audits": ["Halborn"],
        "status": "active",
        "risk_modifier": 0,
    },
    "Orbiter": {
        "exploits": [],
        "audits": [],
        "status": "active",
        "risk_modifier": 0,
    },
    "Connext": {
        "exploits": [],
        "audits": ["Consensys Diligence"],
        "status": "active",
        "risk_modifier": 0,
    },
    "deBridge": {
        "exploits": [],
        "audits": ["Halborn", "Neodyme"],
        "status": "active",
        "risk_modifier": 0,
    },
    "LayerZero": {
        "exploits": [],
        "audits": ["Zellic", "Trail of Bits"],
        "status": "active",
        "risk_modifier": 0,
    },
}

# --- Bridge Design Type Classification ---

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

# Design type risk scores (0-10 contribution, weighted at 15%)
DESIGN_RISK: Dict[str, float] = {
    "optimistic-relay": 2.0,
    "liquidity-pool": 3.0,
    "maker-model": 2.5,
    "message-passing": 3.5,
    "lock-and-mint": 5.0,
    "validator-set": 4.0,
    "unknown": 5.0,
}

# Risk factor weights (must sum to 1.0)
WEIGHT_VOLUME = 0.25
WEIGHT_CHAINS = 0.15
WEIGHT_SECURITY = 0.30
WEIGHT_DESIGN = 0.15
WEIGHT_AUDIT = 0.15


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


def _match_bridge(bridge_data: Dict[str, Any], search_name: str) -> bool:
    """Case-insensitive, partial match for bridge names."""
    search_lower = search_name.strip().lower()
    name = bridge_data.get("name", "").lower()
    display_name = bridge_data.get("displayName", "").lower()
    return (
        search_lower in name
        or search_lower in display_name
        or name in search_lower
        or display_name in search_lower
    )


def _find_security_entry(bridge_name: str) -> Optional[Dict[str, Any]]:
    """Find security database entry for a bridge (fuzzy match).

    Args:
        bridge_name: Bridge name from DeFiLlama.

    Returns:
        Security database entry or None.
    """
    name_lower = bridge_name.lower()
    for key, entry in BRIDGE_SECURITY.items():
        if key.lower() in name_lower or name_lower in key.lower():
            return entry
    return None


def _find_design_type(bridge_name: str) -> str:
    """Find bridge design type from curated database.

    Args:
        bridge_name: Bridge name from DeFiLlama.

    Returns:
        Design type string.
    """
    name_lower = bridge_name.lower()
    for key, design in BRIDGE_DESIGN.items():
        if key.lower() in name_lower or name_lower in key.lower():
            return design
    return "unknown"


def _score_volume(volume_24h: float, all_volumes: List[float]) -> float:
    """Score bridge volume relative to all bridges (0-10, lower is safer).

    High volume bridges are more battle-tested and liquid.

    Args:
        volume_24h: Bridge's 24h volume.
        all_volumes: List of all bridge 24h volumes for percentile calc.

    Returns:
        Volume risk score (0-10).
    """
    if not all_volumes or max(all_volumes) == 0:
        return 5.0

    # Sort volumes to find percentile
    sorted_vols = sorted(all_volumes)
    total = len(sorted_vols)
    rank = 0
    for i, v in enumerate(sorted_vols):
        if volume_24h >= v:
            rank = i + 1

    percentile = rank / total

    # Higher percentile = higher volume = lower risk
    if percentile >= 0.9:
        return 0.5  # Top 10% -- very battle-tested
    elif percentile >= 0.75:
        return 1.5
    elif percentile >= 0.5:
        return 3.0
    elif percentile >= 0.25:
        return 5.0
    elif percentile >= 0.1:
        return 6.5
    else:
        return 8.0  # Bottom 10% -- very low volume


def _score_chains(chains_count: int) -> float:
    """Score chain coverage (0-10, balanced view).

    More chains = more established, but also more attack surface.

    Args:
        chains_count: Number of supported chains.

    Returns:
        Chain coverage risk score (0-10).
    """
    if chains_count >= 10:
        return 2.0  # Well-established
    elif chains_count >= 7:
        return 2.5
    elif chains_count >= 5:
        return 3.0
    elif chains_count >= 3:
        return 4.0
    elif chains_count >= 2:
        return 5.0
    else:
        return 7.0  # Single chain bridge -- limited


def _score_security(security_entry: Optional[Dict[str, Any]]) -> Tuple[float, Dict[str, Any]]:
    """Score based on security history (0-10, lower is safer).

    Args:
        security_entry: Entry from BRIDGE_SECURITY database.

    Returns:
        Tuple of (risk score, details dict).
    """
    if security_entry is None:
        # Unknown bridge -- moderate risk due to lack of data
        return 4.0, {
            "exploits": [],
            "status": "unknown",
            "note": "No security data available in curated database",
        }

    status = security_entry.get("status", "unknown")
    exploits = security_entry.get("exploits", [])
    risk_modifier = security_entry.get("risk_modifier", 0)

    if status == "compromised":
        return 10.0, {
            "exploits": exploits,
            "status": status,
            "note": "Bridge is compromised -- do not use",
        }

    # Base score from exploits
    base = 0.0
    if exploits:
        total_lost = sum(e.get("amount", 0) for e in exploits)
        if total_lost > 100_000_000:
            base = 6.0
        elif total_lost > 10_000_000:
            base = 5.0
        elif total_lost > 1_000_000:
            base = 4.0
        elif total_lost > 0:
            base = 2.0

    # Apply risk modifier (capped at 10)
    score = min(base + risk_modifier, 10.0)

    details: Dict[str, Any] = {
        "exploits": exploits,
        "status": status,
        "total_lost": sum(e.get("amount", 0) for e in exploits),
    }

    if status == "recovered":
        details["note"] = "Bridge recovered from exploit but history remains a risk factor"

    return score, details


def _score_design(design_type: str) -> float:
    """Score based on bridge design type (0-10).

    Args:
        design_type: Bridge design classification.

    Returns:
        Design risk score.
    """
    return DESIGN_RISK.get(design_type, 5.0)


def _score_audit(security_entry: Optional[Dict[str, Any]]) -> float:
    """Score based on audit status (0-10, lower is safer).

    Args:
        security_entry: Entry from BRIDGE_SECURITY database.

    Returns:
        Audit risk score.
    """
    if security_entry is None:
        return 6.0  # Unknown -- no audit data

    audits = security_entry.get("audits", [])

    if len(audits) >= 2:
        return 0.5  # Multiple reputable audits
    elif len(audits) == 1:
        return 2.0  # Single audit
    else:
        return 5.0  # No known audits


def _classify_risk(score: float) -> str:
    """Classify risk score into a named level.

    Args:
        score: Numeric risk score 0-10.

    Returns:
        Risk level string.
    """
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


def _generate_recommendation(
    risk_level: str,
    bridge_name: str,
    security_entry: Optional[Dict[str, Any]],
    design_type: str,
) -> str:
    """Generate a human-readable recommendation.

    Args:
        risk_level: Classified risk level.
        bridge_name: Name of the bridge.
        security_entry: Security database entry.
        design_type: Bridge design type.

    Returns:
        Recommendation string.
    """
    if risk_level == "CRITICAL":
        status = "compromised" if security_entry else "unknown"
        if security_entry and security_entry.get("status") == "compromised":
            return f"AVOID: {bridge_name} is compromised. Do not use this bridge."
        return f"CRITICAL RISK: {bridge_name} has severe risk factors. Not recommended."

    if risk_level == "HIGH":
        return (
            f"HIGH RISK: {bridge_name} has significant risk factors. "
            "Not recommended for large transfers."
        )

    if risk_level == "MEDIUM":
        return (
            f"MODERATE: {bridge_name} has some risk factors. "
            "Proceed with caution and limit exposure."
        )

    if risk_level == "LOW":
        audits = []
        if security_entry:
            audits = security_entry.get("audits", [])
        audit_str = f" Audited by {', '.join(audits)}." if audits else ""
        return (
            f"Low risk. {bridge_name} ({design_type}) has a reasonable track record.{audit_str}"
        )

    # SAFE
    audits = []
    if security_entry:
        audits = security_entry.get("audits", [])
    audit_str = f" Audited by {', '.join(audits)}." if audits else ""
    return (
        f"Low risk. {bridge_name} is battle-tested with high volume "
        f"and clean security record.{audit_str}"
    )


def score_bridge(
    bridge: Dict[str, Any],
    all_volumes: List[float],
) -> Dict[str, Any]:
    """Calculate comprehensive risk score for a bridge.

    Args:
        bridge: Bridge data from DeFiLlama API.
        all_volumes: List of all bridge 24h volumes for comparison.

    Returns:
        Complete risk assessment dictionary.
    """
    name = bridge.get("name", "Unknown")
    display_name = bridge.get("displayName", name)
    volume_24h = float(bridge.get("volumePrevDay", 0) or 0)
    chains = bridge.get("chains", [])

    security_entry = _find_security_entry(name)
    design_type = _find_design_type(name)

    # Calculate individual scores
    vol_score = _score_volume(volume_24h, all_volumes)
    chain_score = _score_chains(len(chains))
    sec_score, sec_details = _score_security(security_entry)
    design_score = _score_design(design_type)
    audit_score = _score_audit(security_entry)

    # Weighted composite score
    composite = (
        vol_score * WEIGHT_VOLUME
        + chain_score * WEIGHT_CHAINS
        + sec_score * WEIGHT_SECURITY
        + design_score * WEIGHT_DESIGN
        + audit_score * WEIGHT_AUDIT
    )
    composite = round(min(composite, 10.0), 1)

    risk_level = _classify_risk(composite)
    recommendation = _generate_recommendation(
        risk_level, display_name, security_entry, design_type
    )

    return {
        "bridge": display_name,
        "bridge_id": bridge.get("id"),
        "risk_score": composite,
        "risk_level": risk_level,
        "breakdown": {
            "volume_score": round(vol_score, 1),
            "chain_coverage_score": round(chain_score, 1),
            "security_score": round(sec_score, 1),
            "design_score": round(design_score, 1),
            "audit_score": round(audit_score, 1),
        },
        "weights": {
            "volume": WEIGHT_VOLUME,
            "chain_coverage": WEIGHT_CHAINS,
            "security": WEIGHT_SECURITY,
            "design": WEIGHT_DESIGN,
            "audit": WEIGHT_AUDIT,
        },
        "details": {
            "volume_24h": round(volume_24h, 2),
            "chains_count": len(chains),
            "chains": sorted(chains),
            "design_type": design_type,
            "exploits": sec_details.get("exploits", []),
            "audits": security_entry.get("audits", []) if security_entry else [],
            "status": security_entry.get("status", "unknown") if security_entry else "unknown",
        },
        "recommendation": recommendation,
    }


def validate_input(data: Dict[str, Any]) -> Optional[str]:
    """Validate input parameters.

    Args:
        data: Parsed input JSON.

    Returns:
        Error message or None if valid.
    """
    has_name = "bridge_name" in data
    has_top = "top" in data

    if not has_name and not has_top:
        return (
            "Missing required parameter. Provide 'bridge_name' (string) "
            "or 'top' (number) for top N bridges."
        )

    if has_name:
        if not isinstance(data["bridge_name"], str) or not data["bridge_name"].strip():
            return "'bridge_name' must be a non-empty string."

    if has_top:
        try:
            top = int(data["top"])
            if top < 1 or top > 30:
                return "'top' must be between 1 and 30."
        except (ValueError, TypeError):
            return "'top' must be a valid integer."

    return None


def main() -> None:
    """Main entry point. Reads JSON from stdin and outputs risk scores."""
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

    # Fetch bridge data
    api_data = _fetch_json(BRIDGES_API)
    all_bridges = api_data.get("bridges", [])

    if not all_bridges:
        _error_exit("No bridge data returned from DeFiLlama API.")
        return

    all_volumes = [float(b.get("volumePrevDay", 0) or 0) for b in all_bridges]

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    if "bridge_name" in data:
        # Score a specific bridge
        search_name = data["bridge_name"]
        matched = None
        for bridge in all_bridges:
            if _match_bridge(bridge, search_name):
                matched = bridge
                break

        if not matched:
            _error_exit(f"Bridge '{search_name}' not found in DeFiLlama data.")
            return

        result = score_bridge(matched, all_volumes)
        result["timestamp"] = timestamp

        print(json.dumps({"success": True, "data": result}, indent=2))

    else:
        # Score top N bridges
        top_n = int(data["top"])
        sorted_bridges = sorted(
            all_bridges,
            key=lambda b: float(b.get("volumePrevDay", 0) or 0),
            reverse=True,
        )[:top_n]

        results = []
        for bridge in sorted_bridges:
            results.append(score_bridge(bridge, all_volumes))

        output = {
            "success": True,
            "data": {
                "bridges": results,
                "total_scored": len(results),
                "scoring_method": "weighted_composite",
                "timestamp": timestamp,
            },
        }
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
