---
name: verify-indexer-completeness-with-counts
description: Use when you must prove an indexer has no gaps. Cross-checks a processed-blocks table and per-block log counts, treating any missing block in range as a hole to fix rather than trusting a grand total.
---

# Verify indexer completeness with counts

An indexer can look healthy while missing whole blocks. Completeness is proven by accounting for every block in the range, not by a total that hides holes.

## Procedure

1. Keep a `blocks` table with one row per processed block:
   `CREATE TABLE blocks(number bigint PRIMARY KEY, hash bytea, log_count int, processed_at timestamptz);`
2. Find gaps as heights present on chain but absent locally:
   ```sql
   SELECT gs.number FROM generate_series($START,$END) gs
   LEFT JOIN blocks b ON b.number = gs.number
   WHERE b.number IS NULL ORDER BY 1;
   ```
3. Independently count logs: for a sampled block, compare `SELECT log_count FROM blocks WHERE number=$N` against `eth_getLogs` for that block; they must match.
4. Sum expected against actual: the total logs over the range should equal the sum of per-block `log_count`; a block with chain logs but zero local rows is a decode gap.
5. Make the check a scheduled assertion, not a manual query; alert when the gap count is non-zero.
6. After a fix, re-run the gap query; it must return zero rows.
7. Run the gap check scoped to the range the cursor covers, not the whole chain, so it stays a second-scale query.
8. Store the completeness result as a metric (`gap_count`) and alert the moment it turns non-zero.

## Pitfalls

- A grand total can match while two errors cancel, one block double-counted and one missed; check per block.
- `generate_series` over 20M blocks is slow; audit windows around the cursor, not the whole history at once.
- Blocks with zero logs are legitimate; distinguish "no logs" from "not processed" by the presence of the `blocks` row.
- Trusting the indexer's own reported count without a chain-side comparison proves nothing.
- A `blocks` row written before its logs commit reports a block as done while it is empty; commit the row with its logs.
- A skipped height logged as a real block makes the gap query miss it; write null-hash rows for skipped heights.

## Verification

    psql -c "SELECT count(*) FROM generate_series($START,$END) gs LEFT JOIN blocks b ON b.number=gs.number WHERE b.number IS NULL;"
    # expect 0 missing blocks

Report the gap count, the sampled block's local-versus-chain log counts, and the range audited.
