---
name: index-internal-transactions-and-traces
description: Use when contract-to-contract value moves matter but emit no logs. Uses trace_block or debug_traceTransaction to index internal transfers, treating traces as best-effort data that some providers do not serve.
---

# Index internal transactions and traces

Value moved inside a contract call, a withdrawal or a flagless transfer, emits no `Transfer` log. Recovering it needs traces, which not every provider serves.

## Procedure

1. Pick a trace method your node supports: `trace_block(blockNumber)` (Parity/OpenEthereum style) or `debug_traceTransaction(txHash, {tracer})` for fine control.
   ```bash
   curl -s $RPC -H 'content-type: application/json' -d '{
     "jsonrpc":"2.0","id":1,"method":"trace_block","params":["0x121EAC0"]}' | jq '.result | length'
   ```
2. Extract value-bearing internal calls: `callType in ("call","suicide","create")` with a non-zero value, plus `SELFDESTRUCT` balance moves.
3. Store under the same identity scheme, keyed on `(block_hash, tx_hash, trace_address)` where `trace_address` is the path array serialised like `[0,1,2]`.
4. Treat traces as a separate, optional dataset: mark rows provisional and never make core balances depend solely on trace availability.
5. Detect provider gaps; a provider returning an empty trace list for a block known to make calls is wrong. Cross-check against a block that must have internal moves.
6. Reconcile: a contract's balance change should equal its internal transfers plus its logs for the block; any difference is the missing piece.
7. Cap trace requests with the same window budgeting as `eth_getLogs`; heavy blocks return large trace arrays that hit provider limits.
8. Join trace rows to their initiating tx by `(block_hash, tx_hash)` and to the call path by `trace_address`.

## Pitfalls

- `trace_block` is not an EIP-standard method; a load-balanced pool may route it to a node that does not implement it and return an error or an empty result.
- Trace shapes differ between clients (OpenEthereum, Erigon, Geth `debug_`), so a decoder must branch on the schema, not assume one.
- Serialising `trace_address` inconsistently gives the same internal transfer two identities.
- Value-zero calls are noise for balance indexing; filter on value but never drop `suicide` traces.
- A provider that answers `trace_block` with an empty array for a heavy block is silently unsupported; validate on a known block first.
- Reorgs orphan traces exactly like logs; key and delete them by `block_hash`.

## Verification

    curl -s $RPC -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"trace_block","params":["0x121EAC0"]}' | jq '[.result[] | select(.action.value != null and .action.value != "0x0")] | length'
    # expect a non-zero count for a block with known internal value transfers

Report whether the provider serves traces, the internal-transfer count for a sampled block, and how trace rows reconcile with logged transfers.
