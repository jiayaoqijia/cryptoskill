---
name: aa
description: ERC-4337 v0.7 account-abstraction foundation. Custody-free utilities for computing userOpHashes, packing UserOperations into the EntryPoint wire format, and proxying bundler-RPC calls (Pimlico / Alchemy / Stackup). Triggers: ERC-4337, account abstraction, smart contract wallet, userop, user operation, bundler, paymaster, session key, EntryPoint, AA wallet, smart wallet, gas sponsorship.
---

# ERC-4337 (Account Abstraction) skill

This skill exposes the **shared primitives** every ERC-4337 v0.7 smart-contract wallet needs:

| Tool | Purpose |
|---|---|
| `chaingpt_aa_userop_hash` | Compute the v0.7 userOpHash the signer signs. |
| `chaingpt_aa_pack_userop` | Pack a UserOp into the EntryPoint wire-format `PackedUserOperation` + emit the bundler-RPC JSON shape. |
| `chaingpt_aa_estimate_userop` | Proxy `eth_estimateUserOperationGas` to an admin-supplied bundler URL. |
| `chaingpt_aa_userop_receipt` | Proxy `eth_getUserOperationReceipt` to check if a userop was bundled and what the on-chain receipt looks like. |

## Custody-free invariant

The plugin **never** signs a UserOp and **never** sees a smart-account owner key or session key. The hash returned by `chaingpt_aa_userop_hash` is the input to the user's wallet (MetaMask, hardware wallet, viem signer, SCW session-key module). The user signs externally and places the signature into the UserOp's `signature` field before submitting via the bundler.

A unit test asserts the surface contract: **no tool input schema may contain a parameter that matches `/privatekey|ownerkey|sessionkey|mnemonic|seedphrase|signer/`**. Future additions that try to accept a secret will fail the build.

## Foundation vs. session-key flow

ERC-4337 session keys live inside the smart-contract wallet's **validator module**. Every major SCW provider has its own validator with its own session-key ABI:

| Provider | Validator | Session-key issuance |
|---|---|---|
| **Safe + Zodiac** | `safe-protocol-kit` modules | enableModule + setSessionKey |
| **Kernel (ZeroDev)** | `EIP-7579` modular validators | installValidator |
| **Biconomy** | `K1Validator` + sponsorship | issueSessionKey |
| **Alchemy Smart Wallet** | Modular Account v2 | installPlugin |
| **SimpleAccount** (canonical reference) | single owner — no session keys natively | (none — add a session-key validator) |

Picking one provider here would lock the plugin into that vendor's surface. Instead, this skill ships the **shared primitives** (packing, hashing, bundler-rpc) that every v0.7 SCW needs, and per-provider session-key issuance / use is queued as follow-up PRs:

- `chaingpt_aa_session_ (SHIPPED v1.21 — vendor-neutral Smart Sessions supersedes the per-vendor safe/kernel plan; Kernel/Safe7579 agent-side signing still queued) chaingpt_aa_safe_*` — Safe enable-module + session-key enable
- `chaingpt_aa_kernel_*` — Kernel install-validator + session-key install
- (etc., one PR per provider)

Each follow-up will use `chaingpt_aa_userop_hash` + `chaingpt_aa_estimate_userop` from this foundation unchanged.

## How a typical signed-userop flow uses these tools

```text
1. Application code builds an unsigned UserOp:
     sender, nonce, callData, gas limits, gas fees, optional paymaster.

2. Estimate gas via the bundler (admin supplies the URL):
     chaingpt_aa_estimate_userop({ bundlerUrl, userOp, entryPoint? })
   → returns callGasLimit / verificationGasLimit / preVerificationGas.
   Fold those back into the UserOp.

3. Compute the hash to sign:
     chaingpt_aa_userop_hash({ userOp, chain, entryPoint? })
   → returns the 0x-prefixed userOpHash.

4. Sign the hash externally (this is the only step the plugin does NOT do):
     - SimpleAccount, Safe (default), Kernel default: ECDSA over personal_sign of the hash.
     - Some SCWs: EIP-712 typed-data signature (see your SCW's docs).

5. Set userOp.signature = the 65-byte ECDSA signature (or session-key-validator-specific encoding).

6. Submit via the bundler (you call this yourself, the plugin does not currently proxy eth_sendUserOperation):
     POST { method: 'eth_sendUserOperation', params: [userOp, entryPoint] }
   → returns userOpHash.

7. Poll inclusion:
     chaingpt_aa_userop_receipt({ bundlerUrl, userOpHash })
   → null until bundled, then the full receipt with tx hash + status.
```

## Why we don't ship `eth_sendUserOperation` (yet)

Submitting a signed userop is the irreversible step. We deliberately leave it to the user's existing bundler-client code path so the plugin doesn't become the broadcast vector. The hash and the estimate are read-only. The receipt is read-only. The signed-submission stays in user code where it's already audited.

## Bundler URL conventions

| Provider | Pattern |
|---|---|
| Pimlico | `https://api.pimlico.io/v2/<chain>/rpc?apikey=YOUR_KEY` |
| Alchemy AA | `https://<chain>.bundler.alchemy.com/<API_KEY>` |
| Stackup | `https://api.stackup.sh/v1/node/<API_KEY>` |
| Particle | `https://bundler.particle.network/?chainId=<id>` (with auth header) |

Pass the full URL to `bundlerUrl`. The plugin does not store it.

## EntryPoint addresses

| Version | Address (deterministic across chains) |
|---|---|
| v0.7 | `0x0000000071727De22E5E9d8BAf0edAc6f37da032` (this foundation targets v0.7) |
| v0.6 | `0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789` (read-only inspection only) |

## What this skill does NOT do (yet)

- **Sign anything.** The plugin returns the hash; you sign elsewhere.
- **Submit `eth_sendUserOperation`.** Done in user code with the signed UserOp.
- **Per-provider session-key issuance.** Safe / Kernel / Biconomy / Alchemy Smart Wallet are follow-up PRs that build on this foundation.
- **Paymaster sponsorship issuance.** The `paymaster*` fields are accepted as inputs; sponsoring a paymaster (calling Pimlico's `pm_sponsorUserOperation` or equivalent) is a follow-up.
- **EIP-7702 (delegated EOAs).** Different scheme; out of scope for v0.7.

## Reference

- `mcp-server/src/lib/erc4337.ts` — primitives (uses viem v2.20+ audited AA module).
- `mcp-server/src/tools/aa.ts` — tool surface (4 tools).
- `mcp-server/src/__tests__/aa.test.ts` — 30 cases including the custody-free invariant test.
