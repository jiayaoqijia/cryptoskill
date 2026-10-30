# 11 — Reporting

## Purpose

Produce a report that a busy investor can act on and an analyst can audit. Lead with the decision, then the evidence, then the limits.

## Inputs

- IPS-lite and data coverage.
- Portfolio snapshot, performance, risk, liquidity.
- Asset-level, tokenomics, DeFi, on-chain, and scenario findings.
- Source table and limitations.

## Method

1. Lead with the main finding and the decision.
2. Separate verified, reported, estimated, modeled, and unverified.
3. Put the evidence in tables with dates and units.
4. State the limits before the recommendation.
5. Record the decision, falsifiers, and review date.
6. Keep the appendix reproducible.

## Report architecture

1. **Cover:** title, as-of timestamp, base currency, mode, data coverage.
2. **Executive summary:** three to five findings; one verdict; what would change it.
3. **IPS-lite and scope:** mandate, constraints, benchmark.
4. **Portfolio snapshot:** value, top positions, cluster map.
5. **Performance and attribution:** TWR/MWR, benchmark, fees, or `not assessable`.
6. **Risk dashboard:** volatility, drawdown, VaR/CVaR, beta, correlation, liquidity.
7. **Asset-level findings:** material positions only; tokenomics and value capture.
8. **DeFi/on-chain:** health factor, liquidation, oracle, incidents, flows.
9. **Market regime and scenarios:** base, adverse, reverse stress.
10. **Alternatives and rebalancing:** trade-offs, costs, bands.
11. **Decision record:** action, rationale, falsifiers, review date.
12. **Sources and limitations:** source/date table; what could not be verified.

## Language rules

- Lead with the result: “Concentration is the main risk,” not “we analyzed many factors.”
- Use plain Turkish in TR templates; define jargon on first use.
- Separate `VERIFIED`, `REPORTED`, `ESTIMATED`, `MODELED`, `UNVERIFIED`.
- Do not use “safe,” “guaranteed,” “risk-free,” or “best” without a defined comparator.
- Do not present a target price as a forecast.
- Do not hide a missing input in a footnote; put it in the data-coverage line.

## Tables

Every table needs:

- as-of date and currency;
- unit (%, $, TAO, etc.);
- source/evidence class;
- a note if values are estimated or modeled.

## Executive summary pattern

1. **What we found:** one sentence.
2. **Why it matters:** the mechanism.
3. **What is verified:** two or three data points.
4. **What is not:** the main gap.
5. **What to do:** conditional action or “no action.”
6. **What would change the view:** falsifiers.

## Decision record

| Field | Content |
|---|---|
| Decision | Hold / reduce / add / review |
| Scope | Position or cluster |
| Rationale | Risk, value, liquidity, mandate |
| Size | Range only if constraints exist |
| Implementation | Venue, tax, timing; no execution by the skill |
| Falsifiers | Named events/data |
| Review | Date and triggers |

## Monitoring table

| Metric | Current | Threshold | Source | Frequency | Action |
|---|---:|---:|---|---|---|
| Top-1 weight | X% | 30% | Wallet | Weekly | Review |
| Health factor | X | 1.3 | Protocol | Daily | Reduce debt |
| Stablecoin depeg | X% | 2% | Market | Daily | Escalate |

## Failure modes

- A data dump with no verdict.
- A verdict with no source.
- A “score” that hides trade-offs.
- Recommendations without constraints.
- A report that cannot be reproduced from the appendix.

## Sources

- CFA Institute, GIPS performance-presentation principles (2026).
- CFA Institute, *Elements of an Investment Policy Statement for Individual Investors* (2010).
