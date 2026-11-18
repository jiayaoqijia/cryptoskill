"""Append-only model judgments and deterministic 30/90 day outcome arithmetic."""
from __future__ import annotations

import json
import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

from common import VERSION, asset_key, digest, instant, now, number, safe_id
from metrics import change

SIGNALS = {"BUY", "SELL", "WATCH", "UNDETERMINED", "NOT_APPLICABLE"}
CLAIM_LABELS = {"fact", "inference", "self_reported", "third_party_estimate", "calculation", "unknown", "unverified"}
CLOCK_SKEW = timedelta(minutes=5)


def entries(runtime: Path) -> list[dict]:
    path = runtime / "judgments.jsonl"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        # A truncated line is an error, not silently skipped history.
        return [json.loads(line) for line in handle if line.strip()]


@contextmanager
def locked(runtime: Path):
    path = runtime / ".ledger.lock"
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.write(descriptor, str(os.getpid()).encode())
        yield
    finally:
        os.close(descriptor)
        path.unlink()


def append(runtime: Path, value: dict) -> dict:
    previous = entries(runtime)
    record = {**value, "recorded_at": now(), "previous_hash": previous[-1]["record_hash"] if previous else None}
    record["record_hash"] = digest(record)
    with (runtime / "judgments.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return record


def audit(runtime: Path) -> dict:
    previous = None
    for row in entries(runtime):
        copy = dict(row)
        stated = copy.pop("record_hash")
        if row["previous_hash"] != previous or digest(copy) != stated:
            raise ValueError("Ledger hash chain mismatch")
        previous = stated
    return {"status": "ok", "entries": len(entries(runtime)), "head": previous,
            "note": "Hash chain detects edits; not a remote timestamp or signature."}


def check_refs(refs: list, evidence: dict):
    available = {item["evidence_id"] for item in evidence["records"] if item["status"] == "ok"}
    if not refs or any(ref not in available for ref in refs):
        raise ValueError("Each judgment/quote requires successful evidence references")


def check_quote(quote: dict, asset: dict, evidence: dict):
    if asset_key(quote["asset"]) != asset_key(asset):
        raise ValueError("Quote asset mismatch")
    if quote.get("currency") != "USD":
        raise ValueError("Review price must use USD; explicitly convert stablecoin quotes with evidence")
    if number(quote["price"]) is None or number(quote["price"]) <= 0:
        raise ValueError("Positive quote required")
    instant(quote["observed_at"])
    check_refs(quote["evidence_refs"], evidence)
    if not quote.get("venue") or not quote.get("instrument"):
        raise ValueError("Quote venue/instrument required")


def check_source(item: dict, where: str, evidence: dict | None = None) -> datetime:
    """Conclusion-level provenance: link, data time, fetch time and raw file location are all mandatory."""
    for key in ("source_url", "observed_at", "fetched_at", "raw_path"):
        if key not in item:
            raise ValueError(f"{where}: missing required evidence field {key}")
    url = str(item["source_url"])
    if not url.startswith(("https://", "http://", "file:///")):
        raise ValueError(f"{where}: source_url must be a full http(s) link, or file:/// for local-only evidence")
    if url.startswith("file:///") and not Path(url[7:]).exists():
        raise ValueError(f"{where}: file:/// source_url must exist")
    fetched = instant(item["fetched_at"])
    if item["observed_at"] is None:
        if not item.get("observed_at_unknown_reason"):
            raise ValueError(f"{where}: observed_at=null requires observed_at_unknown_reason")
    elif instant(item["observed_at"]) > fetched + CLOCK_SKEW:
        raise ValueError(f"{where}: observed_at cannot be after fetched_at")
    if not item["raw_path"] or not Path(item["raw_path"]).is_file():
        raise ValueError(f"{where}: raw_path must point to an existing raw file")
    if evidence is not None:
        record = next((r for r in evidence["records"] if r["evidence_id"] == item.get("evidence_ref") and r["status"] == "ok"), None)
        if record is None:
            raise ValueError(f"{where}: evidence_ref must name a successful evidence record")
        stamps = [instant(record[k]) for k in ("retrieved_at", "fetched_at") if record.get(k)]
        if stamps and fetched not in stamps:
            raise ValueError(f"{where}: fetched_at differs from evidence retrieved_at/fetched_at")
    if item.get("time_precision") is not None and item["time_precision"] not in {"second", "minute", "file_mtime"}:
        raise ValueError(f"{where}: time_precision must be second, minute or file_mtime")
    return fetched


SAFETY_ITEMS = ("mint", "owner_privileges", "proxy_upgrade", "pause_blacklist", "tax", "sell_simulation", "lp_lock", "source_verified")
SAFETY_STATES = {"checked_none_found", "confirmed_risk", "unverified", "not_applicable"}


def check_safety(value: dict, evidence: dict) -> None:
    """0.1.4: every safety item gets one of four explicit states; no blanket 'safe' allowed."""
    if not value.get("asset"):
        return
    checks = value.get("safety_checks")
    if not isinstance(checks, list):
        raise ValueError("safety_checks[] required (states: checked_none_found/confirmed_risk/unverified/not_applicable)")
    seen = {}
    for check in checks:
        item, state = check.get("item"), check.get("status")
        if not item or item in seen:
            raise ValueError(f"safety_checks: missing or duplicate item {item}")
        if state not in SAFETY_STATES:
            raise ValueError(f"safety_checks {item}: status must be one of {sorted(SAFETY_STATES)}")
        if state in {"checked_none_found", "confirmed_risk"}:
            if not check.get("evidence_refs") or not check.get("method"):
                raise ValueError(f"safety_checks {item}: {state} needs evidence_refs and method (what exactly was checked)")
            check_refs(check["evidence_refs"], evidence)
        elif not check.get("note"):
            raise ValueError(f"safety_checks {item}: {state} needs a note (why unverified / not applicable)")
        seen[item] = state
    missing = [item for item in SAFETY_ITEMS if item not in seen]
    if missing:
        raise ValueError(f"safety_checks missing required items: {', '.join(missing)} (use not_applicable with note)")


def check_watch(value: dict, at: datetime) -> None:
    """0.1.4: WATCH records a price baseline and verifiable events by default; gaps must be explicit."""
    if value["signal"] != "WATCH":
        return
    if not value.get("reference_quote") and not value.get("baseline_gap"):
        raise ValueError("WATCH needs reference_quote (price baseline) or an explicit baseline_gap")
    if not value.get("assertions") and not value.get("no_assertion_reason"):
        raise ValueError("WATCH needs verifiable assertions (events) or an explicit no_assertion_reason")
    if not value.get("signal_window") or not value.get("valid_until"):
        raise ValueError("WATCH needs signal_window and valid_until")
    if instant(value["valid_until"]) <= at:
        raise ValueError("Signal validity must end after decision time")


def check_claims(value: dict, evidence: dict) -> datetime:
    claims = value.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("claims[] required: every conclusion needs claim-level sources and times")
    ids, latest = set(), None
    for claim in claims:
        safe_id(claim.get("claim_id", ""))
        if claim["claim_id"] in ids:
            raise ValueError("Claim IDs must be unique")
        ids.add(claim["claim_id"])
        if not claim.get("text") or claim.get("label") not in CLAIM_LABELS:
            raise ValueError(f"claim {claim['claim_id']}: text and label in {sorted(CLAIM_LABELS)} required")
        if claim["label"] == "unverified" and not claim.get("sources"):
            # 0.1.6: memory or un-refetched material may be stated only as 未验证, with a reason and no evidence.
            if not claim.get("unverified_reason"):
                raise ValueError(f"claim {claim['claim_id']}: unverified claim without sources needs unverified_reason")
            continue
        if not claim.get("sources"):
            raise ValueError(f"claim {claim['claim_id']}: at least one source required")
        fresh = 0
        for index, source in enumerate(claim["sources"]):
            where = f"claim {claim['claim_id']} source {index}"
            if source.get("freshness") == "stale":
                # 0.1.6: earlier-run evidence keeps its original evidence_id and fetched_at; not matched to this pack.
                if not source.get("evidence_ref"):
                    raise ValueError(f"{where}: stale source must cite its original evidence_ref")
                check_source(source, where, None)
                continue
            if source.get("freshness", "this_run") != "this_run":
                raise ValueError(f"{where}: freshness must be this_run or stale")
            fetched = check_source(source, where, evidence)
            fresh += 1
            latest = fetched if latest is None or fetched > latest else latest
        if claim["label"] == "fact" and not fresh:
            raise ValueError(f"claim {claim['claim_id']}: fact needs a source fetched in this run; otherwise label unverified")
    if latest is None:
        raise ValueError("At least one claim must rest on evidence fetched in this run")
    return latest


def freshness_warnings(value: dict, evidence: dict) -> list[str]:
    """0.1.6: evidence records cited by claims should carry a request-time fetch stamp."""
    cited = {s.get("evidence_ref") for c in value.get("claims", []) for s in c.get("sources", []) if s.get("freshness", "this_run") == "this_run"}
    return [f"evidence {r['evidence_id']}: no fetched_at/retrieved_at in evidence pack"
            for r in evidence.get("records", []) if r.get("evidence_id") in cited and not (r.get("fetched_at") or r.get("retrieved_at"))]


def check_times(value: dict, latest_fetch: datetime, at: datetime):
    for key in ("data_cutoff", "analysis_completed_at"):
        if not value.get(key):
            raise ValueError(f"{key} required; data cutoff and judgment completion are recorded separately")
    cutoff, completed = instant(value["data_cutoff"]), instant(value["analysis_completed_at"])
    if latest_fetch > cutoff:
        raise ValueError("A cited source was fetched after data_cutoff")
    if not cutoff <= at <= completed:
        raise ValueError("Require data_cutoff <= as_of <= analysis_completed_at")
    if completed > instant(now()) + CLOCK_SKEW:
        raise ValueError("analysis_completed_at is in the future")


def check_objections(value: dict):
    """Release gate: every objection raised by terra/sol review must be adopted or explicitly retained."""
    if "review_objections" not in value:
        raise ValueError("review_objections required (empty list only with review_objections_none_reason)")
    objections = value["review_objections"]
    if not isinstance(objections, list):
        raise ValueError("review_objections must be a list")
    if not objections and not value.get("review_objections_none_reason"):
        raise ValueError("Empty review_objections requires review_objections_none_reason")
    ids, unresolved = set(), []
    for item in objections:
        safe_id(item.get("id", ""))
        if item["id"] in ids:
            raise ValueError("Objection IDs must be unique")
        ids.add(item["id"])
        if not item.get("objection") or not item.get("source") or not Path(item["source"]).is_file():
            raise ValueError(f"objection {item['id']}: objection text and existing review output source required")
        disposition = item.get("disposition")
        if disposition == "adopted" and item.get("summary_change") and item.get("ledger_change"):
            continue
        if disposition == "retained" and item.get("retention_reason"):
            continue
        unresolved.append(item["id"])
    if unresolved:
        raise ValueError("Unresolved review objections (adopt with summary_change+ledger_change, or retain with retention_reason): "
                         + ", ".join(unresolved))


def record_decision(document: dict, evidence: dict, runtime: Path) -> dict:
    value = dict(document)
    safe_id(value["decision_id"])
    if value.get("authored_by") != "model":
        raise ValueError("Analysis and signals must be authored by the model")
    if value["signal"] not in SIGNALS or value["risk"] not in {"low", "medium", "high", "critical", "unknown"}:
        raise ValueError("Invalid signal/risk enum")
    at = instant(value["as_of"])
    if at > instant(now()) + timedelta(minutes=5):
        raise ValueError("Decision timestamp is in the future")
    check_refs(value["evidence_refs"], evidence)
    check_objections(value)
    check_times(value, check_claims(value, evidence), at)
    check_safety(value, evidence)
    check_watch(value, at)
    if not value.get("thesis") or not value.get("recheck_conditions") or not value.get("execution_agent") or not value.get("model"):
        raise ValueError("Thesis, recheck conditions and executing agent required")
    if value.get("asset"):
        value["asset_key"] = asset_key(value["asset"])
    elif value["signal"] != "NOT_APPLICABLE":
        raise ValueError("Tradable judgments require verified asset identity")
    if value.get("reference_quote"):
        check_quote(value["reference_quote"], value["asset"], evidence)
        age = (at - instant(value["reference_quote"]["observed_at"])).total_seconds()
        if not 0 <= age <= 900:
            raise ValueError("Baseline quote must be no more than 15 min before decision")
    if value["signal"] in {"BUY", "SELL"} and not value.get("reference_quote"):
        raise ValueError("BUY/SELL requires a fresh, sourced reference price")
    if value["signal"] in {"BUY", "SELL"}:
        if not value.get("signal_window") or not value.get("invalidation_conditions") or not value.get("valid_until"):
            raise ValueError("BUY/SELL needs signal_window, valid_until and invalidation_conditions")
        if instant(value["valid_until"]) <= at:
            raise ValueError("Signal validity must end after decision time")
        if not value.get("benchmark") and not value.get("benchmark_gap"):
            raise ValueError("Missing benchmark requires an explicit reason")
    if value.get("benchmark"):
        check_quote(value["benchmark"]["reference_quote"], value["benchmark"]["asset"], evidence)
        if not 0 <= (at - instant(value["benchmark"]["reference_quote"]["observed_at"])).total_seconds() <= 900:
            raise ValueError("Benchmark baseline must align within 15 min")
    for assertion in value.get("assertions", []):
        safe_id(assertion["id"])
        if not assertion.get("condition") or not assertion.get("check_by"):
            raise ValueError("Falsifiable assertion needs condition and check_by (deadline/horizon)")
        check_refs(assertion["evidence_refs"], evidence)
    assertion_ids = [item["id"] for item in value.get("assertions", [])]
    if len(assertion_ids) != len(set(assertion_ids)):
        raise ValueError("Assertion IDs must be unique")
    warnings = freshness_warnings(value, evidence)
    if warnings:
        value["validation_warnings"] = warnings
    value.update(record_type="decision", skill_version=VERSION,
                 due_at={str(day): (at + timedelta(days=day)).isoformat().replace("+00:00", "Z") for day in (30, 90)})
    with locked(runtime):
        audit(runtime)
        rows = entries(runtime)
        if any(row.get("decision_id") == value["decision_id"] and row["record_type"] == "decision" for row in rows):
            raise ValueError("Decision already exists; append a new ID with supersedes instead")
        if value.get("supersedes") and not any(row["record_type"] == "decision" and row["decision_id"] == value["supersedes"] for row in rows):
            raise ValueError("supersedes must name an existing decision")
        return append(runtime, value)


def due(runtime: Path, at: str | None = None) -> list[dict]:
    rows, current = entries(runtime), instant(at or now())
    complete = {(r["decision_id"], r["horizon_days"]) for r in rows if r["record_type"] == "review" and r["status"] == "complete"}
    errata = {}
    for r in rows:
        if r["record_type"] == "erratum":
            errata.setdefault(r["target_decision_id"], []).append(r["erratum_id"])
    return [{"decision_id": row["decision_id"], "horizon_days": day, "due_at": timestamp,
             "decision": row, "errata": errata.get(row["decision_id"], [])} for row in rows if row["record_type"] == "decision"
            for horizon, timestamp in row["due_at"].items()
            if (day := int(horizon)) and instant(timestamp) <= current and (row["decision_id"], day) not in complete]


def outcome(decision: dict, review: dict, evidence: dict) -> dict:
    day = review["horizon_days"]
    if day not in (30, 90):
        raise ValueError("Horizon must be 30 or 90 days")
    target = instant(decision["due_at"][str(day)])
    if instant(review["reviewed_at"]) < target:
        raise ValueError("Review not due yet")
    base, quote = decision.get("reference_quote"), review.get("quote")
    result = {"return_pct": None, "direction_hit": None, "excess_return_pp": None,
              "relative_direction_hit": None, "price_status": "not_evaluable",
              "relative_status": "not_evaluable" if decision.get("benchmark") else "not_applicable"}
    if quote and base:
        check_quote(quote, decision["asset"], evidence)
        if any(quote[field] != base[field] for field in ("venue", "instrument", "currency")):
            raise ValueError("Outcome venue/instrument/currency differs from frozen baseline; mark not evaluable")
        if not 0 <= (instant(quote["observed_at"]) - target).total_seconds() <= 86400:
            raise ValueError("Outcome quote must be at/after horizon and within 24h; historical bars needed if late")
        if instant(quote["observed_at"]) > instant(review["reviewed_at"]):
            raise ValueError("Outcome quote is later than review")
        result["return_pct"] = change(base["price"], quote["price"])
        result["price_status"] = "evaluable"
        if decision["signal"] in {"BUY", "SELL"}:
            result["direction_hit"] = result["return_pct"] > 0 if decision["signal"] == "BUY" else result["return_pct"] < 0
    result["counts_toward_hit_rate"] = decision["signal"] in {"BUY", "SELL"}
    benchmark, endpoint = decision.get("benchmark"), review.get("benchmark_quote")
    if benchmark and endpoint and result["return_pct"] is not None:
        check_quote(endpoint, benchmark["asset"], evidence)
        if any(endpoint[field] != benchmark["reference_quote"][field] for field in ("venue", "instrument", "currency")):
            raise ValueError("Outcome benchmark differs from frozen venue/instrument/currency")
        if abs((instant(endpoint["observed_at"]) - instant(quote["observed_at"])).total_seconds()) > 3600:
            raise ValueError("Outcome benchmark must align within 1h")
        if instant(endpoint["observed_at"]) > instant(review["reviewed_at"]):
            raise ValueError("Future benchmark quote")
        excess = result["return_pct"] - change(benchmark["reference_quote"]["price"], endpoint["price"])
        result["excess_return_pp"] = excess
        result["relative_status"] = "evaluable"
        if decision["signal"] in {"BUY", "SELL"}:
            result["relative_direction_hit"] = excess > 0 if decision["signal"] == "BUY" else excess < 0
    return result


def record_review(document: dict, evidence: dict, runtime: Path) -> dict:
    value = dict(document)
    if value.get("authored_by") != "model" or value.get("status") not in {"complete", "pending_data"}:
        raise ValueError("Review explanation must come from model; valid status required")
    if not value.get("assessment") or not value.get("execution_agent") or not value.get("model"):
        raise ValueError("Model assessment and executing agent required")
    if instant(value["reviewed_at"]) > instant(now()) + timedelta(minutes=5):
        raise ValueError("Review timestamp is in the future")
    with locked(runtime):
        audit(runtime)
        rows = entries(runtime)
        decision = next(r for r in rows if r["record_type"] == "decision" and r["decision_id"] == value["decision_id"])
        if any(r["record_type"] == "review" and r["decision_id"] == value["decision_id"] and r["horizon_days"] == value["horizon_days"] and r["status"] == "complete" for r in rows):
            raise ValueError("This horizon already has a completed review")
        assertions = {r["id"] for r in decision.get("assertions", [])}
        reviewed_assertions = set()
        for assertion in value.get("assertion_results", []):
            if assertion["id"] not in assertions or assertion["status"] not in {"occurred", "not_occurred", "unknown"}:
                raise ValueError("Invalid assertion review")
            if assertion["id"] in reviewed_assertions:
                raise ValueError("Duplicate assertion review")
            reviewed_assertions.add(assertion["id"])
            if assertion["status"] != "unknown":
                check_refs(assertion["evidence_refs"], evidence)
        if value["status"] == "complete" and reviewed_assertions != assertions:
            raise ValueError("Completed review must address every original assertion")
        arithmetic = outcome(decision, value, evidence)
        if value["status"] == "pending_data" or arithmetic["price_status"] != "evaluable":
            if not value.get("data_gap"):
                raise ValueError("Missing review price requires an explicit data_gap")
        if arithmetic["relative_status"] == "not_evaluable" and not value.get("benchmark_gap"):
            raise ValueError("Missing preselected benchmark result requires benchmark_gap")
        missing_expected = ((decision.get("reference_quote") and arithmetic["price_status"] != "evaluable")
                            or (decision.get("benchmark") and arithmetic["relative_status"] != "evaluable"))
        if missing_expected and value["status"] == "complete" and not value.get("final_data_unavailable_reason"):
            raise ValueError("Incomplete review must stay pending_data, or explicitly justify permanent data unavailability")
        results = value.get("assertion_results", [])
        arithmetic["event_status"] = ("not_applicable" if not assertions else
                                      "evaluable" if any(r["status"] != "unknown" for r in results) else "not_evaluable")
        arithmetic["events"] = {state: sum(r["status"] == state for r in results) for state in ("occurred", "not_occurred", "unknown")}
        return append(runtime, {**value, "record_type": "review", "outcome": arithmetic})


def record_erratum(document: dict, runtime: Path) -> dict:
    """Append-only correction of an earlier decision; the original record and report are never edited."""
    value = dict(document)
    safe_id(value["erratum_id"])
    if not value.get("execution_agent") or not value.get("model") or not value.get("authored_by"):
        raise ValueError("Erratum requires authored_by, execution_agent and model (unknown allowed)")
    if not value.get("errata_path") or not Path(value["errata_path"]).is_file():
        raise ValueError("errata_path must point to the saved errata document")
    if not value.get("corrections"):
        raise ValueError("Erratum needs at least one correction")
    for item in value["corrections"]:
        safe_id(item.get("id", ""))
        if not item.get("original_text") or not item.get("original_location"):
            raise ValueError(f"correction {item['id']}: original_text and original_location required")
        if item.get("disposition") == "corrected" and not item.get("corrected_text"):
            raise ValueError(f"correction {item['id']}: corrected_text required")
        if item.get("disposition") == "retained" and not item.get("retention_reason"):
            raise ValueError(f"correction {item['id']}: retention_reason required")
        if item.get("disposition") not in {"corrected", "retained"}:
            raise ValueError(f"correction {item['id']}: disposition must be corrected or retained")
        if not item.get("sources"):
            raise ValueError(f"correction {item['id']}: sources required")
        for index, source in enumerate(item["sources"]):
            check_source(source, f"correction {item['id']} source {index}")
    with locked(runtime):
        audit(runtime)
        rows = entries(runtime)
        if not any(r["record_type"] == "decision" and r["decision_id"] == value["target_decision_id"] for r in rows):
            raise ValueError("Erratum target decision does not exist")
        if any(r["record_type"] == "erratum" and r["erratum_id"] == value["erratum_id"] for r in rows):
            raise ValueError("Erratum already exists")
        return append(runtime, {**value, "record_type": "erratum", "skill_version": VERSION})


def summary(runtime: Path) -> dict:
    rows = entries(runtime)
    decisions = {r["decision_id"]: r for r in rows if r["record_type"] == "decision"}
    groups = {}
    for horizon in (30, 90):
        for signal in ("BUY", "SELL"):
            eligible = [r for r in rows if r["record_type"] == "review" and r["status"] == "complete"
                        and r["horizon_days"] == horizon and decisions[r["decision_id"]]["signal"] == signal]
            valid = [r for r in eligible if r["outcome"]["direction_hit"] is not None]
            relative = [r for r in eligible if r["outcome"]["relative_direction_hit"] is not None]
            groups[f"{horizon}d_{signal}"] = {"n": len(valid), "hits": sum(r["outcome"]["direction_hit"] for r in valid),
                "hit_rate": sum(r["outcome"]["direction_hit"] for r in valid) / len(valid) if valid else None,
                "relative_n": len(relative), "relative_hits": sum(r["outcome"]["relative_direction_hit"] for r in relative),
                "relative_not_evaluable": sum(r["outcome"]["relative_status"] == "not_evaluable" for r in eligible),
                "unique_assets": len({decisions[r["decision_id"]].get("asset_key") for r in valid}),
                "not_evaluable": len(eligible) - len(valid)}
    watch = [r for r in rows if r["record_type"] == "review" and r["status"] == "complete" and decisions[r["decision_id"]]["signal"] == "WATCH"]
    groups["WATCH_tracking"] = {"n_reviews": len(watch),
        "price_evaluable": sum(r["outcome"].get("price_status") == "evaluable" for r in watch),
        "returns_pct": [r["outcome"]["return_pct"] for r in watch if r["outcome"].get("return_pct") is not None],
        "events": {state: sum(r["outcome"].get("events", {}).get(state, 0) for r in watch) for state in ("occurred", "not_occurred", "unknown")},
        "counts_toward_hit_rate": False}
    return {"groups": groups, "note": "Observational signal snapshots, not realized trades; excludes WATCH/unknown. Repeated signals on the same asset are correlated; report unique assets."}
