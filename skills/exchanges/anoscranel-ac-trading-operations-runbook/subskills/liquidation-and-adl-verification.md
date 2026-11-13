---
name: liquidation-and-adl-verification
domain: crypto-trading/liquidation-and-adl-verification
trigger: "Verifying what actually happened after a liquidation or auto-deleveraging event."
anti_trigger: "Not for appealing a liquidation, and not for sizing before the fact."
scope: "What to verify after a liquidation or ADL event, what the record must show, and the restart rules."
status: seedling
---

# Liquidation and ADL verification

## Standard

A liquidation is a mechanical event with a paper trail, and the paper trail is usually not what the desk expects. The fill price, the fees, the insurance-fund contribution, and the residual balance can each differ from the naive calculation. Verification establishes what happened before any restart, because restarting on a wrong understanding of the previous loss compounds it.

Auto-deleveraging is the harder case: the venue closes positions against a counterparty rather than through the book, and the desk may learn of it only from a balance change. Verification means reconstructing the event from venue records, not from memory or from the notification.

Primary sources: <https://www.bybit.com/en/help-center> and <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>.

## Decision rules

- Reconstruct the event from venue records: fills, fees, funding, and the final balance.
- Reconcile the loss against the pre-event record within a stated tolerance; anything beyond it is unresolved and blocks restart.
- Record whether the event was a book liquidation, an ADL, or a manual close executed by the venue; they have different causes and different lessons.
- The restart requires a written cause and a written change; "the market moved" is not a cause.
- Never re-enter the same position immediately to "make it back"; that is a separate decision requiring its own memo.
- If the venue's records are incomplete, state that and treat the reconstruction as provisional.

## Procedure

1. Pull the liquidation or ADL record and the surrounding trade history.
2. Rebuild the position history from entry to event, including funding payments.
3. Compute the expected loss from the record and compare with the actual change in balance.
4. Identify the mechanism: liquidation engine, ADL, or manual venue action.
5. Write the cause and the change required before restart.
6. Record the restart decision, or the decision not to restart.

## Anti-patterns

- Accepting the venue's summary without reconciling the arithmetic.
- Treating an ADL as a normal stop-out.
- Restarting the same size and same setup to recover the loss.
- Omitting funding payments from the loss reconstruction.
- Recording a cause as "volatility" with no mechanism behind it.

## Done checklist

- [ ] Event record and surrounding trade history pulled.
- [ ] Position history rebuilt with funding included.
- [ ] Expected loss computed and compared with the balance change.
- [ ] Mechanism identified.
- [ ] Cause and required change written.
- [ ] Restart decision recorded.

## Sources

- Venue documentation on liquidation and auto-deleveraging: <https://www.bybit.com/en/help-center>
- Exchange API documentation for trade and funding history: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>
- Empirical measurement of cascade mechanics: <https://arxiv.org/abs/2608.03616>
