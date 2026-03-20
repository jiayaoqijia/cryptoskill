#!/bin/bash
# TaoStats API Helper Functions
# Source this file to use: source ~/path/to/skills/taostats/taostats.sh

# Load API key from environment variable (preferred) or fallback to .taostats file
if [ -z "$TAOSTATS_API_KEY" ] && [ -f ~/.openclaw/workspace/.taostats ]; then
    export TAOSTATS_API_KEY=$(grep TAOSTATS_API_KEY ~/.openclaw/workspace/.taostats | cut -d= -f2)
fi

if [ -z "$TAOSTATS_API_KEY" ]; then
    echo "⚠️  TAOSTATS_API_KEY not set. Export it: export TAOSTATS_API_KEY=your-key" >&2
fi

# Base URL
TAOSTATS_BASE_URL="https://api.taostats.io"

# Internal helper for GET requests with retry logic
_taostats_get() {
    local endpoint="$1"
    local max_retries=3
    local retry_delay=12
    local attempt=0
    
    while [ $attempt -lt $max_retries ]; do
        local response=$(curl -s "${TAOSTATS_BASE_URL}${endpoint}" \
            -H "Authorization: ${TAOSTATS_API_KEY}" \
            -H "accept: application/json" \
            -w "\n%{http_code}")
        
        local http_code=$(echo "$response" | tail -1)
        local body=$(echo "$response" | sed '$d')
        
        # Check for rate limit (429)
        if [ "$http_code" = "429" ]; then
            attempt=$((attempt + 1))
            if [ $attempt -lt $max_retries ]; then
                echo "  Rate limited. Waiting ${retry_delay}s... (retry $attempt/$max_retries)" >&2
                sleep $retry_delay
                continue
            else
                echo "Error: Rate limit exceeded after $max_retries retries" >&2
                return 1
            fi
        fi
        
        # Check for errors
        if [ "$http_code" != "200" ] || echo "$body" | grep -q '"error"'; then
            echo "API Failure (HTTP $http_code): $body" >&2
            return 1
        fi
        
        echo "$body"
        return 0
    done
}

# Python API Client (more robust, with retry logic)
# Usage: taostats_py <endpoint>
taostats_py() {
    local endpoint="$1"
    python3 "${SKILL_DIR}/taostats_client.py" "$endpoint"
}

# ==================== Core Queries ====================

# Get dTAO pool data for a subnet (includes root_prop, fear_and_greed, 7-day history)
# Usage: taostats_pool <netuid>
taostats_pool() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_pool <netuid>" >&2
        return 1
    fi
    _taostats_get "/api/dtao/pool/latest/v1?netuid=${netuid}"
}

# Get historical pool snapshots for backtesting
# Usage: taostats_pool_history <netuid> [limit]
taostats_pool_history() {
    local netuid="$1"
    local limit="${2:-100}"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_pool_history <netuid> [limit]" >&2
        return 1
    fi
    _taostats_get "/api/dtao/pool/history/v1?netuid=${netuid}&limit=${limit}"
}

# Get validator yield (APY) for a subnet
# Usage: taostats_validator_yield <netuid>
taostats_validator_yield() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_validator_yield <netuid>" >&2
        return 1
    fi
    _taostats_get "/api/dtao/validator/yield/latest/v1?netuid=${netuid}"
}

# Get stake balances for a coldkey across all subnets
# Usage: taostats_stake_balance <coldkey>
taostats_stake_balance() {
    local coldkey="$1"
    if [ -z "$coldkey" ]; then
        echo "Usage: taostats_stake_balance <coldkey>" >&2
        return 1
    fi
    _taostats_get "/api/dtao/stake_balance/latest/v1?coldkey=${coldkey}"
}

# Get delegation transaction history
# Usage: taostats_delegation_history <coldkey> [limit]
taostats_delegation_history() {
    local coldkey="$1"
    local limit="${2:-50}"
    if [ -z "$coldkey" ]; then
        echo "Usage: taostats_delegation_history <coldkey> [limit]" >&2
        return 1
    fi
    _taostats_get "/api/delegation/v1?nominator=${coldkey}&action=all&page=1&limit=${limit}"
}

# Get pruning data for all subnets
# Usage: taostats_pruning
taostats_pruning() {
    _taostats_get "/api/subnet/pruning/latest/v1"
}

# Get dev activity for all subnets
# Usage: taostats_dev_activity
taostats_dev_activity() {
    _taostats_get "/api/dev_activity/latest/v1"
}

# Get metagraph (full subnet state)
# Usage: taostats_metagraph <netuid>
taostats_metagraph() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_metagraph <netuid>" >&2
        return 1
    fi
    _taostats_get "/api/metagraph/latest/v1?netuid=${netuid}"
}

# Get simplified neuron view with pruning risk
# Usage: taostats_neurons <netuid> [limit]
taostats_neurons() {
    local netuid="$1"
    local limit="${2:-100}"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_neurons <netuid> [limit]" >&2
        return 1
    fi
    _taostats_get "/api/neuron/latest/v1?netuid=${netuid}&limit=${limit}"
}

# Get subnet parameters and economics
# Usage: taostats_subnet_info [netuid]
taostats_subnet_info() {
    local netuid="$1"
    if [ -n "$netuid" ]; then
        _taostats_get "/api/subnet/latest/v1?netuid=${netuid}"
    else
        _taostats_get "/api/subnet/latest/v1"
    fi
}

# Get subnet registration details (owner, cost)
# Usage: taostats_subnet_registration <netuid>
taostats_subnet_registration() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_subnet_registration <netuid>" >&2
        return 1
    fi
    _taostats_get "/api/subnet/registration/v1?netuid=${netuid}"
}

# Get detailed validator info
# Usage: taostats_validator_info <netuid>
taostats_validator_info() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_validator_info <netuid>" >&2
        return 1
    fi
    _taostats_get "/api/validator/latest/v1?netuid=${netuid}"
}

# Get validator historical performance
# Usage: taostats_validator_history <netuid> <hotkey> [limit]
taostats_validator_history() {
    local netuid="$1"
    local hotkey="$2"
    local limit="${3:-100}"
    if [ -z "$netuid" ] || [ -z "$hotkey" ]; then
        echo "Usage: taostats_validator_history <netuid> <hotkey> [limit]" >&2
        return 1
    fi
    _taostats_get "/api/validator/history/v1?netuid=${netuid}&hotkey=${hotkey}&limit=${limit}"
}

# Get transfer history (non-staking)
# Usage: taostats_transfer_history <coldkey> [limit]
taostats_transfer_history() {
    local coldkey="$1"
    local limit="${2:-50}"
    if [ -z "$coldkey" ]; then
        echo "Usage: taostats_transfer_history <coldkey> [limit]" >&2
        return 1
    fi
    _taostats_get "/api/transfer/v1?from=${coldkey}&limit=${limit}"
}

# Calculate slippage for a trade
# Usage: taostats_slippage <netuid> <amount_rao> <direction>
# Direction: tao_to_alpha or alpha_to_tao
taostats_slippage() {
    local netuid="$1"
    local amount_rao="$2"
    local direction="$3"
    if [ -z "$netuid" ] || [ -z "$amount_rao" ] || [ -z "$direction" ]; then
        echo "Usage: taostats_slippage <netuid> <amount_rao> <direction>" >&2
        echo "Direction: tao_to_alpha or alpha_to_tao" >&2
        return 1
    fi
    _taostats_get "/api/dtao/slippage/v1?netuid=${netuid}&input_tokens=${amount_rao}&direction=${direction}"
}

# Get free TAO balance (not staked)
# Usage: taostats_coldkey_balance <coldkey>
taostats_coldkey_balance() {
    local coldkey="$1"
    if [ -z "$coldkey" ]; then
        echo "Usage: taostats_coldkey_balance <coldkey>" >&2
        return 1
    fi
    _taostats_get "/api/wallet/coldkey/balance/latest/v2?coldkey=${coldkey}"
}

# ==================== Helper Functions ====================

# Get top N validators by APY for a subnet
# Usage: taostats_top_validators <netuid> [n]
taostats_top_validators() {
    local netuid="$1"
    local n="${2:-10}"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_top_validators <netuid> [n]" >&2
        return 1
    fi
    taostats_validator_yield "$netuid" | jq -r --arg n "$n" \
        '.data | sort_by(-.seven_day_apy) | .[:($n | tonumber)] | .[] | 
        "\(.name // .hotkey.ss58): \(.seven_day_apy * 100 | floor)% APY"'
}

# Get total staked TAO for a coldkey
# Usage: taostats_total_staked <coldkey>
taostats_total_staked() {
    local coldkey="$1"
    if [ -z "$coldkey" ]; then
        echo "Usage: taostats_total_staked <coldkey>" >&2
        return 1
    fi
    taostats_stake_balance "$coldkey" | jq -r \
        '[.data[].balance_as_tao | tonumber] | add / 1000000000'
}

# Check if subnet is at deregistration risk
# Usage: taostats_dereg_risk <netuid>
taostats_dereg_risk() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_dereg_risk <netuid>" >&2
        return 1
    fi
    taostats_pruning | jq -r --arg netuid "$netuid" \
        '.data[] | select(.netuid == ($netuid | tonumber)) | 
        if .is_immune then
            "✅ SAFE - Immune (expires: \(.immunity_period_end))"
        elif .pruning_rank < 20 then
            "🚨 HIGH RISK - Rank \(.pruning_rank)/\(.total_validators) (non-immune)"
        else
            "⚠️  MEDIUM RISK - Rank \(.pruning_rank)/\(.total_validators) (non-immune)"
        end'
}

# Scan all subnets for APY opportunities above threshold
# Usage: taostats_scan_apy <min_apy_percent>
taostats_scan_apy() {
    local min_apy="${1:-100}"
    echo "Scanning for subnets with >${min_apy}% APY..." >&2
    for netuid in {1..50}; do
        max_apy=$(taostats_validator_yield $netuid 2>/dev/null | \
            jq -r '.data | max_by(.seven_day_apy) | .seven_day_apy * 100' 2>/dev/null || echo "0")
        
        if [ "$max_apy" != "null" ] && [ "$max_apy" != "0" ]; then
            if (( $(echo "$max_apy > $min_apy" | bc -l) )); then
                subnet_name=$(python3 ~/.openclaw/workspace/scripts/subnet_db.py name "$netuid" 2>/dev/null || echo "Unknown")
                printf "SN%-3s %-25s %6.1f%%\n" "$netuid" "$subnet_name" "$max_apy"
            fi
        fi
        sleep 0.3  # Rate limit
    done
}

# Get current TAO price in USD
# Usage: taostats_tao_price
taostats_tao_price() {
    # Use subnet pool data
    local pool=$(taostats_pool 1)
    echo "$pool" | jq -r '.data[0].price'
}

# Get root_prop for entry validation
# Usage: taostats_root_prop <netuid>
taostats_root_prop() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_root_prop <netuid>" >&2
        return 1
    fi
    taostats_pool "$netuid" | jq -r '.data[0].root_prop'
}

# Check if entry is safe (root_prop < threshold)
# Usage: taostats_entry_check <netuid> [threshold]
taostats_entry_check() {
    local netuid="$1"
    local threshold="${2:-0.30}"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_entry_check <netuid> [threshold]" >&2
        return 1
    fi
    
    local pool=$(taostats_pool "$netuid")
    local root_prop=$(echo "$pool" | jq -r '.data[0].root_prop')
    local price=$(echo "$pool" | jq -r '.data[0].price')
    local fear_greed=$(echo "$pool" | jq -r '.data[0].fear_and_greed_sentiment')
    
    if (( $(echo "$root_prop < $threshold" | bc -l) )); then
        echo "✅ SN${netuid}: GOOD entry | price: $price | root_prop: $root_prop | sentiment: $fear_greed"
        return 0
    else
        echo "⚠️  SN${netuid}: AVOID | price: $price | root_prop: $root_prop (artificial pump) | sentiment: $fear_greed"
        return 1
    fi
}

# Scan S-tier subnets for best entry opportunities
# Usage: taostats_scan_entries
taostats_scan_entries() {
    echo "=== Scanning S-tier subnets for entry opportunities ==="
    local subnets="33 64 51 13 3 1 100"  # S-tier netuids
    for netuid in $subnets; do
        taostats_entry_check "$netuid" 2>/dev/null
        sleep 0.3
    done
}

# Get fear & greed index for a subnet
# Usage: taostats_sentiment <netuid>
taostats_sentiment() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_sentiment <netuid>" >&2
        return 1
    fi
    taostats_pool "$netuid" | jq -r '.data[0] | "Index: \(.fear_and_greed_index) | Sentiment: \(.fear_and_greed_sentiment)"'
}

# Get 7-day price performance
# Usage: taostats_price_change <netuid>
taostats_price_change() {
    local netuid="$1"
    if [ -z "$netuid" ]; then
        echo "Usage: taostats_price_change <netuid>" >&2
        return 1
    fi
    taostats_pool "$netuid" | jq -r '.data[0] | "1h: \(.price_change_1_hour // 0 * 100)% | 1d: \(.price_change_1_day // 0 * 100)% | 1w: \(.price_change_1_week // 0 * 100)% | 1m: \(.price_change_1_month // 0 * 100)%"'
}

# Convert rao to TAO
# Usage: rao_to_tao <rao_amount>
rao_to_tao() {
    local rao="$1"
    echo "scale=9; $rao / 1000000000" | bc -l
}

# Convert TAO to rao
# Usage: tao_to_rao <tao_amount>
tao_to_rao() {
    local tao="$1"
    echo "$tao * 1000000000" | bc | cut -d. -f1
}

# ==================== Batch Queries ====================

# Get APY for multiple subnets at once
# Usage: taostats_batch_apy <netuid1> <netuid2> ...
taostats_batch_apy() {
    for netuid in "$@"; do
        max_apy=$(taostats_validator_yield $netuid 2>/dev/null | \
            jq -r '.data | max_by(.seven_day_apy) | .seven_day_apy * 100' 2>/dev/null || echo "N/A")
        echo "SN${netuid}: ${max_apy}%"
        sleep 0.3
    done
}

# ==================== Export Functions ====================

# Make functions available to subshells
export -f _taostats_get
export -f taostats_pool
export -f taostats_pool_history
export -f taostats_validator_yield
export -f taostats_validator_info
export -f taostats_validator_history
export -f taostats_stake_balance
export -f taostats_delegation_history
export -f taostats_transfer_history
export -f taostats_pruning
export -f taostats_dev_activity
export -f taostats_metagraph
export -f taostats_neurons
export -f taostats_subnet_info
export -f taostats_subnet_registration
export -f taostats_slippage
export -f taostats_coldkey_balance
export -f taostats_top_validators
export -f taostats_total_staked
export -f taostats_dereg_risk
export -f taostats_scan_apy
export -f taostats_tao_price
export -f taostats_root_prop
export -f taostats_entry_check
export -f taostats_scan_entries
export -f taostats_sentiment
export -f taostats_price_change
export -f rao_to_tao
export -f tao_to_rao
export -f taostats_batch_apy

echo "✅ TaoStats skill loaded. Type 'taostats_' and press TAB to see available functions."
