---
name: order-and-position-reconciliation
domain: crypto-trading/order-and-position-reconciliation
trigger: "Comparing the desk's record of orders and positions against venue state."
anti_trigger: "Not for deciding what to trade, and not for accounting or tax records."
scope: "Matching the desk's records against venue state, and the daily reconciliation that catches drift early."
status: seedling
---

# Order and position reconciliation

## Standard

The desk's record and the venue's state drift apart for ordinary reasons: a fill that arrived twice in a webhook, a cancel that never landed, a partial fill the journal missed. Small drifts are normal; unnoticed drifts become position errors, and a position error at the wrong moment is how a book takes a loss it never chose.

Reconciliation is the routine that closes the gap. It compares what the desk believes with what the venue reports, order by order and position by position, and it runs on a schedule rather than when something feels wrong. The rule is that the venue is the source of truth for state, while the desk record is the source of truth for intent; the reconciliation explains the difference.

Primary sources: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info> and <https://sre.google/sre-book/table-of-contents/>.

## Decision rules

- Venue state wins on positions and balances; the desk record wins on intent and rationale.
- Any position the desk did not intend is an incident, not a rounding error, and is closed or hedged before new risk is added.
- Duplicate fills are reconciled against the venue's trade history, not the notification stream.
- Reconciliation is daily at minimum, and immediately after any order anomaly.
- A delta that persists across two reconciliations escalates to a written incident.
- Never "fix" a position by opening an offsetting trade without first recording the original discrepancy.

## Procedure

1. Pull open orders and positions from the venue, with timestamps.
2. Pull the desk's open orders and positions from its journal.
3. Match by instrument and order identifier; list unmatched items on both sides.
4. For unmatched venue orders, determine origin: manual, automated, or unknown.
5. For unmatched desk records, determine whether a fill was missed or a cancel failed.
6. Resolve each difference: amend the journal, or act on the venue state, with the reason recorded.
7. Record the reconciliation result and the deltas that remain.

## Anti-patterns

- Reconciling only when something looks wrong.
- Trusting the notification stream as the record of fills.
- Offsetting an unexplained position instead of investigating it.
- Adjusting the journal to match the venue without recording why.
- Leaving a persistent delta open because it is small.

## Done checklist

- [ ] Venue orders and positions pulled with timestamps.
- [ ] Desk journal compared item by item.
- [ ] Unmatched items listed with their origin or marked unknown.
- [ ] Each difference resolved with a recorded reason.
- [ ] Persistent deltas escalated to incident.
- [ ] Reconciliation result recorded.

## Sources

- Exchange API documentation for orders and positions: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>
- Reliability practice for state reconciliation: <https://sre.google/sre-book/table-of-contents/>
- Venue operational documentation: <https://www.bybit.com/en/help-center>
