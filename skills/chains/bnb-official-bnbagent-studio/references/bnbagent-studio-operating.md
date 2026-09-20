---
name: bnbagent-studio-operating
description: When the user wants to run, debug, diagnose, or operate a bnbagent-studio agent project. Covers dev server, doctor checks, balance/RPC queries, job status reads, and incident triage - including the delegated deploy lifecycle (`bag deploy status` / `logs` / `verify` / `destroy`), twak-wallet issues, and `PolicyViolation` / `X402PolicyError` signing-policy errors (deep-dive playbooks for those ship as references of the `bnbagent-studio` router skill; read them on demand).
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-operating

Procedure for **day-to-day operation** of an existing bnbagent-studio project. Audience: Claude Code in a current TypeScript workspace (thin root with the `agentcore/` config dir + the workspace-root `.studio/wallets/` + funded wallet, plus the single sub-project `app/agent/` holding `studio.toml` + `src/unifiedMain.ts` / `src/sellerCore.ts` / `src/executor.ts` / `src/agentCard.ts` / `src/signing.ts`). Most commands run from the workspace root; the current project-root fallback locates the `app/agent/` sub-project automatically for wallet/LLM/budget ops.

**Different from**:

- `bnbagent-studio-scaffolding-agent.md` (in this same references/ directory) - creates a brand new project
- `bnbagent-studio-selling-via-8183.md` (in this same references/ directory) - seller flow (`runWork` value, rule-based quote pricing, dispute defense)
- `funding-pieverse-llm` (project-scope skill, Pieverse projects only) - Pieverse credit lifecycle / topup decisions

**Deep-dive references** - plain markdown files in this SAME references/ directory (Claude Code: `~/.claude/skills/bnbagent-studio/references/`; Cursor: `bnbagent-studio/references/` beside the `.mdc` rules). READ the file when the topic comes up - don't answer from memory:

- `bnbagent-studio-use-aws-agentcore.md` - the delegated AgentCore lifecycle (`bag deploy --provider aws` / `status` / `logs` / `verify` / `destroy`) + AWS prerequisites
- `bnbagent-studio-use-bnb-trial.md` - GitHub device login, 48h eligibility, staging verification, and the delegated BNB trial lifecycle
- `bnbagent-studio-using-twak-wallet.md` - `[wallet].kind = "twak"` create / fund / SIWE-bind / container deploy / limitations
- `bnbagent-studio-extending-signing.md` - `PolicyViolation` / `X402PolicyError` diagnosis + extending the EIP-712 allowlist
- `bnbagent-studio-adding-to-project.md` - adding the seller runtime to an existing TypeScript project
- `bnbagent-studio-buying-via-8183.md` - buyer flow (find provider → buy → fetch → settle)
- `bnbagent-studio-selling-via-b402.md` - inbound x402 pricing mode, paid merchant setup, and B402 settlement operations

This playbook covers **generic ops**: dev / doctor / balances / RPC / incident triage. For seller job-lifecycle decisions (submit and dispute defense), read `bnbagent-studio-selling-via-8183.md` (same directory); for buyer settlement, read the buying reference.

## Quick triage decision tree

| User said... | Run first |
| --- | --- |
| "is it healthy?" / "doctor" | `bag doctor` (scans the `app/agent/` sub-project from the workspace root) |
| "run locally" / "start it" / "dev" | `bag dev` (serves the selected protocol: A2A on `:9000`, MCP on `:8000/mcp` - same for any destination) |
| "what's my balance?" / "how much U?" | `bag wallet balance` (native + U; `--network X` / `--all` available; `--address X` is not implemented) |
| "send X tBNB / U to another address" | `bag wallet transfer` is not implemented; move funds with an external wallet |
| "approve commerce contract to spend U" | The `bag erc20` group is not implemented (funding flows auto-approve U; there is no manual approve CLI) |
| "how much have I approved 0x... for?" | `bag erc20 allowance` is not implemented |
| "is my agent registered?" | `bag erc8004 show` (note: registration is normally automatic at `bag deploy verify` - manual `bag erc8004 register` only if you need an identity before deploy) |
| "what's the status of job X?" | `bag erc8183 status <id>` (read-only - neutral) |
| "is `/x402` paid or free?" | `bag x402 sell status` (`Rail state: paid` probes B402 unless `--no-probe`; `free` skips B402) |
| "settle job X" | `bag erc8183 settle <id> --action approve\|reject\|dispute` (default `approve`) is a buyer or quorum action; read `bnbagent-studio-buying-via-8183.md` for timing and authority |
| "submit work for job X" | **seller action** - read `bnbagent-studio-selling-via-8183.md` (same directory) for the submit/dispute flow |
| "tx not confirming" | Read BscScan link from prior tx output + check `eth_getTransactionCount` |
| "wallet balance is wrong" | Check both tBNB (gas) and U (token), and on testnet check the RAIL — `bag wallet balance` gives split assets one column per rail, and the b402 contract is not the ERC-8183 one; see balance section |
| "is it deployed?" / "deploy status" | `bag deploy status` lists every locally recorded BNB/AWS deployment and asks `bnbagent-deploy` for live state; add `--no-probe` for record-only output |
| "deploy logs" / "verify" / "tear it down" | With one recorded deployment, `bag deploy {logs,verify,destroy}` selects it automatically. With multiple, choose interactively or pass `--provider bnb\|aws` in automation. Provider lifecycle and status/log calls go through `bnbagent-deploy`; ERC-8004 reconciliation remains a Studio chain operation. `bag platform credit` shows the BNB trial countdown. |
| "report this error" / "send feedback" | Run `bag feedback`. It creates a redacted `.studio/logs/feedback-<UUID>.json` file and reads the form URL from the platform API (official production by default; shell `BNBAGENT_API_URL` then `BAG_PLATFORM_API_BASE` may override it, but project environment files cannot), falling back to https://forms.gle/h1TWLvTR1yPmPzu19 if configuration is unavailable. Give the user the generated file's actual absolute path and a clickable file link when supported, so they can review and upload it to the form's **Upload diagnostic report** field. If no file is generated, report the command's warning; never invent a file or report. AI/non-interactive sessions do not prompt or open a browser. Never upload the report or submit the form automatically. Do not substitute a project-provided form. The report excludes `.studio/audit-log.jsonl`, argv, output, paths, credentials, addresses, and transaction hashes. |

## Common ops procedures

### A. Run the agent locally (the default)

```bash
# Configure secrets (idempotent - does NOT duplicate existing keys).
# These write into .studio/.env.local (the Agent's secrets):
# Edit .studio/.env.local and set WALLET_PASSWORD there; bag auto-loads it.
# Never put the wallet password on a command line.
bag env set OPENROUTER_API_KEY '<api-key>'   # or whichever provider app/agent/studio.toml [llm] uses

# From the workspace root - `bag dev` serves the selected protocol:
bag dev                # A2A agent on :9000, MCP on :8000/mcp (same for any destination)
bag dev --port 9100    # override the port
```

`bag dev` sets `STORAGE_LOCAL_PATH=~/.bag/deliverables/<workspace-name>/` for the agent subprocess and runs it **without** Cognito env, so the local endpoint is reachable without a token (Cognito is mandatory only on the deployed AgentCore runtime). For A2A projects, the agent (`app/agent/src/unifiedMain.ts`) exposes `/.well-known/agent-card.json` + JSON-RPC `message/send` + `GET /ping` on `:9000`. Smoke-test the card with curl:

```bash
curl http://localhost:9000/.well-known/agent-card.json
```

Expect the agent card with its two skills (`negotiate`, `notify_funded`). For MCP projects, connect an MCP client to `http://localhost:8000/mcp`.

> ⚠️ **The AgentCore inspector chat box cannot test a seller agent.** A seller's skills are structured A2A `DataPart`s (`message/send`), but the inspector chat box can only send plain text - it can never construct a `{"skill":"negotiate", …}` part, so it can't reach the agent's real product surface (and its streaming view expects Task events, not the `message` reply the agent emits). **Test locally with curl or an A2A client sending a `DataPart`**, not the chat box.

Drive a sale by sending the skills directly (`negotiate` `terms` MUST include `deliverables` + `quality_standards`, else the quote is rejected `reason_code 0x04`):

```bash
# negotiate → signed quote envelope
curl -s -X POST http://localhost:9000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0","id":1,"method":"message/send",
  "params":{"message":{"role":"user","parts":[{"kind":"data","data":{
    "skill":"negotiate",
    "task_description":"...",
    "terms":{"deliverables":"...","quality_standards":"..."}
  }}],"messageId":"nego-1"}}}'

# notify_funded → ack (then background delivery; poll the chain for the result)
curl -s -X POST http://localhost:9000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0","id":2,"method":"message/send",
  "params":{"message":{"role":"user","parts":[{"kind":"data","data":{
    "skill":"notify_funded","job_id":<int>
  }}],"messageId":"notify-1"}}}'
```

See `erc8183-buyer-push.md` for the full line protocol. Ctrl-C to stop.

### B. Doctor - full project health

```bash
bag doctor
```

Returns a rich table of checks across the `app/agent/` sub-project:

| Check | What FAIL means | Fix |
| --- | --- | --- |
| app/agent/studio.toml parseable | Missing or syntax error | `bag init` to regenerate, or hand-fix TOML |
| Agent entrypoint imports | Protocol entrypoint raises on load (`src/unifiedMain.ts` for A2A, `src/mcpMain.ts` for MCP) | Fix the error printed by the check (often a missing env var or a broken import) |
| wallet keystore | No `<workspace>/.studio/wallets/*.json` | `bag wallet new` (writes to the workspace root keystore dir) |
| WALLET_PASSWORD env | Not in `.studio/.env.local` / not exported | Edit the owner-only `.studio/.env.local`; never pass the password on argv |
| LLM provider key | API key env not set | Edit `.studio/.env.local` or export the right `*_API_KEY` |
| Network reachable | RPC down/wrong URL | Override via `STUDIO_BSC_TESTNET_RPC=...` (testnet) / `STUDIO_BSC_RPC=...` (mainnet) - per-network env vars read by `@bnbagent/studio-runtime/networks` `getNetwork` |
| Wallet tBNB balance | 0 tBNB | Message https://t.me/bnbchain_official_bot: `I would like to get tBNB to my wallet <address>` (more options: docs.bnbchain.org/bnb-smart-chain/developers/faucet/) |
| Wallet U balance | 0 U | Message https://t.me/bnbchain_official_bot: `I would like to get U to my wallet <address>` (more options: https://united-coin-u.github.io/u-faucet/) |
| 8004 registered | Not registered | Normally registered automatically at `bag deploy verify`. Manual: `bag erc8004 register --endpoint <url>` (only if you need an on-chain identity before deploy). WARN-only in `bag doctor` - it doesn't block local dev. |

WARN-only items don't block; FAIL items do (exit 1).

### C. Balance / wallet inspection

```bash
bag wallet show     # local view: address + keystore path (workspace root .studio/wallets/)
bag wallet list     # all keystores in <workspace>/.studio/wallets/
```

For on-chain balance of the configured wallet (BNB + U):

```bash
bag wallet balance                       # [network].default - BNB + U
bag wallet balance --network bsc-mainnet # override to a specific network
bag wallet balance --all                 # both [network].default AND [llm.pieverse].network
```

The `--all` form is the right move when `app/agent/studio.toml`'s `[network].default = bsc-testnet` and `[llm].provider = pieverse-llm`: testnet U pays ERC-8183 jobs, mainnet U pays the Pieverse LLM auto-renew. Same wallet address on both chains.

A **rail-split asset gets one column per rail**, e.g. `USDC (ERC-8183)` and `USDC (b402)`, and the command lists both contracts underneath. On testnet, U and USDC each pair an 18-decimal ERC-8183 escrow token with a separate 6-decimal b402 settlement token, so funding one rail does NOT fund the other — a wallet can show plenty of `USDC (ERC-8183)` and still fail every x402 purchase. Mainnet assets use a single contract on both rails and stay one unqualified column. `bag doctor` splits the same way (`wallet U (b402) balance`) and reports seller-asset balances from the b402 contract, since that is where b402 payments land.

`bag doctor` prints ERC-8183 pricing as `PAID` or `FREE`. FREE works on the canonical contract stack. If a custom deployment is selected, set `ERC8183_COMMERCE_ADDRESS`, `ERC8183_ROUTER_ADDRESS`, and `ERC8183_POLICY_ADDRESS` together; a partial set fails because it can mix incompatible commerce, router, and policy deployments.

For the inbound x402 seller rail, `bag doctor` also prints `PAID` or `FREE`. PAID requires the complete B402 merchant credential set; any supported wallet kind can be the payout wallet (for altana the payout lands at the admin address anchored as `[wallet].address`). Explicit zero is anonymous FREE passthrough: it does not read B402 credentials, call the facilitator, settle a payment, or apply the paid-mode payout-wallet allowlist. Confirm the same state with `bag x402 sell status`.

> The current CLI has no `bag wallet transfer`, `bag erc20 approve/allowance` group, or `bag wallet balance --address` / `--token` flag. Running them returns an invalid-command or unknown-option error. Use an external wallet to move funds or set allowances; ERC-8183 funding auto-approves U as part of the buy flow.

For programmatic access from inside an agent's code, the MCP tools (when wired into Claude Code) provide `balance_u` / `balance_native` as well - but the CLI is the fastest path during dev.

### D. Job state inspection (8183)

```bash
bag erc8183 list --mine                    # all jobs where I'm the client
bag erc8183 list --provider 0xPROV         # jobs I could serve as seller
bag erc8183 status <job_id>                # one job's full record
```

JobStatus enum: `OPEN` (0) → `FUNDED` (1) → `SUBMITTED` (2) → `COMPLETED` (3) / `REJECTED` (4) / `EXPIRED` (5).

`FUNDED` jobs are what the deployed agent delivers - either when the buyer sends a `notify_funded` A2A message (the agent acks then delivers in the **background**; read the result from the chain) or via the deduped background sweep on the next notify (see `erc8183-buyer-push.md`). While background work is in flight the runtime stays warm via `/ping` `HEALTHY_BUSY`; a scaled-to-zero idle agent won't deliver until the next notify (a v2 Lambda poller closes that cold window). `SUBMITTED` jobs trigger the **buyer decision tree** (approve / dispute / reject within the dispute window) - full flow in the `bnbagent-studio-buying-via-8183.md` reference (see the Deep-dive references list above). From the seller side, defending a dispute is covered in `bnbagent-studio-selling-via-8183.md` (same directory).

### E. Common errors + remediation

| Error pattern | Cause | Fix |
| --- | --- | --- |
| `Submission deadline has passed` | Buyer set `expiredAt` too soon (< dispute_window) | Use `--deadline-min` ≥ 1 (workflow auto-adds dispute_window now) |
| `Transaction would revert: ('0x17be5b7b', ...)` | Trying to `settle approve` before dispute_window | Wait 24h or use `--action dispute` |
| `notify_funded` replies `{"status":"rejected","reason":...}` | `verifySignedJob` failed synchronously in the ack - a **permanent** failure | `reason` names it: not our signature / tampered terms / underfunded / expired (or `error` for a malformed `job_id`). The job is refused outright; re-fund/re-notify with a correct, fully-funded job |
| Job stays `FUNDED`, never reaches `SUBMITTED` after an `accepted` ack | Background delivery failed (`runWork` / `submitResult` raised) - **not** visible in the A2A reply | The ack only confirms verify passed; delivery runs in the background. Observe the failure via the chain (job never leaves `FUNDED`) + CloudWatch logs; a later `notify_funded` re-attempts it via the sweep |
| `ERC8183JobOps` has no such export from `@bnbagent/sdk` | package.json pinned an old `@bnbagent/sdk` (missing class) | Bump the dependency and reinstall |
| ERC-8183 contract override is incomplete | Only one or two of commerce/router/policy were selected | Set or remove all three together; never mix stacks |
| `/x402` is public without a 402 challenge | `payments.seller.price_usd = "0"` selected anonymous FREE passthrough | If payment is intended, set a positive decimal price, configure the complete B402 credential set, rerun `bag doctor`, and redeploy |
| B402 credentials are missing but x402 reports FREE | Expected: FREE bypasses B402 and does not synchronize its secrets | No credential fix is needed; change to a positive price only when the route should charge |
| `OPENROUTER_API_KEY env var is required` | Loading the entrypoint triggers the emitted `buildModel()` factory | Set the env var even for `bag dev --help` smoke |
| RPC `limit exceeded` | Public RPC throttle | Retry, or set `STUDIO_BSC_TESTNET_RPC=<private rpc>` |

## Reference

- `docs/design/single-seller-agent.md` (the A2A deploy model and history)
- `docs/design/erc8183-buyer-push.md` (how a buyer drives an A2A sale)
- `docs/design/architecture.md §2.5` (the single seller runtime - as-built truth)
