---
name: stuck-and-partial-orders
domain: crypto-trading/stuck-and-partial-orders
trigger: "Handling orders that will not fill, will not cancel, or filled only partly."
anti_trigger: "Not for choosing order types in normal conditions."
scope: "Orders that will not fill or cancel, reduce-only traps, cancel-on-disconnect, and the escalation path."
status: seedling
---

# Stuck and partial orders

## Standard

An order that will not behave is a small incident with a large blast radius: a stuck reduce-only order can block an exit, a phantom partial can double a position, and a cancel-on-disconnect flag can leave the desk flat on one venue while believing it is hedged on another.

The runbook treats stuck orders as state to be reconciled rather than a UI problem to be clicked through. Each case has a decision sequence: verify the true order state at the venue, determine what the order is protecting or blocking, act with the minimum intervention that restores the intended state, and record it.

Primary sources: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info> and <https://www.bybit.com/en/help-center>.

## Decision rules

- Fetch the order state from the venue's API, not the interface; the interface lags.
- A reduce-only order that will not cancel is treated as a potential exit blocker and escalated immediately.
- A partial fill is reconciled against trade history before any new order is sent for the remainder.
- Cancel-on-disconnect is either on for every order in a strategy or off for every order; mixed states are how phantom positions appear.
- Never place a second order to "cover" a stuck one until the first is confirmed dead.
- Escalate to the venue's support with the order identifier, timestamp, and observed state, and keep the ticket reference.

## Procedure

1. Pull the order's true state and its fill history from the API.
2. Classify: open and working, partially filled, cancelled, rejected, or unknown.
3. Determine what the order is blocking or protecting.
4. Act with the minimum intervention: cancel and re-place, or let it work, with the reason recorded.
5. If the venue will not cancel, document the identifier and escalate; consider whether the position can be managed around it.
6. Record the resolution and the elapsed time.

## Anti-patterns

- Clicking cancel repeatedly and assuming it worked.
- Placing an offsetting order before confirming the original state.
- Mixing cancel-on-disconnect settings within one strategy.
- Treating a partial fill as a full fill when computing exposure.
- Escalating without the order identifier and timestamps.

## Done checklist

- [ ] Order state and fill history pulled from the API.
- [ ] Classification recorded.
- [ ] Blocking or protecting role identified.
- [ ] Minimum intervention applied and recorded.
- [ ] Venue escalation reference kept where needed.
- [ ] Resolution and elapsed time recorded.

## Sources

- Exchange API documentation for order state and cancellation: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>
- Venue support and operational documentation: <https://www.bybit.com/en/help-center>
- Reliability practice for handling degraded dependencies: <https://sre.google/sre-book/table-of-contents/>
