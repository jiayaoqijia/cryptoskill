---
name: behavioral-rails
domain: crypto-trading/behavioral-rails
trigger: "Documenting failure modes and mechanical rails against revenge trading, size escalation, thesis drift, and action bias"
anti_trigger: "Relying on willpower to resist emotional trading impulses; overriding automated guardrails during high volatility"
scope: "Documented failure modes and mechanical rails: revenge trading, size escalation, thesis drift, sunk-cost holding, action bias"
status: seedling
---

# Behavioral Rails

## Standard

- **Kahneman & Tversky, "Prospect Theory" (1979)**: decision-makers exhibit asymmetric risk aversion, taking excessive risks to recover losses. <https://www.jstor.org/stable/1914185>
- **Odean, "Are Investors Reluctant to Realize Their Losses?" (1998)**: investors hold losing assets too long while prematurely selling winners. <https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00072>
- **Barber & Odean, "Trading Is Hazardous to Your Wealth" (2000)**: excessive trading frequency driven by overconfidence depresses net returns. <https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00226>
- **Thaler, "Mental Accounting Matters" (1999)**: house-money effect causes traders to escalate risk after wins. <https://www.jstor.org/stable/117326>
- ⚠️ Practitioner heuristic: mechanical rails must remove human discretion during emotional stress states.

## Decision rules

1. Pre-committed mechanical rails must exist for revenge trading, size escalation, thesis drift, and action bias.
2. A mandatory cooling-off lockout timer is enforced after consecutive losses, blocking new trade memos.
3. Size escalation after wins is prohibited; position size is hard-capped by the risk budget.
4. Thesis drift is prevented by locking pre-trade memo text upon submission.
5. Action bias in flat markets is neutralized by requiring minimum waiting periods between entries.
6. Overriding behavioral rails requires multi-factor administrative friction.
7. ⚠️ House: attempting to subvert a behavioral rail results in immediate 24-hour operational shutdown.

## Procedure

1. Identify current psychological state before opening any pre-trade memo.
2. Check lockout status: verify that no consecutive-loss timer is active.
3. Enforce position size limits: confirm winning streaks have not triggered unauthorized scaling.
4. Review thesis boundaries: verify execution matches the original locked memo.
5. Apply activity filters: ensure sufficient time has elapsed since last trade closure.
6. Log emotional friction or temptation in the journal.
7. Execute trades strictly within active mechanical rail boundaries.

## Anti-patterns

- **Revenge trading.** Immediately entering trades after losses. Fix: enforce automatic lockout timers.
- **House-money escalation.** Increasing risk size after wins. Fix: treat all capital uniformly under risk budgets.
- **Thesis drift.** Changing reasons for holding positions as conditions break. Fix: close trades immediately when thesis breaks.
- **Over-trading out of boredom.** Opening positions in directionless markets. Fix: embrace flat periods as required states.

## Done checklist

- [ ] Mechanical rails are in place for revenge trading and size escalation.
- [ ] Cooling-off lockout timers are functional after losses.
- [ ] Pre-trade memos are locked against mid-trade editing.
- [ ] Inactivity filters prevent action bias during flat phases.
- [ ] No behavioral rail overrides were executed during sessions.

## Sources

- Kahneman & Tversky, "Prospect Theory": <https://www.jstor.org/stable/1914185>
- Odean, "Are Investors Reluctant to Realize Their Losses?": <https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00072>
- Barber & Odean, "Trading Is Hazardous to Your Wealth": <https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00226>

⚠️ Gaps: psychological fatigue can impair operator self-awareness during extreme market stress.
