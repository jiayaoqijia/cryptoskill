# NEAR Intents Skill — Usage Guide

## How It Works

This skill uses the [1Click API](https://docs.near-intents.org/near-intents/integration/distribution-channels/1click-api) to perform cross-chain token swaps. The flow is:

```
1. Get Quote   → OneClickService.getQuote()  → deposit address + pricing
2. Send Tokens → Send to deposit address      → on origin chain
3. Track       → OneClickService.getExecutionStatus() → poll until done
```

The 1Click API coordinates with market makers to fill your swap. You never interact with `intents.near` directly.

---

## Supported Operations

### Same-Chain Swap
**Example**: NEAR → USDC (both on NEAR)

```typescript
await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'USDC',
  amount: '1.0',
});
```

### Cross-Chain Swap
**Example**: NEAR → USDC on Base

```typescript
await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0xYourBaseAddress',
});
```

### Cross-Chain Bridge (non-NEAR origin)
**Example**: USDC on Arbitrum → USDC on Solana

```typescript
const quote = await executeIntent({
  assetIn: 'arb:USDC',
  assetOut: 'sol:USDC',
  amount: '5.0',
  recipient: 'YourSolanaAddress',
  mode: 'manual',
});
// User sends USDC to the deposit address on Arbitrum
```

### Exact Output
**Example**: "I want exactly 10 USDC on Base"

```typescript
const quote = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '10.0',
  recipient: '0x...',
  mode: 'manual',
  swapType: 'EXACT_OUTPUT',
});
```

---

## Supported Chains

| Chain     | Prefix  | Notes |
|-----------|---------|-------|
| NEAR      | *(none)* | Default |
| Base      | `base:` | L2 |
| Ethereum  | `eth:`  | Mainnet |
| Arbitrum  | `arb:`  | L2 |
| Solana    | `sol:`  | |
| BSC       | `bsc:`  | |
| Bitcoin   | `btc:`  | Native only |
| Dogecoin  | `doge:` | Native only |
| Zcash     | `zec:`  | Native only |
| Litecoin  | `ltc:`  | Native only |

**UTXO Chains** (BTC, DOGE, ZEC, LTC): only native tokens supported — no smart contracts or wrapped tokens.

---

## Decimals

User inputs are automatically converted. You always provide human-readable amounts:

| Token | Decimals | `"1.0"` becomes |
|-------|----------|-----------------|
| NEAR  | 24       | `1000000000000000000000000` |
| USDC  | 6        | `1000000` |
| ETH   | 18       | `1000000000000000000` |
| SOL   | 9        | `1000000000` |
| BTC   | 8        | `100000000` |

---

## Token Reference

See `TOKENS.md` for complete reference. Key tokens:

| Symbol      | Asset ID | Decimals |
|-------------|----------|----------|
| `NEAR`      | `nep141:wrap.near` | 24 |
| `USDC`      | `nep141:17208628f8...` | 6 |
| `base:USDC` | `nep141:base-0x833589...omft.near` | 6 |
| `arb:USDC`  | `nep141:arb-0xaf88d0...omft.near` | 6 |
| `eth:ETH`   | `nep141:eth.omft.near` | 18 |
| `sol:SOL`   | `nep141:sol.omft.near` | 9 |

To discover more tokens programmatically:
```typescript
import { OneClickService } from '@defuse-protocol/one-click-sdk-typescript';
const tokens = await OneClickService.getTokens();
```

---

## Important Notes

### Minimum Amount
Swaps require approximately **$0.10+ USD** value. Below this, solvers may not provide quotes.

### Gas Fees
- **NEAR auto mode**: ~0.001-0.005 NEAR per operation
- **Cross-chain**: Fees vary by pair and are included in the quote

### Quotes Expire
Quotes have a deadline (~10 minutes). Send the deposit before the deadline or request a new quote.

### JWT Token
- Without JWT: 0.2% fee on all swaps
- With JWT: no fee — register at [partners.near-intents.org](https://partners.near-intents.org/)

---

## Transaction Tracking

All swaps can be tracked:
- **NEAR transactions**: `https://nearblocks.io/txns/<txHash>`
- **Swap progress**: `https://explorer.near-intents.org/transactions/<depositAddress>`

### Swap Statuses
| Status | Meaning |
|--------|---------|
| `PENDING_DEPOSIT` | Waiting for tokens |
| `PROCESSING` | Market makers executing |
| `SUCCESS` | Tokens delivered |
| `INCOMPLETE_DEPOSIT` | Deposit too small |
| `REFUNDED` | Failed, tokens returned |
| `FAILED` | Error occurred |

---

## Troubleshooting

### "No deposit address in quote response"
- Solver couldn't match the pair or amount
- Try a larger amount or different token pair
- Wait and retry — solvers may be temporarily unavailable

### "Token not found: X"
- Check spelling and chain prefix
- See `TOKENS.md` for supported tokens
- Use lowercase or uppercase — both work

### "Swap failed with status: REFUNDED"
- Tokens were automatically returned to refund address
- Safe to retry with different parameters

### "Status polling timed out"
- Swap may still complete — check explorer URL manually
- Cross-chain can take 2-10 minutes

### "NEAR_ACCOUNT_ID and NEAR_PRIVATE_KEY must be set"
- Configure `.env` for auto mode
- Or use `mode: 'manual'` to skip auto-sending

---

## Real-World Example

**Scenario**: Bridge 1 NEAR to USDC on Base

```typescript
// Auto mode — one call does everything
const result = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0x30FE694284a082a5D1adfF6D25C0B9B6bF61F77D',
});
// → "Swap Successful! 1.0 NEAR → 0.97 USDC"
// → Transaction: https://nearblocks.io/txns/...
// → Explorer: https://explorer.near-intents.org/transactions/...
```

Result: USDC arrives on Base after ~30 seconds to 3 minutes.

---

## Best Practices

1. **Start small**: Test with small amounts first
2. **Use manual mode for quotes**: Preview before committing
3. **Monitor via explorer**: Always check the explorer URL
4. **Handle errors gracefully**: REFUNDED means tokens are safe
5. **Respect deadlines**: Act within 10 minutes of getting a quote
6. **Native-only for UTXO**: BTC, DOGE, ZEC, LTC — native tokens only

---

## Integration with OpenClaw

The skill integrates seamlessly:
- Auto-detects token symbols via built-in `TOKEN_MAP`
- Handles decimal conversion automatically
- Returns clear transaction URLs
- Supports auto and manual execution modes
- Comprehensive error messages

---

**Version**: 2.0.0
**Powered by**: [1Click SDK](https://github.com/defuse-protocol/one-click-sdk-typescript) + [NEAR Intents](https://docs.near-intents.org)
