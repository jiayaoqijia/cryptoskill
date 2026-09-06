#!/usr/bin/env python3
"""Terraform Plan Risk Auditor.

Analyze `terraform show -json plan.out` output for risky changes and emit a
structured, deterministic risk report.

This script is intentionally self-contained (stdlib only) and uses JSON I/O.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


SEVERITY_ORDER: Dict[str, int] = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
SEVERITY_WEIGHT: Dict[str, int] = {"CRITICAL": 35, "HIGH": 20, "MEDIUM": 10, "LOW": 4}


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def _success(data: Dict[str, Any]) -> str:
    return _json_dumps({"ok": True, "data": data})


def _error(message: str, details: Optional[Dict[str, Any]] = None) -> str:
    payload: Dict[str, Any] = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    return _json_dumps(payload)


def _read_stdin_json() -> Optional[Dict[str, Any]]:
    if sys.stdin is None or sys.stdin.isatty():
        return None
    raw = sys.stdin.read().strip()
    if not raw:
        return None
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("stdin JSON must be an object")
    return parsed


def _load_plan(params: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(params.get("plan_json"), dict):
        return params["plan_json"]

    if isinstance(params.get("plan_json_text"), str):
        return json.loads(params["plan_json_text"])

    if isinstance(params.get("plan_path"), str):
        path = params["plan_path"]
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    raise ValueError("One of plan_json, plan_json_text, or plan_path is required")


def _severity_key(sev: str) -> Tuple[int, str]:
    return (SEVERITY_ORDER.get(sev, 999), sev)


def _actions_to_kind(actions: Sequence[str]) -> str:
    # Terraform uses e.g. ["delete", "create"] for replace.
    a = set(actions)
    if "create" in a and "delete" in a:
        return "replace"
    if actions == ["create"] or a == {"create"}:
        return "create"
    if actions == ["update"] or a == {"update"}:
        return "update"
    if actions == ["delete"] or a == {"delete"}:
        return "delete"
    # catch-all for unknown combinations (e.g. no-op, read)
    return "other"


def _contains_iam(resource_type: str) -> bool:
    t = (resource_type or "").lower()
    # Common patterns: aws_iam_*, google_project_iam_*, azurerm_role_*
    return "iam" in t or "_iam_" in t


def _is_networkish(resource_type: str) -> bool:
    t = (resource_type or "").lower()
    keywords = [
        "vpc",
        "subnet",
        "route",
        "internet_gateway",
        "nat_gateway",
        "network_acl",
        "firewall",
        "security_group",
        "sg_rule",
    ]
    return any(k in t for k in keywords)


def _walk_values(obj: Any) -> Iterable[Any]:
    if isinstance(obj, dict):
        for v in obj.values():
            yield v
            yield from _walk_values(v)
    elif isinstance(obj, list):
        for v in obj:
            yield v
            yield from _walk_values(v)


def _extract_open_cidrs(obj: Any) -> List[str]:
    open_cidrs = []
    for v in _walk_values(obj):
        if isinstance(v, str):
            if v == "0.0.0.0/0" or v == "::/0":
                open_cidrs.append(v)
        elif isinstance(v, list):
            for item in v:
                if item == "0.0.0.0/0" or item == "::/0":
                    open_cidrs.append(item)
    # Stable dedupe
    return sorted(set(open_cidrs))


def _is_s3ish(resource_type: str) -> bool:
    t = (resource_type or "").lower()
    return "s3" in t and "bucket" in t


def _detect_public_bucket(before: Any, after: Any) -> Tuple[bool, Dict[str, Any], float]:
    """Heuristic detection of public S3 bucket exposure."""

    before = before or {}
    after = after or {}

    def get_all_kv(d: Any) -> List[Tuple[str, Any]]:
        out: List[Tuple[str, Any]] = []
        if isinstance(d, dict):
            for k, v in d.items():
                out.append((str(k), v))
                out.extend(get_all_kv(v))
        elif isinstance(d, list):
            for item in d:
                out.extend(get_all_kv(item))
        return out

    public_acl_values = {"public-read", "public-read-write"}
    risky_flags = {
        "public": True,
        "public_read_access": True,
        "public_access": True,
        "block_public_acls": False,
        "ignore_public_acls": False,
        "restrict_public_buckets": False,
        "block_public_policy": False,
    }

    before_kv = {k: v for k, v in get_all_kv(before)}
    after_kv = {k: v for k, v in get_all_kv(after)}

    reasons: List[str] = []

    acl_before = str(before_kv.get("acl", "")).lower() if "acl" in before_kv else ""
    acl_after = str(after_kv.get("acl", "")).lower() if "acl" in after_kv else ""
    if acl_after in public_acl_values and acl_before != acl_after:
        reasons.append(f"acl set to {acl_after}")

    for k, risky_val in risky_flags.items():
        if k in after_kv and after_kv.get(k) == risky_val and before_kv.get(k) != risky_val:
            reasons.append(f"{k}={json.dumps(risky_val)}")

    if not reasons:
        return False, {}, 0.0

    details = {"signals": sorted(reasons)}
    return True, details, 0.6


def _diff_simple(before: Any, after: Any, keys: Sequence[str]) -> Dict[str, Any]:
    before = before or {}
    after = after or {}
    out: Dict[str, Any] = {}
    if not isinstance(before, dict) or not isinstance(after, dict):
        return out
    for k in keys:
        if k in after and before.get(k) != after.get(k):
            out[k] = {"before": before.get(k), "after": after.get(k)}
    return out


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    resource_address: str
    actions: List[str]
    message: str
    remediation: str
    details: Dict[str, Any]
    confidence: Optional[float] = None

    def to_json(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "resource_address": self.resource_address,
            "actions": self.actions,
            "message": self.message,
            "details": self.details,
            "remediation": self.remediation,
        }
        if self.confidence is not None:
            out["confidence"] = self.confidence
        return out


def analyze_plan(plan: Dict[str, Any], *, max_findings: int, focus: str) -> Dict[str, Any]:
    resource_changes = plan.get("resource_changes")
    if resource_changes is None:
        resource_changes = []
    if not isinstance(resource_changes, list):
        raise ValueError("plan_json.resource_changes must be a list")

    counts = {"create": 0, "update": 0, "delete": 0, "replace": 0}
    findings: List[Finding] = []

    for rc in resource_changes:
        if not isinstance(rc, dict):
            continue

        address = str(rc.get("address") or rc.get("name") or "<unknown>")
        rtype = str(rc.get("type") or "")
        change = rc.get("change") or {}
        if not isinstance(change, dict):
            change = {}
        actions = change.get("actions") or []
        if not isinstance(actions, list) or not all(isinstance(a, str) for a in actions):
            actions = []
        actions_norm = [a for a in actions]

        kind = _actions_to_kind(actions_norm)
        if kind in counts:
            counts[kind] += 1

        before = change.get("before")
        after = change.get("after")

        # --- Rules ---

        # 1) Any delete => HIGH
        if focus in ("all", "security") and "delete" in actions_norm and "create" not in actions_norm:
            findings.append(
                Finding(
                    rule_id="TF_DESTROY",
                    severity="HIGH",
                    resource_address=address,
                    actions=actions_norm,
                    message="Resource will be destroyed",
                    details={"resource_type": rtype},
                    remediation="Confirm this is intended; consider lifecycle.prevent_destroy where applicable.",
                    confidence=1.0,
                )
            )

        # 2) Replace => HIGH
        if focus in ("all", "security") and "delete" in actions_norm and "create" in actions_norm:
            findings.append(
                Finding(
                    rule_id="TF_REPLACE",
                    severity="HIGH",
                    resource_address=address,
                    actions=actions_norm,
                    message="Resource will be replaced (delete+create)",
                    details={"resource_type": rtype},
                    remediation="Validate replacement is safe; consider in-place updates or blue/green when possible.",
                    confidence=1.0,
                )
            )

        # 3) IAM resources => HIGH (esp. if delete/replace)
        if focus in ("all", "security") and rtype and _contains_iam(rtype):
            sev = "HIGH"
            findings.append(
                Finding(
                    rule_id="TF_IAM_CHANGE",
                    severity=sev,
                    resource_address=address,
                    actions=actions_norm,
                    message="IAM-related resource change detected",
                    details={"resource_type": rtype},
                    remediation="Review IAM diffs carefully; verify least-privilege and rollout plan.",
                    confidence=0.9,
                )
            )

        # 4) Open ingress 0.0.0.0/0 or ::/0 added in security group/firewall contexts => CRITICAL
        if focus in ("all", "security") and rtype and ("security_group" in rtype.lower() or "firewall" in rtype.lower()):
            before_open = set(_extract_open_cidrs(before))
            after_open = set(_extract_open_cidrs(after))
            added = sorted(after_open - before_open)
            if added:
                findings.append(
                    Finding(
                        rule_id="TF_OPEN_INGRESS",
                        severity="CRITICAL",
                        resource_address=address,
                        actions=actions_norm,
                        message="Potential public ingress detected (0.0.0.0/0 or ::/0)",
                        details={"resource_type": rtype, "open_cidrs_added": added},
                        remediation="Restrict CIDRs to known networks; use least-exposure ingress rules.",
                        confidence=0.8,
                    )
                )

        # 5) S3 public exposure heuristic => CRITICAL
        if focus in ("all", "security") and rtype and _is_s3ish(rtype):
            is_public, details, conf = _detect_public_bucket(before, after)
            if is_public:
                findings.append(
                    Finding(
                        rule_id="TF_S3_PUBLIC_EXPOSURE",
                        severity="CRITICAL",
                        resource_address=address,
                        actions=actions_norm,
                        message="Potential S3 public exposure detected",
                        details={"resource_type": rtype, **details},
                        remediation="Enable S3 Block Public Access; avoid public ACLs/policies unless explicitly required.",
                        confidence=conf,
                    )
                )

        # 6) Network-ish changes => MEDIUM
        if focus in ("all", "security") and rtype and _is_networkish(rtype) and kind in {"create", "update", "replace"}:
            changes = _diff_simple(before, after, ["cidr_block", "cidr_blocks", "ipv6_cidr_blocks", "ingress", "egress"])
            findings.append(
                Finding(
                    rule_id="TF_NETWORK_CHANGE",
                    severity="MEDIUM",
                    resource_address=address,
                    actions=actions_norm,
                    message="Network-related resource change detected",
                    details={"resource_type": rtype, "highlights": changes} if changes else {"resource_type": rtype},
                    remediation="Review network exposure and routing impact; validate against intended architecture.",
                    confidence=0.7,
                )
            )

        # Optional: cost-ish changes
        if focus in ("all", "cost") and kind in {"create", "update", "replace"}:
            cost_keys = [
                "instance_type",
                "allocated_storage",
                "storage_gb",
                "node_count",
                "desired_capacity",
                "min_size",
                "max_size",
            ]
            delta = _diff_simple(before, after, cost_keys)
            if delta:
                findings.append(
                    Finding(
                        rule_id="TF_COST_SCALING",
                        severity="MEDIUM",
                        resource_address=address,
                        actions=actions_norm,
                        message="Potential cost-impacting change detected",
                        details={"resource_type": rtype, "changes": delta},
                        remediation="Estimate cost deltas (FinOps) and confirm the scaling change is intended.",
                        confidence=0.5,
                    )
                )

    # Deterministic ordering and limiting
    findings.sort(
        key=lambda f: (
            SEVERITY_ORDER.get(f.severity, 999),
            f.resource_address,
            f.rule_id,
        )
    )
    if max_findings < 1:
        max_findings = 1
    findings = findings[: max_findings]

    by_resource: Dict[str, Tuple[str, str]] = {}
    for f in findings:
        prev = by_resource.get(f.resource_address)
        if prev is None or SEVERITY_ORDER.get(f.severity, 999) < SEVERITY_ORDER.get(prev[0], 999):
            by_resource[f.resource_address] = (f.severity, f.message)

    top_resources = [
        {"resource_address": addr, "severity": sev, "reason": msg}
        for addr, (sev, msg) in sorted(
            by_resource.items(), key=lambda kv: (SEVERITY_ORDER.get(kv[1][0], 999), kv[0])
        )
    ][:5]

    risk_score = min(100, sum(SEVERITY_WEIGHT.get(f.severity, 0) for f in findings))

    if any(f.severity == "CRITICAL" for f in findings):
        risk_level = "CRITICAL"
    elif any(f.severity == "HIGH" for f in findings):
        risk_level = "HIGH"
    elif any(f.severity == "MEDIUM" for f in findings):
        risk_level = "MEDIUM"
    elif any(f.severity == "LOW" for f in findings):
        risk_level = "LOW"
    else:
        risk_level = "LOW"

    total_changes = sum(counts.values())

    return {
        "summary": {
            "create": counts["create"],
            "update": counts["update"],
            "delete": counts["delete"],
            "replace": counts["replace"],
            "total_changes": total_changes,
        },
        "risk_score": int(risk_score),
        "risk_level": risk_level,
        "findings": [f.to_json() for f in findings],
        "top_resources": top_resources,
    }


def _demo_plan() -> Dict[str, Any]:
    # Minimal, realistic subset of a terraform show -json plan
    return {
        "format_version": "1.1",
        "terraform_version": "1.6.0",
        "resource_changes": [
            {
                "address": "aws_security_group_rule.allow_http",
                "mode": "managed",
                "type": "aws_security_group_rule",
                "name": "allow_http",
                "change": {
                    "actions": ["create"],
                    "before": None,
                    "after": {
                        "type": "ingress",
                        "from_port": 80,
                        "to_port": 80,
                        "protocol": "tcp",
                        "cidr_blocks": ["0.0.0.0/0"],
                    },
                },
            },
            {
                "address": "aws_db_instance.main",
                "mode": "managed",
                "type": "aws_db_instance",
                "name": "main",
                "change": {
                    "actions": ["delete"],
                    "before": {"identifier": "prod-db", "engine": "postgres"},
                    "after": None,
                },
            },
            {
                "address": "aws_iam_policy.app_policy",
                "mode": "managed",
                "type": "aws_iam_policy",
                "name": "app_policy",
                "change": {
                    "actions": ["update"],
                    "before": {"name": "app-policy", "policy": "{...old...}"},
                    "after": {"name": "app-policy", "policy": "{...new...}"},
                },
            },
            {
                "address": "aws_vpc.main",
                "mode": "managed",
                "type": "aws_vpc",
                "name": "main",
                "change": {
                    "actions": ["create"],
                    "before": None,
                    "after": {"cidr_block": "10.0.0.0/16"},
                },
            },
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Terraform plan JSON for risky changes")
    parser.add_argument("--demo", action="store_true", help="Run with embedded demo plan")
    parser.add_argument("--params", type=str, help="JSON parameters")

    args = parser.parse_args()

    try:
        if args.demo:
            params: Dict[str, Any] = {"plan_json": _demo_plan()}
            max_findings = 50
            focus = "all"
            report = analyze_plan(params["plan_json"], max_findings=max_findings, focus=focus)
            report["demo"] = True
            print(_success(report))
            return 0

        if args.params:
            params = json.loads(args.params)
            if not isinstance(params, dict):
                raise ValueError("--params JSON must be an object")
        else:
            stdin_params = _read_stdin_json()
            if stdin_params is None:
                print(_error("Either --demo, --params, or stdin JSON must be provided"))
                return 2
            params = stdin_params

        max_findings_raw = params.get("max_findings", 50)
        if not isinstance(max_findings_raw, int):
            raise ValueError("max_findings must be an integer")
        max_findings = max_findings_raw

        focus = params.get("focus", "all")
        if focus not in {"all", "security", "cost"}:
            raise ValueError("focus must be one of: all, security, cost")

        plan = _load_plan(params)
        if not isinstance(plan, dict):
            raise ValueError("Loaded plan JSON must be an object")

        report = analyze_plan(plan, max_findings=max_findings, focus=focus)
        report["demo"] = False
        print(_success(report))
        return 0

    except FileNotFoundError as e:
        print(_error("Plan file not found", {"path": str(e)}))
        return 1
    except json.JSONDecodeError as e:
        print(_error("Invalid JSON", {"message": str(e)}))
        return 1
    except ValueError as e:
        print(_error(str(e)))
        return 1
    except Exception as e:
        print(_error("Unexpected error", {"message": str(e)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
