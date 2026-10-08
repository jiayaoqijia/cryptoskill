---
name: replay-blocks-idempotently
description: Use when blocks must be processed more than once after a reorg, restart or bug fix. Makes every derived write an upsert keyed on chain identity so reprocessing a block changes nothing.
---

# Replay blocks idempotently

Every indexer will process some block twice. The design that survives it keys derived state on chain identity and upserts, so replay is a no-op rather than a doubling.

## Procedure

1. Choose the natural key from chain data: `(block_hash, tx_hash, log_index)` for events, `(block_hash, tx_hash)` for transactions.
2. Write every derived row as an upsert:
   ```sql
   INSERT INTO transfers (block_hash, tx_hash, log_index, from_addr, to_addr, value)
   VALUES ($1,$2,$3,$4,$5,$6)
   ON CONFLICT (block_hash, tx_hash, log_index) DO UPDATE
     SET value = EXCLUDED.value;
   ```
3. Derive aggregates from the row table, never incrementally, so a replay recomputes rather than adds: `total = SELECT sum(value) FROM transfers WHERE ...`.
4. Never use a bare `INSERT` on chain data; `UPDATE ... SET x = x + 1` is the counter that doubles on replay.
5. Advance the cursor in the same transaction as the block's writes so cursor and data commit together.
6. Test it: process the same block twice and assert the row counts are unchanged.

## Pitfalls

- Increment counters (`balance += value`) applied twice inflate; recompute from logged rows instead.
- A cursor committed before its data leaves a hole on replay-forward; commit together.
- `ON CONFLICT DO NOTHING` hides a decoder change; use `DO UPDATE` when the decoder version changed so re-decoded fields actually land.
- Sequence-generated surrogate IDs are not idempotent keys; they differ on every replay.

## Verification

    for i in 1 2; do python -m indexer replay --block $N; done
    psql -c "SELECT count(*) FROM transfers WHERE block_number=$N;"
    # the count is identical after both runs

Report the block replayed twice and identical derived row counts after each pass.
