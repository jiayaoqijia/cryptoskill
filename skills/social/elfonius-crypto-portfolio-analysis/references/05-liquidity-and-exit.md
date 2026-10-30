# 05 — Liquidity and Exit

## Purpose

Answer a different question from “what is it worth?”: **how much can be converted to cash, how fast, at what cost, and what happens under stress?**

## Inputs

- Position size in base currency.
- Daily traded volume and pool depth for the exact venue.
- Bid-ask spread; fee tier; slippage curve.
- Unstake queue, lock-up, vesting schedule, withdrawal gate.
- Stablecoin redemption terms and bridge delay.
- Market regime: normal vs stressed volume.

## Method

1. Obtain the position value and the executable volume for the exact venue.
2. Estimate exit days at 1%, 5%, and 10% participation.
3. Add lock-up, vesting, unstake, bridge, and redemption delays.
4. Re-run with stressed volume and wider spreads.
5. Report the first position that cannot exit within the mandate window.

## Exit-days estimate

`exit_days = position_value / (daily_executable_volume × participation_rate)`

Where `daily_executable_volume` is the volume you can actually access, not the global reported volume. Use at least three participation rates: 1%, 5%, 10%.

Report:

| Position | Value | Daily executable volume | 1% days | 5% days | 10% days | Gate |
|---|---:|---:|---:|---:|---:|---|
| Example | $X | $Y | X | X | X | None |

## Slippage and market impact

- Use observed order-book depth where available; otherwise a conservative range.
- Separate spread cost from impact cost.
- For long-tail tokens, global volume can be wash-traded or concentrated on one venue.
- For LP exits, include impermanent loss and withdrawal fees.
- For staking, include the unstake queue and the price exposure during the queue.

## Time locks and gates

- **Staking/unstaking:** queue length, unbonding period, slashing risk.
- **Vesting:** cliff, linear unlock, insider allocation.
- **Bridge:** finality time, pause history, wrapped-asset redemption.
- **CeFi:** withdrawal suspension, proof-of-reserves quality, jurisdictional exposure.
- **Stablecoin:** issuer redemption, market depth, depeg behavior.
- **NFT/illiquid:** floor depth, bid-ask, time-to-sale.

## Liquidity stress

Run a stressed case: 25% of normal volume, wider spreads, and a 7-day bridge/chain pause. Report the first position that cannot be exited within the mandate’s liquidity window.

## Output

1. Normal exit days for each material position.
2. Stressed exit days.
3. Liquidity bucket: cash-like, days, weeks, months, illiquid.
4. Concentration of exits in one venue or chain.
5. Liquidity discount applied to the valuation, if any.

## Failure modes

- Using market cap as liquidity.
- Using global volume when only one venue is accessible.
- Ignoring the unstake queue.
- Treating a stablecoin as instantly redeemable at par.
- Assuming a bridge works in stress.

## Sources

- CFA Institute, *Measuring and Managing Market Risk*: liquidity is not captured by VaR.
- CFA Institute, *Asset Allocation with Real-World Constraints*: liquidity needs and stressed exits.
