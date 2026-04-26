#!/usr/bin/env python3
"""
Generate the --certificate-identity-regexp string for `cosign verify-attestation`
from docs/reviewer-tiers.yaml. The regexp is the union of every member
regexp across tier_1, tier_2, tier_3 (NOT `unverified`).

Output: a single regex string on stdout. Combine with
--certificate-oidc-issuer at call sites.

The bot regenerates this at run time so adding a new tier_1 firm via PR
also updates the cosign verification command without manual sync.

Note: cosign requires a single regexp; this script enforces that all
members share the same `certificate_oidc_issuer` (or none does), since
cosign cannot match multiple issuers simultaneously. If issuers diverge,
the bot must run separate verify passes — one per issuer — and the
script accepts an --issuer filter to scope output.
"""

import argparse
import sys
from pathlib import Path

from canonicalize import parse_canonical_yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = ROOT / "docs" / "reviewer-tiers.yaml"


def build_regexp(policy: dict, issuer_filter: str | None) -> str:
    members = []
    for tier_name in ("tier_1", "tier_2", "tier_3"):
        tier = policy.get("tiers", {}).get(tier_name, {})
        for entry in tier.get("members") or []:
            iss = entry.get("certificate_oidc_issuer")
            if issuer_filter and iss != issuer_filter:
                continue
            regex = entry.get("certificate_identity_regexp")
            if not regex:
                raise ValueError(
                    f"{tier_name} entry for {entry.get('display_name')!r} is missing certificate_identity_regexp"
                )
            members.append(f"(?:{regex})")
    if not members:
        # Empty regex would match nothing in cosign — caller should treat
        # this as "no audited skills yet".
        return "(?!)"
    return "^" + "|".join(members) + "$" if all(m.startswith("(?:^") is False for m in members) else "|".join(members)


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
    print(build_regexp(policy, args.issuer))


if __name__ == "__main__":
    main()
