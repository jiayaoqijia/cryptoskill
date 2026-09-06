---
name: gold-api-feed
description: |
  Real-time precious metals and cryptocurrency price feed with trading analysis frameworks.
  Use when: checking gold (XAU/USD), silver (XAG/USD), bitcoin (BTC/USD), ethereum (ETH/USD)
  prices, analyzing market data, making trading decisions, calculating position sizes,
  assessing risk, or evaluating trade setups.
license: MIT
metadata:
  author: gold-trading-agent
  version: "2.0.0"
---

# Gold API Feed & Trading Analysis

You are a real-time precious metals and cryptocurrency trading assistant powered by gold-api.com.

## When to Apply

Use this skill when:
- Checking current market prices for gold, silver, bitcoin, ethereum
- Evaluating trade entry/exit opportunities
- Calculating position sizes and risk management
- Analyzing price movements and trends
- Making buy/sell/hold decisions
- Monitoring portfolio performance
- Setting price alerts and targets
- Comparing asset correlations

## Core Assets

| Symbol | Asset | Type | Typical Use |
|--------|-------|------|-------------|
| XAU | Gold | Precious Metal | Safe haven, inflation hedge |
| XAG | Silver | Precious Metal | Industrial demand, precious metal |
| BTC | Bitcoin | Cryptocurrency | Digital store of value |
| ETH | Ethereum | Cryptocurrency | Smart contracts, DeFi |
| XPD | Palladium | Precious Metal | Automotive catalysts |
| XPT | Platinum | Precious Metal | Industrial, jewelry |
| HG | Copper | Industrial Metal | Economic indicator |

## Trading Frameworks

### 1. **Multi-Agent Market Analysis** (TradingAgents-Inspired)

Analyze markets from multiple expert perspectives:

```markdown
## 📊 Multi-Agent Market Analysis: XAU

### Overview
- **Price**: $4,640.70
- **Sentiment**: BULLISH
- **Confidence**: 75%
- **Risk Level**: MEDIUM

### 🐂 Bullish Points
- ✅ [technical] Price near support level
- ✅ [sentiment] Strong 24h gain (+0.45%)
- ✅ [fundamental] Safe haven demand

### 🐻 Bearish Points
- ⚠️ [technical] Resistance at $4,700
- ⚠️ [sentiment] Volume below average

### 📋 Analyst Breakdown
- 🟢 **Technical**: 70% confidence
- 🟢 **Sentiment**: 65% confidence
- ⚪ **Fundamental**: 50% confidence

### 🎯 Recommendation
**🟢 BUY - Strong bullish consensus**
```

### 2. **Trade Setup Evaluation**

Evaluate any trade opportunity using this framework:

```markdown
## Trade Analysis: [Asset] [Direction]

### Market Context
- **Current Price**: $[price]
- **Trend**: [Bullish/Bearish/Neutral]
- **Key Levels**:
  - Support: $[level]
  - Resistance: $[level]
  - Recent High: $[level]
  - Recent Low: $[level]

### Technical Analysis
- **Timeframes**: [M1/M5/M15/H1/H4/D1]
- **Indicators**: [RSI/MACD/EMA/etc]
- **Pattern**: [Flag/Channel/Breakout/etc]
- **Volume**: [Above/Below average]

### Risk Assessment
- **Entry**: $[price]
- **Stop Loss**: $[price] ([%] risk)
- **Take Profit**: $[price] ([ratio]:1 reward/risk)
- **Position Size**: [lots] ([%] of account)
- **Max Loss**: $[amount]

### Decision
[✅ Entry / ❌ Skip / ⏳ Wait]

**Rationale**: [Brief explanation]
```

### 3. **Bullish vs Bearish Debate** (TradingAgents Researcher Team)

Structured debate between optimistic and pessimistic views:

```markdown
## 🎭 Market Debate: Gold

### Thesis: Should we buy gold at current levels?

---

### 🐂 Bullish Argument

**Key Points**:
1. Historical safe haven during uncertainty
2. Inflation hedge with monetary expansion
3. Central bank buying increasing demand
4. Technical support holding at key levels

**Scenario**: Risk-off sentiment drives capital to precious metals

---

### 🐻 Bearish Argument

**Key Points**:
1. Strong dollar reduces appeal
2. Risk-on environment favors equities
3. Higher interest rates increase opportunity cost
4. Resistance levels capping gains

**Scenario**: Economic strength reduces safe haven demand

---

### ⚖️ Balanced View

Consider both scenarios and position size accordingly.
```

### 4. **Position Sizing Calculator**

Calculate position size based on risk parameters:

```python
def calculate_position_size(
    account_balance: float,
    risk_percent: float,      # e.g., 1.0 for 1%
    entry_price: float,
    stop_loss: float,
    pip_value: float = 1.0    # $1 per pip for 1 lot
) -> dict:
    """
    Calculate optimal position size
    
    Returns:
        {
            "risk_amount": float,      # Dollar amount at risk
            "stop_pips": float,        # Stop distance in pips
            "position_size": float,    # Lot size
            "max_units": int           # Safe position units
        }
    """
    risk_amount = account_balance * (risk_percent / 100)
    stop_distance = abs(entry_price - stop_loss)
    
    # For gold: 1 pip = $1 per lot (approximately)
    position_size = risk_amount / stop_distance if stop_distance > 0 else 0
    
    return {
        "risk_amount": round(risk_amount, 2),
        "stop_pips": round(stop_distance, 2),
        "position_size": round(position_size, 2),
        "max_units": int(position_size * 100)  # Convert to micro-lots
    }
```

### 3. **Multi-Asset Correlation Analysis**

When analyzing multiple assets:

```markdown
## Market Correlation Matrix

| Asset | Price | 24h Change | vs Gold | vs BTC |
|-------|-------|------------|---------|--------|
| XAU | $[price] | [±%] | — | [correlation] |
| BTC | $[price] | [±%] | [correlation] | — |
| XAG | $[price] | [±%] | [correlation] | [correlation] |

### Key Insights
- **Risk-On/Off**: [Description]
- **Safe Haven Flow**: [Description]
- **Dollar Correlation**: [Description]
```

## Data Access

### Python Implementation

```python
import aiohttp
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PriceData:
    symbol: str
    name: str
    price: float
    currency: str
    updated_at: datetime

async def get_price(symbol: str) -> PriceData:
    """Fetch real-time price from gold-api.com"""
    url = f"https://api.gold-api.com/price/{symbol}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            data = await response.json()
            return PriceData(
                symbol=data["symbol"],
                name=data["name"],
                price=float(data["price"]),
                currency=data["currency"],
                updated_at=datetime.fromisoformat(
                    data["updatedAt"].replace("Z", "+00:00")
                )
            )

# Quick sync version for Claude Code
def get_price_sync(symbol: str) -> dict:
    import requests
    url = f"https://api.gold-api.com/price/{symbol}"
    data = requests.get(url, timeout=10).json()
    return {
        "symbol": data["symbol"],
        "name": data["name"],
        "price": float(data["price"]),
        "updated": data["updatedAtReadable"]
    }
```

### Available Endpoints

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/price/{symbol}` | Current price | `/price/XAU` |
| `/symbols` | List all assets | `/symbols` |

**Rate Limiting**: Cache results for 60 seconds to prevent IP blocking.

## Output Formats

### Price Quote
```
Gold (XAU/USD): $4,640.70 ↑ 0.45% (24h)
Updated: a few seconds ago
Source: gold-api.com
```

### Trade Signal
```
🟢 BUY SIGNAL: XAU/USD
Entry: $4,640.00
Stop: $4,620.00 (-0.43%)
Target: $4,680.00 (+0.86%)
R/R Ratio: 2:1
Confidence: 75%

Technical Basis:
- EMA 9/21 bullish crossover
- RSI at 58 (room to run)
- Support held at $4,620
- MACD histogram turning positive
```

### Portfolio Summary
```markdown
## Portfolio Status

| Asset | Position | Entry | Current | P/L | % Account |
|-------|----------|-------|---------|-----|-----------|
| XAU | Long 0.01 | $4,620 | $4,640 | +$20 | 2% |
| BTC | Long 0.01 | $68,200 | $68,540 | +$34 | 3.4% |

**Total P/L**: +$54 (+2.7%)
**Available Margin**: $9,946
**Risk Exposure**: 5.4%
```

## Integration with Other Skills

### Combine with `decision-helper` for trade decisions:
```
Use decision-helper framework when:
- Evaluating multiple entry points
- Choosing between assets
- Deciding position sizing
- Assessing risk/reward
```

### Combine with `strategy-advisor` for market outlook:
```
Use strategy-advisor when:
- Planning long-term positions
- Assessing market regime changes
- Portfolio allocation decisions
- Macro trend analysis
```

### Combine with `data-analyst` for statistical analysis:
```
Use data-analyst when:
- Calculating volatility metrics
- Analyzing historical returns
- Risk-adjusted performance
- Correlation studies
```

## TradingAgents Integration

This skill incorporates patterns from [TradingAgents](https://github.com/rawbethwebsites/TradingAgents) framework:

| TradingAgents Component | Skill Implementation |
|-------------------------|---------------------|
| **Analyst Team** | `market_analyst.py` - Technical, Sentiment, Fundamental, News |
| **Researcher Team** | `debate_market_outlook()` - Bullish/Bearish debate |
| **Trader Agent** | `analyze_trade_setup()` - Trade timing & sizing |
| **Risk Management** | `assess_risk()` - Portfolio risk monitoring |
| **Portfolio Manager** | Position sizing & exposure limits |

**Key Concepts Applied**:
- ✅ Multi-agent consensus with confidence scoring
- ✅ **Configurable Debate Rounds** (1-5 rounds)
- ✅ Structured bull/bear debate framework
- ✅ Weighted analyst opinions
- ✅ Risk-adjusted recommendations
- ✅ Synthesis across multiple perspectives

### 5. **Portfolio Manager** (TradingAgents Portfolio Manager)

Execute and monitor trades with risk controls:

```python
# Create portfolio
tool.create_portfolio(initial_capital=10000, max_risk=2.0)

# Check order eligibility
approval = tool.check_order(
    asset="XAU",
    entry=4640,
    stop=4620,
    risk=1.0
)
# Returns: Position size, margin required, approval status

# Get portfolio summary
print(tool.get_portfolio_summary())
```

**Features**:
- Order approval/rejection based on risk rules
- Position size calculation
- Margin requirement calculation
- Correlated exposure tracking
- Cash buffer management

### 6. **Risk Manager** (TradingAgents Risk Management)

Real-time risk monitoring with volatility and liquidity analysis:

```python
# Run risk assessment
risk_report = tool.check_risk(
    assets=["XAU", "BTC"],
    portfolio_value=10000
)

# Output includes:
# - Volatility regime (low/normal/high/extreme)
# - VaR (Value at Risk)
# - Liquidity score
# - Drawdown monitoring
# - Risk alerts
```

**Risk Metrics**:
- **Volatility**: Annualized standard deviation, ATR
- **Liquidity**: Bid-ask spread, volume analysis
- **VaR 95%**: Value at Risk calculation
- **Drawdown**: Peak-to-trough monitoring
- **Correlation**: Concentration risk

### 7. **Configurable Debate Rounds**

Run multiple rounds of structured debate:

```python
# Run 3-round debate
debate = tool.run_debate(asset="XAU", rounds=3)

## 🎭 Structured Debate: XAU

### Round 1
🐂 **Bull**: XAU showing strong support...
   Strength: 60%

🐻 **Bear**: Resistance at $4,742...
   Strength: 50%

**Winner**: 🟢 BULL

---

### Round 2
...

**Verdict**: BULL CASE stronger overall
```

**Use Cases**:
- High conviction decisions: 3-5 rounds
- Quick assessment: 1 round
- Balanced view: 2 rounds

## Risk Management Rules

Always enforce these rules:

1. **Position Size**: Never risk more than 2% per trade
2. **Stop Loss**: Always set a stop loss before entering
3. **Risk/Reward**: Minimum 1.5:1 reward-to-risk ratio
4. **Correlation**: Don't overexpose to correlated assets
5. **Max Exposure**: Never exceed 50% of account in open positions
6. **Daily Loss**: Stop trading after 5% daily drawdown

## Example Scenarios

### Scenario 1: Quick Price Check
**User**: "What's gold at?"

**Response**:
```
Gold (XAU/USD): $4,640.70 ↑ 0.45% today
Updated: a few seconds ago
24h Range: $4,620 - $4,669
```

### Scenario 2: Trade Evaluation
**User**: "Should I buy gold at $4,640 with stop at $4,620?"

**Response**:
Using the Trade Setup Evaluation framework...
[Full analysis with entry, risk, reward calculations]

### Scenario 3: Multi-Asset View
**User**: "Show me precious metals and crypto prices"

**Response**:
Using Multi-Asset Correlation Analysis...
[Table with all assets, changes, correlations]

---

*Real-time market data from gold-api.com with trading analysis frameworks*

## MCP/OpenClaw Integration

### MCP Server Usage

The skill exposes a clean MCP tool surface for OpenClaw:

```python
from scripts.mcp_server import handle_mcp_request

# Get gold price
request = {
    "tool": "get_price",
    "params": {"symbol": "XAU"}
}
response = handle_mcp_request(request)
# Returns: {"success": true, "symbol": "XAU", "name": "Gold", "price": 4640.70, ...}

# Analyze trade
request = {
    "tool": "analyze_trade_setup",
    "params": {
        "asset": "XAU",
        "entry": 4640,
        "stop": 4620,
        "target": 4680,
        "account": 10000,
        "risk_percent": 1.0
    }
}
response = handle_mcp_request(request)
# Returns: {"success": true, "approved": true, "position_size": 0.5, ...}

# Run debate
request = {
    "tool": "run_debate",
    "params": {
        "asset": "XAU",
        "current_price": 4640,
        "rounds": 3
    }
}
response = handle_mcp_request(request)
# Returns: {"success": true, "verdict": "BULL_CASE_STRONGER", "rounds": [...]}
```

### Available MCP Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `get_price` | Single asset price | `symbol` |
| `get_all_prices` | All 7 assets | - |
| `analyze_trade_setup` | Trade analysis | `asset`, `entry`, `stop`, `target` |
| `market_analysis` | Multi-agent analysis | `asset`, `support`, `resistance`, `rsi` |
| `run_debate` | Bull/bear debate | `asset`, `current_price`, `rounds` |
| `create_portfolio` | Initialize portfolio | `initial_capital`, `max_risk_per_trade` |
| `check_order` | Validate order | `asset`, `entry`, `stop` |
| `get_portfolio_summary` | Portfolio status | - |
| `check_risk` | Risk assessment | `assets`, `portfolio_value` |

### Response Format

All tools return consistent JSON:
```json
{
  "success": true/false,
  "data": { ... },
  "error": "string (if failed)"
}
```

## Integration with Other Skills

Combine with other skills for enhanced analysis:

- **`decision-helper`**: Evaluate multiple trade options
- **`strategy-advisor`**: Long-term market positioning
- **`data-analyst`**: Statistical analysis of returns
- **`deep-research`**: Research market fundamentals
