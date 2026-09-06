#!/usr/bin/env python3
"""
DAO Health — Calculate comprehensive DAO health metrics.

Uses the Snapshot GraphQL API (free, public, no API key required).

Input (JSON via stdin):
    {
        "space_id": "aave.eth",                        // Single DAO analysis
        // OR
        "compare": ["aave.eth", "uniswapgovernance.eth"]  // Comparison mode
    }

Output (JSON via stdout):
    {
        "status": "success",
        "space": "aave.eth",
        "health_score": 78,
        "rating": "HEALTHY",
        "breakdown": {...},
        "metadata": {...}
    }
"""

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

SNAPSHOT_API = "https://hub.snapshot.org/graphql"

SPACE_QUERY = """
query Space($id: String!) {
  space(id: $id) {
    id
    name
    about
    members
    proposals_count
    followers_count
    voting {
      delay
      period
      quorum
    }
    strategies {
      name
    }
  }
}
"""

RECENT_PROPOSALS_QUERY = """
query RecentProposals($space: String!, $first: Int) {
  proposals(
    where: { space: $space }
    first: $first
    orderBy: "created"
    orderDirection: desc
  ) {
    id
    title
    state
    scores
    scores_total
    votes
    quorum
    start
    end
    space { id members }
  }
}
"""

VOTES_QUERY = """
query Votes($proposal: String!, $first: Int) {
  votes(
    where: { proposal: $proposal }
    first: $first
    orderBy: "vp"
    orderDirection: desc
  ) {
    voter
    vp
  }
}
"""

# Health score weights
WEIGHTS = {
    "activity": 0.20,
    "participation": 0.25,
    "decentralization": 0.25,
    "quorum_achievement": 0.15,
    "proposal_success": 0.15,
}


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


def _ts_to_date(ts: int) -> str:
    """Convert UNIX timestamp to date string."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def _fetch_space_info(space_id: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """Fetch space metadata."""
    resp = _graphql_query(SPACE_QUERY, {"id": space_id})
    if "error" in resp:
        return None, {"status": "error", "error": resp["error"]}

    space = (resp.get("data") or {}).get("space")
    if not space:
        return None, {
            "status": "error",
            "error": f"Space '{space_id}' not found.",
            "details": "Verify the space ID on snapshot.org.",
        }

    return space, None


def _fetch_recent_proposals(space_id: str, count: int = 50) -> List[Dict[str, Any]]:
    """Fetch recent proposals for a space."""
    resp = _graphql_query(RECENT_PROPOSALS_QUERY, {
        "space": space_id,
        "first": min(count, 100),
    })

    if "error" in resp:
        return []

    return (resp.get("data") or {}).get("proposals") or []


def _fetch_top_voters(proposal_id: str, count: int = 50) -> List[Dict[str, Any]]:
    """Fetch top voters for a proposal."""
    resp = _graphql_query(VOTES_QUERY, {
        "proposal": proposal_id,
        "first": count,
    })

    if "error" in resp:
        return []

    return (resp.get("data") or {}).get("votes") or []


def _calculate_activity_score(proposals: List[Dict], months: int = 3) -> Dict[str, Any]:
    """Calculate activity score based on proposals per month.

    Scoring:
      - 4+ proposals/month: 100
      - 2-4: linear 60-100
      - 1-2: linear 30-60
      - <1: linear 0-30
    """
    if not proposals:
        return {"score": 0, "proposals_per_month": 0.0, "total_proposals": 0}

    now = int(time.time())
    cutoff = now - (months * 30 * 86400)

    recent = [p for p in proposals if p.get("start", 0) >= cutoff]
    proposals_per_month = len(recent) / months if months > 0 else 0

    if proposals_per_month >= 4:
        score = 100
    elif proposals_per_month >= 2:
        score = 60 + (proposals_per_month - 2) * 20
    elif proposals_per_month >= 1:
        score = 30 + (proposals_per_month - 1) * 30
    else:
        score = proposals_per_month * 30

    return {
        "score": round(min(100, max(0, score))),
        "proposals_per_month": round(proposals_per_month, 1),
        "total_proposals": len(proposals),
        "recent_proposals": len(recent),
        "period_months": months,
    }


def _calculate_participation_score(
    proposals: List[Dict], member_count: int
) -> Dict[str, Any]:
    """Calculate participation score based on average voter turnout.

    Scoring:
      - Uses voter count relative to member count
      - Also considers absolute voter numbers
    """
    if not proposals or member_count <= 0:
        return {"score": 0, "avg_voters": 0, "members": member_count}

    closed = [p for p in proposals if p.get("state") == "closed"]
    if not closed:
        return {"score": 0, "avg_voters": 0, "members": member_count}

    voter_counts = [p.get("votes", 0) for p in closed]
    avg_voters = sum(voter_counts) / len(voter_counts)
    max_voters = max(voter_counts) if voter_counts else 0

    # Participation rate (capped at 1.0 for very active DAOs)
    participation_rate = min(avg_voters / member_count, 1.0)

    # Score: blend of relative and absolute participation
    # High relative participation is great even for small DAOs
    relative_score = participation_rate * 100

    # Bonus for absolute numbers (more than 100 voters is healthy)
    absolute_bonus = min(avg_voters / 500, 1.0) * 20

    score = min(100, relative_score * 0.8 + absolute_bonus)

    return {
        "score": round(max(0, score)),
        "avg_voters": round(avg_voters, 1),
        "max_voters": max_voters,
        "members": member_count,
        "participation_rate": round(participation_rate, 4),
    }


def _calculate_decentralization_score(proposals: List[Dict]) -> Dict[str, Any]:
    """Calculate decentralization score based on voting power concentration.

    Samples the most recent closed proposal to check top-10 voter concentration.

    Scoring:
      - Top 10 < 30%: 100 (highly decentralized)
      - Top 10 30-50%: 60-100
      - Top 10 50-70%: 30-60
      - Top 10 > 70%: 0-30
    """
    closed = [p for p in proposals if p.get("state") == "closed" and p.get("votes", 0) > 10]

    if not closed:
        return {"score": 50, "top_10_concentration": None, "sampled_proposals": 0}

    # Sample up to 3 recent closed proposals
    sample = closed[:3]
    concentrations: List[float] = []

    for proposal in sample:
        proposal_id = proposal.get("id", "")
        top_voters = _fetch_top_voters(proposal_id, count=50)

        if not top_voters:
            continue

        total_vp = sum(v.get("vp", 0) for v in top_voters)
        if total_vp == 0:
            continue

        top_10_vp = sum(v.get("vp", 0) for v in top_voters[:10])
        concentration = (top_10_vp / total_vp) * 100
        concentrations.append(concentration)

        time.sleep(0.3)

    if not concentrations:
        return {"score": 50, "top_10_concentration": None, "sampled_proposals": 0}

    avg_concentration = sum(concentrations) / len(concentrations)

    # Score: inverse of concentration
    if avg_concentration < 30:
        score = 100
    elif avg_concentration < 50:
        score = 100 - (avg_concentration - 30) * 2
    elif avg_concentration < 70:
        score = 60 - (avg_concentration - 50) * 1.5
    else:
        score = max(0, 30 - (avg_concentration - 70))

    return {
        "score": round(max(0, min(100, score))),
        "top_10_concentration": round(avg_concentration, 1),
        "sampled_proposals": len(concentrations),
    }


def _calculate_quorum_score(proposals: List[Dict]) -> Dict[str, Any]:
    """Calculate quorum achievement rate.

    Scoring: percentage of proposals that reached quorum.
    """
    closed = [p for p in proposals if p.get("state") == "closed"]

    if not closed:
        return {"score": 0, "quorum_rate": 0.0, "proposals_with_quorum": 0, "total_closed": 0}

    quorum_met = 0
    quorum_applicable = 0

    for p in closed:
        quorum = p.get("quorum", 0)
        scores_total = p.get("scores_total", 0)

        if quorum > 0:
            quorum_applicable += 1
            if scores_total >= quorum:
                quorum_met += 1

    if quorum_applicable == 0:
        # No quorum set — assume healthy (neutral score)
        return {
            "score": 70,
            "quorum_rate": None,
            "note": "No quorum requirement set for this space",
            "total_closed": len(closed),
        }

    quorum_rate = quorum_met / quorum_applicable
    score = quorum_rate * 100

    return {
        "score": round(score),
        "quorum_rate": round(quorum_rate, 2),
        "proposals_with_quorum": quorum_met,
        "quorum_applicable": quorum_applicable,
        "total_closed": len(closed),
    }


def _calculate_proposal_success_score(proposals: List[Dict]) -> Dict[str, Any]:
    """Calculate proposal success rate.

    Success = proposals where a clear winning choice emerged and quorum was met.
    Scoring: success rate * 100.
    """
    closed = [p for p in proposals if p.get("state") == "closed"]

    if not closed:
        return {"score": 0, "success_rate": 0.0, "successful": 0, "total_closed": 0}

    successful = 0
    for p in closed:
        scores = p.get("scores") or []
        scores_total = p.get("scores_total", 0)
        quorum = p.get("quorum", 0)

        if not scores or scores_total == 0:
            continue

        # A proposal is "successful" if quorum was met (or no quorum) and a choice won clearly
        quorum_ok = scores_total >= quorum if quorum > 0 else True
        max_score = max(scores)
        clear_winner = max_score > scores_total * 0.4  # At least 40% for one choice

        if quorum_ok and clear_winner:
            successful += 1

    success_rate = successful / len(closed) if closed else 0
    score = success_rate * 100

    return {
        "score": round(min(100, score)),
        "success_rate": round(success_rate, 2),
        "successful": successful,
        "total_closed": len(closed),
    }


def _get_rating(score: int) -> str:
    """Convert health score to a rating label."""
    if score >= 80:
        return "EXCELLENT"
    elif score >= 60:
        return "HEALTHY"
    elif score >= 40:
        return "MODERATE"
    elif score >= 20:
        return "WEAK"
    else:
        return "CRITICAL"


def analyze_dao_health(space_id: str) -> Dict[str, Any]:
    """Calculate comprehensive DAO health metrics for a single space."""
    # Fetch space info
    space, error = _fetch_space_info(space_id)
    if error:
        return error

    member_count = len(space.get("members") or [])
    proposals = _fetch_recent_proposals(space_id, count=50)

    # Calculate component scores
    activity = _calculate_activity_score(proposals)
    participation = _calculate_participation_score(proposals, member_count)
    decentralization = _calculate_decentralization_score(proposals)
    quorum = _calculate_quorum_score(proposals)
    success = _calculate_proposal_success_score(proposals)

    # Weighted overall score
    health_score = round(
        activity["score"] * WEIGHTS["activity"]
        + participation["score"] * WEIGHTS["participation"]
        + decentralization["score"] * WEIGHTS["decentralization"]
        + quorum["score"] * WEIGHTS["quorum_achievement"]
        + success["score"] * WEIGHTS["proposal_success"]
    )

    rating = _get_rating(health_score)

    voting_config = space.get("voting") or {}
    strategies = space.get("strategies") or []

    return {
        "status": "success",
        "space": space_id,
        "space_name": space.get("name", ""),
        "health_score": health_score,
        "rating": rating,
        "breakdown": {
            "activity": activity,
            "participation": participation,
            "decentralization": decentralization,
            "quorum_achievement": quorum,
            "proposal_success": success,
        },
        "metadata": {
            "members": member_count,
            "followers": space.get("followers_count", 0),
            "total_proposals": space.get("proposals_count", 0),
            "strategies_count": len(strategies),
            "strategies": [s.get("name", "") for s in strategies[:5]],
            "voting_delay": voting_config.get("delay", 0),
            "voting_period": voting_config.get("period", 0),
            "quorum_setting": voting_config.get("quorum", 0),
        },
    }


def compare_daos(space_ids: List[str]) -> Dict[str, Any]:
    """Compare health metrics across multiple DAOs."""
    results: List[Dict[str, Any]] = []
    errors: List[str] = []

    for space_id in space_ids:
        result = analyze_dao_health(space_id)
        if result.get("status") == "success":
            results.append(result)
        else:
            errors.append(f"{space_id}: {result.get('error', 'unknown error')}")

        time.sleep(0.5)

    if not results:
        return {
            "status": "error",
            "error": "Could not analyze any of the provided spaces.",
            "details": errors,
        }

    # Sort by health score descending
    results.sort(key=lambda r: r.get("health_score", 0), reverse=True)

    # Build comparison table
    comparison = []
    for r in results:
        breakdown = r.get("breakdown", {})
        comparison.append({
            "space": r.get("space", ""),
            "name": r.get("space_name", ""),
            "health_score": r.get("health_score", 0),
            "rating": r.get("rating", ""),
            "activity": breakdown.get("activity", {}).get("score", 0),
            "participation": breakdown.get("participation", {}).get("score", 0),
            "decentralization": breakdown.get("decentralization", {}).get("score", 0),
            "quorum": breakdown.get("quorum_achievement", {}).get("score", 0),
            "success": breakdown.get("proposal_success", {}).get("score", 0),
        })

    output: Dict[str, Any] = {
        "status": "success",
        "mode": "comparison",
        "spaces_analyzed": len(results),
        "comparison": comparison,
        "detailed_results": results,
        "best_overall": results[0].get("space", "") if results else None,
    }

    # Find best in each category
    categories = ["activity", "participation", "decentralization", "quorum", "success"]
    leaders: Dict[str, str] = {}
    for cat in categories:
        best = max(comparison, key=lambda c: c.get(cat, 0))
        leaders[cat] = best.get("space", "")

    output["category_leaders"] = leaders

    if errors:
        output["warnings"] = errors

    return output


def validate_input(data: Dict[str, Any]) -> Optional[str]:
    """Validate input parameters. Returns error message or None."""
    space_id = data.get("space_id")
    compare = data.get("compare")

    if not space_id and not compare:
        return (
            "Missing required input: provide 'space_id' (e.g., 'aave.eth') "
            "or 'compare' (array of space IDs)."
        )

    if compare:
        if not isinstance(compare, list) or len(compare) < 2:
            return "Invalid 'compare': must be a list of at least 2 space IDs."
        if len(compare) > 10:
            return "Too many spaces to compare. Maximum is 10."

    return None


def main() -> None:
    """Read JSON input from stdin, analyze DAO health, write JSON output to stdout."""
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            json.dump({
                "status": "error",
                "error": "No input provided.",
                "details": "Provide space_id or compare array via JSON stdin.",
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

    if data.get("compare"):
        result = compare_daos(data["compare"])
    else:
        result = analyze_dao_health(data["space_id"])

    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
