# Integration Test: Base Sepolia

End-to-end test of the x402 payment flow on Base Sepolia testnet.

## What it does

1. Starts a local Express server with x402 paywall middleware (price: 0.001 USDC)
2. Verifies an unauthenticated request returns HTTP 402
3. Uses `@x402/fetch` with a funded wallet to auto-detect the 402, sign a payment, and retry
4. Verifies the retried request returns HTTP 200 with content

## Prerequisites

### 1. Wallet with testnet USDC on Base Sepolia

You need a wallet funded with USDC on Base Sepolia (chain ID 84532).

**Get testnet USDC:**
- Coinbase faucet: https://portal.cdp.coinbase.com/products/faucet
- Circle faucet: https://faucet.circle.com (select Base Sepolia, USDC)
- Alternatively, bridge testnet ETH to Base Sepolia and swap via a testnet DEX

**Get testnet ETH (for gas):**
- https://www.alchemy.com/faucets/base-sepolia
- https://portal.cdp.coinbase.com/products/faucet

### 2. CDP account (optional, for custom facilitator config)

The test uses the default Coinbase x402 facilitator, which is publicly accessible. No CDP account is required to run this test.

If you need to use a custom facilitator or hit rate limits:
1. Sign up at https://portal.cdp.coinbase.com
2. Create an API key pair
3. Set `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET` environment variables

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `X402_WALLET_PRIVATE_KEY` | Yes | Hex private key (with `0x` prefix) of a wallet funded with testnet USDC on Base Sepolia |
| `X402_PAYTO_ADDRESS` | Yes | Recipient wallet address (any valid `0x` address — can be your own) |

## Running

```bash
# Set env vars
export X402_WALLET_PRIVATE_KEY="0xYOUR_PRIVATE_KEY_HERE"
export X402_PAYTO_ADDRESS="0xYOUR_ADDRESS_HERE"

# Run the integration test
npm run test:integration
```

The test suite automatically skips when environment variables are not set, so `npm run test:integration` is always safe to run.

## Troubleshooting

- **"insufficient funds"**: Your wallet needs both testnet USDC (for the payment) and testnet ETH (for gas) on Base Sepolia
- **Timeout errors**: The Coinbase facilitator or Base Sepolia RPC may be slow — the test has a 120s timeout
- **Facilitator errors**: The public facilitator may rate-limit. Wait a few minutes and retry, or set up a CDP account
