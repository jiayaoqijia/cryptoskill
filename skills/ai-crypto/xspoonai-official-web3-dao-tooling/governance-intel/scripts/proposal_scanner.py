#!/usr/bin/env python3
"""
Proposal Scanner — Scan active and recent governance proposals across major DAOs.

Uses the Snapshot GraphQL API (free, public, no API key required).

Input (JSON via stdin):
    {
        "space_id": "aave.eth",       // Optional: specific space to scan
        "top_daos": true,             // Optional: scan all 12 major DAOs
        "state": "active",            // Optional: filter by state (active/closed/pending)
        "limit": 10                   // Optional: max proposals per space (default 10)
    }

Output (JSON via stdout):
    {
        "status": "success",
        "proposals": [...],
        "summary": { "total": N, "active": N, "closed": N, "pending": N }
    }
"""

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

SNAPSHOT_API = "https://hub.snapshot.org/graphql"

TOP_DAOS: List[str] = [
    "aave.eth",
    "uniswapgovernance.eth",
    "ens.eth",
    "gitcoindao.eth",
    "safe.eth",
    "arbitrumfoundation.eth",
    "opcollective.eth",
    "lido-snapshot.eth",
    "balancer.eth",
    "curve.eth",
    "sushigov.eth",
    "compound-governance.eth",
]

PROPOSALS_QUERY = """
query Proposals($space: String!, $state: String, $first: Int) {
  proposals(
    where: { space: $space, state: $state }
    first: $first
    orderBy: "created"
    orderDirection: desc
  ) {
    id
    title
    body
    choices
    start
    end
    state
    scores
    scores_total
    votes
    quorum
    author
    space {
      id
      name
      members
    }
  }
}
"""


def _graphql_query(query: str, variables: Optional[Dict] = None, retries: int = 3) -> Dict[str, Any]:
    """Execute a GraphQL query against Snapshot Hub with retry logic."""
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "SpoonOS-GovernanceIntel/1.0",
    }

    last_error: Optional[Exception] = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                SNAPSHOT_API,
                data=payload,
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                if "errors" in data:
                    return {"error": data["errors"][0].get("message", "GraphQL error")}
                return data
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 429:
                time.sleep(2 ** attempt)
                continue
            break
        except (urllib.error.URLError, OSError) as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(1.5 ** attempt)
                continue
            break

    return {"error": f"API request failed after {retries} attempts: {last_error}"}


def _ts_to_iso(ts: int) -> str:
    """Convert UNIX timestamp to ISO 8601 string."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _time_remaining(end_ts: int) -> str:
    """Calculate human-readable time remaining from now until end timestamp."""
    now = int(time.time())
    diff = end_ts - now
    if diff <= 0:
        return "ended"
    days = diff // 86400
    hours = (diff % 86400) // 3600
    minutes = (diff % 3600) // 60
    parts: List[str] = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 and days == 0:
        parts.append(f"{minutes}m")
    return " ".join(parts) if parts else "<1m"


def _shorten_address(addr: str) -> str:
    """Shorten an Ethereum address for display."""
    if not addr or len(addr) < 10:
        return addr
    return f"{addr[:6]}...{addr[-4:]}"


def _format_proposal(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Format a raw Snapshot proposal into a clean output object."""
    scores = raw.get("scores") or []
    scores_total = raw.get("scores_total") or 0
    choices = raw.get("choices") or []
    quorum = raw.get("quorum") or 0
    state = raw.get("state", "unknown")
    end_ts = raw.get("end", 0)

    # Determine leading choice
    leading_choice = ""
    leading_pct = 0.0
    if scores and scores_total > 0:
        max_idx = 0
        max_score = scores[0]
        for i, s in enumerate(scores):
            if s > max_score:
                max_score = s
                max_idx = i
        if max_idx < len(choices):
            leading_choice = choices[max_idx]
        leading_pct = round((max_score / scores_total) * 100, 1) if scores_total > 0 else 0.0

    # Quorum check
    quorum_reached = scores_total >= quorum if quorum > 0 else None

    # Score breakdown per choice
    score_breakdown = {}
    for i, choice in enumerate(choices):
        if i < len(scores):
            pct = round((scores[i] / scores_total) * 100, 1) if scores_total > 0 else 0.0
            score_breakdown[choice] = {"vp": round(scores[i], 2), "pct": pct}

    space_info = raw.get("space") or {}

    result: Dict[str, Any] = {
        "id": raw.get("id", ""),
        "title": raw.get("title", "Untitled"),
        "space": space_info.get("id", ""),
        "space_name": space_info.get("name", ""),
        "state": state,
        "author": _shorten_address(raw.get("author", "")),
        "start": _ts_to_iso(raw.get("start", 0)),
        "end": _ts_to_iso(end_ts),
        "votes": raw.get("votes", 0),
        "scores_total": round(scores_total, 2),
        "choices": choices,
        "scores": [round(s, 2) for s in scores],
        "score_breakdown": score_breakdown,
        "leading_choice": leading_choice,
        "leading_pct": leading_pct,
    }

    if quorum > 0:
        result["quorum"] = round(quorum, 2)
        result["quorum_reached"] = quorum_reached

    if state == "active":
        result["time_remaining"] = _time_remaining(end_ts)

    return result


def scan_space(space_id: str, state: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
    """Scan proposals for a single Snapshot space."""
    variables: Dict[str, Any] = {"space": space_id, "first": min(limit, 100)}
    if state:
        variables["state"] = state

    response = _graphql_query(PROPOSALS_QUERY, variables)

    if "error" in response:
        return {
            "status": "error",
            "space": space_id,
            "error": response["error"],
            "details": f"Could not fetch proposals for '{space_id}'. Verify the space ID on snapshot.org.",
        }

    raw_proposals = (response.get("data") or {}).get("proposals") or []

    proposals = [_format_proposal(p) for p in raw_proposals]

    # Summary counts
    state_counts = {"active": 0, "closed": 0, "pending": 0}
    for p in proposals:
        s = p.get("state", "")
        if s in state_counts:
            state_counts[s] += 1

    return {
        "status": "success",
        "space": space_id,
        "proposals": proposals,
        "summary": {
            "total": len(proposals),
            "active": state_counts["active"],
            "closed": state_counts["closed"],
            "pending": state_counts["pending"],
        },
    }


def scan_top_daos(state: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
    """Scan proposals across all top DAOs."""
    all_proposals: List[Dict[str, Any]] = []
    space_summaries: List[Dict[str, Any]] = []
    errors: List[str] = []

    for space_id in TOP_DAOS:
        result = scan_space(space_id, state=state, limit=limit)
        if result["status"] == "success":
            proposals = result.get("proposals", [])
            all_proposals.extend(proposals)
            active_count = sum(1 for p in proposals if p.get("state") == "active")
            space_summaries.append({
                "space": space_id,
                "total": len(proposals),
                "active": active_count,
            })
        else:
            errors.append(f"{space_id}: {result.get('error', 'unknown error')}")

        # Small delay to be respectful to the API
        time.sleep(0.3)

    # Sort all proposals: active first, then by end date
    state_priority = {"active": 0, "pending": 1, "closed": 2}
    all_proposals.sort(key=lambda p: (
        state_priority.get(p.get("state", ""), 3),
        -p.get("scores_total", 0),
    ))

    total_active = sum(s["active"] for s in space_summaries)

    result: Dict[str, Any] = {
        "status": "success",
        "mode": "top_daos",
        "spaces_scanned": len(space_summaries),
        "proposals": all_proposals,
        "summary": {
            "total": len(all_proposals),
            "active": total_active,
            "closed": len(all_proposals) - total_active,
        },
        "space_breakdown": space_summaries,
    }

    if errors:
        result["warnings"] = errors

    return result


def validate_input(data: Dict[str, Any]) -> Optional[str]:
    """Validate the input parameters. Returns error message or None."""
    space_id = data.get("space_id")
    top_daos = data.get("top_daos", False)

    if not space_id and not top_daos:
        return (
            "Missing required input: provide either 'space_id' (e.g., 'aave.eth') "
            "or 'top_daos': true to scan major DAOs."
        )

    state = data.get("state")
    if state and state not in ("active", "closed", "pending"):
        return f"Invalid state '{state}'. Must be one of: active, closed, pending."

    limit = data.get("limit")
    if limit is not None:
        if not isinstance(limit, int) or limit < 1:
            return "Invalid limit: must be a positive integer."

    return None


def main() -> None:
    """Read JSON input from stdin, scan proposals, write JSON output to stdout."""
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            data: Dict[str, Any] = {}
        else:
            data = json.loads(raw_input)
    except json.JSONDecodeError as exc:
        json.dump({
            "status": "error",
            "error": f"Invalid JSON input: {exc}",
            "details": "Provide valid JSON via stdin.",
        }, sys.stdout, indent=2)
        return

    # Default to top_daos if no input
    if not data:
        data = {"top_daos": True, "state": "active"}

    error = validate_input(data)
    if error:
        json.dump({"status": "error", "error": error}, sys.stdout, indent=2)
        return

    state = data.get("state")
    limit = data.get("limit", 10)

    if data.get("top_daos"):
        result = scan_top_daos(state=state, limit=min(limit, 5))
    else:
        result = scan_space(data["space_id"], state=state, limit=limit)

    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
