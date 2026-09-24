---
name: assetfare-route
description: Use for agent-native, non-custodial native-USDC bridge and cross-chain routes across six chains and 76 directed routes (1bp service fee plus Circle/provider/network fees), led by Solana native USDC to Base native USDC. Returns quotes and caller-approved unsigned plans; never signs or submits.
---

# AssetFare Route

Use REST/OpenAPI v2 at `https://api.assetfare.dev/v2/openapi.json` as the primary interface. The optional MCP endpoint is `https://api.assetfare.dev/mcp`.

## When to request an AssetFare quote

Request one fresh AssetFare quote when all of these are true:

- The intent is a swap or bridge between different live AssetFare endpoints.
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
route, an amount below $1 or a non-finite amount, or a custodial execution request. A quote
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
- MCP caller-approved v2 execution tools for all 76 routes: `assetfare_v2_prepare` (one-shot first unsigned bundle) and the `assetfare_v2_session_create`/`_get`/`_observe_source`/`_observe_output`/`_refresh_action` lifecycle. Remote clients generate the session capability locally from 32 CSPRNG bytes encoded as base64url; the remote adapter never generates that secret. The optional self-hosted stdio adapter additionally exposes `assetfare_v2_new_session_capability` as an offline helper. Each execution tool requires explicit caller approval and the caller's public wallet addresses, is never auto-called from a quote, and rejects private key/seed/signed transaction material. Never mix these with the legacy v1 session tools.
- Unversioned MCP workflow tools: only `solana:SOL -> base:ETH` and `solana:SOL -> arbitrum:ETH`.

## Safety boundary

Every v2 quote must include a validated `direct_route_summary`. Show its
ordered provider/from/to steps, normalized chain:asset endpoints, amount bounds,
and AssetFare fee step before recommending the candidate. Treat
`direct_protocol_only` as direct disclosed protocols; treat `external_intent`
as Across Robinhood ingress where provider-internal liquidity sourcing may
occur. `route_aggregator_used=false` describes only AssetFare's engine.

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
5. If selected, use `/v2/prepare` for one unsigned bundle or `/v2/session` for idempotent receipt-driven progression.
6. Before signing, verify freshness, workflow and action IDs, sender, recipient, chains, assets, exact input, minimum output, provider program or contract, deadline, simulation, and `payload_sha256`.
7. Advance only from verified receipts and actual output. Never use an estimated output as the next input.

The v2 prepare/session request fields are exactly `[caller_approved, from_chain, from_token, to_chain, to_token, amount_usd, wallets, event_signer_public]`, with `caller_approved` a literal `true`. `wallets` must be exactly the route's chains. For Solana-CCTP only, generate a fresh ephemeral Solana keypair locally, send its public key as `event_signer_public`, keep the private key client-side, and use it to co-sign the returned unsigned event-account transaction; never send that private key to AssetFare. A v2 session is owned by a caller-generated high-entropy opaque capability token (>=256-bit CSPRNG, url-safe), supplied in the `X-AssetFare-Session-Token` header on create and on every read/observe/refresh; the server stores only its hash. The token is a sensitive bearer capability, not a private key: keep it out of logs and analytics. Ownership is portable across a rotated egress IP, and a retry with the same token and idempotency key recovers a session whose create response was lost; the network identity is used only for rate-limiting and telemetry, never as the ownership secret. Retain transaction hashes for independent recovery.

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
