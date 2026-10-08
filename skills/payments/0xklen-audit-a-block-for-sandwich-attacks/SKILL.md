---
name: audit-a-block-for-sandwich-attacks
description: Use when reviewing a mined block for MEV extraction: reconstructing swaps per pool, identifying sandwich triples with shared profit addresses, and totalling user loss.
---

# Audit a block for sandwich attacks

A block-level sandwich audit reconstructs every swap in a pool, groups them into buy-victim-buy triples, and attributes the profit, so a claim about MEV extraction is backed by a block and a list of transactions rather than an anecdote.

## Procedure

1. Pull all `Swap` events for the target pools in the block, in log order:

   ```bash
   cast logs --from-block $N --to-block $N --address $POOL \
     "Swap(address,address,int256,int256,uint160,uint128)" --rpc-url $RPC
   ```

2. Group by pool and order by log index. A sandwich is three consecutive swaps on one pool where the outer two come from the same sender and the middle is a different address.

3. Confirm the outer legs are an attacker pair, not coincidence: the first swap moves price against the middle swap's direction, and the third reverses the first. Extract the attacker's net token delta — for a proper sandwich it is positive after fees.

   ```bash
   cast run $ATTACKER_TX --rpc-url $RPC --trace | grep -iE "Transfer|Swap"
   ```

4. Quantify victim loss: the difference between the victim's realized rate and the pool mid before the attacker's front leg. That is the extractable value taken from the user, plus their fees.

5. Check for multi-pool sandwiches: an attacker routing through a helper pool still shows as adjacent swaps on the victim's pool; follow the attacker's transfers, not just one pool's events.

6. Attribute MEV to the builder too: the attacker paid a bid to be ordered this way. The builder's take is the coinbase transfer from the attacker's bundle.

7. Totals: sum victim loss, attacker gross, builder bid, and gas. Report per-sandwich rows and a block total. Cross-check the attacker gross against on-chain balance deltas.

## Pitfalls

- Counting any three same-pool swaps as a sandwich. Retail flow produces the same shape; only a shared outer sender plus a positive net delta qualifies.
- Using the victim's displayed quote instead of the pre-front-swap pool mid; that inflates the measured loss.
- Missing sandwiches split across two transactions of a multi-leg router, where the middle swap is embedded in a batch.
- Ignoring that a builder can reorder without a searcher; the outer legs may belong to the block builder's own bundle, which changes who profited.
- Forgetting L2 sequencer reordering, where the same pattern exists without a builder bid to attribute.

## Verification

    cast logs --from-block $N --to-block $N --address $POOL "Swap(address,address,int256,int256,uint160,uint128)" --rpc-url $RPC

Rows with a shared outer sender and a positive attacker net delta on the victim pool confirm a sandwich. Report the block, each triple's tx hashes, victim loss, attacker gross, and the builder bid.
