# Jupiter Swap Integration

Jupiter is Solana's leading DEX aggregator. Use for token swaps.

## API Endpoints

| Endpoint | URL                                          |
| -------- | -------------------------------------------- |
| Quote    | `https://api.jup.ag/swap/v1/quote`           |
| Swap     | `https://api.jup.ag/swap/v1/swap`            |
| Price    | `https://api.jup.ag/price/v2`                |
| Tokens   | `https://tokens.jup.ag/tokens?tags=verified` |

## Get Quote

```typescript
interface QuoteParams {
  inputMint: string; // Token to sell
  outputMint: string; // Token to buy
  amount: string; // Amount in smallest unit (lamports/decimals)
  slippageBps?: number; // Slippage tolerance (100 = 1%)
  onlyDirectRoutes?: boolean;
  asLegacyTransaction?: boolean;
}

async function getQuote(params: QuoteParams) {
  const query = new URLSearchParams({
    inputMint: params.inputMint,
    outputMint: params.outputMint,
    amount: params.amount,
    slippageBps: String(params.slippageBps || 100),
  });

  const response = await fetch(`https://api.jup.ag/swap/v1/quote?${query}`);
  return response.json();
}
```

**Quote Response:**

```json
{
  "inputMint": "So11111111111111111111111111111111111111112",
  "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "inAmount": "1000000000",
  "outAmount": "234567890",
  "priceImpactPct": "0.01",
  "routePlan": [...],
  "contextSlot": 123456789
}
```

## Build Swap Transaction

```typescript
interface SwapParams {
  quoteResponse: QuoteResponse;
  userPublicKey: string;
  wrapAndUnwrapSol?: boolean; // Auto wrap/unwrap SOL (default: true)
  dynamicComputeUnitLimit?: boolean; // Optimize compute units
  prioritizationFeeLamports?: number | "auto";
}

async function buildSwapTransaction(params: SwapParams) {
  const response = await fetch("https://api.jup.ag/swap/v1/swap", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      quoteResponse: params.quoteResponse,
      userPublicKey: params.userPublicKey,
      wrapAndUnwrapSol: params.wrapAndUnwrapSol ?? true,
      dynamicComputeUnitLimit: true,
      prioritizationFeeLamports: "auto",
    }),
  });
  return response.json();
}
```

**Swap Response:**

```json
{
  "swapTransaction": "BASE64_ENCODED_TRANSACTION",
  "lastValidBlockHeight": 123456789,
  "prioritizationFeeLamports": 50000
}
```

## Complete Swap Flow

```typescript
import { Connection, Keypair, VersionedTransaction } from "@solana/web3.js";

async function executeSwap(
  connection: Connection,
  wallet: Keypair,
  inputMint: string,
  outputMint: string,
  amountIn: number,
  inputDecimals: number,
) {
  // 1. Get quote
  const amount = String(amountIn * Math.pow(10, inputDecimals));
  const quoteResponse = await getQuote({
    inputMint,
    outputMint,
    amount,
    slippageBps: 100,
  });

  // 2. Build swap transaction
  const { swapTransaction } = await buildSwapTransaction({
    quoteResponse,
    userPublicKey: wallet.publicKey.toString(),
  });

  // 3. Deserialize and sign
  const txBuffer = Buffer.from(swapTransaction, "base64");
  const tx = VersionedTransaction.deserialize(txBuffer);
  tx.sign([wallet]);

  // 4. Send and confirm
  const signature = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: true,
    maxRetries: 3,
  });

  await connection.confirmTransaction(signature, "confirmed");
  return signature;
}
```

## Get Token Prices

```typescript
async function getPrice(mints: string[]) {
  const ids = mints.join(",");
  const response = await fetch(`https://api.jup.ag/price/v2?ids=${ids}`);
  const data = await response.json();
  return data.data;
}

// Example
const prices = await getPrice([
  "So11111111111111111111111111111111111111112", // SOL
  "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", // USDC
]);
// Returns: { "So11111...": { price: "123.45" }, ... }
```

## Token List

Get verified tokens:

```typescript
async function getVerifiedTokens() {
  const response = await fetch("https://tokens.jup.ag/tokens?tags=verified");
  return response.json();
}

// Response includes:
// - address (mint)
// - symbol
// - name
// - decimals
// - logoURI
// - tags
```

## Error Handling

Common errors:

| Error                    | Cause                         | Solution                             |
| ------------------------ | ----------------------------- | ------------------------------------ |
| `INSUFFICIENT_LIQUIDITY` | Not enough liquidity for swap | Reduce amount or try different route |
| `SLIPPAGE_EXCEEDED`      | Price moved too much          | Increase slippage or retry           |
| `STALE_QUOTE`            | Quote expired                 | Get fresh quote                      |
| `INSUFFICIENT_BALANCE`   | Not enough tokens             | Check balance before swap            |

```typescript
async function safeSwap(params: SwapParams) {
  try {
    const quote = await getQuote(params);

    // Check price impact
    if (parseFloat(quote.priceImpactPct) > 5) {
      throw new Error(`High price impact: ${quote.priceImpactPct}%`);
    }

    const swap = await buildSwapTransaction({
      quoteResponse: quote,
      userPublicKey: params.userPublicKey,
    });

    return swap;
  } catch (error) {
    if (error.message.includes("INSUFFICIENT_LIQUIDITY")) {
      console.log("Try smaller amount or different token pair");
    }
    throw error;
  }
}
```

## Best Practices

1. **Always check price impact** — High impact = bad trade
2. **Use reasonable slippage** — 0.5-1% for majors, 1-3% for smaller tokens
3. **Prefer verified tokens** — Check token list before trading
4. **Handle partial fills** — Some routes may not fill completely
5. **Retry with fresh quote** — Quotes expire quickly in volatile markets
