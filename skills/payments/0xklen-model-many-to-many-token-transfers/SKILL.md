---
name: model-many-to-many-token-transfers
description: Use when indexing token flows where one transaction moves many assets between many holders. Normalises transfers into rows of sender, receiver, token and amount instead of one fat row per transaction.
---

# Model many-to-many token transfers

A swap or batch transfer moves several tokens between several addresses. Cramming them into one transaction row makes per-holder balances and per-token supply queries wrong.

## Procedure

1. Model the event, not the transaction: `transfers(log_index, tx_hash, token, from_addr, to_addr, amount numeric)`.
2. Keep `amount` as a numeric of the token's raw units; a single bigint fails for 18-decimal tokens near their max:
   ```sql
   CREATE TABLE transfers (
     block_number bigint, block_hash bytea, log_index int, tx_hash bytea,
     token bytea, from_addr bytea, to_addr bytea,
     amount numeric(78,0), PRIMARY KEY (block_hash, tx_hash, log_index)
   );
   ```
3. Link to the parent by `tx_hash`, but do not merge transfers into it; a batch holds N transfers per 1 tx.
4. Reconstruct a holder balance with a windowed sum, not a stored running total:
   `SELECT addr, sum(delta) FROM (SELECT to_addr AS addr, amount AS delta FROM transfers WHERE token=$T UNION ALL SELECT from_addr, -amount FROM transfers WHERE token=$T) s GROUP BY 1;`
5. Use the zero address for mints and burns consistently so supply = sum(mints) - sum(burns).
6. Index `(token, to_addr)` and `(token, from_addr)` for holder queries.

## Pitfalls

- One row per transaction loses the intermediate parties of a multi-hop swap; downstream balance math is then wrong.
- `float`/`double` for amounts loses precision on large 18-decimal values; use `numeric(78,0)`.
- Counting a transfer to the zero address as normal inflates holder counts.
- The same log_index under two block hashes (reorg) must stay distinct; key on the hash.

## Verification

    psql -c "SELECT token, sum(CASE WHEN to_addr='\x0000000000000000000000000000000000000000' THEN amount ELSE 0 END) - sum(CASE WHEN from_addr='\x0000000000000000000000000000000000000000' THEN amount ELSE 0 END) AS supply FROM transfers GROUP BY token;"
    # compare each row against totalSupply() for that token via cast call

Report transfer row counts per transaction and per-token supply cross-checked against `totalSupply()`.
