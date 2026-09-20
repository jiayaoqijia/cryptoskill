---
name: bnbagent-studio-using-twak-wallet
description: When the user's project has [wallet].kind = "twak" (a fully-supported wallet kind, opt in with `--wallet-kind twak`) - creating the Trust Wallet Agent Kit wallet, anchoring its address, funding it, SIWE-binding for Pieverse, deploying it as a container, and working around its known limitations.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-using-twak-wallet

Procedure for setting up and operating the **twak** wallet kind (Trust Wallet Agent Kit CLI) in a bnbagent-studio project. twak is a **fully-supported** wallet kind - opt in at scaffold with `bag init <name> --wallet-kind twak` (`evm-local`, a local keystore, is the default). The wallet is a **self-custody, AES-256-GCM-encrypted mnemonic** the user controls (not a hosted service), living by default in a **project-dedicated** home `.studio/twak` (`[wallet].twak_home`), isolated from your main `~/.twak`. The default kind is `evm-local` (local keystore); re-scaffold with `--wallet-kind twak` to use twak.

## 1. CLI installation is project-managed

`bag init --wallet-kind twak` pins `@trustwallet/cli@0.20.0` in the generated `app/agent/package.json`; the normal `pnpm install` installs it. Do **not** ask the user for a global installation and do not call the upstream CLI directly. Studio and the runtime resolve `app/agent/node_modules/.bin/twak`, and `bag doctor` / `bag deploy prepare` verify the project-pinned version floor.

## 2. Studio-managed setup - no upstream wizard

The user creates a Trust Wallet NaaS app at https://portal.trustwallet.com/dashboard/apps, but must never paste the Access ID, HMAC secret, or wallet password into the AI chat. On a human TTY, `bag init` performs the setup automatically. To retry or complete a non-onboarded scaffold, run from `app/agent`:

```bash
bag wallet twak-init
```

This one Studio command:

1. Collects the NaaS Access ID and HMAC secret through hidden Studio prompts. It never starts `twak setup` or asks which AI harnesses to wire.
2. Runs the project-pinned `twak init --json` with the two credentials in the child environment.
3. Performs an authenticated `twak search BNB --networks 20000714 --limit 1 --json` read. Newly written credentials are removed if this verification fails; pre-existing credentials are never deleted.
4. Generates `TWAK_WALLET_PASSWORD` from 32 bytes of the OS cryptographic random source and writes it to `.studio/.env.local` (0600). There is no weak-random fallback and the value is never printed.
5. Creates the project-dedicated wallet with `--no-keychain --json`, tightens `.twak/` to 0700 and its credential/wallet files to 0600, reads the BSC address, and anchors it into `studio.toml`.
6. Refuses to replace an anchored identity and never overwrites an existing wallet or credential file.

Upstream twak v0.20.0 requires `--password` during wallet creation, so the generated password is briefly present in that one child process's argv. It does not enter the user's shell history, Studio output, diagnostics, or AI transcript. Runtime signing reads it from the environment and does not put it on argv.

For non-interactive automation, the user can put `TWAK_ACCESS_ID` and `TWAK_HMAC_SECRET` in `.studio/.env.local` themselves before running `bag wallet twak-init`; Studio still generates the wallet password. The legacy `--password-stdin` and `--password-file <0600-file>` options remain explicit compatibility overrides, not the happy path.

After setup:

```bash
bag wallet show
bag llm activate
bag doctor
```

No separate `bag wallet new` step is required. An existing wallet is adopted only after Studio verifies its password and reads its address. If its password is not already in `.studio/.env.local`, the user enters it through a hidden Studio prompt or supplies the original password using `--password-stdin` / `--password-file <0600 file>`; Studio never invents a replacement password for an existing wallet.

### Other wallet placements

The default is a new project-dedicated `.studio/twak` home, isolated from the user's main `~/.twak`. Alternatives are explicit:

- Reuse an existing wallet across agents with `bag init --twak-home <home-style-path>`; the path contains `.twak/wallet.json`.
- Reuse the main `~/.twak` only with `bag init --twak-home ~`. This is discouraged because deploy would ship that wallet material through the selected secrets channel.

Each wallet address has its own ERC-8004 identity, Pieverse SIWE binding, and secret bundle; `bag doctor` / `bag deploy` resolve the configured `[wallet].twak_home`.

## 3. Fund it - and keep it a HOT wallet

Two assets, two different rules:

- **U (payment token)** - the principal for x402 topups (LLM credit) and what buyers pay you. x402 payments are **GASLESS** (EIP-3009, the facilitator settles), so topping up burns no BNB. A twak wallet is also a supported b402 **seller** payout wallet (`bag init --wallet-kind twak --rails b402`); receiving needs no signature or gas either.
- **BNB (gas)** - **testnet canonical contracts normally use sponsorship; mainnet needs a little for ERC-8183.** Testnet: the SDK forwards MegaFuel's testnet paymaster (`--paymaster-url`, twak >= 0.20.0). Sponsorship still depends on the paymaster policy covering the target contract and method; keep a little tBNB (~0.007) as fallback. Mainnet: x402 stays gasless and `bag 8004 register` is gas-sponsored by twak internally (Trust gateway - studio passes no paymaster flag), but **`8183 settle` / `fund` self-pay gas**, so keep ~0.007 BNB on the wallet for them.

> ⚠️ **MegaFuel testnet relay reliability (BUG-029).** The bsctestnet relay has been observed accepting a sponsored write, returning a tx hash, and then never broadcasting it - the hash is unverifiable on every public RPC and the wallet nonce never moves (reproduced 2026-07-24 and 2026-07-28 with raw `twak erc8183 create-job --paymaster-url …`). Do NOT treat raw `twak erc8183` sponsored bsctestnet writes as a stable PASS path for tests/CI. Drive the write through studio (`bag erc8004 …`, `bag erc8183 …`) or the SDK's `TWAKProvider` instead: those classify the failure (`RelaySubmissionUnverifiedError` = relay swallowed it, never persist the hash as pending; `TransactionPendingError` = the tx IS visible, wait) instead of a bare receipt timeout. Self-pay escape hatches: `--no-paymaster` on studio 8004 writes, or `BNBAGENT_USE_PAYMASTER=0` for any studio/SDK call.

**Hot-wallet rule**: fund only a few days of spend. The Agent wallet is an operational hot wallet, not a treasury - the on-chain balance is the one spending limit nothing can bypass. Studio's daily caps (`[budget].max_per_day_usd`) are in-process guardrails: real across CLI runs (persisted to `.studio/spend-ledger.json`), best-effort in the deployed runtime (in-memory, resets on cold start).

On testnet, message https://t.me/bnbchain_official_bot with `I would like to get tBNB to my wallet <address>` for gas and `I would like to get U to my wallet <address>` for ERC-8183 U. More options: https://docs.bnbchain.org/bnb-smart-chain/developers/faucet/ (tBNB) and https://united-coin-u.github.io/u-faucet/ (U). Mainnet: U via PancakeSwap; keep BNB for ERC-8183 fund/settle.

## 4. SIWE binding (Pieverse) - ALWAYS bind before paying

Pieverse attributes x402 topups to the **SIWE-bound payer address** (the paid call carries no session header on the twak path). `bag llm activate` performs the SIWE login (an EIP-191 `sign_message`, which twak supports) before any payment, so the normal flow is safe. If you ever top up through a custom path: bind first, pay second - an unbound payment cannot be attributed.

## 5. Local dev (no Docker) vs deploy (Container image)

**Local dev needs no Docker.** `bag dev` runs the agent **in-process** by default (the TS entrypoint, no Docker) - the keystore/twak materialize hooks are no-ops locally, so in-process exercises the same code path as the deployed container minus the image. Use `bag dev --container` only if you want the AgentCore dev container for full image parity (that mode runs via `agentcore dev` and needs Docker / Podman / Finch); it is **not** required to develop or test the twak agent locally.

**Deploy ships a Container image.** The managed AgentCore image can't host the twak CLI toolchain, so a twak Agent deploys as a **custom container** (Node >=22

- the twak CLI). `bag init` already configured everything: `agentcore.json` registers a `Container` runtime and `app/agent/Dockerfile` builds the image (linux/arm64 - an x86 machine needs docker buildx for cross-build).

* Local Docker is **required** for `bag deploy --provider aws`: the pinned `bnbagent-deploy` (to which Studio delegates all cloud lifecycle mutations) builds the image locally (linux/arm64) and pushes it to ECR - there is no remote-build fallback, so the Docker daemon must be running.
* Wallet material reaches the runtime ONLY via AWS Secrets Manager (`TWAK_WALLET_JSON` / `TWAK_CREDENTIALS_JSON` / `TWAK_WALLET_PASSWORD`), never inside the image. `bag deploy prepare` verifies all of this.

## 6. Known limitations (upstream twak CLI v0.20.0)

| Limitation | Upstream ref | What you see |
| --- | --- | --- |
| ~~Seller `submit` unavailable~~ | ~~REQ-1~~ RESOLVED in v0.19.0 | `submit --opt-params` works - verified on-chain. |
| ~~Seller `quote` signing broken~~ | ~~S-11 regression in v0.19.0~~ RESOLVED in v0.19.1 | v0.19.0 hex-decoded `0x…` messages and signed the bytes, so provider_sig never verified (testnet also rejected `sign-message --chain bsctestnet`). v0.19.1 signs the literal text (EIP-191): `sign_quote` works on both wallet kinds. |
| ~~No testnet paymaster URL~~ | ~~REQ-2~~ RESOLVED in v0.20.0 | twak accepts `--paymaster-url`; the SDK forwards MegaFuel's testnet endpoint on eligible writes. Actual sponsorship depends on the paymaster policy covering the target and method (the relay itself is flaky - see the BUG-029 warning in §3). The CLI floor is **0.20.0**. |
| Custom ERC-8004 registry | supported | Set `ERC8004_REGISTRY_ADDRESS`; the SDK requires the intent target and env override to match before invoking twak. Sponsorship still depends on paymaster policy coverage, so keep fallback tBNB. |
| Custom ERC-8183 targets unavailable | upstream feature request | twak v0.20.0 has no Commerce/Router/Policy address option. Studio doctor/prepare and the SDK fail closed instead of silently executing on canonical contracts; use `evm-local` for a custom ERC-8183 deployment. |
| No generic EIP-712 signing | P0 (won't fix) | `[wallet.signing]` is ignored; payments go through the delegated payer's own prechecks + `--max-payment`. Endpoints needing an `Authorization` header _and_ x402 are unavailable (e.g. `bag llm key new --initial-usd > 0` - use `--initial-usd 0` + topup + allocate instead, same end state). |
| No wallet import | S-6 | Switching wallet kinds changes your address → re-run `bag 8004 register` (new on-chain identity). |
| Programmatic wallet creation forces password onto argv | S-8 | Bridged by `bag wallet twak-init`: Studio generates 32 CSPRNG bytes, persists the value privately before creation, and forwards it only to the short-lived child because twak requires the flag. The value never enters user shell history or output. |
| CLI has no daily/monthly caps | - | Studio's policy layer (`[budget].max_per_day_usd`, host allowlist, per-request caps) is the spend authority for both wallet kinds. |
| `twak wallet balance --chain bsctestnet` rejects the chain | BUG-031 | Fails with `CHAIN_UNSUPPORTED` even though `wallet address` and `erc8183` accept `bsctestnet`. Use `bag wallet balance` (RPC-based, works on testnet), or raw RPC: `eth_getBalance` for tBNB and an `eth_call` of `balanceOf(address)` on the U token for token balance. |
| `twak tx <hash> --chain bsctestnet` rejects the chain | BUG-032 | Same chain-registry gap on the readback path: transactions twak itself just mined on `bsctestnet` cannot be inspected with `twak tx`. Use public RPC (`eth_getTransactionByHash` / `eth_getTransactionReceipt`) or BscScan testnet instead. |
| Raw `twak erc8183 create-job` has no expiry preflight | BUG-030 | An `--expires-at` inside the policy's dispute window is accepted, all four funding steps succeed, and only the final `submit` reverts `SubmissionTooLate()` (`0x15e5dd74`). Prefer the SDK path (`ERC8183Client` preflights this); if you must use the raw CLI, set `expires_at ≥ now + deadline + dispute_window` - on testnet's 24h window, `now + 172800` (48h) is a safe floor. |

## 7. Quick health checks

```bash
bag doctor                  # [wallet] twak CLI / wallet / address-anchor checks
bag wallet show             # describe(): address, key_location, capabilities
bag wallet balance          # BNB + U via RPC (works on testnet too)
bag deploy prepare          # container/Dockerfile/secret checks before deploy
```
