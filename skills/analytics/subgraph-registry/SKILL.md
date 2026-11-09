---
name: subgraph-registry-mcp
description: Use to discover The Graph subgraphs by chain, protocol, entity or contract and turn a goal into a bounded GraphQL query. Bring-your-own Studio key (set up by a human operator) for execution; discovery never executes queries or signs payments, and x402 is an explicitly paid external option.
metadata:
  {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://github.com/PaulieB14/subgraph-registry"}}
---

# Subgraph Registry

Same abilities as [graphops/subgraph-mcp](https://github.com/graphops/subgraph-mcp) (hosted SSE `https://subgraphs.mcp.thegraph.com/sse`), **better discovery**. Search/recommend/semantic stay DISCOVERY — they never execute GraphQL. Schema and execute are opt-in and use the **same tool names** as official so an agent can swap connectors. Volume is already on every search hit (`query_volume_30d`) — skip official's extra `get_deployment_30day_query_counts` round-trip. Official that tool has been observed returning 0 for ENS/Lido/Uniswap; this registry does not copy those zeros. No private key. Set `THE_GRAPH_STUDIO_API_KEY` (or `GATEWAY_API_KEY`) for execute/live-schema; without a key those tools return `credentials_required` + both URLs and do not hang or auto-pay x402.

## Agent quick path: connect → discover → prepare → opt in

1. **Connect a reviewed, pinned release.** This is the canonical shareable skill;
   share this file with the GitHub repository, not a second `skills.md` recipe.
   For a stdio MCP host, start with this keyless configuration:

   ```json
   {"mcpServers":{"subgraph-registry":{"command":"npx","args":["-y","subgraph-registry-mcp@0.12.0"]}}}
   ```

   Inspect `tools/list` before calling a tool. Keyless 0.12.0 advertises 10
   discovery/preparation tools; execution/schema/health tools are advertised only
   when a Studio key is configured. A mounted connector can use another runtime
   or corpus: do not assume installing a release updates an existing connector.
2. **Discover with explicit chain identity.** For example, call
   `search_subgraphs({"network":"arc","include_unserved":true,"limit":3})`.
   This explicitly broadens discovery to zero-allocation snapshot records; it
   does **not** probe them or establish serving health. `arc` is mainnet;
   `arc-testnet` is different. Other examples: `ethereum`→`mainnet`,
   `arbitrum`→`arbitrum-one`, `polygon`→`matic`, `sei`→`sei-mainnet`.
   Use `query:"ens"` for a protocol and `network` for its chain. Inspect
   `emerging`, network and testnet labels, not just reliability. If results are
   empty, inspect `diagnostics` when available; otherwise check registry stats
   and deliberately broaden the relevant `include_*` flag. Never interpret an
   empty snapshot as proof that a chain or queryable Subgraph does not exist.
3. **Bring your own Studio key — a human handoff.** Keyless discovery and query
   preparation work without one. Executing queries needs the operator's own Graph
   Studio API key; this server never ships or shares a key. Studio keys belong to
   a Studio account managed by a person, so an agent should **not** create
   accounts, sign up or mint keys itself. Relay this to your human (keyless
   `query_for_goal` returns the same text as `onboarding.relay_to_human`):

   > To let me run live queries on The Graph with your own quota: sign in to
   > Subgraph Studio (https://thegraph.com/studio/apikeys/) with a Studio account
   > you manage, create an API key, and add it to this MCP server's environment or
   > secret manager as `THE_GRAPH_STUDIO_API_KEY`, then restart the server. Please
   > don't paste the key into this chat.

   Never ask for the key in ordinary chat or put it in tool arguments, source,
   URLs or logs. A configured key is not proof that it is valid or has quota.
   [Official pricing](https://thegraph.com/studio-pricing/) advertises **100,000
   free monthly queries**; check the account's current plan and remaining usage.
   This is not a fresh allowance per key, and Studio development endpoints have
   separate limits. See "Host configuration" below for copy-paste examples.
4. **Prepare a goal-specific query without spending.** Call, for example,
   `query_for_goal({"goal":"Uniswap V4 pool IDs on Arc","chain":"arc","first":3})`.
   Read `goal_mapping`: the requested entity (pools, swaps, candles/OHLCV,
   daily/hourly data, positions, liquidations, tokens, borrows, mints…),
   `confidence`, `rationale`, `unmet` parts and ranked `alternatives`.
   - Keyless plans use the registry's crawled entity names: the collection is
     derived the way graph-node names it, and fields are `id` plus stored-starter
     fields only when that starter targets the same entity. Ordering, typed
     filters (time ranges, relation addresses) and aggregation intervals are
     listed in `unmet` rather than guessed. Confidence is at most `medium`.
   - With a key, `validate_schema:true` adds ONE scoped introspection request that
     confirms the collection, fields, `orderBy` and `where` filters, then adds
     goal-relevant fields and typed filters. Only then is confidence `high`.
     If a requested address/time filter cannot be applied it appears in
     `filters_not_applied` and execution is skipped instead of returning
     unfiltered rows.
   - `query:null` with `confidence` `low`/`none` means no entity mapped
     confidently: pick from `alternatives` or inspect `get_subgraph_detail`.
     `hidden_candidates` lists matching deployments excluded by default filters;
     opt in with `include_denied` / `include_unserved` (not queryability tests).
   - Goals without entity intent return the stored starter with
     `confidence:"generic_starter"`.
   This goal mapping ships in 0.12.0; earlier releases return the stored
   starter. With an older six-tool connector, use
   `recommend_subgraph` / `get_subgraph_detail` and the stored starter instead.
5. **Execute only when requested and authorized.** With a key configured,
   keyed `query_for_goal` results include `next_action.execute_call`, e.g.
   `{"goal":…,"first":3,"validate_schema":true,"execute":true}`: one schema check
   plus one gateway query from the operator's own allowance, never x402. Execution
   is skipped when no query mapped confidently or live validation failed.
   `execute_query` with a reviewed query is the other opt-in path. A direct keyed
   client uses the returned fixed gateway URL and
   `Authorization: Bearer <STUDIO_API_KEY>`; never print the actual header.
6. **Read errors and evidence.** HTTP 200 can contain GraphQL `errors` or partial
   `data`. Report them, don't claim success from HTTP status alone. For missing
   credentials follow step 3; for quota/billing errors stop rather than silently
   switching to a paid route. Health observations are process-local, stale after
   300 seconds, and do not prove chain-head sync. No observation means unknown.

**Across ALL chains:** rewards/curation eligibility, on-chain allocation counts,
query demand and actual query availability are distinct. A chain can serve data
before rewards or curation signaling are enabled. `include_unserved` is a legacy
flag name for including zero-allocation **snapshot** records, not a declaration
that those records cannot be queried. `denied` means the recorded deployment was
denied indexing rewards, not proof it is malicious or unavailable. The corpus
does not establish every chain's current rewards/signaling eligibility and does
not include every Studio-only deployment. See [supported network modes](https://thegraph.com/docs/en/supported-networks/).

**Paid alternative, never a fallback without consent:** external x402 clients can
sign a USDC payment authorization and retry automatically. This is a financial
capability of that external client, NOT this MCP server. Require the owner's
explicit approval of the payment/amount before using a funded signing client;
do not run the README payment example just because a free/keyed request failed.

## New agent workflow (Node MCP)

- `find_by_contract(address, chain?, limit=3)`: exact normalized EVM manifest lookup; optional chain, limit 1–20. `schema_entities` cover the deployment, not a verified contract/entity mapping. Missing dynamic/substreams coverage is explicit.
- `check_subgraph_health(id | subgraph_id | ipfs_hash | deployment_id)`: opt-in, Studio-key-only fixed `_meta` request; known IDs pin the crawled deployment. `freshness.live` is measured, process-local, stale after 300 seconds, null before observation. Serving is not chain-head sync. `registry_updated_at` is upstream metadata time, not health/crawl time.
- `query_for_goal(goal, chain?, first?, execute=false, validate_schema=false, include_denied=false, include_unserved=false)`: maps goal intent to a deployment entity and returns a bounded query (1–10 rows; `first` defaults to a number in the goal or 5) with `goal_mapping` rationale/confidence/unmet/alternatives, or `query:null` when nothing maps confidently. No calls by default, even with a key. With a key, `validate_schema:true` adds one scoped introspection request and `execute:true` one pinned gateway query; no retry, fallback, arbitrary endpoint or x402 payment. Keyless responses include `onboarding` (human handoff, placeholder-only config and curl). Execution errors/partial data are surfaced.

## Host configuration (bring your own key)

The key is read only from the server process environment
(`THE_GRAPH_STUDIO_API_KEY`, or `GATEWAY_API_KEY`). Prefer your host's secret
or environment interpolation over writing the key into a config file; never
commit a key. Restart the server after setting it, then check that `tools/list`
now includes `execute_query` (19 tools instead of 10).

- **Cursor** (`~/.cursor/mcp.json` or `.cursor/mcp.json`; `${env:NAME}` is
  resolved from the environment Cursor was launched with):

  ```json
  {"mcpServers":{"subgraph-registry":{"command":"npx","args":["-y","subgraph-registry-mcp@0.12.0"],"env":{"THE_GRAPH_STUDIO_API_KEY":"${env:THE_GRAPH_STUDIO_API_KEY}"}}}}
  ```

- **Claude Code** (`.mcp.json` supports `${VAR}` expansion; or
  `claude mcp add --env THE_GRAPH_STUDIO_API_KEY="$THE_GRAPH_STUDIO_API_KEY" --transport stdio subgraph-registry -- npx -y subgraph-registry-mcp@0.12.0`,
  which stores the expanded value in `~/.claude.json`):

  ```json
  {"mcpServers":{"subgraph-registry":{"command":"npx","args":["-y","subgraph-registry-mcp@0.12.0"],"env":{"THE_GRAPH_STUDIO_API_KEY":"${THE_GRAPH_STUDIO_API_KEY}"}}}}
  ```

- **Claude Desktop and other stdio hosts** use the same `mcpServers` shape. If the
  host has no secret/interpolation support, the `env` value is stored as plain
  text in that local config file: only do this on a machine you control, and
  keep the file out of version control.

  ```json
  {"mcpServers":{"subgraph-registry":{"command":"npx","args":["-y","subgraph-registry-mcp@0.12.0"],"env":{"THE_GRAPH_STUDIO_API_KEY":"<your Studio API key>"}}}}
  ```

Direct HTTP, with the key taken from the environment (never inline it):

```bash
curl -sS -X POST "https://gateway.thegraph.com/api/subgraphs/id/<SUBGRAPH_ID>" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $THE_GRAPH_STUDIO_API_KEY" \
  --data '{"query":"{ pools(first: 3) { id } }"}'
```

## Tools

### Discovery (local index, no gateway)

- **search_subgraphs** — Beats official `search_subgraphs_by_keyword`. Filter by domain, network (ethereum/arbitrum/base aliases resolve to mainnet/arbitrum-one/etc.), protocol type, entity, or keyword. Testnets excluded by default. Every hit carries `query_volume_30d`, `reliability_score`, `network`, `age_days`, `maturity`, `example_query`, and both query routes, plus a separate `emerging` list — read `emerging_caveat` before recommending one
- **recommend_subgraph** — Natural language goal like "find DEX trades on Arbitrum" returns the best matching subgraphs
- **get_subgraph_detail** — Full classification, crawled `contract_addresses`, entities, reliability, both query URLs
- **list_registry_stats** — Registry overview with available domains, networks, and protocol types
- **semantic_search_subgraphs** — Embedding-based natural-language search. Uses a bundled ONNX model via `@xenova/transformers`; **if the bundled model is missing it downloads it once from Hugging Face** (see Network & Data Behavior). Skip this tool for a strictly offline runtime.
- **get_schema_changes** — Report schema/entity changes for a subgraph across indexed versions

### Official-name tools (swap-in for graphops/subgraph-mcp)

- **get_schema_by_subgraph_id** / **get_schema_by_deployment_id** / **get_schema_by_ipfs_hash** — Opt-in. Local `registry_schema` with no network when in the corpus; live `__schema` only if a Studio key is set; otherwise `credentials_required` + URLs. Discovery never introspects.
- **execute_query_by_subgraph_id** / **execute_query_by_deployment_id** / **execute_query_by_ipfs_hash** — Opt-in POST to The Graph gateway. Same routing as official (`subgraphs/id` vs `deployments/id`). Without a key: `credentials_required` immediately. Gateway often returns HTTP 200 with a GraphQL error body when auth is missing; `http_status` and `errors` are surfaced honestly. Does not auto-pay x402.
- **execute_query** / **get_schema** — Convenience supersets: one tool that accepts `id` OR `deployment_id` OR `ipfs_hash`.
- **get_top_subgraph_deployments** — `(contract_address, chain)` like official. Official `chain` is `mainnet` (not `ethereum`); we accept both. Ranked by reliability then real volume from crawled manifests, default 3. Substreams gap is reported, not faked.
- **get_deployment_30day_query_counts** — Official name, `ipfs_hashes` in. Returns registry `query_volume_30d` (real). Unknown hashes are `not_in_registry`, never a fake 0. Usually unnecessary — the same number is already on every search hit.

## Query paths

Every discovery result ships with two URLs in `payment_options` (neither is labelled recommended — pick by what you have):

- **`query_url`** — `https://gateway.thegraph.com/api/subgraphs/id/{id}`. POST GraphQL with header `Authorization: Bearer <STUDIO_API_KEY>`. Get a key at [thegraph.com/studio/apikeys](https://thegraph.com/studio/apikeys/). The gateway often returns HTTP 200 with a GraphQL error body when the header is missing — read the body.
- **`query_url_x402`** — `https://gateway.thegraph.com/api/x402/subgraphs/id/{id}`. POST; gateway returns HTTP 402; an x402 client signs **$0.01 USDC on Base**. This server never auto-pays.

Optional next step after discovery: `execute_query_by_subgraph_id` (or `execute_query`) with the `id` and GraphQL, if a Studio key is in env.

## Requirements

- **Runtime:** Node.js 20 is CI-tested (runs via pinned `npx`); install native dependencies for the Node major you actually run
- **Environment variables:** None required for discovery. For opt-in execute / live schema: `THE_GRAPH_STUDIO_API_KEY` (preferred) or `GATEWAY_API_KEY` (official subgraph-MCP name). No private key is in the package.
- **For x402 queries you run yourself:** USDC on Base in the agent's signing wallet (one query ≈ $0.01).

## Install

Pin a known-good version. Audit the source on GitHub before installing if you
plan to ship this in an autonomous-agent runtime.

```bash
# Pin to a published version, do not run unpinned (`npx subgraph-registry-mcp`
# without @VERSION will pull whatever's latest at the moment).
npx subgraph-registry-mcp@0.12.0
```

## Network & Data Behavior

- The `registry.db` (SQLite) is **bundled inside the npm package** — no download and no API key needed for read-only use. (If it's ever missing, e.g. a bare source checkout, the server falls back to downloading it from the [GitHub repository](https://github.com/PaulieB14/subgraph-registry).)
- The downloaded file's SHA-256 is **verified against a hash pinned in the npm package** before loading — see "Verifying the registry" below. A mismatched file is deleted and the server refuses to start.
- Discovery tools (`search_subgraphs`, `recommend_subgraph`, `get_subgraph_detail`, `list_registry_stats`, `get_schema_changes`, `get_top_subgraph_deployments`, `find_by_contract`, `get_deployment_30day_query_counts`) run entirely against the local database — no external API calls at query time.
- **Exception — `semantic_search_subgraphs`:** it loads a bundled ONNX embedding model via `@xenova/transformers`. If that bundled model is not present, the runtime downloads it **once** from Hugging Face (`huggingface.co`), then caches it.
- **Exception — opt-in execute / live schema:** `execute_query*`, `check_subgraph_health`, `query_for_goal` with explicit `validate_schema:true` or `execute:true`, and live `__schema` on `get_schema*` POST to `gateway.thegraph.com` **only when** `THE_GRAPH_STUDIO_API_KEY` (or `GATEWAY_API_KEY`) is set AND the caller invoked that tool. Without a key they return `credentials_required` with both URLs and do not touch the network. Discovery tools never take this path.
- **Optional local HTTP/SSE server:** default transport is **stdio** (no listener). Passing `--http` or `--http-only` starts a local HTTP/SSE server on port 3848 (`MCP_HTTP_PORT` to change), exposing `/messages`, health, and OpenAPI/manifest endpoints. It is off unless you pass those flags — bind only to trusted/firewalled environments.

## Verifying the registry

The npm package version `0.12.0` ships with this expected hash:

```
SHA-256(registry.db) = 672afa2f0d405483af5fb4c403e515fb0f1342c7eeb31968e78a53d5f6ebdd6b
```

This hash is hard-coded in `src/index.js` (`EXPECTED_DB_SHA256`). On every run,
the server checks the cached or freshly-downloaded `registry.db` against it. If
the hashes don't match — which would happen if the GitHub-hosted file were
swapped, or your local cache were tampered with — the server **refuses to load
the database** and exits with an error. The bad file is deleted so the next run
attempts a fresh download.

Verify manually:

```bash
shasum -a 256 ~/.npm/_npx/*/node_modules/subgraph-registry-mcp/data/registry.db
# (path varies by npx cache layout; the file is the one referenced as
# `data/registry.db` inside the package)
```

If you intentionally rebuilt the DB locally (using the optional Python
crawler), the hash will not match. Set `SUBGRAPH_REGISTRY_SKIP_VERIFY=1` to
bypass — never set this in an agent-runtime default config.

When the registry is regenerated, the maintainer bumps the npm version *and*
updates the hash constant atomically — so a given npm version uniquely
corresponds to a known DB.

## Use Cases

- Drop-in for official subgraph-MCP schema/execute/contract tools, with better search
- Discover the right subgraph before querying The Graph — volume is already on the hit, no extra counts call
- Find high-reliability DeFi, NFT, DAO, or governance subgraphs by chain
- Opt-in execute GraphQL when the caller wants data, with a Studio key from env
- Compare subgraphs by reliability score (query fees, volume, curation signal, indexer stake)
