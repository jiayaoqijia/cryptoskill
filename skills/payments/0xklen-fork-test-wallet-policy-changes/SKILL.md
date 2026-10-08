---
name: fork-test-wallet-policy-changes
description: Use when changing an allowlist, spending cap, or guard on a live wallet. Replays the change and a representative transfer against a mainnet fork so the policy is proven before real signers approve.
---

# Fork-test wallet policy changes

Policy changes on a live wallet are hard to undo and easy to get subtly wrong — an off-by-one on a cap, a linked-list error in an allowlist, a guard that reverts legitimate spends. This skill proves the change on a fork first.

## Procedure

1. Snapshot the exact state the change will run against: fork at the current block so token balances, allowances, and the owner set match mainnet.
   `anvil --fork-url $RPC --fork-block-number $LATEST`
2. Apply the pending policy change on the fork with the same calldata you intend to sign (allowlist add, `setGuard`, cap update).
3. Run a representative transaction that should pass — a normal spend to an allowlisted destination within the cap — and confirm it succeeds on the fork.
4. Run the negative cases: over-cap amount, non-allowlisted destination, a below-assumed-decimal token amount, and a transfer during the cool-down. Each must revert with the expected reason.
5. For an allowlist change, exercise the linked-list boundary: add at the head, add at the tail, remove the head, remove the tail. Off-by-one in `prevModule`/`prevOwner` ordering shows up only here.
6. Confirm the change itself is reversible on the fork (a guard can be removed, an allowlist entry deleted) before signing the real one.
7. Record the fork block number and the calldata hashes so the mainnet transaction is provably the tested one.

## Pitfalls

- Forking at a stale block lets your balance assumptions drift; fork at `latest` and state the block number.
- A fork has no mempool competition; success on a fork does not prove gas or MEV outcomes, only that the policy logic holds.
- Testing only the happy path misses the whole point; the revert cases are the test.
- An allowlist implemented as a sorted linked list returns a different `prev` after insertions; copy the exact ordering from the fork state, never from memory.
- Rebuilding the calldata by hand after the fork test means you signed something untested; hash and compare.
- If the guard reads a price oracle, fork at a block where the oracle value is representative; a manipulated block gives false confidence.
- Anvil's default tip may exclude your recent deployment; pin it with `--fork-block-number`.
- A policy that passes on a fork can still fail on mainnet under a different `tx.origin`; test with the real sender.
- Rerun the whole suite after any change to the policy contract; a one-line fix invalidates prior results.

## Verification

    # on the fork: happy path succeeds, and each negative case reverts
    cast send $TOKEN "transfer(address,uint256)" $ALLOWED $SMALL --from $SENDER --rpc-url http://127.0.0.1:8545
    cast send $TOKEN "transfer(address,uint256)" $BLOCKED $SMALL --from $SENDER --rpc-url http://127.0.0.1:8545
    # expect the first to succeed and the second to revert with the policy reason

Report the fork block, the calldata hash tested, and the pass/revert results, quoting the outputs.
