---
name: venue-outage-response
domain: crypto-trading/venue-outage-response
trigger: "Responding to an exchange outage, halt, or withdrawal freeze while holding exposure."
anti_trigger: "Not for choosing where to trade, and not for price speculation about the outage."
scope: "API failures, halts, and withdrawal freezes: the order of decisions, and what not to do into a gapped book."
status: seedling
---

# Venue outage response

## Standard

An outage is a state change, not an event to trade through. When a venue's API fails, halts trading, or freezes withdrawals, the first job is to establish what still works: reads, cancels, closes, withdrawals, transfers. The second is to reduce exposure in the places that still function, in an order that does not make the book worse.

The failure mode that costs the most is acting into a gapped or halted book because action feels better than waiting. A halt means the price you see is not a price you can trade. The correct posture is defensive: assume the displayed book overstates liquidity, assume withdrawals may take longer than stated, and assume the venue may change rules again before it reopens.

Primary sources: <https://www.bybit.com/en/help-center> and <https://sre.google/sre-book/table-of-contents/>.

## Decision rules

- Establish capability first: classify each function (read, cancel, close, withdraw, transfer) as working, degraded, or unavailable.
- Never send a market order into a halted or gapped book; if the book is not functioning, the order is a donation.
- Reduce exposure on venues that still function, before adding hedges on venues that may not.
- Withdrawal freezes are treated as indefinite; plans that assume resumption by a stated time are plans built on a press release.
- Record every action with a timestamp; the timeline is the only defence in the postmortem.
- If the venue's rules change mid-incident, re-read them before acting; earlier permissions may no longer apply.

## Procedure

1. Classify venue capability: read, cancel, close, withdraw, transfer.
2. Freeze new orders on the affected venue.
3. Record the current book: positions, margin, liquidation distances, and what remains reachable.
4. If withdrawal is frozen and exposure is material, decide whether a hedge on a functioning venue is warranted, and record the reasoning.
5. Act only through functions classified as working; verify each action's effect before the next.
6. Monitor the venue's status channel and re-classify periodically.
7. Write the incident timeline as you go, not after.

## Anti-patterns

- Market-closing into a halted book to feel decisive.
- Assuming withdrawals resume on the announced schedule.
- Adding exposure on the affected venue because prices "look wrong".
- Hedging on a venue whose own health is unverified.
- Reconstructing the timeline from memory afterwards.

## Done checklist

- [ ] Capability classified per function.
- [ ] New orders frozen on the affected venue.
- [ ] Book state recorded with liquidation distances.
- [ ] Hedge decision recorded with reasoning, if taken.
- [ ] Each action verified before the next.
- [ ] Timeline written contemporaneously.

## Sources

- Venue operational and status documentation: <https://www.bybit.com/en/help-center>
- Incident-response practice: <https://sre.google/sre-book/table-of-contents/>
- Exchange API documentation for order and withdrawal operations: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>
