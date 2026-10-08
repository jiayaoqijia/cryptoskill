---
name: fetch-archival-state
description: Use when you must read balances, storage or call results at a historical block and a normal full node returns zero or a pruned-state error.
---

# Fetch archival state

Reading state at an old block needs an archive node. A pruned full node often answers with
`0x0` or `null` rather than an error, so the failure mode is silently wrong data — verify the
endpoint is archival before trusting any historical read.

## Procedure

1. Establish a known-good archive endpoint. Free/full RPCs cannot serve state older than the
   pruning window; archive access is a separate, usually paid endpoint (Alchemy archive,
   QuickNode archive, Infura archive, or your own `erigon`/`reth --archive`).
2. Probe whether the endpoint is archival by reading a value that is known non-zero now and at
   the old block:

       cast balance 0x00000000219ab540356cBB839Cbe05303d7705Fa \
         --block 14000000 --rpc-url $ARCHIVE_RPC

   A `0x0` for the deposit contract (which has held ETH since 2020) means pruned state, not an
   empty account.
3. Read storage and calls at a pinned block:

       cast storage $TOKEN 0x0 --block 18000000 --rpc-url $ARCHIVE_RPC
       cast call $TOKEN "balanceOf(address)(uint256)" $HOLDER \
         --block 18000000 --rpc-url $ARCHIVE_RPC
       cast call $CONTRACT "foo()(uint256)" --block 18000000 --rpc-url $ARCHIVE_RPC

4. Recognise the real pruned-state errors so you can fail loudly instead of returning zeros:

       # typical: "missing trie node ... state ... is not available"
       # Erigon/geth: "historical state ... not available" / "pruned"
       cast call $X "bar()(uint256)" --block 1 --rpc-url $FULL_NODE 2>&1 | head -3

5. If no archive node is available, reconstruct from logs (`reconstruct-state-from-event-logs`)
   or use an indexer dataset (Dune, Flipside, an explorer's historical API), and note the lag.

## Pitfalls

- A full node returning `0x0` for a historical `eth_getBalance`/`eth_call` is the most common
  silent failure; it looks identical to a genuinely empty account. Always sanity-check against
  a known non-zero historical value.
- `eth_getLogs` works on full nodes for the whole history (logs are per-block data), but
  `eth_call`/`eth_getStorageAt` at old blocks do not — do not assume one implies the other.
- Archive endpoints are usually a *different URL* from your fast read endpoint, and often 2–5×
  the cost or latency; do not route live reads through them.
- A state read at a block that has since been reorged away returns data for a chain that no
  longer exists; pin to a finalized block for reproducibility.
- Indexer datasets (Dune/Flipside) lag ingestion by minutes to hours and can be re-run with
  changed results; record the run id.

## Verification

    cast balance 0x00000000219ab540356cBB839Cbe05303d7705Fa --block 14000000 --rpc-url $ARCHIVE_RPC
    # non-zero proves the endpoint serves archival state

Report the block pinned, the archive endpoint used, and the historical value; state explicitly
that a pruned `0x0` was distinguished from a real zero.
