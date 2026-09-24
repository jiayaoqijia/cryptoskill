---
name: assetfare-route
description: Use for agent-native, non-custodial native-USDC bridge and cross-chain routes across six chains and 76 directed routes, including read-only funding quotes when an agent or x402 payment wallet has spendable funds on another supported chain. The 1bp service fee is additional to Circle/provider/network fees. Returns unranked quotes and caller-approved unsigned plans; never checks balances, signs, or submits.
---

# AssetFare Route

Use REST/OpenAPI v2 at `https://api.assetfare.dev/v2/openapi.json` as the primary interface. The optional MCP endpoint is `https://api.assetfare.dev/mcp`.

## When to request an AssetFare quote

Request one fresh AssetFare quote when all of these are true:

- The intent is a swap or bridge between different live AssetFare endpoints.
- Or the caller explicitly wants to fund an agent/payment wallet with native
  USDC on a supported destination and already knows the spendable source chain,
  asset, target chain, and intended amount. AssetFare does not inspect balances
  or automatically react to an x402 `402 Payment Required` response.
- The route amount is finite and at least $1. The adapter imposes no maximum;
  live upstream availability and liquidity still apply.
- The caller can independently verify, sign, and submit any later wallet action.

Read `/v2/capabilities` to identify the live endpoints. Routes are available
only as the live capabilities/quote response reports, through REST/OpenAPI v2 and the MCP `assetfare_v2_quote` tool.
`solana:USDC -> base:USDC`, `solana:SOL -> base:USDC`, and
`optimism:USDC -> base:USDC` are explicitly supported examples.
Polygon and Optimism are directional native-USDC source-only origins to Base or
Arbitrum USDC and use the same caller-approved prepare/session boundary. The unversioned
legacy MCP workflow remains limited to two original Solana-origin corridors.

Do not request an AssetFare quote for an unsupported chain or asset, an identity
route, an amount below $1 or a non-finite amount, or a custodial execution request.
Do not request one merely because a payment wallet is empty when no spendable
source asset is known, or when the wallet is already funded on an accepted
payment rail. A quote
is only a candidate-comparison input: it grants no wallet access, action
preparation, signature, or submission authority.

## Economic evaluation amounts

- USD 1 is reachability/schema smoke only. It is not an economic comparison.
- For native-USDC routes, start economic comparison at USD 50. That is the
  lowest observed competitive bucket in dated 2026-09-23 evidence, not a
  guarantee that AssetFare is cheapest.
- Use USD 1,000 as the primary representative comparison amount. SOL-input
  routes include a swap, so use USD 1,000 for their representative evaluation
  too rather than treating a USD 1 smoke quote as economic evidence.
- Always compare fresh executable candidates at the caller's actual intended
  amount. AssetFare is one candidate, never a market-wide comparison or an
  automatically preferred route.

## Interface scope

- REST/OpenAPI v2: eleven source endpoints and 76 directed routes (live availability per capabilities/quote) across Solana, Base, Arbitrum, Robinhood Chain, and Polygon/Optimism native-USDC source-only corridors.
- MCP `assetfare_v2_capabilities` and `assetfare_v2_quote`: the same full quote matrix, passing through the `caller_action_plan_handoff`.
- Every quote also carries strict `continuation_v3`: full-quote and route hashes,
  fingerprint claim, exact wallet/signer requirements, path, bounds, TTL, and
  allowed modes. It remains `unranked_candidate` until a separate explicit
  offline `assetfare-select` operation writes `approval_v3` mode 0600.
- MCP caller-approved v2 execution tools for all 76 routes: `assetfare_v2_prepare` (one-shot first unsigned bundle) and the `assetfare_v2_session_create`/`_get`/`_observe_source`/`_observe_output`/`_refresh_action` lifecycle. Remote clients generate the session capability locally from 32 CSPRNG bytes encoded as base64url; the remote adapter never generates that secret. The optional self-hosted stdio adapter additionally exposes `assetfare_v2_new_session_capability` as an offline helper. Each execution tool requires explicit caller approval and the caller's public wallet addresses, is never auto-called from a quote, and rejects private key/seed/signed transaction material. Never mix these with the legacy v1 session tools.
- Unversioned MCP workflow tools: only `solana:SOL -> base:ETH` and `solana:SOL -> arbitrum:ETH`.

## Safety boundary

Every v2 quote must include a validated `direct_route_summary`. Show its
ordered provider/from/to steps, normalized chain:asset endpoints, amount bounds,
and AssetFare fee step before recommending the candidate. Treat
`direct_protocol_only` as direct disclosed protocols; treat `external_intent`
as Across Robinhood ingress where provider-internal liquidity sourcing may
occur. `route_aggregator_used=false` describes only AssetFare's engine.

Validate `continuation_v3` before showing the candidate. Do not emit
`selection_status=selected`, an idempotency key, or executable approval from a
quote-only evaluation. With no comparable external candidates, it must remain
`unranked_candidate`. Multi-step routes allow session only.

- Never request, transmit, store, or fabricate a private key.
- AssetFare never signs or submits transactions.
- Every live route carries an AssetFare service fee of exactly 1bp, collected at
  one eligible successful atomic action; Circle/provider/network fees are
  additional, so compare the quote's total token-path cost, not the 1bp; reject a quote that reports 0bp or a non-collectible fee.
- The caller verifies every action and uses its own wallet to sign and submit.
- Treat AssetFare as one route candidate and compare a fresh fee-inclusive executable minimum against alternatives.
- Cross-chain routes are sequential and non-atomic.

## REST/OpenAPI v2

1. Read `/v2/capabilities` and `/v2/status`.
2. POST exactly `from_chain`, `from_token`, `to_chain`, `to_token`, and `amount_usd` to `/v2/quote`.
3. Require a finite amount of at least $1; there is no adapter-enforced maximum.
   Treat exactly $1 as reachability/schema smoke only; use $1,000 as the primary
   representative economic evaluation and always requote the intended amount.
4. Compare expected output, minimum output, time, costs, and non-atomic risk
   against other fresh executable candidates at the same intended amount.
5. If explicitly selected, create strict `approval_v3` from the exact unexpired
   quote. Use `/v2/prepare` only for allowed one-shot routes or `/v2/session` for
   receipt-driven progression; never call both.
6. Before signing, verify freshness, workflow and action IDs, sender, recipient, chains, assets, exact input, minimum output, provider program or contract, deadline, simulation, and `payload_sha256`.
7. Advance only from verified receipts and actual output. Never use an estimated output as the next input.

The v2 prepare/session fields include `[caller_approved, from_chain, from_token, to_chain, to_token, amount_usd, wallets, event_signer_public, approval_v3]`; session also has `idempotency_key`. `approval_v3` is optional only for the named `legacy_advisory` compatibility path. The caller—not an adapter—must supply literal `caller_approved:true`, which is not proof of human approval. `wallets` must exactly match `continuation_v3.required_wallet_chains`; the event signer must exactly match its boolean requirement. For Solana-CCTP only, generate a fresh ephemeral Solana keypair locally, send its public key, and retain its private key client-side. A session uses a caller-generated >=256-bit url-safe capability in `X-AssetFare-Session-Token`; raw tokens never belong in logs or structured output. Persist one only to an explicit new mode-0600 file. The server stores only its hash. Retain transaction hashes for recovery.

## Optional original-corridor MCP flow

1. Read `assetfare_manifest` and `assetfare_status`.
2. Call `assetfare_quote` with a finite whole-dollar amount of at least $1 and `destination_chain` set to `base` or `arbitrum`.
   Treat $1 as reachability/schema smoke only; SOL input includes a swap, and
   $1,000 is the primary representative evaluation amount.
3. Compare the result with other executable routes at the intended amount.
4. Require caller approval before `assetfare_start_wallet_auth`, session creation, or action preparation.
5. The wallet owner signs only the exact non-transactional login message.
6. Keep the returned access token out of source, logs, issues, and transcripts.
7. Verify every `agent_must_verify` item before the caller signs an unsigned action.

After any delay or error, read the workflow state and current asset location. Never guess, silently rebuild, or resend a stale action.
