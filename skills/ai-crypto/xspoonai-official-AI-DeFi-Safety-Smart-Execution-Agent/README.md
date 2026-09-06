# AI DeFi Safety & Smart Execution Agent

A SpoonOS skill that transforms DeFi intent into a **safe, simulated, and explainable execution plan**.

## Overview

This READ-ONLY skill analyzes DeFi actions (swaps) without executing transactions. It provides:
- Token safety analysis
- Swap simulation with slippage/gas estimates
- Safety scoring (0-100) with verdict
- Plain-English explanations

## Usage

```python
from defi_safety import analyze_defi_action

result = analyze_defi_action({
    "action": "swap",
    "from_token": "USDC",
    "to_token": "ETH",
    "amount": 500,
    "chain": "Arbitrum",
    "max_slippage": 1.0,
    "risk_tolerance": "medium"
})

print(result["safety_score"])  # 85
print(result["verdict"])       # "SAFE"
print(result["explanation"])   # Plain-English summary
```

## Input Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action | string | Yes | Action type (currently "swap") |
| from_token | string | Yes | Source token symbol |
| to_token | string | Yes | Destination token symbol |
| amount | number | Yes | Amount of from_token |
| chain | string | Yes | Blockchain name |
| max_slippage | number | No | Max slippage % (default: 1.0) |
| risk_tolerance | string | No | "low", "medium", "high" (default: "medium") |

## Output Structure

```json
{
  "input_summary": { ... },
  "from_token_analysis": {
    "token": "USDC",
    "risk_level": "low",
    "risk_score": 5,
    "liquidity_usd": 500000000,
    "risk_flags": []
  },
  "to_token_analysis": { ... },
  "swap_simulation": {
    "expected_output": 0.15625,
    "slippage_percent": 0.25,
    "gas_estimate_usd": 0.30,
    "mev_risk": "low"
  },
  "safety_score": 85,
  "verdict": "SAFE",
  "explanation": "This swap appears safe...",
  "recommendation": "Proceed with confidence."
}
```

## Verdict Levels

| Score | Verdict | Meaning |
|-------|---------|---------|
| 80-100 | SAFE | Low risk, proceed normally |
| 50-79 | CAUTION | Moderate risk, review details |
| 0-49 | DANGEROUS | High risk, avoid or proceed carefully |

## Security Guarantees

- **READ-ONLY**: No wallet connections or transaction signing
- **No Secrets Required**: Runs without API keys (LLM optional)
- **Deterministic Fallback**: Works offline with rule-based analysis
- **Non-Custodial**: Never handles private keys or funds

## Architecture

```
skill.py          → Entry point, orchestration
safety_analyzer.py → Token risk analysis
swap_simulator.py  → DEX swap simulation
risk_engine.py     → Safety scoring
ai_explainer.py    → LLM/fallback explanations
```

## License

MIT

