#!/usr/bin/env python3
"""
Skill Composition Engine — Interactive Demo
=============================================
Demonstrates three composition scenarios with progressive complexity:
  1. Pipeline:     Security audit → Report generation (sequential)
  2. Fan-out:      Parallel multi-domain blockchain analysis
  3. Mixed DAG:    Complex DeFi workflow with dependencies

Usage:
    conda activate spoonos-skill
    export DASHSCOPE_API_KEY=your_key
    python demo.py [--no-llm] [--fast]
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
import argparse
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Resolve project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent  # → spoon-awesome-skill/

# Ensure scripts/ is importable (both package-level and sibling imports)
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

from scripts.skill_discovery import run_skill_discovery  # noqa: E402
from scripts.workflow_composer import run_workflow_composer  # noqa: E402

# ---------------------------------------------------------------------------
# ANSI colour helpers (no external deps)
# ---------------------------------------------------------------------------
class C:
    """ANSI escape codes for terminal colours."""
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[36m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    RED     = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE    = "\033[34m"
    WHITE   = "\033[97m"
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_CYAN = "\033[46m"

DELAY = 0.03  # typewriter delay (seconds per char)
FAST  = False


def typed(text: str, *, color: str = "", end: str = "\n") -> None:
    """Print with optional typewriter effect."""
    full = f"{color}{text}{C.RESET}" if color else text
    if FAST:
        print(full, end=end, flush=True)
        return
    for ch in full:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(DELAY)
    sys.stdout.write(end)
    sys.stdout.flush()


def banner(title: str, *, bg: str = C.BG_BLUE) -> None:
    """Print a full-width banner."""
    width = 70
    pad = (width - len(title) - 4) // 2
    print()
    print(f"{bg}{C.WHITE}{C.BOLD}{'═' * width}{C.RESET}")
    print(f"{bg}{C.WHITE}{C.BOLD}{'║'}{' ' * pad}  {title}  {' ' * (width - pad - len(title) - 5)}{'║'}{C.RESET}")
    print(f"{bg}{C.WHITE}{C.BOLD}{'═' * width}{C.RESET}")
    print()


def section(title: str) -> None:
    """Print a section header."""
    print(f"\n{C.CYAN}{C.BOLD}{'─' * 60}{C.RESET}")
    print(f"{C.CYAN}{C.BOLD}  ▸ {title}{C.RESET}")
    print(f"{C.CYAN}{C.BOLD}{'─' * 60}{C.RESET}\n")


def kv(key: str, value: Any, *, indent: int = 4) -> None:
    """Print a key-value pair."""
    print(f"{' ' * indent}{C.DIM}{key}:{C.RESET} {C.WHITE}{value}{C.RESET}")


def ok(msg: str) -> None:
    print(f"  {C.GREEN}✓{C.RESET} {msg}")


def warn(msg: str) -> None:
    print(f"  {C.YELLOW}⚠{C.RESET} {msg}")


def err(msg: str) -> None:
    print(f"  {C.RED}✗{C.RESET} {msg}")


# ---------------------------------------------------------------------------
# Graph visualisation (ASCII art)
# ---------------------------------------------------------------------------

def render_graph_ascii(graph: dict) -> str:
    """Render a StateGraph definition as ASCII art."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    # Build adjacency
    adj: dict[str, list[str]] = {}
    for e in edges:
        adj.setdefault(e["source"], []).append(e["target"])

    # Find layers via BFS from __start__
    layers: list[list[str]] = []
    visited: set[str] = set()
    current = ["__start__"]
    while current:
        layers.append(current)
        visited.update(current)
        nxt: list[str] = []
        for n in current:
            for t in adj.get(n, []):
                if t not in visited and t not in nxt:
                    nxt.append(t)
        current = nxt

    lines: list[str] = []
    for i, layer in enumerate(layers):
        if len(layer) == 1:
            node = layer[0]
            icon = "◉" if node in ("__start__", "__end__") else "◆"
            color = C.GREEN if node == "__end__" else C.CYAN
            label = node.replace("_", " ").title()
            lines.append(f"    {color}{icon} [{label}]{C.RESET}")
        else:
            # Parallel nodes
            lines.append(f"    {C.YELLOW}┌{'─' * 40}┐{C.RESET}")
            for j, node in enumerate(layer):
                prefix = "├" if j < len(layer) - 1 else "└"
                lines.append(
                    f"    {C.YELLOW}{prefix}── ◆ [{node.replace('_', ' ').title()}]{C.RESET}"
                )
            lines.append(f"    {C.YELLOW}└{'─' * 40}┘{C.RESET}")

        if i < len(layers) - 1:
            lines.append(f"    {C.DIM}    │{C.RESET}")
            lines.append(f"    {C.DIM}    ▼{C.RESET}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo scenarios
# ---------------------------------------------------------------------------

SCENARIOS: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Pipeline — DeFi Security Audit + Report",
        "description": (
            "A user wants to audit a DeFi protocol's smart contracts and "
            "generate a security report. The engine discovers security-analysis "
            "and documentation skills, then composes them into a sequential pipeline."
        ),
        "query": "analyze DeFi protocol security vulnerabilities and generate audit report",
        "expected_strategy": "pipeline",
        "bg": C.BG_BLUE,
    },
    {
        "id": 2,
        "title": "Fan-out — Multi-Domain Blockchain Analysis",
        "description": (
            "A user needs comprehensive blockchain intelligence: on-chain data "
            "analysis, wallet tracking, and token economics — all independent. "
            "The engine detects no data-flow dependencies and generates a "
            "parallel fan-out/fan-in graph."
        ),
        "query": "comprehensive blockchain analysis with on-chain data, wallet tracking, and DeFi protocol review",
        "expected_strategy": "fan_out_fan_in",
        "bg": C.BG_GREEN,
    },
    {
        "id": 3,
        "title": "Mixed DAG — DAO Governance + Identity + Bridge",
        "description": (
            "A complex cross-domain request: build a DAO governance tool that "
            "requires identity verification before voting, and cross-chain "
            "bridge integration for multi-chain governance. The engine detects "
            "mixed dependencies and generates a DAG."
        ),
        "query": "build DAO governance system with identity verification for voting and cross-chain bridge for multi-chain token governance",
        "expected_strategy": "mixed",
        "bg": C.BG_CYAN,
    },
]


# ---------------------------------------------------------------------------
# Core demo runner
# ---------------------------------------------------------------------------

def print_matches(matches: list[dict]) -> None:
    """Pretty-print discovered skill matches."""
    if not matches:
        warn("No skills matched this query")
        return

    print(f"\n  {C.BOLD}{'Rank':<6}{'Skill':<35}{'Score':<10}{'Tier':<12}{C.RESET}")
    print(f"  {'─' * 62}")
    for i, m in enumerate(matches, 1):
        score = m.get("score", 0)
        tier = m.get("tier", "unknown")
        name = m.get("skill_name", "?")
        sc = C.GREEN if score >= 0.7 else C.YELLOW if score >= 0.4 else C.RED
        print(
            f"  {C.DIM}{i:<6}{C.RESET}"
            f"{C.WHITE}{name:<35}{C.RESET}"
            f"{sc}{score:<10.3f}{C.RESET}"
            f"{C.MAGENTA}{tier:<12}{C.RESET}"
        )


def print_confidence(confidence: dict) -> None:
    """Pretty-print composition confidence metrics."""
    coverage = confidence.get("coverage", 0)
    compat = confidence.get("compatibility", 0)
    rec = confidence.get("recommendation", "UNKNOWN")

    rec_color = {
        "COMPOSE": C.GREEN,
        "PARTIAL_COMPOSE": C.YELLOW,
        "MANUAL_REVIEW": C.RED,
    }.get(rec, C.WHITE)

    print(f"\n  {C.BOLD}Composition Confidence{C.RESET}")
    print(f"  {'─' * 40}")

    bar_len = 30
    cov_filled = int(coverage * bar_len)
    cov_bar = f"{'█' * cov_filled}{'░' * (bar_len - cov_filled)}"
    print(f"    Coverage:      {C.CYAN}{cov_bar}{C.RESET} {coverage:.1%}")

    com_filled = int(compat * bar_len)
    com_bar = f"{'█' * com_filled}{'░' * (bar_len - com_filled)}"
    print(f"    Compatibility: {C.CYAN}{com_bar}{C.RESET} {compat:.1%}")

    print(f"    Recommendation: {rec_color}{C.BOLD}{rec}{C.RESET}")


async def run_scenario(scenario: dict, *, provider: str, use_llm: bool) -> None:
    """Run a single demo scenario end-to-end."""
    banner(
        f"Scenario {scenario['id']}: {scenario['title']}",
        bg=scenario["bg"],
    )

    typed(f"  {scenario['description']}", color=C.DIM)
    print()

    # Show query
    section("Step 1 — User Query")
    typed(f'  "{scenario["query"]}"', color=C.YELLOW)

    # Phase 1: Skill Discovery
    section("Step 2 — Skill Discovery (scan → match → rank)")
    typed("  Scanning skill registry...", color=C.DIM)

    discovery_input = {
        "query": scenario["query"],
        "skill_registry_path": str(PROJECT_ROOT),
        "max_skills": 5,
        "provider": provider,
        "use_llm": use_llm,
    }

    t0 = time.time()
    discovery_result = await run_skill_discovery(discovery_input)
    t_disc = time.time() - t0

    if discovery_result.get("error"):
        err(f"Discovery failed: {discovery_result['error']}")
        return

    ok(
        f"Scanned {discovery_result.get('total_skills_scanned', 0)} "
        f"skills in {t_disc:.1f}s"
    )
    ok(f"Found {discovery_result.get('matches_found', 0)} matching skills")
    if use_llm:
        ok(f"LLM provider: {provider}")
    else:
        warn("LLM disabled — using keyword + tag heuristics only")

    matches = discovery_result.get("matches", [])
    print_matches(matches)

    # Phase 2: Workflow Composition
    section("Step 3 — Workflow Composition (deps → strategy → StateGraph)")
    typed("  Analyzing dependencies and generating workflow...", color=C.DIM)

    composer_input = {
        "query": scenario["query"],
        "matches": matches,
        "execution_mode": "auto",
        "provider": provider,
        "use_llm": use_llm,
    }

    t0 = time.time()
    compose_result = await run_workflow_composer(composer_input)
    t_comp = time.time() - t0

    if compose_result.get("error"):
        err(f"Composition failed: {compose_result['error']}")
        return

    strategy = compose_result.get("strategy", "unknown")
    exec_mode = compose_result.get("execution_mode", "unknown")
    skill_count = compose_result.get("skill_count", 0)

    ok(f"Strategy detected: {C.BOLD}{strategy}{C.RESET}")
    ok(f"Execution mode: {exec_mode}")
    ok(f"Skills composed: {skill_count}")
    ok(f"Composition time: {t_comp:.1f}s")

    # Show graph
    graph = compose_result.get("graph", {})
    if graph:
        section("Step 4 — Generated StateGraph")
        print(render_graph_ascii(graph))

    # Show confidence
    confidence = compose_result.get("confidence", {})
    if confidence:
        print_confidence(confidence)

    # Summary
    print(f"\n  {C.GREEN}{C.BOLD}{'━' * 50}{C.RESET}")
    print(
        f"  {C.GREEN}{C.BOLD}  ✓ Scenario {scenario['id']} complete"
        f" — {strategy} workflow generated{C.RESET}"
    )
    print(f"  {C.GREEN}{C.BOLD}{'━' * 50}{C.RESET}")
    time.sleep(1.0 if not FAST else 0.2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def async_main(provider: str, use_llm: bool) -> None:
    """Run all demo scenarios."""
    banner("Skill Composition Engine — Live Demo", bg=C.BG_BLUE)

    typed("  SpoonOS Skill Composition Engine", color=C.BOLD)
    typed("  Automatic workflow orchestration from skill metadata", color=C.DIM)
    print()
    kv("Skill Registry", str(PROJECT_ROOT))
    kv("LLM Provider", provider if use_llm else "disabled (heuristic only)")
    kv("Scenarios", len(SCENARIOS))
    print()

    time.sleep(1.0 if not FAST else 0.2)

    for scenario in SCENARIOS:
        await run_scenario(scenario, provider=provider, use_llm=use_llm)
        print("\n")

    # Final summary
    banner("Demo Complete", bg=C.BG_GREEN)
    typed("  The Skill Composition Engine demonstrated:", color=C.WHITE)
    print()
    ok("Three-layer skill matching (keyword → tag → LLM semantic)")
    ok("Automatic dependency analysis between skills")
    ok("Strategy detection (pipeline / fan-out / mixed DAG)")
    ok("StateGraph generation ready for SpoonOS execution")
    ok("Confidence scoring with actionable recommendations")
    print()
    typed(
        "  Skills become composable building blocks, not isolated tools.",
        color=C.CYAN,
    )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill Composition Engine Demo")
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Disable LLM semantic matching (heuristic only)",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Disable typewriter effect for faster output",
    )
    parser.add_argument(
        "--provider",
        default="qwen",
        choices=["openai", "anthropic", "deepseek", "qwen"],
        help="LLM provider (default: qwen)",
    )
    args = parser.parse_args()

    global FAST
    FAST = args.fast

    use_llm = not args.no_llm
    asyncio.run(async_main(args.provider, use_llm))


if __name__ == "__main__":
    main()
