# TaoStats Skill - Quick Start

## Installation
```bash
# Already installed at ~/.openclaw/workspace/skills/taostats/
```

## Setup
1. Ensure `.taostats` file exists in workspace root with your API key
2. Source the functions: `source ~/.openclaw/workspace/skills/taostats/taostats.sh`

## Most Useful Commands

### Check Portfolio
```bash
taostats_stake_balance "YOUR_COLDKEY" | jq '.data[] | "SN\(.netuid): \((.balance_as_tao | tonumber) / 1e9) TAO"'
```

### Find Best Validator
```bash
taostats_top_validators 12
```

### Scan for High APY
```bash
taostats_scan_apy 80  # Find subnets with >80% APY
```

### Check Transaction History
```bash
taostats_delegation_history "YOUR_COLDKEY" 10
```

### Get Total Staked
```bash
taostats_total_staked "YOUR_COLDKEY"
```

## Full Documentation
See `SKILL.md` for complete function reference and examples.
