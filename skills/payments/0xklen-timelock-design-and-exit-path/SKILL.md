---
name: timelock-design-and-exit-path
description: Use when designing or reviewing a timelock-controlled contract. Sets the delay and grace period, separates proposer/executor/canceller roles, and guarantees users can exit before a queued change lands.
---

# Design a timelock with an exit path

A timelock only protects users if they can act during the delay. This skill sets a delay long enough to be useful, confirms every privileged action is queued through it, and verifies that funds can be withdrawn before a queued upgrade executes.

## Procedure

1. Set the delay against the value at risk. Common floors: 48 hours for governance, 72 hours for upgrades touching user funds, 7 days for an upgradeable proxy holding a treasury. Read the current value:
   `cast call $TIMELOCK "getMinDelay()(uint256)" --rpc-url $RPC`
2. Confirm the delay is non-zero and enforced: `getMinDelay()` must be > 0, and every `onlyTimelock` path must go through `schedule`/`execute`, not a direct admin call.
3. Separate the roles. `PROPOSER_ROLE`, `EXECUTOR_ROLE`, and `CANCELLER_ROLE` should be distinct; a single key holding all three can fast-track its own proposal through the same window it controls.
4. Verify a queued operation's ETA:
   `cast call $TIMELOCK "getTimestamp(bytes32)(uint256)" $OP_ID --rpc-url $RPC`
   The `OP_ID` is `keccak256(abi.encode(target, value, data, predecessor, salt))`.
5. Prove the exit path: before any upgrade executes, a user must be able to withdraw their principal without admin cooperation. Test the withdrawal on a fork at the post-upgrade state.
6. Set a grace period (for example `2 * delay`), after which a scheduled op is invalid and must be re-proposed — a never-expiring queue is a latent backdoor.
7. Document every scheduled op with its ETA and successor so users know the window.
8. Alert on every `CallScheduled` event so the exit window is never missed.

## Pitfalls

- A timelock with admin functions outside the timelock is decorative; audit for a direct owner setter or an `emergencyExecute`.
- A very long delay with no cancellable path means a legitimate fix is stuck; keep CANCELLER separate from PROPOSER.
- Schedule and execute in the same block via a malicious `predecessor` ordering bypasses the waiting period.
- If the delay elapses but users cannot exit (locked in a vault with no withdraw), the timelock protects no one.
- Role renouncement or a self-administered timelock that can lower its own delay removes the protection entirely.

- A timelock that governs the proxy admin but not the implementation's initializer still leaves a gap.
- Executing a queued op requires the delay to have elapsed; a bot that auto-executes removes the review time.
- Queued calldata that is not decoded at schedule time is reviewed only after it can no longer be stopped.

## Verification

    cast call $TIMELOCK "getMinDelay()(uint256)" --rpc-url $RPC && cast call $TIMELOCK "getTimestamp(bytes32)(uint256)" $OP_ID --rpc-url $RPC
    # expect a nonzero min delay and an ETA at least min-delay in the future

Report the min delay, the queued op's ETA, and whether the exit path was exercised on the fork, quoting the commands.
