# x402 Payment Skill

Pay for resources using the x402 HTTP payment protocol. Enables agents to pay for compute, domains, APIs, and other services using USDC on Base — no accounts, no KYC, just cryptographic identity.

## What is x402?

HTTP 402 "Payment Required" was reserved in the original HTTP spec but never standardized. The [x402 protocol](https://x402.org) implements it for machine-to-machine payments:

1. Request a paid resource → get HTTP 402 + payment requirements
2. Sign an EIP-3009 `transferWithAuthorization` (gasless USDC transfer)
3. Resubmit with `X-Payment` header containing the signed authorization
4. Payment verified on-chain → resource granted

No API keys. No accounts. Pure wallet → payment → access.

## Prerequisites

- An Ethereum wallet with private key
- USDC on Base (chain ID 8453)
- Node.js with `viem` installed

## Usage

### Basic x402 Fetch

```javascript
import { x402Fetch } from './x402.mjs';
import { privateKeyToAccount } from 'viem/accounts';

// Load your wallet (NEVER hardcode keys!)
const account = privateKeyToAccount(process.env.PRIVATE_KEY);

// Fetch with automatic x402 payment
const response = await x402Fetch(account, 'https://api.example.com/paid-resource');
const data = await response.json();
```

### Manual Payment Flow

For more control, use the individual functions:

```javascript
import { parsePaymentRequired, createPaymentSignature, encodePaymentHeader } from './x402.mjs';

// 1. Make initial request
const response = await fetch(url);

if (response.status === 402) {
  // 2. Parse payment requirements
  const requirements = await parsePaymentRequired(response);
  
  // 3. Find supported option (Base USDC)
  const option = requirements.accepts.find(
    a => a.scheme === 'exact' && a.network === 'eip155:8453'
  );
  
  // 4. Sign payment
  const payment = await createPaymentSignature(account, option, requirements.x402Version);
  
  // 5. Retry with payment header
  const paidResponse = await fetch(url, {
    headers: { 'X-Payment': encodePaymentHeader(payment) }
  });
}
```

## Scripts

### `x402.mjs` — Core Library

The main x402 implementation. Functions:

- `parsePaymentRequired(response)` — Parse 402 response for payment requirements
- `createPaymentSignature(account, requirement, version)` — Sign EIP-3009 authorization
- `encodePaymentHeader(payload)` — Base64 encode for X-Payment header
- `x402Fetch(account, url, options)` — Fetch with automatic payment handling

### `conway-credits.mjs` — Conway Compute Credits

Top up Conway compute credits:

```bash
PRIVATE_KEY=0x... node conway-credits.mjs 5
# Tops up $5 in Conway credits
```

### `conway-domain.mjs` — Conway Domain Registration

Register domains via Conway:

```bash
PRIVATE_KEY=0x... node conway-domain.mjs example.com
```

## Wallet Security

**NEVER commit private keys to version control.**

Recommended patterns:
- Environment variables: `process.env.PRIVATE_KEY`
- Secure file with restricted permissions: `chmod 600 wallet.json`
- Hardware wallet via WalletConnect (advanced)

## Supported Networks

| Network | Chain ID | USDC Address |
|---------|----------|--------------|
| Base | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Base Sepolia | 84532 | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

## Known x402 Providers

- **Conway** — Compute, inference, domains (conway.tech)
- **Farcaster Hub** — Some hubs accept x402 for API access

## References

- [x402 Protocol Spec](https://x402.org)
- [EIP-3009: Transfer With Authorization](https://eips.ethereum.org/EIPS/eip-3009)
- [Conway Documentation](https://docs.conway.tech)

## Author

Built by [Lumen](https://x.com/LumenFTFuture) — March 2026

First successful x402 payment: TX `0xba5eaf2e4f1c7b9f79581c1771adc2527b2029dbbc900c429d3f69eafe6d3ba7`
