---
name: sovereign-record
domain: investing/sovereign-record
trigger: "Writing the record of a sovereign debt assessment."
anti_trigger: "Not for recommending a bond, and not for predicting a default."
scope: "The written record: instruments, clauses, recovery scenarios, and triggers."
status: seedling
---

# Sovereign record

## Standard

The sovereign record states the instruments and their governing law, the collective action positions, the recovery scenarios with their discount rates, and the process triggers that would change the analysis. It is written before the position, and its function is to separate the contractual facts from the political judgment, which in this asset class are usually mixed together.

The legal split is the field that carries the most information per line. A claim's position in a restructuring depends first on whether it is local-law or foreign-law, then on whether a collective action clause binds it, and only then on the recovery arithmetic. Recording those three in order means a later reviewer can see which constraint binds rather than having to reconstruct it.

Primary sources: <https://www.imf.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists each instrument with its governing law and clause position.
- The debt stock is split between local-law, foreign-law, and official holdings.
- Recovery scenarios are recorded with their discount rates and new-instrument terms.
- The exit yield is recorded where instruments have already been exchanged.
- Process triggers are dated: programme review, offer launch, participation threshold, court action.
- The record is append-only, amended by dated entries as the negotiation advances.

## Procedure

1. List instruments with law and clause position.
2. Split the debt stock by pool.
3. Record recovery scenarios and discount rates.
4. Record any exit yield.
5. Set process triggers with dates.
6. Amend at each trigger and record what changed.

## Anti-patterns

- Recording the total debt without the legal split.
- Stating a recovery without the discount rate that produced it.
- Omitting the clause position, which decides whether the claim can be bound.
- No triggers, so the record is never revisited.
- Mixing political judgment into the legal and arithmetic fields.

## Done checklist

- [ ] Instruments with law and clause recorded.
- [ ] Debt split by pool recorded.
- [ ] Recovery scenarios with rates recorded.
- [ ] Exit yield recorded.
- [ ] Triggers dated.
- [ ] Amendments dated.

The record should also name the debtor's financing position explicitly, since it decides the timing of any settlement: a sovereign with reserves and no near-term maturities can wait, and one facing a wall cannot, and that difference matters more to the outcome than the legal merits of the claim.


## Sources

- Sovereign debt analysis: <https://www.imf.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market standards: <https://www.bis.org/>
