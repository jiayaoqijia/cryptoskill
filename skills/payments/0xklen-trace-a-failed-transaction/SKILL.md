---
name: trace-a-failed-transaction
description: Use when a transaction reverted or a simulation fails and you need the exact revert reason and the call stack that produced it.
---

# Trace a failed transaction

A receipt only tells you the tx reverted. To get the reason you must replay the call or fetch
a trace. Replay on a fork is the most portable method; `debug_*` RPCs give the full call tree
when the provider enables them.

## Procedure

1. Confirm it actually failed and get the basics.

       cast receipt $TX --json --rpc-url $RPC | jq -r '.status, .gasUsed, .to, .from, .blockNumber'
       # status 0x0 == reverted

2. Replay it locally with a trace. `cast run` re-executes the tx against a fork and prints the
   call tree and revert reason. It needs archival state at that block.

       cast run $TX --rpc-url $ARCHIVE_RPC -vvvv

3. If the provider exposes `debug_`, fetch a structured trace:

       cast rpc debug_traceTransaction $TX \
         '{"tracer":"callTracer"}' --rpc-url $RPC | jq -r '.result.error, .result.revertReason'

   Or the parity-style trace API:

       cast rpc trace_transaction $TX --rpc-url $RPC | jq -r '.[].traceAddress, .[].error'

4. To reproduce without a mined tx, simulate the same call at the failing block:

       cast call $TO --trace $INPUT --from $FROM --block $((BLOCK-1)) --rpc-url $ARCHIVE_RPC

5. Decode the reason. Custom errors resolve to a 4-byte selector; `Error(string)` is
   `0x08c379a0`; `Panic(uint256)` is `0x4e487b71` (arithmetic, overflow, div-by-zero).

       cast 4byte 0x4e487b71
       cast sig "InsufficientBalance(uint256,uint256)"

## Pitfalls

- `debug_traceTransaction` and `trace_*` are disabled on most free and many mid-tier providers;
  a "method not found" error is an entitlement problem, not a tx problem.
- Tracing a tx from a block the node has pruned fails with a state error even though the receipt
  is available; use an archive endpoint for `cast run`.
- The callTracer truncates or omits internal reverts that were caught in Solidity `try/catch`:
  the outer tx can have `status 1` while an internal call reverted silently.
- A revert inside a `require` without a message yields no reason — you must infer it from the
  call context (balances, allowances, block).
- `cast call` at `latest` may succeed while the historical tx failed because state changed;
  always pin the block to just before the failing tx.

## Verification

    cast run $TX --rpc-url $ARCHIVE_RPC -vvvv 2>&1 | grep -i -m1 revert
    cast 4byte <revert selector>              # names the custom error, if any

Report the failing tx hash, the reverted frame (from function → to function), and the decoded
revert reason (string, `Panic(code)`, or custom-error name).
