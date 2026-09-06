# Yield Calculator Skill

The **Yield Calculator** answers the most common DeFi question: "How much will I earn?". By standardizing yield calculations, SpoonOS agents can optimize portfolios effectively.

## Features

- **APR to APY**: Converts simple interest to compound interest.
- **Compounding Frequency**: Supports Daily, Weekly, or Continuous compounding.
- **Profit Projection**: Estimates total return in USD/Token terms.

## Usage

### Parameters

- `principal` (float, required): Initial amount invested.
- `apr_percent` (float, required): Annual Percentage Rate (e.g., 5.5 for 5.5%).
- `days` (int, optional): Duration of investment (default: 365).
- `compounds_per_year` (int, optional): 365 = Daily, 52 = Weekly, 1 = Simple (default: 365).

### Example Agent Prompts

> "If I put 10 ETH in a staking pool at 4% APR for 6 months, how much do I get?"
> "Compare 10% APR daily compounded vs 11% APR simple interest."

### Output

```json
{
  "principal": 1000.0,
  "apy_percent": 6.18,
  "projected_balance": 1061.80,
  "net_profit": 61.80
}
```
