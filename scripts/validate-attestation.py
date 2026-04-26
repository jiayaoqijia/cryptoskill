#!/usr/bin/env python3
"""
Stage 2 of the trust-manifest attestation pipeline (TRUST.md §"Audit
attestation"): predicate body validation. Run AFTER `cosign
verify-attestation` has confirmed the signature; this script enforces the
predicate v1 required-field set and resolves the digests against bytes
the registry has actually fetched.

Stage-2 failure -> the calling pipeline writes
`audit.tier = unverified` and `audit.validation_error = <reason>` into
the skill's manifest. The audit is preserved (visible only via "show all
attestations" toggle), not deleted.

Usage:
  python3 scripts/validate-attestation.py path/to/statement.json
  python3 scripts/validate-attestation.py --stdin            # read from stdin
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PREDICATE_TYPE = "https://cryptoskill.org/attestations/skill-audit/v1"
REQUIRED_FIELDS = (
    "manifest_digest",
    "bom_digest",
    "report_digest",
    "extractor_version",
    "taxonomy_version",
    "hostlist_version",
    "reviewer_tiers_digest",
    "reviewed_at",
    "expires_at",
    "reviewer",
)
REVIEWER_REQUIRED = ("name", "identity", "tier")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class ValidationError(Exception):
    pass


def _ensure(cond: bool, msg: str) -> None:
    if not cond:
        raise ValidationError(msg)


def _ensure_str(obj, field: str) -> str:
    if not isinstance(obj, str):
        raise ValidationError(f"{field} must be a string; got {type(obj).__name__}")
    return obj


def _parse_iso(value, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be an ISO-8601 string; got {type(value).__name__}")
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        dt = datetime.fromisoformat(normalized)
    except (ValueError, TypeError) as exc:
        raise ValidationError(f"{field} is not a valid ISO-8601 timestamp: {value!r}") from exc
    if dt.tzinfo is None:
        raise ValidationError(f"{field} must be timezone-aware (use Z or explicit offset)")
    return dt.astimezone(timezone.utc)


def _resolve_digest(field: str, want: str, fetcher) -> None:
    """Re-derive the digest from the registry-fetched bytes for `field`."""
    if fetcher is None:
        return  # caller opted into signature-only validation
    bytes_ = fetcher(field)
    if bytes_ is None:
        raise ValidationError(f"{field} bytes not available in the registry")
    got = "sha256:" + hashlib.sha256(bytes_).hexdigest()
    if got != want:
        raise ValidationError(
            f"{field} digest mismatch: predicate says {want}, registry bytes hash to {got}"
        )


def validate_statement(stmt, fetcher=None) -> None:
    _ensure(isinstance(stmt, dict), f"top-level value must be a JSON object; got {type(stmt).__name__}")
    _type = stmt.get("_type")
    _ensure(isinstance(_type, str), f"_type must be a string; got {type(_type).__name__}")
    _ensure(_type.startswith("https://in-toto.io/Statement/v"),
            f"_type must be an in-toto Statement, got {_type!r}")
    pred_type = stmt.get("predicateType")
    _ensure(pred_type == PREDICATE_TYPE,
            f"predicateType must be {PREDICATE_TYPE!r}, got {pred_type!r}")
    pred = stmt.get("predicate")
    _ensure(isinstance(pred, dict), "predicate must be an object")

    missing = [f for f in REQUIRED_FIELDS if f not in pred]
    _ensure(not missing, f"predicate missing required field(s): {', '.join(missing)}")

    for digest_field in ("manifest_digest", "bom_digest", "report_digest", "reviewer_tiers_digest"):
        v = pred[digest_field]
        _ensure(isinstance(v, str), f"{digest_field} must be a string; got {type(v).__name__}")
        _ensure(DIGEST_RE.match(v) is not None,
                f"{digest_field} must match sha256:[0-9a-f]{{64}}; got {v!r}")

    _ensure_str(pred["extractor_version"], "extractor_version")
    _ensure(isinstance(pred["taxonomy_version"], int) and pred["taxonomy_version"] >= 0,
            f"taxonomy_version must be a non-negative int; got {pred['taxonomy_version']!r}")
    _ensure_str(pred["hostlist_version"], "hostlist_version")

    reviewed_at = _parse_iso(pred["reviewed_at"], "reviewed_at")
    expires_at = _parse_iso(pred["expires_at"], "expires_at")
    _ensure(expires_at > reviewed_at, "expires_at must be strictly after reviewed_at")

    reviewer = pred.get("reviewer")
    _ensure(isinstance(reviewer, dict), "reviewer must be an object")
    missing_r = [f for f in REVIEWER_REQUIRED if f not in reviewer]
    _ensure(not missing_r, f"reviewer missing required field(s): {', '.join(missing_r)}")
    _ensure_str(reviewer["name"], "reviewer.name")
    _ensure_str(reviewer["identity"], "reviewer.identity")
    _ensure(reviewer["tier"] in ("tier_1", "tier_2", "tier_3", "unverified"),
            f"reviewer.tier must be one of tier_1/tier_2/tier_3/unverified; got {reviewer['tier']!r}")

    # Risk-weighted TTL cap is enforced at the calling layer that knows the
    # skill's capability set; we surface the parsed timestamps for the
    # caller to gate.
    now = datetime.now(timezone.utc)
    if expires_at < now:
        # Soft warning (not an error) — stale attestations are legal but
        # hidden from Stage badges; we record a flag.
        sys.stderr.write(f"warning: attestation has expired ({expires_at.isoformat()})\n")

    # Re-derive digests if a fetcher is provided.
    for field in ("manifest_digest", "bom_digest", "report_digest", "reviewer_tiers_digest"):
        _resolve_digest(field, pred[field], fetcher)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", nargs="?", help="Path to in-toto Statement JSON; omit with --stdin")
    p.add_argument("--stdin", action="store_true")
    args = p.parse_args()
    if args.stdin:
        stmt = json.load(sys.stdin)
    else:
        if not args.path:
            print("usage: validate-attestation.py <path> | --stdin", file=sys.stderr)
            sys.exit(2)
        stmt = json.loads(Path(args.path).read_text(encoding="utf-8"))
    try:
        # No fetcher in CLI mode — Stage 2 in production is invoked by the
        # bot, which provides a fetcher closure that resolves digests
        # against the current registry state. The CLI form validates
        # structure only.
        validate_statement(stmt, fetcher=None)
    except ValidationError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        # Defense in depth: any unexpected exception during validation is
        # treated as INVALID rather than letting the calling pipeline see
        # a hard crash. Stage 2 must always exit 0 (OK) or 1 (INVALID).
        print(f"INVALID: validation failed with {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
