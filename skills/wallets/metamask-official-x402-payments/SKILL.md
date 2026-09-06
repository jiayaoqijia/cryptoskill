---
name: x402-payments
description: Build x402 payment flows using MetaMask Smart Accounts Kit, machine to machine payments over HTTP with ERC-7710 delegations and ERC-7715 Advanced Permissions
---

# x402 Payments

x402 is an open payment protocol that uses the HTTP 402 status code to enable programmatic, machine-to-machine payments over HTTP. It lets servers charge for API access without requiring traditional payment infrastructure, buyer accounts, or API keys.

## When to use

- You want to charge for API access using onchain payments.
- You want to build AI agents that pay per request for API resources.
- You want to enable micro payments for premium data or services.
- You want to set up recurring payments with periodic budgets.
- You want to use MetaMask smart account delegations for x402 settlement.

## Installation

```bash
npm install @x402/core @x402/fetch @metamask/x402 @metamask/smart-accounts-kit
```

For seller endpoints:

```bash
npm install @x402/core @x402/express @metamask/x402
```

## How x402 works

1. The buyer sends a request to a protected endpoint.
2. The server responds with HTTP 402 and a `PAYMENT-REQUIRED` header containing payment terms.
3. The buyer creates a payment payload (delegation or permission) matching the terms.
4. The buyer resends the request with the payment in the `PAYMENT-SIGNATURE` header.
5. The server validates the payment through a facilitator and returns the resource.

## x402 ERC-7710 payments

The standard x402 protocol supports direct token transfers (using ERC-20 Permit2 or EIP-3009). ERC-7710 extends this by enabling delegation-based payments from MetaMask smart accounts.

With ERC-7710, a buyer's smart account creates a delegation that authorizes the facilitator to transfer tokens on their behalf. The buyer doesn't sign a direct token approval. Instead, they sign a delegation that the facilitator redeems during settlement.

This approach enables buyers to pay from MetaMask wallet. Buyers can restrict delegations to specific facilitator addresses, amounts, and time windows using delegation scopes. They can also create long-lived delegations that allow recurring payments without re-signing for each request.

## Workflows

| Workflow | Use case |
|----------|----------|
| [Seller endpoint setup](./workflows/seller-endpoint-setup.md) | You want to protect API endpoints with x402 payment requirements. |
| [Delegation payments](./workflows/delegation-payments.md) | You control the buyer smart account and want to automate payments programmatically. |
| [Advanced Permissions (recurring)](./workflows/recurring-payments.md) | You want to request a periodic budget from a MetaMask user for ongoing API access. Best for subscriptions and recurring usage. |

If the user hasn't specified which payment method they need, present the options.

## Supported networks

| Network | Chain ID | Facilitator URL |
|---------|----------|-----------------|
| Base | eip155:8453 | `https://tx-sentinel-base-mainnet.dev-api.cx.metamask.io/platform/v2/x402` |
| Base Sepolia | eip155:84532 | `https://tx-sentinel-base-sepolia.dev-api.cx.metamask.io/platform/v2/x402` |
| Monad | eip155:143 | `https://tx-sentinel-monad-mainnet.dev-api.cx.metamask.io/platform/v2/x402` |

## Resources

- x402 protocol: https://www.x402.org/
- Smart Accounts Kit docs: https://docs.metamask.io/smart-accounts-kit
- [x402 overview](https://docs.metamask.io/smart-accounts-kit/guides/x402/overview.md)
