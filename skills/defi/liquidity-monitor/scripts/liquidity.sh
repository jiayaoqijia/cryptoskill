#!/usr/bin/env bash
# Liquidity Monitor — Monitor DEX liquidity pools and calculate IL
# Usage: bash liquidity.sh <command> [options]
set -euo pipefail

COMMAND="${1:-help}"
shift 2>/dev/null || true

DATA_DIR="${HOME}/.liquidity-monitor"
mkdir -p "$DATA_DIR"

case "$COMMAND" in
  pools)
    CHAIN="${1:-ethereum}"
    LIMIT="${2:-20}"
    SORT="${3:-tvl}"
    
    python3 << 'PYEOF'
import sys, os, json, time
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

chain = sys.argv[1] if len(sys.argv) > 1 else "ethereum"
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
sort_by = sys.argv[3] if len(sys.argv) > 3 else "tvl"

chain_map = {
    "ethereum": "Ethereum",
    "bsc": "BSC", 
    "polygon": "Polygon",
    "arbitrum": "Arbitrum",
    "base": "Base",
    "avalanche": "Avalanche",
    "optimism": "Optimism",
    "solana": "Solana"
}

chain_name = chain_map.get(chain, chain)

# Use DeFiLlama API for pool data
try:
    url = "https://yields.llama.fi/pools"
    req = Request(url)
    req.add_header("User-Agent", "LiquidityMonitor/1.0")
    resp = urlopen(req, timeout=15)
    data = json.loads(resp.read().decode("utf-8"))
    
    pools = data.get("data", [])
    
    # Filter by chain
    filtered = [p for p in pools if p.get("chain", "").lower() == chain.lower() or chain_name.lower() in p.get("chain", "").lower()]
    
    # Sort
    if sort_by == "apy":
        filtered.sort(key=lambda x: x.get("apy", 0) or 0, reverse=True)
    elif sort_by == "tvl":
        filtered.sort(key=lambda x: x.get("tvlUsd", 0) or 0, reverse=True)
    
    filtered = filtered[:limit]
    
    print("=" * 80)
    print("TOP LIQUIDITY POOLS — {} (sorted by {})".format(chain_name, sort_by.upper()))
    print("Time: {}".format(time.strftime("%Y-%m-%d %H:%M")))
    print("=" * 80)
    print("")
    print("{:<4} {:<20} {:<25} {:>12} {:>10} {:>8}".format(
        "#", "Protocol", "Pool", "TVL", "APY", "IL Risk"))
    print("-" * 80)
    
    for i, pool in enumerate(filtered, 1):
        protocol = pool.get("project", "?")[:19]
        symbol = pool.get("symbol", "?")[:24]
        tvl = pool.get("tvlUsd", 0) or 0
        apy = pool.get("apy", 0) or 0
        il_risk = pool.get("ilRisk", "unknown")
        
        if tvl >= 1000000:
            tvl_str = "${:.1f}M".format(tvl / 1000000)
        elif tvl >= 1000:
            tvl_str = "${:.0f}K".format(tvl / 1000)
        else:
            tvl_str = "${:.0f}".format(tvl)
        
        print("{:<4} {:<20} {:<25} {:>12} {:>9.1f}% {:>8}".format(
            i, protocol, symbol, tvl_str, apy, il_risk or "?"))
    
    print("")
    print("Data source: DeFiLlama (yields.llama.fi)")
    
    # Cache
    cache = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "chain": chain, "pools": filtered[:limit]}
    cache_file = os.path.join(os.path.expanduser("~/.liquidity-monitor"), "pools-{}.json".format(chain))
    with open(cache_file, "w") as f:
        json.dump(cache, f, indent=2)

except Exception as e:
    print("Error fetching pool data: {}".format(str(e)))
    print("Try again in a few moments or check your internet connection.")
PYEOF
    ;;

  il-calc)
    PRICE_CHANGE="${1:-2.0}"
    DEPOSIT="${2:-1000}"
    
    python3 << 'PYEOF'
import sys, math

price_ratio = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
deposit = float(sys.argv[2]) if len(sys.argv) > 2 else 1000

# Impermanent Loss formula: IL = 2*sqrt(r)/(1+r) - 1
# where r = price_ratio

scenarios = [
    0.1, 0.25, 0.5, 0.75, 0.9, 1.0,
    1.1, 1.25, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0
]

print("=" * 65)
print("IMPERMANENT LOSS CALCULATOR")
print("=" * 65)
print("")
print("Initial deposit: ${:,.0f}".format(deposit))
print("(50% Token A, 50% Token B)")
print("")
print("-" * 65)
print("{:>15} {:>12} {:>15} {:>15}".format(
    "Price Change", "IL %", "Pool Value", "vs HODL"))
print("-" * 65)

for r in scenarios:
    if r <= 0:
        continue
    il = 2 * math.sqrt(r) / (1 + r) - 1
    il_pct = abs(il) * 100
    
    # Pool value with IL
    hodl_value = deposit * (1 + r) / 2  # simplified: half in token, half in stable
    pool_value = deposit * 2 * math.sqrt(r) / (1 + r)
    diff = pool_value - hodl_value
    
    direction = "+" if r > 1 else ""
    pct_change = (r - 1) * 100
    
    marker = " <<<" if abs(r - price_ratio) < 0.01 else ""
    
    print("{:>14.0f}% {:>11.2f}% {:>14,.0f} {:>+14,.0f}{}".format(
        pct_change, il_pct, pool_value, diff, marker))

print("")
print("-" * 65)
print("KEY INSIGHTS:")
print("")

# Calculate for the specific input
il = 2 * math.sqrt(price_ratio) / (1 + price_ratio) - 1
il_pct = abs(il) * 100
hodl_value = deposit * (1 + price_ratio) / 2
pool_value = deposit * 2 * math.sqrt(price_ratio) / (1 + price_ratio)
diff = pool_value - hodl_value

print("  At {}x price change:".format(price_ratio))
print("    IL: {:.2f}%".format(il_pct))
print("    Pool value: ${:,.0f}".format(pool_value))
print("    HODL value: ${:,.0f}".format(hodl_value))
print("    Difference: ${:+,.0f}".format(diff))
print("")

# Break-even APR calculation
days_in_year = 365
holding_periods = [30, 90, 180, 365]
print("  To break even, you need APR of:")
for days in holding_periods:
    needed_apr = (il_pct / 100) * (365 / days) * 100
    print("    {}-day hold: {:.1f}% APR".format(days, needed_apr))

print("")
print("  Rule of thumb:")
print("    - < 1.25x change: IL is negligible (<0.6%)")
print("    - 2x change: IL = 5.7% (manageable with good APR)")
print("    - 5x change: IL = 25.5% (need very high APR)")
print("    - Stablecoin pairs: Near-zero IL")
PYEOF
    ;;

  yield-compare)
    CHAIN="${1:-ethereum}"
    
    python3 << 'PYEOF'
import sys, os, json, time
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

chain = sys.argv[1] if len(sys.argv) > 1 else "ethereum"

try:
    url = "https://yields.llama.fi/pools"
    req = Request(url)
    req.add_header("User-Agent", "LiquidityMonitor/1.0")
    resp = urlopen(req, timeout=15)
    data = json.loads(resp.read().decode("utf-8"))
    pools = data.get("data", [])
    
    # Filter and categorize
    stable_pools = []
    volatile_pools = []
    
    for p in pools:
        if p.get("chain", "").lower() != chain.lower():
            continue
        tvl = p.get("tvlUsd", 0) or 0
        apy = p.get("apy", 0) or 0
        if tvl < 100000 or apy <= 0:
            continue
        
        symbol = p.get("symbol", "").lower()
        is_stable = any(s in symbol for s in ["usdc", "usdt", "dai", "frax", "lusd", "busd"])
        
        entry = {
            "protocol": p.get("project", "?"),
            "symbol": p.get("symbol", "?"),
            "tvl": tvl,
            "apy": apy,
            "il_risk": p.get("ilRisk", "?")
        }
        
        if is_stable:
            stable_pools.append(entry)
        else:
            volatile_pools.append(entry)
    
    stable_pools.sort(key=lambda x: x["apy"], reverse=True)
    volatile_pools.sort(key=lambda x: x["apy"], reverse=True)
    
    print("=" * 70)
    print("YIELD COMPARISON — {} Chain".format(chain.upper()))
    print("=" * 70)
    
    print("")
    print("STABLECOIN POOLS (Low IL Risk):")
    print("-" * 70)
    for i, p in enumerate(stable_pools[:10], 1):
        tvl_str = "${:.1f}M".format(p["tvl"] / 1e6) if p["tvl"] >= 1e6 else "${:.0f}K".format(p["tvl"] / 1e3)
        print("  {}. {:<18} {:<22} TVL:{:>10} APY:{:>8.1f}%".format(
            i, p["protocol"][:17], p["symbol"][:21], tvl_str, p["apy"]))
    
    print("")
    print("VOLATILE POOLS (Higher IL Risk, Higher APY):")
    print("-" * 70)
    for i, p in enumerate(volatile_pools[:10], 1):
        tvl_str = "${:.1f}M".format(p["tvl"] / 1e6) if p["tvl"] >= 1e6 else "${:.0f}K".format(p["tvl"] / 1e3)
        print("  {}. {:<18} {:<22} TVL:{:>10} APY:{:>8.1f}%".format(
            i, p["protocol"][:17], p["symbol"][:21], tvl_str, p["apy"]))
    
    print("")
    if stable_pools and volatile_pools:
        avg_stable = sum(p["apy"] for p in stable_pools[:10]) / min(len(stable_pools), 10)
        avg_volatile = sum(p["apy"] for p in volatile_pools[:10]) / min(len(volatile_pools), 10)
        print("  Average APY (top 10 stable): {:.1f}%".format(avg_stable))
        print("  Average APY (top 10 volatile): {:.1f}%".format(avg_volatile))
        print("  Premium for IL risk: {:.1f}%".format(avg_volatile - avg_stable))
    
except Exception as e:
    print("Error: {}".format(str(e)))
PYEOF
    ;;

  lp-calc)
    TOKEN_A_AMOUNT="${1:-1}"
    TOKEN_A_PRICE="${2:-3000}"
    TOKEN_B_AMOUNT="${3:-3000}"
    TOKEN_B_PRICE="${4:-1}"
    APR="${5:-20}"
    DAYS="${6:-365}"
    
    python3 << 'PYEOF'
import sys, math

a_amount = float(sys.argv[1]) if len(sys.argv) > 1 else 1
a_price = float(sys.argv[2]) if len(sys.argv) > 2 else 3000
b_amount = float(sys.argv[3]) if len(sys.argv) > 3 else 3000
b_price = float(sys.argv[4]) if len(sys.argv) > 4 else 1
apr = float(sys.argv[5]) if len(sys.argv) > 5 else 20
days = int(sys.argv[6]) if len(sys.argv) > 6 else 365

total_value = (a_amount * a_price) + (b_amount * b_price)
daily_yield = total_value * (apr / 100) / 365
period_yield = daily_yield * days

print("=" * 55)
print("LP YIELD CALCULATOR")
print("=" * 55)
print("")
print("Position:")
print("  Token A: {} @ ${:,.2f} = ${:,.2f}".format(a_amount, a_price, a_amount * a_price))
print("  Token B: {} @ ${:,.2f} = ${:,.2f}".format(b_amount, b_price, b_amount * b_price))
print("  Total Value: ${:,.2f}".format(total_value))
print("")
print("Yield ({:.1f}% APR over {} days):".format(apr, days))
print("  Daily: ${:,.2f}".format(daily_yield))
print("  Weekly: ${:,.2f}".format(daily_yield * 7))
print("  Monthly: ${:,.2f}".format(daily_yield * 30))
print("  Period ({} days): ${:,.2f}".format(days, period_yield))
print("  Annual: ${:,.2f}".format(daily_yield * 365))
print("")

# With compounding
if apr > 0:
    daily_rate = apr / 100 / 365
    compound_value = total_value * ((1 + daily_rate) ** days)
    compound_yield = compound_value - total_value
    print("With daily compounding:")
    print("  APY: {:.2f}%".format(((1 + daily_rate) ** 365 - 1) * 100))
    print("  Value after {} days: ${:,.2f}".format(days, compound_value))
    print("  Yield: ${:,.2f}".format(compound_yield))
    print("  Extra vs simple: ${:,.2f}".format(compound_yield - period_yield))
PYEOF
    ;;

  help|*)
    cat << 'HELPEOF'
Liquidity Monitor — Track DEX pools, calculate IL, compare yields

COMMANDS:
  pools [chain] [limit] [sort]
         List top liquidity pools (sort: tvl|apy)

  il-calc <price_ratio> [deposit]
         Calculate impermanent loss

  yield-compare [chain]
         Compare stable vs volatile pool yields

  lp-calc <tokenA_amt> <tokenA_price> <tokenB_amt> <tokenB_price> [apr] [days]
         Calculate LP position yield

EXAMPLES:
  bash liquidity.sh pools ethereum 20 apy
  bash liquidity.sh il-calc 2.0 10000
  bash liquidity.sh yield-compare base
  bash liquidity.sh lp-calc 1 3000 3000 1 25 180

SUPPORTED CHAINS: ethereum, bsc, polygon, arbitrum, base, avalanche, optimism, solana
HELPEOF
    ;;
esac

echo ""
echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
