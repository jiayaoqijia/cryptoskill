---
name: Seller endpoint setup
description: Set up an Express server with x402 payment middleware for ERC-7710 payments
---

# Seller endpoint setup

## Install dependencies

```bash
npm install @metamask/x402 @x402/core @x402/express cors express
```

## Create the Express server

Set up an Express app with CORS configured to expose the x402 payment headers:

```typescript
import express from 'express'
import cors from 'cors'

const app = express()

app.use(cors({
  exposedHeaders: ['PAYMENT-REQUIRED', 'PAYMENT-RESPONSE'],
}))
```

## Configure the facilitator client and resource server

Initialize an `HTTPFacilitatorClient` pointing to the MetaMask facilitator for your network, then create an `x402ResourceServer` and register the ERC-7710 server scheme so the middleware can parse and validate delegation-based payment payloads:

```typescript
import { HTTPFacilitatorClient } from '@x402/core/server'
import { paymentMiddleware, x402ResourceServer } from '@x402/express'
import { x402ExactEvmErc7710ServerScheme } from '@metamask/x402'

const facilitatorClient = new HTTPFacilitatorClient({
  url: '<FACILITATOR_URL>',
})

const resourceServer = new x402ResourceServer(facilitatorClient).register(
  'eip155:84532',
  new x402ExactEvmErc7710ServerScheme(),
)
```

MetaMask facilitator URLs by network:
- Base Sepolia: `https://tx-sentinel-base-sepolia.dev-api.cx.metamask.io/platform/v2/x402`
- Base: `https://tx-sentinel-base-mainnet.dev-api.cx.metamask.io/platform/v2/x402`
- Monad: `https://tx-sentinel-monad-mainnet.dev-api.cx.metamask.io/platform/v2/x402`

## Add payment middleware to protected routes

Define the payment requirements for each route and apply the middleware with the resource server:

```typescript
app.use(
  paymentMiddleware(
    {
      'GET /api/hello': {
        accepts: [{
          scheme: 'exact',
          price: '$0.01',
          network: 'eip155:84532',
          payTo: '<SELLER_ADDRESS>',
          extra: { assetTransferMethod: 'erc7710' },
        }],
        description: 'A paid hello endpoint',
        mimeType: 'application/json',
      },
    },
    resourceServer,
  ),
)
```

## Add the protected route handler

Define the route handler as usual. The payment middleware runs before your handler — by the time your handler executes, the payment has already been verified and settled through the facilitator:

```typescript
app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello, paid user!' })
})

app.listen(3000)
```

For more details, see the [seller endpoint guide](https://docs.metamask.io/smart-accounts-kit/development/guides/x402/seller.md).
