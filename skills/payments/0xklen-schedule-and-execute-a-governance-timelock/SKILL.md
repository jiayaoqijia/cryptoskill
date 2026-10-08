---
name: schedule-and-execute-a-governance-timelock
description: Use when queuing a passed proposal into a timelock or executing one after the delay. Reads the ETA and grace window, checks the predecessor/salt, and confirms the executed transaction matches the queued payload.
---

# Schedule and execute a governance timelock

The timelock is the last gate between a passed vote and a state change; queuing the wrong payload, or missing the grace window, strands a legitimate proposal. Read the delay and the ETA before you queue, and re-decode at execution time.

## Procedure

1. Read the timelock parameters:
   `cast call $TIMELOCK "getMinDelay()(uint256)" --rpc-url $RPC`
   `cast call $GOV "proposalEta(uint256)(uint256)" $ID --rpc-url $RPC`
   The ETA is `queuedAt + delay`; some governors set ETA at propose time instead.
2. Confirm the payload identity. OpenZeppelin v5 derives the timelock id from
   `keccak256(abi.encode(targets, values, calldatas, predecessor, salt))`; a single changed calldata byte yields a different id and the execute reverts.
3. Queue through the governor so the id is computed consistently:
   `cast send $GOV "queue(address[],uint256[],bytes[],bytes32)" $TARGETS $VALUES $CALLDATAS $DESC_HASH --rpc-url $RPC --private-key $KEY`
4. Wait until `block.timestamp >= eta`. Executing early reverts with `TimelockController: operation is not ready`.
5. Check the grace window before executing. If `getTimestamp(id)` returns a time beyond the grace period, the operation is expired and must be re-proposed:
   `cast call $TIMELOCK "getTimestamp(bytes32)(uint256)" $OP_ID --rpc-url $RPC`
6. Execute, then prove the effect: decode the transaction's logs and compare the target contract's state before and after.
7. If the timelock is cancelled before execution, `isOperationDone` stays false and the id is marked cancelled.

## Pitfalls

- Assuming ETA equals queue time plus delay without reading `proposalEta`; a governor can set it at proposal creation, making the real dwell time shorter.
- Queueing components separately instead of the batch; a timelock operation is atomic and partial queues never execute.
- Letting the grace period lapse during a holiday; the operation silently expires and a fresh vote is required.
- Executing from a key without `EXECUTOR_ROLE`; on a permissioned timelock the caller must be granted the role, not just anyone.
- Trusting the governor's `execute` to hit the intended contract; a modified calldata between queue and execute changes the id, so re-decode rather than assume.

## Verification

    cast call $TIMELOCK "getTimestamp(bytes32)(uint256)" $OP_ID --rpc-url $RPC
    # non-zero and <= now (within grace) means executable; 0 means never queued, done means already run

Report the min delay, the ETA, the operation id, and the post-execution state change, each backed by its command output.
