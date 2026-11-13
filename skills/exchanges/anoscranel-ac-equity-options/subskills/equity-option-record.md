---
name: equity-option-record
domain: investing/equity-option-record
trigger: "Writing the record of an equity or index option position."
anti_trigger: "Not for recommending a position, and not for the broker statement."
scope: "The written record: contract family, settlement, dividends, borrow, and assignment plan."
status: seedling
---

# Equity option record

## Standard

The equity option record states which contract family the position belongs to, how it settles, whether dividends or borrow could change it, and what happens on assignment. Those four facts distinguish an equity option record from a generic options record, and each of them can change the payoff without any move in the underlying.

The assignment plan is the field most often missing. A short option is a commitment to deliver or receive something, and what that something is depends on the contract's settlement rules and on the corporate actions in its life. Writing the plan at entry means the assignment, when it arrives, is an event that was expected rather than a surprise discovered on a statement.

Primary sources: <https://www.cboe.com/> and <https://osf.io/prereg/>.

## Decision rules

- Record the contract, its family, exercise style, and settlement method.
- Record the expiry, the settlement source, and the last trading day.
- Record dividends inside the life and the assignment exposure they create.
- Record borrow terms where the position is short stock or synthetic short.
- Record the assignment plan with the resulting position and its funding.
- Record any corporate action adjustment affecting the contract.

## Procedure

1. Record the contract terms and family.
2. Record settlement conventions and dates.
3. Record dividends and borrow.
4. Record the assignment plan.
5. Record any adjustment.
6. Review before each expiry and each ex-dividend date.

## Anti-patterns

- Recording an index and a single-name position with the same fields.
- Omitting settlement type.
- Leaving dividends out of a short call's record.
- Writing no assignment plan.
- Ignoring an adjustment notice.

## Done checklist

- [ ] Contract and family recorded.
- [ ] Settlement conventions recorded.
- [ ] Dividends and borrow recorded.
- [ ] Assignment plan written.
- [ ] Adjustments recorded.
- [ ] Reviews scheduled.

The record should also state the position's maximum obligation rather than only its maximum gain: a short call's loss is unbounded in principle and bounded in practice only by the share count the writer could be assigned, and writing both numbers makes the asymmetry impossible to forget at review.


Keeping the record beside the underlying position's record is what makes the pairing legible: a covered call, a protective put, and a collar are one exposure described in two instruments, and a reviewer reading only the option side cannot see the risk that the stock leg removes.

## Sources

- Exchange option specifications: <https://www.cboe.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Regulatory context: <https://www.sec.gov/investor>
