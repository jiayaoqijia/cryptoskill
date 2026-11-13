---
name: cap-table-mechanics
domain: investing/cap-table-mechanics
trigger: "Building and maintaining the cap table across priced rounds."
anti_trigger: "Not for valuing the business, and not for legal advice."
scope: "The cap table as the single source of ownership truth across rounds."
status: seedling
---

# Cap table mechanics

## Standard

The cap table lists every security that can become common stock: each share class with its rights, outstanding options by grant, the unvested portion, the pool reserved for future grants, and every convertible instrument with its conversion terms. It is the single source of ownership truth, and every later calculation — a round's dilution, an exit's waterfall — derives from it. A stale or simplified cap table produces confident wrong answers.

The mechanics that trip the unwary are share classes and convertibles. Preferred stock converts by its own formula, which may have changed across rounds; a SAFE or a convertible note converts by a formula that depends on the *next* priced round's valuation and any discount or cap it carries, so the dilution from those instruments lands in the round in which they convert. Fully diluted ownership includes all of it. A founder who computes their percentage from outstanding common stock is partway done and often the optimistic part of the way.

Primary sources: <https://www.law.cornell.edu/> and <https://www.fasb.org/>.

## Decision rules

- List every class and series of stock held, with shares outstanding and per-round rights (voting, board, preemptive).
- List all convertible instruments — SAFEs, notes — with conversion triggers and formulas, not just amounts.
- List all outstanding options with their exercise prices, vesting state, and expiry.
- Record the unallocated option pool separately from granted options; total authorised minus granted equals available.
- Compute fully diluted share count and each holder's fully diluted ownership as a standing line, updated each round.
- Preserve the audit trail: every change to the cap table is an event (issuance, conversion, exercise, cancellation) with a date and a document behind it.

## Procedure

1. Gather every stock incentive plan, option grant, and security from formation onward.
2. Rebuild the table from its events; never start from the most recent spreadsheet alone.
3. Compute fully diluted shares and per-holder ownership.
4. Verify the preferred conversion ratios against each series' current terms, allowing for changes across rounds.
5. Project the table for the next round: the round's new shares at an assumed price per share, the conversion of all convertibles at the conversion terms, and the pool if it is refreshed in the round.
6. Publish the updated table as the single source for ownership questions, dated.

## Anti-patterns

- Treating the fully diluted number as static across a round: instruments convert into the round.
- Excluding unvested options from the option pool: fully diluted counts total outstanding grants, vested or not.
- Deferring a pool-refresh decision and realising later that the round implicitly priced it in.
- Reading a SAFE as fixed ownership; SAFEs convert at the *next* round's terms, not at issuance.
- Confusing authorised with outstanding share counts.

## Done checklist

- [ ] Every event reconstructed from documents, not from the last spreadsheet.
- [ ] All holders, classes, and Convertibles listed with terms.
- [ ] Fully diluted ownership computed as a standing line.
- [ ] Option pool granted-vs-remaining separated.
- [ ] Preferred conversion ratios verified against current terms.
- [ ] Table projected through the next round's conversion events.

## Sources

- Statutory reference for corporate records: <https://www.law.cornell.edu/>
- Stock-based compensation accounting: <https://www.fasb.org/>
- Investor education on private company records: <https://www.investor.gov/introduction-investing>
