#!/usr/bin/env python3
"""
Weighted Voting Aggregator for Multi-Agent Consensus

Takes agent results from consensus_engine and produces a final consensus
through weighted voting, confidence scoring, and agreement mapping.

Consensus Modes:
    - majority:     Weighted majority vote on verdict
    - conservative: Any risk flag above threshold → escalate
    - union:        Merge all findings, deduplicate by similarity
    - diversity:    Preserve all perspectives with weighted ranking

Design Principles:
    - Pure functions: All aggregation is side-effect-free
    - Immutable data: frozen dataclasses throughout
    - Byzantine tolerance: Weighted voting filters minority hallucinations
"""

import json
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
from typing import Optional


# ---------------------------------------------------------------------------
# Constants & Risk Ordering
# ---------------------------------------------------------------------------

VERDICT_SEVERITY: dict[str, int] = {
    "SAFE": 0,
    "LOW_RISK": 1,
    "MODERATE_RISK": 2,
    "HIGH_RISK": 3,
    "CRITICAL_RISK": 4,
    "ERROR": -1,
    "UNKNOWN": -1,
}

SEVERITY_TO_VERDICT: dict[int, str] = {
    v: k for k, v in VERDICT_SEVERITY.items() if v >= 0
}

FINDING_SIMILARITY_THRESHOLD = 0.65


# ---------------------------------------------------------------------------
# Data Types (Immutable)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AgentVote:
    """A single agent's vote with weight applied."""
    agent_id: str
    provider: str
    verdict: str
    severity: int
    confidence: float
    weight: float
    weighted_confidence: float
    findings: tuple[str, ...]


@dataclass(frozen=True)
class FindingCluster:
    """A group of similar findings across agents."""
    canonical: str
    sources: tuple[str, ...]
    count: int
    avg_confidence: float


@dataclass(frozen=True)
class AgreementMap:
    """Categorized findings by agreement level."""
    agreed: tuple[FindingCluster, ...]
    disputed: tuple[FindingCluster, ...]
    unique: tuple[FindingCluster, ...]


# ---------------------------------------------------------------------------
# Pure Aggregation Functions
# ---------------------------------------------------------------------------


def build_votes(
    agent_results: list[dict],
    agent_weights: dict[str, float],
) -> tuple[AgentVote, ...]:
    """Convert raw agent results into weighted votes, filtering errors."""
    votes: list[AgentVote] = []

    for result in agent_results:
        verdict = result.get("verdict", "UNKNOWN")
        severity = VERDICT_SEVERITY.get(verdict, -1)

        # Skip error/unknown results — they don't participate in consensus
        if severity < 0:
            continue

        agent_id = result.get("agent_id", "unknown")
        weight = agent_weights.get(agent_id, 1.0)
        confidence = float(result.get("confidence", 0.5))

        votes.append(AgentVote(
            agent_id=agent_id,
            provider=result.get("provider", "unknown"),
            verdict=verdict,
            severity=severity,
            confidence=confidence,
            weight=weight,
            weighted_confidence=confidence * weight,
            findings=tuple(result.get("findings", [])),
        ))

    return tuple(votes)


def finding_similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two finding strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def cluster_findings(
    votes: tuple[AgentVote, ...],
) -> tuple[FindingCluster, ...]:
    """Group similar findings across agents into clusters."""
    all_findings: list[tuple[str, str, float]] = []
    for vote in votes:
        for finding in vote.findings:
            all_findings.append((finding, vote.agent_id, vote.confidence))

    if not all_findings:
        return ()

    clusters: list[dict] = []

    for finding, agent_id, confidence in all_findings:
        merged = False
        for cluster in clusters:
            if finding_similarity(finding, cluster["canonical"]) >= FINDING_SIMILARITY_THRESHOLD:
                cluster["sources"].add(agent_id)
                cluster["confidences"].append(confidence)
                merged = True
                break

        if not merged:
            clusters.append({
                "canonical": finding,
                "sources": {agent_id},
                "confidences": [confidence],
            })

    return tuple(
        FindingCluster(
            canonical=c["canonical"],
            sources=tuple(sorted(c["sources"])),
            count=len(c["sources"]),
            avg_confidence=sum(c["confidences"]) / len(c["confidences"]),
        )
        for c in clusters
    )


def build_agreement_map(
    clusters: tuple[FindingCluster, ...],
    total_agents: int,
) -> AgreementMap:
    """Categorize finding clusters by agreement level.

    - agreed:   Found by majority (>50%) of agents
    - disputed: Found by 2+ agents but not majority
    - unique:   Found by only 1 agent
    """
    majority_threshold = total_agents / 2

    agreed: list[FindingCluster] = []
    disputed: list[FindingCluster] = []
    unique: list[FindingCluster] = []

    for cluster in clusters:
        if cluster.count > majority_threshold:
            agreed.append(cluster)
        elif cluster.count > 1:
            disputed.append(cluster)
        else:
            unique.append(cluster)

    return AgreementMap(
        agreed=tuple(agreed),
        disputed=tuple(disputed),
        unique=tuple(unique),
    )


# ---------------------------------------------------------------------------
# Consensus Mode Implementations
# ---------------------------------------------------------------------------


def consensus_majority(
    votes: tuple[AgentVote, ...],
    threshold: float,
) -> dict:
    """Weighted majority vote — the most common verdict wins.

    Each agent's vote is weighted by (confidence × domain_weight).
    If the winning verdict's weighted share < threshold, returns INCONCLUSIVE.
    """
    if not votes:
        return {"verdict": "INCONCLUSIVE", "confidence": 0.0, "method": "majority"}

    weighted_votes: dict[str, float] = {}
    for vote in votes:
        weighted_votes[vote.verdict] = (
            weighted_votes.get(vote.verdict, 0.0) + vote.weighted_confidence
        )

    total_weight = sum(weighted_votes.values())
    if total_weight == 0:
        return {"verdict": "INCONCLUSIVE", "confidence": 0.0, "method": "majority"}

    winner = max(weighted_votes, key=weighted_votes.get)  # type: ignore[arg-type]
    winner_share = weighted_votes[winner] / total_weight

    return {
        "verdict": winner if winner_share >= threshold else "INCONCLUSIVE",
        "confidence": round(winner_share, 4),
        "method": "majority",
        "vote_distribution": {
            k: round(v / total_weight, 4) for k, v in weighted_votes.items()
        },
    }


def consensus_conservative(
    votes: tuple[AgentVote, ...],
    threshold: float,
) -> dict:
    """Conservative mode — escalate to the highest risk found.

    Used for security/smart-contract domains where missing a risk
    is worse than a false positive. Any agent flagging HIGH_RISK or above
    with confidence >= threshold triggers escalation.
    """
    if not votes:
        return {"verdict": "INCONCLUSIVE", "confidence": 0.0, "method": "conservative"}

    max_severity = max(v.severity for v in votes)
    high_risk_votes = tuple(
        v for v in votes
        if v.severity >= 3 and v.weighted_confidence >= threshold
    )

    if high_risk_votes:
        avg_conf = sum(v.weighted_confidence for v in high_risk_votes) / len(high_risk_votes)
        verdict = SEVERITY_TO_VERDICT.get(max_severity, "HIGH_RISK")
    else:
        # Fall back to weighted average severity
        total_weight = sum(v.weight for v in votes)
        avg_severity = sum(v.severity * v.weight for v in votes) / total_weight if total_weight else 0
        avg_conf = sum(v.weighted_confidence for v in votes) / len(votes)
        verdict = SEVERITY_TO_VERDICT.get(round(avg_severity), "MODERATE_RISK")

    return {
        "verdict": verdict,
        "confidence": round(min(1.0, avg_conf), 4),
        "method": "conservative",
        "escalation_triggers": len(high_risk_votes),
    }


def consensus_union(
    votes: tuple[AgentVote, ...],
    threshold: float,
) -> dict:
    """Union mode — merge all findings, deduplicate by similarity.

    Verdict is determined by the highest severity among findings
    that appear in at least 2 agents (or all if only 1 agent).
    """
    if not votes:
        return {"verdict": "INCONCLUSIVE", "confidence": 0.0, "method": "union"}

    # Use weighted average severity as baseline
    total_weight = sum(v.weight for v in votes)
    avg_severity = sum(v.severity * v.weight for v in votes) / total_weight if total_weight else 0
    avg_conf = sum(v.weighted_confidence for v in votes) / len(votes)

    verdict = SEVERITY_TO_VERDICT.get(round(avg_severity), "MODERATE_RISK")

    return {
        "verdict": verdict,
        "confidence": round(min(1.0, avg_conf), 4),
        "method": "union",
    }


def consensus_diversity(
    votes: tuple[AgentVote, ...],
    threshold: float,
) -> dict:
    """Diversity mode — preserve all perspectives with weighted ranking.

    Returns the full spectrum of verdicts rather than collapsing to one.
    Useful for exploratory analysis where multiple viewpoints matter.
    """
    if not votes:
        return {"verdict": "INCONCLUSIVE", "confidence": 0.0, "method": "diversity"}

    perspectives = []
    for vote in votes:
        perspectives.append({
            "agent_id": vote.agent_id,
            "provider": vote.provider,
            "verdict": vote.verdict,
            "confidence": round(min(1.0, vote.weighted_confidence), 4),
        })

    # Sort by weighted confidence descending
    perspectives.sort(key=lambda p: p["confidence"], reverse=True)

    # Primary verdict = highest weighted confidence
    primary = perspectives[0]

    return {
        "verdict": primary["verdict"],
        "confidence": primary["confidence"],
        "method": "diversity",
        "perspectives": perspectives,
    }


# ---------------------------------------------------------------------------
# Mode Dispatch
# ---------------------------------------------------------------------------

CONSENSUS_MODES = {
    "majority": consensus_majority,
    "conservative": consensus_conservative,
    "union": consensus_union,
    "diversity": consensus_diversity,
}


# ---------------------------------------------------------------------------
# Main Orchestrator
# ---------------------------------------------------------------------------


def aggregate_consensus(input_data: dict) -> dict:
    """Orchestrate the full voting aggregation pipeline.

    Pipeline:
        1. Build weighted votes from agent results
        2. Cluster similar findings across agents
        3. Build agreement map (agreed/disputed/unique)
        4. Run consensus mode to determine final verdict
        5. Assemble structured output
    """
    agent_results = input_data.get("agent_results", [])
    agent_weights = input_data.get("agent_weights", {})
    consensus_mode = input_data.get("consensus_mode", "majority")
    threshold = float(input_data.get("threshold", 0.6))
    domain = input_data.get("domain", "general")

    # Step 1: Build weighted votes
    votes = build_votes(agent_results, agent_weights)

    if not votes:
        return {
            "success": False,
            "error": "No valid agent results to aggregate",
            "consensus": {"verdict": "INCONCLUSIVE", "confidence": 0.0},
        }

    # Step 2: Cluster findings
    clusters = cluster_findings(votes)

    # Step 3: Build agreement map (use valid vote count, not total agents)
    agreement = build_agreement_map(clusters, len(votes))

    # Step 4: Run consensus mode
    mode_fn = CONSENSUS_MODES.get(consensus_mode, consensus_majority)
    consensus = mode_fn(votes, threshold)

    # Step 5: Assemble output
    return {
        "success": True,
        "domain": domain,
        "consensus": consensus,
        "agreement_map": {
            "agreed": [asdict(c) for c in agreement.agreed],
            "disputed": [asdict(c) for c in agreement.disputed],
            "unique": [asdict(c) for c in agreement.unique],
        },
        "statistics": {
            "total_agents": len(agent_results),
            "valid_votes": len(votes),
            "error_agents": len(agent_results) - len(votes),
            "total_findings": sum(len(v.findings) for v in votes),
            "finding_clusters": len(clusters),
            "agreed_findings": len(agreement.agreed),
            "disputed_findings": len(agreement.disputed),
            "unique_findings": len(agreement.unique),
        },
    }


# ---------------------------------------------------------------------------
# Main Entry Point (stdin/stdout JSON protocol)
# ---------------------------------------------------------------------------


def main() -> None:
    """Read JSON from stdin, run aggregation, output JSON to stdout."""
    try:
        input_data = json.loads(sys.stdin.read())
        result = aggregate_consensus(input_data)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Voting aggregation failed: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
