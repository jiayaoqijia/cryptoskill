---
name: reconcile-custody-balances-against-the-ledger
description: Use when on-chain custody balances must be proven against internal records. Compares per-address on-chain holdings with the ledger, isolates timing and fee effects, and reports every unreconciled unit.
---

# Reconcile custody balances against the ledger

On-chain balances and the internal ledger diverge for innocent reasons — in-flight transfers, pending fees, rebasing tokens — and for the reason you care about. This skill reconciles at a fixed block height and explains every difference instead of rounding it away.

## Procedure

1. Pin a block height so both sides measure the same instant:
   `cast block-number --rpc-url $RPC` and record it; a moving head makes the comparison meaningless.
2. Sum on-chain holdings per address, including native gas token and every ERC-20 that matters, at that block:
   `cast balance $ADDR --block $HEIGHT --rpc-url $RPC`
   `cast call $TOKEN "balanceOf(address)(uint256)" $ADDR --block $HEIGHT --rpc-url $RPC`
3. Compare each token's totals. Normalise units by decimals before comparing — never compare raw integer units across tokens.
4. Categorise each difference:
   - In-flight: a transfer included after the ledger cut-off. Match it by tx hash.
   - Fees: gas paid from a hot wallet shows on-chain but may post to the ledger late.
   - Rebasing / yield: a token whose `balanceOf` grows without transfers breaks naive equality.
5. Investigate any difference not explained by those categories. A missing outflow with no matching ledger entry is the signal, not noise.
6. Produce a reconciliation table: address, token, on-chain, ledger, delta, and the reason. Round nothing to "close enough".
7. Re-run at the next epoch; a difference that persists across two reconciliations is real.

## Pitfalls

- Comparing at `latest` on one side and a stale cache on the other invents differences; pin one block for both.
- Ignoring decimals makes a 6-decimal stablecoin look off by a factor of 10^12 against an 18-decimal token.
- A pending incoming transfer counted in the ledger but not yet mined is an expected delta, not a loss.
- Wrapped or staked positions move the "real" balance off the address; reconcile against the position, not the wrapper's own balances, or you double-count.
- Treating a rebase token like a normal balance produces a permanent unexplained delta; track shares, not balances.

## Verification

    cast balance $HOT --block $HEIGHT --rpc-url $RPC && cast call $TOKEN "balanceOf(address)(uint256)" $HOT --block $HEIGHT --rpc-url $RPC
    # expect each delta to carry a reason; any unexplained delta fails the reconciliation

Report the block height, per-token deltas, and the reason for each, quoting the commands behind them.
