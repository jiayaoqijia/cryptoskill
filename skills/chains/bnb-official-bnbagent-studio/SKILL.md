---
name: bnbagent-studio
description: The single entry point for bnbagent-studio - a TypeScript CLI (`bag`) for building a blockchain SELLER agent that earns U/USD1/USDC/USDT stable assets on BNB Chain via ERC-8004 + ERC-8183 + an x402 or MPP B402 payment face (Pieverse LLM inside). Mainnet USD1 is EIP-3009-only and still requires live-release gates; Testnet USD1 is unavailable. Load this skill whenever the user works in a bnbagent-studio / `bag` project, or wants to create/scaffold, deploy, run, debug, operate, or monetize such a seller agent (composable A2A, MCP, and alternative X402/MPP faces; BNB Chain trial, AWS AgentCore, Azure Foundry, or CreateOS). All detailed playbooks ship as references/ files inside this skill - route via the decision tree in the body. When invoked with arguments, treat them as the user's intent and route the same way.
---

# bnbagent-studio (the single entry point)

`bnbagent-studio` (CLI: `bag`) wires the `@bnbagent/sdk` protocol layer (wallet / ERC-8004 / ERC-8183 / Pieverse LLM) into a TypeScript agent project, then deploys it as a **single blockchain seller runtime**. A2A, MCP, and X402 are composable public faces selected with `--protocols`; every wallet kind scaffolds A2A + X402 with both ERC-8183 and B402 rails by default (for altana the paid B402 payout lands at the admin address). `bag deploy` uses **scheme C**: every new deploy or redeploy explicitly selects BNB, AWS, Azure, or CreateOS; a recorded deployment is used only to offer an explicit update action, never as a silent default. BNB is a 48h testnet trial and is disabled after expiry. AWS and Azure self-deploy into the user's own account. All cloud lifecycle mutations go through the pinned deploy packages (NodeOps uses their Node.js SDK); the optional AWS CLI is used only by the fail-open, read-only AgentCore quota check in `bag deploy prepare`. AgentCore and Azure Foundry share the unified A2A/X402 entrypoint; Azure rejects MCP. Treat an incompatible provider row as unavailable-do not force through it or mutate the scaffold during deploy.

Invoked as `/bnbagent-studio <ask>`? Treat `<ask>` as the user's intent and route it through the decision tree below, exactly like a natural-language ask.

## Runtime preflight

This skill requires `bag` **0.0.14 or newer**. Before following any workflow,
run the read-only command `bag --version`. If `bag` is missing or older, stop
and ask the user to run `npm install -g @bnbagent/studio-cli@latest`, then
repeat the version check. Never install or upgrade a global executable without
the user's approval.

<!-- bag-compatibility: >=0.0.14 -->

## The single seller runtime model (the invariants)

One deployed runtime, one signer: a single valuable Agent serves the selected faces (A2A `src/unifiedMain.ts` on `:9000`, MCP `src/mcpMain.ts` on `:8000/mcp`, or A2A-native `src/dualMain.ts` on `:9000` with tunneled `/mcp`), holds the key, and signs in-process. The ERC-8183 rail exposes exactly two bounded operations - **`negotiate`** (deterministic canonical USD price conversion + EIP-191 sign; **no LLM touches money**) and **`notify_funded`** (verify the funded job → produce the deliverable → submit on-chain; A2A acks then delivers in the background, MCP delivers synchronously in the tool call). The optional x402 rail adds an anonymous HTTP request at `/x402`; positive prices settle through B402 before work, while explicit zero is FREE passthrough and bypasses the facilitator. It does not expose a general signing tool. Read-only chain tools remain available. ALL signing is fixed entrypoint code in `app/agent/src/signing.ts` or the runtime's bounded x402 payment handler, never an LLM-callable tool. The encrypted keystore lives at the workspace root `.studio/wallets/`, outside the deploy codeLocation, and is injected only via the selected provider's delegated secret channel. `settle` is manual (`bag erc8183 settle`). Full layout and lifecycle details live in the references below - read them before acting.

## Decision tree - which reference to read next

**References are plain markdown files installed in THIS skill's directory** at `references/<name>.md`. When a row matches, READ THAT FILE before acting - do not answer from memory.

| User intent | Read / do |
| --- | --- |
| Create a brand new single seller project from zero | `references/bnbagent-studio-scaffolding-agent.md` |
| Add wallet / the single seller runtime to an existing TypeScript agent | `references/bnbagent-studio-adding-to-project.md` |
| Run / debug / dev / doctor / RPC / balance / incident triage | `references/bnbagent-studio-operating.md` |
| Report a CLI problem or share product feedback | Run `bag feedback`, review the local JSON bundle before attaching it, and read `references/bnbagent-studio-operating.md`; Studio never uploads or submits it automatically |
| Implement what the Agent sells, tune pricing, publish over A2A and/or MCP, defend disputes (seller flow) | `references/bnbagent-studio-selling-via-8183.md` |
| Sell one paid or FREE HTTP request through the selected B402-backed x402 or MPP rail (pricing choice; paid merchant application, RSA key, credentials, IP allowlist, activation) | `references/bnbagent-studio-selling-via-b402.md` |
| Deploy / redeploy / status / logs / destroy | Run `bag deploy` and explicitly choose a provider. Non-interactive deploy requires `--provider bnb\|aws\|azure\|nodeops --yes` (and `--allow-multiple` when keeping another provider active). Read `references/bnbagent-studio-use-bnb-trial.md`, `references/bnbagent-studio-use-aws-agentcore.md`, `references/bnbagent-studio-use-azure-foundry.md`, or `references/bnbagent-studio-use-createos.md` for the selected provider. `bag deploy status` lists every recorded provider; multi-deployment logs/verify/destroy require `--provider`. |
| Build an agent and deploy it to NodeOps; CreateOS account/wallet deployment, wallet balances or payment recovery | Read `references/bnbagent-studio-use-createos.md` first; also read the scaffolding reference for a new project. Use its task-completion flow to select compatible defaults, honor an explicit hosting-payment protocol and verify the deployed business operation. |
| Wire chain-read tools into the Agent's LLM (AI SDK `tool()` wrappers, or any TS agent framework) | `references/bnbagent-studio-wiring-llm-tools.md` |
| Buy a service from another ERC-8183 seller via CLI - incl. testing your own seller from the buyer side (v2/internal - NOT the v1 seller product flow) | `references/bnbagent-studio-buying-via-8183.md` |
| Give the agent a PAID x402 capability - CMC market data / Binance Bazaar (B402) merchants / any pay-per-call API (`bag x402 trust`, x402-buyer recipe, 402 buyer errors) | `references/bnbagent-studio-buying-from-bazaar.md` |
| Give the agent a native MPP+B402 buyer capability (`bag mpp trust/quote/buy`, mpp-buyer recipe, recipient/realm pins, unknown outcomes) | `references/bnbagent-studio-buying-via-mpp.md` |
| Extend the EIP-712 signing allowlist (custom contract / new x402 service / diagnose `PolicyViolation` / `X402PolicyError`) | `references/bnbagent-studio-extending-signing.md` |
| Project uses `[wallet].kind = "twak"` (create / fund / SIWE-bind / container deploy / known limitations) | `references/bnbagent-studio-using-twak-wallet.md` |
| NodeOps wallet selection, deployment payment or hosting renewal | Read `references/bnbagent-studio-use-createos.md` before choosing a wallet or promising payment/renewal support. |
| Project uses `[wallet].kind = "altana"` (admin keystore / bounded session / quote checker / x402 allowance / local dev / session-only deploy + renewal) | `references/bnbagent-studio-using-altana-wallet.md` |
| (Pieverse projects only) Fund the LLM, switch to a paid model, hit insufficient credits (`PieverseBudgetExhaustedError` / `PieverseAccountBalanceExhaustedError`) | skill `funding-pieverse-llm` (project-scope; emitted at `bag init --llm-provider pieverse-llm`) |

If two or more match, read both - they're designed to be orthogonal.

### Where the references live

Next to this file: this skill installs as a directory with a `references/` subdirectory (Claude Code: `~/.claude/skills/bnbagent-studio/references/` or the project-scope `<project>/.claude/skills/bnbagent-studio/references/`; Cursor: `bnbagent-studio/references/` under the rules directory, beside the `.mdc` rules). If a reference file is missing, `bag skills install` (re)installs it.

<!-- Maintainers: this skill's DESCRIPTION only carries ENTRY intents (identity + create/deploy/run/debug/operate/monetize). Mid-journey topics such as twak, EIP-712, disputes, buyer flow, and tool wiring are routed by the decision tree above and must NOT be added to the description - see docs/design/decisions.md §14. -->

## 5 core commitments (always honor)

1. **Agent project code is user-owned** - recipe-emitted files are theirs to edit; studio doesn't auto-rewrite them.
2. **Keep wallet material out of chat, source and build artifacts; describe the runtime custody boundary accurately.** The encrypted keystore lives at the workspace root, outside the deploy codeLocation. Payment integrations use public signing interfaces without private-key export. Deploying an evm-local agent separately sends its encrypted keystore and unlock password to the selected runtime through the provider's runtime-secret channel, so that runtime can sign. NodeOps hosts that runtime on third-party infrastructure in both account and wallet modes; do not promise that its operator never receives usable wallet material. Use an existing wallet only within the user's authorized custody scope; otherwise prepare a dedicated deployment wallet and explain funding requirements. Altana's supported runtime paths receive only `ALTANA_SESSION`, not the local admin keystore; this does not make Altana compatible with NodeOps hosting payment. The BNB trial remains testnet-only with a throwaway wallet recommended.
3. **Signing is fixed handler code, never an LLM-callable tool** - the ERC-8183 rail exposes bounded `negotiate` / `notify_funded` flows and the x402 rail exposes a bounded request handler; raw/arbitrary signing is never exposed. Read-only chain queries remain read-only tools.
4. **SDK protocol layer stays pure** - studio's opinions don't pollute `bnbagent-sdk`.
5. **The user can jump ship at any point** - emitted code is theirs to edit / fork / migrate; studio depends on no closed SaaS. Emitted code imports from `@bnbagent/studio-runtime` and depends on that runtime lib (not the CLI), so uninstalling the `@bnbagent/studio-cli` package never breaks a deployed agent.

Treat ERC-8183 amounts as decimal strings at CLI/config boundaries and `bigint` internally. A job binds exactly one immutable catalog token. Mainnet Seller assets share one USD price and may be any non-empty U/USD1/USDC/USDT subset; Testnet supports `TEST_U`, `TEST_USDC`, `TEST_USDT` and does not support USD1. Testnet U and USDC are rail-specific: U uses `0xc70B…` with 18 decimals for ERC-8183 and `0x3309…` with 6 decimals for B402/x402/MPP; USDC uses `0x6454…` with 18 decimals for ERC-8183 and `0xEC1C…` with 6 decimals for B402/x402/MPP. Mainnet USD1 is 18-decimal EIP-3009 (`World Liberty Financial USD / 1`) only, without Permit2, and its live Commerce/facilitator verification remains a release gate. Buyer omission means U; an unavailable or underfunded selection yields verified `--asset` hints but never an automatic switch. Canonical FREE is `[payments.seller]` with `price_usd = "0"`; it is an explicit choice, not a missing value. Legacy U-only `[payments.erc8183]` price bounds apply only when the canonical section is absent; canonical and legacy price/asset fields together are an ambiguity error. If a custom stack is selected, require all three contract-address overrides from one verified deployment. The same canonical zero is anonymous FREE passthrough for B402: verify/settle and secret injection are skipped. Positive prices retain the paid merchant flow; `permit2-upto` is never active.

## CLI groups at a glance

`init`, `scan`, `recipe`, `skills`, `wallet`, `erc8004`, `erc8183`, `x402`, `mpp`, `agents`, `config`, `env`, `dev`, `doctor`, `feedback`, `audit`, `deploy`, `platform`, `llm`, `bundle`, `budget` - see `bag --help` for details. `bag deploy [--provider bnb\|aws\|azure\|nodeops] [--backend aws\|azure]` is the primary deploy command; `--backend` is valid only for provider `bnb` and confirms the recipe-derived managed backend. `prepare`, `list`, `verify`, `status`, `info`, `destroy`, `logs`, and `fix-gitignore` remain lifecycle subcommands (`deploy agent` is a deprecated compatibility alias). Provider deploy/status/logs/destroy and deploy-time credential validation are delegated to pinned `@bnbagent/deploy-cli@0.6.6`.

## Tool surface

- **CLI** - write-side (wallet ops, on-chain register, x402/MPP buy, deploy)
- **MCP** - an external seller face (`bag init --protocols MCP`), composable with A2A; dual mode is A2A-native so `HEALTHY_BUSY` preserves background work
- **`@bnbagent/studio-runtime/tools`** - 15 pure read-only functions, wrapped into LLM tools by the chain-tools recipe (read `references/bnbagent-studio-wiring-llm-tools.md`)

## Where docs live

- `docs/design/architecture.md` - layered architecture
- `docs/design/decisions.md` - decision records (Pieverse default, signing policy, chain tools, zero-deposit, skill reorg, **single seller runtime + protocol faces**)
- `docs/guides/pieverse-integration.md` - Pieverse LLM full lifecycle
- `docs/guides/user-guide.md` - end-user procedures
