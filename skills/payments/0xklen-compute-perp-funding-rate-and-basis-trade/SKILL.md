---
name: compute-perp-funding-rate-and-basis-trade
description: Use when comparing a perpetual price to spot, computing funding cost, or evaluating a cash-and-carry/basis trade: annualizes the basis and funding into a carrying yield net of fees.
---

# Compute perp funding rate and basis trade

A perpetual has no expiry, so its price is tethered to spot by a funding payment; when perp > spot longs pay shorts, and the annualized funding is the yield a delta-neutral basis trade earns.

## Procedure

1. Read both legs: perp mark and spot index. `basis = (perp - spot)/spot`. Worked example: perp 2,010, spot 2,000 → `+0.5%`.

2. Do not annualize the perp basis by 365: a perp has no expiry, so the basis is managed by funding, not convergence. Only a dated future's basis converges.

3. Funding is paid per interval (8h on most venues): `funding_apr = rate * (24/interval_hours) * 365`. A 0.01% per 8h rate = `0.0001 * 3 * 365 = 10.95%/yr`.

4. Cash-and-carry P&L: long spot + short perp captures funding while staying delta-neutral. Net = `funding_received - taker_fees - borrow_cost - slippage`. Worked: 10.95% funding − 2*(0.05% taker) − 4% USDC borrow ≈ 6.9%/yr.

5. Read the live rate rather than a dashboard:

   curl -s "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ETHUSDT" | jq '.lastFundingRate'

   Multiply by `3*365` for APR.

6. Manage the short's liquidation risk: size the perp leg to survive a 30% adverse move, or post the spot leg as collateral where the venue allows it.

## Pitfalls

- Annualizing a perp basis by 365 as if it converged at expiry — a perp has none.
- Ignoring funding sign flips: a heavily-long market pays shorts, but after a flush the same trade pays out instead of earning.
- Counting gross funding as yield: borrow cost and fees routinely eat 30–50% of it.

## Verification

    curl -s "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ETHUSDT" | jq '.lastFundingRate * 3 * 365'

Compare to the venue's displayed funding APR; a mismatch means an interval assumption is wrong.

Report basis, funding APR, net carry after fees and borrow, and the endpoint read.
