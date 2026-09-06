---
name: fortune
description: Integrate QLWY on-chain fortune casting (I Ching divination) into applications. Use when user says "算卦", "起卦", "卜卦", "cast fortune", "hexagram", "I Ching", "divination", "fortune telling", or mentions 潜龙勿用 fortune/casting.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npm:*), Bash(npx:*), Bash(bun:*), Bash(curl:*), WebFetch
model: opus
license: MIT
metadata:
  author: qlwy
  version: '1.0.0'
---

# QLWY Fortune Casting (链上算卦)

Integrate on-chain I Ching divination powered by VRF randomness, with AI-powered hexagram interpretation.

## Overview

QLWY Fortune Casting uses Binance Oracle VRF to generate truly random hexagrams on-chain. Users pay a small BNB fee to cast, receive one of 64 hexagrams with rarity and luck attributes, and can optionally mint the result as an NFT. An AI interpretation API provides personalized readings based on the hexagram and user's question.

## Quick Decision Guide

| Building...                        | Use This Method                     |
| ---------------------------------- | ----------------------------------- |
| Frontend with React/Next.js        | viem contract calls + Interpret API |
| Backend bot or automation          | viem contract calls + Interpret API |
| Telegram bot / social integration  | Interpret API (with pre-cast data)  |

## Architecture

```text
┌─────────────┐     ┌───────────────────────┐
│  Frontend /  │────▶│  Interpret API         │
│  Agent       │     │  (Vercel Edge, GPT-4o) │
└──────┬───────┘     └───────────────────────┘
       │
       │  viem / ethers.js
       ▼
┌──────────────────────────────┐
│  QLWYFortuneCore Contract    │
│  (VRF casting, NFT minting)  │
│  BSC Mainnet                 │
└──────────────────────────────┘
```

**Key flow**: User calls `requestCast()` → VRF generates random hexagram → query `casts(castId)` for result → call Interpret API with hexagram data + question → AI returns reading.

## Core Concepts

| Concept           | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| **Hexagram (卦)**  | One of 64 I Ching hexagrams, each with 6 lines (阴/阳 yin/yang)    |
| **Lines (爻)**     | 6 values, each 0 (yin ⚋) or 1 (yang ⚊), bottom to top            |
| **Rarity**        | 0=Common, 1=Rare, 2=Epic, 3=Legendary, 4=Mythic                   |
| **Luck**          | 0–255 luck value, affects NFT rarity and jackpot eligibility       |
| **Cast Fee**      | ~0.001 BNB per cast (free casts available via credits)             |
| **VRF**           | Binance Oracle VRF for provably fair randomness                    |
| **Mint**          | Optionally mint a hexagram result as an ERC-721 NFT                |

## Cast Lifecycle

> ⚠️ **IMPORTANT: `requestCast()` is ASYNCHRONOUS.** It does NOT return the hexagram result. It only triggers a VRF randomness request. You **MUST** poll `casts(castId)` afterwards until `ready === true` (usually 3-10 seconds) to get the actual hexagram. Without polling, the agent will never know the divination result.

```text
requestCast() → VRF Request → VRF Callback → Cast Ready → (optional) mintFortuneNFT()
                                                  ↓
                                          Interpret API → AI Reading
```

1. **requestCast()** — User pays cast fee, VRF request sent. Returns `castId` (from CastRequested event logs). **The hexagram is NOT available yet.**
2. **Poll for result (REQUIRED)** — Every 3-5 seconds, call `casts(castId)` and check if `ready === true`. This is the only way to know the result is available. Typically takes 3-10 seconds.
3. **Read hexagram data** — Once `ready === true`, the same `casts(castId)` call returns the full hexagram: `hx.id` (hexagram number), `hx.lines` (six yao lines), `rarity`, `luck`.
4. **Interpret** — Send hexagram data + question to Interpret API for AI reading
5. **Mint (optional)** — Call `mintFortuneNFT(castId)` to mint as NFT

**Common mistake**: Calling `requestCast()` and stopping. The agent must complete steps 1→2→3 at minimum to obtain any useful result.

### After Cast: How to Present the Result

Once `ready === true`, the `casts(castId)` return value (via viem) looks like:

```
result[0] = user       // address — who cast
result[1] = ts         // uint40  — timestamp
result[2] = minted     // bool    — already minted as NFT?
result[3] = hx         // { lines: [1,0,1,0,1,1], id: 42 } — hexagram data
result[4] = rarity     // uint8   — 0=Common, 1=Rare, 2=Epic, 3=Legendary, 4=Mythic
result[5] = ready      // bool    — must be true
result[6] = luck       // uint8   — 0-255
```

**Step-by-step for the agent:**

1. **Map hexagram ID** — `hexId = hx.id + 1` (contract is 0-indexed, hexagramData.json is 1-indexed)
2. **Look up hexagram info** — Find the entry in `references/hexagramData.json` where `id === hexId`. This gives you:
   - `name` — 卦名 (e.g. "乾")
   - `full` — 全名 (e.g. "乾为天")
   - `text` — 卦辞/judgment (e.g. "元，亨，利，贞。天行健，君子以自强不息。")
   - `lines` — canonical line pattern
   - `pinyin` — pronunciation
3. **Get hexagram image** — Build the image URL:

   > ⚠️ **IMPORTANT: You MUST copy the base URL below EXACTLY as-is. Do NOT modify, truncate, or retype any part of it — especially the subdomain (`prawn`, not `pawn`) and the full IPFS CID.**

   **Base URL (do NOT change):**
   ```
   https://scarlet-obliged-prawn-408.mypinata.cloud/ipfs/bafybeiemssmg65azrtivoi4ka535h76r5qrdczvbpxyk3au3zfnifybaea
   ```
   **Append** `/{hexId}_{rarity}.svg` to form the full URL.

   For example, hexagram 1 with rarity 2 (Epic):
   ```
   https://scarlet-obliged-prawn-408.mypinata.cloud/ipfs/bafybeiemssmg65azrtivoi4ka535h76r5qrdczvbpxyk3au3zfnifybaea/1_2.svg
   ```
   Display this image to the user alongside the hexagram info.
4. **Present to user** — Display:
   - 🎴 Hexagram image (the SVG URL above)
   - Hexagram name and full name (e.g. "乾 · 乾为天")
   - Lines visualization (⚊ yang / ⚋ yin, bottom to top)
   - Judgment text (卦辞)
   - Rarity and luck value
5. **If rarity ≥ 1 (Rare or above)** — Prompt the user: *"Your hexagram is [Rare/Epic/Legendary/Mythic]! You can mint it as an NFT to keep it on-chain."* and offer to call `mintFortuneNFT(castId)`.
6. **Prompt for AI interpretation** — Ask the user: *"Would you like an AI I Ching reading? Tell me your question and I'll interpret the hexagram for you."* Then call the Interpret API with the hexagram data + user's question.

**Rarity display names:**

| Value | English   | 中文 |
|-------|-----------|------|
| 0     | Common    | 普通 |
| 1     | Rare      | 稀有 |
| 2     | Epic      | 史诗 |
| 3     | Legendary | 传奇 |
| 4     | Mythic    | 神话 |

---

## Smart Contract Reference

### Contract: QLWYFortuneCore

**Address (BSC Mainnet)**: `0xcE6f2F55898050C0D1769164c4Ceb828B4fC54f8`

**Chain**: BNB Smart Chain (chainId: 56)

### Request Cast (起卦)

```typescript
import { parseEther, parseEventLogs } from 'viem';

// 1. Read cast fee
const castFee = await publicClient.readContract({
  address: FORTUNE_CORE_ADDRESS,
  abi: fortuneCoreAbi,
  functionName: 'castFee',
});

// 2. Request cast (pays BNB)
const tx = await walletClient.writeContract({
  address: FORTUNE_CORE_ADDRESS,
  abi: fortuneCoreAbi,
  functionName: 'requestCast',
  args: ['0x'],  // opts: empty bytes
  value: castFee,
});
// NOTE: writeContract returns a tx hash, NOT the castId.
// You MUST parse the castId from CastRequested event logs:
const receipt = await publicClient.waitForTransactionReceipt({ hash: tx });
const castLogs = parseEventLogs({ abi: fortuneCoreAbi, logs: receipt.logs });
const castEvent = castLogs.find((l) => l.eventName === 'CastRequested');
const castId = castEvent.args.castId;   // bigint — this is the real castId
```

### Query Cast Result (查卦)

```typescript
const result = await publicClient.readContract({
  address: FORTUNE_CORE_ADDRESS,
  abi: fortuneCoreAbi,
  functionName: 'casts',
  args: [castId],
});
// Returns: { user, ts, minted, hx: { lines: uint8[6], id: uint16 }, rarity, ready, luck }
// Wait until ready === true before reading hexagram data
// hx.id is 0-indexed internally; add 1 for the standard hexagram number (1-64)
```

### Mint Fortune NFT (铸造卦象 NFT)

```typescript
// Read mint fee for this rarity
const mintFee = await publicClient.readContract({
  address: FORTUNE_CORE_ADDRESS,
  abi: fortuneCoreAbi,
  functionName: 'mintFeeForRarity',
  args: [rarity],  // 0-4
});

// Mint NFT
const tx = await walletClient.writeContract({
  address: FORTUNE_CORE_ADDRESS,
  abi: fortuneCoreAbi,
  functionName: 'mintFortuneNFT',
  args: [castId],
  value: mintFee,
});
// Returns: tokenId (uint256)
```

### Read Token Attributes

```typescript
const view = await publicClient.readContract({
  address: FORTUNE_CORE_ADDRESS,
  abi: fortuneCoreAbi,
  functionName: 'tokenView',
  args: [tokenId],
});
// Returns: { rarity: uint8, luck: uint8, lines: uint8[6], id: uint16 }
// id is 1-indexed (1-64)
```

---

## Interpret API Reference

**Endpoint**: `POST https://qlwy.xyz/api/interpret`

**Authentication**: `Authorization: Bearer <Privy JWT>`

### Request

```json
{
  "castId": "42",
  "question": "我的事业运如何？",
  "hexagramId": 1,
  "hexagramName": "乾为天",
  "hexagramJudgment": "元，亨，利，贞。天行健，君子以自强不息。",
  "lines": [1, 1, 1, 1, 1, 1],
  "rarity": 2,
  "luck": 180
}
```

| Field            | Required | Description                              |
| ---------------- | -------- | ---------------------------------------- |
| `castId`         | No       | On-chain cast ID (for ownership verify)  |
| `question`       | **Yes**  | User's question in any language          |
| `hexagramId`     | **Yes**  | Hexagram number (1-64)                   |
| `hexagramName`   | No       | Full hexagram name (e.g. "乾为天")        |
| `hexagramJudgment` | No     | Hexagram judgment text (卦辞)            |
| `lines`          | No       | Array of 6 line values (0=yin, 1=yang)   |
| `rarity`         | No       | Rarity level (0-4)                       |
| `luck`           | No       | Luck value (0-255)                       |

### Response

Streaming SSE response (`text/event-stream`) with AI-generated interpretation in Chinese (~300-500 characters). The AI acts as an I Ching master (易经解卦大师), providing poetic yet practical readings.

**Notes**:
- If `castId` is provided, the API verifies the caller owns the cast via subgraph
- `hexagramId` and `question` are the only required fields
- Hexagram name/judgment are auto-filled from built-in data if not provided
- Response is streamed for real-time display

---

## Hexagram Data

All 64 hexagrams are available in `references/hexagramData.json`. Each entry:

```json
{
  "id": 1,
  "name": "乾",
  "full": "乾为天",
  "pinyin": "qián wéi tiān",
  "text": "元，亨，利，贞。\n天行健，\n君子以自强不息。",
  "lines": [1, 1, 1, 1, 1, 1],
  "name_pinyin": "Qian"
}
```

---

## Common Integration Patterns

### Full Cast + Interpret Flow

```typescript
import { createPublicClient, createWalletClient, http, parseEventLogs } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { bsc } from 'viem/chains';
import hexagramData from './references/hexagramData.json';
import fortuneCoreAbi from './references/QLWYFortuneCore.abi.json';

const FORTUNE_CORE = '0xcE6f2F55898050C0D1769164c4Ceb828B4fC54f8';

// 1. Cast
const castFee = await publicClient.readContract({
  address: FORTUNE_CORE, abi: fortuneCoreAbi, functionName: 'castFee',
});
const tx = await walletClient.writeContract({
  address: FORTUNE_CORE, abi: fortuneCoreAbi,
  functionName: 'requestCast', args: ['0x'], value: castFee,
});
const receipt = await publicClient.waitForTransactionReceipt({ hash: tx });
const castLogs = parseEventLogs({ abi: fortuneCoreAbi, logs: receipt.logs });
const castEvent = castLogs.find((l) => l.eventName === 'CastRequested');
const castId = castEvent.args.castId;   // bigint

// 2. Poll for result
let ready = false;
let castResult;
while (!ready) {
  await new Promise(r => setTimeout(r, 5000));
  castResult = await publicClient.readContract({
    address: FORTUNE_CORE, abi: fortuneCoreAbi,
    functionName: 'casts', args: [castId],
  });
  ready = castResult[5]; // ready field
}

// 3. Interpret
const hexId = Number(castResult[3].id) + 1; // 0-indexed → 1-indexed
const hex = hexagramData.find(h => h.id === hexId);
const interpretRes = await fetch('https://qlwy.xyz/api/interpret', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jwt}` },
  body: JSON.stringify({
    castId: castId.toString(),
    question: '我的事业运如何？',
    hexagramId: hexId,
    hexagramName: hex?.full,
    hexagramJudgment: hex?.text,
    lines: [...castResult[3].lines],
  }),
});
// Read streaming response...
```

---

## Key Configuration

| Parameter      | Value                                        | Description                    |
| -------------- | -------------------------------------------- | ------------------------------ |
| `castFee`      | ~0.001 BNB                                   | Fee per cast (owner-adjustable)|
| `cooldown`     | 10 seconds                                   | Minimum time between casts     |
| `mintFee`      | Varies by rarity (0=cheapest, 4=most expensive) | Fee to mint NFT from cast   |
| `freeCasts`    | Per-address credits                          | Free casts granted by owner    |

## Contract Events

| Event              | Description                                      |
| ------------------ | ------------------------------------------------ |
| `CastRequested`    | New cast initiated (castId, user, requestId)     |
| `CastFulfilled`    | VRF callback received, hexagram generated        |
| `FortuneMinted`    | NFT minted from cast result                      |
| `JackpotWon`       | User won the jackpot pool                        |

## Troubleshooting

| Issue                          | Solution                                             |
| ------------------------------ | ---------------------------------------------------- |
| `QLWY: invalid cast fee`      | Read `castFee()` and send exact BNB amount as `value`|
| `CooldownActive` revert       | Wait at least 10 seconds between casts               |
| Cast `ready` stays false      | VRF callback pending; wait a few more seconds        |
| `AlreadyMinted` revert        | This castId was already minted as NFT                |
| Interpret API 401              | Privy JWT expired or invalid                         |
| Interpret API 403              | Caller doesn't own this castId                       |

