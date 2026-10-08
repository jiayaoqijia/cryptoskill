---
name: handle-block-gaps-and-skipped-slots
description: Use when a chain skips block numbers through empty slots or missed proposers. Advances the cursor over absent heights by confirming parent linkage, instead of treating an absent block as a fetch failure.
---

# Handle block gaps and skipped slots

Some chains do not produce every height: an empty slot or a missed proposer means block N+1 or N+2 follows N with a height missing in between. Treating an absent height as "fetched nothing, retry" stalls the indexer forever.

## Procedure

1. When `eth_getBlockByNumber(N)` returns null, decide which case it is: N is in the future, N was skipped, or the provider is lying.
2. Confirm a skip through parent linkage: if block N+1 exists with `parentHash == hash(N-1)`, then N was skipped.
   ```python
   nxt = block(n + 1)
   if nxt and nxt["parentHash"] == block(n - 1)["hash"]:
       skipped.add(n)          # a legitimately absent height
   ```
3. For a skipped height, write a `blocks` row with `hash = NULL` and `log_count = 0`, then advance the cursor; do not retry.
4. Retry a null only when the head has not yet passed N (the future case). Once head > N and linkage confirms a skip, move on.
5. Never loop on `null` without a bound; cap retries, then advance with a logged warning.
6. On slot-based chains, index by slot or by height consistently; mixing the two manufactures phantom gaps.
7. Batch the skip check: fetch N+1 and N-1 together so proving a skip costs two lookups, not a walk.
8. Persist the skip as a null-hash block row so a restart does not re-ask the provider about a height that never existed.

## Pitfalls

- Infinite retry on a permanently skipped height is a silent stall; bound the retries.
- Assuming contiguous heights breaks on chains that allow gaps; never `for n in range(last+1, head+1): fetch(n)` without handling null.
- Confusing a provider's "not found yet" with "skipped" and advancing early can index a block that later appears.
- A reorg removal and a skip both yield a missing height; only linkage distinguishes them.
- A provider that returns null for a block it does not have yet is indistinguishable from a skip until the head passes it; wait for head > N.
- Backfilling across a skipped range double-counts if the gap row is later overwritten by a real block; upsert on height.

## Verification

    cast block $N --rpc-url $RPC --json | jq -r '.hash // "skipped"'
    # and confirm block $N+1's parentHash equals block $N-1's hash to prove the skip

Report the skipped heights found, that each has a null-hash cursor row, and that processing advanced past them.
