---
name: bnbagent-studio-scaffolding-agent
description: When the user wants to create a brand-new blockchain SELLER from zero - a single valuable Agent on AWS Bedrock AgentCore that serves A2A + X402 with ERC-8183 + B402 by default (or another selected face/rail combination), holds the key, and signs in-process. Drives the full intake → todo-list → execute flow.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-scaffolding-agent

Procedure for **greenfield** seller creation. Audience: Claude Code (or another agent) running in an empty directory with shell + edit access.

For a request that already selects NodeOps, first read `bnbagent-studio-use-createos.md` and follow its build-and-deploy task flow. Its targeted intake and provider choices override the generic form, platform default and AWS-specific provisioning below. Do not make the user complete the full technical questionnaire or confirm a provider they already selected. Use this reference's project-generation mechanics, then return to the NodeOps reference for payment, deployment and business verification.

**Different from** the `bnbagent-studio-adding-to-project.md` reference (in this same references/ directory): that one adds to an existing repo; this one creates from zero.

## The single seller runtime (current workspace layout)

`bag init` scaffolds a **blockchain seller** as a thin workspace root containing **one sub-project** under `app/agent/`:

```
<name>/                              workspace root (thin wrapper / deploy anchor)
├── package.json                     workspace root marker (private)
├── pnpm-workspace.yaml              packages: ["app/agent"]
├── README.md                        1-page pointer at app/agent/
├── .gitignore
├── agentcore/                       AgentCore config dir (SELF-RENDERED by `bag init`;
│   │                                names the deploy + drives `bag dev --container`)
│   ├── agentcore.json               deploy descriptor (one native protocol + authorizerConfiguration)
│   └── aws-targets.json             AWS account + region
├── .studio/                          workspace-local state, outside the codeLocation
│   ├── .env.local                    wallet and provider secrets
│   └── wallets/                      evm-local keystore; Agent sole reader
└── app/
    └── agent/                       the single sub-project - the seller agent
        ├── package.json             @bnbagent/studio-runtime + @bnbagent/sdk + ai (AI SDK)
        │                            + protocol deps (A2A: @a2a-js/sdk + express;
        │                            MCP: @modelcontextprotocol/sdk)
        ├── tsconfig.json            builds src/ → dist/ (the deployed entrypoint is dist/*.js)
        ├── studio.toml              wallet / llm / budget / canonical payments.seller / rail config / storage
        ├── Dockerfile               container deploy path only (for example, twak)
        └── src/                     unifiedMain.ts / mcpMain.ts / dualMain.ts / sellerCore.ts / executor.ts / agentCard.ts / signing.ts / tools.ts / model.ts
```

- **The Agent (`<name>/app/agent/`, → AWS Bedrock AgentCore).** ONE valuable agent (memory / tools / skills / KB / LLM) that **serves the selected faces** (A2A: `0.0.0.0:9000`; MCP: `0.0.0.0:8000/mcp`; A2A+MCP: A2A-native `dualMain.ts` on `:9000` with `/mcp` tunneled), holds the key, and signs **in-process**. Its outward surface is two fixed-code commerce operations (A2A skills on `SellerAgentExecutor`, or MCP tools on the MCP server):
  - **`negotiate`** → canonical shared USD price converted exactly for the selected asset → `signing.ts` `signQuote` EIP-191 sign. **No LLM.**
  - **`notify_funded`** → `signing.ts` `verifySignedJob` (synchronous) → delivery: A2A ACKs then runs LLM work + `signing.ts` `submitResult` in the background (plus a best-effort in-process sweep of other FUNDED jobs); MCP runs the work and submit synchronously inside the tool call.

  ALL signing is fixed `app/agent/src/signing.ts` code, **never** an LLM tool - the LLM gets read-only chain tools only. The keystore lives at the **workspace root** `.studio/wallets/` (outside the `app/agent/` codeLocation) and is injected at deploy via AWS Secrets Manager - see Step 3 and Stage 4.

There is **no** second service, **no** keyless EC2 host, **no** `InvokeAgentRuntime` relay, and **no** background poller. The agent is its own public surface.

v1 is **seller-only**; chat / buyer roles are deferred to v2. (A studio agent can still _buy_ other agents' 8183 services via `bag erc8183 buy/fetch/...`, but the buyer flow is not yet productized.)

## Preconditions

- Node.js ≥22 available.
- `bnbagent-studio` (the CLI) installed - `npm install -g @bnbagent/studio-cli` (auto-pulls the `@bnbagent/studio-runtime` lib); for local dev use a monorepo clone (`pnpm install` at the workspace root). `bag --version` works.
- `bag skills install` was run so this skill is loaded.
- **Bun 1.3+ (`bunx`) - needed for `bag deploy`, NOT for `bag init`.** Deploys delegate all cloud lifecycle mutations to the pinned `@bnbagent/deploy-cli`, run via `bunx --bun` (override with `BNBAGENT_DEPLOY_COMMAND`); `bag deploy prepare` fails a CRITICAL check when `bunx` is missing. The npm `@aws/agentcore` CLI is needed ONLY for `bag dev --container` (image-parity local runs). The optional AWS CLI is used only for a fail-open, read-only AgentCore quota check during `bag deploy prepare`. If the AgentCore CLI is installed, ensure the `agentcore` that resolves first on PATH is that npm CLI, not the incompatible `bedrock-agentcore-starter-toolkit` shim some environments carry. (Node ≥22 and `bag` itself are NOT re-checked in the flow: running the CLI already required Node, and this skill only runs because `bag` is installed.)
- **Permission prompts on `bag` calls are normal - do not try to remove them.** The IDE asking the user to confirm each `bag` command is the expected flow; whether to allowlist anything is the user's own decision, made in their own settings UI/file. NEVER edit permission settings yourself, NEVER run `claude config` (or any equivalent) to grant yourself permissions, and do not ask the user to pre-authorize `bag` - `bag:*` includes money-spending commands (deploy, erc8183 buy/settle), so a blanket grant is unsafe.
- Current working directory is where the project should live. The project is created at `<cwd>/<name>/` - pick the parent before triggering this skill.

## Stage 1 - Intake (collect ALL answers in one round, then echo back)

**Do not ask one question at a time.** Present the full form in a single message, with defaults pre-filled. Accept the user's reply (which may be just "go with defaults" or selective overrides), then echo a confirmation block and proceed. This matches a shell-style prompt - one round-trip, then execute.

The fields (give the user all of them at once):

| # | Field | Options | Default |
| --- | --- | --- | --- |
| 1 | **Project name** | Must start with a letter, contain ASCII letters and digits only, and be at most 23 characters. `bag init` rejects `-`, `_`, `.`, and overlong names instead of renaming them. For example: `newsagent`, `twcopywriter`. | (required) |
| 2 | **Network** | `bsc-testnet` / `bsc-mainnet` | `bsc-testnet` |
| 3 | **LLM provider** | `pieverse-llm` / `openrouter` / `openai` / `anthropic` / `bedrock` | `pieverse-llm` |
| 4 | **Wallet kind** (`--wallet-kind`) | `evm-local` (encrypted local keystore at the workspace root; Studio generates its password on the new-wallet happy path; `--evm-keystore <v3-file>` copies and adopts an existing encrypted keystore with its original password; `--private-key` imports an existing raw key; CodeZip deploy) / `twak` (**fully supported, opt in with `--wallet-kind twak`** - project-pinned Trust Wallet CLI 0.20.0, self-custody encrypted mnemonic in a **project-dedicated** home `.studio/twak`, isolated from the main `~/.twak`; `bag wallet twak-init` performs credential init/verification, password generation, wallet creation/adoption, and address anchoring without the upstream wizard; container deploy. Reuse an existing wallet across agents with `--twak-home <path>`) / `altana` (bounded-session custody - admin keystore stays local, deploys ship ONLY the `ALTANA_SESSION` secret; zip deploy; not compatible with `pieverse-llm`; supports PAID B402 seller payout. Outbound x402 buying is separately opt-in and restricted to atomically bound `requestExact` + `permit2-exact`; flow: `references/bnbagent-studio-using-altana-wallet.md`) | `evm-local` |
| 5 | **Storage** | `local` (offline only) / `ipfs` / `s3` / `azure-blob`. Self-hosted deploys use BYOS credentials; managed-platform deploys receive an operator-owned storage endpoint and scoped token through the sealed runtime-secret channel. | `local` |
| 6 | **Protocol faces** (`--protocols`) | any non-empty subset of `A2A`, `MCP`, and one B402 face: `X402` or `MPP` (the payment faces are alternatives and cannot coexist) | `A2A,X402` for every wallet kind; use `--payment-protocol mpp` to choose `A2A,MPP` instead |
| 7 | **LLM model** | provider catalogue; for `pieverse-llm` the default `auto/free` runs at $0/token | `auto/free` |
| 8 | **Auto-topup** | `enable` / `disable` - lets the Agent auto-pay $U from the wallet when LLM credits run low | deferred (non-interactive `bag init` records no `[budget]`; enable later with `bag budget enable`) |
| 9 | **Scaffold destination** (`--destination`) | `self` (prepare the AgentCore scaffold for **your own** AWS account; runtime material stays under your cloud-account control) / `platform` (prepare for a 48h **testnet-only** trial on the BNB Chain managed platform - runs the _same_ agent in the **operator's** AWS, so a wallet key **leaves your control**; it hard-forces `[network].default = bsc-testnet`, pins runtime=`agentcore`, packages an artifact, and auth is GitHub device flow. Use a **throwaway** `bag wallet new`, never your main wallet). This is scaffold intent only; deploy still explicitly selects `--provider`. | `platform` while the trial campaign runs (bare init falls back to `self` once it ends, or when `--network bsc-mainnet` / a non-agentcore `--runtime` is passed) |
| 10 | **Unified seller price** (`--seller-price-usd`) | non-negative decimal USD string shared by every configured asset and enabled commerce rail; `0` explicitly selects FREE | `$0.10` |

`--erc8183-price` and `--b402-price` remain legacy compatibility inputs only. Studio converts either value into canonical `payments.seller.price_usd`; they have no independent default, and conflicting price flags are rejected.

v1 is **seller-only** - there is no role to choose. `bag init` scaffolds the single seller agent under `app/agent/` (serves the selected public faces, sole signer). Chat / buyer roles are deferred to v2.

**Architecture selections** (this playbook uses the advertised `agentcore` runtime; protocol faces are selected above). **Render these as their own visible table in the intake form**, right after the fields above - do NOT compress them to a one-line footnote: they are part of the config the user is confirming, and "where's A2A / the runtime?" is a real question. Each row: Field | Value | What it is.

| Field | Value | What it is |
| --- | --- | --- |
| **Agent stack** | AI SDK (`ai`) | The library the agent's brain is built with - the emitted `src/model.ts` factory returns an AI SDK `LanguageModel`, and `src/tools.ts` wraps the chain reads as AI SDK `tool()`s. (There is no `--framework` flag: the old framework axis folded into the runtime templates.) |
| **Runtime** | `agentcore` | AWS Bedrock AgentCore - where the agent is hosted and served (`--runtime agentcore`). |
| **Protocol faces** | selected above (`A2A,X402` default for every wallet; `A2A,MPP` when the alternative B402 adapter is selected; MCP composable on AgentCore) | A2A hosts agent card + JSON-RPC on `:9000`; MCP-only hosts `/mcp` on `:8000`; A2A+MCP uses A2A-native `dualMain.ts` on `:9000` and tunnels buffered MCP through the platform; X402 adds `/x402`, MPP adds `/mpp`, and a payment-only selection suppresses public protocol discovery. X402 and MPP never coexist. |

**Not surfaced** (handled automatically, no need to show or ask):

- **Dependency install** - on by default (`bag init` runs the package install for the workspace unless `--no-install`).
- **IDE skill target** - auto-detected (`--ide`), falls back to `claude-code`.

The following are auto-included by default (don't ask, just mention in the confirmation block):

- **Read-only chain tools** wired into the Agent's LLM (`app/agent/src/tools.ts`) - the LLM can query wallet / balances / ERC-8004 / ERC-8183 state but **never signs**.
- **LLM-credit auto-renew** via the emitted `app/agent/src/model.ts` - the Agent's `buildModel()` factory (in user-owned code) returns an AI SDK `LanguageModel` wrapped (via `wrapLanguageModel` middleware) with an **automatic, budget-gated auto-renew hook** that tops up the active Pieverse key before an LLM call when the cached balance is below the floor. The stack-neutral credit-ensurer logic lives in `@bnbagent/studio-runtime/pieverse` (`PieverseCreditEnsurer`); the AI-SDK shell is in the emitted `app/agent/src/model.ts`. This is the ONLY automatic signing path outside `signing.ts`; it rides on the hardened x402 buyer kernel (`@bnbagent/studio-runtime/x402`) but is **not an LLM tool** - the Agent (the sole key-holder) does it transparently inside the model wrapper. If the budget gate is off / exhausted, the hook raises `PieverseAccountBalanceExhaustedError` pointing at `bag llm topup --amount N`. Opt out via `[llm.auto_renew].enabled = false`.

Also collect, if natural to gather: a one-sentence description of what the agent does (used in the agent's instruction prompt and, later, in ERC-8004 metadata when the user runs `bag deploy verify`).

After collecting, **echo back** a confirmation block like:

```
Will create (single seller agent):
  name:        newsagent           (≤23 chars, alphanumeric, letter-start - AgentCore rule)
  agent:       app/agent/ (AgentCore, --protocols <faces>, sole signer, signs in-process)
  network:     bsc-testnet
  llm:         pieverse-llm (model: auto/free, auto-renew enabled)
  wallet:      evm-local - encrypted keystore at the workspace root (.studio/wallets/)
               (twak is fully supported too - opt in with --wallet-kind twak)
  price:       $0.10 shared by every configured asset and enabled commerce rail
  storage:     local (offline dev; switch to ipfs - needs a pinning endpoint + key - before deploy)
  fixed:       stack=AI SDK (model factory + tools), runtime=agentcore (AWS Bedrock AgentCore)
  protocol:    A2A (src/unifiedMain.ts on 0.0.0.0:9000; local 127.0.0.1:9000)
               or MCP (src/mcpMain.ts on 0.0.0.0:8000/mcp; local localhost:8000/mcp)
  destination: platform (campaign default while the trial runs - 48h testnet on the operator's AWS; key leaves your machine, use a throwaway wallet)
               or self (prepare for your own AWS Bedrock AgentCore; runtime material stays in your account - pass --destination self)
  extras:      read-only chain tools wired into the Agent LLM
  location:    /Users/.../newsagent/

Proceeding in 3 commands… (interrupt now if anything's off)
```

Then execute Stage 2 **without further prompts** until you hit a step that genuinely requires user action (funding the wallet).

For NodeOps deployment, first read `bnbagent-studio-use-createos.md`: select account or wallet mode, verify the installed deploy capabilities, and choose a compatible wallet. Use `--destination self` for NodeOps and the user's AWS/Azure account. NodeOps wallet funding uses USDC plus possible BNB approval gas; the optional U-funding guidance below does not cover cloud payment. Pieverse auto-renew renews model credits, not NodeOps hosting.

## Stage 2 - Generate a todo list (visible to the user)

Build a TodoWrite list. The shape depends on the `wallet kind`. The canonical 8-step layout (evm-local default, Pieverse default LLM; plus a conditional Step 6b for self-hosted durable storage):

> **Step 0 - Pre-flight (informational; do NOT block `bag init` on it).** `bag init` self-renders the `agentcore/` deploy descriptor, and deploys delegate to the pinned `@bnbagent/deploy-cli` run via `bunx`, so Bun is only needed later, at `bag deploy` time. Do **not** re-check Node or `bag` (both are necessarily present - running the CLI required Node, and this skill only loads because `bag` is installed).
>
> ```bash
> command -v bunx >/dev/null || echo "bunx not found - OK for init; install Bun 1.3+ before deploy: https://bun.sh"
> ```
>
> If Bun is missing at deploy time, **PAUSE** and have the USER install it (Bun 1.3+, or set `BNBAGENT_DEPLOY_COMMAND`). Likewise for `bag dev --container` only: the npm `@aws/agentcore` CLI must be present and must win on PATH over the incompatible `bedrock-agentcore-starter-toolkit` shim - global tools on the user's machine, so the user installs them, not you.

> **Onboarding note.** On a human TTY, `bag init` runs steps 3, 4 and 6 automatically (a new evm-local wallet gets a CSPRNG password without prompting; `--evm-keystore` instead asks for the existing file's original password; then Studio runs `bag wallet new`, zero-deposit-activates Pieverse, and prints faucet URLs). **You (Claude Code) drive `bag init` non-interactively**, so that auto-flow does NOT fire - keep steps 3/4/6 below. Pass `--no-onboard` to `bag init` to make this explicit and deterministic regardless of how the shell wires stdin.

1. `bag init <name> --llm-provider <p> --network <n> --storage-provider <s> --wallet-kind <k> [--protocols <comma-list>] [--rails <8183|b402|both>] [--seller-price-usd <usd>] --no-onboard` - scaffold the current workspace. **`<name>` must start with a letter, use ASCII letters and digits only, and be at most 23 characters.** `bag init` rejects `-`, `_`, `.`, and overlong names instead of renaming them. Pass `--wallet-kind evm-local` (default) or `--wallet-kind twak` (twak is fully supported - pass the flag to opt in), and `--storage-provider local` (default) or `ipfs`, per the Stage-1 choices; for twak, add `--twak-home <path>` ONLY if the user wants to reuse an existing wallet (otherwise omit - a project-dedicated `.studio/twak` is the safe default). Omit `--protocols` and `--rails` for the default A2A + X402 faces with both ERC-8183 and B402 rails (all wallet kinds, altana included — its paid B402 payout lands at the admin address). Pass either flag when the user chose another face/rail combination (`--protocol <one>` is only a legacy alias), add `--model <m>` only if the user overrode the provider default, and `--enable-auto-topup` / `--no-auto-topup` only if they made an explicit choice (otherwise omit - consent stays deferred). Pass `--seller-price-usd 0` only when the user explicitly chose FREE; omitting the flag preserves the shared `$0.10` paid default. The generated config writes canonical `[payments.seller]` once for every selected commerce rail. The older `--erc8183-price` and `--b402-price` options are compatibility inputs that are converted to that shared USD value and must agree when both are present. The canonical stack supports FREE; if a custom deployment is selected, set all three `ERC8183_COMMERCE_ADDRESS`, `ERC8183_ROUTER_ADDRESS`, and `ERC8183_POLICY_ADDRESS` values from that same stack. FREE bypasses B402 verify/settle and needs no merchant credentials. **Destination:** while the trial campaign runs, bare `bag init` (no `--destination`) defaults to `platform` - so pass `--destination self` **explicitly** whenever the user chose their own AWS, otherwise studio.toml silently records `platform` and the confirmation block you echoed no longer matches what was written. Omit `--destination` only when the user actually wants the `platform` 48h testnet trial (the campaign default) - do NOT treat that default as a mistake or re-confirm it; it is the intended behavior while the campaign is open. (Bare init also resolves to `self` once the campaign ends, or when `--network bsc-mainnet` / a non-agentcore `--runtime` is passed.) On the `platform` path `bag init` hard-forces `bsc-testnet`, pins `--runtime agentcore` + packages an artifact (a zip for the default evm-local and altana wallets, a container for twak). For evm-local a wallet key will later leave your machine, so pair it with a throwaway `bag wallet new`; for altana only the bounded session ships - do NOT create a new wallet (full flow: `docs/guides/platform-deploy.md`). Defaults `--runtime agentcore` (the only advertised runtime; the Preview `azure-foundry` runtime remains explicitly selectable but is outside this playbook; there is no `--framework` flag because the AI SDK model/tools story is part of the runtime templates). Creates `<name>/` workspace root + `<name>/app/agent/` (the single sub-project: A2A emits `src/unifiedMain.ts` (the express + A2A entrypoint, one code set for both deploy clouds) + `src/sellerCore.ts` (the protocol-neutral core; executor inherits it) + `src/executor.ts` + `src/agentCard.ts`; MCP emits `src/mcpMain.ts`; both include `src/signing.ts` + `src/tools.ts` + `src/model.ts` + their own `studio.toml` + `package.json` + `tsconfig.json`) + `<name>/agentcore/` (`agentcore.json` + `aws-targets.json`, self-rendered - no agentcore CLI needed at init). The workspace root holds the `agentcore/` deploy descriptor, the `.studio/wallets/` keystore, a thin `package.json` + `pnpm-workspace.yaml`, README, and `.gitignore`. (v1 is seller-only - no `--role`.)
> **Current storage choices:** `--storage-provider` accepts `local`, `ipfs`, `s3`, and `azure-blob`. The latter three are BYOS only for self-hosted deployment; a managed-platform deployment replaces the writer with its injected API endpoint/token.
>
> **Altana + custom contracts:** Altana sessions remain bound to the canonical ERC-8183 targets. Use `evm-local` for a custom Commerce/Router/Policy stack; doctor and deploy readiness reject this unsupported combination when the ERC-8183 rail is active.

2. `cd <name>`, then make sure the dependencies are installed. `bag init` already runs the install by default (skip only if it was scaffolded with `--no-install`); the manual equivalent from the workspace root is:
   ```bash
   pnpm install        # npm install works too - tooling is the user's choice
   ```
   The sub-project's `package.json` carries its deps: `@bnbagent/studio-runtime` (the runtime lib, pinned to the scaffolding CLI's exact version - NOT the CLI itself) + `@bnbagent/sdk` + `ai` (the AI SDK) plus the **protocol-specific** group - A2A adds `@a2a-js/sdk` + `express`, MCP adds `@modelcontextprotocol/sdk` instead (an A2A-only deploy never ships the MCP SDK, and an MCP-only deploy never ships the A2A one). For local dev against unreleased libs, `bag init` vendors local `.tgz` tarballs and points the manifest at them automatically.
3. **Keep all wallet secrets out of chat.** Never ask for, read, echo, or log a wallet password, NaaS Access ID/HMAC secret, mnemonic, or private key. Studio generates new-wallet passwords with the OS cryptographic random source and stores them in `.studio/.env.local` (0600). There is no weak-random fallback.

4. **Create / adopt the wallet** - depends on the wallet kind:

   - **twak**: the generated project pins `@trustwallet/cli@0.20.0`; no global CLI install is needed. `bag init` on a human TTY delegates the full happy path to Studio. For a `--no-onboard` or agent-driven scaffold, ask the user to create a NaaS app at https://portal.trustwallet.com/dashboard/apps and run this command in their terminal, where Studio can collect both values through hidden prompts:

     ```bash
     cd app/agent && bag wallet twak-init
     ```

     Do not run or explain the upstream `twak setup` wizard. `twak-init` uses the project-pinned binary, runs `twak init --json`, verifies an authenticated read, generates and persists `TWAK_WALLET_PASSWORD`, creates/adopts the project-dedicated no-keychain wallet, and anchors the address. No separate `bag wallet new` step exists. For CI, the user may place `TWAK_ACCESS_ID` + `TWAK_HMAC_SECRET` in `.studio/.env.local` themselves; never route them through chat. Reuse an existing wallet only with explicit `--twak-home <home-style-path>`; `--twak-home ~` is a discouraged opt-in to the main wallet. Load `bnbagent-studio-using-twak-wallet.md` for the exact security and deploy contract.

   - **evm-local** (default): the new-wallet TTY happy path generates `WALLET_PASSWORD` with the OS CSPRNG, persists it privately, then creates the encrypted keystore in-process. After `--no-onboard`, run `(cd app/agent && bag wallet new --generate-password)` for the same non-interactive safe path. It refuses to replace an existing or anchored wallet. For an existing encrypted v3 file, prefer `bag init ... --wallet-kind evm-local --evm-keystore <path>` and use the file's original password; Studio copies and verifies the file without re-encrypting it. To import a raw key into a new wallet, use `bag wallet new --private-key --generate-password` (hidden key prompt) or `--private-key - --generate-password` (stdin). For a user-selected password, the user privately reads/exports `WALLET_PASSWORD` in their own terminal and replaces `--generate-password` with `--save-password`, which persists it privately and refuses existing wallets or a different saved password. Never pass a key or password inline.

5. **Fund the wallet - OPTIONAL; do NOT block on it.** The default `auto/free` LLM model runs at $0 and AgentCore deploy consumes no wallet balance, so a brand-new seller can scaffold, run `bag dev`, and deploy with an empty wallet. `bag doctor` and `bag deploy` only **WARN** (never block) on zero balance. Funding is needed later only for: a paid LLM model, on-chain settle, paying positive-price ERC-8183 job buys, or buying/smoking a PAID B402 request. A FREE ERC-8183 buy needs no U escrow or ERC-20 approval, but still needs the ERC-8183 state-changing calls and their gas/paymaster path. A FREE B402/x402 request needs neither token funding nor a facilitator call. When funding is needed, the wallet uses **TWO distinct U balances on TWO chains** (same wallet address, same private key, different chains):
   - **tBNB (gas)** on BSC testnet: message the official Telegram bot https://t.me/bnbchain_official_bot with `I would like to get tBNB to my wallet <address>` (up to 0.3 tBNB/day; replies with the tx hash). More options: https://docs.bnbchain.org/bnb-smart-chain/developers/faucet/
   - **BSC mainnet U** (`0xcE24439F2D9C6a2289F741120FE202248B666666`) - for Pieverse LLM topup. Minimum **0.2 U** recommended (0.1 for activate + slack). Pieverse runs **only on mainnet chainId=56**; testnet U cannot pay for LLM credits. Acquire via PancakeSwap. Wallet-funded renewal stays off unless the operator explicitly enables it with `bag budget enable`; otherwise refill Account Balance with `bag llm topup` as needed.
   - **BSC testnet U** (`0xc70B8741B8B07A6d61E54fd4B20f22Fa648E5565`) - for ERC-8183 job payments if `[network].default = bsc-testnet`. Message the official Telegram bot https://t.me/bnbchain_official_bot with `I would like to get U to my wallet <address>`. More options: https://united-coin-u.github.io/u-faucet/ (see also `docs/guides/U-token-testnet.md`).

   Both U balances live in the **same agent wallet** - one address, same private key - just on different chains. Verify both with `bag wallet balance --all`.

6. **Activate Pieverse LLM** (only if `llm=pieverse-llm`, default): `bag llm activate` - **zero-deposit by default** (`--initial-usd` defaults to 0). SIWE-logs in with the agent wallet (an off-chain EIP-191 signature - no gas, no U), creates an `sk-pv-...` key with a $0 allocation, and writes `PIEVERSE_LLM_API_KEY` to `.env.local` + `key_hash` to studio.toml. The default model `auto/free` runs at $0/token, so **no funding is required to start**. Only when you switch to a paid model do you fund the wallet and run `bag llm topup --amount N` (then `[llm.auto_renew]` auto-**allocates** from your Pieverse Account Balance to the key below the floor; wallet U is spent only when `[budget]` has been explicitly enabled). For non-Pieverse providers, manually set the API key env var instead.

   **Step 6b - Set self-hosted deliverable-storage credentials** (skip this for managed-platform deploys; the platform injects its own scoped upload token). With `--storage-provider ipfs` the self-hosted Agent pins each deliverable to IPFS at delivery and publishes `ipfs://CID` on-chain. Works with any IPFS pinning service or a self-hosted node:

   > Pick a pinning service and create a write key/JWT in its console (or run your own IPFS node - its `/api/v0/add` endpoint usually needs no key), then:
   >
   > ```bash
   > bag env set STORAGE_API_URL <your-service-upload-endpoint>
   > bag env set STORAGE_API_KEY <your-write-key>
   > ```
   >
   > Written to `.studio/.env.local`. They are required before deploy and the first real delivery. You can also pass `--ipfs-key <key>` to `bag init` upfront.

   For self-hosted `s3`, fill `bucket`/`region` and set `DELIVERABLE_S3_ACCESS_KEY_ID` plus `DELIVERABLE_S3_SECRET_ACCESS_KEY`. For self-hosted `azure-blob`, fill `account_url`/`container` and set a write SAS or the complete namespaced service-principal variables scaffolded in `.studio/.env.local`. A `public_base_url` may point at the user's CloudFront/Azure Front Door/CDN; otherwise the bucket/container must itself allow anonymous reads. Never use a presigned/SAS URL for the public base. Canonical JSON deliverables are capped at 10 MiB before upload and are re-read/hash-verified through the public URL before on-chain submit. `credential_mode = "ambient"` is a runtime option, not an IAM/RBAC provisioner: the operator must grant the runtime identity write access. Managed-platform deploys ignore this BYOS writer configuration and use the API-injected storage endpoint/token. For pure offline dev, keep `local`.

7. **Recipe code is already emitted by `bag init`** - the `app/agent/` sub-project plus its `studio.toml` is written by step 1, so **skip manual recipe emission**. To re-emit or inspect a recipe later, `bag recipe code agent` / `bag recipe code runtimes/agentcore` (emits under `{{PKG}}` = the agent's `src/` dir; pass `--pkg <name>` to override). The real work is editing the Agent's `runWork` hook in `app/agent/src/sellerCore.ts` (A2A) / `app/agent/src/mcpMain.ts` (MCP) (see `bnbagent-studio-selling-via-8183.md` in this same directory).
8. **Verify**: `bag doctor` - confirms the scaffold + Pieverse key activation (if applicable) + config. Zero BNB / U are **WARN only** (not failures) - funding is optional (see step 5), so do NOT refuse to continue on a balance warning. Only refuse on real FAILs (missing keystore, unparseable config, etc.).

**Do not** register ERC-8004 identity at this stage - it needs the deployed agent's public AgentCore endpoint, so it happens **last** at deploy time (`bag deploy verify`). Telling the user upfront:

> ERC-8004 on-chain identity registers at deploy time with your agent's public AgentCore endpoint (A2A card URL or MCP `/mcp` URL + access metadata). Skipped now so you don't burn gas before you know whether you'll ship this seller.

ERC-8183 service publishing is also a deploy-time concern - defer it.

Present the todo list to the user; ask "is this OK or do you want me to add/remove steps?" **only if** the wallet kind is unusual (e.g. `evm-local` with a key import, or `twak`). For the `evm-local` default, skip the confirmation and execute.

## Stage 3 - Execute step by step

For each todo item:

- Mark `in_progress` before running
- Run the command via shell (or Edit/Write for code changes)
- Show the user the output
- Mark `completed` when done

**Stop and ask the user** at:

- Step 3 (wallet secrets): do not stop for a brand-new evm-local wallet; `bag wallet new --generate-password` uses the OS CSPRNG and writes the private local env file itself. Stop only when the selected flow requires an existing secret: an imported v3 keystore needs its original `WALLET_PASSWORD`, an existing TWAK wallet needs its original `TWAK_WALLET_PASSWORD`, and TWAK credential initialization needs the NaaS values. The USER enters those **themselves, in their own terminal**; never request or route them through chat, argv, or logs. Wait only for completion, not for the value.
- Step 5 (funding): OPTIONAL - only stop here if the user explicitly wants a paid LLM model, on-chain settle, or to pay ERC-8183 buys now. Otherwise skip; the `auto/free` default needs no funds.
- Step 6 (Pieverse activation): zero-deposit, so it just works - no funding precheck needed. If `bag llm activate` fails on connectivity, retry once.
- Step 6b (deliverable storage): skip for `local` and for every managed-platform deploy. Self-hosted IPFS needs its write endpoint, S3 needs namespaced keys unless ambient identity is deliberately configured, and Azure Blob needs a write SAS/service principal unless ambient identity is deliberately configured. Do not ask for secret values in chat; have the user set them with `bag env set`. Self-hosted deploy readiness blocks incomplete storage configuration.
- Business-logic step: ask the user what the Agent should produce when it delivers a job - the `runWork` hook in `app/agent/src/sellerCore.ts` (A2A) / `app/agent/src/mcpMain.ts` (MCP) is the developer hook. Leave the generic LLM passthrough stub if they don't know yet

**Never** ask the user to `echo "KEY=VALUE" >> .env.local`. Always call `bag env set KEY VALUE` - it replaces the existing line if present, otherwise appends, so it's safe to run repeatedly.

## Stage 4 - Summary

After step 8 passes (doctor clean - Pieverse key activated; balances may be 0 and that's fine), print:

```
✅ <name> ready for local development (single seller agent).

Wallet:    <0x...>
Network:   bsc-testnet
BNB bal:   <X> tBNB
U bal:     <Y> U

Local dev (from workspace root <name>/):
  bag dev                            # A2A: local :9000; MCP: local :8000/mcp (same for any destination)
                                     # (no Cognito env locally)
                                     # For A2A, test with curl/A2A DataPart, NOT the
                                     # AgentCore inspector chat box (it can't send a
                                     # seller's skills). For MCP, use an MCP client.

When ready to deploy:
  bag deploy prepare                 # readiness sweep
  bag deploy --provider aws          # ship the Agent to AgentCore (selected faces);
                                     # provisions the Cognito pool + buyer M2M client and
                                     # prints the token URL / client id / scope;
                                     # keystore injected via Secrets Manager (never in the CodeZip)
  bag deploy verify --provider aws --endpoint <url> # delegated status + reconcile ERC-8004

Edit (from workspace root):
  app/agent/src/sellerCore.ts or mcpMain.ts # the VALUE - implement the runWork hook (your work product)
  app/agent/src/signing.ts           # fixed price conversion + signing code; NOT LLM tools
  app/agent/src/tools.ts             # read-only chain tools the LLM may call
  app/agent/src/agentCard.ts         # A2A only: advertised card (2 skills + OAuth2 scheme)
  app/agent/studio.toml              # Agent config (LLM, canonical [payments.seller], rails, [budget])
```

## Gotchas

- Token decimals come from the exact-network catalog and differ by asset/network. The `@bnbagent/studio-runtime/networks` `toRaw`/`fromRaw` helpers handle conversion; never infer one token's decimals from another.
- **`buy_workflow`'s `deadline_minutes`** is the seller's _submission_ window. The on-chain job lifetime is automatically `deadline_minutes + 24h dispute_window`.
- **`bag init` runs wallet onboarding only on a human TTY** (evm-local: generates and privately persists the password, then creates the keystore; twak: delegates credential init/verification, password generation, create/adopt, and address anchoring to `bag wallet twak-init`). When an agent runs `bag init` non-interactively, use `--no-onboard` for deterministic scaffolding, then follow Step 4 without collecting secrets in chat.
- **The agent is the sole key-holder; the key material never enters the deploy package.** For **evm-local** the encrypted keystore lives at the **workspace root** `.studio/wallets/` (outside the `app/agent/` codeLocation, so no packaging path can bundle it); for **twak** the mnemonic lives at `~/.twak` (or `.studio/twak/`), never in the repo. Either way it is injected at deploy via AWS Secrets Manager (default `--secrets-mode secretsmanager`) - `WALLET_KEYSTORE_JSON` / `WALLET_PASSWORD` for evm-local, `TWAK_WALLET_JSON` / `TWAK_CREDENTIALS_JSON` / `TWAK_WALLET_PASSWORD` for twak - reconstructed at cold start, never in the package; the testnet-only `--secrets-mode envvars` fallback is refused on mainnet.
- **AgentCore seller endpoints are never anonymous.** `bag deploy --provider aws` provisions the Cognito OAuth2 pool + buyer M2M client itself and prints the token URL / client id / scope to hand to buyers (`bag deploy provision-cognito` is deprecated - a deploy uses its own pool regardless). Locally, `bag dev` runs without Cognito env, so the card omits the scheme and is reachable without a token.
- **ERC-8183 does NOT require ERC-8004** at the protocol level (commerce contract doesn't check the identity registry). Local two-agent dev can run end-to-end without ever touching 8004. Use 8004 only when you actually want discoverable identity.
- **Seller code that needs `ERC8183JobOps` directly** should import the public `import { ERC8183JobOps } from "@bnbagent/sdk/erc8183"` - the headless funded-job lifecycle ops. `getPendingJobs()` returns FUNDED jobs assigned to this provider (the basis for the executor's best-effort sweep).

## Reference

- the `bnbagent-studio-using-twak-wallet.md` reference (in this same references/ directory) (the fully-supported `twak` wallet kind, opt in with `--wallet-kind twak`: setup / funding / SIWE / container deploy)
- `docs/design/single-seller-agent.md` (the v1 deploy model)
- `docs/design/erc8183-buyer-push.md` (negotiate → fund → notify_funded, the sweep)
- `docs/design/decisions.md` (single seller runtime + protocol faces; CLI vs skill responsibilities)
- `docs/design/architecture.md` §2.5 / §2.7 (the single seller runtime + workspace layout)
- `docs/guides/U-token-testnet.md` (how to obtain testnet U tokens)
