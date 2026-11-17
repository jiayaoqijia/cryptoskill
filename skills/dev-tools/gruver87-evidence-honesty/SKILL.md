---
name: evidence-honesty
description: >-
  Fail-closed claims for DUP Labs — packs on disk, no invented PASS, no soak
  without approx_48h_claim_ok. Use for readiness, audit language, marketing
  copy, CHANGELOG, or diligence text.
license: MIT
compatibility: Policy skill; cite on-disk packs in dup-market-radar or dup-protocol*.
metadata:
  author: dup-labs
  version: "0.1.6"
  product: dup-labs
---

# Evidence honesty

## When to Use

- Any readiness / PASS / mainnet / soak statement
- Editing CHANGELOG, README badges, diligence briefs

## Steps

1. Identify product (radar vs L1 pin vs experimental).
2. Require pack path or refuse.
3. Use matrix in [references/claim-matrix.md](references/claim-matrix.md).

## Refuse

- “Mainnet ready” without sealed packs.
- Equating CI green with soak PASS.
- Mixing radar and L1 evidence — skill `l1-boundary`.
