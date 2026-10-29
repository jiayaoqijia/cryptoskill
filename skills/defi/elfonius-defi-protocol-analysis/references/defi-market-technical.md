# DeFi Market and Technical Context

Technical analysis is timing and market-structure context, not proof of fundamental value.

## Market-data contract

For every price/volume number record:

- venue (CEX, DEX, aggregator, pool);
- pair and quote asset;
- price type (last, mark, index, pool mid, TWAP);
- UTC timestamp and block;
- provider;
- second venue or primary pool for divergence;
- adjustments for splits, redenominations, migrations and wrapped/bridged assets.

Do not present a token-denominated return as a USD return. Do not treat nominal volume as executable liquidity.

## Liquidity and exit

- Depth at ±1% and ±2%; slippage for the intended size.
- Bid/ask spread, pool fee, price impact and MEV/sandwich risk.
- Exit concentration: top LPs, top holders, locked liquidity and withdraw queues.
- CEX depth vs DEX depth; stablecoin pair vs volatile pair.
- Bridge/chain exit latency and caps.
- Stress: 25% / 50% / 100% of the position exits at once; what is the realized price?

## Volatility and drawdown

- Realized volatility (daily/weekly), maximum drawdown, drawdown duration.
- Realized vs implied volatility where options exist.
- Correlation with BTC/ETH, the relevant sector and the user's existing book.
- Tail events: depeg, exploit, chain halt, oracle failure, governance attack.
- Use ranges and scenarios, not a single point estimate.

## Perps, funding and basis

- Funding rate, predicted funding, open interest, long/short skew.
- Mark vs index; basis; annualized carry.
- Insurance fund, ADL, liquidation waterfall and venue counterparty.
- Funding is not free yield; it compensates for positioning and venue risk.
- A delta-neutral basis trade still has venue, custody, liquidation and smart-contract risk.

## Technical indicators

- Trend, relative strength, momentum, moving averages, RSI/MACD only as secondary context.
- Volume confirmation; divergence; support/resistance.
- On-chain flow and holder changes are separate evidence.
- A bullish chart cannot offset a failed gate or an unenforceable claim.
- If timing is not part of the decision, omit technicals rather than decorate the report.

## Macro and regime

- Rates, liquidity, risk appetite and the BTC/ETH cycle affect borrow demand, funding, TVL and exit.
- Stablecoin flows, regulatory regime and chain activity can change the opportunity set.
- Map macro to a named channel (borrow demand, funding, TVL, exit, compliance); do not use it as a standalone thesis.
- Label regime calls as judgment, not evidence.

## Community, news and catalysts

- Official vs unofficial channels; X, Discord, Telegram, Reddit, Farcaster.
- Engagement quality, not follower count: reply/quote ratio, bot-like repetition, real users.
- GitHub: commits, contributors, releases, issues, audit artifacts.
- Governance forum: proposals, turnout, delegate concentration, execution.
- News: independent vs sponsored, author, date; a press release is a claim.
- Catalyst calendar: unlocks, upgrades, fee switches, audits, listings, regulatory dates.
- Label sentiment as signal, never as evidence. A catalyst is not a thesis.

## Catalysts and events

- Unlocks, emissions changes, fee switches, upgrades, audits, listings, governance votes.
- Macro/regulatory dates that affect the sector or venue.
- Competitor launches, bridge migrations, chain upgrades.
- Date every catalyst and distinguish confirmed from rumored.

## Checklist

- [ ] Price/volume from at least two venues; timestamp and price type recorded.
- [ ] Depth/slippage at the intended size measured.
- [ ] Exit stress and queue/bridge latency tested.
- [ ] Volatility/drawdown/correlation described.
- [ ] Funding/basis/OI checked for perps.
- [ ] Technicals labelled as timing, not value.
- [ ] Catalysts dated and sourced.
