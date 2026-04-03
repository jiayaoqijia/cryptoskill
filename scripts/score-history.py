#!/usr/bin/env python3
"""CryptoSkill Evaluation Framework — Phase 4: Score Regression Tracking.

Tracks skill score changes over time by appending snapshots to a JSONL history
file and reporting regressions, improvements, and trends.

Usage:
    python3 scripts/score-history.py            # append snapshot + print diff
    python3 scripts/score-history.py --report   # print trend report from history
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = REPO_ROOT / "docs" / "skills.json"
HISTORY_FILE = REPO_ROOT / "scripts" / ".score-history.jsonl"

CHANGE_THRESHOLD = 5  # points change to flag as notable

GRADE_ORDER = {"A": 5, "B": 4, "C": 3, "D": 2, "F": 1}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_skills_json():
    """Load current scores from docs/skills.json."""
    if not SKILLS_JSON.exists():
        print(f"ERROR: {SKILLS_JSON} not found", file=sys.stderr)
        sys.exit(1)

    with open(SKILLS_JSON, "r") as f:
        data = json.load(f)

    skills = data.get("skills", [])
    scores = {}
    for skill in skills:
        name = skill.get("name", "")
        score_data = skill.get("score")
        if not name or not score_data:
            continue
        scores[name] = {
            "total": score_data.get("total", 0),
            "grade": score_data.get("grade", "F"),
            "risk_gate": score_data.get("risk_gate", "UNKNOWN"),
        }
    return scores


def load_history():
    """Load all snapshots from the JSONL history file."""
    if not HISTORY_FILE.exists():
        return []

    snapshots = []
    with open(HISTORY_FILE, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                snapshots.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"WARNING: Skipping malformed line {line_num} in history",
                      file=sys.stderr)
    return snapshots


def append_snapshot(snapshot):
    """Append a single snapshot to the JSONL history file."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(snapshot, separators=(",", ":")) + "\n")


def build_snapshot(scores):
    """Build a snapshot dict from current scores."""
    totals = [s["total"] for s in scores.values()]
    avg_score = round(sum(totals) / len(totals), 1) if totals else 0.0

    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_skills": len(scores),
        "avg_score": avg_score,
        "scores": scores,
    }


def diff_snapshots(prev_scores, curr_scores):
    """Compare two score dicts and return categorized changes."""
    improved = []   # (name, old_total, new_total, delta)
    degraded = []   # (name, old_total, new_total, delta)
    new_skills = [] # (name, total)
    removed = []    # (name, old_total)
    grade_changes = []  # (name, old_grade, new_grade)

    prev_names = set(prev_scores.keys())
    curr_names = set(curr_scores.keys())

    for name in sorted(curr_names - prev_names):
        new_skills.append((name, curr_scores[name]["total"]))

    for name in sorted(prev_names - curr_names):
        removed.append((name, prev_scores[name]["total"]))

    for name in sorted(prev_names & curr_names):
        old_total = prev_scores[name]["total"]
        new_total = curr_scores[name]["total"]
        delta = new_total - old_total

        if delta > CHANGE_THRESHOLD:
            improved.append((name, old_total, new_total, delta))
        elif delta < -CHANGE_THRESHOLD:
            degraded.append((name, old_total, new_total, delta))

        old_grade = prev_scores[name].get("grade", "F")
        new_grade = curr_scores[name].get("grade", "F")
        if old_grade != new_grade:
            grade_changes.append((name, old_grade, new_grade))

    # Sort by magnitude of change
    improved.sort(key=lambda x: -x[3])
    degraded.sort(key=lambda x: x[3])

    return {
        "improved": improved,
        "degraded": degraded,
        "new_skills": new_skills,
        "removed": removed,
        "grade_changes": grade_changes,
    }


def print_diff(diff, curr_snapshot, prev_snapshot=None):
    """Print the diff between snapshots in a readable format."""
    print("=" * 60)
    print("SCORE SNAPSHOT RECORDED")
    print("=" * 60)
    print(f"  Timestamp:    {curr_snapshot['timestamp']}")
    print(f"  Total skills: {curr_snapshot['total_skills']}")
    print(f"  Avg score:    {curr_snapshot['avg_score']}")

    if prev_snapshot:
        delta_skills = curr_snapshot["total_skills"] - prev_snapshot["total_skills"]
        delta_avg = round(curr_snapshot["avg_score"] - prev_snapshot["avg_score"], 1)
        sign_skills = "+" if delta_skills >= 0 else ""
        sign_avg = "+" if delta_avg >= 0 else ""
        print(f"  Delta skills: {sign_skills}{delta_skills}")
        print(f"  Delta avg:    {sign_avg}{delta_avg}")

    print()

    if diff["new_skills"]:
        print(f"NEW SKILLS ({len(diff['new_skills'])}):")
        for name, total in diff["new_skills"][:20]:
            print(f"  + {name} (score: {total})")
        if len(diff["new_skills"]) > 20:
            print(f"  ... and {len(diff['new_skills']) - 20} more")
        print()

    if diff["removed"]:
        print(f"REMOVED SKILLS ({len(diff['removed'])}):")
        for name, total in diff["removed"][:20]:
            print(f"  - {name} (was: {total})")
        if len(diff["removed"]) > 20:
            print(f"  ... and {len(diff['removed']) - 20} more")
        print()

    if diff["improved"]:
        print(f"IMPROVED >{CHANGE_THRESHOLD}pts ({len(diff['improved'])}):")
        for name, old, new, delta in diff["improved"][:20]:
            print(f"  ^ {name}: {old} -> {new} (+{delta})")
        if len(diff["improved"]) > 20:
            print(f"  ... and {len(diff['improved']) - 20} more")
        print()

    if diff["degraded"]:
        print(f"DEGRADED >{CHANGE_THRESHOLD}pts ({len(diff['degraded'])}):")
        for name, old, new, delta in diff["degraded"][:20]:
            print(f"  v {name}: {old} -> {new} ({delta})")
        if len(diff["degraded"]) > 20:
            print(f"  ... and {len(diff['degraded']) - 20} more")
        print()

    if diff["grade_changes"]:
        print(f"GRADE CHANGES ({len(diff['grade_changes'])}):")
        for name, old_g, new_g in diff["grade_changes"][:20]:
            arrow = "^" if GRADE_ORDER.get(new_g, 0) > GRADE_ORDER.get(old_g, 0) else "v"
            print(f"  {arrow} {name}: {old_g} -> {new_g}")
        if len(diff["grade_changes"]) > 20:
            print(f"  ... and {len(diff['grade_changes']) - 20} more")
        print()

    if (not diff["new_skills"] and not diff["removed"]
            and not diff["improved"] and not diff["degraded"]
            and not diff["grade_changes"]):
        print("No notable changes since last snapshot.")
        print()


# ---------------------------------------------------------------------------
# Report mode
# ---------------------------------------------------------------------------

def print_report(snapshots):
    """Print a trend report from history."""
    if not snapshots:
        print("No history data available. Run without --report first.")
        return

    print("=" * 60)
    print("SCORE REGRESSION REPORT")
    print("=" * 60)
    print()

    # --- Score trend over last 10 snapshots ---
    recent = snapshots[-10:]
    print(f"SCORE TREND (last {len(recent)} snapshots):")
    print("-" * 50)
    for snap in recent:
        ts = snap["timestamp"][:19].replace("T", " ")
        total = snap.get("total_skills", "?")
        avg = snap.get("avg_score", "?")
        print(f"  {ts}  |  skills: {total:>4}  |  avg: {avg:>5}")
    print()

    if len(recent) >= 2:
        first_avg = recent[0].get("avg_score", 0)
        last_avg = recent[-1].get("avg_score", 0)
        trend = round(last_avg - first_avg, 1)
        sign = "+" if trend >= 0 else ""
        print(f"  Overall trend: {sign}{trend} points")
        print()

    # --- 30-day window for per-skill analysis ---
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=30)

    # Find the earliest snapshot within 30 days
    baseline_snap = None
    for snap in snapshots:
        try:
            ts = datetime.strptime(snap["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
        except (ValueError, KeyError):
            continue
        if ts >= cutoff:
            baseline_snap = snap
            break

    latest_snap = snapshots[-1]

    if baseline_snap and baseline_snap is not latest_snap:
        baseline_scores = baseline_snap.get("scores", {})
        latest_scores = latest_snap.get("scores", {})
        common = set(baseline_scores.keys()) & set(latest_scores.keys())

        # Compute deltas
        deltas = []
        for name in common:
            old_total = baseline_scores[name].get("total", 0)
            new_total = latest_scores[name].get("total", 0)
            delta = new_total - old_total
            if delta != 0:
                old_grade = baseline_scores[name].get("grade", "F")
                new_grade = latest_scores[name].get("grade", "F")
                deltas.append((name, old_total, new_total, delta, old_grade, new_grade))

        deltas.sort(key=lambda x: -x[3])

        # Biggest improvements
        improvements = [d for d in deltas if d[3] > 0]
        if improvements:
            print(f"BIGGEST IMPROVEMENTS (last 30 days, top 15):")
            print("-" * 50)
            for name, old, new, delta, _, _ in improvements[:15]:
                print(f"  +{delta:>3}  {name}: {old} -> {new}")
            print()

        # Biggest degradations
        degradations = [d for d in deltas if d[3] < 0]
        degradations.sort(key=lambda x: x[3])
        if degradations:
            print(f"BIGGEST DEGRADATIONS (last 30 days, top 15):")
            print("-" * 50)
            for name, old, new, delta, _, _ in degradations[:15]:
                print(f"  {delta:>4}  {name}: {old} -> {new}")
            print()

        # Grade changes
        grade_changes = [
            d for d in deltas
            if d[4] != d[5]
        ]
        if grade_changes:
            print(f"GRADE CHANGES (last 30 days):")
            print("-" * 50)
            for name, old, new, delta, old_g, new_g in grade_changes:
                arrow = "^" if GRADE_ORDER.get(new_g, 0) > GRADE_ORDER.get(old_g, 0) else "v"
                print(f"  {arrow} {name}: {old_g} -> {new_g} (score: {old} -> {new})")
            print()

        if not improvements and not degradations and not grade_changes:
            print("No score changes in the last 30 days.")
            print()
    elif baseline_snap is latest_snap:
        print("Only one snapshot in the last 30 days. Need more data for trend analysis.")
        print()
    else:
        print("No snapshots within the last 30 days for comparison.")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="CryptoSkill score regression tracker"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Print trend report from history instead of appending a snapshot",
    )
    args = parser.parse_args()

    if args.report:
        snapshots = load_history()
        print_report(snapshots)
        return

    # --- Snapshot mode (default) ---
    scores = load_skills_json()
    if not scores:
        print("ERROR: No scored skills found in skills.json", file=sys.stderr)
        sys.exit(1)

    curr_snapshot = build_snapshot(scores)

    # Load previous snapshot for diffing
    history = load_history()
    prev_scores = {}
    prev_snapshot = None
    if history:
        prev_snapshot = history[-1]
        prev_scores = prev_snapshot.get("scores", {})

    # Compute diff
    diff = diff_snapshots(prev_scores, scores)

    # Append new snapshot
    append_snapshot(curr_snapshot)

    # Print results
    print_diff(diff, curr_snapshot, prev_snapshot)

    print(f"Snapshot appended to {HISTORY_FILE}")


if __name__ == "__main__":
    main()
