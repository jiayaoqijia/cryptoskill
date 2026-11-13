---
name: leverage-sizing
domain: investing/leverage-sizing
trigger: "Choosing a leverage ratio that survives a plausible fall."
anti_trigger: "Not for recommending borrowing, and not for predicting markets."
scope: "Choosing a ratio that survives a plausible fall, with pre-committed rules for reducing it."
status: seedling
---

# Leverage sizing

## Standard

Sizing leverage is a survival question rather than a return question. The workable approach is to choose the fall the position must survive — drawn from the strategy's own worst evidence, not from a comfortable scenario — and then choose the ratio at which that fall leaves the collateral intact with a margin above the requirement. That is a constraint, not an optimisation, and it usually produces a smaller ratio than the investor expected.

The second half is the rule for reducing leverage before the boundary is reached. A pre-committed de-risking rule turns a decision made under stress into a decision made in advance, and it is the difference between a position that is managed and one that is discovered. The rule needs a trigger, an action, and a deadline, written before the borrowing begins.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://osf.io/prereg/>.

## Decision rules

- Set the survival scenario first: a stated fall in percent, from the strategy's evidence.
- Compute the maximum ratio at which that fall leaves a buffer above the requirement.
- Record the buffer explicitly, and keep it large enough for a requirement increase.
- Write the de-risking trigger, the action, and the deadline before borrowing.
- Record the conditions under which leverage is reduced to zero.
- Where the survival scenario is judgement rather than evidence, label it.

## Procedure

1. State the survival scenario with its source.
2. Compute the ratio that survives it with a stated buffer.
3. Compare with the ratio the investor intended, and record the gap.
4. Write the de-risking rule with trigger, action, and deadline.
5. Write the exit condition that removes leverage entirely.
6. Record the sizing and the rules together.

## Anti-patterns

- Choosing a ratio from the maximum the broker permits.
- Setting a survival scenario below the worst evidence.
- Leaving the buffer equal to the requirement rather than above it.
- Writing a de-risking rule that requires a discretionary decision.
- Reviewing the ratio only when a call arrives.

## Done checklist

- [ ] Survival scenario stated with source.
- [ ] Ratio computed against it with buffer.
- [ ] Gap between intended and survivable ratio recorded.
- [ ] De-risking rule written with trigger and deadline.
- [ ] Exit condition written.
- [ ] Sizing and rules filed together.

## Sources

- Investor education on margin and risk: <https://www.investor.gov/introduction-investing>
- Pre-registration practice for stated rules: <https://osf.io/prereg/>
- Margin requirement guidance: <https://www.finra.org/>
