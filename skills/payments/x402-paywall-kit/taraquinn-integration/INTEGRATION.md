# Adding x402 Paywall Kit to taraquinn.ai

Step-by-step guide for adding the product to the taraquinn.ai Products page with both Stripe and USDC payment options.

## Overview

| Payment Method | Flow | Status |
|---------------|------|--------|
| Stripe (card) | Product card -> Stripe Checkout -> email delivery | Ready to implement |
| USDC (crypto) | Product card -> 402 paywall -> wallet sign -> download | Ready to implement |

## Files in This Directory

| File | Purpose |
|------|---------|
| `product.json` | Product metadata (name, price, features, links) |
| `product-card.tsx` | React component for the Products page |
| `stripe-checkout.ts` | Stripe Checkout session config and examples |
| `usdc-paywall.ts` | x402 USDC payment config using our own middleware |

## Step 1: Create Stripe Product

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/products) -> Products -> Add Product
2. Name: "x402 Paywall Kit"
3. Price: $29.00 (one-time)
4. Save the **Price ID** (starts with `price_`)
5. Add to `.env`:
   ```
   STRIPE_PRICE_ID=price_xxxxxxxxxxxxx
   ```

## Step 2: Add API Endpoints

### Stripe Checkout Endpoint

Create `/api/checkout/x402-paywall-kit` using the example in `stripe-checkout.ts`.

Key config:
- Price: `$29` (from `STRIPE_PRICE_ID`)
- Success URL: `/products/x402-paywall-kit/success?session_id={CHECKOUT_SESSION_ID}`
- Metadata: `{ product: "x402-paywall-kit", version: "1.0.0" }`

### USDC Payment Endpoint

Create `/api/products/x402-paywall-kit/download` using `@x402-kit/express`:

```typescript
import { x402EnhancedMiddleware } from "@x402-kit/express";

app.use(
  x402EnhancedMiddleware({
    routes: {
      "GET /api/products/x402-paywall-kit/download": {
        price: "$29.00",
        recipient: process.env.X402_PAYTO_ADDRESS!,
        network: "eip155:8453",
        description: "x402 Paywall Kit — one-time purchase",
      },
    },
    logFilePath: "./logs/x402-sales.jsonl",
  }),
);
```

Add to `.env`:
```
X402_PAYTO_ADDRESS=0x5b99070C84aB6297F2c1a25490c53eE483C8B499
```

## Step 3: Add Product Card to Products Page

Use the `product-card.tsx` component or adapt for the existing product card style:

```tsx
<X402PaywallKitCard
  stripeCheckoutUrl="/api/checkout/x402-paywall-kit"
  usdcPaymentUrl="/api/products/x402-paywall-kit/download"
/>
```

## Step 4: Email Delivery (Stripe)

Same flow as Business Starter:

1. Handle `checkout.session.completed` webhook event
2. Extract customer email from the session
3. Send email with:
   - Download link (GitHub release tarball or signed URL)
   - Getting started instructions
   - NPM package names for quick install

## Step 5: Download Delivery (USDC)

After successful x402 payment, the endpoint returns:

```json
{
  "product": "x402-paywall-kit",
  "version": "1.0.0",
  "downloadUrl": "https://github.com/tara-quinn-ai/x402-kit/archive/refs/tags/v1.0.0.tar.gz"
}
```

The frontend should redirect to or trigger download of the URL.

## Environment Variables

| Variable | Where | Description |
|----------|-------|-------------|
| `STRIPE_SECRET_KEY` | taraquinn.ai `.env` | Stripe secret key |
| `STRIPE_PRICE_ID` | taraquinn.ai `.env` | Price ID for the $29 product |
| `STRIPE_WEBHOOK_SECRET` | taraquinn.ai `.env` | For webhook signature verification |
| `X402_PAYTO_ADDRESS` | taraquinn.ai `.env` | Tara's wallet for USDC payments |
| `SITE_URL` | taraquinn.ai `.env` | Base URL (e.g., `https://taraquinn.ai`) |

## Testing

1. **Stripe**: Use test mode + test card `4242 4242 4242 4242`
2. **USDC**: Test on Base Sepolia first (`eip155:84532`), then switch to mainnet
3. **Email**: Verify delivery email arrives with correct download link
4. **End-to-end**: Complete a purchase through each payment method
