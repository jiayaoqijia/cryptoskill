---
name: wallet-health
description: Analyze wallet activity and calculate a health/risk score.
version: 1.0.0
author: SpoonOS Contributor
tags: [web3, security, compliance, analysis]
---

# Wallet Health Analyzer

A security skill that profiles an address based on its on-chain footprint. It checks nonce (activity level), balance (liquidity), and contract interaction patterns to assign a rudimentary "Health Score".

## Quick Start

```python
# Analyze a target address
report = await agent.run_tool(
    "wallet_health",
    target_address="0x123..."
)
print(f"Health Score: {report['score']}/100")
```

## Scripts

| Script | Purpose |
|--------|---------|
| [health_score.py](scripts/health_score.py) | Profiling script using `web3` |

## Best Practices

1. Use before interacting with unknown users in a P2P context.
2. High scores indicate active, mature wallets (likely safe).
3. Low scores (fresh wallets with 0 activity) warrant caution.
