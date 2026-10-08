---
name: simulate-a-transaction-before-broadcast
description: Use when preparing to broadcast a state-changing mainnet transaction. Runs the tx against forked state, inspects balance deltas and logs, and halts on unexpected effects.
---

# Simulate a transaction before broadcast

Simulation is the cheapest way to discover that a transaction drains an account, reverts after spending gas, or hits a contract that is not the one you think. This skill replays the exact tx on real state and reads the net effect before anything is irreversible.

## Procedure

1. Simulate the pending or built transaction against a mainnet fork at the current block:
   `cast run <txhash> --fork-url $RPC`
   For a not-yet-broadcast tx, run `cast run --from $SENDER --to $TO --data $CALLDATA --value $WEI --fork-url $RPC`.
2. Read the trace for the actual value flow: list the `Transfer`, `Approval`, and `DelegateCall` events and confirm each sender and recipient is expected.
3. Check the receiver's token balance before and after:
   `cast call $TOKEN "balanceOf(address)(uint256)" $RECIPIENT --rpc-url $RPC`
4. Capture the gas the simulation used and compare it to your gas limit; a tx that reverts only on-chain often diverges from the estimate here.
5. For an ABI-heavy payload, produce a full simulation via an external service when local forking is impractical:
   `curl -s -X POST https://api.tenderly.co/api/v1/simulate -H "X-Access-Key: $TENDERLY_KEY" -H "Content-Type: application/json" -d @sim.json`
6. Assert the effect you expect. If the simulation shows a transfer to an address you did not name, stop and re-review.
7. Re-simulate at a fresh block immediately before broadcasting; state changes every block.

## Pitfalls

- A fork at an old block hides a proxy upgrade or a pausing guardian that landed since; always fork at `latest`.
- Simulation skips the mempool: MEV, front-running, and sandwich effects will not appear. Simulate to catch contract bugs, not market effects.
- `eth_call` with a stale nonce can pass while the real send fails; check the nonce the simulation used.
- Treating a "success" as safe when the trace shows an internal `DELEGATECALL` to an unknown implementation is how proxy traps slip through.
- A simulation that reverts for an environmental reason (gas cap, block gas limit) can look benign while the real tx would execute a harmful path.

- Simulating with a different `from` than the real sender changes allowances and balances in the trace.
- Oracle reads at the forked block can differ from the block the tx lands in; treat price-dependent paths carefully.
- A simulation that passes on a public RPC still may not reflect a private mempool's ordering.

## Verification

    cast run <txhash> --fork-url $RPC 2>&1 | grep -E "Transfer|Approval|Revert"
    # expect only the events you predicted and no Revert

Report the in-trace asset movements and the gas used, quoting the simulation command.
