#!/usr/bin/env python3
"""Crypto research data CLI. All investment interpretation belongs to the host model."""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

from common import VERSION, ensure_runtime, now, read_json, safe_id, write_json
from collect import collect, configure_transport, import_native, prepare, request, transport_settings
from ledger import audit, due, record_decision, record_erratum, record_review, summary
from metrics import calculate
from install import verify as verify_manifest
from review_log import append_entry, build_entry, parse_outcomes, parse_started
from factcheck import finalize as finalize_factcheck, skeleton as factcheck_skeleton, validate as validate_factcheck


def doctor(network: bool) -> dict:
    proxy, hosts = transport_settings()
    result = {"status": "local_ready", "skill_version": VERSION, "python": platform.python_version(),
              "python_supported": sys.version_info >= (3, 10), "skill_path": str(Path(__file__).resolve().parents[1]),
              "optional_credentials_configured": {key: bool(os.environ.get(key)) for key in
                   ("COINGECKO_DEMO_API_KEY", "BRAVE_SEARCH_API_KEY")},
              "native_x": "Must test host x tools; subscription is not an API credential; no cookies read by scripts.",
              "transport": {"trusted_proxy_ip": proxy, "trusted_public_hosts": sorted(hosts)}, "network": {}}
    try:
        members = verify_manifest(Path(__file__).resolve().parents[1])
        result["manifest"] = {"status": "ok", "members": len(members), "models_md_pinned": "references/models.md" in members}
    except Exception as exc:
        result["manifest"] = {"status": "failed", "reason": str(exc)}
        result["status"] = "degraded"
    if network:
        for name, url in {"dexscreener": "https://api.dexscreener.com/latest/dex/search?q=ethereum",
                          "binance_public_data": "https://data-api.binance.vision/api/v3/time"}.items():
            try:
                payload, _ = request(url)
                json.loads(payload)
                result["network"][name] = {"status": "ok", "checked_at": now()}
            except Exception as exc:
                result["network"][name] = {"status": "unavailable", "error_type": type(exc).__name__,
                                         "reason": str(exc) if isinstance(exc, ValueError) else "Network/provider request failed", "checked_at": now()}
        result["status"] = "network_ready" if result["status"] != "degraded" and all(row["status"] == "ok" for row in result["network"].values()) else "degraded"
    return result


def review_log(args) -> dict:
    """Always appends a line, even if doctor or due fails; failures are recorded as errors."""
    from datetime import datetime, timezone
    started = parse_started(args.started_at) or datetime.now(timezone.utc)
    errors = list(args.error)
    root = ensure_runtime(args.runtime)
    try:
        configure_transport(root)
        doctor_status = doctor(False)["status"]
    except Exception as exc:
        doctor_status, _ = "error", errors.append(f"doctor: {type(exc).__name__}: {exc}")
    try:
        outcomes = parse_outcomes(args.outcome)
    except ValueError as exc:
        outcomes, _ = {}, errors.append(str(exc))
    try:
        audit(root)
        rows = due(root, args.at)
    except Exception as exc:
        rows, _ = None, errors.append(f"due: {type(exc).__name__}: {exc}")
    entry = build_entry(started=started, finished=datetime.now(timezone.utc), doctor_status=doctor_status,
                        due_items=rows, outcomes=outcomes, agent=args.agent, model=args.model, errors=errors)
    path = append_entry(root, entry)
    return {"review_runs_path": str(path), **entry}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("doctor")
    p.add_argument("--network", action="store_true")
    p.add_argument("--runtime", help="Read this runtime's explicitly configured platform transport.json")
    for name in ("collect", "prepare", "metrics", "record", "errata", "due", "review", "stats", "audit"):
        p = sub.add_parser(name)
        p.add_argument("--runtime", required=True, help="Data directory outside installed skill")
        if name in {"collect", "prepare"}:
            p.add_argument("--run-id", required=True)
            p.add_argument("--full", action="store_true", help="Print full evidence; default prints only index and file paths")
        if name == "collect":
            p.add_argument("--plan", required=True)
        if name == "prepare":
            p.add_argument("--native", help="Actual captured host search/X evidence JSON")
        if name in {"metrics", "record", "review", "errata"}:
            p.add_argument("--input", required=True)
        if name in {"record", "review"}:
            p.add_argument("--evidence", required=True)
        if name == "due":
            p.add_argument("--at", help="Audit/testing only; normal scheduled runs omit this")
    p = sub.add_parser("review-log", help="Append one line per routine run to RUNTIME/review_runs.jsonl (append-only)")
    p.add_argument("--runtime", required=True)
    p.add_argument("--agent", help="Executing agent; unknown if omitted")
    p.add_argument("--model", help="Model actually used; unknown if omitted")
    p.add_argument("--started-at", help="ISO time the routine started; defaults to now")
    p.add_argument("--outcome", action="append", default=[], help="<decision_id>:<horizon>=reviewed|pending_data|failed")
    p.add_argument("--error", action="append", default=[])
    p.add_argument("--at", help="Audit/testing only: evaluate due at this time")
    p = sub.add_parser("factcheck", help="Quick fact-check (0.1.6): no signals, no ledger, no reviews")
    fsub = p.add_subparsers(dest="action", required=True)
    f = fsub.add_parser("new", help="Print (or write) a skeleton record for one claim; touches no runtime")
    f.add_argument("--claim", required=True)
    f.add_argument("--requested-by", choices=("user", "bot"), default="user")
    f.add_argument("--requester-name")
    f.add_argument("--id")
    f.add_argument("--supersedes")
    f.add_argument("--output", help="Write skeleton to this new file (never overwrites)")
    f = fsub.add_parser("validate", help="Check a filled record; exit 2 on errors")
    f.add_argument("--input", required=True)
    f = fsub.add_parser("finalize", help="Validate and save append-only to RUNTIME/factchecks/<id>.json")
    f.add_argument("--runtime", required=True)
    f.add_argument("--input", required=True)
    args = parser.parse_args()
    if args.command == "factcheck":
        if args.action == "new":
            result = factcheck_skeleton(args.claim, args.requested_by, args.requester_name, args.id, args.supersedes)
            if args.output:
                write_json(args.output, result, exclusive=True)
        elif args.action == "validate":
            result = validate_factcheck(read_json(args.input))
            result["status"] = "ok" if not result["errors"] else "invalid"
        else:
            result = finalize_factcheck(read_json(args.input), ensure_runtime(args.runtime))
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        if result.get("status") == "invalid":
            sys.exit(2)
        return
    if args.command == "review-log":
        result = review_log(args)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return
    if args.command == "doctor":
        if args.runtime:
            configure_transport(ensure_runtime(args.runtime))
        result = doctor(args.network)
    else:
        root = ensure_runtime(args.runtime)
        configure_transport(root)
        if args.command == "collect":
            run = root / "runs" / safe_id(args.run_id)
            if (run / "collection.json").exists():
                raise ValueError("Run already exists; use a new run-id")
            plan = read_json(args.plan)
            write_json(run / "plan.json", plan, exclusive=True)
            result = collect(plan, root)
            write_json(run / "collection.json", result, exclusive=True)
            if not args.full:
                result = {"collection_path": str(run / "collection.json"), "requests_planned": result["requests_planned"],
                          "cache_hits": result["cache_hits"], "gaps": result["gaps"],
                          "records": [{k: row.get(k) for k in ("evidence_id", "kind", "status", "url", "raw_path")}
                                      for row in result["records"]]}
        elif args.command == "prepare":
            run = root / "runs" / safe_id(args.run_id)
            native = import_native(read_json(args.native)) if args.native else None
            result = prepare(read_json(run / "collection.json"), native)
            write_json(run / "evidence.json", result, exclusive=True)
            if not args.full:
                result = {"evidence_path": str(run / "evidence.json"), "gaps": result.get("gaps", []),
                          "records": [{k: row.get(k) for k in ("evidence_id", "kind", "status", "duplicate_of", "raw_path")}
                                      for row in result["records"]]}
        elif args.command == "metrics":
            document = read_json(args.input)
            result = {"created_at": now(), "operation": document["operation"],
                      "evidence_refs": document.get("evidence_refs", []), "result": calculate(document)}
            write_json(root / "calculations" / (Path(args.input).stem + "-" + now().replace(":", "") + ".json"), result, exclusive=True)
        elif args.command == "record":
            result = record_decision(read_json(args.input), read_json(args.evidence), root)
        elif args.command == "errata":
            result = record_erratum(read_json(args.input), root)
        elif args.command == "review":
            result = record_review(read_json(args.input), read_json(args.evidence), root)
        elif args.command == "due":
            audit(root)
            result = {"due": due(root, args.at)}
        elif args.command == "stats":
            audit(root)
            result = summary(root)
        else:
            result = audit(root)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    if args.command == "doctor" and result["status"] == "degraded":
        sys.exit(3)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, StopIteration, FileExistsError, FileNotFoundError) as exc:
        print(json.dumps({"status": "error", "error": type(exc).__name__, "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
