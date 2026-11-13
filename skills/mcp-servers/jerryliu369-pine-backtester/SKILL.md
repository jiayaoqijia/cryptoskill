<!--
  Imported from: https://github.com/TradersPost/pinescript-agents
  Source Path: skills/pine-backtester/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: pine-backtester
description: Implements comprehensive backtesting and performance metrics. Use when adding trade analysis, equity curves, or statistical validation.
allowed-tools: Read, Edit, Grep, Glob
---

# Pine Script Backtester

Specialized in adding comprehensive testing and validation capabilities to Pine Script indicators and strategies.

## Core Responsibilities

### Strategy Performance Metrics
- Win rate and profit factor
- Maximum drawdown analysis
- Sharpe and Sortino ratios
- Risk-adjusted returns
- Trade distribution analysis

### Indicator Accuracy Testing
- Signal accuracy measurements
- False positive/negative rates
- Lag analysis
- Divergence detection accuracy
- Multi-timeframe validation

### Statistical Analysis
- Monte Carlo simulations
- Walk-forward analysis
- Confidence intervals
- Statistical significance tests
- Correlation analysis

## Pine Script v6 2025 Backtesting Features

### Enhanced Reporting (August 2025: 40,960 char strings)

Now possible: comprehensive multi-section reports:
```pinescript
// Build detailed performance report (up to 40K chars!)
var string fullReport = ""
fullReport := "═══════════════════════════════════════════\n"
fullReport += "           COMPREHENSIVE BACKTEST REPORT    \n"
fullReport += "═══════════════════════════════════════════\n\n"
fullReport += "PERFORMANCE SUMMARY\n"
fullReport += "───────────────────\n"
fullReport += "Win Rate: " + str.tostring(winRate, "#.##") + "%\n"
fullReport += "Profit Factor: " + str.tostring(pf, "#.##") + "\n"
fullReport += "Sharpe Ratio: " + str.tostring(sharpe, "#.##") + "\n\n"
fullReport += "TRADE DISTRIBUTION\n"
fullReport += "───────────────────\n"
// ... Can include much more detailed analysis
```

### Use `for...in` for Trade Arrays (March 2025)

The preferred way to iterate over trade data arrays:

```pinescript
// ✅ BEST: Use for...in for arrays (safe, clean)
for tradeReturn in tradeReturns
    // Process each return directly

// ✅ BEST: With index when needed
for [i, tradeReturn] in tradeReturns
    // Have both index and value

// ❌ AVOID: Traditional for with dynamic boundary
for i = 0 to array.size(tradeReturns) - 1
    array.push(newArray, processedValue)  // Can infinite loop!

// ✅ FALLBACK: If traditional for needed, cache boundary
arrSize = array.size(tradeReturns)
for i = 0 to arrSize - 1
    // Safe processing
```

### Conditional Backtest Settings (July 2025)

Use `active` parameter to show relevant settings:
```pinescript
showAdvancedMetrics = input.bool(false, "Show Advanced Metrics", group="Backtest")
sharpeRiskFreeRate = input.float(0.02, "Risk-Free Rate",
    group="Backtest",
    active=showAdvancedMetrics,  // Only show when advanced enabled
    tooltip="Annual risk-free rate for Sharpe calculation")
```

### Visual Line Styles (September 2025)

Differentiate backtest visualization with line styles:
```pinescript
// Primary metrics: solid
plot(strategy.equity, "Equity", color.blue, linestyle=plot.linestyle_solid)
// Benchmarks: dashed
plot(benchmarkEquity, "Benchmark", color.gray, linestyle=plot.linestyle_dashed)
// Projections: dotted
plot(projectedEquity, "Projected", color.yellow, linestyle=plot.linestyle_dotted)
```

## ⚠️ UDT-First Trade Tracking

**For comprehensive trade analysis, use UDTs to track individual trades.**

### Trade UDT Pattern

```pinescript
// Define Trade UDT for detailed tracking
type Trade
    // Time coordinates (for historical analysis)
    int entryTime
    int exitTime
    int entryBar
    int exitBar

    // Trade data
    float entryPrice
    float exitPrice
    float positionSize
    bool isLong
    string exitReason

    // Calculated metrics
    float pnl = 0.0
    float pnlPercent = 0.0
    int duration = 0

    // Visualization (optional)
    line tradeLine = na
    label entryLabel = na
    label exitLabel = na

// Methods for trade analysis
method calculate(Trade this) =>
    this.duration := this.exitBar - this.entryBar
    if this.isLong
        this.pnl := (this.exitPrice - this.entryPrice) * this.positionSize
        this.pnlPercent := ((this.exitPrice - this.entryPrice) / this.entryPrice) * 100
    else
        this.pnl := (this.entryPrice - this.exitPrice) * this.positionSize
        this.pnlPercent := ((this.entryPrice - this.exitPrice) / this.entryPrice) * 100

method draw(Trade this, color winColor, color loseColor) =>
    tradeColor = this.pnl >= 0 ? winColor : loseColor
    // Use xloc.bar_time for unlimited lookback!
    this.tradeLine := line.new(this.entryTime, this.entryPrice,
         this.exitTime, this.exitPrice,
         xloc=xloc.bar_time, color=tradeColor, width=2)

// Storage
var array<Trade> completedTrades = array.new<Trade>()
var Trade currentTrade = na
```

### Trade Analysis with for...in

```pinescript
// Analyze all trades using for...in
if barstate.islastconfirmedhistory
    totalPnl = 0.0
    wins = 0
    losses = 0
    totalDuration = 0

    for trade in completedTrades
        totalPnl += trade.pnl
        if trade.pnl >= 0
            wins += 1
        else
            losses += 1
        totalDuration += trade.duration

    winRate = array.size(completedTrades) > 0 ? (wins / array.size(completedTrades)) * 100 : 0
    avgDuration = array.size(completedTrades) > 0 ? totalDuration / array.size(completedTrades) : 0
```

### Trade Distribution with UDT Arrays

```pinescript
// Categorize trades by exit reason
var array<Trade> stopLossTrades = array.new<Trade>()
var array<Trade> takeProfitTrades = array.new<Trade>()
var array<Trade> timeoutTrades = array.new<Trade>()

// When trade closes, categorize it
if tradeJustClosed
    if currentTrade.exitReason == "SL"
        array.push(stopLossTrades, currentTrade)
    else if currentTrade.exitReason == "TP"
        array.push(takeProfitTrades, currentTrade)
    else
        array.push(timeoutTrades, currentTrade)

// Analyze by category
if barstate.islast
    slCount = array.size(stopLossTrades)
    tpCount = array.size(takeProfitTrades)
    // ... display distribution
```

### Visualize Trade History with xloc.bar_time

```pinescript
// Draw all historical trades (no 5000 bar limit!)
if barstate.islast and showTradeHistory
    for trade in completedTrades
        trade.draw(color.green, color.red)
```

## Backtesting Components

### 1. Comprehensive Strategy Metrics Table
```pinescript
// Strategy Performance Metrics
var table metricsTable = table.new(position.bottom_right, 2, 15, bgcolor=color.new(color.black, 90))

if barstate.islastconfirmedhistory
    wins = strategy.wintrades
    losses = strategy.losstrades
    totalTrades = wins + losses
    winRate = totalTrades > 0 ? (wins / totalTrades) * 100 : 0

    avgWin = strategy.grossprofit / math.max(wins, 1)
    avgLoss = math.abs(strategy.grossloss) / math.max(losses, 1)
    profitFactor = avgLoss > 0 ? avgWin / avgLoss : 0

    // Drawdown calculation
    var float maxEquity = strategy.initial_capital
    var float maxDrawdown = 0.0
    currentEquity = strategy.equity
    if currentEquity > maxEquity
        maxEquity := currentEquity
    drawdown = ((maxEquity - currentEquity) / maxEquity) * 100
    maxDrawdown := math.max(maxDrawdown, drawdown)

    // Populate table
    table.cell(metricsTable, 0, 0, "METRIC", bgcolor=color.gray, text_color=color.white)
    table.cell(metricsTable, 1, 0, "VALUE", bgcolor=color.gray, text_color=color.white)

    table.cell(metricsTable, 0, 1, "Total Trades", text_color=color.white)
    table.cell(metricsTable, 1, 1, str.tostring(totalTrades), text_color=color.yellow)

    table.cell(metricsTable, 0, 2, "Win Rate", text_color=color.white)
    table.cell(metricsTable, 1, 2, str.tostring(winRate, "#.##") + "%", text_color=winRate > 50 ? color.green : color.red)

    table.cell(metricsTable, 0, 3, "Profit Factor", text_color=color.white)
    table.cell(metricsTable, 1, 3, str.tostring(profitFactor, "#.##"), text_color=profitFactor > 1 ? color.green : color.red)

    table.cell(metricsTable, 0, 4, "Max Drawdown", text_color=color.white)
    table.cell(metricsTable, 1, 4, str.tostring(maxDrawdown, "#.##") + "%", text_color=maxDrawdown < 20 ? color.green : color.red)

    table.cell(metricsTable, 0, 5, "Net Profit", text_color=color.white)
    netProfit = strategy.netprofit
    table.cell(metricsTable, 1, 5, str.tostring(netProfit, "#,###.##"), text_color=netProfit > 0 ? color.green : color.red)
```

### 2. Trade Distribution Analysis
```pinescript
// Trade distribution tracking
var array<float> tradeReturns = array.new<float>()
var array<int> tradeDurations = array.new<int>()
var int tradeStartBar = 0

if strategy.position_size != strategy.position_size[1]
    if strategy.position_size != 0
        // Trade entry
        tradeStartBar := bar_index
    else
        // Trade exit
        tradeReturn = (strategy.equity - strategy.equity[bar_index - tradeStartBar]) / strategy.equity[bar_index - tradeStartBar] * 100
        array.push(tradeReturns, tradeReturn)
        array.push(tradeDurations, bar_index - tradeStartBar)

// Calculate distribution stats
if barstate.islastconfirmedhistory and array.size(tradeReturns) > 0
    avgReturn = array.avg(tradeReturns)
    stdReturn = array.stdev(tradeReturns)
    medianReturn = array.median(tradeReturns)
    maxReturn = array.max(tradeReturns)
    minReturn = array.min(tradeReturns)

    // Display distribution
    table.cell(metricsTable, 0, 6, "Avg Return", text_color=color.white)
    table.cell(metricsTable, 1, 6, str.tostring(avgReturn, "#.##") + "%", text_color=avgReturn > 0 ? color.green : color.red)

    table.cell(metricsTable, 0, 7, "Std Dev", text_color=color.white)
    table.cell(metricsTable, 1, 7, str.tostring(stdReturn, "#.##") + "%", text_color=color.yellow)
```

### 3. Sharpe Ratio Calculation
```pinescript
// Sharpe Ratio calculation
var array<float> returns = array.new<float>()
var float previousEquity = strategy.initial_capital

if bar_index > 0
    currentReturn = (strategy.equity - previousEquity) / previousEquity
    array.push(returns, currentReturn)
    if array.size(returns) > 252  // Keep 1 year of daily returns
        array.shift(returns)
    previousEquity := strategy.equity

if barstate.islastconfirmedhistory and array.size(returns) > 30
    avgReturn = array.avg(returns) * 252  // Annualized
    stdReturn = array.stdev(returns) * math.sqrt(252)  // Annualized
    riskFreeRate = 0.02  // 2% risk-free rate
    sharpeRatio = stdReturn > 0 ? (avgReturn - riskFreeRate) / stdReturn : 0

    table.cell(metricsTable, 0, 8, "Sharpe Ratio", text_color=color.white)
    table.cell(metricsTable, 1, 8, str.tostring(sharpeRatio, "#.##"), text_color=sharpeRatio > 1 ? color.green : sharpeRatio > 0 ? color.yellow : color.red)
```

### 4. Indicator Accuracy Testing
```pinescript
// For indicators: Track signal accuracy
var int truePositives = 0
var int falsePositives = 0
var int trueNegatives = 0
var int falseNegatives = 0

// Define what constitutes a successful signal (example: price moves 1% in signal direction)
targetMove = input.float(1.0, "Target Move %", group="Backtest Settings")
lookforward = input.int(10, "Bars to Confirm", group="Backtest Settings")

if barstate.isconfirmed and bar_index > lookforward
    // Check if past signal was correct
    if buySignal[lookforward]
        priceChange = (close - close[lookforward]) / close[lookforward] * 100
        if priceChange >= targetMove
            truePositives += 1
        else
            falsePositives += 1
    else if sellSignal[lookforward]
        priceChange = (close[lookforward] - close) / close[lookforward] * 100
        if priceChange >= targetMove
            trueNegatives += 1
        else
            falseNegatives += 1

// Display accuracy metrics
if barstate.islastconfirmedhistory
    accuracy = (truePositives + trueNegatives) / math.max(truePositives + trueNegatives + falsePositives + falseNegatives, 1) * 100
    precision = truePositives / math.max(truePositives + falsePositives, 1) * 100
    recall = truePositives / math.max(truePositives + falseNegatives, 1) * 100

    table.cell(metricsTable, 0, 9, "Signal Accuracy", text_color=color.white)
    table.cell(metricsTable, 1, 9, str.tostring(accuracy, "#.##") + "%", text_color=accuracy > 60 ? color.green : color.red)
```

### 5. Equity Curve Visualization
```pinescript
// Plot equity curve (for strategies)
plot(strategy.equity, "Equity Curve", color=color.blue, linewidth=2)

// Add drawdown visualization
equityMA = ta.sma(strategy.equity, 20)
plot(equityMA, "Equity MA", color=color.orange, linewidth=1)

// Underwater equity (drawdown visualization)
var float peakEquity = strategy.initial_capital
peakEquity := math.max(peakEquity, strategy.equity)
drawdownValue = (peakEquity - strategy.equity) / peakEquity * 100

// Plot drawdown as histogram
plot(drawdownValue, "Drawdown %", color=color.red, style=plot.style_histogram, histbase=0)
```

### 6. Multi-Timeframe Validation
```pinescript
// Test indicator on multiple timeframes
htf1_signal = request.security(syminfo.tickerid, "60", buySignal)
htf2_signal = request.security(syminfo.tickerid, "240", buySignal)
htf3_signal = request.security(syminfo.tickerid, "D", buySignal)

// Confluence scoring
confluenceScore = 0
confluenceScore += buySignal ? 1 : 0
confluenceScore += htf1_signal ? 1 : 0
confluenceScore += htf2_signal ? 1 : 0
confluenceScore += htf3_signal ? 1 : 0

// Track confluence performance
var array<float> confluenceReturns = array.new<float>()
if confluenceScore >= 3 and barstate.isconfirmed
    // Track returns when high confluence
    futureReturn = (close[10] - close) / close * 100  // 10-bar forward return
    array.push(confluenceReturns, futureReturn)
```

### 7. Walk-Forward Analysis
```pinescript
// Simple walk-forward testing
lookbackPeriod = input.int(100, "Training Period", group="Walk-Forward")
forwardPeriod = input.int(20, "Testing Period", group="Walk-Forward")

// Optimize parameters on lookback period
var float optimalParam = na
if bar_index % (lookbackPeriod + forwardPeriod) == 0
    // Re-optimize parameters based on past performance
    // This is simplified - real implementation would test multiple values
    optimalParam := ta.sma(close, lookbackPeriod) > close ? 20 : 50

// Use optimized parameters
maLength = int(optimalParam)
ma = ta.sma(close, maLength)
```

## Strategy Requirements

**CRITICAL: All strategies must include branding and alert annotation:**
```pinescript
// built with PineScript Agents by TradersPost
//@version=6
strategy("My Strategy", overlay=true)
//@strategy_alert_message {{strategy.order.alert_message}}
```

This enables alert messages passed by `alert()` functions and `strategy.order.alert_message` attributes to work with TradingView's native alert system.

## Testing Checklist

### Architecture (Check First!)
- [ ] Trade UDT defined for detailed tracking
- [ ] Time + bar_index stored for each trade
- [ ] Trade visualization uses xloc.bar_time
- [ ] for...in used for trade array iteration

### Strategy Requirements
- [ ] `//@strategy_alert_message` annotation included (after the `strategy()` call)
- [ ] Net profit/loss calculation
- [ ] Win rate and trade count
- [ ] Maximum drawdown tracking
- [ ] Risk-adjusted returns (Sharpe/Sortino)
- [ ] Trade distribution analysis
- [ ] Equity curve visualization
- [ ] Signal accuracy for indicators
- [ ] Multi-timeframe validation
- [ ] Statistical significance tests
- [ ] Forward testing results

## Output Format

Always provide:
1. Performance metrics table
2. Equity curve visualization
3. Drawdown analysis
4. Trade distribution stats
5. Risk metrics
6. Recommendations for improvement

Backtesting in Pine Script has limitations. Past performance doesn't guarantee future results. Always include appropriate disclaimers.
