---
name: Delegation payments
description: Pay for x402-protected APIs using ERC-7710 delegations from a smart account
---

# Delegation payments

Use this workflow when you control the buyer smart account and want to automate payments programmatically. Best for AI agents and backend services.

## Install dependencies

```bash
npm install @x402/core @x402/fetch @metamask/x402 @metamask/smart-accounts-kit
```

## Create the buyer smart account

Create a public client for your target network, then create a MetaMask smart account. Ensure the smart account is funded with the required token (typically USDC):

```typescript
import { createPublicClient, http } from 'viem'
import { baseSepolia } from 'viem/chains'
import { Implementation, toMetaMaskSmartAccount } from '@metamask/smart-accounts-kit'
import { privateKeyToAccount } from 'viem/accounts'

const chain = baseSepolia
const publicClient = createPublicClient({ chain, transport: http() })

const account = privateKeyToAccount('<BUYER_PRIVATE_KEY>')

const buyerSmartAccount = await toMetaMaskSmartAccount({
  client: publicClient,
  implementation: Implementation.Hybrid,
  deployParams: [account.address, [], [], []],
  deploySalt: '0x',
  signer: { account },
})
```

## Create the x402 delegation provider

Use `createx402DelegationProvider` to create an ERC-7710 client that automatically creates, signs, and encodes open root delegations with the required caveats:

```typescript
import { createx402DelegationProvider } from '@metamask/smart-accounts-kit/experimental'
import { x402Erc7710Client } from '@metamask/x402'

const erc7710Client = new x402Erc7710Client({
  delegationProvider: createx402DelegationProvider({
    account: buyerSmartAccount,
  }),
})
```

For API reference, see [`createx402DelegationProvider`](https://docs.metamask.io/smart-accounts-kit/reference/x402.md).

## Register the client and wrap fetch

Register the ERC-7710 client for all EVM networks, then create an HTTP client and wrap `fetch` with automatic payment handling:

```typescript
import { x402Client, x402HTTPClient } from '@x402/core/client'
import { wrapFetchWithPayment } from '@x402/fetch'

const coreClient = new x402Client().register('eip155:*', erc7710Client)
const httpClient = new x402HTTPClient(coreClient)
const fetchWithPayment = wrapFetchWithPayment(fetch, httpClient)
```

## Make paid requests

Call protected endpoints using the wrapped fetch. It automatically handles 402 responses, creates the delegation payment, and retries the request:

```typescript
const response = await fetchWithPayment('https://api.example.com/paid-endpoint')
const data = await response.json()
```

For more details, see the [delegation payments guide](https://docs.metamask.io/smart-accounts-kit/development/guides/x402/buyer/delegations.md).
