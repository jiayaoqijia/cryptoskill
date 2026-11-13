---
name: ac-fund-reporting-and-metrics
description: "Reading private-fund performance the way the numbers actually behave: IRR and its reinvestment and timing assumptions, TVPI DPI and RVPI and what each measures, the J-curve and early-period distortion, since-inception and vintage benchmarking, dry powder and unfunded commitments, peer universe selection, and the written reporting record. It explains the arithmetic of private-fund metrics; it never recommends a fund and never predicts a return. Use when asking \"TVPI\", \"DPI\", \"net IRR\", \"J-curve\", \"vintage year\", \"dry powder\", \"unfunded commitment\", \"how is my fund doing\", \"peer universe\", \"since inception return\". Not for measuring a marketable portfolio (ac-performance-measurement), not for the manager's operations and terms (ac-manager-and-vehicle-diligence), not for fund-level financing (ac-portfolio-financing)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Fund reporting and metrics

## Overview

Private-fund performance is reported in a vocabulary built for a different purpose than public-market returns. IRR answers "what rate of return did the cash flows produce", TVPI answers "how much value is there relative to what was put in", DPI answers "how much cash has actually come back", and none of them answers "is this a good result" without a comparison that respects vintage, strategy, and the fund's position in its life.

This skill covers that arithmetic and its distortions: why an early IRR is meaningless, why a multiple without a duration is half a fact, why unfunded commitments belong in the denominator, and why a peer universe chosen by the manager is not a benchmark. It reads the numbers; it does not judge whether a fund will perform.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## When to use

- When reading a quarterly report, an annual report, or a pitch deck from a private fund.
- When comparing two funds or two vintages on reported performance.
- When unfunded commitments or dry powder affect the allocation picture.
- When a peer universe or a since-inception figure is being presented as evidence.

## When NOT to use

- For time-weighted returns and attribution on a marketable portfolio (use ac-performance-measurement).
- For the manager's operations, terms, and side letters (use ac-manager-and-vehicle-diligence).
- For subscription lines and continuation vehicles (use ac-portfolio-financing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/irr-and-its-assumptions.md` | `investing/irr-and-its-assumptions` | IRR, reinvestment, timing, and why it flatters early-stage funds. |
| `subskills/tvpi-dpi-and-rvpi.md` | `investing/tvpi-dpi-and-rvpi` | The multiples, what each measures, and the duration they omit. |
| `subskills/j-curve-and-early-period.md` | `investing/j-curve-and-early-period` | Why the first years look bad, and when the shape is a genuine warning. |
| `subskills/vintage-and-peer-benchmarks.md` | `investing/vintage-and-peer-benchmarks` | Vintage year, peer universe selection, and the comparison that is fair. |
| `subskills/dry-powder-and-commitments.md` | `investing/dry-powder-and-commitments` | Unfunded commitments, overcommitment, and the denominator problem. |
| `subskills/fund-reporting-record.md` | `investing/fund-reporting-record` | The written record: metrics, dates, definitions, and the comparison used. |

## Status and honest limits

Private-fund valuations are estimates produced by the manager, audited annually at best, and marked by judgement in between. Every metric in this skill is computed from those estimates, so its precision is illusory: two funds with the same reported IRR can have materially different realised outcomes. Nothing here recommends a fund, and a metric quoted without its date, its definition, and its comparison is not evidence of anything.
