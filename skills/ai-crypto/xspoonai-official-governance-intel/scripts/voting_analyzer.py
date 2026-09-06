#!/usr/bin/env python3
"""
Voting Analyzer — Analyze voting patterns, whale influence, and outcome predictability.

Uses the Snapshot GraphQL API (free, public, no API key required).

Input (JSON via stdin):
    {
        "proposal_id": "0xabc...",           // Direct proposal ID
        // OR
        "space_id": "aave.eth",              // Space ID + proposal_index
        "proposal_index": 0                  // 0 = most recent
    }

Output (JSON via stdout):
    {
        "status": "success",
        "proposal": {...},
        "vote_distribution": {...},
        "whale_analysis": {...},
        "participation": {...},
        "concentration": {...},
        "timing": {...}
    }
"""

import json
import math
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

SNAPSHOT_API = "https://hub.snapshot.org/graphql"

PROPOSALS_QUERY = """
query Proposals($space: String!, $first: Int) {
  proposals(
    where: { space: $space }
    first: $first
    orderBy: "created"
    orderDirection: desc
  ) {
    id
    title
    choices
    start
    end
    state
    scores
    scores_total
    votes
    quorum
    space { id name members }
  }
}
"""

VOTES_QUERY = """
query Votes($proposal: String!, $first: Int, $skip: Int) {
  votes(
    where: { proposal: $proposal }
    first: $first
    skip: $skip
    orderBy: "vp"
    orderDirection: desc
  ) {
    voter
    choice
    vp
    created
  }
}
"""

PROPOSAL_BY_ID_QUERY = """
query Proposal($id: String!) {
  proposal(id: $id) {
    id
    title
    choices
    start
    end
    state
    scores
    scores_total
    votes
    quorum
    space { id name members }
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


def _shorten_address(addr: str) -> str:
    """Shorten an Ethereum address for display."""
    if not addr or len(addr) < 10:
        return addr
    return f"{addr[:6]}...{addr[-4:]}"


def _ts_to_iso(ts: int) -> str:
    """Convert UNIX timestamp to ISO 8601 string."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_proposal_id(space_id: str, proposal_index: int) -> Tuple[Optional[str], Optional[Dict]]:
    """Resolve a proposal ID from space_id and index."""
    resp = _graphql_query(PROPOSALS_QUERY, {
        "space": space_id,
        "first": proposal_index + 5,
    })

    if "error" in resp:
        return None, {"status": "error", "error": resp["error"]}

    proposals = (resp.get("data") or {}).get("proposals") or []
    if proposal_index >= len(proposals):
        return None, {
            "status": "error",
            "error": f"Proposal index {proposal_index} out of range. "
                     f"Space '{space_id}' has {len(proposals)} recent proposals.",
        }

    return proposals[proposal_index]["id"], None


def _fetch_proposal(proposal_id: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """Fetch proposal details by ID."""
    resp = _graphql_query(PROPOSAL_BY_ID_QUERY, {"id": proposal_id})
    if "error" in resp:
        return None, {"status": "error", "error": resp["error"]}

    proposal = (resp.get("data") or {}).get("proposal")
    if not proposal:
        return None, {
            "status": "error",
            "error": f"Proposal '{proposal_id}' not found.",
            "details": "Verify the proposal ID on snapshot.org.",
        }

    return proposal, None


def _fetch_all_votes(proposal_id: str, max_votes: int = 1000) -> List[Dict[str, Any]]:
    """Fetch all votes for a proposal with pagination."""
    all_votes: List[Dict[str, Any]] = []
    skip = 0
    page_size = 1000

    while len(all_votes) < max_votes:
        resp = _graphql_query(VOTES_QUERY, {
            "proposal": proposal_id,
            "first": min(page_size, max_votes - len(all_votes)),
            "skip": skip,
        })

        if "error" in resp:
            break

        votes = (resp.get("data") or {}).get("votes") or []
        if not votes:
            break

        all_votes.extend(votes)
        skip += len(votes)

        if len(votes) < page_size:
            break

        time.sleep(0.3)

    return all_votes


def _calculate_gini(values: List[float]) -> float:
    """Calculate the Gini coefficient for a list of values."""
    if not values or len(values) < 2:
        return 0.0

    sorted_vals = sorted(values)
    n = len(sorted_vals)
    total = sum(sorted_vals)

    if total == 0:
        return 0.0

    cumulative_sum = 0.0
    weighted_sum = 0.0
    for i, val in enumerate(sorted_vals):
        cumulative_sum += val
        weighted_sum += (2 * (i + 1) - n - 1) * val

    gini = weighted_sum / (n * total)
    return round(max(0.0, min(1.0, gini)), 4)


def _analyze_vote_distribution(
    votes: List[Dict[str, Any]], choices: List[str]
) -> Dict[str, Any]:
    """Analyze vote distribution across choices."""
    choice_votes: Dict[str, Dict[str, Any]] = {}
    for choice in choices:
        choice_votes[choice] = {"count": 0, "vp": 0.0}

    total_vp = 0.0

    for vote in votes:
        vp = vote.get("vp", 0)
        total_vp += vp
        choice_idx = vote.get("choice")

        # Snapshot uses 1-based choice indexing for single-choice
        if isinstance(choice_idx, int) and 1 <= choice_idx <= len(choices):
            choice_name = choices[choice_idx - 1]
            choice_votes[choice_name]["count"] += 1
            choice_votes[choice_name]["vp"] += vp
        elif isinstance(choice_idx, dict):
            # Weighted voting: choice is a dict like {1: 0.6, 2: 0.4}
            for idx_str, weight in choice_idx.items():
                idx = int(idx_str)
                if 1 <= idx <= len(choices):
                    choice_name = choices[idx - 1]
                    choice_votes[choice_name]["count"] += 1
                    choice_votes[choice_name]["vp"] += vp * weight

    distribution = {}
    for choice_name, data in choice_votes.items():
        pct = round((data["vp"] / total_vp) * 100, 1) if total_vp > 0 else 0.0
        distribution[choice_name] = {
            "votes": data["count"],
            "vp": round(data["vp"], 2),
            "pct": pct,
        }

    return distribution


def _analyze_whales(votes: List[Dict[str, Any]], choices: List[str], top_n: int = 10) -> Dict[str, Any]:
    """Analyze whale influence — top voters by voting power."""
    if not votes:
        return {
            "top_10_share_pct": 0.0,
            "whale_dominant": False,
            "top_voters": [],
        }

    # Votes are already sorted by VP (desc) from the query
    total_vp = sum(v.get("vp", 0) for v in votes)
    top_votes = votes[:top_n]
    top_vp = sum(v.get("vp", 0) for v in top_votes)
    top_share = round((top_vp / total_vp) * 100, 1) if total_vp > 0 else 0.0

    top_voters = []
    for v in top_votes:
        choice_idx = v.get("choice")
        choice_name = "Unknown"
        if isinstance(choice_idx, int) and 1 <= choice_idx <= len(choices):
            choice_name = choices[choice_idx - 1]
        elif isinstance(choice_idx, dict):
            # Weighted: show the highest-weighted choice
            max_choice = max(choice_idx.items(), key=lambda x: x[1])
            idx = int(max_choice[0])
            if 1 <= idx <= len(choices):
                choice_name = f"{choices[idx - 1]} (weighted)"

        vp = v.get("vp", 0)
        pct = round((vp / total_vp) * 100, 1) if total_vp > 0 else 0.0

        top_voters.append({
            "voter": _shorten_address(v.get("voter", "")),
            "voter_full": v.get("voter", ""),
            "vp": round(vp, 2),
            "choice": choice_name,
            "pct_of_total": pct,
        })

    return {
        "top_10_share_pct": top_share,
        "whale_dominant": top_share > 50.0,
        "top_voters": top_voters,
    }


def _analyze_concentration(votes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate concentration metrics including Gini coefficient."""
    vp_values = [v.get("vp", 0) for v in votes]

    if not vp_values:
        return {
            "gini_coefficient": 0.0,
            "top_10_pct": 0.0,
            "top_25_pct": 0.0,
            "total_voters": 0,
        }

    total_vp = sum(vp_values)
    sorted_vp = sorted(vp_values, reverse=True)

    top_10 = sorted_vp[:10]
    top_10_pct = round((sum(top_10) / total_vp) * 100, 1) if total_vp > 0 else 0.0

    top_25 = sorted_vp[:25]
    top_25_pct = round((sum(top_25) / total_vp) * 100, 1) if total_vp > 0 else 0.0

    gini = _calculate_gini(vp_values)

    return {
        "gini_coefficient": gini,
        "top_10_pct": top_10_pct,
        "top_25_pct": top_25_pct,
        "total_voters": len(vp_values),
    }


def _analyze_timing(
    votes: List[Dict[str, Any]], proposal_start: int, proposal_end: int
) -> Dict[str, Any]:
    """Analyze voting timing patterns: early vs late voters."""
    if not votes or proposal_start >= proposal_end:
        return {
            "early_voters_pct": 0.0,
            "late_voters_pct": 0.0,
            "early_vp_pct": 0.0,
            "late_vp_pct": 0.0,
        }

    midpoint = proposal_start + (proposal_end - proposal_start) // 2

    early_count = 0
    late_count = 0
    early_vp = 0.0
    late_vp = 0.0

    for vote in votes:
        created = vote.get("created", 0)
        vp = vote.get("vp", 0)

        if created <= midpoint:
            early_count += 1
            early_vp += vp
        else:
            late_count += 1
            late_vp += vp

    total_count = early_count + late_count
    total_vp = early_vp + late_vp

    return {
        "early_voters_pct": round((early_count / total_count) * 100, 1) if total_count > 0 else 0.0,
        "late_voters_pct": round((late_count / total_count) * 100, 1) if total_count > 0 else 0.0,
        "early_vp_pct": round((early_vp / total_vp) * 100, 1) if total_vp > 0 else 0.0,
        "late_vp_pct": round((late_vp / total_vp) * 100, 1) if total_vp > 0 else 0.0,
        "early_voters": early_count,
        "late_voters": late_count,
    }


def _determine_outcome_analysis(
    whale_analysis: Dict[str, Any],
    distribution: Dict[str, Any],
    timing: Dict[str, Any],
) -> Dict[str, Any]:
    """Determine whether whales or community decided the outcome."""
    top_share = whale_analysis.get("top_10_share_pct", 0)
    whale_dominant = whale_analysis.get("whale_dominant", False)

    # Check if whales voted differently from the community
    top_voters = whale_analysis.get("top_voters", [])
    whale_choices: Dict[str, float] = {}
    for v in top_voters:
        choice = v.get("choice", "Unknown")
        whale_choices[choice] = whale_choices.get(choice, 0) + v.get("vp", 0)

    whale_leading = max(whale_choices, key=whale_choices.get) if whale_choices else "Unknown"

    # Find overall leading choice
    overall_leading = ""
    max_vp = 0.0
    for choice, data in distribution.items():
        if data.get("vp", 0) > max_vp:
            max_vp = data["vp"]
            overall_leading = choice

    whale_aligned = whale_leading == overall_leading

    analysis = {
        "outcome_decided_by": "whales" if whale_dominant else "community",
        "whale_aligned_with_outcome": whale_aligned,
        "top_10_concentration": top_share,
        "risk_level": "HIGH" if top_share > 70 else "MEDIUM" if top_share > 50 else "LOW",
    }

    if timing.get("late_vp_pct", 0) > 70:
        analysis["timing_concern"] = "High late-voting VP suggests potential vote sniping"
    elif timing.get("early_vp_pct", 0) > 70:
        analysis["timing_concern"] = "High early-voting VP suggests whale signaling"

    return analysis


def analyze_proposal(proposal_id: str) -> Dict[str, Any]:
    """Perform full voting analysis on a proposal."""
    # Fetch proposal details
    proposal, error = _fetch_proposal(proposal_id)
    if error:
        return error

    choices = proposal.get("choices", [])
    space = proposal.get("space") or {}

    # Fetch votes
    votes = _fetch_all_votes(proposal_id)

    if not votes:
        return {
            "status": "success",
            "proposal": {
                "id": proposal.get("id", ""),
                "title": proposal.get("title", ""),
                "space": space.get("id", ""),
                "state": proposal.get("state", ""),
                "choices": choices,
            },
            "vote_distribution": {},
            "whale_analysis": {"top_10_share_pct": 0, "whale_dominant": False, "top_voters": []},
            "participation": {"total_voters": 0, "total_vp": 0},
            "concentration": {"gini_coefficient": 0, "top_10_pct": 0, "top_25_pct": 0},
            "timing": {},
            "outcome_analysis": {"outcome_decided_by": "no votes", "risk_level": "N/A"},
            "message": "No votes found for this proposal.",
        }

    # Run analysis
    distribution = _analyze_vote_distribution(votes, choices)
    whale_analysis = _analyze_whales(votes, choices)
    concentration = _analyze_concentration(votes)
    timing = _analyze_timing(
        votes,
        proposal.get("start", 0),
        proposal.get("end", 0),
    )
    outcome_analysis = _determine_outcome_analysis(whale_analysis, distribution, timing)

    total_vp = sum(v.get("vp", 0) for v in votes)

    # Quorum info
    quorum = proposal.get("quorum", 0)
    quorum_info = {}
    if quorum > 0:
        quorum_info = {
            "quorum_required": round(quorum, 2),
            "total_vp": round(total_vp, 2),
            "quorum_reached": total_vp >= quorum,
            "quorum_pct": round((total_vp / quorum) * 100, 1) if quorum > 0 else 0,
        }

    result: Dict[str, Any] = {
        "status": "success",
        "proposal": {
            "id": proposal.get("id", ""),
            "title": proposal.get("title", ""),
            "space": space.get("id", ""),
            "space_name": space.get("name", ""),
            "state": proposal.get("state", ""),
            "choices": choices,
            "start": _ts_to_iso(proposal.get("start", 0)),
            "end": _ts_to_iso(proposal.get("end", 0)),
        },
        "vote_distribution": distribution,
        "whale_analysis": whale_analysis,
        "participation": {
            "total_voters": len(votes),
            "total_vp": round(total_vp, 2),
        },
        "concentration": concentration,
        "timing": timing,
        "outcome_analysis": outcome_analysis,
    }

    if quorum_info:
        result["quorum"] = quorum_info

    return result


def validate_input(data: Dict[str, Any]) -> Optional[str]:
    """Validate input parameters. Returns error message or None."""
    proposal_id = data.get("proposal_id")
    space_id = data.get("space_id")

    if not proposal_id and not space_id:
        return (
            "Missing required input: provide 'proposal_id' directly, "
            "or 'space_id' with 'proposal_index' (0 = most recent)."
        )

    if space_id and not proposal_id:
        idx = data.get("proposal_index")
        if idx is None:
            # Default to most recent
            data["proposal_index"] = 0
        elif not isinstance(idx, int) or idx < 0:
            return "Invalid proposal_index: must be a non-negative integer."

    return None


def main() -> None:
    """Read JSON input from stdin, analyze voting, write JSON output to stdout."""
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            json.dump({
                "status": "error",
                "error": "No input provided.",
                "details": "Provide a proposal_id or space_id via JSON stdin.",
            }, sys.stdout, indent=2)
            return
        data = json.loads(raw_input)
    except json.JSONDecodeError as exc:
        json.dump({
            "status": "error",
            "error": f"Invalid JSON input: {exc}",
        }, sys.stdout, indent=2)
        return

    error = validate_input(data)
    if error:
        json.dump({"status": "error", "error": error}, sys.stdout, indent=2)
        return

    proposal_id = data.get("proposal_id")

    # Resolve proposal ID from space + index if needed
    if not proposal_id:
        space_id = data["space_id"]
        proposal_index = data.get("proposal_index", 0)
        proposal_id, resolve_error = _resolve_proposal_id(space_id, proposal_index)
        if resolve_error:
            json.dump(resolve_error, sys.stdout, indent=2)
            return

    result = analyze_proposal(proposal_id)
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
