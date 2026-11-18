"""Quick fact-check records (0.1.6): structure and validation only; the model decides the verdict.

Fact-checks never carry trading signals, never touch the judgment ledger and never schedule reviews.
Finalized records live append-only under RUNTIME/factchecks/<id>.json; corrections use a new id + supersedes.
"""
from __future__ import annotations

import re
from datetime import timedelta
from pathlib import Path

from common import VERSION, instant, now, read_json, safe_id, write_json

VERDICTS = {"true": "属实", "partly_true": "部分属实", "false": "不实", "unverifiable": "无法核实"}
SOURCE_TYPES = {"primary", "secondary", "self_claim"}
FRESHNESS = {"this_run", "stale"}
NOTE_KINDS = ("fact", "self_claim", "inference", "unknown")
FORBIDDEN_KEYS = {"signal", "due_at", "reference_quote", "benchmark", "assertions", "decision_id", "valid_until"}
SECOND = re.compile(r".*T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
CLOCK_SKEW = timedelta(minutes=5)


def skeleton(claim: str, requested_by: str = "user", requester_name: str | None = None,
             factcheck_id: str | None = None, supersedes: str | None = None) -> dict:
    if not claim or not claim.strip():
        raise ValueError("claim text required")
    if requested_by not in {"user", "bot"}:
        raise ValueError("requested_by must be user or bot")
    created = now()
    fid = safe_id(factcheck_id or "fc-" + created.replace("-", "").replace(":", "").replace(".", "")[:15])
    return {"record_type": "factcheck", "factcheck_id": fid, "skill_version": VERSION, "status": "draft",
            "claim": claim.strip(), "requested_by": {"kind": requested_by, "name": requester_name},
            "created_at": created, "completed_at": None, "verdict": None, "verdict_zh": None,
            "evidence": [], "notes": {kind: [] for kind in NOTE_KINDS}, "values": {},
            "supersedes": supersedes, "execution_agent": None, "model": None,
            "_template": {"evidence_item": {"evidence_id": "e1", "source_url": "https://...", "source_type": "primary|secondary|self_claim",
                                            "fetched_at": "request time, UTC seconds", "data_time": "time of the data itself or null",
                                            "data_time_unknown_reason": "required when data_time is null",
                                            "freshness": "this_run|stale (stale = earlier run, not re-fetched)", "note": "what it shows"},
                          "fact_note": {"text": "...", "evidence_ids": ["e1"]},
                          "values": "named numbers; missing stays null with a reason, never 0"}}


def validate(record: dict) -> dict:
    """Return {errors, warnings}. Errors block finalize."""
    errors, warnings = [], []
    if record.get("record_type") != "factcheck":
        errors.append("record_type must be factcheck")
    try:
        safe_id(record.get("factcheck_id") or "")
    except ValueError as exc:
        errors.append(f"factcheck_id: {exc}")
    if not record.get("claim"):
        errors.append("claim text required")
    bad = sorted(FORBIDDEN_KEYS & set(record))
    if bad:
        errors.append(f"fact-checks must not carry signals/review fields: {', '.join(bad)}")
    verdict = record.get("verdict")
    if verdict not in VERDICTS:
        errors.append(f"verdict must be one of {sorted(VERDICTS)}")
    elif record.get("verdict_zh") not in (None, VERDICTS[verdict]):
        errors.append(f"verdict_zh must be {VERDICTS[verdict]} for {verdict}")
    for key in ("execution_agent", "model"):
        if not record.get(key):
            errors.append(f"{key} required (write unknown if not available)")
    try:
        completed = instant(record["completed_at"]) if record.get("completed_at") else None
    except (ValueError, AttributeError):
        completed, _ = None, errors.append("completed_at must be ISO 8601 with Z/offset")
    if completed is None and not any(e.startswith("completed_at") for e in errors):
        errors.append("completed_at required")
    ids, fresh = set(), set()
    for index, item in enumerate(record.get("evidence") or []):
        where = f"evidence {index}"
        eid = item.get("evidence_id")
        if not eid or eid in ids:
            errors.append(f"{where}: missing or duplicate evidence_id")
        ids.add(eid)
        if not str(item.get("source_url", "")).startswith(("https://", "http://", "file:///")):
            errors.append(f"{where}: source_url must be a full link")
        if item.get("source_type") not in SOURCE_TYPES:
            errors.append(f"{where}: source_type must be primary/secondary/self_claim")
        freshness = item.get("freshness", "this_run")
        if freshness not in FRESHNESS:
            errors.append(f"{where}: freshness must be this_run or stale")
        fetched = item.get("fetched_at")
        if not fetched:
            errors.append(f"{where}: fetched_at required (no evidence without a fetch time)")
        else:
            try:
                stamp = instant(fetched)
                if not SECOND.match(fetched):
                    errors.append(f"{where}: fetched_at must be UTC with seconds precision")
                if stamp > instant(now()) + CLOCK_SKEW or (completed and stamp > completed + CLOCK_SKEW):
                    errors.append(f"{where}: fetched_at after completion/now")
            except ValueError:
                errors.append(f"{where}: fetched_at must be ISO 8601 with Z/offset")
        if "data_time" not in item:
            errors.append(f"{where}: data_time key required (null if unknown)")
        elif item["data_time"] is None and not item.get("data_time_unknown_reason"):
            errors.append(f"{where}: data_time=null requires data_time_unknown_reason")
        if freshness == "this_run" and fetched and not any(e.startswith(where) for e in errors):
            fresh.add(eid)
        if freshness == "stale":
            warnings.append(f"{where}: stale evidence (earlier run, not re-fetched) cannot support a verdict alone")
    notes = record.get("notes") or {}
    for kind in NOTE_KINDS:
        if not isinstance(notes.get(kind, []), list):
            errors.append(f"notes.{kind} must be a list")
    for index, note in enumerate(notes.get("fact") or []):
        refs = note.get("evidence_ids") if isinstance(note, dict) else None
        if not refs:
            errors.append(f"notes.fact {index}: a fact needs evidence_ids from this run; otherwise label it unknown/未验证")
        elif any(ref not in fresh for ref in refs):
            errors.append(f"notes.fact {index}: evidence_ids must name valid this_run evidence")
    if verdict in {"true", "partly_true", "false"} and not fresh:
        errors.append("a true/partly_true/false verdict needs at least one evidence item fetched in this run")
    for name, value in (record.get("values") or {}).items():
        if isinstance(value, dict) and value.get("value") is None and not value.get("missing_reason"):
            warnings.append(f"values.{name}: null without missing_reason")
    return {"errors": errors, "warnings": warnings}


def finalize(record: dict, runtime: Path) -> dict:
    result = validate(record)
    if result["errors"]:
        raise ValueError("factcheck invalid: " + "; ".join(result["errors"]))
    folder = runtime / "factchecks"
    if record.get("supersedes") and not (folder / f"{safe_id(record['supersedes'])}.json").is_file():
        raise ValueError("supersedes must name an existing factcheck")
    value = {k: v for k, v in record.items() if k != "_template"}
    value.update(status="final", verdict_zh=VERDICTS[value["verdict"]], finalized_at=now(),
                 finalized_by_version=VERSION, validation_warnings=result["warnings"])
    target = folder / f"{value['factcheck_id']}.json"
    if target.exists():
        raise ValueError("Factcheck already exists; use a new id with supersedes")
    write_json(target, value, exclusive=True)
    return {"factcheck_path": str(target), "verdict": value["verdict"], "verdict_zh": value["verdict_zh"],
            "warnings": result["warnings"]}
