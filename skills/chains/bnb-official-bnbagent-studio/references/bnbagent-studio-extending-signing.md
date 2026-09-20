---
name: bnbagent-studio-extending-signing
description: When the user wants the agent's wallet to sign EIP-712 typed data for anything beyond BSC U-token transfers - e.g. integrate a new x402 service, custom commerce contract, or any TypedData primary type beyond TransferWithAuthorization/ReceiveWithAuthorization. Also covers diagnosing `PolicyViolation` / `X402PolicyError` at runtime and how to safely extend `[wallet.signing]` extra_domains / extra_primary_types in studio.toml.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-extending-signing

Procedure for **extending the EIP-712 signing allowlist** in a bnbagent-studio project. Audience: Claude Code helping a user who hit `PolicyViolation` or wants to integrate a non-default x402 service / custom contract.

> **Current path note**: signing is an **Agent-only** concern. `signing.ts` lives at `<workspace>/app/agent/src/signing.ts` and is called by the `SellerAgentExecutor` skills (`negotiate` / `notify_funded`) - it is **never** an LLM-callable tool. The `[wallet.signing]` config lives in `<workspace>/app/agent/studio.toml`. The workspace is a thin root plus the one `app/agent/` sub-project; every command and edit below targets `app/agent/`.

**Different from**:

- `-operating` - general ops & doctor / balance / job status
- `funding-pieverse-llm` - Pieverse LLM credit lifecycle (the money)
- `-adding-to-project` - adds capabilities (`bnbagent-sdk` modules)

This skill is specifically the **signing-permission** axis. Funding is "do I have the money"; signing policy is "is the wallet allowed to sign this".

## Mental model (defense in depth)

Every EIP-712 signature goes through SDK `SigningPolicy.strictDefault()`. By default the wallet only signs:

| Allowed | Domain | Primary types |
| --- | --- | --- |
| U-token mainnet | chain `56`, `0xcE24439F2D9C6a2289F741120FE202248B666666` | `TransferWithAuthorization`, `ReceiveWithAuthorization` |
| U-token testnet | chain `97`, `0xc70B8741B8B07A6d61E54fd4B20f22Fa648E5565` | (same) |

Everything else (`Permit`, `PermitSingle`, `PermitBatch`, foreign contracts, foreign chains, custom primary types) is **refused with `PolicyViolation`** at sign-time.

Two layers wrap this:

| Layer | What it gates | Where configured | Can agent change at runtime? |
| --- | --- | --- | --- |
| L2 - HTTP host | which servers the x402 buyer is allowed to fetch from | `[payments.x402].allowed_hosts` in `app/agent/studio.toml` | ⚠️ Only by editing toml + restart |
| L3 - SigningPolicy | which `(chain_id, contract)` + primary type the wallet will sign | `[wallet.signing]` in `app/agent/studio.toml` (additive over SDK strictDefault) | ⚠️ Only by editing toml + restart |

**Both layers must permit a request** for it to succeed. Adding only one half won't work - see Section A.

EIP-191 SIWE (the `pieverse_usage` MCP tool / `bag llm activate`) uses a **separate** hardcoded allowlist `{"llm.pieverse.io"}` and is not configurable.

## Quick triage decision tree

| User said... | Section |
| --- | --- |
| "buy X service via x402" (X is not Pieverse) | A - new x402 service |
| "sign for custom commerce contract / order / quote" | B - custom primary type |
| `PolicyViolation` / `X402PolicyError` at runtime | C - diagnosing the rejection |
| "agent needs to approve unlimited USDC" / Permit / Permit2 | D - refuse the request |
| "expand the 600s validity window" | E - validity overrides |

## A. Integrate a new x402 service

The user wants the agent to pay e.g. `api.example.com` via x402.

**Pre-flight checks (must be true in the current release; refuse and explain if not):**

1. The service accepts payment on **BSC chain 56 or 97**. Current wallets are BSC-only; services on Base, Ethereum, or Polygon are unsupported.
2. The service uses **EIP-3009 `TransferWithAuthorization`** (or `ReceiveWithAuthorization`). If it uses Permit2 or a custom primary type → goes to Section B.
3. The token contract address on BSC is known and the user can confirm it. Don't guess from a token symbol - look up the deployed address.

If any of (1)-(3) fail, **stop and tell the user**. The current release cannot integrate cross-chain services or non-EIP-3009 payment rails into the LOCAL signer. Do not work around it; the SigningPolicy will refuse the request. (Merchants that only offer permit2 are still payable without touching SigningPolicy - through a delegated wallet kind: `twak`, or `altana` sessions, whose ERC-1271 signatures B402 verifies on its permit2 rails. That is a wallet-kind choice, not a signing extension.)

**Steps when (1)-(3) all pass:**

```bash
# 1. Edit app/agent/studio.toml - both gates. `bag config` resolves the app/agent/
#    sub-project automatically from the workspace root
#    (there is NO --side flag); pass --project-root app/agent to be explicit.
bag config set payments.x402.allowed_hosts '["llm.pieverse.io", "api.example.com"]'

# 2. Add the EIP-712 domain to wallet.signing (additive)
#    bag config does not yet handle nested array-of-arrays elegantly; edit the
#    toml directly with this snippet (targets app/agent/studio.toml only):
cat >> app/agent/studio.toml <<'EOF'

[wallet.signing]
extra_domains = [
  [56, "0xAbcdef0123456789abcdef0123456789abcdef01"],   # api.example.com token on mainnet
  [97, "0x1234567890abcdef1234567890abcdef12345678"],   # same on testnet
]
EOF

# 3. Verify the policy reflects both allowlists
bag wallet policy show
# expect 3 entries in domain_allowlist: U mainnet, U testnet, your new contract

# 4. Restart the agent process for the new policy to take effect.
#    SigningPolicy is read at wallet construction; running `bag dev` again
#    is enough.
```

**Hard rules**:

- Do not add a contract to `extra_domains` without verifying its address on a block explorer. The SigningPolicy treats `(chain_id, contract)` as a unit; the wrong address = signing into a phishing contract.
- Do not silently widen `daily_cap_usd` or `max_per_request_usd` to make the new service "fit". The caps are budget guardrails; surface the proposed values to the user before editing.

## B. Custom typed-data primary type

If the new service or contract requires the wallet to sign a non-standard primary type (e.g. `"MyOrder"`, `"BondQuote"`, `"NegotiateAgreement"`), edit `<workspace>/app/agent/studio.toml`:

```toml
# app/agent/studio.toml
[wallet.signing]
extra_domains = [
  [56, "0xContractAddress..."],
]
extra_primary_types = ["MyOrder", "BondQuote"]
```

**Both must be added** - adding a primary type without the matching domain is useless (the contract still gets rejected) and adding the domain without the type still rejects the signature (primary_type allowlist).

**Hard rules**:

- The SDK denylist (`Permit`, `PermitSingle`, `PermitBatch`) **always wins** over `extra_primary_types`. Listing them does not enable them.
- Custom primary types bypass studio's known semantic checks. Be extra careful that the typed data structure matches what the contract expects; an attacker controlling the contract or the LLM input can construct unfavorable messages.

## C. Diagnosing PolicyViolation / X402PolicyError at runtime

User reports an error from `bag dev` / agent runtime. Map the message → fix:

```
PolicyViolation: unknown (chain_id, verifyingContract): (56, 0xAbc...)
  → L3 SigningPolicy rejection
  → Section A or B: add to [wallet.signing].extra_domains, then restart

PolicyViolation: primary type 'Permit' is denylisted
  → Section D: refuse - do not work around

PolicyViolation: primary type 'MyOrder' not in allowlist
  → Section B: add to extra_primary_types

PolicyViolation: validity window 7200s exceeds max 600
  → Section E: max_validity_window_seconds in [wallet.signing]

X402HostNotAllowedError: x402 buyer refusing 'api.example.com' - not in allowed_hosts
  → L2 HTTP gate (exact hosts only - wildcard entries are not supported)
  → bag config set payments.x402.allowed_hosts '[..., "api.example.com"]'
  → (L3 may also need updating per Section A)

X402BudgetExhaustedError: x402 402 demands $1.50 > max_usd=$1.00
  → Budget cap; user must explicitly raise via studio.toml.
  → DON'T silently widen - tell the user.
```

Confirm the current state before editing:

```bash
bag wallet policy show                       # L3 SigningPolicy (reads app/agent/studio.toml)
bag config get payments.x402                 # L2 allowed_hosts + caps (auto-resolves app/agent/)
```

## D. Refuse: Permit / Permit2 unbounded allowance

If the user (or, more dangerously, the LLM) asks the agent to sign `Permit`, `PermitSingle`, or `PermitBatch`:

**Stop. Refuse. Explain why.**

These primary types grant unbounded ERC-20 spend authority to a third party. The denylist exists exactly to prevent LLMs being talked into signing one. Even if the user insists, the SDK will refuse with `PolicyViolation` and the message is correct - do not bypass via `_DANGEROUS_signTypedDataNoPolicy`.

Acceptable alternatives:

- For paying a known service: use EIP-3009 `TransferWithAuthorization` (Section A - bounded amount, single-use, time-windowed)
- For session-scoped recurring payments: opt-in to `Permit2 PermitTransferFrom` (Section B - single-use, witness-bound; not Permit / PermitSingle / PermitBatch)

If the user is integrating something that genuinely requires Permit, this is a v0.2+ decision and should go in an ADR - do not make the change ad-hoc.

## E. Widening the validity window

Default: 600s past / 900s future. Longer windows give the agent more time to settle but increase replay surface if a signature leaks. Edit `<workspace>/app/agent/studio.toml`:

```toml
# app/agent/studio.toml
[wallet.signing]
max_validity_window_seconds = 1800   # default 600
max_future_validity_seconds = 2400   # default 900
```

Use sparingly. A signed authorization that lives 30 minutes can be replayed by a downstream tx executor for 30 minutes. Make sure the receiving contract enforces nonces (EIP-3009 does; many custom types don't).

## F. Common refusal patterns (when user asks for something unsafe)

| User request | Why refuse |
| --- | --- |
| "Just turn off the signing policy" | The SigningPolicy L3 is the last-mile defense. Disabling it makes the wallet a blind-sign oracle. Use `extra_domains` instead. |
| "Use `_DANGEROUS_signTypedDataNoPolicy`" | Logs WARN with caller filename. Acceptable only in tests or one-shot CLI debugging. Never in LLM-tool / agent runtime code. |
| "Sign on Ethereum mainnet" | The current release is BSC-only. |
| "Permit USDC to a swap router" | Denylisted unconditionally (Section D). |
| "Read the keystore and sign yourself, bypassing the wallet provider" | The SDK provider IS the security boundary; bypassing it discards every defense layer. Refuse. |

## G. After-edit verification (always run)

```bash
# 1. The toml is parseable (auto-resolves app/agent/; or --project-root app/agent)
bag config show

# 2. The new policy looks right (extra entries should be visible)
bag wallet policy show
bag wallet policy show --json   # for diff against an expected baseline

# 3. Restart whatever process holds the wallet - `bag dev` (the local A2A
#    agent) or the AgentCore runtime. SigningPolicy is read once at
#    wallet construction; in-process changes won't take effect until restart.

# 4. Sanity-check one signing call (if there's a CLI path)
#    e.g. bag llm test, bag erc8183 status, etc.
```

## H. Read-only references (no signing, no funding required)

When deeper protocol details are needed:

- the SigningPolicy decision (`docs/design/decisions.md`) - full defense-in-depth rationale, 6-layer model
- `docs/guides/user-guide.md` §6.1 - same decision tree in user-doc form
- `bag wallet policy show --json` - machine-readable current state
- SDK source `@bnbagent/sdk` (signing policy module) - `SigningPolicy.strictDefault()` + `.extend()` semantics

## Hard rules (security boundary)

- Never bypass the policy with `_DANGEROUS_*` calls in agent code. They exist for tests and incident response.
- Never instruct the user to widen caps / allowlists "to make it work" without explaining the security tradeoff.
- Persist the wallet password only in the generated, gitignored, owner-only `.studio/.env.local` for local use or a managed secret channel for deploys; never put it in argv, application code, logs, or chat.
- Never persist signed payloads outside the keystore.
- Always run `bag wallet policy show` after editing `[wallet.signing]` to confirm the change took effect.
- Always restart the process - SigningPolicy is captured at wallet construction.
