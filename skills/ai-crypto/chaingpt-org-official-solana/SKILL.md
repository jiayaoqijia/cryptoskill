---
name: solana
description: Solana signing foundation — build unsigned native SOL and SPL token transfers. Custody-free. Returns base64 VersionedTransaction the user signs externally with Phantom / Backpack / Solflare / hardware wallet. The foundation that Drift / Marginfi / Kamino signed actions build on.
---

# Solana signing

This skill exposes a small foundation for building **unsigned Solana transactions** from chat. The plugin never sees a Solana private key — every state-changing tool returns a base64-encoded `VersionedTransaction` that the user signs in their wallet.

## When to use this skill

- The user asks to "send SOL to X" or "transfer USDC to Y" from a Solana address they control.
- The user wants to inspect a Solana transaction someone else built before signing it.
- A more advanced Solana flow (Drift order, Marginfi deposit, Kamino borrow) builds on the foundation here — when those land, they will reuse `lib/solana-sign.ts` directly.

## What the surface is

- `chaingpt_solana_build_transfer_tx` — build an unsigned transfer.
  - **Native SOL** when `mint` is omitted. Decimals: 9 (`LAMPORTS_PER_SOL`).
  - **SPL Token (classic or Token-2022)** when `mint` is provided. Decimals fetched from the mint account. Source + destination Associated Token Accounts derived automatically. Idempotent `CreateATAIdempotent` instruction included so first-time-recipient transfers work without an extra setup step.
  - `acknowledgeMainnet: true` required when `network=mainnet`. Same gate as the EVM tools.
- `chaingpt_solana_decode_tx` — decode an unsigned base64 versioned transaction for review (payer, blockhash, instruction count, program ids with annotations).

## Custody model

Identical to the rest of the plugin: **custody-free**. The plugin builds the transaction; the user signs it elsewhere. There is no MCP tool that accepts a `secretKey`, `mnemonic`, or `seedPhrase` parameter, and a unit test asserts this surface contract so future additions cannot accidentally break it.

If the user wants policy-gated signing (agent wallet pattern), the existing **agent wallet** skill provides that for EVM. A Solana counterpart is queued as a follow-up to this foundation.

## Mainnet safety gate

When `network=mainnet`, the build tool refuses unless `acknowledgeMainnet=true` is also passed. The refusal message lists what to verify before re-call (recipient address, amount, mint, network). This matches `feedback_mainnet_default`: mainnet is the target, but mainnet transactions require an explicit ack.

## Typical flow

```text
User: "Build a 0.5 USDC transfer from 7uDsTC...EUd to 9WzDXw...WWM on mainnet"
Agent: chaingpt_solana_build_transfer_tx({
  from: "7uDsTC1u4eRkxsfvQHvi3vCSqGBHc4uS9wpYbobcdEUd",
  to:   "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
  amount: "0.5",
  mint:  "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  // USDC mint
  network: "mainnet",
  acknowledgeMainnet: true
})
→ returns:
  - decoded summary (from ATA, to ATA, amount in base units, decimals)
  - the base64 VersionedTransaction
  - the blockhash + lastValidBlockHeight
  - next-step instructions for the signer
User: paste base64 into Phantom → review → sign → submit.
```

## RPC endpoints

Default public RPC fallback per network:

| Network  | Endpoints                                                     |
|----------|---------------------------------------------------------------|
| mainnet  | api.mainnet-beta.solana.com → solana-rpc.publicnode.com        |
| devnet   | api.devnet.solana.com                                          |
| testnet  | api.testnet.solana.com                                         |

Override via `SOLANA_RPC_URL` env var (Helius / QuickNode / Triton recommended for production loads).

## Why `TransferChecked` instead of `Transfer`

The classic SPL Token program has two transfer instructions:

- `Transfer` (discriminator 3): minimal — source, destination, owner, amount.
- `TransferChecked` (discriminator 12): also takes `mint` + `decimals` and the runtime verifies they match the source account's mint.

We always emit `TransferChecked`. The mint/decimals check prevents an attacker from swapping an unrelated ATA into the `destination` slot to redirect funds.

## What this skill does NOT do (yet)

- **Drift signed orders** — read-only via `chaingpt_drift_*` today. Signed `placePerpOrder`, `deposit`, `withdraw` are queued as follow-up PRs that will use the foundation here.
- **Marginfi signed lending** — read-only today. Same story.
- **Kamino signed lending** — read-only today. Same story.
- **Jupiter swaps** — already supported via `chaingpt_dex_jupiter_quote` (the unsigned-swap-tx call from Jupiter's API is returned directly; no foundation needed).
- **NFT transfers / Metaplex** — out of scope for the foundation.

When you build those follow-ups, the pattern is:

1. Import `buildVersionedTransaction`, `serializeUnsigned`, `makeConnection`, `parseAddress` from `lib/solana-sign.ts`.
2. Build the protocol-specific `TransactionInstruction[]` (account derivation + IDL-encoded data).
3. Call `buildVersionedTransaction({ payer, instructions, connection })`.
4. Return `serializeUnsigned(tx)` plus a decoded summary.
5. Gate any mainnet build behind `acknowledgeMainnet:true`.
6. Add a vitest with mocked `Connection.getLatestBlockhash` so the test never touches the network.

## Reference

- `mcp-server/src/lib/solana-sign.ts` — utilities (RPC fallback, parseAddress, instruction builders, ATA derivation, mint info fetch, v0 message build, base64 ser/de).
- `mcp-server/src/tools/solana.ts` — tool surface (`build_transfer_tx`, `decode_tx`).
- `mcp-server/src/__tests__/solana.test.ts` — 29 cases.
