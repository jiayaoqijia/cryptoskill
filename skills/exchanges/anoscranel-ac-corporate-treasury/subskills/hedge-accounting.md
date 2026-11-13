---
name: hedge-accounting
domain: investing/hedge-accounting
trigger: "Understanding why accounting treatment constrains a hedging programme."
anti_trigger: "Not for computing a tax position, and not for accounting advice."
scope: "Designation, effectiveness testing, and why accounting constrains the hedge."
status: seedling
---

# Hedge accounting

## Standard

Hedge accounting is an election that changes when a hedge's gains and losses appear in the income statement. Without it, a derivative is marked to market through earnings while the hedged item is accounted for on a different basis, which produces reported volatility that the economic hedge was meant to remove. With it, the two are matched, and the reported result reflects the hedged position rather than the instrument.

The election is not free. It requires documentation at inception, a designated hedge relationship, and a test of effectiveness that must be performed and passed. Those requirements constrain what a treasury can do: a hedge that fails the test, or a hedge of a risk that cannot be reliably measured, loses the accounting match, and a programme designed without regard to those rules can produce exactly the volatility it was meant to avoid.

Primary sources: <https://www.fasb.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record which hedges are designated for hedge accounting and which are not.
- Record the hedged item and the risk being hedged.
- Record the effectiveness method and its results, where disclosed.
- Record where the gains and losses appear: income statement, other comprehensive income, or both.
- Record any reclassification from other comprehensive income into earnings.
- Record hedges that failed designation, since their volatility is reported directly.

## Procedure

1. Read the derivative note for designated and undesignated hedges.
2. Record the hedged item and risk for each relationship.
3. Record the effectiveness method and result.
4. Record where gains and losses are recognised.
5. Record any amounts reclassified into earnings.
6. Write the summary with the reported versus economic effect distinguished.

## Anti-patterns

- Assuming all hedges receive hedge accounting.
- Treating other comprehensive income as if it were outside the economics.
- Ignoring the effectiveness test, which can fail and remove the match.
- Overlooking reclassification, which brings prior gains into current earnings.
- Reading the derivative's fair value change as the programme's result.

## Done checklist

- [ ] Designated and undesignated hedges recorded.
- [ ] Hedged item and risk recorded.
- [ ] Effectiveness method and result recorded.
- [ ] Recognition locations recorded.
- [ ] Reclassification recorded.
- [ ] Reported versus economic effect distinguished.

The practical consequence for a reader is that reported earnings can move for reasons the business did not experience: a hedge that no longer qualifies for the election brings its mark-to-market into the income statement, and a period of reported volatility may reflect a documentation failure rather than a change in the underlying exposure.


## Sources

- Derivative and hedging disclosure: <https://www.sec.gov/investor>
- Hedge accounting standards: <https://www.fasb.org/>
- Investor education on reported results: <https://www.investor.gov/introduction-investing>
