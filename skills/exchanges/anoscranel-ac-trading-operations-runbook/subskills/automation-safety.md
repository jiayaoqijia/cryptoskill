---
name: automation-safety
domain: crypto-trading/automation-safety
trigger: "Putting guardrails around automated trading before it runs live."
anti_trigger: "Not for designing the strategy the automation implements."
scope: "Guardrails for automated trading: size caps, rate limits, dead-man switches, staged rollout, rollback."
status: seedling
---

# Automation safety

## Standard

Automation multiplies whatever the desk already is: a good process scales, and a bug scales faster. The guardrails below assume the automation will eventually do something nobody intended, and constrain the damage rather than the probability. They are the same whether the automation is a full strategy engine or a small script that rebalances once a day.

The core idea is the dead-man switch: the system must stop when it stops hearing from its operator, not keep running on stale intent. A second idea is the size cap that the automation cannot raise itself. A third is staged rollout: the same code runs on a paper book, then at a fraction of size, before full size, with each stage having an exit criterion.

Primary sources: <https://sre.google/sre-book/table-of-contents/> and <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>.

## Decision rules

- Every automated order passes through a hard size cap enforced outside the strategy logic.
- The system halts if it cannot reach the operator or the venue for longer than a stated timeout.
- Rate limits are respected in code, with backoff on rejection, never by retrying blindly.
- Rollout is staged: paper, then a fraction, then full; each stage has a stated exit criterion and a rollback command tested beforehand.
- The automation's error path is exercised deliberately before go-live.
- Any change to the automation re-enters the staged rollout; no exceptions for "small" changes.

## Procedure

1. Define the size cap, the timeout, and the rollback command before writing strategy logic.
2. Build the dead-man switch first: no heartbeat, no orders.
3. Run on a paper book until the exit criterion is met.
4. Run at a fraction of target size with monitoring on fills, errors, and latency.
5. Promote to full size only after the fraction stage's criterion is met and recorded.
6. Record the rollout stages, dates, and observed behaviour.

## Anti-patterns

- A size cap implemented inside the strategy, which the strategy can bypass.
- Running unattended without a heartbeat.
- Retrying rejected orders without backoff.
- Skipping the paper stage because the logic "is simple".
- Treating a small code change as exempt from staged rollout.

## Done checklist

- [ ] Size cap enforced outside strategy logic.
- [ ] Dead-man switch implemented and tested.
- [ ] Rate limits and backoff implemented.
- [ ] Rollback command tested.
- [ ] Staged rollout completed with criteria recorded.
- [ ] Change policy applied to subsequent edits.

## Sources

- Reliability practice for automation and rollouts: <https://sre.google/sre-book/table-of-contents/>
- Exchange API documentation for rate limits and order management: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>
- Venue operational documentation: <https://www.bybit.com/en/help-center>
