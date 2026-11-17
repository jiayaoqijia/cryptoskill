---
name: l1-boundary
description: >-
  Keep DUP L1 mesh evidence separate from Market Radar and trading-bot packs.
  Use when mixing readiness claims, soak language, or repo URLs across products.
license: MIT
compatibility: Policy skill across dup-protocol, dup-protocol-experimental, dup-market-radar.
metadata:
  author: dup-labs
  version: "0.1.6"
  product: dup-labs
---

# L1 vs radar boundary

## When to Use

- User cites “mesh soak” for radar (or reverse)
- Docs/README that blur products

## Boundaries

| Product | Repo | Evidence |
|---------|------|----------|
| L1 industrial pin | `Gruver87/dup-protocol` | mesh probe / industrial_gate / sealed packs |
| L1 experimental | `Gruver87/dup-protocol-experimental` | labs; not pin soak |
| Market Radar | `Gruver87/dup-market-radar` | go_ready / soak packs / live-money |
| Agent skills | `Gruver87/dup-agent-skills` | validate_skills / CI |

## Rules

1. Radar pytest ≠ L1 integration gate.
2. L1 `FEATURE_LONG_RANGE` stays off in prod JSON until ADR 0017.
3. Brand URLs only the two protocol repos + radar/skills as listed — never obsolete Absolute_* GitHub names as current links.

## Refuse

- Copying L1 soak claims into radar README.
- Flipping experimental libp2p into the audit pin.
