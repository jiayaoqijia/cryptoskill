---
name: commerce
description: End-to-end agentic commerce workflow using Lightning Network. Use when an agent needs to set up a full payment stack (lnd + lnget + aperture), buy or sell data via L402, or enable agent-to-agent micropayments.
user-invocable: false
---

# Agentic Commerce Toolkit

This plugin provides a complete toolkit for agent-driven Lightning Network
commerce. Three skills work together to enable agents to send and receive
micropayments over the Lightning Network using the L402 protocol.

## Components

| Skill | Purpose |
|-------|---------|
| **lnd** | Run Lightning Terminal (litd: lnd + loop + pool + tapd) |
| **lnget** | Fetch L402-protected resources (pay for data) |
| **aperture** | Host paid API endpoints (sell data) |

## Full Setup Workflow

### Step 1: Install All Components

```bash
# Install litd (Lightning Terminal — bundles lnd + loop + pool + tapd)
skills/lnd/scripts/install.sh

# Install lnget (Lightning HTTP client)
skills/lnget/scripts/install.sh

# Install aperture (L402 reverse proxy)
skills/aperture/scripts/install.sh
```

### Step 2: Set Up the Lightning Node

```bash
# Start litd container (testnet by default)
skills/lnd/scripts/start-lnd.sh

# Create an encrypted wallet
skills/lnd/scripts/create-wallet.sh --mode standalone

# Verify node is running
skills/lnd/scripts/lncli.sh getinfo
```

### Step 3: Fund the Wallet

```bash
# Generate a Bitcoin address
skills/lnd/scripts/lncli.sh newaddress p2tr

# Send BTC to this address from an exchange or another wallet

# Verify balance
skills/lnd/scripts/lncli.sh walletbalance
```

### Step 4: Open a Channel

```bash
# Connect to a well-connected node (e.g., ACINQ, Bitfinex)
skills/lnd/scripts/lncli.sh connect <pubkey>@<host>:9735

# Open a channel
skills/lnd/scripts/lncli.sh openchannel --node_key=<pubkey> --local_amt=1000000

# Wait for channel to confirm (6 blocks)
skills/lnd/scripts/lncli.sh listchannels
```

### Step 5: Configure lnget

```bash
# Initialize lnget config (auto-detects local lnd)
lnget config init

# Verify connection
lnget ln status
```

### Step 6: Fetch Paid Resources

```bash
# Fetch an L402-protected resource
lnget --max-cost 1000 https://api.example.com/paid-data

# Preview without paying
lnget --no-pay https://api.example.com/paid-data

# Check cached tokens
lnget tokens list
```

### Step 7: Host Paid Endpoints (Optional)

```bash
# Start your backend service
python3 -m http.server 8080 &

# Configure aperture to protect it
skills/aperture/scripts/setup.sh --insecure --port 8081

# Start the L402 paywall
skills/aperture/scripts/start.sh

# Other agents can now pay to access your endpoints
# lnget --max-cost 100 https://your-host:8081/api/data
```

## Agent-to-Agent Commerce

The full loop for autonomous agent commerce:

```
Agent A (buyer)                    Agent B (seller)
─────────────                      ─────────────
lnd node running                   lnd node running
  ↓                                  ↓
lnget fetches URL ──────────────→ aperture receives request
                                     ↓
                                   Returns 402 + invoice
  ↓
lnget pays invoice ─────────────→ lnd receives payment
  ↓                                  ↓
lnget retries with token ───────→ aperture validates token
                                     ↓
                                   Proxies to backend
  ↓                                  ↓
Agent A receives data ←──────────  Backend returns data
```

### Buyer Agent Setup

```bash
# One-time setup
skills/lnd/scripts/install.sh
skills/lnget/scripts/install.sh
skills/lnd/scripts/start-lnd.sh
skills/lnd/scripts/create-wallet.sh --mode standalone
lnget config init

# Fund wallet and open channels (one-time)
skills/lnd/scripts/lncli.sh newaddress p2tr
# ... send BTC ...
skills/lnd/scripts/lncli.sh openchannel --node_key=<pubkey> --local_amt=500000

# Ongoing: fetch paid resources
lnget --max-cost 100 -q https://seller-api.example.com/api/data | jq .
```

### Seller Agent Setup

```bash
# One-time setup
skills/lnd/scripts/install.sh
skills/aperture/scripts/install.sh
skills/lnd/scripts/start-lnd.sh
skills/lnd/scripts/create-wallet.sh --mode standalone

# Configure and start paywall
skills/aperture/scripts/setup.sh --port 8081 --insecure

# Start backend with content to sell
mkdir -p /tmp/api-data
echo '{"market_data": "..."}' > /tmp/api-data/data.json
cd /tmp/api-data && python3 -m http.server 8080 &

# Start aperture
skills/aperture/scripts/start.sh

# Buyers can now access:
# https://your-host:8081/api/data.json (100 sats per request)
```

## Cost Management

Agents should always control spending:

```bash
# Set a hard limit per request
lnget --max-cost 500 https://api.example.com/data

# Check cost before paying
lnget --no-pay --json https://api.example.com/data | jq '.invoice_amount_sat'

# Track spending via token list
lnget tokens list --json | jq '[.[] | .amount_paid_sat] | add'
```

## Security Summary

| Component | Security Model |
|-----------|---------------|
| **Wallet passphrase** | Stored at `~/.lnget/lnd/wallet-password.txt` (0600) |
| **Seed mnemonic** | Stored at `~/.lnget/lnd/seed.txt` (0600) |
| **L402 tokens** | Stored at `~/.lnget/tokens/<domain>/` per domain |
| **lnd macaroons** | Standard lnd paths at `~/.lnd/data/chain/...` |
| **Aperture DB** | SQLite at `~/.aperture/aperture.db` |

For production use with significant funds, use watch-only mode with a remote
signer container. See the `lightning-security-module` skill for details.

## Stopping Everything

```bash
skills/aperture/scripts/stop.sh
skills/lnd/scripts/stop-lnd.sh
```
