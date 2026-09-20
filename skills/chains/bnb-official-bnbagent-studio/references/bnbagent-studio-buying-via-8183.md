---
name: bnbagent-studio-buying-via-8183
description: When the user is acting as ERC-8183 buyer - finding a provider, getting a quote, buying a service, fetching the deliverable, and deciding to approve / dispute / reject the work. Owns the buyer-side decision tree for the entire job lifecycle including settle-window timing (24h dispute window), dispute governance flow, and `Submission deadline has passed` recovery.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-buying-via-8183

> **v1 scope note:** v1 is **seller-only** - buyer flows are **NOT** the main v1 payment path. The x402 buyer kernel survives only as the Agent's _automatic_ LLM top-up (`@bnbagent/studio-runtime/x402`, budget-gated, not an LLM tool), and the erc8183 `buyWorkflow` survives as an **underlying capability** still reachable via the `bag erc8183 buy/status/fetch/settle` CLI. Full buyer-side _product_ flows (a buyer agent, buyer-side negotiation wrapping) are deferred to v2. The CLI procedure below still works for manual / testing use.

Procedure for **buyer-side flow**: have your agent (or you directly via CLI) purchase a service from another ERC-8183 seller, verify the deliverable, and close out the job with the right `settle` action.

Audience: Claude Code in a current TypeScript workspace with a funded wallet (gas + the explicitly selected active catalog asset: Mainnet U/USD1/USDC/USDT or Testnet U/USDC/USDT). The buying CLI (`bag erc8183 buy/status/fetch/settle`) targets the **Agent sub-project's** wallet - these commands resolve to `<workspace>/app/agent/` automatically when run from the workspace root.

> **Protocol facts** (independent of the local filesystem layout): 24h dispute window, `0x17be5b7b` revert, `expired_at` arithmetic.

**Different from**:

- `bnbagent-studio-operating.md` (same directory) - generic ops (dev / doctor / balance / RPC); jumps here for buyer-specific decisions
- `bnbagent-studio-adding-to-project` - covers wiring a buyer tool set into an existing project (the static setup, not the runtime decisions)
- `bnbagent-studio-selling-via-8183.md` (same directory) - the mirror playbook for the seller side (`on_job`, dispute defense)

This skill owns: **buy → fetch → approve/dispute/reject loop**, whether driven via CLI or the agent's LLM calling `erc8183_buyer_set` tools.

## Buyer settle decision tree (load this skill when the user hits any of these)

`SUBMITTED` job → buyer has three options, **time-gated by the on-chain dispute window**:

| Action | Allowed | What happens |
| --- | --- | --- |
| `bag erc8183 settle <id> --action approve` | **After 24h dispute_window has passed** (chain enforces; reverts with `0x17be5b7b` if early) | Job → `COMPLETED`; seller receives the job-bound token |
| `bag erc8183 settle <id> --action dispute` | **Within dispute_window** | Opens governance flow; quorum vote decides; refund possible |
| `bag erc8183 settle <id> --action reject` | **Only if you're a quorum voter, not the buyer** | Job → `REJECTED` via governance |

If the buyer agent (or LLM) is about to call `settle --action approve` and it's been <24h since SUBMITTED, **wait** or use `dispute`. Don't try to retry through the revert - read the error and pick the right action.

Common error: `Submission deadline has passed` → buyer set `expiredAt` too short (< dispute_window). Fix: re-buy with `--deadline-min ≥ 1` (the buy flow now auto-adds dispute_window).

## Preconditions

- `bag doctor` is clean (or only warns on LLM key)
- For a paid job, the wallet has gas and enough of the selected catalog token for the budget plus slack. On Mainnet, `USD1` is `0x8d0D000Ee44948FC98c9B98A4FA4921476f08B0d`, 18 decimals and EIP-3009-only (`World Liberty Financial USD / 1`); it is implemented but needs Commerce allowlist/live verification before release. On Testnet, ERC-8183 U resolves to `TEST_U` at `0xc70B8741B8B07A6d61E54fd4B20f22Fa648E5565` (18 decimals); USDC/USDT resolve to their network-specific canonical IDs, and USD1 is unsupported. A job stores exactly one immutable token. Sponsorship remains target-specific, and an ERC-20 approval may still need gas. For a FREE job use `--budget-usd 0`: no token balance, approval, or escrow is needed.
- You know the **provider's wallet address** (the seller agent's address)
- The seller is **reachable** (its A2A agent is deployed somewhere); discoverable via the provider's `bag erc8004 resolve <agent_id>` endpoint URI

## Stage 1 - Pre-flight checks

```bash
# 1. Confirm wallet + balances
bag wallet show
bag doctor       # tBNB + U checks should be PASS

# 2. Confirm the provider's 8004 record (optional but recommended)
bag erc8004 resolve <provider_agent_id>
# → returns the agent_uri; decode it (base64 data: URI) to verify the endpoint URL
```

Automatic negotiation by `--agent-id` requires a public HTTPS provider endpoint and refuses redirects, credentials in the URL, loopback, and private addresses. For local protocol testing, negotiate manually and buy with `--provider <addr> --no-negotiate` instead.

## Stage 2 - (Optional) Negotiate price

The current `@bnbagent/studio-runtime` wraps the buyer-side negotiation handshake (`@bnbagent/studio-runtime/erc8183` `negotiateWithSeller`, wired into the buy workflow). It fires automatically when you buy by `--agent-id` (resolves the seller's endpoint from its ERC-8004 record, then POSTs `/negotiate`); pass `--no-negotiate` to skip it. When you buy by `--provider <addr>` you supply the budget directly and assume the price was agreed off-chain.

If you want to talk to the seller manually, the seller now exposes its `negotiate` skill over **A2A** (the seller's ERC-8004 endpoint URI is an A2A base URL): send an A2A `message/send` JSON-RPC call carrying a `DataPart` `{"skill": "negotiate", "task_description": "...", "terms": {...}}` (+ the seller's OAuth2 Bearer when deployed). The reply data part is the signed `NegotiationResult` quote. For the normal CLI flow, go straight to buy.

## Stage 3 - Buy

```bash
# Omit --asset only when you intentionally want default U.
# --budget-u remains a U-only compatibility flag; --budget-usd is preferred.
# --deadline-min is the seller's submission window (default 30).
bag erc8183 buy --provider <provider_addr> "<task description>" \
  --asset USDC \
  --budget-usd <amount> \
  --deadline-min <minutes> \
  --network bsc-testnet
# provider is a REQUIRED flag (--provider <addr> OR --agent-id <id>), not a positional;
# `--agent-id` resolves the endpoint + negotiates first.

# Mainnet USD1 is explicit; it never changes the Buyer default U.
bag erc8183 buy --provider <provider_addr> "<task description>" \
  --asset USD1 \
  --budget-usd <amount> \
  --deadline-min <minutes> \
  --network bsc-mainnet
```

For a signed FREE quote:

```bash
bag erc8183 buy --provider <provider_addr> "<task description>" \
  --budget-usd 0 --deadline-min 30 --network bsc-testnet
```

> **Task can be passed two ways** (both accepted): as a positional argument `bag erc8183 buy --provider <addr> "<task>"` OR via the flag `bag erc8183 buy --provider <addr> --task "<task>"`. Pass it once - supplying both at the same time is an error.

The 4 on-chain steps run sequentially:

1. `createJobWithToken(provider, expiredAt, description, token)` → returns `job_id`
2. `registerJob(jobId)`
3. `setBudget(jobId, rawBudget)`
4. `fund(jobId, rawBudget, approveFloor=rawBudget)` - auto-approves the job token only when the positive budget needs allowance; budget 0 skips approval and escrow

If the selected asset is unavailable or underfunded, Studio prints only verified alternatives with exact `--asset SYMBOL` hints. It does not switch token, create a job, or retry payment automatically.

Output prints 4 tx hashes + `job_id`. Note the `job_id` for later.

**Gotcha**: `expired_at = now + deadline_minutes*60 + dispute_window` (24h). This is intentional - the chain enforces that submission must happen before `expired_at - dispute_window`. If you set `deadline_minutes=30`, the seller has 30 min to submit (then a 24h dispute window starts).

## Stage 4 - Wait for SUBMITTED

The single seller runtime has **no standalone poller** - after funding, send a `notify_funded` A2A message to the seller ("I funded job X, please deliver"). The seller **acks `accepted` immediately and delivers in the background**, so you do **not** get the deliverable in the A2A reply - you poll the chain for it. The seller also sweeps other funded jobs on each `notify_funded` (in the background, deduped). Check status:

```bash
bag erc8183 status <job_id>
```

Statuses:

- `OPEN` → not yet funded (shouldn't see this after Step 3)
- `FUNDED` → waiting for seller to pick up + submit
- `SUBMITTED` → ready to fetch + settle
- `EXPIRED` → seller missed the deadline; use `bag erc8183 settle --action ...` or the SDK's `mark_expired` / `claim_refund`

Delivery is no longer instant: because the seller works in the background, the wait is however long its work takes (seconds to minutes). Poll until `SUBMITTED`, then read `deliverable_url` (Stage 5). If it stays `FUNDED`, either no one sent `notify_funded` (and the sweep hasn't run - the seller may be scaled to zero), or the seller's background work failed or hasn't finished yet - re-send `notify_funded` to nudge it while the runtime is warm. (Also possible: a config mismatch, most often `expired_at` too soon - but the workflow auto-fixes this now.)

## Stage 5 - Fetch the deliverable

The single seller runtime serves **no** job-query endpoint - the deliverable is read back from the on-chain submission (the `submit` tx carries the stable `deliverable_url`). This may be IPFS for self-hosting or a content-addressed HTTPS URL for S3, Azure Blob, or managed-platform storage. Get the URL via CLI:

```bash
bag erc8183 fetch <job_id>
```

Prints the `deliverable_url`. Fetch it directly (using a gateway when the scheme is `ipfs://`) to read the `DeliverableManifest`: `{"chain_id", "contracts", "job_id", "response": {"content": ..., "content_type": ...}, "metadata": {...}}`.

## Stage 6 - Settle

```bash
# Happy path: accept the deliverable. NOTE: must wait 24h dispute_window first.
bag erc8183 settle <job_id> --action approve

# Bad deliverable: dispute (within dispute_window, no wait needed)
bag erc8183 settle <job_id> --action dispute

# (rare) you're a quorum voter and want to reject:
bag erc8183 settle <job_id> --action reject
```

Returns a tx hash. Verify on BscScan.

**On `--action approve` revert with `0x17be5b7b`**: chain refuses because `submitted_at + dispute_window > now`. Either wait the remaining time or use `--action dispute` for immediate effect.

## Stage 7 - Verify on-chain settlement

```bash
bag erc8183 status <job_id>
# Expect: status COMPLETED (after approve) or unchanged SUBMITTED (after dispute, until voters resolve)
```

Check seller's U balance increased (minus platform fee - see `CommerceClient.platform_fee_bp()`).

## End-to-end smoke (one-shot, for testing your setup)

```bash
# Buyer side (this assumes the seller's A2A agent is already deployed somewhere)
PROVIDER=<seller_address>
JOB=$(bag erc8183 buy --provider $PROVIDER "test task" --budget-u 0.5 | awk -F': *' '/job_id:/{print $2; exit}')
# send a `notify_funded` A2A message to the seller for that JOB (buyer-push),
# then poll the chain (the seller acks at once and delivers in the background):
sleep 60
bag erc8183 status $JOB
bag erc8183 settle $JOB --action dispute
```

For the FREE regression, change the budget to `0` and confirm the compatible contract job still reaches `FUNDED` and `SUBMITTED` without an ERC-20 approval or balance change.

This is the exact end-to-end flow used to validate real-chain buying. See the references below for the canonical picture.

## Reference

- `docs/design/erc8183-reference.md` (SDK surface map / negotiation envelope)
- `docs/design/single-seller-agent.md` + `docs/design/erc8183-buyer-push.md` (the v1 single-agent model + buyer-push flow)
- `docs/guides/verification.md` (manual on-chain verification)
