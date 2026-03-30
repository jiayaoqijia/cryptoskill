# ERC-20 Swap Example (Requires Approval)

## User Input

```
100 USDC to ETH on ethereum from 0xYourWalletAddress
```

## Expected Output

```
## KyberSwap Swap Transaction

**100 USDC → 0.0426 ETH** on Ethereum

| Detail | Value |
|---|---|
| Input | 100 USDC (~$100.00) |
| Expected output | 0.0426 ETH (~$99.85) |
| Minimum output (after slippage) | 0.0424 ETH |
| Slippage tolerance | 0.5% |
| Gas estimate | 280000 units (~$3.89) |

### Transaction Details

| Field | Value |
|---|---|
| To (Router) | `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` |
| Value | `0` (in wei — ERC-20 input, not native token) |
| Data | `0x...` |
| Sender | `0xYourWalletAddress` |
| Recipient | `0xYourWalletAddress` |

> **WARNING:** Review the transaction details carefully before submitting on-chain.

### Token Approval Required

Before submitting this swap, approve the KyberSwap router to spend USDC:

- **Token contract:** `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- **Spender (router):** `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5`
- **Amount:** `100000000` (exact amount, recommended) or `type(uint256).max` (unlimited — risky if the router is compromised)

> **Security note:** Prefer exact-amount approvals for large holdings. Unlimited approvals allow the spender to transfer your entire token balance.

Use a wallet or a tool like `cast` to send the approval transaction first.
```

## Notes

- ERC-20 token inputs require a separate approval transaction
- The `value` field is `0` for ERC-20 swaps (non-zero only for native token input)
- Consider using `permit` for gasless approvals if the token supports ERC-2612
