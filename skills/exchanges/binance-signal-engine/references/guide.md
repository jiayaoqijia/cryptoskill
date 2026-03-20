# Binance Signal Engine — Complete Reference Guide

> Full reference documentation for the **binance-signal-engine** OpenClaw skill.
> This file is loaded on demand (Level 3) — it has zero token cost until the agent or user reads it.

---

## Table of Contents

1. [What This Tool Does](#1-what-this-tool-does)
2. [Core Philosophy: Multi-Timeframe Analysis](#2-core-philosophy-multi-timeframe-analysis)
3. [Getting Started](#3-getting-started)
4. [Command-Line Usage](#4-command-line-usage)
5. [Configuration Deep Dive](#5-configuration-deep-dive)
6. [The Three Analysis Layers Explained](#6-the-three-analysis-layers-explained)
7. [Technical Indicators: What They Are and Why They Matter](#7-technical-indicators-what-they-are-and-why-they-matter)
8. [The Signal Scoring System](#8-the-signal-scoring-system)
9. [Support and Resistance](#9-support-and-resistance)
10. [The Trade Plan](#10-the-trade-plan)
11. [Position Sizing and Risk Management](#11-position-sizing-and-risk-management)
12. [Reading the Output](#12-reading-the-output)
13. [Backtest Record Format](#13-backtest-record-format)
14. [Configuration File Reference](#14-configuration-file-reference)
15. [Common Scenarios and Examples](#15-common-scenarios-and-examples)
16. [Glossary](#16-glossary)
17. [Limitations and Disclaimers](#17-limitations-and-disclaimers)

---

## 1. What This Tool Does

This tool is an automated technical analysis engine for cryptocurrency markets. You give it a trading pair (like BTC/USDT), and it fetches real price data from an exchange (Binance by default), runs it through a battery of well-known technical indicators across three timeframes, and produces a structured verdict that includes a directional bias (bullish, bearish, or neutral), a concrete trade plan with entry, stop-loss, and take-profit prices, a position size calibrated to your account balance and risk tolerance, and a detailed list of reasons explaining every component of the score.

It does **not** execute trades automatically. It is a decision-support tool. You read the output, evaluate the reasoning, and decide whether to act.

Think of it as a disciplined analyst who checks the same set of indicators the same way every time, never gets emotional, never skips a step, and always shows their working.

---

## 2. Core Philosophy: Multi-Timeframe Analysis

Most beginners make the mistake of looking at a single chart — say, the 15-minute chart — and making decisions based only on what they see there. The problem is that a 15-minute chart can look incredibly bullish right before a massive daily downtrend resumes and crushes the trade.

Multi-timeframe analysis solves this by checking three "zoom levels" of the same market. Imagine standing at the edge of a river. The **daily chart** tells you which direction the river flows — you generally want to trade in the direction of this current, not against it. The **4-hour chart** tells you the speed and rhythm of the waves within that current — is momentum building, fading, or turning? The **15-minute chart** tells you about the ripples right at your feet — it's where you decide the exact moment to step in.

This tool formalises that idea into three layers.

The **high timeframe** (1-day candles) determines the **trend regime**. It answers: "Over the last several weeks, is this market trending up, trending down, or going sideways?" This sets the overall context for everything else.

The **mid timeframe** (4-hour candles) measures **momentum**. It answers: "Within the established trend, is the current push gaining strength or losing it?" A bullish trend with fading momentum might be about to pull back, while a bullish trend with accelerating momentum suggests continuation.

The **low timeframe** (15-minute candles) looks for **entry triggers**. It answers: "Right now, on this specific candle, is there a concrete technical signal that says the moment to enter is here?" This is where you'd see things like an RSI bouncing off oversold in an uptrend — a classic pullback-buying opportunity.

The tool scores each layer independently and then combines them. A trade signal only fires when all three layers broadly agree.

---

## 3. Getting Started

### Prerequisites

You need Python 3.8 or later installed on your system. The tool depends on three external libraries: `ccxt` for connecting to cryptocurrency exchanges and fetching price data, `pandas` for data manipulation and time-series handling, and `ta` (Technical Analysis Library) for computing indicators. You also need `numpy`, though it is installed automatically as a dependency of pandas.

Install all dependencies with:

```bash
pip install ccxt pandas ta numpy
```

No exchange API keys are needed. The tool uses only public market data endpoints (OHLCV candle data), which all major exchanges provide without authentication.

### Your First Analysis

If you installed via ClawHub, you can simply ask your OpenClaw agent:

> "Analyze BTC/USDT"

Or run the script directly from the command line:

```bash
python3 scripts/binance_signal_engine.py BTC/USDT
```

This fetches Bitcoin/USDT data from Binance across three timeframes, computes all indicators, scores the signal, plans a trade, sizes a position for a hypothetical $10,000 account risking 1% per trade, and prints a human-readable summary.

---

## 4. Command-Line Usage

### Basic Syntax

```bash
python3 scripts/binance_signal_engine.py [OPTIONS] SYMBOL [SYMBOL ...]
```

One or more trading pairs are required. Each must be in the format the exchange recognises — typically `BASE/QUOTE`, such as `BTC/USDT`, `ETH/USDT`, or `SOL/USDT`.

### Options

**`--market` or `-m`** chooses between `spot` and `futures`. Spot mode (the default) means you can only buy and sell — there is no ability to short. When the tool detects a bearish signal in spot mode, it recommends exiting or watching rather than opening a short position. Futures mode enables short-selling, meaning bearish signals can produce a full trade plan with entry, stop, and target for a short position. Example: `-m futures`.

**`--exchange` or `-e`** selects the exchange to pull data from. The default is `binance`. Any exchange supported by the ccxt library can be used in principle — `bybit`, `okx`, `kraken`, `coinbase`, etc. — though the tool has been tested primarily with Binance. Example: `-e bybit`.

**`--balance` or `-b`** sets your account balance in the quote currency (usually USDT). This is used purely for position sizing calculations. The tool does not connect to your account or access your real balance. Default is 10,000. Example: `-b 5000`.

**`--risk` or `-r`** sets the percentage of your account you're willing to lose on a single trade. A value of 1.0 means 1%, which on a $10,000 account means you're budgeting $100 of risk per trade. The tool then calculates how many units to buy/sell such that if your stop-loss is hit, you lose approximately that amount. Default is 1.0. Example: `-r 0.5` for a more conservative 0.5%.

**`--leverage` or `-l`** applies only to futures trading. A leverage of 2.0 means you can control twice the notional value with the same margin. In spot mode this should always be 1.0 (the default). Example: `-l 3` for 3x leverage on futures.

**`--config` or `-c`** points to a JSON file containing any configuration overrides. This lets you tune indicator periods, scoring weights, risk parameters, and everything else without editing the script. See the Configuration File Reference section for the full schema. Example: `-c my_settings.json`.

**`--output` or `-o`** controls the format. `summary` (the default) prints a human-readable report. `json` prints the full structured output as JSON, which is useful for piping into other tools, logging, or building dashboards. Example: `-o json`.

**`--debug`** enables verbose logging. You'll see exactly what data is being fetched, whether open candles were dropped, and other internal details. Useful for troubleshooting.

### Examples

Analyze one pair in spot mode with default settings:
```bash
python3 scripts/binance_signal_engine.py BTC/USDT
```

Analyze three pairs in futures mode with 3x leverage:
```bash
python3 scripts/binance_signal_engine.py BTC/USDT ETH/USDT SOL/USDT -m futures -l 3
```

Conservative settings — small account, low risk:
```bash
python3 scripts/binance_signal_engine.py ETH/USDT -b 2000 -r 0.5
```

Full JSON output for scripting:
```bash
python3 scripts/binance_signal_engine.py BTC/USDT -o json > btc_report.json
```

---

## 5. Configuration Deep Dive

Every tuneable parameter lives in the `Config` dataclass. When you run the tool from the command line, a few key parameters can be overridden via flags (`--balance`, `--risk`, etc.), but for full control you use a JSON config file.

The configuration is organised into logical groups.

**Exchange and market settings** control where data comes from and what kind of trading is assumed. `exchange_id` is the ccxt exchange name. `market_type` is either `"spot"` or `"futures"`.

**Timeframes and data limits** define how much history is fetched for each analysis layer. The defaults fetch 200 candles of daily, 4-hour, and 15-minute data. 200 daily candles is roughly 9-10 months of history, which gives long-term indicators like the 50-period EMA enough data to stabilise.

**Indicator periods** control the lookback windows for every technical indicator. These are standard values used widely in technical analysis — for instance, a 14-period RSI is the default proposed by its inventor, J. Welles Wilder. Changing these requires understanding what the indicator does (explained below).

**Scoring weights** are the points awarded or deducted for each signal component. These allow you to emphasise certain indicators over others. If you believe trend following is more important than momentum, you increase the trend weights. If you want to rely more heavily on RSI triggers, you increase the trigger RSI weight.

**Risk model parameters** control how stop-losses and take-profits are calculated, what minimum risk-reward ratio is acceptable, and how much slippage to budget.

**Account parameters** are used solely for position sizing. They don't connect to any real account.

---

## 6. The Three Analysis Layers Explained

### Layer 1: Trend (Daily Chart)

This layer answers the single most important question in trading: **"What is the dominant direction?"**

Trading against the trend is one of the most common ways beginners lose money. A market in a strong uptrend will have many pullbacks that look like reversals on a short-term chart — beginners sell these, and then the trend resumes and the price keeps climbing. The trend layer exists to prevent this. When the daily chart says "bullish," the tool looks for buying opportunities. When it says "bearish," the tool looks for short opportunities (futures) or recommends staying out (spot).

The trend layer uses three tools: EMA position (is price above or below the 50-day EMA?), EMA structure (is the fast EMA above or below the slow EMA?), and ADX directional strength (is the trend strong, and in which direction?). Each contributes a score, and the combined score determines the **regime** — bullish, bearish, or neutral.

### Layer 2: Momentum (4-Hour Chart)

Once you know the trend direction, you need to know whether the current move within that trend has energy. A bullish trend doesn't go straight up — it advances in waves. Momentum tells you where you are in the wave.

The momentum layer uses MACD (are the moving average convergence/divergence lines positioned bullishly, and is the histogram growing?) and Stochastics (has the market pulled back enough to offer a good risk/reward entry, and is it starting to turn back in the trend direction?).

Crucially, the momentum layer interprets stochastic signals **differently depending on the regime**. In a bullish trend, a stochastic dipping into the oversold zone and then crossing back up is a classic "buy the dip" signal and gets a high positive score. The same signal in a bearish trend gets less weight because it might just be a temporary bounce within a larger decline.

### Layer 3: Trigger (15-Minute Chart)

This is the precision layer. Even if the trend is bullish and momentum is turning up, you don't want to buy at a random moment. You want to buy when there's a concrete, observable event on a short-term chart that confirms the move is starting.

The trigger layer watches for RSI reclaiming oversold (in a bullish context, the RSI dips below the oversold threshold and then pops back above it — this suggests selling pressure has exhausted and buyers are stepping in), Bollinger Band re-entry (price falls below the lower Bollinger Band and then climbs back inside — the same exhaustion idea from a volatility perspective), and volume spikes (a sudden increase in trading volume on a bullish candle confirms that real participation is behind the move, not just random noise).

Additionally, this layer runs a **divergence detector** that checks whether price and RSI are disagreeing. If price makes a new low but RSI makes a higher low, it suggests the downward momentum is weakening even though price hasn't turned yet — a classic early warning of a reversal.

---

## 7. Technical Indicators: What They Are and Why They Matter

### Exponential Moving Average (EMA)

A moving average smooths out price data by averaging the last N closing prices. The "exponential" part means recent prices are weighted more heavily than older ones, so the EMA responds faster to new price action than a simple average would.

The tool uses three EMAs. The **fast EMA (9-period)** hugs price closely and reacts quickly. The **slow EMA (21-period)** is smoother and reacts more slowly. The **trend EMA (50-period)** is the slowest and represents the medium-term trend direction.

**Why it matters:** When price is above the 50 EMA, the market has generally been going up. When the 9 EMA is above the 21 EMA, the short-term trend is outpacing the medium-term trend — a sign of bullish momentum. When the 9 crosses below the 21, the opposite is true. These crossovers are among the most widely used signals in all of technical analysis.

**How the tool uses it:** The daily chart checks whether price is above or below the 50 EMA (±15 points) and whether the 9 EMA is above or below the 21 EMA (±10 points). These are the two highest-weight components of the trend score.

### MACD (Moving Average Convergence Divergence)

MACD is calculated by subtracting a slow EMA (26-period) from a fast EMA (12-period). The result is a line that oscillates around zero. A 9-period EMA of the MACD line itself is called the "signal line." The difference between the MACD and its signal line is plotted as a histogram.

**Why it matters:** When the MACD line is above the signal line, short-term momentum is stronger than its recent average — the move is accelerating. When the MACD line crosses above the signal line, it's a bullish momentum shift. The histogram makes this easier to see: growing bars mean momentum is building, shrinking bars mean it's fading.

**How the tool uses it:** On the 4-hour chart, the tool checks whether MACD is above or below its signal line (±10 points) and whether the histogram is growing or shrinking compared to the previous bar (±5 points).

### ADX (Average Directional Index)

ADX measures the **strength** of a trend regardless of its direction. It ranges from 0 to 100. A reading above 25 is generally considered a strong trend; below 25 suggests the market is ranging or choppy. ADX comes with two companion lines: DI+ (positive directional indicator) and DI- (negative directional indicator). When DI+ is above DI-, the trend is up; when DI- is above DI+, the trend is down.

**Why it matters:** Many indicators work well in trending markets but give false signals in sideways markets, and vice versa. ADX helps you know which type of market you're in. If ADX is below 25, trend-following strategies should be used cautiously because the market isn't actually trending.

**How the tool uses it:** On the daily chart, if ADX is above the threshold (25) and DI+ > DI-, the tool adds 10 points (strong bullish trend). If ADX > 25 and DI- > DI+, it subtracts 10 points (strong bearish trend). If ADX is below 25, no directional score is added and the tool notes that the trend is weak or ranging.

### RSI (Relative Strength Index)

RSI measures how much of the recent price movement has been upward versus downward. It ranges from 0 to 100. Traditionally, readings above 70 are "overbought" (price may have risen too far, too fast) and below 30 are "oversold" (price may have fallen too far, too fast). This tool uses slightly less extreme thresholds — 65 for overbought and 35 for oversold — because crypto markets tend to trend more aggressively than traditional markets.

**Why it matters:** RSI helps you avoid buying at the top and selling at the bottom. More importantly for this tool, the moment when RSI **crosses back** above the oversold line is a powerful signal. It means the selling has exhausted and buyers are starting to win. This is different from simply being oversold, which can persist for a long time in a downtrend.

**How the tool uses it:** On the 15-minute chart, the tool watches for RSI to cross above 35 from below (bullish reclaim, +15 points in a bullish regime) or cross below 65 from above (bearish rejection, -15 points in a bearish regime). Simply being oversold or overbought without a cross produces no trigger score — the tool waits for confirmation.

### Stochastic Oscillator

The Stochastic compares a closing price to the range of prices over a lookback period. It produces two lines: %K (the raw reading, 0-100) and %D (a smoothed average of %K). Like RSI, readings above 80 are overbought and below 20 are oversold.

**Why it matters:** The Stochastic is particularly useful for timing entries during pullbacks within a trend. In an uptrend, price often pulls back until the Stochastic dips below 20 (oversold within the trend's context), and then the next upward cross of %K above %D signals the pullback is over and the trend is resuming.

**How the tool uses it:** On the 4-hour chart, the tool looks for %K/%D crossovers in context-appropriate zones. In a bullish regime, a bullish cross below 30 gets +8 points (buying a pullback). In a bearish regime, a bearish cross above 70 gets -8 points (selling a rally). The scores are asymmetric — crossovers that agree with the regime get the full primary weight, while counter-trend crossovers get a smaller secondary weight.

### Bollinger Bands

Bollinger Bands consist of three lines: a middle line (20-period simple moving average), an upper band (middle + 2 standard deviations), and a lower band (middle - 2 standard deviations). The bands expand when volatility increases and contract when it decreases.

**Why it matters:** About 95% of price action occurs within the bands under normal conditions. When price pierces outside a band and then re-enters, it often signals that the extreme move has exhausted. Bollinger Band "re-entry" is a powerful mean-reversion signal, especially when combined with trend context.

**How the tool uses it:** On the 15-minute chart, the tool checks if price was below the lower band on the previous candle and has climbed back above it on the current candle (bullish re-entry, +10 points in bullish regime), or the mirror image for bearish re-entry. The key word is **re-entry** — price must have been outside and come back in, not just be near the band.

**Bollinger Band Width** is also calculated (the distance between upper and lower bands divided by the middle band). While not scored directly, it is computed and available in the enriched data. It is useful for identifying periods of low volatility that often precede large moves (the "Bollinger Squeeze").

### ATR (Average True Range)

ATR measures volatility by looking at the average size of recent price bars (specifically, the "true range," which accounts for gaps between bars). A Bitcoin ATR of $1,500 on the daily chart means the average daily price range has been about $1,500 recently.

**Why it matters:** ATR is the backbone of the tool's risk management. Rather than placing a stop-loss a fixed dollar amount or percentage from your entry, the tool uses ATR to adapt to current market conditions. In calm markets, stops are tighter (because normal fluctuations are smaller, so you don't need much room). In volatile markets, stops are wider (to avoid being stopped out by normal noise).

**How the tool uses it:** ATR is used to calculate stop-loss distances (1.5× ATR from entry by default), to measure how far price is from support/resistance levels (in ATR units), and as a buffer around S/R levels for entry, stop, and target placement. Nearly every price-level calculation in the trade plan is ATR-denominated, making the entire system adaptive to volatility.

### Volume and Volume Ratio

Volume is the number of units traded during a given period. The tool calculates a volume moving average (20-period average of prior bars' volume, excluding the current bar to avoid lookahead) and then a **volume ratio** — the current bar's volume divided by that average.

**Why it matters:** Volume confirms or denies price moves. A bullish candle on 2× average volume is much more significant than the same candle on 0.5× average volume. High volume means more market participants agree with the direction of the move. Low volume on a breakout is a warning that the move might fail.

**How the tool uses it:** On the 15-minute chart, if the volume ratio exceeds the spike threshold (1.5× by default), the tool checks whether the candle was bullish (close > open) or bearish (close < open). A bullish candle with a volume spike adds +5 points; a bearish one subtracts 5. A high-volume doji (open ≈ close) is noted but not scored because the direction is ambiguous.

### RSI Divergence

Divergence occurs when price and an oscillator (here, RSI) disagree about direction. **Bullish divergence** means price makes a lower low but RSI makes a higher low — selling pressure is weakening under the surface even though price hasn't turned yet. **Bearish divergence** is the mirror: price makes a higher high but RSI makes a lower high.

**Why it matters:** Divergence is one of the most reliable early warning signs of a potential trend change or at least a significant pullback. It's not a timing signal on its own (divergence can persist for many bars), but combined with other triggers it adds confidence.

**How the tool uses it:** The divergence detector scans the last 20 bars of the 15-minute chart using a simplified comparison method. It finds the lowest close (for bullish divergence) or highest close (for bearish divergence) within the window and compares the RSI at that point to the current RSI. This is a pragmatic approximation rather than a swing-point-based detector — it does not identify discrete pivot highs and lows in the way a manual chart reader would, but it catches the most prominent divergences effectively. If bullish divergence is found, +5 points are added. If bearish divergence is found, -5 points are subtracted. The specific price and RSI values are reported in the reasons.

---

## 8. The Signal Scoring System

The scoring system converts qualitative indicator readings into a single numerical score that can be compared across time and across assets.

### How Scores Are Built

Each of the three layers produces an independent score.

The **trend score** ranges from roughly -35 to +35 and reflects the daily chart's structural condition. It's the most important layer because it determines the **regime** (bullish, bearish, or neutral), and the regime changes how the other two layers interpret their signals.

The **momentum score** ranges from roughly -23 to +23 and reflects 4-hour momentum conditions.

The **trigger score** ranges from roughly -35 to +35 and reflects 15-minute entry conditions.

The **total score** is the sum of all three. It can theoretically range from about -93 to +93, though extreme readings require every single indicator to align perfectly in one direction.

### Thresholds and What They Mean

The total score maps to a bias and recommended action through four thresholds.

A score of **+30 or above** is classified as **STRONG BULLISH**. This means the daily trend is up, 4-hour momentum confirms, and the 15-minute chart shows an active entry trigger. The recommended action is **BUY**, and the `entry_ready` flag is set to true, meaning the system considers this an actionable signal right now.

A score of **+10 to +29** is classified as **BULLISH**. The trend is favorable but not all conditions are met for immediate entry. The recommended action is **WATCH LONG** — the setup is developing but isn't ready yet.

A score of **-9 to +9** is classified as **NEUTRAL**. The indicators are mixed or the market is ranging. The recommended action is **WAIT**. No trade plan is generated.

A score of **-10 to -29** is classified as **BEARISH**. In futures mode the action is **WATCH SHORT**. In spot mode it's **WATCH / EXIT BIAS** because you can't profit from declining prices in spot.

A score of **-30 or below** is classified as **STRONG BEARISH**. In futures mode the action is **SELL (SHORT)** with `entry_ready` set to true. In spot mode the action is **SELL / EXIT** — close any existing long position.

### Why This Approach

The numerical scoring system has several advantages over a simple "buy/sell" binary signal. It communicates **conviction** — a score of +55 is much more compelling than +31, even though both are "strong bullish." It reveals **which layer is contributing and which isn't** — the breakdown into trend, momentum, and trigger scores lets you see if the signal is strong across the board or if one layer is carrying all the weight. It creates a **comparable metric** for backtesting — you can ask questions like "do trades with a score above 50 have a higher win rate than those between 30 and 40?"

---

## 9. Support and Resistance

### What They Are

Support is a price level where buying pressure has historically been strong enough to stop prices from falling further. Resistance is a price level where selling pressure has historically been strong enough to stop prices from rising further. These levels matter because they tend to "repeat" — when price approaches a level where it previously bounced, there's a reasonable chance it will bounce again, because the traders who bought there before may buy again, and new traders see the historical level and place orders there.

### How the Tool Calculates Them

The tool uses a straightforward approach: support is the lowest low of the last 20 bars, and resistance is the highest high of the last 20 bars. Crucially, these are computed using `shift(1)` — meaning only **prior** bars are considered, never the current bar. This is essential for backtesting integrity; if you include the current bar, you're using information that wasn't available at the time, which makes backtested results unrealistically optimistic.

### How They're Used in Trading

Support and resistance serve three purposes in the trade plan.

For **entry placement**: in a long trade, the ideal entry is just above support (support + a small ATR buffer). The idea is that support provides a "floor" beneath your trade. If you enter near support and it holds, your potential loss is small because your stop is just below it. If you enter far above support, you have much more to lose if the trade goes wrong.

For **stop-loss placement**: the stop-loss is placed below support for longs (or above resistance for shorts), with a buffer. If support breaks, the premise of the trade is invalidated and you want to exit.

For **take-profit placement**: the take-profit is placed just below resistance for longs (or just above support for shorts). Resistance is where selling pressure is likely to appear, so you want to take your profit before that happens rather than hoping price blows through it.

The tool measures distances in ATR units rather than raw price or percentages. "Price is 0.8 ATR from support" is meaningful regardless of whether the asset is a $60,000 Bitcoin or a $0.50 altcoin.

### The MAX_ENTRY_DISTANCE_ATR Filter

If the current price is more than 1 ATR away from the relevant support/resistance level, the tool considers the entry suboptimal. In this case, even if all signal conditions are met, the plan status will be "waiting" rather than "ready," and a limit order at the ideal entry price will be suggested instead of a market order. This prevents you from chasing a move that has already extended far from its support base.

---

## 10. The Trade Plan

When the signal score crosses a threshold and a tradeable side is identified, the tool generates a concrete trade plan. Here's what each field means and how it's calculated.

### Side

Either `long` (you expect price to go up and want to buy) or `short` (you expect price to go down and want to sell, futures only). In spot mode, bearish signals don't produce a trade plan because you can't open a short position — the tool recommends exiting any existing long instead.

### Entry

The price at which you would open the position. If the trade is `entry_ready` (strong signal and price is near the relevant S/R level), the entry is the current market price (plus a small slippage buffer for longs, minus for shorts) and the entry type is `market`. If the setup is valid but price hasn't pulled back to the ideal zone yet, the entry is a calculated limit price near support (for longs) or resistance (for shorts) and the entry type is `limit`.

### Stop Loss

The price at which you exit the trade to limit your loss if the market moves against you. This is the most important field in the plan. The tool calculates two candidate stop levels and uses the more protective one.

The **ATR-based stop** is placed 1.5× ATR from the entry. This ensures the stop accounts for the asset's current volatility — you're not placing a stop so tight that normal price noise triggers it, but not so wide that you take an unnecessarily large loss.

The **structure-based stop** is placed just below support (for longs) or just above resistance (for shorts), with an ATR buffer. The logic is: if the key S/R level breaks, the trade thesis is invalid.

For a long trade, the tool takes the **lower** of the two candidates (more protective). For a short trade, it takes the **higher** of the two (more protective).

### Take Profit

The price at which you exit to lock in your gain. Like the stop-loss, the tool considers two candidates.

The **RR-based target** is calculated by multiplying the risk (entry-to-stop distance) by the configured risk-reward ratio (default 2.0). If your stop is $100 away from entry, the RR target is $200 in profit from entry. This ensures that winning trades are always worth at least twice as much as losing trades, which means you can be wrong more often than you're right and still be profitable.

The **structure-based target** is placed just before the nearest resistance (for longs) or just above the nearest support (for shorts). The idea is that even if the theoretical RR target is further away, there's no point setting a target beyond a level where the market is likely to reverse.

The tool uses the structure-based target when available. If the structure target is closer than the RR target, a note is added warning that "resistance caps target before ideal RR." This is important information — it means the trade has less profit potential than the risk model would ideally want.

### Effective Risk-Reward Ratio

This is the actual reward-to-risk ratio of the planned trade, accounting for S/R adjustments. If the entry is at $100, the stop at $98 (risk of $2), and the take-profit at $105.50 (reward of $5.50), the effective RR is 2.75. The tool requires a minimum effective RR of 1.2 (configurable). If the nearest resistance or support caps the target so severely that the RR drops below this threshold, the trade is marked as `reject` and flagged as not tradeable.

### Plan Status

The `plan_status` field summarises the trade plan's readiness. There are five possible values.

**`ready`** means all signal conditions are met, price is near the ideal entry zone, and the risk-reward ratio is acceptable. You could act on this plan now. The entry type will be `market`, meaning a market order at the current price (plus slippage buffer).

**`waiting`** means the signal is valid and the trade plan is sound, but price hasn't reached the ideal entry zone yet. The entry type will be `limit` at a calculated price near the relevant support (for longs) or resistance (for shorts). The idea is to let the market come to you rather than chasing.

**`reject`** means a directional side was identified and a plan was attempted, but the math doesn't work. The most common cause is that the nearest support or resistance level caps the profit target so severely that the effective risk-reward ratio falls below the minimum acceptable threshold (default 1.2). The tool is saying: "I agree with the direction, but the reward doesn't justify the risk at these levels." You should wait for either a better entry (pullback closer to support for longs) or for resistance to break, opening up more room.

**`none`** means no trade plan was generated at all. This happens in two cases. First, when the signal is **neutral** (score between -9 and +9), the tool has no directional conviction and no side to trade — the output will note "No actionable side." Second, when the signal is **bearish but you're in spot mode**, the tool cannot generate a short plan because spot markets don't support short selling — the output will note "Spot mode: bearish = exit-only, no short plan." In both cases, there is no entry, stop-loss, take-profit, or position size because there is no trade. If you hold an existing long position and the status is "none" due to a bearish reading, treat the signal reasons as guidance for whether to reduce or close that position.

**`invalid`** means the tool attempted to build a plan but the underlying data was insufficient or contradictory. This can happen if the ATR is zero or missing (meaning volatility couldn't be calculated, often because there aren't enough candles), if the calculated risk distance is zero or negative (entry and stop-loss ended up at the same price or inverted), or if critical price data is missing. This status is rare and usually indicates a data issue with the specific trading pair rather than a flaw in the logic.

---

## 11. Position Sizing and Risk Management

### The Core Principle

Position sizing answers: "How much should I buy or sell?" Most beginners either bet the same dollar amount every time (which doesn't account for the varying riskiness of different trades) or bet based on gut feeling (which leads to oversized positions on the trades they feel most confident about — often the ones most likely to fail due to overconfidence).

This tool uses **fixed-fractional risk sizing**. You decide in advance what percentage of your account you're willing to lose on any single trade (default: 1%). The tool then calculates the exact position size such that if your stop-loss is hit, you lose that amount and no more.

### The Calculation

The formula is straightforward. Your **risk budget** is your account balance times your risk percentage. On a $10,000 account with 1% risk, that's $100.

The **stop distance** is the absolute price difference between your entry and your stop-loss. If you enter a long at $100 and your stop is at $97, the stop distance is $3.

The **units** you can trade are your risk budget divided by the stop distance. $100 / $3 = 33.33 units.

Your **notional exposure** is the units times the entry price. 33.33 × $100 = $3,333.

### Notional Cap

There's a secondary check: the tool caps your notional exposure as a percentage of your account (default: 100%). On a $10,000 account without leverage, you can't hold a position worth more than $10,000. With 3× leverage, you could hold up to $30,000.

If the risk-based position size would result in a notional exposure exceeding the cap, the position is reduced. The `capped_by_notional_limit` field in the output tells you when this happens.

### Exchange Precision

Exchanges have rules about the minimum trade size and the granularity of order quantities (lot-size step). You can't buy 1.23456789 BTC if the exchange only allows increments of 0.00001. The tool reads these rules from the exchange and rounds your position size accordingly. It also checks the exchange's minimum notional value and warns if your calculated position is below it.

### Output Fields Explained

The position sizing output includes: `units` (how many units to trade), `notional` (the total value of the position in quote currency), `risk_budget` (how much you've allocated to lose on this trade), `actual_risk` (the precise dollar loss if the stop is hit, which may differ slightly from the budget due to rounding), `potential_reward` (the dollar gain if the take-profit is hit), `position_pct_of_account` (what fraction of your account this position represents), and `capped_by_notional_limit` (whether the notional cap forced a smaller position).

---

## 12. Reading the Output

### Summary Mode

When you run the tool with default output, you'll see something like this:

```
============================================================
  BTC/USDT  |  SPOT  |  Score: 38.0
============================================================
  Regime : bullish
  Bias   : STRONG BULLISH
  Action : BUY
  Trend  : +25.0  |  Momentum: +10.0  |  Trigger: +3.0

  Signal Reasons:
    • Price > EMA50 (1D)
    • EMA9 > EMA21 (1D)
    • ADX=32.4 strong bullish trend
    • MACD > Signal (4H)
    • MACD histogram rising (4H)
    • RSI still oversold (32.1) — waiting for reclaim
    • Price re-entered above lower BB

  Trade Plan (WAITING):
    Side       : long
    Entry_type : limit
    Entry      : 84250.00
    Stop_loss  : 82100.00
    Take_profit: 88550.00
    Effective_risk_reward: 2.00

  Position Size:
    Units      : 0.04651163
    Notional   : $3,918.60
    Risk Budget: $100.00
============================================================
```

Here's how to read it.

The header shows the symbol, market mode, and total score. A score of 38 is above the strong bullish threshold of 30, hence the "STRONG BULLISH" bias and "BUY" action.

The sub-scores show where the conviction comes from. Trend is +25 (almost maxed out — the daily chart is solidly bullish). Momentum is +10 (positive but not extreme). Trigger is +3 (the 15-minute entry conditions are only partially met). This tells you the trade idea is strong from a top-down perspective but the precise entry moment hasn't arrived yet — which is why the plan status is "WAITING" rather than "READY."

The reasons list every scored component in plain English, letting you audit the logic.

The trade plan shows a limit entry at $84,250, a stop-loss at $82,100, and a take-profit at $88,550. The effective risk-reward is 2.00. The `entry_type` of `limit` and plan status of `WAITING` indicate that the signal favours a long but price hasn't reached the ideal entry zone yet — you would place a limit order and wait.

The position size shows that on a $10,000 account risking 1% ($100), you'd buy 0.0465 BTC worth about $3,919. If the stop is hit, you lose approximately your $100 risk budget.

When a plan is not tradeable, the summary prints the plan status and any notes explaining why — for example, "Rejected: effective RR < min 1.20" or "No actionable side / Spot restrictions applied."

### JSON Mode

JSON output contains the same information in a structured format with four top-level sections: `signal`, `trade_plan`, `position_size`, and `backtest_row`. This is useful for piping into other tools, logging to a file, or building dashboards. Every field described in this guide appears in the JSON under its corresponding section.

---

## 13. Backtest Record Format

The `backtest_row` is a flat dictionary included in the JSON output, designed to be collected over time (one row per signal) and assembled into a DataFrame or CSV for analysis.

The current version outputs the following fields:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 timestamp of the 15-minute trigger bar |
| `symbol` | The trading pair, e.g. `BTC/USDT` |
| `close_15m` | Closing price of the 15-minute bar |
| `score_total` | Composite signal score |
| `bias` | Directional bias string (e.g. `STRONG BULLISH`) |
| `plan_side` | Trade direction: `long`, `short`, or `null` |
| `plan_tradeable` | Whether the plan passed all filters (`true`/`false`) |
| `plan_effective_rr` | Effective risk-reward ratio of the plan, or `null` |
| `size_units` | Position size in asset units, or `null` |

This is a compact snapshot suitable for quick filtering and statistical analysis. For example, you can collect rows over time and ask questions like "what percentage of `score_total >= 40` signals with `plan_tradeable == true` would have been profitable?" by comparing the entry direction against subsequent price action.

If you need a richer backtest record with per-indicator values from all three timeframes, you can extend the `BacktestFormatter.build()` method in the script — all indicator columns are available on the enriched DataFrames passed to it.

---

## 14. Configuration File Reference

Create a JSON file with any of the following keys. Only include the ones you want to override — all others keep their defaults.

```json
{
    "exchange_id": "binance",
    "market_type": "spot",

    "timeframes": {
        "high": "1d",
        "mid": "4h",
        "low": "15m"
    },
    "limits": {
        "high": 200,
        "mid": 200,
        "low": 200
    },

    "ema_fast": 9,
    "ema_slow": 21,
    "ema_trend": 50,

    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,

    "adx_period": 14,
    "adx_trend_threshold": 25.0,

    "rsi_period": 14,
    "rsi_oversold": 35.0,
    "rsi_overbought": 65.0,

    "stoch_window": 14,
    "stoch_smooth": 3,
    "stoch_oversold": 20.0,
    "stoch_overbought": 80.0,

    "bb_window": 20,
    "bb_std": 2.0,

    "atr_period": 14,

    "volume_ma_period": 20,
    "volume_spike_threshold": 1.5,

    "sr_lookback": 20,
    "sr_entry_buffer_atr": 0.10,
    "sr_stop_buffer_atr": 0.25,
    "sr_target_buffer_atr": 0.10,
    "max_entry_distance_atr": 1.0,

    "weak_signal_threshold": 10.0,
    "strong_signal_threshold": 30.0,

    "weight_trend_ema_position": 15.0,
    "weight_trend_ema_cross": 10.0,
    "weight_trend_adx": 10.0,
    "weight_momentum_macd_cross": 10.0,
    "weight_momentum_macd_hist": 5.0,
    "weight_momentum_stoch_primary": 8.0,
    "weight_momentum_stoch_secondary": 4.0,
    "weight_trigger_rsi": 15.0,
    "weight_trigger_bb": 10.0,
    "weight_trigger_volume": 5.0,

    "atr_sl_multiplier": 1.5,
    "risk_reward_ratio": 2.0,
    "min_acceptable_rr": 1.2,
    "slippage_buffer_pct": 0.05,

    "account_balance": 10000.0,
    "account_risk_pct": 1.0,
    "max_position_notional_pct": 100.0,
    "leverage": 1.0,

    "cooldown_bars": 4
}
```

**Note on `cooldown_bars`:** This parameter is defined in the configuration schema but is not currently used by the signal engine. It is reserved for a future version that will enforce a minimum number of bars between consecutive signals on the same symbol, preventing rapid-fire entries during choppy conditions. You can set it now and it will be picked up when the feature is implemented.

A few tuning suggestions for different styles. **Conservative / swing trading**: increase `ema_trend` to 100, raise `strong_signal_threshold` to 40, raise `min_acceptable_rr` to 2.0, lower `account_risk_pct` to 0.5. **Aggressive / scalping**: decrease `ema_trend` to 20, lower `strong_signal_threshold` to 25, lower `min_acceptable_rr` to 1.0, raise `account_risk_pct` to 2.0 (higher risk). **Ranging / mean-reversion focus**: lower `adx_trend_threshold` to 15, increase `weight_trigger_rsi` and `weight_trigger_bb`, decrease trend weights.

---

## 15. Common Scenarios and Examples

### Scenario 1: Strong Uptrend With a Clean Pullback Entry

The daily chart shows price well above the 50 EMA, the 9 EMA is above the 21 EMA, and ADX is at 35 with DI+ > DI-. The trend score is +35 (maximum). The 4-hour MACD is above its signal line and the histogram is growing. The 4-hour Stochastic dipped below 30 and just crossed back up — a classic pullback buy signal. The momentum score is +23. On the 15-minute chart, RSI just crossed above 35 from below, and price re-entered the lower Bollinger Band from outside. The volume on this candle is 2× the average. The trigger score is +30.

Total score: +88. Bias: STRONG BULLISH. Action: BUY. The plan shows a market entry, a stop just below 15m support (also backed by ATR), and a target just below 15m resistance. Effective RR: 2.4. Position sized for 1% risk.

This is the ideal case — every layer agrees, and the tool recommends immediate action.

### Scenario 2: Bullish Trend, But Trigger Not Ready

The daily and 4-hour charts are bullish (similar to above), but the 15-minute RSI is at 52 (not oversold, so no reclaim trigger), price is inside the Bollinger Bands (no re-entry signal), and volume is average. The trend and momentum scores are high, but the trigger score is near zero.

Total score: +25. Bias: BULLISH. Action: WATCH LONG. The plan is generated with a limit entry near support, status: WAITING. The tool is saying: "The trend and momentum are in your favor, but there's no immediate catalyst on the short timeframe. Place a limit order near support and wait for price to come to you."

### Scenario 3: Mixed Signals — Neutral

The daily chart shows price above the 50 EMA (+15) but the 9 EMA just crossed below the 21 EMA (-10), and ADX is at 18 (no directional score). Trend score: +5 — not enough for a bullish regime; the regime is neutral. The 4-hour MACD is below its signal line (-10), histogram is rising (+5). Momentum score: -5. The 15-minute chart shows nothing remarkable. Trigger score: 0.

Total score: 0. Bias: NEUTRAL. Action: WAIT. No trade plan is generated. The tool is saying: "The indicators are contradicting each other. The daily structure is weakening, momentum is mixed, and there's no trigger. Sit on your hands."

### Scenario 4: Bearish Signal in Spot Mode

Everything is negative. Daily trend is down, 4-hour momentum confirms, 15-minute shows a bearish trigger. Total score: -45. Bias: STRONG BEARISH. But you're in spot mode. Action: SELL / EXIT. No short trade plan is generated. The tool is saying: "If you have an open long, close it. There's nothing to buy here."

### Scenario 5: Trade Rejected Due to Poor Risk-Reward

The signal is strong bullish (+35), but the current price is very close to resistance — meaning the take-profit has almost no room. The tool calculates the entry-to-target distance, divides by the entry-to-stop distance, and gets an effective RR of 0.8. This is below the minimum acceptable RR of 1.2.

Plan status: REJECT. Tradeable: false. The tool is saying: "The signal is fine, but the math doesn't work. You'd be risking more than you stand to gain. Wait for a pullback that gives you a better entry, or wait for resistance to be broken."

---

## 16. Glossary

**ATR (Average True Range):** A measure of how much price moves per bar on average. Used as a yardstick for stop-loss, target, and buffer distances.

**Backtest:** Running a trading strategy on historical data to see how it would have performed. The backtest_row output is designed for this purpose.

**Bias:** The tool's directional assessment — STRONG BULLISH, BULLISH, NEUTRAL, BEARISH, or STRONG BEARISH.

**Bollinger Bands:** Volatility envelopes around a moving average. Price outside the bands often reverts back inside.

**Candle / Candlestick:** A bar representing a time period's open, high, low, and close prices.

**Divergence:** When price and an indicator move in opposite directions, suggesting the current trend may be weakening.

**EMA (Exponential Moving Average):** A smoothed price average that weights recent data more heavily.

**Entry:** The price at which you open a trade.

**Futures:** A market where you can profit from falling prices (short selling) using leverage.

**Leverage:** Borrowing to control a larger position than your capital alone would allow. Amplifies both gains and losses.

**Limit Order:** An order to buy or sell at a specific price or better. It waits in the order book until the market reaches your price.

**Long:** Buying an asset expecting its price to rise.

**MACD:** An indicator comparing two EMAs to measure momentum and trend changes.

**Market Order:** An order to buy or sell immediately at the best available price.

**Notional:** The total market value of a position. 0.5 BTC at $80,000 has a notional value of $40,000.

**OHLCV:** Open, High, Low, Close, Volume — the five data points that describe each candle.

**Regime:** The trend classification determined by the daily chart — bullish, bearish, or neutral.

**Resistance:** A price level where selling pressure tends to emerge, creating a "ceiling."

**Risk-Reward Ratio (RR):** The potential profit divided by the potential loss. An RR of 2.0 means you stand to make twice what you stand to lose.

**RSI (Relative Strength Index):** A momentum oscillator measuring the speed and magnitude of recent price changes, scaled 0-100.

**Short:** Selling an asset you don't own (borrowing it) expecting its price to fall, then buying it back at a lower price. Only available in futures.

**Slippage:** The difference between the price you expect to get and the price you actually get when a market order executes.

**Spot:** A market where you buy and sell the actual asset. You can only profit from rising prices.

**Stochastic Oscillator:** A momentum indicator comparing the closing price to the price range over a lookback period.

**Stop-Loss:** An order to automatically exit a trade at a specified price to limit losses.

**Support:** A price level where buying pressure tends to emerge, creating a "floor."

**Take-Profit:** An order to automatically exit a trade at a specified price to lock in gains.

**Timeframe:** The duration each candle represents. "1d" = one day per candle, "4h" = four hours, "15m" = fifteen minutes.

**Volume:** The quantity of an asset traded during a given time period. Higher volume = more market participation and conviction.

---

## 17. Limitations and Disclaimers

**This tool does not guarantee profitable trading.** No technical analysis system does. Markets can behave irrationally for longer than you can stay solvent. Technical indicators are probabilistic tools, not crystal balls.

**Past performance is not indicative of future results.** Backtesting this system on historical data may show profitable results, but market conditions change. Strategies that worked in a trending bull market may fail in a choppy, ranging market.

**The support/resistance calculation is simplistic.** Rolling min/max captures obvious levels but misses volume-weighted zones, pivot point clusters, and multi-timeframe confluence. Professional traders typically layer multiple S/R methods. Consider these levels as a starting point, not gospel.

**The divergence detector is a simplified approximation.** It compares the current bar's price and RSI against the extreme point within a 20-bar window, rather than identifying discrete swing highs and swing lows. This catches prominent divergences effectively but may miss subtler patterns or occasionally flag coincidental alignments. For higher-confidence divergence signals, consider layering this with manual chart inspection.

**The tool does not account for fundamental analysis.** Major news events, regulatory changes, exchange hacks, protocol upgrades, and macroeconomic shifts can override any technical signal instantly. Always be aware of the news environment.

**The tool does not manage open positions.** It tells you where to enter, where to stop, and where to take profit, but it does not monitor your trade, trail your stop, take partial profits, or adjust for changed conditions after entry. Managing the trade is your responsibility.

**Latency and slippage.** The tool works with closed candle data. By the time you see the output and act, the market may have moved. The slippage buffer helps, but in fast markets or for illiquid pairs, the actual execution price may differ significantly from the plan.

**Exchange-specific quirks.** Different exchanges have different fee structures, minimum order sizes, and market rules. The tool reads some of these from the exchange metadata, but you should verify important details yourself before placing real trades.

**Risk management is your responsibility.** The 1% risk-per-trade default is a widely recommended starting point, but it assumes you're only taking one or two trades at a time. If you run this tool on ten symbols simultaneously and they're all correlated (as crypto assets often are), you might have 10% of your account at risk, not 1%. Think about portfolio-level risk, not just per-trade risk.

**Start with paper trading.** Before risking real money on any system, run it in simulation mode for at least several weeks. Record every signal, note whether it would have been profitable, and build confidence (or discover flaws) without financial consequences.
```

---