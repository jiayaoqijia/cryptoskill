# DeFi DEX and Trading Venues

## Venue types

- **AMM (constant product / stable / weighted):** LPs supply both sides; fees accrue to LPs; IL and LVR are structural.
- **CLMM / concentrated liquidity:** LPs choose ranges; capital efficiency rises, but out-of-range and LVR risk rise.
- **Order book / RFQ / aggregator:** liquidity may be off-chain or routed; check the actual settlement venue.
- **Perps / derivatives DEX:** margin, funding, oracle/index, insurance fund, ADL and liquidation waterfall.
- **Intent / solver venue:** user signs an intent; solver competition and MEV capture determine execution.

## LP economics

```
LP net return = trading fees + incentives − impermanent loss/LVR − gas − MEV leakage
```

- Fee APR depends on volume, fee tier and the LP's share of active liquidity.
- Concentrated ranges can be out of range for most of the period; headline APR is not realized APR.
- Impermanent loss is the divergence between the pool and holding the assets; LVR is the adverse-selection loss to arbitrageurs.
- Emissions can make an unprofitable pool look profitable. Decompose base fees vs incentives.
- A pool with high TVL and low volume has low capital efficiency; a pool with high volume and thin depth has high slippage.
- Check whether the LP can exit at size; withdraw fees and queued liquidity.

## DEX metrics

| Metric | Definition / caution |
|---|---|
| Volume | Reported vs normalized; wash trading and incentives inflate it |
| Fees | Trader fees; split between LPs, protocol and referrers |
| TVL | Pool assets; not the same as active/executable depth |
| Volume/TVL | Turnover; high can mean efficient or mercenary |
| Fee/TVL | Capital efficiency |
| Depth | Cost to move price by 1–2%; measure at the user's size |
| Active LPs / concentration | A few LPs can control exit |
| Aggregator share | Distribution power vs protocol moat |
| Token incentives | Subsidy; separate from organic fees |

## Perps

- Margin mode, maintenance margin, liquidation price and close factor.
- Oracle/index composition; mark price vs index; stale-price and manipulation resistance.
- Funding rate, open interest, long/short skew and basis.
- Insurance fund size, ADL rules, liquidation waterfall and socialized loss.
- Counterparty/venue risk: who holds the collateral, who settles, what happens on a chain halt?
- Volume quality: wash trading, rebates, market-maker concentration.

## Competitive analysis

- Fee tier, latency, chain distribution, asset coverage, routing quality and uptime.
- Liquidity network effects: deep pools attract flow; flow attracts LPs.
- Aggregators commoditize the front end; the venue with the best fill can still lose the user.
- Fork risk: open-source code can be copied; the moat is liquidity, integrations, brand and governance.
- Token value capture: does the DEX fee switch, buyback or staking actually route fees to holders?

## Checklist

- [ ] Exact venue, pool/contracts, fee tier and chain verified.
- [ ] Volume normalized; incentives and wash trading separated.
- [ ] LP return includes fees, incentives, IL/LVR, gas and MEV.
- [ ] Depth/slippage measured at the intended size.
- [ ] Perps: oracle, insurance fund, ADL and liquidation path checked.
- [ ] Admin/upgrade/fee-switch powers mapped.
- [ ] Token value capture separated from LP economics.
- [ ] Exit tested under stress.
