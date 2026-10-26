---
name: bnbagent-studio-using-altana-wallet
description: Use when a bnbagent-studio project selects wallet.kind = "altana" and needs the encrypted admin keystore, bounded runtime session lifecycle, ERC-8183 quote checker, x402 allowance, local dev, or session-only deployment and renewal.
---

# Using the Altana wallet

Altana separates trusted administration from runtime authority:

- `.studio/wallets/<address>.json` is the encrypted admin keystore.
- `.studio/wallets/altana-session.json` is the one bounded, expiring runtime session and must stay mode `0600`.
- `WALLET_PASSWORD` is admin-only. The Agent gets `ALTANA_SESSION`, never the password or admin keystore.
- Generic signing is refused. ERC-8183 uses `sessionQuoteSigner()` and the approved quote checker.
- The generated project pins `@bnbagent/sdk@0.6.1` and `@altananetwork/sdk@0.7.1`; doctor, readiness, and runtime loading reject Altana SDK drift, and deploy readiness refuses an `@bnbagent/sdk` below the 0.6.1 security floor (doctor warns). SDK 0.5.4 introduced selector-bound calls, removed session-key token approvals, and requires an admin-provisioned bounded Commerce allowance. Projects upgrading from SDK versions older than 0.5.4 must update it, re-grant with `bag wallet session grant --force`, and redeploy.
- After upgrading to SDK 0.6.1: a wallet that ran `x402-setup` before Studio 0.0.16 should `bag wallet session revoke --yes` (optionally `--archive-rpc-url` to lock down what the session signed), re-grant, and re-run `x402-setup --archive-rpc-url`. Sessions granted with SDK 0.5.0–0.5.3 need a one-time check of the identity Registry's `ApprovalForAll` / `Approval` events for the wallet. Retire sessions by revoking them; expiry runs no code.
- Deployment ships ONLY the serialized session as the `ALTANA_SESSION` runtime secret; the admin keystore and `WALLET_PASSWORD` never leave the operator machine. Renewal after expiry: `bag wallet session grant --force`, then re-run `bag deploy`. Readiness fails on a missing/expired/address-mismatched session, a group/world-readable session file, a session inside the artifact root, or an unresolvable project-local `@altananetwork/sdk`; it warns under 7 days remaining. `bag deploy verify` needs `--skip-register` (no generic signing for the ERC-8004 register).
- Altana refuses generic message signing, so Pieverse SIWE cannot authenticate `bag llm activate` or runtime credit renewal. `bag init --wallet-kind altana --llm-provider pieverse-llm` is rejected outright; use OpenRouter, OpenAI, or Anthropic (API-key providers). `bag llm activate` and `bag doctor` also flag the combination on projects edited by hand.

## Procedure

```bash
bag init <name> --wallet-kind altana --destination self --no-onboard
# --destination platform is also accepted (48h trial; same session-only transport).
# Non-TTY defaults to OpenRouter. In a TTY, choose OpenRouter, OpenAI, or
# Anthropic from the provider menu; a flag remains available when desired:
# bag init <name> --wallet-kind altana --llm-provider anthropic --destination self
# Edit <name>/.studio/.env.local and set WALLET_PASSWORD first.
cd <name>/app/agent
bag wallet new
# after GitHub login, request the configured tBNB + U grant for the admin
bag wallet fund
bag wallet session grant
bag wallet session status
bag doctor
bag dev
```

`bag wallet fund` always uses the Altana admin's encrypted keystore for an
EIP-191 ownership signature and sends funds to that same admin address. The
bounded runtime session is not involved in faucet claims.

Interactive grant recommendations are 10 U/day, 30 days, register=yes. In a non-TTY, pass `--budget-u`, `--expiry-days`, optional `--no-register`, and `--yes`. Stdout from a successful grant is only the session public key.

The grant persists the owner-only session, provisions a Commerce allowance no higher than its U-token cap, and approves the quote checker. Every relay-backed management write must return `CONFIRMED`; `PENDING` fails closed and preserves the session file. If either setup step fails after the paid grant, repair both with:

```bash
bag wallet session grant --approve-only
```

`--approve-only`, runtime loading, and deploy readiness reject pre-0.5.4 target-wide sessions. Replace one with `grant --force`; Studio zeros the old Commerce allowance before revoking, and both operations must be confirmed before the new grant begins. Revoke with `bag wallet session revoke --yes`; the file is deleted once the revoke is confirmed. The SDK then resets the outer Permit2 approval of the catalog tokens plus every x402 token Studio arms (a split asset such as Testnet USDC settles B402 on its own contract, so Studio passes it explicitly and resets any token the batch did not cover), which pauses x402 until the next `x402-setup`; with `--archive-rpc-url` it also locks down the allowances the session signed. If that reset fails after the revoke, Studio resets the x402 tokens itself and names any it could not — retry with `bag wallet session permit2-reset --yes`. `grant --force` does not grant the replacement while such a token remains.

x402 buying remains separate and exact-bounded:

```bash
bag wallet session x402-setup --allowance <amount> --archive-rpc-url <archive-rpc> --yes
```

A non-zero Permit2 approval re-arms allowances earlier sessions signed (SDK 0.6.1), so pass exactly one of:

- `--archive-rpc-url <url>` (or `STUDIO_BSC_ARCHIVE_RPC` / `STUDIO_BSC_TESTNET_ARCHIVE_RPC`): historical state, `eth_getProof`, and logs since the wallet's first EIP-7702 delegation. The SDK locks those allowances down in the approval batch. Public BSC RPCs do not qualify; the command fails before any relay call when the probe fails.
- `--no-prior-permit2-checker`: the user attests no session of this wallet was ever approved for x402. Studio refuses it once `.studio/wallets/altana-x402-approvals.json` or the project's audit log shows an earlier `x402-setup`.

Ask the user which applies; never pass the attestation on their behalf without that confirmation. Use an Altana agent wallet with no other Permit2 approvals.

The ceiling applies per asset, in that asset's own units, and is written on each
asset's b402 token contract at that contract's decimals. Without `--asset`, the
command arms every asset that is both spendable under
`payments.allowed_payment_tokens` and settled through `permit2-exact`; EIP-3009
assets (testnet U, mainnet USD1) are skipped because they need no allowance.

Once armed, `bag x402 buy` may use an Altana Permit2 Exact route only through
`requestExact`: it binds the same challenge's resource, exact CAIP-2 network, canonical asset,
atomic amount, payTo, scheme/version, method, timeout and curated proxy/name/version before
signing. The preflight checks the selected token's bounded allowance against canonical Permit2;
the proxy is a separate trust root. EIP-3009-only routes still require an EOA signature. These
are enforced implementation boundaries; complete merchant/live-chain verification remains a
release gate. Use `@altananetwork/sdk` 0.7.1 in the project.

Altana can also be the b402 **seller** payout wallet for a positive price: the payout lands at `[wallet].address`, which for an EIP-7702 altana account is the admin EOA, so the locally-held admin keystore can always move the revenue. Issue the B402 merchant credentials for that exact address. Explicit `[payments.seller]` `price_usd = "0"` stays FREE passthrough (no payout, bypasses B402). The outbound buying authority above remains a separate feature.

For troubleshooting, run `bag doctor` and `bag wallet session status`. Do not print, parse, or copy the `signer` portion of the serialized session, and never move `.studio/wallets/` under `app/agent/`.
