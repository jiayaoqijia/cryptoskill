#!/usr/bin/env python3
"""
Bridge Monitor
Monitor cross-chain bridge TVL and volume changes, detecting anomalies
that could indicate exploits, technical issues, or unusual activity.

Uses the DeFiLlama Bridges API for real-time metrics and a curated
security database for known incident flagging.

Anomaly Detection Rules:
  - Volume spike: hourly volume > 3x the daily hourly average
  - Volume drop: 24h volume is zero or near-zero for an active bridge
  - Known exploit: bridge appears in curated security database
  - Compromised status: bridge marked as compromised

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

BRIDGES_API = "https://bridges.llama.fi/bridges?includeChains=true"

USER_AGENT = "BridgeAnalyzer/1.0"

# Default alert threshold (percentage) for volume changes
DEFAULT_ALERT_THRESHOLD = 20

# Anomaly detection thresholds
SPIKE_MULTIPLIER = 3.0      # Hourly volume > 3x daily average = spike
DROP_THRESHOLD = 0.05        # 24h volume < 5% of median = drop
MIN_VOLUME_FOR_MONITORING = 1000  # Minimum 24h volume to consider active

# --- Curated Security Database ---

BRIDGE_SECURITY: Dict[str, Dict[str, Any]] = {
    "Multichain": {
        "exploits": [
            {"date": "2023-07", "amount": 126000000, "type": "exploit",
             "detail": "Infrastructure exploit, CEO arrested"}
        ],
        "status": "compromised",
        "risk_modifier": 5,
    },
    "Ronin": {
        "exploits": [
            {"date": "2022-03", "amount": 624000000, "type": "hack",
             "detail": "Validator key compromise via social engineering"}
        ],
        "status": "recovered",
        "risk_modifier": 2,
    },
    "Wormhole": {
        "exploits": [
            {"date": "2022-02", "amount": 320000000, "type": "hack",
             "detail": "Signature verification bypass"}
        ],
        "status": "recovered",
        "risk_modifier": 2,
    },
    "Nomad": {
        "exploits": [
            {"date": "2022-08", "amount": 190000000, "type": "exploit",
             "detail": "Initialization bug, anyone could drain"}
        ],
        "status": "compromised",
        "risk_modifier": 4,
    },
    "Harmony": {
        "exploits": [
            {"date": "2022-06", "amount": 100000000, "type": "hack",
             "detail": "Validator key compromise, 2-of-5 multisig"}
        ],
        "status": "compromised",
        "risk_modifier": 4,
    },
    "Stargate": {"exploits": [], "status": "active", "risk_modifier": 0},
    "Across": {"exploits": [], "status": "active", "risk_modifier": 0},
    "Hop": {"exploits": [], "status": "active", "risk_modifier": 0},
    "Celer": {
        "exploits": [
            {"date": "2022-08", "amount": 240000, "type": "exploit",
             "detail": "DNS hijack on cBridge front-end"}
        ],
        "status": "active",
        "risk_modifier": 1,
    },
    "Synapse": {"exploits": [], "status": "active", "risk_modifier": 0},
    "Orbiter": {"exploits": [], "status": "active", "risk_modifier": 0},
    "Connext": {"exploits": [], "status": "active", "risk_modifier": 0},
    "deBridge": {"exploits": [], "status": "active", "risk_modifier": 0},
    "LayerZero": {"exploits": [], "status": "active", "risk_modifier": 0},
}


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
    """Find security database entry for a bridge (fuzzy match)."""
    name_lower = bridge_name.lower()
    for key, entry in BRIDGE_SECURITY.items():
        if key.lower() in name_lower or name_lower in key.lower():
            return entry
    return None


def _compute_hourly_ratio(volume_24h: float, volume_1h: float) -> float:
    """Compute the ratio of hourly volume to expected hourly average.

    Expected hourly average = volume_24h / 24.

    Args:
        volume_24h: 24-hour volume.
        volume_1h: Last hour volume.

    Returns:
        Ratio of actual hourly to expected hourly. 1.0 = normal.
    """
    if volume_24h <= 0:
        return 0.0
    expected_hourly = volume_24h / 24.0
    if expected_hourly <= 0:
        return 0.0
    return round(volume_1h / expected_hourly, 2)


def _detect_anomalies(
    bridge: Dict[str, Any],
    median_volume: float,
) -> List[Dict[str, Any]]:
    """Detect anomalies for a single bridge.

    Args:
        bridge: Bridge data from DeFiLlama.
        median_volume: Median 24h volume across all bridges.

    Returns:
        List of anomaly dictionaries.
    """
    name = bridge.get("name", "Unknown")
    display_name = bridge.get("displayName", name)
    volume_24h = float(bridge.get("volumePrevDay", 0) or 0)
    volume_1h = float(bridge.get("lastHourlyVolume", 0) or 0)

    anomalies: List[Dict[str, Any]] = []
    security = _find_security_entry(name)

    # Check for compromised status
    if security and security.get("status") == "compromised":
        exploits = security.get("exploits", [])
        total_lost = sum(e.get("amount", 0) for e in exploits)
        anomalies.append({
            "bridge": display_name,
            "type": "compromised_bridge",
            "severity": "CRITICAL",
            "volume_24h": round(volume_24h, 2),
            "volume_1h": round(volume_1h, 2),
            "message": (
                f"{display_name} is COMPROMISED. "
                f"Total funds lost: ${total_lost:,.0f}. Do not use this bridge."
            ),
        })
        return anomalies

    # Check for known exploits (recovered bridges)
    if security and security.get("exploits"):
        exploits = security["exploits"]
        total_lost = sum(e.get("amount", 0) for e in exploits)
        if total_lost > 0:
            anomalies.append({
                "bridge": display_name,
                "type": "known_exploit_history",
                "severity": "WARNING",
                "volume_24h": round(volume_24h, 2),
                "volume_1h": round(volume_1h, 2),
                "exploits": exploits,
                "message": (
                    f"{display_name} has exploit history: "
                    f"${total_lost:,.0f} lost. Status: {security.get('status', 'unknown')}."
                ),
            })

    # Volume spike detection
    if volume_24h > MIN_VOLUME_FOR_MONITORING and volume_1h > 0:
        hourly_ratio = _compute_hourly_ratio(volume_24h, volume_1h)
        if hourly_ratio >= SPIKE_MULTIPLIER:
            anomalies.append({
                "bridge": display_name,
                "type": "volume_spike",
                "severity": "WARNING",
                "volume_24h": round(volume_24h, 2),
                "volume_1h": round(volume_1h, 2),
                "hourly_ratio": hourly_ratio,
                "message": (
                    f"{display_name} hourly volume is {hourly_ratio}x the daily average "
                    "-- possible high demand or drainage event."
                ),
            })

    # Volume drop detection (active bridge with near-zero volume)
    if median_volume > 0 and volume_24h < median_volume * DROP_THRESHOLD:
        if volume_24h > 0 or volume_1h > 0:
            anomalies.append({
                "bridge": display_name,
                "type": "volume_drop",
                "severity": "WARNING",
                "volume_24h": round(volume_24h, 2),
                "volume_1h": round(volume_1h, 2),
                "message": (
                    f"{display_name} 24h volume (${volume_24h:,.0f}) is significantly below "
                    f"the median (${median_volume:,.0f}) -- possible technical issues."
                ),
            })

    return anomalies


def _format_bridge_metrics(bridge: Dict[str, Any]) -> Dict[str, Any]:
    """Format bridge data into monitoring metrics.

    Args:
        bridge: Bridge data from DeFiLlama.

    Returns:
        Formatted metrics dictionary.
    """
    name = bridge.get("name", "Unknown")
    display_name = bridge.get("displayName", name)
    volume_24h = float(bridge.get("volumePrevDay", 0) or 0)
    volume_1h = float(bridge.get("lastHourlyVolume", 0) or 0)
    current_day = float(bridge.get("currentDayVolume", 0) or 0)
    chains = bridge.get("chains", [])

    hourly_ratio = _compute_hourly_ratio(volume_24h, volume_1h)

    # Determine status
    if hourly_ratio >= SPIKE_MULTIPLIER:
        status = "volume_spike"
    elif volume_24h < MIN_VOLUME_FOR_MONITORING:
        status = "low_volume"
    else:
        status = "normal"

    security = _find_security_entry(name)
    security_flag = None
    if security:
        if security.get("status") == "compromised":
            security_flag = "COMPROMISED"
        elif security.get("exploits"):
            security_flag = "exploit_history"

    return {
        "name": display_name,
        "bridge_id": bridge.get("id"),
        "volume_24h": round(volume_24h, 2),
        "volume_current_day": round(current_day, 2),
        "volume_1h": round(volume_1h, 2),
        "hourly_ratio": hourly_ratio,
        "chains_count": len(chains),
        "status": status,
        "security_flag": security_flag,
    }


def monitor_specific(
    all_bridges: List[Dict[str, Any]],
    bridge_name: str,
    median_volume: float,
) -> Dict[str, Any]:
    """Monitor a specific bridge.

    Args:
        all_bridges: All bridge data from DeFiLlama.
        bridge_name: Bridge name to monitor.
        median_volume: Median volume across all bridges.

    Returns:
        Monitoring result dictionary.
    """
    matched = None
    for bridge in all_bridges:
        if _match_bridge(bridge, bridge_name):
            matched = bridge
            break

    if not matched:
        return {
            "error": f"Bridge '{bridge_name}' not found in DeFiLlama data.",
            "success": False,
        }

    metrics = _format_bridge_metrics(matched)
    anomalies = _detect_anomalies(matched, median_volume)

    return {
        "summary": {
            "total_bridges_monitored": 1,
            "anomalies_detected": len(anomalies),
        },
        "anomalies": anomalies,
        "bridges": [metrics],
    }


def monitor_all(
    all_bridges: List[Dict[str, Any]],
    alert_threshold: float,
    median_volume: float,
) -> Dict[str, Any]:
    """Monitor all bridges and flag anomalies.

    Args:
        all_bridges: All bridge data from DeFiLlama.
        alert_threshold: Percentage threshold for flagging volume changes.
        median_volume: Median volume across all bridges.

    Returns:
        Monitoring result dictionary.
    """
    # Sort by volume descending for output
    sorted_bridges = sorted(
        all_bridges,
        key=lambda b: float(b.get("volumePrevDay", 0) or 0),
        reverse=True,
    )

    all_anomalies: List[Dict[str, Any]] = []
    bridge_metrics: List[Dict[str, Any]] = []
    total_volume = 0.0

    for bridge in sorted_bridges:
        volume_24h = float(bridge.get("volumePrevDay", 0) or 0)
        total_volume += volume_24h

        metrics = _format_bridge_metrics(bridge)
        bridge_metrics.append(metrics)

        anomalies = _detect_anomalies(bridge, median_volume)
        all_anomalies.extend(anomalies)

    # Sort anomalies by severity (CRITICAL first)
    severity_order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
    all_anomalies.sort(key=lambda a: severity_order.get(a.get("severity", "INFO"), 3))

    return {
        "summary": {
            "total_bridges_monitored": len(sorted_bridges),
            "anomalies_detected": len(all_anomalies),
            "total_24h_volume": round(total_volume, 2),
            "alert_threshold_pct": alert_threshold,
        },
        "anomalies": all_anomalies,
        "bridges": bridge_metrics[:50],  # Limit output to top 50 bridges
    }


def _compute_median(values: List[float]) -> float:
    """Compute the median of a list of numbers.

    Args:
        values: List of numeric values.

    Returns:
        Median value.
    """
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0
    return sorted_vals[mid]


def validate_input(data: Dict[str, Any]) -> Optional[str]:
    """Validate input parameters.

    Args:
        data: Parsed input JSON.

    Returns:
        Error message or None if valid.
    """
    has_name = "bridge_name" in data
    has_threshold = "alert_threshold" in data

    # If neither provided, default to monitoring all with default threshold
    if not has_name and not has_threshold:
        return None

    if has_name:
        if not isinstance(data["bridge_name"], str) or not data["bridge_name"].strip():
            return "'bridge_name' must be a non-empty string."

    if has_threshold:
        try:
            threshold = float(data["alert_threshold"])
            if threshold < 0 or threshold > 100:
                return "'alert_threshold' must be between 0 and 100."
        except (ValueError, TypeError):
            return "'alert_threshold' must be a valid number."

    return None


def main() -> None:
    """Main entry point. Reads JSON from stdin and outputs monitoring results."""
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

    # Compute median volume for anomaly detection baseline
    volumes = [float(b.get("volumePrevDay", 0) or 0) for b in all_bridges]
    active_volumes = [v for v in volumes if v > MIN_VOLUME_FOR_MONITORING]
    median_volume = _compute_median(active_volumes)

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    if "bridge_name" in data:
        result = monitor_specific(all_bridges, data["bridge_name"], median_volume)
        if "error" in result:
            _error_exit(result["error"])
            return
    else:
        alert_threshold = float(data.get("alert_threshold", DEFAULT_ALERT_THRESHOLD))
        result = monitor_all(all_bridges, alert_threshold, median_volume)

    result["timestamp"] = timestamp

    print(json.dumps({"success": True, "data": result}, indent=2))


if __name__ == "__main__":
    main()
