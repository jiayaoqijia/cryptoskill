# DeFi Lending and Credit

## Market map

- **Pooled money market:** shared liquidity, variable rates, reserve factor, isolation/eMode (Aave, Compound, Morpho-style).
- **Isolated market:** one collateral/debt pair, capped exposure, oracle and LLTV specific.
- **CDP stablecoin:** user mints a stablecoin against collateral; stability fee, liquidation and peg management.
- **Credit vault / RWA:** curated off-chain or structured credit; legal claim and servicer risk are central.
- **Leveraged loop:** supply, borrow, re-supply; risk compounds across legs.

## Core parameters

| Parameter | Question |
|---|---|
| LTV | How much can be borrowed at origination? |
| Liquidation threshold (LLTV) | At what collateral ratio does liquidation start? |
| Liquidation bonus | Is the keeper rewarded enough at realistic gas/depth? |
| Close factor | How much debt can one liquidation repay? |
| Reserve factor | What share of borrow interest goes to the protocol? |
| Supply/borrow caps | Can the market grow beyond safe liquidity? |
| Isolation/eMode | Are correlated assets grouped, and what does that allow? |
| Oracle | Which feed, staleness and fallback per collateral? |

## Data reconciliation

- **Deposits, borrows, TVL and available liquidity are different numbers.** Aavescan-style TVL = deposits − borrows; DefiLlama may use another chain/asset scope. Record both when they diverge; never average silently.
- Utilization = borrows / (deposits − reserves). Aggregate utilization can hide asset-level constraints; exit stress must use the asset you will actually withdraw.
- A protocol can be code-safe but not supplier-safe: a bridge/collateral failure can create bad debt while the lending contracts work.

## Health and liquidation

```
Health factor = Σ(collateral value × liquidation threshold) / debt value
Liquidation price ≈ debt / (collateral amount × liquidation threshold)  [single-collateral approximation]
Utilization = borrowed / (supplied − reserves)
```

Model the liquidation path at realistic gas and DEX depth. A position can be “overcollateralized” at the oracle price and still produce bad debt if the collateral cannot be sold at that price.

- Is the liquidation profitable for a keeper after gas, slippage and competition?
- Is the close factor partial or full? Does a partial liquidation actually improve health?
- Can a borrower front-run or grief the liquidator?
- What happens when the price gaps beyond the liquidation bonus in one block?
- Who absorbs bad debt: reserves, insurance fund, depositors, token dilution or a socialized loss?
- Can a flash loan manipulate the health factor or the oracle?

## Interest rate model

- Utilization curve, kink, base/slope1/slope2 and reserve factor.
- Does the rate behave at 0% and 100% utilization? Any overflow/negative rate?
- Is interest accrued before state changes in borrow/repay/liquidate?
- Is the time base seconds, blocks or epochs? Rounding at tiny/large positions.
- Can a large flash deposit/borrow move the rate against existing users?
- Are supply and borrow rates consistent with the fee/revenue split?

## Collateral quality

- Volatility, depth, oracle class, depeg history and correlation with debt asset.
- Recursive collateral: token accepted for itself or a wrapper priced off its own pool.
- Rehypothecation and re-use of collateral across protocols.
- Fee-on-transfer, rebasing and rebasing-wrapper accounting.
- Correlated assets (stETH/ETH, stablecoin pairs): low volatility in normal times, simultaneous shock in stress.
- Concentration: one borrower, one collateral, one market or one curator.
- For bridged/LST/RWA collateral, record the bridge verification model and issuer. A 1-of-1 DVN, single validator or unbacked bridged asset is a fail for collateral; a cap or LTV does not fix a broken bridge.

## Bad debt

Trace the loss path:

1. Collateral falls below debt.
2. Liquidation is unprofitable or unavailable.
3. Position becomes insolvent.
4. Reserve/insurance fund absorbs the loss.
5. If insufficient, depositors or token holders absorb it.

Check the reserve balance, insurance fund size, historical bad debt and the governance process for covering a shortfall. A protocol with no bad-debt history in a benign cycle has not been stress-tested.

- Separate **modeled bad debt**, **accounting provision** and **actual supplier make-whole**. A clean core exploit does not prove suppliers were repaid.
- Check whether the reserve/Umbrella/backstop actually held enough liquid assets at the time; a program's existence is not coverage.
- If a bridge or collateral failure caused the loss, the lending code can be clean while suppliers still take a haircut.

## Stablecoin and CDP specifics

- Collateral basket, mint/redeem rights, stability fee and peg mechanism.
- Oracle and liquidation design; surplus/deficit auctions.
- Reserve attestation, custodian, redemption gates and sanctions.
- Peg history in stress; dependence on a centralized issuer or a single market maker.
- Is the stablecoin’s yield real cash flow, a subsidy, or a leveraged basis trade?

## Stress tests

- Collateral −30% / −50% / −70% in one block; debt asset +10% / +30%.
- Oracle stale for 1 hour / 6 hours; one feed unavailable.
- 50% of TVL withdraws in one day; utilization 100%; borrow rate spike.
- Largest borrower exits; top collateral depegs; bridge pauses.
- Liquidation gas doubles; keeper participation halves.

Report the loss to depositors and token holders separately. A lender’s depositors and its governance token are not the same claim.
