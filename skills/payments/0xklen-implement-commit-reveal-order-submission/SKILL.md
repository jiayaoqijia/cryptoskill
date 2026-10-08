---
name: implement-commit-reveal-order-submission
description: Use when building or using an orderflow path that must resist front-running by design: splitting an order into a commitment and a later reveal, with the hashing, deadline, and bonding that make it safe.
---

# Implement commit-reveal order submission

Commit-reveal replaces a free option for searchers with a revealed-but-unfrontrunnable order: the searcher sees the order only at reveal time, so it cannot position ahead of it unless the reveal itself is front-runnable, which the deadline and bond prevent.

## Procedure

1. Define the commitment: `commit = keccak256(abi.encode(order, salt, user, deadline))`. The salt prevents guessing low-entropy orders from a dictionary of common sizes.

2. Publish the commitment on-chain before submitting the order anywhere. The commitment must be visible, or the reveal is not binding on anyone:

   ```solidity
   function commit(bytes32 c) external { commitments[c] = block.number; }
   ```

3. Reveal within a bounded window. `require(block.number <= committedAt + MAX_DELAY)`. A reveal that can happen arbitrarily later lets a searcher wait to see whether the order is profitable.

4. Reveal through a path that binds execution to the same block, e.g. submit the payload to a builder bundle that includes the order and the matching swell of liquidity, so a front-runner cannot insert between reveal and fill.

5. Add a bond or a refundable deposit on the revealer so a reveal-and-revert spam cannot grief the order book. Without a cost, anyone can reveal and drop.

6. Verify the revealed payload matches the commitment exactly — same order fields, same salt, same user. Any mismatch is a gossip attack; reject and slash if bonded.

7. Bind the fill price to the reveal. The order must execute at a price derived from the state at reveal, not at commit; otherwise the commitment is stale and a searcher can game the interval.

8. For a maker-side auction, expose only the hash pre-trade and the full order post-trade; this is the same shape as MEV-Share hints, but with the order contents rather than calldata as the secret.

## Pitfalls

- Low-entropy salt. If the salt is predictable, the order is brute-forceable from the commitment and the commit phase is decorative.
- Revealing to the public mempool. That reintroduces exactly the extractable window commit-reveal was built to remove; reveal into a private or bundled path.
- An unbounded reveal window, which converts the commitment into a free option: wait, see, then reveal only if you still like the price.
- Forgetting that the order contents leak at reveal; a searcher with lower latency can still beat the reveal to the pool unless the reveal is bundled.
- Assuming commit-reveal protects against a censoring sequencer or builder that simply drops the reveal.

## Verification

    cast call $COMMITTER "commitments(bytes32)(uint256)" $COMMIT_HASH --rpc-url $RPC

The commitment exists before the order is visible anywhere, and the reveal's `block.number <= committedAt + MAX_DELAY` holds. Report the commitment hash, reveal block, delay, and whether the two payloads matched.
