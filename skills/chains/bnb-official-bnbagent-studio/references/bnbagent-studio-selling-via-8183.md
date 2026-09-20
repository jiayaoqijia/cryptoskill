---
name: bnbagent-studio-selling-via-8183
description: When the user is acting as an ERC-8183 seller on the single selected-protocol AgentCore runtime - implementing the value `notify_funded` produces, tuning the deterministic canonical USD quote price (exact asset conversion + sign - no LLM in the negotiate path), understanding A2A async delivery vs MCP synchronous delivery, handling submitted jobs, defending against buyer disputes, and ensuring LLM credit continuity during long jobs. Owns the seller-side decision tree for the entire job lifecycle.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-selling-via-8183

Procedure for the **single seller flow**: implement the value your Agent produces, deploy it to AgentCore (where the default scaffold serves A2A + X402, while ERC-8183 remains available through A2A or an explicitly selected MCP face), and handle the job lifecycle (Agent quotes → buyer funds → buyer calls `notify_funded` → Agent delivers → buyer reads the result from the chain → buyer settles or disputes).

Audience: Claude Code in a working repo with a funded gas wallet and an Agent that produces some valuable output (text, classification, image - whatever).

**Different from**:

- `bnbagent-studio-scaffolding-agent.md` (same directory) - creates the project (this playbook runs after)
- `bnbagent-studio-adding-to-project.md` (in this same references/ directory) - wires the seller runtime into an existing project (the static setup, not the runtime behavior)
- `bnbagent-studio-operating.md` (same directory) - generic ops (dev / doctor / balance); jumps here for seller-specific decisions

This skill owns: **implement the `notify_funded` value → deploy the agent → defend disputes**.

## The single seller runtime (one workspace sub-project)

A v1 seller ships as **one runtime**: a single valuable Agent on AWS Bedrock AgentCore that **serves its selected protocol directly** (A2A: `0.0.0.0:9000`; MCP: `0.0.0.0:8000/mcp`), holds the key, and signs in-process. It exposes two fixed-code commerce operations - `negotiate` and `notify_funded` - as A2A skills on `SellerAgentExecutor` or tools on the MCP server, behind a mandatory Cognito OAuth2 authorizer. There is no separate forwarding service.

| Sub-project | Role |
| --- | --- |
| `<workspace>/app/agent/` | The value (LLM/memory/tools/KB) AND the **sole signer**, deployed to AgentCore and serving the selected protocol. A2A uses `SellerAgentExecutor` in `<workspace>/app/agent/src/executor.ts`, which reads the inbound A2A message's data part and dispatches on its `"skill"` (`negotiate` / `notify_funded`); MCP uses `src/mcpMain.ts` tools with the same bounded operations. ALL signing is fixed `<workspace>/app/agent/src/signing.ts` code - never an LLM tool. Keystore lives at the WORKSPACE root `<workspace>/.studio/wallets/` (outside the AgentCore codeLocation, so no deploy packaging path can bundle it; the Agent is its sole reader via `[wallet].keystore_dir`). At deploy the keystore is injected via AWS Secrets Manager (`WALLET_KEYSTORE_JSON`) and reconstructed at cold start by the entrypoint's `loadRuntimeSecrets()`. Config in `<workspace>/app/agent/studio.toml`. |

> The earlier two-layer model (an invoke-only Agent plus a public keyless EC2 service relaying via `InvokeAgentRuntime`) is **removed**. Once AgentCore could serve the protocol surface on a public HTTPS endpoint, the agent became its own public surface and the relay disappeared. See `docs/design/single-seller-agent.md` for the A2A decision history.

## Preconditions

- `bag doctor` is clean (or only warns on optional checks) - run from workspace root
- Wallet has gas to submit deliverables. Sellers receive the job-bound active catalog token (Mainnet U/USD1/USDC/USDT; Testnet U/USDC/USDT) and do not fund buyer escrow. Testnet does not support USD1.
- The agent sub-project is emitted (`<workspace>/app/agent/src/unifiedMain.ts` for A2A or `src/mcpMain.ts` for MCP, plus `src/signing.ts`). If not, run `bag init` or read the `bnbagent-studio-adding-to-project.md` reference first.
- For LLM-using sellers: `[llm].provider` configured in `app/agent/studio.toml` + (if Pieverse) `bag llm activate` has been run

## Stage 1 - Implement the `notify_funded` value (the `runWork` hook)

The valuable work lives in the `notify_funded` path. When a buyer calls `notify_funded` for a `job_id`, the runtime first synchronously re-verifies the job is genuinely FUNDED + ours on-chain (`signing.ts` `verifySignedJob`). In A2A mode, the executor **acks `accepted`** at once and then runs the LLM work + `signing.ts` `submitResult` (which SIGNS + broadcasts the deliverable) in a **background task**. In MCP mode, the tool call verifies, runs the LLM work, and submits synchronously, reporting progress while it runs. The block to specialise is the **developer hook** - the work function that produces the deliverable text:

```ts
async function runWork(
  prompt: string,
  opts: { sessionId: string },
): Promise<string> {
  // DEVELOPER HOOK - replace the generic LLM passthrough with your real work:
  // call domain tools, hit your APIs, run a pipeline, use the KB.
  // Return the deliverable TEXT - the executor handles submit + on-chain signing.
  const { text } = await generateText({ model, tools: LLM_READ_TOOLS, prompt });
  return text;
}
```

**Hard rules**:

- The `notify_funded` work must finish before the on-chain `submitDeadline` - keep it bounded (A2A also has to land within the session max-lifetime, ≤8h).
- Don't raise unhandled exceptions through `submitResult`. A permanently-bad job is rejected synchronously. In A2A, once accepted, a background delivery FAILURE leaves the job FUNDED (never reaching SUBMITTED) and is surfaced in CloudWatch - not the A2A reply. Let work errors surface so the job simply doesn't get a deliverable and the buyer can dispute cleanly; don't fake a deliverable.
- All chain WRITES go through `app/agent/src/signing.ts` (fixed code). In the `notify_funded` work the LLM only PRODUCES work text - it never signs, and it never sets the price (the quote price is rule-based; see Stage 2).

## Stage 2 - Canonical pricing (shared USD price, exact conversion + sign - no LLM)

A `negotiate` skill message hits the executor, which dispatches to the quote path. The quote path is **deterministic policy - no LLM, no tools**:

1. Fixed code reads the shared USD **list price** and ordered canonical asset set from `[payments.seller]`. The LLM is never invoked in the negotiate path and never proposes or touches the price.
2. Fixed code resolves the requested asset on the exact network and converts the shared USD value to that token's atomic units using its catalog decimals. Canonical `price_usd` is not passed through the legacy U-only `min_price`/`max_price` clamp.
3. `signing.ts` `signQuote` does the **EIP-191 sign** with a short TTL (returns the SDK `NegotiationResult` envelope verbatim - price, currency, negotiation_hash, provider_sig), which the executor returns directly to the buyer over A2A. `chain_id` + `verifying_contract`, the canonical token address, and the amount are bound into the signature, so the quote cannot be replayed on another chain, contract, or asset. **Money is never in the LLM.**

Configure the canonical seller price in `<workspace>/app/agent/studio.toml`:

```toml
# app/agent/studio.toml
[payments.seller]
price_usd = "0.10"
assets = ["TEST_U", "TEST_USDC", "TEST_USDT"] # network-canonical AssetIds

[payments.erc8183]
quote_ttl_seconds = 300
default_estimated_completion_seconds = 600
```

Every configured asset uses the same USD value and its own decimals. Any non-empty subset is
valid; Mainnet may use USD1-only or any USD1/USDC/USDT combination, while the shown Testnet
example correctly excludes unsupported USD1 on Testnet. The quote binds a canonical token address and
each job binds exactly one immutable token. Mainnet USD1 is 18-decimal EIP-3009 with domain
`World Liberty Financial USD / 1`, has no Permit2 route, and still requires Commerce/live
verification before release. Canonical FREE is explicit:

```toml
[payments.seller]
price_usd = "0"
```

Legacy U-only projects without `[payments.seller]` retain `[payments.erc8183]`
`price`/`min_price`/`max_price`/`currency` and their existing clamp semantics. Those legacy
bounds never alter canonical `price_usd`. Defining `[payments.seller]` together with any legacy
price or asset field is an ambiguity error; use `bag config migrate-seller` rather than relying
on precedence.

Prefer the CLI so the zero-price choice is visible and remains a decimal string:

```bash
bag config set payments.seller.price_usd 0
bag doctor
bag deploy prepare
```

Doctor/prepare announce `zero token escrow` for the canonical stack. If the operator intentionally selects a custom deployment, take all three `ERC8183_*_ADDRESS` values from that same compatible stack; partial or invalid overrides are rejected.

## Stage 3 - LLM credit continuity (Pieverse projects only)

If `[llm].provider = "pieverse-llm"`, the Agent's emitted `app/agent/src/model.ts` `buildModel()` factory returns an AI SDK model wrapped with credit-ensure middleware (the stack-neutral credit logic lives in `@bnbagent/studio-runtime/pieverse` `PieverseCreditEnsurer`; the AI-SDK shell is the emitted file). Its **automatic, budget-gated auto-renew hook** tops up the active Pieverse key before an LLM call when the cached balance is below the floor. It fires **only in `notify_funded` work** (the `negotiate` path runs no LLM, so it never triggers there). This is the **only automatic signing path outside `signing.ts`**; it rides on the hardened x402 buyer kernel (`@bnbagent/studio-runtime/x402`, the payment signer) but is **NOT an LLM tool** - the Agent (the sole key-holder) does it transparently inside the model wrapper.

| Layer | Mechanism | When it fires |
| --- | --- | --- |
| **Per-call auto-renew hook** | The emitted managed-model wrapper checks key balance before each LLM call | Cache miss (60s default) or balance < `min_balance_usd` |

If `[budget].enabled = true` (opt-in), the hook auto-tops-up from the wallet within the 6-gate budget; otherwise it raises `PieverseAccountBalanceExhaustedError` and the executor's `notify_funded` work should:

1. Let the error surface in the background task so the job stays FUNDED (never reaches SUBMITTED) and the buyer can dispute (don't silently fake a deliverable). The job was already acked `accepted`, so the failure is visible on-chain + in CloudWatch, not in the A2A reply.
2. **Don't** retry - the buyer's deadline keeps ticking
3. The owner sees the error in CloudWatch logs + should run `bag llm topup` to refill (or `bag budget enable`)

Full Pieverse credit decisions live in `funding-pieverse-llm` (project-scope skill in Pieverse projects).

## Stage 4 - Deploy + register (announce to buyers)

ERC-8183 / ERC-8004 registration is a **deploy-time** concern: the public AgentCore endpoint must exist before you register, so register **last**. The agent endpoint has no anonymous mode; `bag deploy` provisions the Cognito OAuth2 authorizer as part of the deploy.

```bash
bag deploy prepare                  # readiness sweep
bag deploy --provider aws           # ship the agent to AgentCore (selected protocol)
bag deploy verify --provider aws    # delegated status + reconcile ERC-8004 identity
```

ERC-8004 identity is registered with the **AgentCore endpoint**: A2A uses `AgentEndpoint.a2a(baseUrl, "0.3.0")` (normalizing to `/.well-known/agent-card.json`), while MCP records the `/mcp` endpoint plus access metadata. Buyers reach the agent directly. `bag deploy verify --provider aws` asks bnbagent-deploy for live status first, then performs the reconcile.

**Hard rules**:

- The endpoint must be **reachable** when registered. For A2A, smoke test the normalized card URL directly, for example `curl <agentcore-invocations-url>/.well-known/agent-card.json` (or `curl <already-registered-card-url>` if the endpoint already includes `/.well-known/agent-card.json`). For MCP, connect an MCP client to the deployed `/mcp` URL. Chain doesn't verify reachability, but buyers will see failures.
- `bag deploy --provider aws` provisions the Cognito user pool + buyer M2M client and prints the token URL, client id, and scope. Hand those to each buyer (the client secret is retrieved read-only from the AWS Console - studio never stores it). `bag deploy provision-cognito` is deprecated; its CDK pool is never used by a deploy.
- Canonical `[payments.seller].price_usd` lives with the Agent; fixed code converts it for the selected asset and signs the quote. Only a legacy U-only config without `[payments.seller]` uses `min_price`/`max_price` clamp semantics.

## Stage 5 - How a SUBMITTED job happens

There is **no background poll loop** in v1. Delivery is triggered by `notify_funded`; the execution model depends on the selected protocol:

1. **A2A buyer push (the prompt path):** buyer negotiates over A2A (`negotiate` skill) → buyer anchors the signed quote on-chain (`createJob` → `register` → `setBudget` → `fund`, provider = the agent address) → buyer pushes a `notify_funded` A2A message for the `job_id` → the executor synchronously re-verifies (`verifySignedJob`) and **acks `accepted`** at once, then in a **background task** does the LLM work and SIGNS + submits the deliverable on-chain → job → SUBMITTED. The buyer **polls the chain** for the result (it does not wait on the ack), then approves or disputes within `dispute_window` (24h on testnet). While any background delivery is in flight the runtime reports `/ping` `HEALTHY_BUSY` (AgentCore's long-running async pattern), so the scale-to-zero runtime stays warm until the work lands - bounded by the session max-lifetime (≤8h).
2. **A2A in-process sweep (the fallback):** on every accepted `notify_funded`, the executor opportunistically sweeps (in the background) `ERC8183JobOps.getPendingJobs()` for other FUNDED jobs assigned to this provider and delivers them too. This catches jobs whose buyer funded on-chain but never pushed `notify_funded`. The sweep is **deduped** (a job already being delivered - by the notification or a concurrent sweep - is skipped via an in-flight set, so notify + sweep never double-deliver the same job), **idempotent** (`verifySignedJob` returns non-OK for an already-SUBMITTED job, so there is no state file), and **best-effort** (one bad job never aborts the sweep, and a sweep failure never affects the ack).
3. **MCP synchronous delivery:** buyer negotiates through the `negotiate` MCP tool, funds on-chain, then calls `notify_funded`; the tool verifies, runs the work, and signs + submits before returning, with progress heartbeats. There is no background ack/sweep path in MCP.

Because the sweep runs only when _someone_ invokes `notify_funded` (and only while the runtime is warm), a totally idle, scaled-to-zero agent will not deliver during the cold window until the next notify. A periodic Lambda poller is the v2 robustness path that closes it. The full line protocol is in `docs/design/erc8183-buyer-push.md`.

Manual override (rare - only the agent holds the key):

```bash
bag erc8183 submit <job_id> "<deliverable text>" [--metadata-json '{...}']
```

Use only if the Agent produced a deliverable out-of-band and you need to attach it manually.

## Stage 6 - Defending against disputes

Buyer can `settle --action dispute` within `dispute_window`. Seller responses:

| Symptom | Diagnosis | Action |
| --- | --- | --- |
| Buyer disputed within 24h | Their right; goes to quorum vote | Provide evidence via the off-chain governance flow; don't argue on-chain |
| `0x17be5b7b` revert when buyer tried to `approve` | Buyer tried to approve before 24h passed | This is buyer's mistake, not yours; they'll need to wait or use `dispute` |
| `Submission deadline has passed` when you tried to submit | Buyer set too-short `expiredAt` on the job | You can't submit late; politely tell buyer to re-buy with longer deadline |
| Job stuck `FUNDED` for >24h | Nobody pushed `notify_funded` (and the agent stayed idle, so the sweep never ran) or the background `runWork` crashed (the job was acked `accepted` but never reached SUBMITTED) | Inspect CloudWatch logs; push a `notify_funded` to wake the agent, or submit work manually if a deliverable exists but submit failed |

**Hard rules**:

- Never tamper with quorum vote signals (no fake validators / no spam-disputes).
- If you produced a defective deliverable, **don't dispute** - accept the buyer's reject; chain reputation is real.
- Keep the agent's logs (it prints redacted audit events to stdout → CloudWatch).

## Stage 7 - Buyer settlement and seller payout

`settle` is the **buyer's** manual step; a quorum voter may also reject or resolve a dispute. There is no in-runtime auto-settle in the current single-runtime seller. After the dispute window elapses, the buyer can approve:

```bash
bag erc8183 settle <job_id>    # buyer wallet; default --action approve
bag erc8183 status <job_id>    # confirm COMPLETED
# Funds auto-transfer on COMPLETED in the current contract; no manual withdraw needed.
```

Older contracts may have required a manual `withdraw` - confirm against the deployed commerce contract's behavior.

## How a buyer reads the deliverable

The agent serves **no** job-query endpoint. The buyer reads the stable `deliverable_url` from the on-chain submission, then fetches the content-addressed object from IPFS, self-hosted S3/Blob, or the managed API proxy. This is by design - the chain is the shared source of truth, and the agent stays a thin A2A surface.

## Common errors + remediation

| Error | Cause | Fix |
| --- | --- | --- |
| A2A job acked `accepted` but never reaches SUBMITTED | background `runWork` / `submitResult` raised (the failure is NOT in the A2A reply - the ack already went out) | Inspect CloudWatch logs; wrap LLM/domain calls; let the error surface so the buyer can dispute, don't fake a deliverable |
| `notify_funded` reply `{ "status": "rejected", "reason": ... }` | synchronous verify failed (not our signature, tampered terms, underfunded, expired) or malformed `job_id` | Confirm the buyer funded the exact signed quote against this provider; re-quote if terms changed |
| `submit_work reverts gas estimation` | Job already SUBMITTED (idempotency violation) | Check `bag erc8183 status <id>` before retry - the sweep already handles this idempotently |
| `PieverseAccountBalanceExhaustedError` mid-job | Agent's LLM credit ran out | Let it surface; run `bag llm topup`; consider `bag budget enable` |
| Agent unreachable (buyer reports) | AgentCore runtime is down, DNS wrong, or the OAuth2 bearer is missing/expired | `bag deploy status` / `bag deploy logs --provider aws` to inspect; redeploy via `bag deploy --provider aws` |

## Hard rules (security boundary)

- Don't store buyer-supplied data outside the request lifecycle (privacy + storage cost).
- The Agent signs only its own quote and submit actions; the buyer or quorum signs settlement actions.
- The key lives ONLY in the agent at the workspace root `.studio/wallets/` (outside every codeLocation, so no packaging path can bundle it) and is injected into the agent via AWS Secrets Manager at deploy - never inlined into the code artifact (mainnet refuses the envvars fallback). Never log API keys / PII into stdout (the agent's audit events are redacted before they hit CloudWatch).
- Inbound auth is mandatory Cognito OAuth2 - buyers send plain HTTPS + a Bearer (no AWS SigV4). An unauthorized request is rejected 401; there is no anonymous mode.
- LLM model name selection (paid vs free) is a per-project decision - load `funding-pieverse-llm` if user is unsure which model to use for paid services.

## Reference

- `docs/design/single-seller-agent.md` (the A2A deploy model and history)
- `docs/design/erc8183-buyer-push.md` (the negotiate → fund → notify_funded line protocol)
- `docs/design/architecture.md` §2.5 (the single seller runtime - as-built)
- the `bnbagent-studio-wiring-llm-tools.md` reference (in this same references/ directory) - wiring read-only chain tools into the Agent's LLM
