---
name: fx-exercise-and-delivery
domain: investing/fx-exercise-and-delivery
trigger: "Working out whether an FX option delivers currency or settles in cash."
anti_trigger: "Not for option pricing, and not for spot trading mechanics."
scope: "European and American exercise, delivery versus cash settlement, and NDF options."
status: seedling
---

# FX exercise and delivery

## Standard

Most FX options are European: they are exercised, or not, at a single cut, and settlement follows two business days later as a spot transaction. A few are American, exercisable at any time before expiry, and those carry an early-exercise premium that is usually small but not always negligible in high-carry pairs.

Settlement matters more than it appears. Deliverable options create an actual currency exchange on the settlement date, which is a funding event as well as a market event. Cash-settled options pay the difference against a fixing, and options on non-deliverable forwards are cash-settled by construction because the currency cannot be delivered freely. A position that expects a cash payment but is documented as deliverable faces a very different settlement.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the exercise style and the cut time.
- Record whether settlement is deliverable or cash, and the fixing source if cash.
- Record the settlement date convention and any holiday calendar.
- Record the notional in both currencies for a deliverable option.
- Record the early-exercise terms and any notice requirement for American options.
- For NDF options, record the fixing and the settlement currency.

## Procedure

1. Record the exercise style and cut.
2. Record the settlement method and the fixing source.
3. Record the settlement date and its calendar.
4. Record the notional in both currencies.
5. Record the notice requirement for early exercise.
6. Write the settlement summary with the confirmation reference.

## Anti-patterns

- Assuming all FX options cash-settle.
- Ignoring the settlement date's effect on funding.
- Treating an American option as European when the carry is large.
- Forgetting that a deliverable option requires the currency to be received.
- Missing a holiday that shifts the settlement date.

## Done checklist

- [ ] Exercise style and cut recorded.
- [ ] Settlement method and fixing recorded.
- [ ] Settlement date and calendar recorded.
- [ ] Both notionals recorded.
- [ ] Early-exercise notice recorded.
- [ ] Summary references the confirmation.

The cut also interacts with the settlement calendar: an option expiring on a day when one of the currencies has a holiday may settle on a different date than the standard two business days, and the funding for a deliverable position has to be arranged against the actual date rather than the nominal one.


## Sources

- Foreign exchange settlement conventions: <https://www.bis.org/>
- Market rates and settlement context: <https://www.federalreserve.gov/>
- Investor education on currency products: <https://www.investor.gov/introduction-investing>
