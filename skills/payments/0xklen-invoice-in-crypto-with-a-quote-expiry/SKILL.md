---
name: invoice-in-crypto-with-a-quote-expiry
description: Use when invoicing a customer in crypto and the price moves between issue and payment. Fixes the amount in crypto at a rate with a short expiry and states the exact unit and chain.
---

# Invoice in crypto with a quote expiry

A crypto invoice with no expiry is an open FX position: the customer pays in the right coin at the wrong rate a day later. Fix the amount in base units, tie it to a rate with a short validity window, and state chain and token unambiguously.

## Procedure

1. Choose the denomination: bill in fiat and convert, or bill in crypto. Billing in fiat with a crypto settlement amount makes the FX risk explicit and short.
2. Fetch the rate from a source with a timestamp (exchange ticker, Chainlink feed):
   `cast call $FEED "latestRoundData()(uint80,int256,uint256,uint256,uint80)" --rpc-url $RPC`.
3. Add a buffer for volatility over the payment window (e.g. +1.5% for a 24h window on ETH).
4. Convert to base units with the correct decimals and floor, never round up:
   `python3 -c "print(int(1500/(rate*1.015)*10**6))"` for a 6-decimal stablecoin.
5. Set the expiry: both a block height and a wall-clock time. After expiry the invoice is void and a new rate is issued.
6. On the invoice state the token contract address, chain id, amount in base units, destination address, and the accepted tolerance. Do not rely on ticker symbols alone.
7. Record the rate, timestamp, feed id, and expiry alongside the invoice for reconciliation and tax.

## Pitfalls

- Omitting the token contract address: two tokens share a ticker and the customer pays the worthless one.
- Using a rate with no timestamp; you cannot prove the rate at dispute time.
- Rounding the crypto amount up for the customer creates a mismatch you reconcile forever.
- A long expiry silently becomes a free option for the customer against you.
- A quote expiry in wall-clock time means nothing if the chain halts; pair it with a block-height expiry.
- Buffering the rate protects against adverse moves but can silently overcharge and look like a hidden fee.
- An invoice can be paid late and still land on-chain before your void; reconcile the on-chain time, not the receipt time.
- A stablecoin invoice still carries peg risk; the buffer for a stablecoin is depeg risk, not volatility.

## Verification

    python3 -c "print(int(1500/(rate*1.015)*10**6))"   # amount in base units
    # cross-check: amount_base_units / 10**decimals * rate ~= invoice_usd + buffer

Report the locked rate and its timestamp, the base-unit amount, the expiry, and the token contract on the invoice.
