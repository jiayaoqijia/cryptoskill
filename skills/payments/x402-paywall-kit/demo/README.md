# Demo: Paywalled API + Agent That Pays It

A runnable demo of the x402-kit: an Express API that charges 0.01 USDC per joke, and an AI agent that auto-pays for it. Runs on Base Sepolia testnet.

## What It Does

1. **Server** (`server.ts`): Express app with `GET /api/joke` behind an x402 paywall (0.01 USDC)
2. **Agent** (`agent.ts`): Calls the server, auto-detects the 402 paywall, pays via x402 protocol, prints the joke

## Prerequisites

### 1. Node.js 18+

```bash
node --version  # Must be >= 18
```

### 2. Wallet with testnet USDC on Base Sepolia

You need a wallet funded with USDC on Base Sepolia (chain ID 84532).

**Get testnet USDC:**
- Circle faucet: https://faucet.circle.com (select Base Sepolia, USDC)
- Coinbase faucet: https://portal.cdp.coinbase.com/products/faucet

**Get testnet ETH (for gas):**
- https://www.alchemy.com/faucets/base-sepolia
- https://portal.cdp.coinbase.com/products/faucet

### 3. Two terminal windows

The server and agent run as separate processes.

## Setup

From the repo root:

```bash
# Install dependencies
npm install

# Build all packages
npm run build
```

## Environment Variables

| Variable | Required | Used By | Description |
|----------|----------|---------|-------------|
| `X402_WALLET_PRIVATE_KEY` | Yes | Agent | Hex private key (`0x...`) of a wallet funded with testnet USDC on Base Sepolia |
| `X402_PAYTO_ADDRESS` | Yes | Server | Recipient wallet address — any valid `0x` address (can be your own) |

```bash
export X402_WALLET_PRIVATE_KEY="0xYourPrivateKeyHere"
export X402_PAYTO_ADDRESS="0xYourAddressHere"
```

## Running

### Terminal 1: Start the server

```bash
npx tsx demo/server.ts
```

Expected output:
```
x402-kit demo server running on http://localhost:3000
  Paywalled:  GET http://localhost:3000/api/joke (0.01 USDC)
  Free:       GET http://localhost:3000/health
  Payments to: 0xYourAddress
  Network:    Base Sepolia (eip155:84532)

Waiting for requests...
```

### Terminal 2: Run the agent

```bash
npx tsx demo/agent.ts
```

Expected output:
```
x402-kit Demo Agent
===================
Server: http://localhost:3000
Network: Base Sepolia (eip155:84532)

1. Checking server health...
   Server is healthy.

2. Requesting joke from paywalled endpoint...
   GET http://localhost:3000/api/joke

3. Payment successful! Got a joke:

   "Why do programmers prefer dark mode? Because light attracts bugs."

   Paid: 0.01 USDC via x402 protocol
   Network: Base Sepolia

Check ./demo/payments-agent.jsonl for the payment log.
```

## How It Works

1. Agent sends `GET /api/joke` to the server
2. Server's `x402EnhancedMiddleware` returns HTTP 402 with payment requirements
3. Agent's `createAgentFetch` detects the 402, parses x402 requirements
4. Agent's policy engine checks: amount within limits? Network allowed? Asset allowed?
5. If approved: agent signs an EIP-3009 USDC transfer authorization
6. Agent retries the request with the signed payment in the `X-PAYMENT` header
7. Server's middleware verifies the payment via the Coinbase facilitator
8. On success: server settles the payment on-chain and returns the joke
9. Both sides log the payment event to their respective JSONL files

## Payment Logs

After a successful run, check the payment logs:

- **Server log**: `demo/payments-server.jsonl`
- **Agent log**: `demo/payments-agent.jsonl`

## Troubleshooting

- **"Server not reachable"**: Make sure the server is running in Terminal 1 before starting the agent.
- **"Payment was not made"**: Check that your wallet has testnet USDC and ETH on Base Sepolia. Verify the env vars are set correctly.
- **"insufficient funds"**: Your wallet needs both testnet USDC (for the payment) and testnet ETH (for gas) on Base Sepolia.
- **Timeout errors**: The Coinbase facilitator or Base Sepolia RPC may be slow. Try again after a moment.
- **Facilitator errors**: The public facilitator may rate-limit. Wait a few minutes and retry.
