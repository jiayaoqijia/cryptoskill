---
name: record-crypto-payment-tax-events
description: Use when accepting crypto creates a taxable event and you must keep the records. Captures acquisition and disposal lots, the fair-market value at the time, fees, and the chain of custody.
---

# Record crypto payment tax events

Receiving crypto is usually a disposal for the payer and an acquisition for you; spending or refunding it is another event. Record lot-level facts at the moment of each transaction, because the chain can be replayed later but the fiat value at that block cannot.

## Procedure

1. For every received payment, record at the block timestamp: asset, amount, USD fair-market value (a spot price for that minute), tx hash, and the counterparty.
   `cast block $BLK --rpc-url $RPC | grep timestamp`
2. Treat the acquisition basis as the FMV at receipt plus any gas you paid to receive. Keep the lot id = tx hash.
3. For every disposal (spend, refund, swap, sale), record the lot consumed, the proceeds, and the gain/loss = proceeds minus basis.
4. Preserve the price source and its API response, not just the number; the number is unverifiable without the source.
5. Do not substitute a daily average if the jurisdiction requires the spot at the time; capture the spot.
6. Keep refunds as their own events with a link to the original receipt lot.
7. Store the export as immutable rows (append-only CSV or JSONL) with the block and price source.

## Pitfalls

- Recording only the fiat-equivalent total and losing per-lot basis, making later disposals uncalculable.
- Using the value when a payment was *credited* rather than received on-chain when a soft-confirm policy delays crediting.
- Ignoring gas paid in the native token as a disposal of that token.
- Mixing personal and business wallets and destroying the cost-basis chain.
- Backfilling prices from today's API, which may not retain historical minute data.
- A wallet that received and sent crypto internally generates disposal events even though no economic trade occurred.
- Fork tokens and airdrops create taxable acquisitions with a basis the ledger may not have captured.
- DeFi positions that wrap or stake without disposal still change the lot's character and location.
- A stablecoin swap of equal value is still a disposal of the first and an acquisition of the second worth recording.

## Verification

    python3 -c "print(proceeds - basis)"   # loss is negative and must be recorded too
    # every received lot must have exactly one row; count(lots) == count(receipts)

Report the number of lots, the total FMV at receipt, the total disposals, and the price sources used.
