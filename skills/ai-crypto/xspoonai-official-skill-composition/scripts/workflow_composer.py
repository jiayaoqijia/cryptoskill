#!/usr/bin/env python3
"""Workflow Composer — Auto-generate StateGraph workflows from discovered skills.

This script is the second stage of the Skill Composition Engine pipeline:
    skill_discovery.py → workflow_composer.py

It receives matched skills from the discovery stage, analyzes data-flow
dependencies between them, and generates a StateGraph DAG definition that
SpoonOS can execute directly.

Composition Strategies:
    Pipeline        — Linear data transformation (A → B → C)
    Fan-out/Fan-in  — Independent analyses (A → [B, C, D] → Aggregate)
    Conditional     — Domain-dependent routing (A → if(X) B else C)
    Mixed           — Complex DAG with multiple patterns combined

stdin/stdout JSON protocol (SpoonOS compatible):
    echo '{"matches": [...], "execution_mode": "auto"}' | python workflow_composer.py

Dependencies: Python 3.10+, _llm_client.py (shared LLM module).
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, FrozenSet, Tuple

from _llm_client import extract_json, llm_chat, load_env


# ---------------------------------------------------------------------------
# Environment bootstrap
# ---------------------------------------------------------------------------

load_env()


# ---------------------------------------------------------------------------
# Domain Types (immutable)
# ---------------------------------------------------------------------------

class ExecutionMode(Enum):
    """How skills should be orchestrated in the workflow."""
    AUTO = "auto"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    MIXED = "mixed"


class CompositionStrategy(Enum):
    """High-level composition pattern detected."""
    DIRECT = "direct"           # Single skill, no composition
    PIPELINE = "pipeline"       # A → B → C
    FAN_OUT_FAN_IN = "fan_out_fan_in"  # A → [B, C] → Aggregate
    CONDITIONAL = "conditional" # A → if(X) B else C
    MIXED_DAG = "mixed_dag"     # Complex multi-pattern


class Recommendation(Enum):
    """Composition confidence recommendation."""
    COMPOSE = "COMPOSE"
    PARTIAL_COMPOSE = "PARTIAL_COMPOSE"
    MANUAL_REVIEW = "MANUAL_REVIEW"


@dataclass(frozen=True)
class SkillNode:
    """A node in the composition graph representing one skill."""
    node_id: str
    skill_name: str
    score: float
    tier: str
    description: str
    scripts: Tuple[str, ...]
    parameters: Tuple[dict, ...]
    tags: FrozenSet[str]
    composable: bool


@dataclass(frozen=True)
class GraphEdge:
    """A directed edge in the StateGraph."""
    source: str
    target: str
    condition: str = ""       # Empty means unconditional
    data_mapping: str = ""    # Describes what data flows along this edge


@dataclass(frozen=True)
class DependencyInfo:
    """Dependency analysis result for a pair of skills."""
    source_skill: str
    target_skill: str
    dependency_type: str      # "data_flow" | "semantic" | "none"
    confidence: float
    reasoning: str


@dataclass(frozen=True)
class StateGraphDefinition:
    """Complete StateGraph definition ready for SpoonOS execution."""
    nodes: Tuple[dict, ...]
    edges: Tuple[dict, ...]
    entry_point: str
    terminal_nodes: Tuple[str, ...]
    execution_mode: str
    strategy: str
    state_schema: dict
    estimated_steps: int


@dataclass(frozen=True)
class CompositionResult:
    """Final output of the workflow composer."""
    success: bool
    query: str
    skill_count: int
    strategy: str
    execution_mode: str
    graph: dict
    dependency_analysis: Tuple[dict, ...]
    confidence: dict
    recommendation: str
    elapsed_ms: int
    error: str = ""



# ---------------------------------------------------------------------------
# Skill Node Parsing (from discovery output)
# ---------------------------------------------------------------------------

def _sanitize_node_id(name: str) -> str:
    """Convert a skill name to a valid graph node ID."""
    return name.lower().replace(" ", "_").replace("-", "_")


def parse_skill_nodes(matches: list[dict]) -> tuple[SkillNode, ...]:
    """Parse discovery output matches into immutable SkillNode objects."""
    nodes: list[SkillNode] = []
    for match in matches:
        meta = match.get("metadata", {})
        node = SkillNode(
            node_id=_sanitize_node_id(match.get("skill_name", "")),
            skill_name=match.get("skill_name", ""),
            score=float(match.get("score", 0.0)),
            tier=match.get("tier", "none"),
            description=meta.get("description", ""),
            scripts=tuple(meta.get("scripts", [])),
            parameters=tuple(meta.get("parameters", [])),
            tags=frozenset(meta.get("tags", [])),
            composable=meta.get("composable", True),
        )
        nodes.append(node)
    return tuple(nodes)


# ---------------------------------------------------------------------------
# Tag-Based Dependency Detection (heuristic, no LLM needed)
# ---------------------------------------------------------------------------

# Semantic tag groups that imply data-flow relationships
_TAG_FLOW_PAIRS: tuple[tuple[frozenset[str], frozenset[str], str], ...] = (
    (frozenset({"security", "audit", "vulnerability"}),
     frozenset({"report", "summary", "documentation"}),
     "Security analysis feeds into reporting"),
    (frozenset({"defi", "finance", "trading"}),
     frozenset({"risk", "security", "audit"}),
     "Financial data feeds into risk analysis"),
    (frozenset({"analysis", "research", "data"}),
     frozenset({"visualization", "report", "dashboard"}),
     "Analysis results feed into visualization"),
    (frozenset({"smart-contract", "solidity", "evm"}),
     frozenset({"testing", "verification", "formal-verification"}),
     "Contract code feeds into verification"),
    (frozenset({"extraction", "parsing", "scraping"}),
     frozenset({"analysis", "processing", "transformation"}),
     "Extracted data feeds into analysis"),
)


def _detect_tag_dependency(
    source: SkillNode, target: SkillNode
) -> DependencyInfo | None:
    """Detect data-flow dependency between two skills via tag overlap."""
    for src_tags, tgt_tags, reasoning in _TAG_FLOW_PAIRS:
        src_overlap = source.tags & src_tags
        tgt_overlap = target.tags & tgt_tags
        if src_overlap and tgt_overlap:
            confidence = min(1.0, (len(src_overlap) + len(tgt_overlap)) / 4.0)
            return DependencyInfo(
                source_skill=source.node_id,
                target_skill=target.node_id,
                dependency_type="data_flow",
                confidence=confidence,
                reasoning=reasoning,
            )
    return None


# ---------------------------------------------------------------------------
# LLM-Based Dependency Analysis
# ---------------------------------------------------------------------------

_DEPENDENCY_PROMPT_TEMPLATE = """Analyze the data-flow dependencies between these skills.

Skills:
{skills_json}

User Query: {query}

For each pair of skills, determine:
1. Is there a data-flow dependency? (one skill's output feeds another's input)
2. What is the dependency direction? (which skill produces, which consumes)
3. Confidence level (0.0 to 1.0)

Respond in JSON format:
{{
  "dependencies": [
    {{
      "source": "skill_node_id",
      "target": "skill_node_id",
      "type": "data_flow",
      "confidence": 0.85,
      "reasoning": "brief explanation"
    }}
  ],
  "independent_skills": ["skill_ids that have no dependencies"]
}}

IMPORTANT: Only include real dependencies. If skills are independent, say so.
Respond with ONLY the JSON object, no markdown fences."""


async def analyze_dependencies_llm(
    nodes: tuple[SkillNode, ...],
    query: str,
    provider: str = "openai",
) -> list[DependencyInfo]:
    """Use LLM to analyze data-flow dependencies between skills."""
    if len(nodes) < 2:
        return []

    skills_desc = json.dumps([
        {
            "node_id": n.node_id,
            "name": n.skill_name,
            "description": n.description,
            "tags": list(n.tags),
        }
        for n in nodes
    ], indent=2)

    prompt = _DEPENDENCY_PROMPT_TEMPLATE.format(
        skills_json=skills_desc, query=query
    )

    raw = await llm_chat(
        messages=[{"role": "user", "content": prompt}],
        provider=provider,
        system="You are a workflow composition expert.",
        temperature=0.2,
        max_tokens=2048,
    )
    if not raw:
        return []

    data = extract_json(raw)
    if not isinstance(data, dict):
        return []

    deps: list[DependencyInfo] = []
    valid_ids = {n.node_id for n in nodes}

    for dep in data.get("dependencies", []):
        src = dep.get("source", "")
        tgt = dep.get("target", "")
        if src in valid_ids and tgt in valid_ids and src != tgt:
            deps.append(DependencyInfo(
                source_skill=src,
                target_skill=tgt,
                dependency_type=dep.get("type", "data_flow"),
                confidence=min(1.0, max(0.0, float(dep.get("confidence", 0.5)))),
                reasoning=dep.get("reasoning", ""),
            ))
    return deps


# ---------------------------------------------------------------------------
# Composite Dependency Analysis (heuristic + LLM)
# ---------------------------------------------------------------------------

async def analyze_all_dependencies(
    nodes: tuple[SkillNode, ...],
    query: str,
    provider: str = "openai",
    use_llm: bool = True,
) -> tuple[DependencyInfo, ...]:
    """Combine tag-based heuristics with LLM analysis for dependency detection."""
    all_deps: dict[tuple[str, str], DependencyInfo] = {}

    # Layer 1: Tag-based heuristic detection
    for i, src in enumerate(nodes):
        for j, tgt in enumerate(nodes):
            if i == j:
                continue
            dep = _detect_tag_dependency(src, tgt)
            if dep is not None:
                key = (dep.source_skill, dep.target_skill)
                all_deps[key] = dep

    # Layer 2: LLM-based semantic analysis (if enabled)
    if use_llm and len(nodes) >= 2:
        llm_deps = await analyze_dependencies_llm(nodes, query, provider)
        for dep in llm_deps:
            key = (dep.source_skill, dep.target_skill)
            if key in all_deps:
                # Merge: keep higher confidence
                existing = all_deps[key]
                if dep.confidence > existing.confidence:
                    all_deps[key] = dep
            else:
                all_deps[key] = dep

    return tuple(all_deps.values())


# ---------------------------------------------------------------------------
# Strategy Detection
# ---------------------------------------------------------------------------

def detect_strategy(
    nodes: tuple[SkillNode, ...],
    deps: tuple[DependencyInfo, ...],
    requested_mode: ExecutionMode,
) -> CompositionStrategy:
    """Determine the optimal composition strategy from dependency graph."""
    if len(nodes) <= 1:
        return CompositionStrategy.DIRECT

    # User override
    if requested_mode == ExecutionMode.SEQUENTIAL:
        return CompositionStrategy.PIPELINE
    if requested_mode == ExecutionMode.PARALLEL:
        return CompositionStrategy.FAN_OUT_FAN_IN

    # Auto-detect from dependency structure
    if not deps:
        return CompositionStrategy.FAN_OUT_FAN_IN

    # Build adjacency sets
    has_incoming: set[str] = set()
    has_outgoing: set[str] = set()
    for dep in deps:
        has_outgoing.add(dep.source_skill)
        has_incoming.add(dep.target_skill)

    all_ids = {n.node_id for n in nodes}
    roots = all_ids - has_incoming      # No incoming edges
    leaves = all_ids - has_outgoing     # No outgoing edges
    independent = all_ids - has_incoming - has_outgoing

    # Pure linear chain: each node has at most 1 in and 1 out
    in_count: dict[str, int] = {}
    out_count: dict[str, int] = {}
    for dep in deps:
        out_count[dep.source_skill] = out_count.get(dep.source_skill, 0) + 1
        in_count[dep.target_skill] = in_count.get(dep.target_skill, 0) + 1

    is_linear = all(
        out_count.get(nid, 0) <= 1 and in_count.get(nid, 0) <= 1
        for nid in all_ids
    )

    if is_linear and not independent:
        return CompositionStrategy.PIPELINE

    # Fan-out/fan-in: single root fans out, single aggregation point
    if len(roots) == 1 and len(leaves) == 1 and len(independent) == 0:
        return CompositionStrategy.FAN_OUT_FAN_IN

    return CompositionStrategy.MIXED_DAG


# ---------------------------------------------------------------------------
# Topological Sort (for execution ordering)
# ---------------------------------------------------------------------------

def _topological_sort(
    node_ids: frozenset[str],
    deps: tuple[DependencyInfo, ...],
) -> list[str]:
    """Kahn's algorithm for topological ordering. Falls back to score order."""
    in_degree: dict[str, int] = {nid: 0 for nid in node_ids}
    adjacency: dict[str, list[str]] = {nid: [] for nid in node_ids}

    for dep in deps:
        if dep.source_skill in node_ids and dep.target_skill in node_ids:
            adjacency[dep.source_skill].append(dep.target_skill)
            in_degree[dep.target_skill] = in_degree.get(dep.target_skill, 0) + 1

    queue = sorted(nid for nid, deg in in_degree.items() if deg == 0)
    result: list[str] = []

    while queue:
        current = queue.pop(0)
        result.append(current)
        for neighbor in sorted(adjacency.get(current, [])):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If cycle detected, append remaining nodes
    remaining = [nid for nid in node_ids if nid not in result]
    result.extend(sorted(remaining))

    return result


# ---------------------------------------------------------------------------
# StateGraph Generation
# ---------------------------------------------------------------------------

def _build_state_schema(nodes: tuple[SkillNode, ...]) -> dict:
    """Generate a state schema for the composed workflow."""
    properties: dict[str, dict] = {
        "query": {"type": "string", "description": "Original user query"},
        "current_step": {"type": "string", "description": "Active node ID"},
        "completed_steps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of completed node IDs",
        },
        "results": {
            "type": "object",
            "description": "Accumulated results keyed by node ID",
        },
        "errors": {
            "type": "array",
            "items": {"type": "object"},
            "description": "Error records from failed nodes",
        },
    }
    # Add per-skill output slots
    for node in nodes:
        properties[f"{node.node_id}_output"] = {
            "type": "object",
            "description": f"Output from {node.skill_name}",
        }
    return {
        "type": "object",
        "properties": properties,
        "required": ["query", "current_step"],
    }


def generate_state_graph(
    nodes: tuple[SkillNode, ...],
    deps: tuple[DependencyInfo, ...],
    strategy: CompositionStrategy,
    execution_mode: ExecutionMode,
) -> StateGraphDefinition:
    """Generate a complete StateGraph definition from nodes and dependencies."""
    if not nodes:
        return StateGraphDefinition(
            nodes=(),
            edges=(),
            entry_point="__start__",
            terminal_nodes=("__end__",),
            execution_mode=execution_mode.value,
            strategy=strategy.value,
            state_schema={},
            estimated_steps=0,
        )

    node_ids = frozenset(n.node_id for n in nodes)
    node_map = {n.node_id: n for n in nodes}
    ordered = _topological_sort(node_ids, deps)

    # Build graph nodes (including utility nodes)
    graph_nodes: list[dict] = [
        {"id": "__start__", "type": "entry", "label": "Start"},
    ]
    for nid in ordered:
        n = node_map[nid]
        graph_nodes.append({
            "id": nid,
            "type": "skill",
            "label": n.skill_name,
            "scripts": list(n.scripts),
            "parameters": list(n.parameters),
        })

    # Add aggregator for fan-out/fan-in and mixed strategies
    needs_aggregator = strategy in (
        CompositionStrategy.FAN_OUT_FAN_IN,
        CompositionStrategy.MIXED_DAG,
    )
    if needs_aggregator:
        graph_nodes.append({
            "id": "__aggregate__",
            "type": "aggregator",
            "label": "Aggregate Results",
        })

    graph_nodes.append({"id": "__end__", "type": "terminal", "label": "End"})

    # Build edges based on strategy
    graph_edges: list[dict] = []

    if strategy == CompositionStrategy.DIRECT:
        # Single skill: start → skill → end
        nid = ordered[0]
        graph_edges.append(_edge("__start__", nid))
        graph_edges.append(_edge(nid, "__end__"))

    elif strategy == CompositionStrategy.PIPELINE:
        # Linear chain: start → A → B → C → end
        graph_edges.append(_edge("__start__", ordered[0]))
        for i in range(len(ordered) - 1):
            dep_info = _find_dep(deps, ordered[i], ordered[i + 1])
            mapping = dep_info.reasoning if dep_info else ""
            graph_edges.append(_edge(ordered[i], ordered[i + 1], data_mapping=mapping))
        graph_edges.append(_edge(ordered[-1], "__end__"))

    elif strategy == CompositionStrategy.FAN_OUT_FAN_IN:
        # Parallel: start → [all skills] → aggregate → end
        for nid in ordered:
            graph_edges.append(_edge("__start__", nid))
            graph_edges.append(_edge(nid, "__aggregate__"))
        graph_edges.append(_edge("__aggregate__", "__end__"))

    else:
        # Mixed DAG: use dependency edges + fill gaps
        dep_sources = {d.source_skill for d in deps}
        dep_targets = {d.target_skill for d in deps}
        roots = node_ids - dep_targets
        leaves = node_ids - dep_sources

        # Connect start to roots
        for root in sorted(roots):
            graph_edges.append(_edge("__start__", root))

        # Add dependency edges
        for dep in deps:
            graph_edges.append(_edge(
                dep.source_skill,
                dep.target_skill,
                data_mapping=dep.reasoning,
            ))

        # Connect leaves to aggregator or end
        terminal = "__aggregate__" if needs_aggregator else "__end__"
        for leaf in sorted(leaves):
            graph_edges.append(_edge(leaf, terminal))

        if needs_aggregator:
            graph_edges.append(_edge("__aggregate__", "__end__"))

    # Determine terminal nodes
    terminal_nodes = ("__end__",)
    estimated_steps = len(nodes) + (1 if needs_aggregator else 0)

    return StateGraphDefinition(
        nodes=tuple(graph_nodes),
        edges=tuple(graph_edges),
        entry_point="__start__",
        terminal_nodes=terminal_nodes,
        execution_mode=execution_mode.value,
        strategy=strategy.value,
        state_schema=_build_state_schema(nodes),
        estimated_steps=estimated_steps,
    )


def _edge(
    source: str,
    target: str,
    condition: str = "",
    data_mapping: str = "",
) -> dict:
    """Create an edge dict for the StateGraph definition."""
    edge = {"source": source, "target": target}
    if condition:
        edge["condition"] = condition
    if data_mapping:
        edge["data_mapping"] = data_mapping
    return edge


def _find_dep(
    deps: tuple[DependencyInfo, ...], src: str, tgt: str
) -> DependencyInfo | None:
    """Find a dependency between two specific nodes."""
    for dep in deps:
        if dep.source_skill == src and dep.target_skill == tgt:
            return dep
    return None


# ---------------------------------------------------------------------------
# Confidence Scoring
# ---------------------------------------------------------------------------

def compute_confidence(
    nodes: tuple[SkillNode, ...],
    deps: tuple[DependencyInfo, ...],
    strategy: CompositionStrategy,
) -> dict:
    """Compute composition confidence metrics."""
    if not nodes:
        return {"coverage": 0.0, "compatibility": 0.0, "recommendation": Recommendation.MANUAL_REVIEW.value}

    # Coverage: average match score of selected skills
    avg_score = sum(n.score for n in nodes) / len(nodes)
    coverage = min(1.0, avg_score)

    # Compatibility: based on dependency confidence and composability flags
    composable_ratio = sum(1 for n in nodes if n.composable) / len(nodes)
    dep_confidence = (
        sum(d.confidence for d in deps) / len(deps) if deps else 0.5
    )
    compatibility = composable_ratio * 0.6 + dep_confidence * 0.4

    # Recommendation
    combined = coverage * 0.5 + compatibility * 0.5
    if combined >= 0.7:
        rec = Recommendation.COMPOSE
    elif combined >= 0.4:
        rec = Recommendation.PARTIAL_COMPOSE
    else:
        rec = Recommendation.MANUAL_REVIEW

    return {
        "coverage": round(coverage, 3),
        "compatibility": round(compatibility, 3),
        "recommendation": rec.value,
    }


# ---------------------------------------------------------------------------
# Serialization Helpers
# ---------------------------------------------------------------------------

def _dep_to_dict(dep: DependencyInfo) -> dict:
    """Serialize a DependencyInfo to JSON-compatible dict."""
    return {
        "source": dep.source_skill,
        "target": dep.target_skill,
        "type": dep.dependency_type,
        "confidence": round(dep.confidence, 3),
        "reasoning": dep.reasoning,
    }


def _graph_to_dict(graph: StateGraphDefinition) -> dict:
    """Serialize a StateGraphDefinition to JSON-compatible dict."""
    return {
        "nodes": list(graph.nodes),
        "edges": list(graph.edges),
        "entry_point": graph.entry_point,
        "terminal_nodes": list(graph.terminal_nodes),
        "execution_mode": graph.execution_mode,
        "strategy": graph.strategy,
        "state_schema": graph.state_schema,
        "estimated_steps": graph.estimated_steps,
    }


# ---------------------------------------------------------------------------
# Main Composition Pipeline
# ---------------------------------------------------------------------------

async def run_workflow_composer(input_data: dict) -> dict:
    """Main entry point: compose a StateGraph workflow from discovered skills.

    StateGraph node mapping:
        graph.add_node("compose", run_workflow_composer)
        graph.add_edge("discover", "compose")
        graph.add_edge("compose", "end")

    Expected input (from skill_discovery.py output or direct):
        {
            "query": "user intent",
            "matches": [...],           # from skill_discovery output
            "execution_mode": "auto",   # auto|sequential|parallel|mixed
            "provider": "openai",
            "use_llm": true
        }
    """
    query = input_data.get("query", "")
    if not query:
        return {"error": "Missing required parameter: query"}

    matches = input_data.get("matches", [])
    if not matches:
        return {
            "success": True,
            "query": query,
            "skill_count": 0,
            "strategy": CompositionStrategy.DIRECT.value,
            "execution_mode": "auto",
            "graph": {},
            "dependency_analysis": [],
            "confidence": {"coverage": 0.0, "compatibility": 0.0, "recommendation": "MANUAL_REVIEW"},
            "recommendation": "MANUAL_REVIEW",
            "elapsed_ms": 0,
            "message": "No skills matched the query. Consider broadening the search.",
        }

    mode_str = input_data.get("execution_mode", "auto").lower()
    try:
        execution_mode = ExecutionMode(mode_str)
    except ValueError:
        execution_mode = ExecutionMode.AUTO

    provider = input_data.get("provider", "openai")
    use_llm = input_data.get("use_llm", True)

    start_ms = int(time.time() * 1000)

    # Step 1: Parse skill nodes from discovery output
    nodes = parse_skill_nodes(matches)

    # Step 2: Analyze dependencies
    deps = await analyze_all_dependencies(nodes, query, provider, use_llm)

    # Step 3: Detect optimal strategy
    strategy = detect_strategy(nodes, deps, execution_mode)

    # Step 4: Resolve execution mode (auto → detected)
    if execution_mode == ExecutionMode.AUTO:
        if strategy == CompositionStrategy.PIPELINE:
            execution_mode = ExecutionMode.SEQUENTIAL
        elif strategy == CompositionStrategy.FAN_OUT_FAN_IN:
            execution_mode = ExecutionMode.PARALLEL
        else:
            execution_mode = ExecutionMode.MIXED

    # Step 5: Generate StateGraph
    graph = generate_state_graph(nodes, deps, strategy, execution_mode)

    # Step 6: Compute confidence
    confidence = compute_confidence(nodes, deps, strategy)

    elapsed_ms = int(time.time() * 1000) - start_ms

    return {
        "success": True,
        "query": query,
        "skill_count": len(nodes),
        "strategy": strategy.value,
        "execution_mode": execution_mode.value,
        "graph": _graph_to_dict(graph),
        "dependency_analysis": [_dep_to_dict(d) for d in deps],
        "confidence": confidence,
        "recommendation": confidence["recommendation"],
        "elapsed_ms": elapsed_ms,
    }


# ---------------------------------------------------------------------------
# Main Entry Point (stdin/stdout JSON protocol)
# ---------------------------------------------------------------------------

def main() -> None:
    """Read JSON from stdin, compose workflow, output JSON to stdout."""
    try:
        input_data = json.loads(sys.stdin.read())
        result = asyncio.run(run_workflow_composer(input_data))
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Workflow composition failed: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()

