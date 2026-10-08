---
name: join-events-to-offchain-orders
description: Use when matching on-chain fills to off-chain order records. Joins on the intent hash or order UID carried in the event, never on amounts or timestamps that collide across orders.
---

# Join events to off-chain orders

Fills on chain must be matched to the order placed off chain. The join key is an identifier embedded in the event (order UID, intent hash), because amounts and times are not unique.

## Procedure

1. Find the identity the settlement contract emits: e.g. CoW `orderUid`, a 0x `orderHash`, or a `bytes32` nonce. That is the join key.
2. Store the raw off-chain order under the same key: `orders(uid bytea PRIMARY KEY, ...)`.
3. Join on the key, not on heuristic columns:
   ```sql
   SELECT f.tx_hash, f.filled_amount, o.owner, o.limit_price
   FROM fills f JOIN orders o ON o.uid = f.order_uid
   WHERE f.block_number BETWEEN $1 AND $2;
   ```
4. Record fills that match no order (`LEFT JOIN ... WHERE o.uid IS NULL`) as anomalies; a fill with no known order means the off-chain store missed it or the contract changed.
5. Reconcile counts: fills per batch must equal the sum of off-chain orders marked `filled` for that batch.
6. Normalise the key representation (hex case, bytea) on both sides before joining; a case mismatch silently yields zero rows.
7. Persist the join result separately from both sources so a re-run of either side does not need the other to be live.
8. Alert when the unmatched-fill count rises above a threshold for a batch; a growing trend means off-chain ingest is falling behind.

## Pitfalls

- Joining on `(amount, timestamp)` matches multiple same-sized orders; the UID is the only safe key.
- Off-chain orders expire and get pruned while their fills persist; keep a tombstone so the join does not go null.
- One settlement tx can fill several orders; a one-to-one join drops all but one.
- When the off-chain DB and chain diverge, the fill is the source of truth for what settled.
- An order UID stored as hex-with-prefix on chain and raw bytes off chain never joins; normalise both to bytea.
- Partial fills mean one UID appears across several fills; aggregate before comparing to the order's filled total.

## Verification

    psql -c "SELECT count(*) FROM fills f LEFT JOIN orders o ON o.uid=f.order_uid WHERE o.uid IS NULL;"
    # expect 0 unmatched fills over settled batches

Report filled-vs-ordered counts per batch and any fill without a matching off-chain order.
