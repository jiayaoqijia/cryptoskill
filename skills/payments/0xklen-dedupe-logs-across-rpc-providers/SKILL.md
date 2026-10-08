---
name: dedupe-logs-across-rpc-providers
description: Use when ingesting from several RPC providers in parallel. Keys every log on block_hash, tx_hash and log_index so the same event arriving twice collapses to one row instead of double-counting.
---

# Dedupe logs across RPC providers

Running two providers for redundancy means the same event arrives twice. Identity is not the block number; it is the `(block_hash, tx_hash, log_index)` triple.

## Procedure

1. Fan the same `eth_getLogs` call to at least two providers and compare lengths before trusting either:
   ```python
   a = provider_a.get_logs(rng); b = provider_b.get_logs(rng)
   assert len(a) == len(b), f"provider divergence {len(a)} vs {len(b)}"
   ```
2. Normalise each log and insert against a uniqueness constraint:
   ```sql
   INSERT INTO raw_logs (block_hash, tx_hash, log_index, address, topics, data)
   VALUES ($1,$2,$3,$4,$5,$6)
   ON CONFLICT (block_hash, tx_hash, log_index) DO NOTHING;
   ```
3. When the counts differ, fetch the divergent block by hash from both and diff the sets; a missing log is a provider bug worth alerting on.
4. Use `log_index` (position in block), never a per-provider array index, since provider ordering is not guaranteed.
5. Keep `source_provider` for debugging but never in the primary key.
6. On recurring divergence, drop the unreliable provider from the read path rather than averaging the two.

## Pitfalls

- Keying on `(tx_hash, log_index)` alone collides across a reorg where the same tx is re-mined unchanged in a new block.
- Deduping after decoding hides the divergence; compare raw counts first.
- A provider returning logs in a different order breaks any positional merge; always sort by `(block_number, log_index)`.
- Equal event counts do not mean equal finality; one provider may serve a lagging fork with the same count.

## Verification

    psql -c "SELECT count(*), count(DISTINCT (block_hash,tx_hash,log_index)) FROM raw_logs WHERE block_number=$N;"
    # the two counts must be equal: no duplicate identity rows

Report the cross-provider counts per range and that the distinct-key count equals the total row count.
