**Original Prompt**
Given this anecdotal trading bot information, create a plan for each bot's strategy, include the tools, indicators, techniques and algorithms used to recreate each trading style.
------------------------
gave each bot $500
bot 1- copies whales. just mirrors top-5 wallets
bot 2 - contrarian. waits for crowd to be 80%+ confident and bets against
bot 3 - scalper. catches delay between binance and prediction markets
bot 4 - weather guy. trades only temperature. three meteo models, enters when all three agree
 
stats for 7 days:
day 1: scalper ahead.
+$180 others around zero
day 2: nothing interesting
day 3: contrarian caught skew on sports market.
+$740 on one trade. took the lead
day 4: scalper started dumping.
delay shrank, edge gone. $500 → $310
day 5: weather guy silent for 4 days.
then made TWO trades. both profit. +$420
day 6: whale copier steady in the middle.
no fails, no highs. boring but alive
day 7: scalper dead. $82 left
 
results:
contrarian - $1,740.
one explosion decided everything weather guy - $1,120.
two trades in a week copier - $780.
survived but unimpressive scalper - $82. corpse
 
the dumbest bot won.
it just waited for everyone to err and entered once

-----------------------

**Strategy Recreation Plans for Each Trading Bot**

The following plans outline precise, reproducible strategies derived directly from the described anecdotal behaviors. Each plan specifies the core logic, required tools and data sources, key indicators/metrics, techniques/algorithms, execution workflow, and risk controls. These are designed for implementation in a production-grade trading system (e.g., using Python with asynchronous execution via asyncio or a framework such as CCXT + Web3). All strategies assume a starting capital of $500 per bot, access to a compatible prediction-market or exchange platform with sufficient liquidity, and compliance with platform rules. Backtesting against historical data and paper-trading are recommended prior to live deployment.

### 1. Bot 1: Whale-Copying Strategy (Mirror Top-5 Wallets)
**Strategy Overview**  
The bot continuously identifies the five highest-ranked “smart-money” wallets (by historical profitability or activity) on a target blockchain and mirrors their buy/sell actions in real time with proportional sizing. The goal is steady, low-volatility participation in proven flows without independent analysis.

**Tools and Data Sources**  
- Blockchain RPC and indexing: Web3.py (Ethereum) or Solana.py + Helius/Birdeye RPC for Solana; Moralis or Bitquery streaming API for transaction monitoring.  
- Wallet-ranking service: Custom Dune Analytics SQL queries or Arkham Intelligence / Nansen API (free tier or self-hosted alternative via public labels).  
- Execution: Binance API (spot/futures) or DEX router (Uniswap V3 / Raydium) via Web3 transactions.  
- Alerting: WebSocket event listeners or TheGraph subgraphs for instant transaction detection.

**Key Indicators and Metrics**  
- Wallet score: 60 % historical PNL + 30 % win rate on last 30 trades + 10 % AUM (recalculated hourly).  
- Transaction threshold: Minimum $10,000 equivalent move by a top-5 wallet.  
- Portfolio allocation per mirrored trade: 10–20 % of bot capital, scaled to whale’s position size relative to its own holdings.

**Techniques and Algorithms**  
- Real-time monitoring engine using WebSocket subscriptions to wallet addresses.  
- Ranking algorithm (Python pandas): periodic sort of candidate wallets, maintain fixed top-5 list.  
- Mirror logic: if whale buys token X for amount A, bot executes market buy of (A / whale_portfolio_value) × bot_risk_allocation.  
- Exit rule: mirror whale’s sell or apply fixed 24-hour trailing stop (5 %).  

**Risk Controls**  
Maximum 2 concurrent positions; hard stop-loss at –15 % per trade; daily loss limit 10 % of capital. No leverage.

### 2. Bot 2: Contrarian Strategy (Bet Against 80 %+ Crowd Confidence)
**Strategy Overview**  
The bot scans prediction markets for contracts where the crowd-implied probability exceeds 80 % on one side, then takes the opposing position. It enters only on high-volume skews and holds until resolution or probability reversion, exploiting overconfidence.

**Tools and Data Sources**  
- Prediction-market API: Polymarket GraphQL subgraph or Kalshi REST/WebSocket API (for sports/weather/events).  
- Volume and order-book data: direct platform endpoints or third-party aggregator (e.g., Polymarket SDK).  
- Execution: same platform API for limit-order placement.

**Key Indicators and Metrics**  
- Crowd confidence: max(implied probability) ≥ 80 % (calculated as yes-share price for binary contracts).  
- Skew signal: ≥ 70 % of 24-hour volume on the dominant side + minimum $50,000 open interest.  
- Edge threshold: market probability deviates ≥ 12 % from a simple external benchmark (e.g., Binance odds for crypto-linked events or betting-exchange average).

**Techniques and Algorithms**  
- Continuous polling/scanning loop (every 30 seconds) across active markets.  
- Entry algorithm: if confidence ≥ 80 % and skew conditions met, place opposing limit order sized by Kelly criterion (fractional Kelly f = 0.25) capped at 30 % of capital.  
- Exit algorithm: close at 50 % probability reversion or at market resolution.  
- One-trade-at-a-time discipline (as observed in the anecdote: single +$740 winner dominated results).

**Risk Controls**  
Position size never exceeds 30 % of capital; maximum 1 open position; mandatory 24-hour cooldown after loss >10 %; no averaging down.

### 3. Bot 3: Scalping Strategy (Exploit Binance ↔ Prediction-Market Delay)
**Strategy Overview**  
The bot monitors latency between Binance spot/futures prices and correlated prediction-market contracts, entering short-duration trades when the prediction market lags observable price moves. Positions are closed within minutes once convergence occurs.

**Tools and Data Sources**  
- Binance: official WebSocket streams (ticker, depth) for sub-100 ms updates.  
- Prediction market: Polymarket or equivalent WebSocket/REST for contract price and oracle updates.  
- Latency measurement: synchronized NTP clock + timestamp differencing.

**Key Indicators and Metrics**  
- Price delta: |Binance spot – implied prediction price| > 0.4 % (adjusted for contract granularity).  
- Lag detection: time since last oracle update > 15 seconds while Binance has moved.  
- Convergence speed: historical average time-to-convergence < 5 > minutes.

**Techniques and Algorithms**  
- Dual-feed real-time engine: parallel WebSocket listeners feeding a shared order-book state.  
- Arbitrage detector (vectorized NumPy comparison every 200 ms): if delta exceeds threshold and lag confirmed, execute market order on the slower venue.  
- Exit logic: automatic market close when delta < 0.1 % > or after 10-minute hard timeout.  
- Micro-position sizing: 5–15 % of capital per scalp, targeting 0.3–0.8 % gross per trade.

**Risk Controls**  
Maximum 4 scalps per hour; per-trade stop-loss at –0.5 %; daily drawdown kill-switch at –20 % (as observed: edge evaporated, capital collapsed to $82).

### 4. Bot 4: Weather-Only Strategy (Three-Meteo-Model Consensus)
**Strategy Overview**  
The bot trades exclusively temperature contracts (daily high/low for specified cities) and enters only when three independent meteorological models produce identical directional forecasts that diverge from market pricing. No other markets are monitored.

**Tools and Data Sources**  
- Meteorological models (via free/public APIs):  
  – GFS (NOAA/Open-Meteo)  
  – ECMWF (Open-Meteo or Meteomatics free tier)  
  – ICON or HRRR (Open-Meteo aggregation)  
- Prediction-market weather contracts: Kalshi API (daily temperature buckets) or equivalent platform.  
- Execution: Kalshi REST API for order placement.

**Key Indicators and Metrics**  
- Consensus score: all three models agree on “above” or “below” the contract strike (within 0.5 °C tolerance).  
- Mispricing delta: |model-consensus probability – market implied probability| ≥ 15 %.  
- Forecast horizon: only next 1–3 days (highest model accuracy).

**Techniques and Algorithms**  
- Daily batch run at 00:00 UTC: fetch 3-model ensemble forecasts for active Kalshi cities.  
- Entry filter (strict AND logic): full consensus + mispricing delta + minimum $20,000 contract liquidity.  
- Position algorithm: fixed 25 % capital allocation per qualifying trade; direction follows model consensus.  
- Exit: hold to resolution (typical 1–2 days) or early exit if any model revises and breaks consensus.

**Risk Controls**  
Maximum 2 open positions; no leverage; daily loss limit 8 %; silent periods (no signal) are expected and enforced.

**Implementation Notes Common to All Bots**  
- Unified architecture: single Python service with modular strategy classes, shared database (PostgreSQL) for trade logging, and Prometheus monitoring.  
- Capital isolation: separate API keys/wallets per bot.  
- Backtesting framework: replay historical market data (Polymarket snapshots, Binance archives, Open-Meteo archives) to validate edge persistence.  
- The contrarian approach ultimately delivered the highest return through a single high-conviction trade, illustrating that infrequent, high-edge entries can outperform high-frequency or consensus-following styles when market inefficiencies are correctly identified.

These plans faithfully recreate the observed trading styles while adding explicit, quantifiable rules for robustness and regulatory compliance.
