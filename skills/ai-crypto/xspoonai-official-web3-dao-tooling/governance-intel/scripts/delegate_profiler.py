#!/usr/bin/env python3
"""
Delegate Profiler — Profile a delegate or voter's governance participation.

Uses the Snapshot GraphQL API (free, public, no API key required).

Input (JSON via stdin):
    {
        "voter_address": "0x...",     // Required: Ethereum address
        "space_id": "aave.eth",       // Optional: specific space
        "top_daos": true,             // Optional: scan across major DAOs
        "limit": 100                  // Optional: max votes to fetch (default 100)
    }

Output (JSON via stdout):
    {
        "status": "success",
        "voter": "0x...",
        "summary": {...},
        "participation": {...},
        "choice_distribution": {...},
        "alignment": {...},
        "recent_votes": [...]
    }
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

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

VOTER_HISTORY_QUERY = """
query VoterHistory($voter: String!, $space: String, $first: Int, $skip: Int) {
  votes(
    where: { voter: $voter, space: $space }
    first: $first
    skip: $skip
    orderBy: "created"
    orderDirection: desc
  ) {
    proposal {
      id
      title
      choices
      state
      scores
      scores_total
      space { id name }
    }
    choice
    vp
    created
  }
}
"""

VOTER_HISTORY_NO_SPACE_QUERY = """
query VoterHistory($voter: String!, $first: Int, $skip: Int) {
  votes(
    where: { voter: $voter }
    first: $first
    skip: $skip
    orderBy: "created"
    orderDirection: desc
  ) {
    proposal {
      id
      title
      choices
      state
      scores
      scores_total
      space { id name }
    }
    choice
    vp
    created
  }
}
"""

SPACE_PROPOSALS_COUNT_QUERY = """
query SpaceInfo($id: String!) {
  space(id: $id) {
    id
    name
    proposals_count
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


def _ts_to_date(ts: int) -> str:
    """Convert UNIX timestamp to date string."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def _ts_to_iso(ts: int) -> str:
    """Convert UNIX timestamp to ISO 8601 string."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_valid_address(addr: str) -> bool:
    """Check if a string looks like a valid Ethereum address."""
    return bool(re.match(r"^0x[a-fA-F0-9]{40}$", addr))


def _resolve_choice_name(choice_idx: Any, choices: List[str]) -> str:
    """Resolve choice index to choice name."""
    if isinstance(choice_idx, int) and 1 <= choice_idx <= len(choices):
        return choices[choice_idx - 1]
    elif isinstance(choice_idx, dict):
        # Weighted voting
        if not choice_idx:
            return "Abstain"
        max_entry = max(choice_idx.items(), key=lambda x: x[1])
        idx = int(max_entry[0])
        if 1 <= idx <= len(choices):
            return f"{choices[idx - 1]} (weighted)"
    return "Unknown"


def _determine_winning_choice(proposal: Dict[str, Any]) -> Optional[str]:
    """Determine the winning choice for a closed proposal."""
    scores = proposal.get("scores") or []
    choices = proposal.get("choices") or []
    state = proposal.get("state", "")

    if state != "closed" or not scores or not choices:
        return None

    max_idx = 0
    max_score = scores[0] if scores else 0
    for i, s in enumerate(scores):
        if s > max_score:
            max_score = s
            max_idx = i

    if max_idx < len(choices):
        return choices[max_idx]

    return None


def _fetch_voter_votes(
    voter: str, space_id: Optional[str] = None, limit: int = 100
) -> List[Dict[str, Any]]:
    """Fetch votes for a voter, with optional space filter and pagination."""
    all_votes: List[Dict[str, Any]] = []
    skip = 0
    page_size = min(limit, 1000)

    while len(all_votes) < limit:
        if space_id:
            query = VOTER_HISTORY_QUERY
            variables: Dict[str, Any] = {
                "voter": voter,
                "space": space_id,
                "first": min(page_size, limit - len(all_votes)),
                "skip": skip,
            }
        else:
            query = VOTER_HISTORY_NO_SPACE_QUERY
            variables = {
                "voter": voter,
                "first": min(page_size, limit - len(all_votes)),
                "skip": skip,
            }

        resp = _graphql_query(query, variables)
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


def _get_space_proposal_count(space_id: str) -> int:
    """Get the total proposal count for a space."""
    resp = _graphql_query(SPACE_PROPOSALS_COUNT_QUERY, {"id": space_id})
    if "error" in resp:
        return 0
    space = (resp.get("data") or {}).get("space")
    if not space:
        return 0
    return space.get("proposals_count", 0)


def _calculate_consistency_score(choice_names: List[str]) -> float:
    """Calculate how consistently the voter votes the same way (0-1)."""
    if not choice_names:
        return 0.0

    # Count each choice type
    choice_counts: Dict[str, int] = {}
    for c in choice_names:
        # Normalize weighted choices
        base_choice = c.replace(" (weighted)", "")
        choice_counts[base_choice] = choice_counts.get(base_choice, 0) + 1

    # Consistency = max choice frequency / total votes
    max_count = max(choice_counts.values())
    return round(max_count / len(choice_names), 2)


def profile_voter(
    voter_address: str,
    space_id: Optional[str] = None,
    top_daos: bool = False,
    limit: int = 100,
) -> Dict[str, Any]:
    """Profile a voter's governance participation."""
    voter = voter_address.lower()

    if top_daos and not space_id:
        # Scan across top DAOs
        return _profile_cross_dao(voter, limit)

    # Single space or all spaces
    votes = _fetch_voter_votes(voter, space_id=space_id, limit=limit)

    if not votes:
        return {
            "status": "success",
            "voter": _shorten_address(voter_address),
            "voter_full": voter_address,
            "space": space_id or "all",
            "summary": {
                "total_votes": 0,
                "unique_spaces": 0,
                "avg_voting_power": 0,
                "total_voting_power_used": 0,
            },
            "message": f"No votes found for {_shorten_address(voter_address)}"
                       + (f" in {space_id}" if space_id else "") + ".",
        }

    # Compute summary statistics
    unique_spaces: Dict[str, int] = {}
    total_vp = 0.0
    choice_names: List[str] = []
    choice_distribution: Dict[str, int] = {}
    aligned_count = 0
    decided_count = 0
    recent_votes_list: List[Dict[str, Any]] = []

    for vote in votes:
        vp = vote.get("vp", 0)
        total_vp += vp

        proposal = vote.get("proposal") or {}
        space_info = proposal.get("space") or {}
        space_key = space_info.get("id", "unknown")

        unique_spaces[space_key] = unique_spaces.get(space_key, 0) + 1

        choices = proposal.get("choices") or []
        choice_name = _resolve_choice_name(vote.get("choice"), choices)
        choice_names.append(choice_name)

        base_choice = choice_name.replace(" (weighted)", "")
        choice_distribution[base_choice] = choice_distribution.get(base_choice, 0) + 1

        # Alignment: did the voter vote with the winning choice?
        winning_choice = _determine_winning_choice(proposal)
        if winning_choice is not None:
            decided_count += 1
            if base_choice == winning_choice:
                aligned_count += 1

        # Build recent vote entry
        recent_votes_list.append({
            "proposal_id": proposal.get("id", ""),
            "proposal": proposal.get("title", "Untitled"),
            "space": space_key,
            "space_name": space_info.get("name", ""),
            "choice": choice_name,
            "vp": round(vp, 2),
            "date": _ts_to_date(vote.get("created", 0)),
            "proposal_state": proposal.get("state", ""),
        })

    total_votes = len(votes)
    avg_vp = round(total_vp / total_votes, 2) if total_votes > 0 else 0.0

    # Participation rate (only if single space)
    participation_info: Dict[str, Any] = {
        "proposals_voted": total_votes,
    }
    if space_id:
        total_proposals = _get_space_proposal_count(space_id)
        if total_proposals > 0:
            participation_info["proposals_available"] = total_proposals
            participation_info["participation_rate"] = round(
                min(total_votes / total_proposals, 1.0), 2
            )

    # Consistency score
    consistency = _calculate_consistency_score(choice_names)

    # Alignment rate
    alignment_info: Dict[str, Any] = {
        "aligned_with_outcome": aligned_count,
        "total_decided": decided_count,
    }
    if decided_count > 0:
        alignment_info["alignment_rate"] = round(aligned_count / decided_count, 2)

    # Space breakdown
    space_breakdown = [
        {"space": s, "votes": c}
        for s, c in sorted(unique_spaces.items(), key=lambda x: -x[1])
    ]

    result: Dict[str, Any] = {
        "status": "success",
        "voter": _shorten_address(voter_address),
        "voter_full": voter_address,
        "space": space_id or "all",
        "summary": {
            "total_votes": total_votes,
            "unique_spaces": len(unique_spaces),
            "avg_voting_power": avg_vp,
            "total_voting_power_used": round(total_vp, 2),
        },
        "participation": participation_info,
        "choice_distribution": dict(
            sorted(choice_distribution.items(), key=lambda x: -x[1])
        ),
        "consistency_score": consistency,
        "alignment": alignment_info,
        "recent_votes": recent_votes_list[:20],
    }

    if len(unique_spaces) > 1:
        result["space_breakdown"] = space_breakdown

    return result


def _profile_cross_dao(voter: str, limit: int) -> Dict[str, Any]:
    """Profile a voter across top DAOs."""
    all_space_profiles: List[Dict[str, Any]] = []
    total_votes = 0
    total_vp = 0.0
    active_spaces: List[str] = []

    for space_id in TOP_DAOS:
        votes = _fetch_voter_votes(voter, space_id=space_id, limit=min(limit, 50))
        if votes:
            vote_count = len(votes)
            vp_sum = sum(v.get("vp", 0) for v in votes)
            total_votes += vote_count
            total_vp += vp_sum
            active_spaces.append(space_id)

            all_space_profiles.append({
                "space": space_id,
                "votes": vote_count,
                "total_vp": round(vp_sum, 2),
                "avg_vp": round(vp_sum / vote_count, 2) if vote_count > 0 else 0,
                "latest_vote": _ts_to_date(votes[0].get("created", 0)),
            })

        time.sleep(0.3)

    if not all_space_profiles:
        return {
            "status": "success",
            "voter": _shorten_address(voter),
            "voter_full": voter,
            "mode": "cross_dao",
            "summary": {
                "total_votes": 0,
                "active_spaces": 0,
                "spaces_checked": len(TOP_DAOS),
            },
            "message": f"No governance activity found for {_shorten_address(voter)} across top DAOs.",
        }

    # Sort by vote count
    all_space_profiles.sort(key=lambda x: -x["votes"])

    return {
        "status": "success",
        "voter": _shorten_address(voter),
        "voter_full": voter,
        "mode": "cross_dao",
        "summary": {
            "total_votes": total_votes,
            "active_spaces": len(active_spaces),
            "spaces_checked": len(TOP_DAOS),
            "total_voting_power_used": round(total_vp, 2),
        },
        "space_profiles": all_space_profiles,
        "most_active_space": all_space_profiles[0]["space"] if all_space_profiles else None,
    }


def validate_input(data: Dict[str, Any]) -> Optional[str]:
    """Validate input parameters. Returns error message or None."""
    voter = data.get("voter_address")
    if not voter:
        return "Missing required parameter: 'voter_address' (Ethereum address, e.g., '0x...')."

    if not _is_valid_address(voter):
        return (
            f"Invalid address format: '{voter}'. "
            "Expected format: 0x followed by 40 hex characters."
        )

    limit = data.get("limit")
    if limit is not None:
        if not isinstance(limit, int) or limit < 1:
            return "Invalid limit: must be a positive integer."

    return None


def main() -> None:
    """Read JSON input from stdin, profile voter, write JSON output to stdout."""
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            json.dump({
                "status": "error",
                "error": "No input provided.",
                "details": "Provide voter_address via JSON stdin.",
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

    result = profile_voter(
        voter_address=data["voter_address"],
        space_id=data.get("space_id"),
        top_daos=data.get("top_daos", False),
        limit=data.get("limit", 100),
    )

    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
