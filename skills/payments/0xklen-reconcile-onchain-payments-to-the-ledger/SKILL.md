---
name: reconcile-onchain-payments-to-the-ledger
description: Use when closing the books on crypto receipts. Pulls confirmed transfers into a ledger snapshot and proves every invoice is matched exactly once, using a cut-off block.
---

# Reconcile on-chain payments to the ledger

A crypto ledger reconciles when every confirmed transfer maps to exactly one invoice line at the rate recorded on the invoice, bounded by a cut-off block. Prove that equality; do not eyeball totals.

## Procedure

1. Fix the cut-off: block number and timestamp. Everything at or below is in scope; later transfers are next period.
   `cast block $CUTOFF --rpc-url $RPC | grep -E "number|timestamp"`
2. Pull all inbound transfers to your addresses up to the cut-off:
   `cast logs --address $TOKEN --from-block $START --to-block $CUTOFF "$TRANSFER_TOPIC" > transfers.json`
3. Normalise each transfer: tx hash, from, value in base units to decimal, and the rate recorded on the matching invoice.
4. Match: join transfers to invoices by reference (or from-address plus window). Flag transfers with no invoice (unidentified) and invoices with no transfer (unpaid).
5. Sum in a script, never by hand:
   `python3 -c "print(sum(x['usd'] for x in transfers) - sum(i['usd'] for i in matched))"`
   The difference must be 0, or fully explained by tolerance, fees, and customer credits.
6. Confirm each matched tx has enough confirmations per policy before treating it as settled.
7. Output three lists: matched, unidentified, outstanding. The unidentified list is the one that hides theft and misdirected payments.

## Pitfalls

- Reconciling at the current block while new confirmations keep arriving: fix a cut-off or totals move under you.
- Summing raw base units across tokens with different decimals.
- Using today's exchange rate instead of the invoice's rate, creating phantom FX gains and losses.
- Counting your own hot-to-cold moves as revenue.
- A matched tx that later reorged out leaves a phantom receipt.
- Native-coin payments have no Transfer log; they must be pulled by a block scan, which token-only reconciliation misses.

## Verification

    python3 -c "print(sum(inv) - sum(tx))"   # must be 0 (or explicitly reconciled)
    # matched + unidentified + outstanding == total in-scope transfers

Report the cut-off block, the matched/unidentified/outstanding counts, and the exact difference with its explanation.
