---
name: preflight-checks
domain: crypto-trading/preflight-checks
trigger: "Running the session ritual before any trading activity."
anti_trigger: "Not for strategy decisions, and not a substitute for risk sizing."
scope: "The session ritual: keys, balances, margin, connectivity, clock sync, and kill switches armed."
status: seedling
---

# Pre-flight checks

## Standard

Every incident report that begins "I did not notice" is a pre-flight failure. The check takes two minutes and covers the things that are cheap to verify and expensive to discover late: whether the key works, whether the balance is what the desk thinks, whether margin is sufficient, whether the connection is stable, whether clocks are synced, and whether the kill switch exists and works.

The ritual is deliberately boring. Its value is that it is the same every time, so a deviation is itself a signal. A desk that skips the check on a calm day has no baseline for the day the venue behaves oddly.

Primary sources: <https://www.bybit.com/en/help-center> and <https://sre.google/sre-book/table-of-contents/>.

## Decision rules

- No trading until every check passes or is explicitly waived with a recorded reason.
- A failed authentication check ends the session before any order is sent.
- Balance mismatch against the desk record of more than a stated tolerance blocks new orders until reconciled.
- If margin utilisation is above the desk's stated cap, no new exposure is added, regardless of the setup.
- The kill switch is tested, not assumed; if it has never been fired, fire it on a paper account.
- Clock drift beyond a few seconds is a real risk on signed requests; verify time sync.

## Procedure

1. Authenticate each configured key and confirm its permissions match the intent (no withdrawal rights on a trading key).
2. Pull balances and open positions; compare with the desk record; note any delta beyond tolerance.
3. Check margin utilisation and available collateral against the cap.
4. Confirm connectivity: a read call, a latency measurement, and the venue's status page.
5. Verify clock sync on the device used for signed requests.
6. Confirm the kill switch exists and is reachable, and that the order-size cap is set.
7. Record the check result with a timestamp.

## Anti-patterns

- Running the check mentally instead of executing it.
- Treating a previous session's pass as today's pass.
- Skipping the check because the market is quiet.
- Holding a key with more permission than the session needs.
- Assuming the kill switch works because it is configured.

## Done checklist

- [ ] Keys authenticated; permissions scoped to the session's needs.
- [ ] Balances and positions compared with the desk record; deltas noted.
- [ ] Margin utilisation checked against cap.
- [ ] Connectivity and venue status confirmed.
- [ ] Clock sync verified.
- [ ] Kill switch reachable; size cap set.
- [ ] Result recorded with timestamp.

## Sources

- Venue operational documentation and status conventions: <https://www.bybit.com/en/help-center>
- Reliability practice for operational checks and incident culture: <https://sre.google/sre-book/table-of-contents/>
- Exchange API documentation for authentication and permissions: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>
