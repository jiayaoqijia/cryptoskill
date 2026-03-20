#!/usr/bin/env bash
# DEX Aggregator — Compare prices across decentralized exchanges
set -euo pipefail
COMMAND="${1:-help}"; shift 2>/dev/null || true
DATA_DIR="${HOME}/.dex-aggregator"; mkdir -p "$DATA_DIR"

case "$COMMAND" in
  quote)
    TOKEN_IN="${1:-ETH}"; TOKEN_OUT="${2:-USDC}"; AMOUNT="${3:-1}"; CHAIN="${4:-ethereum}"
    python3 << 'PYEOF'
import sys, os, json, time
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

token_in = sys.argv[1] if len(sys.argv) > 1 else "ETH"
token_out = sys.argv[2] if len(sys.argv) > 2 else "USDC"
amount = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
chain = sys.argv[4] if len(sys.argv) > 4 else "ethereum"

print("=" * 65)
print("DEX PRICE COMPARISON")
print("=" * 65)
print("")
print("Swap: {} {} → {} on {}".format(amount, token_in, token_out, chain.upper()))
print("Time: {}".format(time.strftime("%Y-%m-%d %H:%M")))
print("")

# Get current prices from CoinGecko
coin_map = {
    "ETH": "ethereum", "BTC": "bitcoin", "SOL": "solana", "BNB": "binancecoin",
    "USDC": "usd-coin", "USDT": "tether", "DAI": "dai", "WETH": "ethereum",
    "MATIC": "matic-network", "ARB": "arbitrum", "OP": "optimism",
    "AVAX": "avalanche-2", "LINK": "chainlink", "UNI": "uniswap",
    "AAVE": "aave", "CRV": "curve-dao-token", "MKR": "maker"
}

in_id = coin_map.get(token_in.upper(), token_in.lower())
out_id = coin_map.get(token_out.upper(), token_out.lower())

in_price = 0
out_price = 0

try:
    url = "https://api.coingecko.com/api/v3/simple/price?ids={},{}&vs_currencies=usd".format(in_id, out_id)
    req = Request(url)
    req.add_header("User-Agent", "DEXAggregator/1.0")
    resp = urlopen(req, timeout=10)
    prices = json.loads(resp.read().decode("utf-8"))
    in_price = prices.get(in_id, {}).get("usd", 0)
    out_price = prices.get(out_id, {}).get("usd", 1)
except Exception:
    pass

if in_price and out_price:
    mid_rate = in_price / out_price
    expected_out = amount * mid_rate
    value_usd = amount * in_price
    
    print("Market Price:")
    print("  {} = ${:,.2f}".format(token_in, in_price))
    print("  {} = ${:,.2f}".format(token_out, out_price))
    print("  Mid rate: 1 {} = {:.6f} {}".format(token_in, mid_rate, token_out))
    print("  Expected output: {:.6f} {}".format(expected_out, token_out))
    print("  Value: ${:,.2f}".format(value_usd))
    print("")

# DEX comparison with estimated slippage
dex_list = {
    "ethereum": [
        {"name": "Uniswap V3", "fee": 0.003, "slippage_factor": 0.001, "url": "app.uniswap.org"},
        {"name": "SushiSwap", "fee": 0.003, "slippage_factor": 0.002, "url": "sushi.com"},
        {"name": "Curve", "fee": 0.0004, "slippage_factor": 0.0005, "url": "curve.fi"},
        {"name": "Balancer", "fee": 0.002, "slippage_factor": 0.0015, "url": "balancer.fi"},
        {"name": "1inch", "fee": 0.0, "slippage_factor": 0.001, "url": "1inch.io"}
    ],
    "bsc": [
        {"name": "PancakeSwap", "fee": 0.0025, "slippage_factor": 0.001, "url": "pancakeswap.finance"},
        {"name": "BiSwap", "fee": 0.001, "slippage_factor": 0.002, "url": "biswap.org"},
        {"name": "1inch BSC", "fee": 0.0, "slippage_factor": 0.001, "url": "1inch.io"}
    ],
    "arbitrum": [
        {"name": "Camelot", "fee": 0.003, "slippage_factor": 0.001, "url": "camelot.exchange"},
        {"name": "SushiSwap", "fee": 0.003, "slippage_factor": 0.002, "url": "sushi.com"},
        {"name": "Uniswap V3", "fee": 0.003, "slippage_factor": 0.001, "url": "app.uniswap.org"}
    ],
    "base": [
        {"name": "Aerodrome", "fee": 0.002, "slippage_factor": 0.001, "url": "aerodrome.finance"},
        {"name": "BaseSwap", "fee": 0.003, "slippage_factor": 0.002, "url": "baseswap.fi"},
        {"name": "Uniswap V3", "fee": 0.003, "slippage_factor": 0.001, "url": "app.uniswap.org"}
    ],
    "polygon": [
        {"name": "QuickSwap", "fee": 0.003, "slippage_factor": 0.001, "url": "quickswap.exchange"},
        {"name": "SushiSwap", "fee": 0.003, "slippage_factor": 0.002, "url": "sushi.com"},
        {"name": "Uniswap V3", "fee": 0.003, "slippage_factor": 0.001, "url": "app.uniswap.org"}
    ],
    "solana": [
        {"name": "Jupiter", "fee": 0.0, "slippage_factor": 0.0005, "url": "jup.ag"},
        {"name": "Raydium", "fee": 0.0025, "slippage_factor": 0.001, "url": "raydium.io"},
        {"name": "Orca", "fee": 0.003, "slippage_factor": 0.001, "url": "orca.so"}
    ]
}

dexes = dex_list.get(chain, dex_list["ethereum"])

if in_price and out_price:
    print("-" * 65)
    print("{:<18} {:>10} {:>12} {:>12} {:>10}".format(
        "DEX", "Fee", "Output", "vs Mid", "Score"))
    print("-" * 65)
    
    results = []
    for dex in dexes:
        fee = dex["fee"]
        slippage = dex["slippage_factor"] * amount
        net_rate = mid_rate * (1 - fee - slippage)
        output = amount * net_rate
        diff_pct = ((output - expected_out) / expected_out) * 100 if expected_out > 0 else 0
        
        score = 100 + diff_pct * 10
        results.append({"dex": dex, "output": output, "diff_pct": diff_pct, "score": score})
    
    results.sort(key=lambda x: x["output"], reverse=True)
    
    for i, r in enumerate(results):
        marker = " ← BEST" if i == 0 else ""
        print("{:<18} {:>9.2f}% {:>12,.4f} {:>+11.3f}% {:>10.1f}{}".format(
            r["dex"]["name"], r["dex"]["fee"] * 100, r["output"], r["diff_pct"], r["score"], marker))
    
    best = results[0]
    print("")
    print("RECOMMENDATION:")
    print("  Use {} for best rate".format(best["dex"]["name"]))
    print("  URL: https://{}".format(best["dex"]["url"]))
    print("  Expected output: {:.4f} {}".format(best["output"], token_out))
    
    if value_usd > 10000:
        print("")
        print("  ⚠️ Large trade (${:,.0f})".format(value_usd))
        print("  Consider splitting across multiple DEXes")
        print("  Use 1inch or Paraswap for automatic split routing")
else:
    print("Could not fetch prices. Rate limited or token not found.")
    print("")
    print("DEXes available on {}:".format(chain))
    for dex in dexes:
        print("  • {} — https://{}".format(dex["name"], dex["url"]))
PYEOF
    ;;

  pools)
    TOKEN="${1:-ETH}"; CHAIN="${2:-ethereum}"
    python3 << 'PYEOF'
import sys, json, time
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

token = sys.argv[1] if len(sys.argv) > 1 else "ETH"
chain = sys.argv[2] if len(sys.argv) > 2 else "ethereum"

print("=" * 70)
print("LIQUIDITY POOLS — {} on {}".format(token, chain.upper()))
print("=" * 70)
print("")

try:
    url = "https://api.dexscreener.com/latest/dex/search?q={}".format(token)
    req = Request(url)
    req.add_header("User-Agent", "DEXAggregator/1.0")
    resp = urlopen(req, timeout=15)
    data = json.loads(resp.read().decode("utf-8"))
    pairs = data.get("pairs", [])
    
    filtered = [p for p in pairs if chain.lower() in (p.get("chainId", "") or "").lower()]
    filtered.sort(key=lambda x: (x.get("liquidity", {}).get("usd", 0) or 0), reverse=True)
    
    print("{:<4} {:<18} {:<20} {:>12} {:>12} {:>10}".format(
        "#", "DEX", "Pair", "Liquidity", "Volume 24h", "Price"))
    print("-" * 70)
    
    for i, p in enumerate(filtered[:15], 1):
        dex = p.get("dexId", "?")[:17]
        base = p.get("baseToken", {}).get("symbol", "?")
        quote = p.get("quoteToken", {}).get("symbol", "?")
        pair = "{}/{}".format(base, quote)[:19]
        liq = p.get("liquidity", {}).get("usd", 0) or 0
        vol = p.get("volume", {}).get("h24", 0) or 0
        price = p.get("priceUsd", "?")
        
        liq_str = "${:.1f}M".format(liq/1e6) if liq >= 1e6 else "${:.0f}K".format(liq/1e3) if liq >= 1e3 else "${:.0f}".format(liq)
        vol_str = "${:.1f}M".format(vol/1e6) if vol >= 1e6 else "${:.0f}K".format(vol/1e3) if vol >= 1e3 else "${:.0f}".format(vol)
        
        print("{:<4} {:<18} {:<20} {:>12} {:>12} {:>10}".format(
            i, dex, pair, liq_str, vol_str, "${}".format(price)[:10] if price != "?" else "?"))
    
    if not filtered:
        print("No pools found for {} on {}".format(token, chain))

except Exception as e:
    print("Error: {}".format(str(e)[:80]))
PYEOF
    ;;

  trending)
    CHAIN="${1:-ethereum}"
    python3 << 'PYEOF'
import sys, json, time
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

chain = sys.argv[1] if len(sys.argv) > 1 else "ethereum"

print("=" * 65)
print("TRENDING PAIRS — {}".format(chain.upper()))
print("=" * 65)
print("")

try:
    url = "https://api.dexscreener.com/latest/dex/search?q=trending%20{}".format(chain)
    req = Request(url)
    req.add_header("User-Agent", "DEXAggregator/1.0")
    resp = urlopen(req, timeout=15)
    data = json.loads(resp.read().decode("utf-8"))
    pairs = data.get("pairs", [])
    
    filtered = [p for p in pairs if chain.lower() in (p.get("chainId", "") or "").lower()]
    filtered.sort(key=lambda x: (x.get("volume", {}).get("h24", 0) or 0), reverse=True)
    
    for i, p in enumerate(filtered[:10], 1):
        base = p.get("baseToken", {})
        name = base.get("name", "?")[:25]
        symbol = base.get("symbol", "?")
        price = p.get("priceUsd", "?")
        change = p.get("priceChange", {}).get("h24", 0) or 0
        vol = p.get("volume", {}).get("h24", 0) or 0
        
        direction = "📈" if float(change) > 0 else "📉" if float(change) < 0 else "➡️"
        vol_str = "${:.1f}M".format(vol/1e6) if vol >= 1e6 else "${:.0f}K".format(vol/1e3)
        
        print("{}. {} {} ({}) — ${} ({:+.1f}%) Vol: {}".format(
            i, direction, name, symbol, price, float(change), vol_str))
    
    if not filtered:
        print("No trending pairs found. Try: ethereum, bsc, solana, base")

except Exception as e:
    print("Error: {}".format(str(e)[:80]))
PYEOF
    ;;

  gas)
    CHAIN="${1:-ethereum}"
    python3 << 'PYEOF'
import sys, json
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

chain = sys.argv[1] if len(sys.argv) > 1 else "ethereum"

gas_apis = {
    "ethereum": "https://api.etherscan.io/api?module=gastracker&action=gasoracle",
    "bsc": "https://api.bscscan.com/api?module=gastracker&action=gasoracle",
    "polygon": "https://api.polygonscan.com/api?module=gastracker&action=gasoracle"
}

print("=" * 50)
print("GAS PRICES — {}".format(chain.upper()))
print("=" * 50)
print("")

url = gas_apis.get(chain)
if url:
    try:
        req = Request(url)
        resp = urlopen(req, timeout=10)
        data = json.loads(resp.read().decode("utf-8"))
        result = data.get("result", {})
        
        if isinstance(result, dict):
            print("  🐢 Low: {} Gwei".format(result.get("SafeGasPrice", "?")))
            print("  🚶 Average: {} Gwei".format(result.get("ProposeGasPrice", "?")))
            print("  🚀 Fast: {} Gwei".format(result.get("FastGasPrice", "?")))
            
            # Estimated swap cost
            avg = float(result.get("ProposeGasPrice", 30))
            swap_gas = 150000
            swap_cost_eth = (avg * swap_gas) / 1e9
            print("")
            print("  Est. swap cost (~150K gas):")
            print("  {:.6f} ETH at average speed".format(swap_cost_eth))
    except Exception as e:
        print("Error: {}".format(str(e)[:50]))
else:
    print("Gas tracker not available for {}".format(chain))
    print("Available: ethereum, bsc, polygon")
PYEOF
    ;;

  help|*)
    cat << 'HELPEOF'
DEX Aggregator — Find best swap rates across DEXes

COMMANDS:
  quote <in> <out> <amount> [chain]  Compare swap rates
  pools <token> [chain]              Find liquidity pools
  trending [chain]                   Trending trading pairs
  gas [chain]                        Current gas prices

CHAINS: ethereum, bsc, polygon, arbitrum, base, solana

EXAMPLES:
  bash dex.sh quote ETH USDC 1 ethereum
  bash dex.sh quote SOL USDC 10 solana
  bash dex.sh pools UNI ethereum
  bash dex.sh trending base
  bash dex.sh gas ethereum
HELPEOF
    ;;
esac
echo ""
echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
