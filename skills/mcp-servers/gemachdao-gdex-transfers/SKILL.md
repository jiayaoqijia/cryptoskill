---
name: gdex-transfers
description: Native and ERC20/SPL token transfers via GDEX managed custody — send assets to any recipient on supported chains
---

# GDEX: Transfers

Send native assets (ETH, SOL, SUI, BNB, …) or ERC20 / SPL tokens from a
managed-custody wallet to any recipient.

## When to Use

- Withdrawing native assets to an external wallet
- Sending ERC20 / SPL tokens to a recipient
- Paying out winnings, rewards, or peer-to-peer transfers

## Prerequisites

- `@gemachdao/gdex-skill` installed
- Authenticated via managed-custody sign-in — see **gdex-authentication**
- Session keypair (`sessionPrivateKey` + `sessionKey`) from sign-in
- Pre-built `computedData` payload (encrypted via the standard AES-256-CBC
  managed-custody contract). Caller is responsible for ABI-encoding the
  transfer parameters and signing with the session key — schema is
  documented in `src/api/services/ServiceMain.ts` of the backend.

## Backend Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/v1/transfer` | Native token transfer |
| `POST` | `/v1/transfer_token` | ERC20 / SPL token transfer |

Both endpoints accept:
```json
{ "computedData": "<hex>", "chainId": 8453 }
```

## SDK Usage

```typescript
import { GdexSkill } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(process.env.GDEX_API_KEY!);

// Native ETH transfer (caller pre-builds computedData)
const result = await skill.transferNative({
  computedData,           // hex-encoded encrypted payload
  chainId: 8453,
});

// ERC20 / SPL transfer
const result2 = await skill.transferToken({
  computedData,
  chainId: 622112261,     // Solana SPL
});
```

## Response

Typically:
```json
{ "requestId": "...", "status": "pending", "createdAt": 1717000000 }
```
Poll status via `GET /v1/trade-status/:requestId` (or `skill.getManagedTradeStatus(requestId)`).

## Notes

- Both endpoints follow the standard managed-custody encrypted-payload pattern.
- For Solana SPL transfers, the first transfer to a recipient may incur an
  Associated Token Account (ATA) creation fee (~0.002 SOL).
- Chain id semantics match the rest of the SDK — Solana uses `622112261`,
  Sui uses `1313131213`.
