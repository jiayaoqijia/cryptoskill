---
name: dividends-and-early-exercise
domain: investing/dividends-and-early-exercise
trigger: "Handling dividend risk and early exercise on equity options."
anti_trigger: "Not for predicting the dividend, and not for option theory."
scope: "Dividend-driven exercise of calls, and assignment timing."
status: seedling
---

# Dividends and early exercise

## Standard

A deep in-the-money American call is exercised for one reason: to capture the dividend. The holder compares the remaining time value, which is forfeited on exercise, with the dividend that will be paid only to shareholders of record. When the dividend exceeds the time value, early exercise is rational, and the short side of that call receives an assignment it may not have expected.

The timing is what matters. Assignment arrives before the ex-dividend date, the notice is delivered after the close, and the resulting short stock position must be covered or borrowed. A trader who is short calls into an ex-dividend date without checking the open interest and the dividend size is exposed to an assignment that appears on the statement rather than in the plan.

Primary sources: <https://www.cboe.com/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the ex-dividend date and the dividend amount for names where the position is American.
- Record the option's time value against the dividend, per contract.
- Record the open interest at the strike, which indicates the assignment likelihood.
- Record the plan for assignment: cover, borrow, or hold the resulting position.
- Record the borrow cost if a short stock position results.
- Record the position's exposure for each name with an ex-dividend date inside its life.

## Procedure

1. List the ex-dividend dates inside each American option's life.
2. Compute time value against the dividend for in-the-money calls.
3. Record open interest at the relevant strikes.
4. Write the assignment plan per position.
5. Record borrow availability and cost.
6. Review the positions before each ex-dividend date.

## Anti-patterns

- Ignoring a dividend inside a short call's life.
- Assuming assignment occurs on the ex-dividend date rather than before it.
- Forgetting the borrow cost of a resulting short position.
- Checking time value against the gross dividend without the tax treatment.
- Treating a European index option as if it carried dividend exercise risk.

## Done checklist

- [ ] Ex-dividend dates listed.
- [ ] Time value versus dividend computed.
- [ ] Open interest recorded.
- [ ] Assignment plan written.
- [ ] Borrow recorded.
- [ ] Pre-ex-date review scheduled.

The dividend calendar should be read alongside the option's own expiry: a call expiring just after an ex-dividend date carries the exercise risk for its whole life, while one expiring just before carries none, so the same strike and the same name can have entirely different assignment profiles depending on the expiry chosen.


## Sources

- Exchange exercise and dividend guidance: <https://www.cboe.com/>
- Corporate action and dividend disclosure: <https://www.sec.gov/investor>
- Investor education on assignment: <https://www.investor.gov/introduction-investing>
