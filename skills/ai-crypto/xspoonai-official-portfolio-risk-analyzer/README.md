# Portfolio Risk Analyzer Skill

Advanced portfolio risk analysis and real-time monitoring for Web3 assets, DeFi positions, and liquidation warnings.

## 🎯 Overview

The Portfolio Risk Analyzer provides comprehensive risk assessment for Web3 portfolios, enabling investors and traders to:

- **Identify liquidation risks** before they occur with real-time LTV monitoring
- **Analyze concentration risk** across tokens and protocols
- **Understand correlation exposure** between holdings
- **Get diversification recommendations** based on risk metrics
- **Monitor DeFi positions** across lending protocols (Aave, Compound, Curve)
- **Track health metrics** with customizable alert thresholds

## ✨ Core Features

### 1. Portfolio Risk Scoring
- **Comprehensive risk assessment** (0-100 score)
- Multi-factor analysis including:
  - Concentration risk (single token dominance)
  - Volatility exposure
  - Liquidity risk
  - Smart contract risk
  - Market correlation

### 2. Concentration Analysis
- Identify overexposed tokens
- Track asset distribution
- Alert on single-token dominance
- Visualize allocation breakdown

### 3. Correlation Tracking
- Analyze token price correlations
- Identify diversification gaps
- Find uncorrelated assets for hedging
- Understand systemic risk exposure

### 4. DeFi Position Monitoring
- Track lending positions (Aave, Compound, etc.)
- Monitor borrowing requirements
- Calculate current LTV ratios
- Estimate liquidation prices
- Alert on approaching liquidation thresholds

### 5. Liquidation Risk Warnings
- Real-time liquidation price calculation
- LTV health status (Green/Yellow/Red)
- Distance to liquidation metrics
- Historical LTV trends

### 6. Diversification Recommendations
- Allocation suggestions based on risk tolerance
- Rebalancing guidance
- Asset pairing recommendations
- Protocol diversification tips

## 📊 Risk Score Breakdown

```
Portfolio Risk Score (0-100)
├── Concentration Risk (0-25 points)
│   ├── Single token dominance
│   └── Protocol exposure
├── Volatility Risk (0-25 points)
│   ├── Token volatility
│   └── Correlated movement
├── Liquidity Risk (0-25 points)
│   ├── Token trading volume
│   └── Exit difficulty
└── Smart Contract Risk (0-25 points)
    ├── Protocol audits
    └── Exploit history
```

## 🚀 Usage Examples

### Basic Portfolio Analysis
```python
from portfolio_risk_analyzer import PortfolioRiskAnalyzer

analyzer = PortfolioRiskAnalyzer(api_key="your_alchemy_key")

# Get comprehensive risk report
report = await analyzer.analyze_portfolio(
    address="0x742d35Cc6634C0532925a3b844Bc0e6dB1Eae543",
    chain="ethereum",
    analysis_type="comprehensive"
)

print(f"Risk Score: {report.risk_score}/100")
print(f"Liquidation Status: {report.liquidation_status}")
print(f"Top Risk Factor: {report.primary_risk}")
```

### Monitor Liquidation Risk
```python
# Track DeFi position safety
liquidation_data = await analyzer.check_liquidation_risk(
    address="0x742d35Cc6634C0532925a3b844Bc0e6dB1Eae543",
    protocol="aave",
    chain="ethereum"
)

print(f"Current LTV: {liquidation_data.current_ltv}%")
print(f"Liquidation Price: {liquidation_data.liquidation_price}")
print(f"Health Factor: {liquidation_data.health_factor}")
```

### Diversification Analysis
```python
# Get rebalancing recommendations
recommendations = await analyzer.get_recommendations(
    address="0x742d35Cc6634C0532925a3b844Bc0e6dB1Eae543",
    risk_tolerance="moderate"  # low, moderate, high
)

for rec in recommendations.rebalancing_suggestions:
    print(f"Consider: {rec.action}")
```

## 📈 Supported Chains

- Ethereum (ETH)
- Polygon (MATIC)
- Arbitrum One (ARB)
- Optimism (OP)
- Avalanche (AVAX)
- Base (BASE)

## 🔌 API Requirements

### Required
- **Alchemy API Key** - For portfolio data and token metadata
- **Etherscan API Key** - For transaction and token data

### Optional (for enhanced DeFi analysis)
- Aave Subgraph endpoint
- Compound Subgraph endpoint
- Curve Finance API
- CoinGecko API (free tier available)

## 🛡️ Security Considerations

✅ **What this skill does:**
- Read-only operations on public blockchain data
- No wallet modifications
- No transaction signing
- Public address analysis only

❌ **What this skill does NOT do:**
- Execute transactions
- Store private keys
- Modify wallet settings
- Access private/internal transactions

**Best Practices:**
1. Use read-only API keys
2. Monitor API rate limits
3. Cache results when possible
4. Set reasonable alert thresholds

## 📁 File Structure

```
portfolio-risk-analyzer/
├── SKILL.md                           # Skill metadata & configuration
├── README.md                          # This file
├── scripts/
│   ├── portfolio_fetcher.py          # Fetch wallet holdings
│   ├── risk_calculator.py            # Calculate risk metrics
│   ├── correlation_analyzer.py       # Analyze token correlations
│   ├── defi_exposure_analyzer.py     # DeFi position analysis
│   ├── liquidation_monitor.py        # Liquidation risk monitoring
│   ├── diversification_recommender.py # Generate recommendations
│   └── requirements.txt               # Python dependencies
└── examples/
    ├── basic_analysis.py
    ├── defi_monitoring.py
    └── alert_system.py
```

## 📊 Output Examples

### Portfolio Analysis Report
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc0e6dB1Eae543",
  "chain": "ethereum",
  "total_value_usd": 125450.50,
  "risk_score": 62,
  "risk_level": "MODERATE",
  "updated_at": "2026-02-07T14:23:00Z",
  "holdings": [
    {
      "symbol": "ETH",
      "allocation": 45.2,
      "value_usd": 56720.43,
      "risk_factor": 0.75
    },
    {
      "symbol": "USDC",
      "allocation": 25.0,
      "value_usd": 31362.63,
      "risk_factor": 0.1
    }
  ],
  "concentration_risk": 45.2,
  "primary_risk_factor": "Overweight in ETH",
  "liquidation_status": "SAFE",
  "recommendations": [
    "Reduce ETH allocation to below 40%",
    "Add stablecoin buffer to 30%",
    "Diversify into uncorrelated assets"
  ]
}
```

## 🎓 Learning Resources

- [Aave Risk Management](https://docs.aave.com/risk/risk-management)
- [Understanding LTV & Health Factor](https://academy.binance.com/en/articles/defi-risks)
- [Portfolio Diversification Guide](https://www.investopedia.com/terms/p/portfolio-theory.asp)

## 🤝 Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for submission guidelines.

**Areas for enhancement:**
- Additional protocol integrations (Yearn, Convex, etc.)
- Advanced correlation models
- Machine learning risk prediction
- Historical backtest analysis
- Mobile alert integration

## 📝 License

Part of the spoon-awesome-skill community contribution program.

## 🆘 Support

For issues or questions:
1. Check the [examples](./examples/) directory
2. Review the [CONTRIBUTING.md](../../CONTRIBUTING.md)
3. Open an issue in the repository

## 🚀 Next Steps

1. **Test the skill** with sample addresses
2. **Customize alert thresholds** for your use case
3. **Integrate with monitoring systems** (Discord, Telegram, Email)
4. **Extend with additional protocols** as needed

---

**Last Updated:** February 7, 2026  
**Status:** Production Ready  
**Support Level:** Community
