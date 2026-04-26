#!/usr/bin/env python3
"""
Generate the --certificate-identity-regexp string for `cosign verify-attestation`
from docs/reviewer-tiers.yaml. The regexp is the union of every member
regexp across tier_1, tier_2, tier_3 (NOT `unverified`).

Output: a single regex string on stdout. Combine with
--certificate-oidc-issuer at call sites.

Cosign accepts only one --certificate-oidc-issuer per call. To safely emit
a single regex, all included members MUST share the same issuer; the
script enforces this and aborts otherwise. Pass --issuer to scope to a
specific issuer when the policy mixes providers.

Each member regex must be present and non-empty; an empty regex would
match anything in cosign and silently authorize attestations the policy
never issued.
"""

import argparse
import sys
from pathlib import Path

from canonicalize import parse_canonical_yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = ROOT / "docs" / "reviewer-tiers.yaml"


class PolicyError(Exception):
    pass


def collect_members(policy: dict, issuer_filter: str | None):
    members = []
    for tier_name in ("tier_1", "tier_2", "tier_3"):
        tier = policy.get("tiers", {}).get(tier_name, {})
        for entry in tier.get("members") or []:
            iss = entry.get("certificate_oidc_issuer")
            regex = entry.get("certificate_identity_regexp")
            display = entry.get("display_name") or "<unnamed>"
            if not iss:
                raise PolicyError(
                    f"{tier_name}/{display}: certificate_oidc_issuer is required"
                )
            if not regex:
                raise PolicyError(
                    f"{tier_name}/{display}: certificate_identity_regexp is required and must be non-empty"
                )
            if issuer_filter and iss != issuer_filter:
                continue
            members.append((tier_name, display, iss, regex))
    return members


def build_regexp(members) -> str:
    """Wrap each member pattern in a non-capturing group and OR them.

    Cosign uses Go's regexp/syntax (RE2). The alternation precedence rules
    require the WHOLE alternation be grouped, otherwise `^a|b$` parses as
    `(?:^a)|(?:b$)` and authorizes any identity ending with the second
    alternative. We always emit `(?:p1|p2|...)`.
    """
    if not members:
        return "(?!)"  # never matches anything; cosign call will fail-closed
    return "(?:" + "|".join(f"(?:{m[3]})" for m in members) + ")"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--policy", default=str(POLICY_PATH))
    p.add_argument("--issuer", help="Restrict to this OIDC issuer URL")
    args = p.parse_args()

    text = Path(args.policy).read_text(encoding="utf-8")
    try:
        policy = parse_canonical_yaml(text)
    except ValueError as exc:
        print(f"reviewer-tiers.yaml violates canonical-form constraints: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        members = collect_members(policy, args.issuer)
    except PolicyError as exc:
        print(f"policy error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not args.issuer and members:
        issuers = {m[2] for m in members}
        if len(issuers) > 1:
            print(
                "policy mixes OIDC issuers but --issuer was not given; cosign "
                "accepts only one --certificate-oidc-issuer at a time. Re-run "
                f"with --issuer set to one of: {sorted(issuers)}",
                file=sys.stderr,
            )
            sys.exit(1)

    print(build_regexp(members))


if __name__ == "__main__":
    main()
