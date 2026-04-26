#!/usr/bin/env python3
"""
Stage 3 of the trust-manifest attestation pipeline (TRUST.md §"Audit
attestation"): signer authorization re-check against the policy snapshot
pinned in the predicate body (NOT the current HEAD).

CRITICAL: the cert identity and OIDC issuer used for authorization MUST
come from the verified Sigstore certificate (as printed by Stage 1
`cosign verify-attestation --output json`), NOT from
`predicate.reviewer.identity`. The latter is a self-asserted claim and
can be set to anything by the signer; using it would let any signer
forge tier_1 status. We accept the verified values via CLI args.

Inputs:
  --statement <path>           in-toto Statement JSON (already signature-verified)
  --policy <path>              reviewer-tiers.yaml at the digest pinned in the predicate
  --cert-identity <str>        Verified cert identity (from cosign output)
  --cert-issuer <url>          Verified OIDC issuer URL (from cosign output)

Exit codes:
  0  signer authorized AND predicate.reviewer.tier matches verified tier
  1  signer NOT in the pinned policy at any tier (=> unverified)
  2  pinned policy digest mismatch (=> reject the attestation outright)
  3  malformed inputs
  4  signer authorized but predicate claimed a different tier
     (the verified tier supersedes the claim; pipeline SHOULD render
     with disclaimer rather than display the claimed tier)
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


def _full_match(pattern: str, value: str) -> bool:
    if not pattern:
        return False  # empty pattern must NOT match anything
    try:
        return re.fullmatch(pattern, value) is not None
    except re.error:
        return False


def check(statement: dict, policy: dict, policy_path: Path,
          cert_identity: str, cert_issuer: str) -> tuple[int, str]:
    pred = statement.get("predicate") or {}
    pinned = pred.get("reviewer_tiers_digest")
    actual = _digest_of(policy_path)
    if pinned != actual:
        return 2, (
            f"pinned reviewer_tiers_digest {pinned} != supplied policy digest {actual}; "
            "re-resolve at the pinned commit"
        )

    for tier_name in ("tier_1", "tier_2", "tier_3"):
        tier = (policy.get("tiers") or {}).get(tier_name) or {}
        for entry in tier.get("members") or []:
            iss = entry.get("certificate_oidc_issuer") or ""
            regex = entry.get("certificate_identity_regexp") or ""
            if not iss or not regex:
                # Malformed policy entry — fail closed.
                continue
            if cert_issuer != iss:
                continue
            if _full_match(regex, cert_identity):
                claimed = (pred.get("reviewer") or {}).get("tier")
                if claimed != tier_name:
                    return 4, (
                        f"signer authorized at {tier_name} (verified cert); "
                        f"predicate claimed {claimed!r} — render with "
                        "disclaimer or downgrade to verified tier"
                    )
                return 0, f"signer authorized at {tier_name}"
    return 1, (
        f"verified cert identity {cert_identity!r} (issuer {cert_issuer!r}) "
        "is not present in pinned reviewer-tiers policy"
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--statement", required=True)
    p.add_argument("--policy", required=True, help="reviewer-tiers.yaml at the pinned digest")
    p.add_argument("--cert-identity", required=True,
                   help="Cert identity from cosign Stage 1 --output json")
    p.add_argument("--cert-issuer", required=True,
                   help="OIDC issuer URL from cosign Stage 1 --output json")
    args = p.parse_args()

    if not args.cert_identity or not args.cert_issuer:
        print("--cert-identity and --cert-issuer are required and must be non-empty",
              file=sys.stderr)
        sys.exit(3)

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

    code, msg = check(stmt, policy, policy_path, args.cert_identity, args.cert_issuer)
    if code == 0:
        print(f"OK: {msg}")
    elif code == 4:
        print(f"AUTHORIZED-WITH-DISCLAIMER (4): {msg}", file=sys.stderr)
    else:
        print(f"REJECT ({code}): {msg}", file=sys.stderr)
    sys.exit(code)


if __name__ == "__main__":
    main()
