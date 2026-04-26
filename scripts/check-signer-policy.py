#!/usr/bin/env python3
"""
Stage 3 of the trust-manifest attestation pipeline (TRUST.md §"Audit
attestation"): signer authorization re-check against the policy snapshot
pinned in the predicate body (NOT the current HEAD).

This step catches the case where a reviewer was tier_1/tier_2/tier_3 at
sign time but is no longer on the policy today — the attestation stays
visible but is badged "reviewer tier was downgraded after signing", and
a tier never granted at the pinned snapshot lands in `unverified`.

Inputs:
  --statement <path>   in-toto Statement JSON (already signature-verified)
  --policy <path>      reviewer-tiers.yaml at the digest pinned in the predicate

The bot resolves the pinned digest to bytes via git (the policy file is
versioned in this repo); this CLI accepts either the resolved file or
the raw git ref.

Exit codes:
  0  signer authorized at the pinned snapshot
  1  signer NOT in the pinned policy at any tier (=> unverified)
  2  pinned policy digest mismatch (=> reject the attestation outright)
  3  malformed inputs
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from canonicalize import parse_canonical_yaml, to_canonical_json_bytes

ROOT = Path(__file__).resolve().parent.parent


def _digest_of(path: Path) -> str:
    return "sha256:" + hashlib.sha256(
        to_canonical_json_bytes(path.read_text(encoding="utf-8"))
    ).hexdigest()


def _identity_matches(cert_identity: str, regex: str) -> bool:
    try:
        return re.match(regex, cert_identity) is not None
    except re.error:
        return False


def check(statement: dict, policy: dict, policy_path: Path) -> tuple[int, str]:
    pred = statement.get("predicate", {})
    pinned = pred.get("reviewer_tiers_digest")
    actual = _digest_of(policy_path)
    if pinned != actual:
        return 2, (
            f"pinned reviewer_tiers_digest {pinned} != supplied policy digest {actual}; "
            "the bot must re-check at the pinned commit"
        )

    reviewer = pred.get("reviewer", {})
    cert_identity = reviewer.get("identity") or ""
    cert_issuer = reviewer.get("certificate_oidc_issuer")

    for tier_name in ("tier_1", "tier_2", "tier_3"):
        tier = policy.get("tiers", {}).get(tier_name, {})
        for entry in tier.get("members") or []:
            iss = entry.get("certificate_oidc_issuer")
            regex = entry.get("certificate_identity_regexp", "")
            if cert_issuer and iss and cert_issuer != iss:
                continue
            if _identity_matches(cert_identity, regex):
                # Bonus: cross-check the predicate's claimed tier with the
                # tier the cert was actually granted under.
                claimed = reviewer.get("tier")
                if claimed != tier_name:
                    return 0, (
                        f"signer authorized at {tier_name}; predicate claimed {claimed!r} "
                        "(rendered with disclaimer)"
                    )
                return 0, f"signer authorized at {tier_name}"
    return 1, "signer identity not present in pinned reviewer-tiers policy"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--statement", required=True)
    p.add_argument("--policy", required=True, help="reviewer-tiers.yaml at the pinned digest")
    args = p.parse_args()

    try:
        stmt = json.loads(Path(args.statement).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"malformed statement JSON: {exc}", file=sys.stderr)
        sys.exit(3)
    try:
        policy_path = Path(args.policy)
        policy = parse_canonical_yaml(policy_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"malformed/non-canonical policy YAML: {exc}", file=sys.stderr)
        sys.exit(3)

    code, msg = check(stmt, policy, policy_path)
    if code == 0:
        print(f"OK: {msg}")
    else:
        print(f"REJECT ({code}): {msg}", file=sys.stderr)
    sys.exit(code)


if __name__ == "__main__":
    main()
