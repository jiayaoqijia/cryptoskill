# TaoStats Skill

**Purpose**: Interact with TaoStats API for Bittensor blockchain data - subnets, validators, miners, staking, emissions, and more.

**API Documentation**: https://docs.taostats.io/  
**Base URL**: `https://api.taostats.io`  
**Rate Limit**: 5 calls/minute (free tier)

---
## Setup

### 1. Set API Key
Get a free API key from [taostats.io](https://taostats.io) and export it as an environment variable:
```bash
export TAOSTATS_API_KEY="tao-xxxxx:yyyyy"
```

### 2. Source Helper Functions
```bash
source ~/.openclaw/workspace/skills/taostats/taostats.sh
```

---

## Complete Endpoint Reference

### dTAO Pool Endpoints

#### `GET /api/dtao/pool/latest/v1?netuid={N}`
**CRITICAL**: This endpoint has EVERYTHING for trading decisions.

**Key Fields**:
- `price` - Current alpha price in TAO
- `root_prop` - % of price from root TAO injection (CRITICAL for entry validation)
- `fear_and_greed_index` / `fear_and_greed_sentiment` - Market sentiment
- `seven_day_prices` - Historical price array (42 data points)
- `price_change_1_hour`, `price_change_1_day`, `price_change_1_week`, `price_change_1_month`
- `market_cap`, `liquidity`, `total_tao`, `total_alpha`
- `tao_volume_24_hr`, `alpha_volume_24_hr`, `buys_24_hr`, `sells_24_hr`
- `highest_price_24_hr`, `lowest_price_24_hr`

**Example**:
```bash
curl -s "https://api.taostats.io/api/dtao/pool/latest/v1?netuid=33" \
  -H "Authorization: $TAOSTATS_API_KEY" | jq '.data[0].root_prop'
# Returns: "0.2104087259347016725" (21% - GOOD entry)
```

#### `GET /api/dtao/pool/history/v1?netuid={N}&limit={L}`
Historical pool snapshots for backtesting.

#### `GET /api/dtao/validator/yield/latest/v1?netuid={N}`
Validator APYs with multiple timeframes.

**Key Fields**:
- `seven_day_apy` - Primary metric for staking decisions
- `one_day_apy`, `one_hour_apy`, `thirty_day_apy`
- `seven_day_epoch_participation` - Validator reliability
- `name`, `hotkey.ss58`, `stake`, `take`

**Example**:
```bash
curl -s "https://api.taostats.io/api/dtao/validator/yield/latest/v1?netuid=33" \
  -H "Authorization: $TAOSTATS_API_KEY" | \
  jq -r '.data | sort_by(-.seven_day_apy) | .[0] | 
  "\(.name // .hotkey.ss58): \(.seven_day_apy * 100)% APY"'
```

#### `GET /api/dtao/stake_balance/latest/v1?coldkey={COLDKEY}`
All stake positions across all subnets.

**Key Fields**:
- `netuid`, `hotkey.ss58`, `hotkey_name`
- `balance_as_tao` - ⚠️ IN RAO (divide by 1e9)
- `price`, `price_change_1_day`
- `root_prop` - Per-position root proportion

### Subnet Endpoints

#### `GET /api/subnet/latest/v1` or `?netuid={N}`
Complete subnet parameters and economics.

**Key Fields**:
- `netuid`, `emission`, `projected_emission`
- `net_flow_1_day`, `net_flow_7_days`, `net_flow_30_days` - Capital flow tracking
- `recycled_24_hours`, `recycled_lifetime` - Registration economics
- `tao_flow`, `excess_tao` - dTAO mechanics
- `immune_owner_uids_limit`, `immunity_period` - Risk assessment
- `max_validators`, `active_validators`
- `difficulty`, `adjustment_alpha` - Mining economics

#### `GET /api/subnet/registration/v1?netuid={N}`
Subnet registration details.

**Key Fields**:
- `owner.ss58` - Subnet owner
- `registration_cost` - Current registration cost
- `timestamp` - When registered

### Validator Endpoints

#### `GET /api/validator/latest/v1?netuid={N}`
Current validator state.

**Key Fields**:
- `apr`, `apr_7_day_average`, `apr_30_day_average`
- `nominator_return_per_k` - Staker yield per 1000 TAO
- `nominators`, `nominators_24_hr_change` - Capital inflows/outflows
- `stake`, `stake_24_hr_change`, `validator_stake`, `system_stake`
- `take` - Commission rate
- `name`, `coldkey.ss58`, `hotkey.ss58`
- `permits` - Subnet permissions

#### `GET /api/validator/history/v1?netuid={N}&hotkey={H}&limit={L}`
Historical validator performance.

**Key Fields**:
- All APR metrics with daily granularity
- `nominators_24_hr_change` - Track capital movements
- `dominance`, `subnet_dominance` - Market share

### Transaction Endpoints

#### `GET /api/delegation/v1?nominator={COLDKEY}&action={all|stake|unstake}&limit={L}`
Complete transaction history (stakes, unstakes, transfers).

**Key Fields**:
- `action` ("add" = stake, "remove" = unstake)
- `amount`, `rate` (price), `tao_amount`, `alpha_amount`
- `fee`, `slippage`
- `block_number`, `timestamp`
- `hotkey.ss58`, `coldkey.ss58`

#### `GET /api/transfer/v1?from={COLDKEY}&limit={L}`
TAO transfer history (not staking).

**Key Fields**:
- `from.ss58`, `to.ss58`, `amount`, `fee`
- `block_number`, `timestamp`

### Metagraph Endpoints

#### `GET /api/metagraph/latest/v1?netuid={N}&limit={L}`
Complete subnet state for every neuron.

**Key Fields**:
- `uid`, `hotkey.ss58`, `coldkey.ss58`
- `rank`, `trust`, `consensus`, `incentive`, `dividends`, `emission`
- `alpha_stake`, `root_stake`, `total_alpha_stake`
- `daily_mining_alpha`, `daily_validating_alpha`, `daily_reward`
- `validator_permit`, `is_immunity_period`, `in_danger`
- `daily_burned_alpha`, `daily_owner_alpha`

#### `GET /api/neuron/latest/v1?netuid={N}&limit={L}`
Simplified neuron view with pruning risk.

**Key Fields**:
- `uid`, `name`, `hotkey.ss58`, `coldkey.ss58`
- `pruning_score`, `in_danger`, `is_immune`
- `miner_rank`, `validator_rank`

---

## Quick Reference

### Get Subnet Pool Data
```bash
taostats_pool 33
# Returns: price, root_prop, fear_and_greed_index, 7-day price history, volume
```

### Get Validator APYs
```bash
taostats_validator_yield 33
# Returns: All validators with 1h/1d/7d/30d APYs
```

### Get Stake Balances
```bash
taostats_stake_balance "YOUR_COLDKEY_HERE"
# Returns: All positions with root_prop per subnet
```

### Get Transaction History
```bash
taostats_delegation_history "YOUR_COLDKEY_HERE"
# Returns: All stake/unstake transactions with slippage
```

### Get Subnet Parameters
```bash
taostats_subnet_info 33
# Returns: Emissions, net flows, registration cost, immunity params
```

### Get Metagraph
```bash
taostats_metagraph 33
# Returns: All neurons with stakes, ranks, emissions
```

---

## Common Patterns

### Check Entry Quality (root_prop < 0.30)
```bash
NETUID=33
ROOT_PROP=$(curl -s "https://api.taostats.io/api/dtao/pool/latest/v1?netuid=$NETUID" \
  -H "Authorization: $TAOSTATS_API_KEY" | jq -r '.data[0].root_prop')

if (( $(echo "$ROOT_PROP < 0.30" | bc -l) )); then
  echo "SN$NETUID: GOOD entry (root_prop: $ROOT_PROP)"
else
  echo "SN$NETUID: AVOID (root_prop: $ROOT_PROP - artificial price)"
fi
```

### Find Best Validator for Subnet
```bash
NETUID=33
curl -s "https://api.taostats.io/api/dtao/validator/yield/latest/v1?netuid=$NETUID" \
  -H "Authorization: $TAOSTATS_API_KEY" | \
  jq -r '.data | sort_by(-.seven_day_apy) | .[0] | 
  "\(.name // .hotkey.ss58) | APY: \(.seven_day_apy * 100)% | Commission: \(.take * 100)%"'
```

### Check Portfolio with root_prop per Position
```bash
COLDKEY="YOUR_COLDKEY_HERE"
curl -s "https://api.taostats.io/api/dtao/stake_balance/latest/v1?coldkey=$COLDKEY" \
  -H "Authorization: $TAOSTATS_API_KEY" | \
  jq -r '.data[] | 
  "SN\(.netuid): \((.balance_as_tao | tonumber) / 1000000000) TAO | root_prop: \(.root_prop)"'
```

### Scan for High APY Opportunities (S-tier only)
```bash
for NETUID in 33 64 51 13 3 1 100; do
  MAX_APY=$(curl -s "https://api.taostats.io/api/dtao/validator/yield/latest/v1?netuid=$NETUID" \
    -H "Authorization: $TAOSTATS_API_KEY" | jq -r '.data | max_by(.seven_day_apy) | .seven_day_apy')
  echo "$NETUID|$MAX_APY"
  sleep 0.3
done | sort -t'|' -k2 -rn | while IFS='|' read netuid apy; do
  printf "SN%-3s: %6.1f%%\n" "$netuid" "$(echo "$apy * 100" | bc -l)"
done
```

### Monitor Capital Flows (net_flow indicates momentum)
```bash
curl -s "https://api.taostats.io/api/subnet/latest/v1" \
  -H "Authorization: $TAOSTATS_API_KEY" | \
  jq -r '.data[] | select(.netuid != 0) | 
  "SN\(.netuid): net_flow_7d=\(.net_flow_7_days) | emission=\(.emission)"' | \
  sort -t'=' -k2 -rn | head -10
```

---

## Python Tools

### `taostats_client.py`
Robust API client with automatic retry logic.

```python
from taostats_client import TaostatsAPI

api = TaostatsAPI("your-api-key")

# Single call with retry
result = api.get_json("dtao/pool/latest/v1?netuid=33")

# Paginated (handles all pages automatically)
all_data = api.get_paginated("dtao/stake_balance/latest/v1?coldkey=XYZ")

# Balance history
history = api.get_balance_history(coldkey, start_timestamp, end_timestamp)
```

### `balance_history.py`
Track daily portfolio changes over time.

```bash
# View last 30 days
python3 skills/taostats/balance_history.py --days 30

# Export to CSV
python3 skills/taostats/balance_history.py --days 90 --export
```

**Output:**
```
📊 Portfolio History (30 records):
--------------------------------------------------------------------------------
Date         Free τ    Staked τ    Total τ    Daily Δ
--------------------------------------------------------------------------------
2026-01-07   0.0234    1.9567    1.9801            
2026-01-08   0.0256    1.9789    2.0045   +0.0244
...
Overall Change: +0.5399 τ (+27.27%)
```

---

## Bash Functions (taostats.sh)

### Core Trading Functions

#### `taostats_pool <netuid>`
Get full pool data including root_prop and fear & greed.
- **Returns**: price, root_prop, fear_and_greed_index, seven_day_prices, volume
- **Use for**: Entry validation, sentiment analysis, price history

#### `taostats_pool_history <netuid> [limit]`
Historical pool snapshots.
- **Returns**: Time-series of pool state
- **Use for**: Backtesting, trend analysis

#### `taostats_validator_yield <netuid>`
All validators with APYs.
- **Returns**: 1h/1d/7d/30d APYs, participation rates
- **Use for**: Validator selection

#### `taostats_stake_balance <coldkey>`
All positions with per-subnet root_prop.
- **Returns**: Balance, price, root_prop per position
- **Use for**: Portfolio monitoring, risk assessment

#### `taostats_delegation_history <coldkey> [limit]`
Transaction history with slippage.
- **Returns**: Stakes, unstakes, fees, slippage
- **Use for**: Performance tracking, tax records

### Subnet Analysis Functions

#### `taostats_subnet_info [netuid]`
Subnet parameters and economics.
- **Returns**: Emissions, net flows, registration costs
- **Use for**: Fundamental analysis

#### `taostats_subnet_registration <netuid>`
Subnet ownership and registration details.
- **Returns**: Owner, registration cost, timestamp
- **Use for**: Due diligence

### Validator Analysis Functions

#### `taostats_validator_info <netuid>`
Current validator state.
- **Returns**: APR, nominator returns, stake changes
- **Use for**: Deep validator research

#### `taostats_validator_history <netuid> <hotkey> [limit]`
Historical validator performance.
- **Returns**: Daily APR trends
- **Use for**: Validator reliability assessment

### Metagraph Functions

#### `taostats_metagraph <netuid>`
Complete subnet state.
- **Returns**: All neurons with stakes, emissions, ranks
- **Use for**: Ecosystem analysis

#### `taostats_neurons <netuid>`
Simplified neuron view.
- **Returns**: Pruning scores, immunity status
- **Use for**: Risk monitoring

---

## Rate Limit Handling

**Free tier**: 5 calls per minute

**Best practices**:
1. Cache pool data (changes slowly)
2. Use `sleep 0.3` between calls (20 calls/min safe)
3. Batch where possible
4. Monitor for 429 errors

**Example rate-limited loop**:
```bash
for NETUID in {1..50}; do
  taostats_pool $NETUID | jq -r '.data[0] | "SN\(.netuid): root_prop=\(.root_prop)"'
  sleep 0.3
done
```

---

## Error Handling

| Code | Cause | Fix |
|------|-------|-----|
| 401 | Invalid API key | Check `.taostats` format, no "Bearer" prefix |
| 404 | Wallet not indexed | Wait 1-2 hours for new wallets |
| 429 | Rate limit | Add `sleep` delays between calls |
| Empty | Inactive subnet | Check if subnet exists first |

---

## Critical Fields for Trading

### Entry Validation
- `root_prop` < 0.30 = Good (organic price)
- `root_prop` > 0.70 = Bad (artificially pumped)

### Momentum Signals
- `net_flow_7_days` > 0 = Capital inflow
- `nominators_24_hr_change` > 0 = Growing validator stake

### Risk Metrics
- `in_danger` = true → Pruning risk
- `is_immunity_period` = true → Protected from dereg
- `pruning_score` → Lower is safer

### Sentiment
- `fear_and_greed_index` < 30 = Fear (potential buy)
- `fear_and_greed_index` > 70 = Greed (potential wait)

---

## Known Issues

### `balance_as_tao` Field Bug
**Issue**: Returns value in rao (raw units), not TAO.

**Workaround**: Always divide by 1,000,000,000
```bash
balance_tao=$(echo "$balance_as_tao / 1000000000" | bc -l)
```

**Affected endpoints**:
- `/api/dtao/stake_balance/latest/v1`

---

## Integration Examples

### Entry Scanner (root_prop + APY + flow)
```bash
#!/bin/bash
source ~/.openclaw/workspace/skills/taostats/taostats.sh

echo "=== High-Quality Entry Opportunities ==="
for NETUID in 33 64 51 13 3 1 100 117 12 120; do
  POOL=$(taostats_pool $NETUID)
  ROOT_PROP=$(echo "$POOL" | jq -r '.data[0].root_prop')
  PRICE=$(echo "$POOL" | jq -r '.data[0].price')
  FEAR_GREED=$(echo "$POOL" | jq -r '.data[0].fear_and_greed_sentiment')
  
  MAX_APY=$(taostats_validator_yield $NETUID | jq -r '.data | max_by(.seven_day_apy) | .seven_day_apy')
  
  if (( $(echo "$ROOT_PROP < 0.30" | bc -l) )); then
    printf "SN%-3s | root_prop: %.2f | APY: %5.1f%% | Sentiment: %s\n" \
      "$NETUID" "$ROOT_PROP" "$(echo "$MAX_APY * 100" | bc -l)" "$FEAR_GREED"
  fi
  sleep 0.3
done
```

### Portfolio Risk Monitor
```bash
#!/bin/bash
source ~/.openclaw/workspace/skills/taostats/taostats.sh

COLDKEY="YOUR_COLDKEY"
echo "=== Portfolio Risk Assessment ==="

taostats_stake_balance $COLDKEY | jq -r '.data[] | 
  "\(.netuid)|\(.balance_as_tao)|\(.root_prop)"' | while IFS='|' read netuid balance root_prop; do
  BALANCE_TAO=$(echo "$balance / 1000000000" | bc -l)
  if (( $(echo "$root_prop > 0.50" | bc -l) )); then
    printf "⚠️ SN%-3s: %6.3f TAO | HIGH root_prop: %.2f - Consider exit\n" "$netuid" "$BALANCE_TAO" "$root_prop"
  else
    printf "✅ SN%-3s: %6.3f TAO | OK root_prop: %.2f\n" "$netuid" "$BALANCE_TAO" "$root_prop"
  fi
done
```

---

## Python Wrapper

```python
import requests
import os

class TaoStatsAPI:
    def __init__(self):
        self.base_url = "https://api.taostats.io"
        self.api_key = os.getenv("TAOSTATS_API_KEY")
        
    def _get(self, endpoint):
        headers = {"Authorization": self.api_key, "accept": "application/json"}
        r = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        return r.json()
    
    def pool(self, netuid):
        """Get pool data with root_prop and fear & greed"""
        return self._get(f"/api/dtao/pool/latest/v1?netuid={netuid}")
    
    def validator_yield(self, netuid):
        """Get all validators with APYs"""
        return self._get(f"/api/dtao/validator/yield/latest/v1?netuid={netuid}")
    
    def stake_balance(self, coldkey):
        """Get all positions with root_prop per subnet"""
        return self._get(f"/api/dtao/stake_balance/latest/v1?coldkey={coldkey}")
    
    def subnet_info(self, netuid=None):
        """Get subnet parameters and net flows"""
        if netuid:
            return self._get(f"/api/subnet/latest/v1?netuid={netuid}")
        return self._get("/api/subnet/latest/v1")

# Usage
api = TaoStatsAPI()
pool = api.pool(33)
print(f"SN33 root_prop: {pool['data'][0]['root_prop']}")
```

---

## Skill Maintenance

**Last Updated**: 2026-02-06  
**Author**: vanlabs-dev  
**Dependencies**: `curl`, `jq`, `bc`

**Changelog**:
- 2026-02-06: COMPLETE OVERHAUL - Discovered root_prop, fear_and_greed, 7-day history in pool endpoint
- 2026-02-06: Added all working endpoints from discovery testing
- 2026-02-06: Added entry validation patterns using root_prop
- 2026-02-03: Initial version

**TODO**:
- [ ] Add caching layer for pool data
- [ ] Build retry logic with exponential backoff
- [ ] Create real-time monitoring dashboard
- [ ] Add root_prop alerts for portfolio positions
