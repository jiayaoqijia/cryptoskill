---
name: compute-vote-escrow-decay-weight
description: Use when measuring locking voting power (veCRV-style) at a future date or comparing locks. Computes the linear decay to unlock and the resulting weight, not the locked balance.
---

# Compute vote-escrow decay weight

In a vote-escrow system your weight is the locked balance scaled by the time remaining, so it decays every second toward zero at unlock. The lock balance is not the vote.

## Procedure

1. Read the lock:
   `cast call $VE "locked(address)(int128,uint256)" $WHO --rpc-url $RPC` returns (amount, end).
   `cast call $VE "balanceOf(address)(uint256)" $WHO --rpc-url $RPC` returns the current decayed weight.
2. Reproduce the decay. Curve's formula is `weight = amount * (end - now) / MAXTIME`, where `MAXTIME = 4 years` (126144000 seconds).
   Worked example: amount = 1000e18, end - now = 2 years = 63072000, so weight = 1000 * 63072000 / 126144000 = 500.
3. Verify against the contract:
   `python3 -c "print(1000*63072000//126144000)"` -> `500`, matching `balanceOf`.
4. Extend the lock to raise weight: `increase_unlock_time` resets to a longer end and raises `balanceOf`; re-read after the transaction.
5. For a future date, project: `weight_t = amount * (end - t) / MAXTIME` for `t < end`, else 0.
6. Aggregate for voting: only the current `balanceOf` counts, so a snapshot taken near an unlock has materially less weight than a month earlier.

7. Convert the unlock timestamp to a date and state it, so the decay is anchored to a calendar, not a raw block.
8. If the lock is transferable (a veNFT), check the current owner: the weight follows the NFT, not the original locker.
9. For a vote, read `balanceOf` at the snapshot block, not at execution time, since weight decays between them.

## Pitfalls

- Treating the locked amount as voting power in a tokenomics or concentration analysis; the decayed balance is the correct figure and is often far lower.
- Forgetting the decay is continuous, so two reads a week apart differ; always tag a ve-weight figure with its timestamp.
- Assuming `MAXTIME` is four years for every project; some forks change it, so read the constant from the contract.
- Counting an expired lock (past `end`) as still locked; after expiry `balanceOf` is 0 and the tokens are withdrawable.
- Comparing ve-weight across protocols as if interchangeable; each uses its own lock duration and scale.

- Assuming the lock can be extended to full weight instantly; `increase_unlock_time` is capped at `MAXTIME` from now.
- Forgetting that a withdrawn lock leaves `balanceOf` at 0 while the tokens have left the ve contract.
- Reading the clock from the local machine rather than the chain; time in the formula is the block timestamp.

## Verification

    python3 -c "amt=1000; end=63072000; print(amt*end//126144000)"
    # 500, equal to cast call $VE "balanceOf(address)(uint256)" at the same timestamp

Report the locked amount, the unlock time, the decayed weight, and the formula's result at the same timestamp, with both readings shown.
