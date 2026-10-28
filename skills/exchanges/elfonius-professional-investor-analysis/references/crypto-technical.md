# Crypto Technical and Market Structure

Purpose: describe market structure and timing context. It is not a valuation input and not proof of quality.

## Data contract

- Venue, pair, quote currency, price type (last / mark / index / pool mid), UTC timestamp, provider.
- Second venue or primary DEX pool cross-check; flag divergence.
- Series adjusted for splits, redenominations and token migrations.
- Pin conventions: daily UTC closes; 30d/90d/1y windows; simple versus log returns; annualisation ×√365; MA20/50/200; RSI14; ATR14.

## Dashboard

| Metric | What it tells | How to read it |
|---|---|---|
| Trend | Price vs MA20/50/200; higher highs/lows | Structure, not a forecast |
| Relative strength | Return vs TAO/BTC/sector over 7/30/90/130d | Whether the move is asset-specific or beta |
| Momentum | RSI, MACD, ROC | Short-term condition; avoid over-reading |
| Volatility | Annualised vol, ATR, max drawdown, recovery | Position sizing and risk |
| Volume | ADV, volume/market cap, volume trend | Participation, not executable liquidity |
| Liquidity | Depth ±1/2/5%, slippage at size, days-to-exit | What a real exit costs |
| Derivatives | Funding, open interest, basis, liquidation clusters | Positioning and squeeze risk; descriptive only |
| Beta/correlation | vs TAO/BTC; R² | How much is market beta |

## Relative strength

- Compute asset return and benchmark return over the same window and currency.
- If beta is high and R² is high, the move is largely market-driven; do not attribute it to project merit.
- Show alpha-versus-TAO/BTC and absolute USD return side by side.

## Liquidity and exit

- Depth at a stated UTC snapshot for the stated size; participation as % of ADV and book depth.
- Days-to-exit at a stated participation cap.
- Fees, withdrawal limits, off-ramp, transfer restrictions.
- For locked/vesting positions: no executable exit before the date; secondary sale at an assumed discount, or not executable.
- Constant-product impact is an approximation; use the shallower of the model and the observed depth.

## Derivatives

Where a perpetual exists: venue, mark/index, annualised funding with sign history, open interest and change versus price, basis, visible liquidation levels. Label all of it descriptive positioning context; never a valuation input or directional forecast.

## Backtests — two tiers

- **Default:** no backtest; technicals are descriptive; print `no validated edge claimed`.
- **Strategy evidence:** at least one bar of execution lag; fees and funding; buy-and-hold on the same window; shuffled-signal null; trade count; number of variants tested; show the result is not carried by a handful of outcomes. Below that bar: `not interpretable`.

## Sources

- Price/volume: venue APIs, CoinGecko, TradingView; on-chain pool: Taostats, DEX pool state; derivatives: venue API, Coinglass.
- Record the venue, pair, quote, price type, UTC timestamp and retrieval date for every chart.

## Red flags

- MEV/sandwich and private-mempool exposure on DEX execution; quote-asset (USDT/USDC) depeg risk.
- Illiquid book or venue concentration; nominal volume dominated by wash/self-trading.
- Perp funding extreme with rising OI; liquidation cascade risk.
- Price series not adjusted for migration/split; drawdown figures wrong.
- Technical claim presented as fundamental proof or as a validated edge.

## Reporting

- Standard/deep: at least one compressed market-structure paragraph, even when timing is not the question.
- Full technical section only when timing or strategy evidence is requested.
- Every chart carries venue, pair, price type, UTC window and source.
