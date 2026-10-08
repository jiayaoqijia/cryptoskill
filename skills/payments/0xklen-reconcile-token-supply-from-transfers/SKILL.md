---
name: reconcile-token-supply-from-transfers
description: Use when indexed transfer sums must agree with on-chain totalSupply. Reconstructs circulating supply from mint and burn events and flags any gap between the indexer and the contract.
---

# Reconcile token supply from transfers

If the sum of indexed mints minus burns does not equal `totalSupply()`, the indexer missed events. This is the single sharpest correctness check for a token indexer.

## Procedure

1. Treat `Transfer(0x0, to, amount)` as a mint and `Transfer(from, 0x0, amount)` as a burn.
2. Compute net supply from indexed rows:
   ```sql
   SELECT COALESCE(sum(CASE WHEN from_addr='\x0000000000000000000000000000000000000000' THEN amount
                            WHEN to_addr  ='\x0000000000000000000000000000000000000000' THEN -amount END),0) AS minted
   FROM transfers WHERE token = $TOKEN;
   ```
3. Read the contract's figure and compare exactly:
   `cast call $TOKEN "totalSupply()(uint256)" --rpc-url $RPC`
4. A mismatch means a missed block, a decoder miss, or a non-canonical mint. Find the block where the two series first diverge, not just the end.
5. For rebasing or fee-on-transfer tokens the event sum will exceed `totalSupply`; account for that model explicitly before calling it a bug.
6. Run the check per token on a schedule and store the delta so drift is a metric, not a surprise.
7. Compare at increasing granularity: total, then per-epoch, then per-block, to localise the first divergence fast.
8. Persist each reconciliation snapshot (block, indexed, on-chain, delta) so the drift's slope is visible over time.

## Pitfalls

- Assuming zero-address burns always reduce supply: some tokens burn to a dead address (`0x...dEaD`), not the zero address; read the contract.
- Wrapped or bridged tokens mint against a deposit; supply here reconciles to the wrapper, not the underlying.
- A token migrated across a proxy shows two supply histories at one address; sum per implementation.
- Comparing at `latest` right after a mint can show a transient one-block gap; compare at a finalized block.
- A reorg between reading the chain and reading the indexer makes a correct indexer look wrong; read both at the same finalized block.
- Bridged tokens mint on one chain against a burn on another; reconcile each side separately, not across chains.

## Verification

    python -c "import checker; print(checker.supply_delta('$TOKEN'))"
    # expect 0 for a standard token, or a documented protocol delta for rebasing/fee tokens

Report the indexed mint-minus-burn total, the contract totalSupply, and the block where any divergence first appears.
