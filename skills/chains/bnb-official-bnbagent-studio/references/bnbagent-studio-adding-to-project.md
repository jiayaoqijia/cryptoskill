---
name: bnbagent-studio-adding-to-project
description: When the user wants to add bnbagent-studio's single seller runtime (one valuable Agent on AWS Bedrock AgentCore that serves A2A + X402 with ERC-8183 + B402 by default, or another selected face/rail combination, holds the key, and signs in-process) to an existing TypeScript agent project.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-adding-to-project

Procedure for adding `bnbagent-studio`'s **single selected-protocol seller** to an **existing** TypeScript/Node repo. Audience: Claude Code (or another agent) running with shell + edit access in the user's repo.

## The single seller runtime model (v1 workspace)

studio turns the user's existing valuable agent into a paid blockchain seller as a **thin workspace root with one sub-project** under it:

- **Agent (`app/agent/` sub-project, → AWS Bedrock AgentCore).** The user's agent value (LLM / memory / tools / KB) AND the **sole key-holder/signer**. AgentCore runs the container with the selected protocol (A2A: `0.0.0.0:9000`; MCP: `0.0.0.0:8000/mcp`), so the Agent **serves directly** - it is its own public HTTPS surface, gated by a mandatory Cognito OAuth2 authorizer. Owns its own `app/agent/package.json`, `app/agent/studio.toml`, and `.studio/.env.local`; the keystore lives at the WORKSPACE root `.studio/wallets/` (outside the AgentCore codeLocation, so no deploy packaging path can bundle it - at deploy it is injected via AWS Secrets Manager as `WALLET_KEYSTORE_JSON`). The outward surface is A2A's `SellerAgentExecutor` (`negotiate` / `notify_funded` skills) or the MCP server's tools with the same bounded operations; ALL signing is fixed `app/agent/src/signing.ts` code, never an LLM tool.

There is **no** second service: the Agent signs in-process and answers buyers directly over its selected protocol. (The earlier two-layer split - an invoke-only Agent plus a public keyless EC2 service relaying to it - was removed once AgentCore could serve the protocol surface on a public endpoint; see `docs/design/single-seller-agent.md` for the A2A decision history.)

"Adding to an existing project" in v1 means **scaffolding a fresh workspace and migrating your value into it** - `bag init` always creates a _new_ workspace directory (there is no in-place adoption); you then move your existing agent's LLM / tools / memory code into the generated `app/agent/` sub-project.

v1 is **seller-only**; chat / buyer roles are deferred to v2.

## Preconditions

- The repo is a TypeScript/Node project (has a `package.json`).
- The user has Node.js ≥22 and can install the CLI - `npm install -g @bnbagent/studio-cli` (auto-pulls the `@bnbagent/studio-runtime` lib); for local dev use a monorepo clone (`pnpm install` at the workspace root).
- Network access to BSC testnet RPC (default: `https://data-seed-prebsc-1-s1.binance.org:8545`).

## Step 1 - Bootstrap studio config

Check for the v1 workspace layout - `app/agent/studio.toml` (not a root-level `studio.toml`):

```bash
ls app/agent/studio.toml 2>/dev/null || echo MISSING
```

If missing, scaffold a new workspace. `bag init <name>` **always creates a new directory `<name>/` under the current working directory** - it does not adopt the current repo in place. Pick a workspace name, then migrate your existing agent's value into the generated `app/agent/` sub-project (Step 4):

```bash
bag init myagent && cd myagent   # creates ./myagent/ with the single app/agent/ sub-project
```

**Scaffold note:** while the trial campaign runs, bare `bag init` defaults to `--destination platform` (the 48h managed-platform testnet trial - no AWS account needed). Pass `--destination self` to make AWS the scaffold intent. Both AgentCore variants include a Studio-rendered local deploy descriptor so a later explicit AWS deployment does not require re-scaffolding. Deploy provider selection remains explicit in Step 5.

Verify the workspace tree: `app/agent/studio.toml`, `.studio/.env.local`, `.studio/wallets/` at the root, and `.gitignore` at root + sub-project. A runtime=`agentcore` scaffolds (including platform-destined ones) also have `agentcore/agentcore.json` + `agentcore/aws-targets.json`. The managed BNB platform does not consume those local AWS files; they exist only to permit a later explicit `bag deploy --provider aws` choice.

## Step 2 - Detect framework (best-effort)

```bash
bag scan
```

**v1 note**: `scan` is a stub - it just reports detected files. Don't rely on its decisions; ask the user what their existing agent is built with (AI SDK / LangChain.js / a custom express service) before emitting recipes.

## Step 3 - Emit the agent

A seller is the single Agent serving the selected protocol. `bag init` already composes it from recipes - `agent` (the fixed-code `src/signing.ts`) and `runtimes/agentcore` (A2A: `src/unifiedMain.ts` (the express + A2A entrypoint, one code set for both deploy clouds) + `src/sellerCore.ts` (the protocol-neutral core; executor inherits it) + `src/executor.ts` + `src/agentCard.ts`; MCP: `src/mcpMain.ts`; shared `src/tools.ts` + `src/model.ts`; a `Dockerfile` is added only for a container deployment path such as TWAK). Use `bag recipe code` to inspect or re-emit a piece:

```bash
bag recipe code agent              > /dev/null   # inspect; bag init writes app/agent/src/signing.ts for you
bag recipe code runtimes/agentcore > /dev/null   # inspect; bag init writes the A2A serving files for you
```

In practice `bag init` already scaffolds `app/agent/`. Use `bag recipe code agent` / `bag recipe code runtimes/agentcore` to inspect or re-emit (emits under `{{PKG}}` = the agent's `src/` dir, or pass `--pkg <name>` explicitly).

Gotcha: the payment asset is a configured catalog token, not BNB: Mainnet supports **U/USD1/USDC/USDT** and Testnet supports **U/USDC/USDT**. Mainnet USD1 is EIP-3009-only; Testnet does not support USD1. The canonical seller price is in USD; each job amount is converted to and bound to exactly one selected token.

## Step 4 - Wire your existing agent's value into the Agent

The Agent sub-project (`app/agent/`) is where your existing valuable agent lives. Move your LLM construction / tools / memory / KB wiring into it, and implement the `runWork` developer hook (in `app/agent/src/sellerCore.ts` for A2A, `app/agent/src/mcpMain.ts` for MCP; called from `notify_funded`'s delivery) to produce the deliverable. Read-only chain tools go in `app/agent/src/tools.ts` (see `bnbagent-studio-wiring-llm-tools`). ALL signing stays in `app/agent/src/signing.ts` - never expose a signing call as an LLM tool.

Tune the canonical price in `app/agent/studio.toml` under `[payments.seller]`: the `negotiate` path is **rule-based, no LLM** - fixed code resolves the requested asset on the exact network, converts the shared `price_usd` using catalog decimals, then `signing.ts` EIP-191-signs the offer. The buyer anchors the signed envelope on-chain via `createJob` + `fund`.

Legacy U-only projects without `[payments.seller]` retain `[payments.erc8183]` `price`/`min_price`/`max_price`/`currency` and their clamp behavior. Those bounds do not apply to canonical `price_usd`. Canonical `[payments.seller]` plus any legacy price or asset field is ambiguous and fails readiness; run `bag config migrate-seller` or remove the legacy fields instead of depending on precedence.

Use `bag config set payments.seller.price_usd 0` only for an explicit FREE product decision; it writes `[payments.seller]` with `price_usd = "0"`. The canonical seller policy stores one USD price and an ordered, non-empty canonical asset set; all active assets use that same value. Studio reports FREE in `bag doctor`; the canonical stack supports zero funding. If a custom deployment is selected, set all three `ERC8183_*_ADDRESS` overrides from that same stack. The buyer still runs `setBudget(0)` and `fund(0)`, but no ERC-20 approval or token escrow occurs. Require `bag doctor` and `bag deploy prepare` to pass.

For an X402 or MPP face, use the same `[payments.seller].price_usd`. Set it to `0` only when the existing agent is intentionally becoming an unrestricted anonymous FREE API. This path bypasses B402 verify/settle, payment, and settlement audit; it needs no merchant credentials and Studio will not synchronize any configured B402 secrets. Positive prices retain the paid B402 onboarding and settle-before-work flow. Verify the choice with status, `bag doctor`, and `bag deploy prepare`.

## Step 4c - LLM credit continuity (automatic, NOT an LLM tool)

For Pieverse projects, the Agent's `buildModel()` factory in the emitted `app/agent/src/model.ts` returns an AI SDK model wrapped with credit-ensure middleware. Its **automatic, budget-gated auto-renew hook** (the stack-neutral logic lives in `@bnbagent/studio-runtime/pieverse` `PieverseCreditEnsurer`; the AI-SDK shell is the emitted file) tops up the active Pieverse key from the wallet (when `[budget].enabled = true`) before an LLM call whose cached balance is below `[llm.auto_renew].min_balance_usd`. The Agent keeps delivering jobs even if it runs low mid-shift - the resilience is transparent.

Crucially this is **not** an LLM tool. It rides on the hardened x402 buyer kernel (`@bnbagent/studio-runtime/x402`, the payment signer) - but the Agent (the sole key-holder) drives it transparently inside the model wrapper; the LLM never decides to spend. The LLM-credit self-top-up you get for free is the managed-model auto-renew hook described above.

If the budget gate is off / exhausted, the hook raises `PieverseAccountBalanceExhaustedError` - let it surface so the buyer can dispute; refill with `bag llm topup` or enable the budget with `bag budget enable`.

## Step 5 - Deploy the agent

`bag deploy` always asks the operator to choose BNB or AWS; it never silently reuses `[deploy].destination` or the last provider.

**Platform scaffold** (the bare-init default while the campaign runs) - one command; first run does a GitHub device-flow login, the wallet key goes to the operator's Secrets Manager (testnet-forced, use a throwaway wallet):

```bash
bag platform login                 # prints GitHub device URL + code; does not open a browser
bag deploy --provider bnb          # ship to the managed platform (48h testnet trial)
```

**Self-deploy scaffold** (`--destination self`) - the Agent serves the selected protocol directly behind a mandatory Cognito authorizer; register ERC-8004/8183 **last** with the deployed AgentCore endpoint:

```bash
bag deploy prepare                 # readiness sweep
bag deploy --provider aws          # ship the Agent to AgentCore
bag deploy verify --provider aws   # delegated status + reconcile ERC-8004 identity
```

Gotcha: `bag deploy --provider aws` provisions the Cognito user pool and the buyer M2M client itself and prints the token URL, client id, and scope - hand those to each buyer (Cognito has no public M2M self-registration; retrieve the client secret read-only from the AWS Console). Do not run `bag deploy provision-cognito`: it is deprecated and its CDK pool is never used by a deploy.

Gotcha: `dispute_window` is read from the on-chain policy contract (24h on testnet). Buyers can dispute within that window after submit - the Agent can't claim funds until the window closes.

## Step 6 - Verify

```bash
bag doctor    # run from workspace root; scans the agent sub-project
```

Should show green for: `app/agent/studio.toml` present, wallet decryptable (needs `WALLET_PASSWORD` set in `.studio/.env.local`), RPC reachable, 8004 identity registered (if applicable), LLM key present (if `[llm]` configured in `app/agent/studio.toml`).

If anything is red, fix and re-run `bag doctor` before deploying.

## Step 7 - Smoke test the Agent locally

`bag dev` from the workspace root launches the Agent with the selected protocol. Locally it runs without Cognito env, so the A2A card / MCP metadata is reachable without a token:

```bash
bag dev               # A2A on :9000, or MCP on :8000/mcp
```

For A2A projects, in another shell, fetch the card and send a `negotiate` message (`message/send` JSON-RPC with a single `DataPart`):

```bash
curl -s http://localhost:9000/.well-known/agent-card.json   # 2 skills: negotiate / notify_funded

curl -X POST http://localhost:9000/ \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"message/send","params":{"message":{"role":"user","messageId":"nego-1","parts":[{"kind":"data","data":{"skill":"negotiate","task_description":"summarize a webpage"}}]}}}'
```

The reply data part is the SDK `NegotiationResult` envelope, signed by the agent: the quoted `price`, `currency`, and the signature fields (`negotiation_hash`, `provider_sig`). The buyer anchors it on-chain via `createJob` + `fund`, then sends a `notify_funded` message; the agent acks `accepted` at once and delivers in the background, and the buyer reads the result from the chain (SUBMITTED → `deliverable_url`). For MCP projects, connect an MCP client to `http://localhost:8000/mcp`; `notify_funded` verifies, runs the work, and submits synchronously inside the tool call (see `bnbagent-studio-selling-via-8183.md` (same directory) and `docs/design/erc8183-buyer-push.md`).

## Reference

- `docs/design/single-seller-agent.md` (the A2A deploy model and history).
- `docs/design/erc8183-buyer-push.md` (how a buyer drives a sale: negotiate → fund → notify_funded).
- `docs/design/decisions.md` (single seller runtime + protocol-choice decision records).
- `docs/design/architecture.md` (recipes, selected-protocol runtime, project layout - §2.5 / §9.2).
- `bnbagent-studio-selling-via-8183.md` (same directory) - the runtime seller flow (negotiate, notify_funded, submit, and dispute defense); buyer settlement lives in the buying reference.
