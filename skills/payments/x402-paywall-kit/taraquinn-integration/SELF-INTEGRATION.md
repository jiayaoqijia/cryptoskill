# Self-Integration: x402 USDC Payments on taraquinn.ai

End-to-end guide for adding "Pay with USDC" to taraquinn.ai products using our own x402 middleware. This is the dogfooding step — we use the same tools we sell.

## Architecture

```
User clicks "Pay with USDC"
  │
  ▼
Browser: fetch(/api/products/x402-paywall-kit/download)
  │
  ▼
Server: x402EnhancedMiddleware returns 402 + payment requirements
  │
  ▼
Browser: useX402Payment hook parses requirements
  │
  ▼
Browser: Wallet popup → user signs EIP-3009 authorization (no gas!)
  │
  ▼
Browser: Retry with X-PAYMENT header
  │
  ▼
Server: Coinbase facilitator verifies + settles on Base
  │
  ▼
Server: Returns download URL
  │
  ▼
Browser: Redirects to download
```

Key: The user never leaves taraquinn.ai. The EIP-3009 signature authorizes a USDC transfer without gas fees — the Coinbase facilitator handles on-chain settlement.

## Files in This Directory

| File | Purpose |
|------|---------|
| `wagmi-config.ts` | Wagmi config for Base + Base Sepolia with injected wallet connector |
| `use-x402-payment.ts` | React hook — manages the full 402 → sign → retry flow |
| `pay-with-usdc-button.tsx` | "Pay with USDC" button component with wallet connect + status UI |
| `usdc-paywall.ts` | Server-side middleware config (from Task 3.4) |
| `product-card.tsx` | Product card with both Stripe and USDC buttons (from Task 3.4) |

## Step 1: Install Dependencies

```bash
npm install @x402-kit/express @x402/fetch @x402/evm wagmi viem @tanstack/react-query
```

## Step 2: Add Wagmi Provider (App Root)

```tsx
// app/layout.tsx or _app.tsx
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { wagmiConfig } from "@/lib/wagmi-config";

const queryClient = new QueryClient();

export default function RootLayout({ children }) {
  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

## Step 3: Add Server Middleware

```typescript
// Server endpoint (Express or Next.js API route)
import { x402EnhancedMiddleware } from "@x402-kit/express";

app.use(
  x402EnhancedMiddleware({
    routes: {
      "GET /api/products/x402-paywall-kit/download": {
        price: "$29.00",
        recipient: "0x5b99070C84aB6297F2c1a25490c53eE483C8B499", // Tara's wallet
        network: "eip155:8453", // Base mainnet
        description: "x402 Paywall Kit — one-time purchase",
      },
    },
    logFilePath: "./logs/x402-sales.jsonl",
  }),
);

app.get("/api/products/x402-paywall-kit/download", (req, res) => {
  res.json({
    downloadUrl: "https://github.com/tara-quinn-ai/x402-kit/archive/refs/tags/v1.0.0.tar.gz",
    product: "x402-paywall-kit",
    version: "1.0.0",
  });
});
```

## Step 4: Add "Pay with USDC" Button

```tsx
// products/x402-paywall-kit/page.tsx
import { PayWithUsdcButton } from "@/components/pay-with-usdc-button";

export default function ProductPage() {
  return (
    <div>
      <h1>x402 Paywall Kit — $29</h1>

      {/* Stripe checkout */}
      <a href="/api/checkout/x402-paywall-kit">
        <button>Buy with Card — $29</button>
      </a>

      {/* USDC payment */}
      <PayWithUsdcButton
        productUrl="/api/products/x402-paywall-kit/download"
        price="$29"
        onSuccess={(data) => {
          window.location.href = data.downloadUrl;
        }}
      />
    </div>
  );
}
```

## Step 5: Test on Base Sepolia

Before going to mainnet, test on Base Sepolia testnet:

1. Change the server middleware network to `"eip155:84532"`
2. Add `paywallConfig: { testnet: true }` to the middleware config
3. Get testnet USDC from https://faucet.circle.com (select Base Sepolia)
4. Connect your browser wallet to Base Sepolia network
5. Click "Pay with USDC" and complete the flow
6. Verify the download URL is returned

## Step 6: Switch to Base Mainnet

1. Change server middleware network back to `"eip155:8453"`
2. Remove `testnet: true` from paywallConfig
3. Ensure Tara's wallet is set as recipient: `0x5b99070C84aB6297F2c1a25490c53eE483C8B499`
4. Test with a real $29 USDC payment
5. Verify USDC arrives in Tara's wallet on Base

## Environment Variables

Add to taraquinn.ai `.env`:

```
# x402 USDC payments
X402_PAYTO_ADDRESS=0x5b99070C84aB6297F2c1a25490c53eE483C8B499

# Optional: WalletConnect for mobile wallet support
NEXT_PUBLIC_WC_PROJECT_ID=your-walletconnect-project-id
```

## Payment Flow Details

### EIP-3009 (Gasless Signatures)

The user signs an EIP-3009 `transferWithAuthorization` message. This:
- Authorizes the Coinbase facilitator to move USDC from buyer to Tara's wallet
- **Costs zero gas** for the buyer — the facilitator pays gas
- Is a standard EIP-712 typed data signature (the wallet popup shows human-readable details)
- Is valid for a limited time (`maxTimeoutSeconds` from the payment requirements)

### What the User Sees

1. "Pay with USDC — $29" button
2. Wallet popup (MetaMask/Coinbase Wallet) asking to connect
3. Wallet popup showing signature request: "Authorize transfer of 29.00 USDC"
4. Brief "Processing payment..." while facilitator settles
5. Download starts automatically

### Sales Logging

All USDC payments are logged to `./logs/x402-sales.jsonl`:

```json
{"timestamp":"2026-02-27T...","url":"/api/products/...","amount":"29.00","asset":"USDC","network":"eip155:8453","success":true,"policyDecision":"approved"}
```

## Troubleshooting

- **"Wallet not connected"**: User needs MetaMask or Coinbase Wallet browser extension, or use WalletConnect
- **"User rejected"**: User declined the signature in their wallet — no funds moved
- **Wrong network**: User's wallet must be on Base (chain ID 8453). Wagmi auto-prompts to switch.
- **Insufficient USDC**: User needs 29+ USDC on Base. No ETH needed (gasless signature).
- **Facilitator timeout**: The Coinbase facilitator may be slow. Retry after a moment.
