---
name: store-raw-logs-before-decoding
description: Use when ingesting chain events whose ABI may change. Persists the raw log before any decode so a decoder bug is repairable without re-fetching from an archive node.
---

# Store raw logs before decoding

Decoding during ingestion is a one-way door: if the ABI was wrong the original bytes are gone. Persist the untouched log first, decode into derived tables second.

## Procedure

1. Ingest the raw log verbatim into `raw_logs`, keyed so re-ingestion is a no-op:
   ```sql
   CREATE TABLE raw_logs (
     block_hash bytea NOT NULL, block_number bigint NOT NULL,
     tx_hash bytea NOT NULL, log_index int NOT NULL,
     address bytea NOT NULL, topics bytea[] NOT NULL, data bytea NOT NULL,
     removed boolean NOT NULL DEFAULT false,
     PRIMARY KEY (block_hash, tx_hash, log_index)
   );
   ```
2. Insert with `ON CONFLICT DO NOTHING` so replaying a block adds nothing.
3. Decode in a second pass from `raw_logs` into typed tables (`transfers`, `swaps`). A decoder bug then means re-running the second pass, not an archive hit.
4. Record the decoder used per row: `decoder_version smallint NOT NULL`.
5. Check the raw row count for a block equals the node's `eth_getLogs` count before decoding.
6. Keep the `removed` flag as the node passed it; a reorg marks rows rather than silently dropping them.

## Pitfalls

- Decoding inside the fetch loop and discarding the bytes makes an ABI fix a full historical refetch of hours of archive RPC.
- Storing only decoded columns means a newly wanted field cannot be recovered for past blocks without archive access you may not have.
- `topics` is an array; flattening it to one column loses the indexed-parameter positions you need to decode.
- Ignoring `removed` makes reorg-dropped logs look like valid events.

## Verification

    psql -c "SELECT count(*) FROM raw_logs WHERE block_number=$N;"
    # expect it to equal the eth_getLogs length for block $N

Report raw rows ingested per block and that decode runs as a separate, re-runnable pass keyed on raw_logs.
