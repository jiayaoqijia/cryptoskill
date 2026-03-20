---
name: x402-client
description: Make paid API requests using the x402 HTTP payment protocol (USDC on Base Sepolia). Use when you need to access x402-protected services, pay for API calls with crypto, or perform web searches via an x402 search gateway. Handles wallet setup, payment signing, and request retry automatically.
---

# x402 Client

Make HTTP requests to x402-protected APIs. The x402 protocol uses HTTP 402 responses to request payment — this skill handles signing USDC payments and retrying automatically.

## Prerequisites

- Node.js 18+ installed
- A Base Sepolia wallet with ETH (gas) and USDC (payments)

## First-Time Setup

### 1. Install dependencies

```bash
bash <skill-dir>/scripts/setup.sh
```

This installs the x402 SDK to `~/.x402-client/`. Only needed once.

### 2. Generate a wallet (if you don't have one)

```bash
node <skill-dir>/scripts/wallet-gen.mjs --out ~/.x402-client/wallet.key
```

### 3. Fund the wallet

Get testnet tokens from faucets:

- **Base Sepolia ETH** (gas): https://www.alchemy.com/faucets/base-sepolia
- **Base Sepolia USDC** (payments): https://faucet.circle.com/ → select Base Sepolia + USDC

Send both to the wallet address printed by wallet-gen.

### 4. Store the key

Set the environment variable for future use:

```bash
export X402_PRIVATE_KEY=$(cat ~/.x402-client/wallet.key)
```

Or pass `--key-file ~/.x402-client/wallet.key` to each request.

## Making Paid Requests

Use `x402-fetch.mjs` to make any x402-paid HTTP request:

```bash
# Search the web ($0.001 USDC per query)
node <skill-dir>/scripts/x402-fetch.mjs \
  "https://<service-url>/web/search?q=latest+AI+news&count=5" \
  --key-file ~/.x402-client/wallet.key
```

The script automatically:
1. Makes the HTTP request
2. If 402 received, parses payment requirements
3. Signs a USDC payment with your wallet
4. Retries with the payment header
5. Outputs the response JSON to stdout

All scripts must be run from `~/.x402-client/` (where node_modules lives):

```bash
cd ~/.x402-client && node <skill-dir>/scripts/x402-fetch.mjs "<url>" --key-file wallet.key
```

## Known Services

See [references/services.md](references/services.md) for a list of known x402 endpoints including a web search service.

## Troubleshooting

- **"insufficient funds"**: Wallet needs more USDC or ETH. Use faucets above.
- **402 with no auto-payment**: Ensure setup.sh was run and you're executing from `~/.x402-client/`.
- **Tunnel URL not working**: The service URL may have changed. Ask the service operator or check `/health`.
