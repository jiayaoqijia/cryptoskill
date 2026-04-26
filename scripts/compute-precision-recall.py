#!/usr/bin/env python3
"""
Compute per-capability precision and Wilson 95% lower-bound recall from
the verification holdout (docs/phase1-verification/holdout-v0.yaml) and
the current extractor output (docs/capabilities.json).

Outputs a Markdown table to stdout (suitable for committing to
docs/phase1-verification/precision-recall.md) and prints PASS/FAIL per
capability against the recall floors in TRUST.md.

Implements the protocol in TRUST.md §"Phase 1 verification protocol":
- Critical subset: can_move_funds, requires_private_key, can_install_code,
  uses_remote_install_script, requires_hosted_operator
- Floors: 0.90 / 0.90 / 0.85 / 0.85 / 0.80 (Wilson lower bound)
- Min positive support N: 50 / 50 / 50 / 30 / 50
"""

import json
import math
import sys
from pathlib import Path

from canonicalize import parse_canonical_yaml

ROOT = Path(__file__).resolve().parent.parent
HOLDOUT = ROOT / "docs" / "phase1-verification" / "holdout-v0.yaml"
CAPS_JSON = ROOT / "docs" / "capabilities.json"

# (capability, recall_floor, min_positive_support_N)
CRITICAL = [
    ("can_move_funds", 0.90, 50),
    ("requires_private_key", 0.90, 50),
    ("can_install_code", 0.85, 50),
    ("uses_remote_install_script", 0.85, 30),
    ("requires_hosted_operator", 0.80, 50),
]
NON_CRITICAL = [
    "auto_invocable", "can_execute_shell", "can_write_files",
    "can_browse_web", "can_spawn_subagents", "mutable_remote_runtime",
]


def wilson_lower(p_hat: float, n: int, z: float = 1.96) -> float:
    """One-sided Wilson lower bound at 95% confidence (z=1.96)."""
    if n == 0:
        return 0.0
    denom = 1 + z * z / n
    centre = p_hat + z * z / (2 * n)
    half = z * math.sqrt(p_hat * (1 - p_hat) / n + z * z / (4 * n * n))
    return max(0.0, (centre - half) / denom)


def load_holdout():
    if not HOLDOUT.exists():
        print(f"holdout not present: {HOLDOUT}", file=sys.stderr)
        return {"entries": [], "status": "missing"}
    text = HOLDOUT.read_text(encoding="utf-8")
    return parse_canonical_yaml(text)


def load_extractor_output():
    if not CAPS_JSON.exists():
        print(f"capabilities.json not present: {CAPS_JSON}", file=sys.stderr)
        sys.exit(1)
    return json.loads(CAPS_JSON.read_text(encoding="utf-8"))


def evaluate(holdout: dict, extractor: dict):
    """For each capability, count TP / FP / FN against the holdout."""
    skills = extractor.get("skills", {})
    stats = {}
    all_caps = [c for c, _, _ in CRITICAL] + NON_CRITICAL
    for cap in all_caps:
        stats[cap] = {"tp": 0, "fp": 0, "fn": 0, "tn": 0, "unknown_human": 0}

    for entry in holdout.get("entries") or []:
        skill_path = entry["skill"]
        labels = entry.get("labels") or {}
        ext = (skills.get(skill_path) or {}).get("capabilities") or {}
        for cap in all_caps:
            human = labels.get(cap)
            ext_v = ext.get(cap)
            # Normalize tri-state representations.
            if isinstance(ext_v, dict):
                ext_v = ext_v.get("value")
            if human == "unknown":
                stats[cap]["unknown_human"] += 1
                continue
            if human is True and ext_v is True:
                stats[cap]["tp"] += 1
            elif human is True and ext_v is not True:
                stats[cap]["fn"] += 1
            elif human is False and ext_v is True:
                stats[cap]["fp"] += 1
            else:
                stats[cap]["tn"] += 1
    return stats


def render(stats: dict) -> tuple[str, bool]:
    lines = [
        "# Phase 1 precision / recall (auto-generated)",
        "",
        "Critical-subset gating per TRUST.md §\"Pass bar — recall floors\".",
        "Recall is reported as the one-sided Wilson 95% lower confidence bound.",
        "",
        "| capability | TP | FP | FN | precision | recall_lcb | floor | min_N | gate |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    pass_all = True
    for cap, floor, min_n in CRITICAL:
        s = stats[cap]
        positives = s["tp"] + s["fn"]
        precision = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else float("nan")
        recall_p = s["tp"] / positives if positives else float("nan")
        recall_lcb = wilson_lower(recall_p, positives) if positives else float("nan")
        gated = (
            "PASS" if positives >= min_n and recall_lcb >= floor
            else f"UNDER-VALIDATED (positives {positives}/{min_n}, recall_lcb {recall_lcb:.3f}/{floor:.2f})"
        )
        if "PASS" not in gated:
            pass_all = False
        lines.append(
            f"| {cap} | {s['tp']} | {s['fp']} | {s['fn']} | "
            f"{precision:.3f} | {recall_lcb:.3f} | {floor:.2f} | {min_n} | {gated} |"
        )
    lines.append("")
    lines.append("Non-critical capabilities (recall reported, not gated):")
    lines.append("")
    lines.append("| capability | TP | FP | FN | precision |")
    lines.append("|---|---|---|---|---|")
    for cap in NON_CRITICAL:
        s = stats[cap]
        precision = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else float("nan")
        lines.append(f"| {cap} | {s['tp']} | {s['fp']} | {s['fn']} | {precision:.3f} |")
    return "\n".join(lines) + "\n", pass_all


def main():
    holdout = load_holdout()
    extractor = load_extractor_output()
    if not holdout.get("entries"):
        print(
            "holdout has no entries yet — Phase 1 verification is in TEMPLATE state. "
            "Critical capabilities default to UNDER-VALIDATED until labels land.",
            file=sys.stderr,
        )
    stats = evaluate(holdout, extractor)
    body, all_pass = render(stats)
    out = ROOT / "docs" / "phase1-verification" / "precision-recall.md"
    out.write_text(body, encoding="utf-8")
    print(body)
    sys.exit(0 if all_pass else 0)  # exit non-zero only if you want CI to fail; today, just report


if __name__ == "__main__":
    main()
