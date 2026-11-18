"""Append-only log of daily review routine runs (0.1.5). One JSON line per run, written even when nothing is due."""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from common import VERSION, instant

OUTCOMES = {"reviewed", "pending_data", "failed", "none"}
BANGKOK = timezone(timedelta(hours=7), "Asia/Bangkok")


def stamp(moment: datetime) -> dict:
    moment = moment.astimezone(timezone.utc).replace(microsecond=0)
    return {"utc": moment.isoformat().replace("+00:00", "Z"), "bangkok": moment.astimezone(BANGKOK).isoformat()}


def parse_outcomes(items: list[str]) -> dict[str, str]:
    """Each item is '<decision_id>:<horizon_days>=<outcome>'."""
    result = {}
    for item in items or []:
        key, _, value = item.partition("=")
        if ":" not in key or value not in OUTCOMES - {"none"}:
            raise ValueError("--outcome must be <decision_id>:<horizon>=reviewed|pending_data|failed")
        result[key] = value
    return result


def build_entry(*, started: datetime, finished: datetime, doctor_status: str, due_items: list[dict] | None,
                outcomes: dict[str, str], agent: str | None, model: str | None, errors: list[str]) -> dict:
    errors = list(errors)
    items = []
    keys = []
    for row in due_items or []:
        key = f"{row['decision_id']}:{row['horizon_days']}"
        keys.append(key)
        state = outcomes.get(key)
        items.append({"due_id": key, "decision_id": row["decision_id"], "horizon_days": row["horizon_days"],
                      "errata": row.get("errata", []), "outcome": state or "pending_data",
                      "outcome_reported": state is not None})
    unknown = sorted(set(outcomes) - set(keys))
    if unknown:
        errors.append("outcome given for ids not due: " + ", ".join(unknown))
    if due_items is None:
        run_outcome = "failed"
    elif not items:
        run_outcome = "none"
    elif any(i["outcome"] == "failed" for i in items):
        run_outcome = "failed"
    elif all(i["outcome"] == "reviewed" for i in items):
        run_outcome = "reviewed"
    else:
        run_outcome = "pending_data"
    return {"schema_version": 1, "skill_version": VERSION,
            "run_started_at": stamp(started), "run_finished_at": stamp(finished),
            "doctor_status": doctor_status, "due_ids": keys, "due_count": len(keys), "items": items,
            "run_outcome": run_outcome, "execution_agent": agent or "unknown", "model": model or "unknown",
            "errors": errors}


def append_entry(runtime: Path, entry: dict) -> Path:
    path = runtime / "review_runs.jsonl"
    with path.open("a", encoding="utf-8") as handle:  # append only; never rewrites earlier lines
        handle.write(json.dumps(entry, ensure_ascii=False, allow_nan=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return path


def parse_started(value: str | None) -> datetime | None:
    return instant(value) if value else None
