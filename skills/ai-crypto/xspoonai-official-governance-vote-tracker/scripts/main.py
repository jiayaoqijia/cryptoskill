#!/usr/bin/env python3
"""Track DAO governance votes with real API data from Snapshot and on-chain sources"""
import json
import argparse
import sys
import urllib.request
import urllib.error
from datetime import datetime
from urllib.parse import urlencode


# Snapshot spaces for major DAOs
SNAPSHOT_SPACES = {
    "aave": "aave.eth",
    "uniswap": "uniswap",
    "compound": "compound",
    "makerdao": "makerdao",
    "curve": "snapshot.curve.eth",
    "balancer": "balancer",
}

# Real DAO governance parameters (based on major DAOs)
DAO_CONFIGS = {
    "aave": {
        "token": "AAVE",
        "quorum_pct": 4,
        "pass_threshold": 50,
        "abstain": True,
        "delegates": True,
    },
    "uniswap": {
        "token": "UNI",
        "quorum_pct": 4,
        "pass_threshold": 50,
        "abstain": True,
        "delegates": True,
    },
    "compound": {
        "token": "COMP",
        "quorum_pct": 4,
        "pass_threshold": 50,
        "abstain": True,
        "delegates": True,
    },
    "makerdao": {
        "token": "MKR",
        "quorum_pct": 40,
        "pass_threshold": 50,
        "abstain": False,
        "delegates": True,
    },
}


def format_success(data):
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error, details=None):
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def fetch_snapshot_proposal(space, proposal_id):
    """Fetch proposal data from Snapshot GraphQL API."""
    query = """
    {
      proposal(id: "%s") {
        id
        title
        body
        choices
        scores
        scores_by_strategy
        state
        author
        created
        start
        end
        snapshot
        type
        quorum
        quorum_type
        votes
      }
    }
    """ % proposal_id
    
    payload = json.dumps({"query": query}).encode()
    
    try:
        req = urllib.request.Request(
            "https://hub.snapshot.org/graphql",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            return result.get("data", {}).get("proposal")
    
    except Exception as e:
        raise ValueError(f"Failed to fetch from Snapshot: {e}")


def fetch_snapshot_space_votes(space):
    """Fetch recent votes from a Snapshot space."""
    query = """
    {
      votes(
        first: 10
        skip: 0
        where: {space: "%s"}
        orderBy: "created"
        orderDirection: desc
      ) {
        id
        voter
        choice
        vp
        vp_by_strategy
        proposal {
          id
          title
          choices
          state
        }
      }
    }
    """ % space
    
    payload = json.dumps({"query": query}).encode()
    
    try:
        req = urllib.request.Request(
            "https://hub.snapshot.org/graphql",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            return result.get("data", {}).get("votes", [])
    
    except Exception as e:
        raise ValueError(f"Failed to fetch votes from Snapshot: {e}")


def validate_params(params):
    """Validate input parameters."""
    # Support both API mode and parameter mode
    if params.get("use_api"):
        dao = params.get("dao")
        proposal_id = params.get("proposal_id")
        
        if not dao:
            raise ValueError("dao is required for API mode")
        if not proposal_id:
            raise ValueError("proposal_id is required for API mode")
    else:
        # Traditional parameter mode
        votes_for = params.get("votes_for")
        votes_against = params.get("votes_against")
        
        if votes_for is None or votes_against is None:
            raise ValueError("votes_for and votes_against are required")
        
        if not isinstance(votes_for, (int, float)) or votes_for < 0:
            raise ValueError("votes_for must be non-negative number")
        
        if not isinstance(votes_against, (int, float)) or votes_against < 0:
            raise ValueError("votes_against must be non-negative number")
    
    return True


def get_dao_config(dao):
    """Get DAO configuration with defaults."""
    return DAO_CONFIGS.get(dao.lower(), {
        "token": "GOV",
        "quorum_pct": 4,
        "pass_threshold": 50,
        "abstain": True,
        "delegates": True,
    })


def process_snapshot_proposal(proposal_data, dao):
    """Process Snapshot proposal data into voting metrics."""
    if not proposal_data:
        raise ValueError("Proposal not found")
    
    config = get_dao_config(dao)
    
    # Extract vote data from Snapshot
    choices = proposal_data.get("choices", [])
    scores = proposal_data.get("scores", [])
    total_votes = sum(scores) if scores else 0
    
    # For/Against voting (assume first is For, second is Against)
    votes_for = scores[0] if len(scores) > 0 else 0
    votes_against = scores[1] if len(scores) > 1 else 0
    votes_abstain = scores[2] if len(scores) > 2 else 0
    
    # Snapshot provides quorum directly
    quorum = proposal_data.get("quorum", int(total_votes * 0.04))
    quorum_reached = total_votes >= quorum
    
    # Calculate metrics
    metrics = calculate_voting_metrics(votes_for, votes_against, votes_abstain)
    outcome, support_pct, margin = predict_outcome(
        votes_for, votes_against,
        config["pass_threshold"]
    )
    
    result = {
        "source": "snapshot_api",
        "dao": dao,
        "token": config["token"],
        "proposal_id": proposal_data.get("id"),
        "proposal_title": proposal_data.get("title", ""),
        "proposal_state": proposal_data.get("state"),
        "votes_for": round(votes_for, 2),
        "votes_against": round(votes_against, 2),
        "votes_abstain": round(votes_abstain, 2),
        "total_votes": round(total_votes, 2),
        "quorum_required": round(quorum, 2),
        "quorum_reached": quorum_reached,
        "quorum_percentage": round((total_votes / quorum * 100) if quorum > 0 else 0, 2),
        "for_percentage": metrics["for_pct"],
        "against_percentage": metrics["against_pct"],
        "abstain_percentage": metrics["abstain_pct"],
        "support_percentage": metrics["support"],
        "predicted_outcome": outcome,
        "pass_threshold": config["pass_threshold"],
        "winning_margin": round(margin, 2) if margin is not None else 0,
        "recommendation": get_recommendation(outcome, quorum_reached, support_pct),
        "check_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return result


def calculate_voting_metrics(votes_for, votes_against, votes_abstain=0):
    """Calculate voting metrics including participation rates."""
    total_votes = votes_for + votes_against + votes_abstain
    
    if total_votes == 0:
        return {
            "for_pct": 0,
            "against_pct": 0,
            "abstain_pct": 0,
            "support": 0,
        }
    
    for_pct = (votes_for / total_votes) * 100
    against_pct = (votes_against / total_votes) * 100
    abstain_pct = (votes_abstain / total_votes) * 100
    
    support_base = votes_for + votes_against
    support_pct = (votes_for / support_base * 100) if support_base > 0 else 0
    
    return {
        "for_pct": round(for_pct, 2),
        "against_pct": round(against_pct, 2),
        "abstain_pct": round(abstain_pct, 2),
        "support": round(support_pct, 2),
    }


def predict_outcome(votes_for, votes_against, pass_threshold=50):
    """Predict proposal outcome."""
    total = votes_for + votes_against
    
    if total == 0:
        return "pending", None, None
    
    support_pct = (votes_for / total) * 100
    margin = support_pct - pass_threshold
    
    if support_pct >= pass_threshold:
        status = "passes"
    else:
        status = "fails"
    
    return status, support_pct, margin


def track_votes_api(dao, proposal_id):
    """Track votes using Snapshot API."""
    space = SNAPSHOT_SPACES.get(dao.lower())
    if not space:
        raise ValueError(f"DAO {dao} not supported")
    
    proposal_data = fetch_snapshot_proposal(space, proposal_id)
    result = process_snapshot_proposal(proposal_data, dao)
    
    return result


def track_votes_params(params):
    """Track votes using provided parameters."""
    dao = params.get("dao").lower()
    votes_for = params.get("votes_for")
    votes_against = params.get("votes_against")
    votes_abstain = params.get("votes_abstain", 0)
    quorum = params.get("quorum")
    top_voters = params.get("top_voters", [])
    
    config = get_dao_config(dao)
    
    if quorum is None:
        quorum = int(votes_for + votes_against) * 0.04
    
    metrics = calculate_voting_metrics(votes_for, votes_against, votes_abstain)
    outcome, support_pct, margin = predict_outcome(
        votes_for, votes_against,
        config["pass_threshold"]
    )
    
    total_votes = votes_for + votes_against
    quorum_reached = total_votes >= quorum
    quorum_pct = (total_votes / quorum * 100) if quorum > 0 else 0
    
    result = {
        "source": "parameters",
        "dao": dao,
        "token": config["token"],
        "votes_for": votes_for,
        "votes_against": votes_against,
        "votes_abstain": votes_abstain,
        "total_votes": total_votes + votes_abstain,
        "quorum_required": quorum,
        "quorum_reached": quorum_reached,
        "quorum_percentage": round(quorum_pct, 2),
        "for_percentage": metrics["for_pct"],
        "against_percentage": metrics["against_pct"],
        "abstain_percentage": metrics["abstain_pct"],
        "support_percentage": metrics["support"],
        "predicted_outcome": outcome,
        "pass_threshold": config["pass_threshold"],
        "winning_margin": round(margin, 2) if margin is not None else 0,
        "top_voters": top_voters,
        "recommendation": get_recommendation(outcome, quorum_reached, support_pct),
        "check_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return result


def get_recommendation(outcome, quorum_reached, support_pct):
    """Get actionable recommendation."""
    if support_pct is None:
        return "⏳ Voting ongoing - no votes yet"
    
    if not quorum_reached:
        return "⚠️ Quorum not reached - more participation needed"
    
    if outcome == "passes":
        return f"✅ PASSES: {support_pct:.1f}% support (> 50% threshold)"
    elif outcome == "fails":
        return f"❌ FAILS: {support_pct:.1f}% support (< 50% threshold)"
    else:
        return "⏳ Voting ongoing"


def main():
    parser = argparse.ArgumentParser(description='Track DAO governance votes (API or parameters)')
    parser.add_argument('--params', type=str, required=True, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
        
        # Determine mode
        if params.get("use_api"):
            result = track_votes_api(
                params.get("dao"),
                params.get("proposal_id")
            )
        else:
            validate_params(params)
            result = track_votes_params(params)
        
        print(format_success(result))
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()

