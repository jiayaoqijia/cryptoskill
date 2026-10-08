---
name: cap-balances-in-a-hot-wallet
description: Use when an operational key signs autonomously and sits online. Sets a float ceiling, keeps the rest cold, and funds the hot wallet on a schedule instead of letting it accumulate.
---

# Cap the balance a hot wallet may hold

An online signing key must be assumed leakable, so the point of a hot wallet is to hold only what the next few hours of operations need. This skill fixes a hard ceiling per hot wallet and sweeps surplus to cold storage on a schedule.

## Procedure

1. Measure real outflow. Pull the last 30 days of outbound value from the hot address and take the 99th-percentile daily figure:
   `cast logs --address $TOKEN --from-block $START --to-block $LATEST --json | jq -r '.[].data'`
   or query an indexer for daily outbound totals.
2. Set the ceiling to that 99th-percentile amount rounded up — commonly 2–5% of the treasury per hot wallet. The ceiling is never "everything".
3. Sweep surplus to cold whenever the balance exceeds the ceiling, with an idempotent sweeper on a cron:
   `cast send $TOKEN "transfer(address,uint256)" $COLD $SURPLUS --account sweeper --rpc-url $RPC`
4. Fund the hot wallet on a schedule from cold rather than letting deposits rest there. Inbound customer funds route to a cold receiving address, not the operational key.
5. Alert when the balance is within 20% of the ceiling so a human reviews before the sweeper fires.
6. Re-derive the ceiling quarterly and after any volume change; a stale ceiling either starves operations or over-exposes funds.

## Pitfalls

- A sweeper holding an unlimited allowance from the cold wallet makes the sweeper key the new best target; cap its allowance to a single sweep amount.
- On high-fee chains the sweeper needs native balance for gas; a drained gas balance strands the tokens it was sent to move.
- Round-number ceilings ("keep 10 ETH") rot fast; derive from measured volume.
- If surplus moves only when a human clicks, the ceiling is aspirational, not enforced.
- A hot wallet that also holds the deployer key conflates roles; the sweeper should not be able to upgrade contracts.
- A hot wallet refilled by an automated payout job keeps restoring itself after a sweep; cap the job's per-run amount or the ceiling is fiction.
- A multisig hot wallet is still hot: the convenience of an API signer does not change the online-exposure assumption.
- Track the ceiling in the same units you measure volume; mixing a token float with a native gas float hides the real exposure.
- If the sweeper and the signer share one key, an attacker who takes that key both sweeps and drains with it.

## Verification

    cast balance $HOT --rpc-url $RPC && echo "ceiling=$CEILING"
    # expect balance <= ceiling; a value above it means a sweep is overdue

Report the measured ceiling, the current balance, and the sweeper's last run, with the commands behind them.
