# AI Agent Workflows

Example workflows for AI agents using the Alchemy skill to automate blockchain monitoring, analysis, and actions.

## 1. Whale Wallet Tracker

Monitor large wallets for significant moves.

```bash
#!/bin/bash
# whale-tracker.sh - Run every hour via cron

WHALE="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
DATA_DIR="$HOME/.openclaw/workspace/data/whales"
mkdir -p "$DATA_DIR"

# Get recent transfers
~/.openclaw/workspace/skills/alchemy-web3/scripts/alchemy.sh transfers "$WHALE" --raw > "$DATA_DIR/latest.json"

# Agent analyzes for large moves (>100 ETH)
# If found → send alert to Telegram/Discord
```

**Cron setup:**
```bash
# Every hour, check whale activity
0 * * * * /path/to/whale-tracker.sh
```

---

## 2. Portfolio Monitor

Track your own wallet across multiple chains.

```bash
#!/bin/bash
# portfolio-check.sh

WALLET="0x76D75605C770d6B17eFE12C17C001626D371710a"
OUTPUT="$HOME/.openclaw/workspace/data/portfolio.json"

echo "{" > "$OUTPUT"

for chain in eth-mainnet polygon-mainnet arb-mainnet base-mainnet; do
    echo "Checking $chain..."
    
    # Get balances
    balance=$(~/.openclaw/workspace/skills/alchemy-web3/scripts/alchemy.sh --chain "$chain" balance "$WALLET" 2>/dev/null)
    
    echo "\"$chain\": \"$balance\"," >> "$OUTPUT"
done

echo "\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" >> "$OUTPUT"
echo "}" >> "$OUTPUT"

echo "Portfolio saved to $OUTPUT"
```

---

## 3. NFT Floor Price Alert

Monitor collections and alert on price drops.

```bash
#!/bin/bash
# nft-floor-alert.sh

COLLECTIONS=(
    "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"  # BAYC
    "0x60E4d786628Fea6478F785A6d7e704777c86a7c6"  # MAYC
    "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB"  # CryptoPunks
)

for contract in "${COLLECTIONS[@]}"; do
    floor=$(curl -s "https://eth-mainnet.g.alchemy.com/nft/v3/$ALCHEMY_API_KEY/getFloorPrice?contractAddress=$contract" | jq -r '.openSea.floorPrice // "N/A"')
    
    echo "$contract: $floor ETH"
    
    # Agent can compare to previous, alert if >10% drop
done
```

---

## 4. Token Balance Change Detector

Detect when tokens enter/leave a wallet.

```python
# token-monitor.py
import json
import subprocess
from datetime import datetime

WALLET = "0x..."
STATE_FILE = "token-state.json"

def get_tokens():
    result = subprocess.run([
        "./alchemy.sh", "tokens", WALLET, "--raw"
    ], capture_output=True, text=True)
    return json.loads(result.stdout)

def load_previous():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)

# Compare current vs previous
current = get_tokens()
previous = load_previous()

for token in current['result']['tokenBalances']:
    addr = token['contractAddress']
    balance = token['tokenBalance']
    
    if addr in previous and previous[addr] != balance:
        print(f"CHANGE: {addr} {previous[addr]} -> {balance}")
        # Agent action: log, alert, or respond

save_state({t['contractAddress']: t['tokenBalance'] 
            for t in current['result']['tokenBalances']})
```

---

## 5. Gas Price Optimizer

Wait for low gas to execute transactions.

```bash
#!/bin/bash
# wait-for-gas.sh

TARGET_GWEI=20

while true; do
    gas=$(~/.openclaw/workspace/skills/alchemy-web3/scripts/alchemy.sh gas | grep -oE '[0-9.]+')
    
    echo "Current gas: $gas Gwei (target: $TARGET_GWEI)"
    
    if (( $(echo "$gas < $TARGET_GWEI" | bc -l) )); then
        echo "Gas is low! Execute transaction now."
        # Agent triggers transaction
        break
    fi
    
    sleep 60
done
```

---

## 6. New NFT Mint Detector

Watch for new mints in a collection.

```bash
#!/bin/bash
# mint-detector.sh

CONTRACT="0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
LAST_SEEN_FILE="last-token-id.txt"

# Get latest token
latest=$(curl -s "https://eth-mainnet.g.alchemy.com/nft/v3/$ALCHEMY_API_KEY/getNFTsForContract?contractAddress=$CONTRACT&limit=1&orderBy=transferTime" | jq -r '.nfts[0].tokenId')

last_seen=$(cat "$LAST_SEEN_FILE" 2>/dev/null || echo "0")

if [ "$latest" != "$last_seen" ]; then
    echo "NEW MINT: Token #$latest"
    echo "$latest" > "$LAST_SEEN_FILE"
    # Agent action: alert, analyze, or auto-bid
fi
```

---

## 7. Multi-Wallet Dashboard Generator

Generate HTML dashboard of all wallets.

```bash
#!/bin/bash
# generate-dashboard.sh

WALLETS=(
    "0x76D75605C770d6B17eFE12C17C001626D371710a"
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
)

OUTPUT="$HOME/.openclaw/workspace/data/dashboard.html"

cat > "$OUTPUT" << 'EOF'
<!DOCTYPE html>
<html><head><title>Wallet Dashboard</title></head>
<body style="font-family: monospace; background: #0a0a0a; color: #fff; padding: 20px;">
<h1>Wallet Dashboard</h1>
EOF

for wallet in "${WALLETS[@]}"; do
    balance=$(~/.openclaw/workspace/skills/alchemy-web3/scripts/alchemy.sh balance "$wallet" 2>/dev/null | grep -oE '[0-9.]+')
    nft_count=$(~/.openclaw/workspace/skills/alchemy-web3/scripts/alchemy.sh nfts "$wallet" 2>/dev/null | grep -oE 'NFTs owned: [0-9]+' | grep -oE '[0-9]+')
    
    cat >> "$OUTPUT" << EOF
<div style="border: 1px solid #333; padding: 15px; margin: 10px 0;">
  <code>${wallet:0:12}...</code><br>
  <b>$balance ETH</b> | $nft_count NFTs
</div>
EOF
done

echo "</body></html>" >> "$OUTPUT"
echo "Dashboard: $OUTPUT"
```

---

## Agent Integration Pattern

```
┌─────────────────────────────────────────────────────┐
│                    AI AGENT                          │
│                                                      │
│  1. QUERY    ─────► alchemy.sh nfts 0x...           │
│                           │                          │
│  2. STORE    ◄───── workspace/data/nfts.json        │
│                           │                          │
│  3. ANALYZE  ─────► compare, filter, score          │
│                           │                          │
│  4. DECIDE   ─────► threshold crossed?              │
│                           │                          │
│  5. ACT      ─────► alert / trade / report          │
│                           │                          │
│  6. REPEAT   ─────► cron schedule                   │
└─────────────────────────────────────────────────────┘
```

The agent treats blockchain data like any other data source - query, store, process, act.
