---
name: enforce-velocity-limits-on-withdrawals
description: Use when a wallet or treasury processes withdrawals and you must bound how fast funds can leave. Applies per-transaction, daily, and rolling-window caps with an approval path above the cap.
---

# Enforce velocity limits on outbound funds

A stolen key is only as damaging as how fast it can drain, so limits buy time: they turn a catastrophic loss into an incident with a window to react. This skill sets per-transaction and rolling-window caps with an explicit escalation path above them.

## Procedure

1. Define three numbers: a per-transaction cap, a rolling 24h cap, and a rolling 7d cap. Express each as a percentage of treasury — commonly 0.5% per tx, 2% per day, 5% per week — so they scale as the treasury grows.
2. Enforce at the signing layer, not the UI. A guard on a smart account or a policy in the signing service is what actually blocks an over-limit transfer; a frontend check is bypassed by calling the contract directly.
   - Safe: attach a guard whose `checkTransaction` reverts above the cap.
   - MPC/custody: set the transaction policy in the vendor console and export it for audit.
3. Route anything above the per-tx cap through human approval with a distinct quorum; never let one operator both request and approve.
4. Compute windows on a rolling basis, not calendar days, so a drain cannot reset at midnight:
   ```python
   recent = [t for t in outbound if now - t.ts < 24*3600]
   assert sum(t.value for t in recent) + amount <= daily_cap
   ```
5. Emit an event every time a limit is hit, with the attempted amount and requester; a burst of near-limit attempts is the signal to freeze.
6. Review limits after any outage, volume spike, or new counterparty.

## Pitfalls

- Limits on the customer app while a second internal tool can send directly — the attacker uses the unguarded path.
- Daily windows keyed to UTC midnight let two transfers straddle the boundary and double the day's outflow.
- One cap shared by employees and automated payouts drifts upward when payroll needs more room; use per-role caps.
- Counting raw token units instead of USD value makes a low-decimal token look tiny.
- An approver who signs everything in seconds is not a control — measure and cap approval latency too.

## Verification

    cast call $GUARD "checkTransaction(address,address,uint256,bytes,uint8,uint256,uint256,uint256,address,address,bytes)" \
      0x0 0x0 $AMOUNT "0x" 0 0 0 0 0x0 0x0 "0x" --from $SENDER --rpc-url $RPC
    # expect a revert above the cap and success below it

Report the three limits, the guard address or vendor policy id, and the amount at which the call reverts, quoting the output.
