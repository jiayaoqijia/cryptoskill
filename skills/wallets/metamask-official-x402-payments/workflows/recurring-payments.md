---
name: Recurring payments
description: Set up recurring x402 payments using ERC-7715 Advanced Permissions with periodic budgets
---

# Recurring payments

Use this workflow when you want to request a periodic budget from a MetaMask user for ongoing API access. The permission resets each period, enabling subscription-style payment flows.

## Install dependencies

```bash
npm install @x402/core @x402/fetch @metamask/x402 @metamask/smart-accounts-kit
```

## Set up the wallet client

Create a viem wallet client connected to MetaMask and extend it with ERC-7715 actions. This enables the `requestExecutionPermissions` method needed to request periodic spending budgets from the user:

```typescript
import { createWalletClient, custom } from 'viem'
import { baseSepolia } from 'viem/chains'
import { erc7715ProviderActions } from '@metamask/smart-accounts-kit/actions'

const chain = baseSepolia

const walletClient = createWalletClient({
  chain,
  transport: custom(window.ethereum),
}).extend(erc7715ProviderActions())
```

## Create a session account

Generate a session key that will act on behalf of the user within the granted permission. This account signs x402 payment delegations without requiring the user's approval for each individual payment:

```typescript
import { privateKeyToAccount } from 'viem/accounts'

const sessionAccount = privateKeyToAccount('<SESSION_PRIVATE_KEY>')
```

## Request periodic permissions

Request a periodic ERC-20 permission that resets each period. This example requests 10 USDC per week for 30 days:

```typescript
import { parseUnits } from 'viem'

const currentTime = Math.floor(Date.now() / 1000)

const grantedPermissions = await walletClient.requestExecutionPermissions([
  {
    chainId: chain.id,
    expiry: currentTime + 30 * 86400,
    to: sessionAccount.address,
    permission: {
      type: 'erc20-token-periodic',
      data: {
        tokenAddress: '<TOKEN_ADDRESS>',
        periodAmount: parseUnits('10', 6),
        periodDuration: 604800,
        justification: 'Weekly budget for API access',
      },
      isAdjustmentAllowed: true,
    },
  },
])
```

## Create the x402 delegation provider

Use `createx402DelegationProvider` with the granted permission context. This sets up open redelegation so facilitators can redeem payments within the granted budget:

```typescript
import { createx402DelegationProvider } from '@metamask/smart-accounts-kit/experimental'
import { x402Erc7710Client } from '@metamask/x402'

const permission = grantedPermissions[0]

const erc7710Client = new x402Erc7710Client({
  delegationProvider: createx402DelegationProvider({
    account: sessionAccount,
    parentPermissionContext: permission.context,
    from: permission.from,
  }),
})
```

For API reference, see [`createx402DelegationProvider`](https://docs.metamask.io/smart-accounts-kit/reference/x402.md).

## Register and wrap fetch

Register the ERC-7710 client for all EVM networks, then create an HTTP client and wrap `fetch` with automatic payment handling. When a server responds with HTTP 402, the wrapped fetch creates a payment within the granted budget and retries the request:

```typescript
import { x402Client, x402HTTPClient } from '@x402/core/client'
import { wrapFetchWithPayment } from '@x402/fetch'

const coreClient = new x402Client().register('eip155:*', erc7710Client)
const httpClient = new x402HTTPClient(coreClient)
const fetchWithPayment = wrapFetchWithPayment(fetch, httpClient)
```

## Make recurring paid requests

Each call automatically handles x402 payment within the granted periodic budget:

```typescript
const response = await fetchWithPayment('https://api.example.com/paid-endpoint')
const data = await response.json()
```

The periodic budget resets at the start of each new period. The user doesn't need to approve each individual payment.

For more details, see the [recurring payments guide](https://docs.metamask.io/smart-accounts-kit/development/guides/x402/buyer/recurring-payments.md).
