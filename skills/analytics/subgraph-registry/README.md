# Subgraph Registry

<a href="https://glama.ai/mcp/servers/PaulieB14/subgraph-registry">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/PaulieB14/subgraph-registry/badge" />
</a>

Discover published subgraphs on [The Graph Network](https://thegraph.com) by chain, protocol, entity or contract, then prepare a bounded GraphQL starter.

The bundled snapshot contains **15,452 classified subgraph records**. It is not a live directory of every subgraph: Studio-only deployments, dynamic contracts and later updates may be absent. Availability must be checked separately from ranking.

## Start here: agents and MCP users

Share the canonical [SKILL.md](SKILL.md) for the complete agent workflow.

1. **Connect a pinned, published release** (Node 20 is CI-tested):

   ```json
   {"mcpServers":{"subgraph-registry":{"command":"npx","args":["-y","subgraph-registry-mcp@0.12.0"]}}}
   ```

   Inspect `tools/list`: Node 0.12.0 exposes **10 tools without a key**, or **19
   total with a Studio key**. A hosted connector can mount a different subset or
   corpus; installing npm does not update or restart it.
2. **Discover explicitly.** Tool-call parameters below work with published 0.12.0:

   ```json
   {"name":"search_subgraphs","arguments":{"query":"uniswap v3","network":"ethereum","limit":3}}
   ```

   For newer networks, an explicit discovery opt-in can include zero-allocation
   snapshot records without probing them:

   ```json
   {"name":"search_subgraphs","arguments":{"network":"arc","include_unserved":true,"limit":3}}
   ```

   `arc` is mainnet; `arc-testnet` is distinct. Neither missing rewards/curation nor
   zero allocations proves unqueryability. Denied/testnet opt-ins remain separate.
3. **Prepare locally**, if the tool is advertised:

   ```json
   {"name":"query_for_goal","arguments":{"goal":"Uniswap v3 pools on Ethereum","first":2,"execute":false}}
   ```

   Inspect the selected deployment, query, `goal_mapping` and validation labels.
   Releases before 0.12.0 return a stored starter that may not answer the goal;
   older connectors can use recommendation/detail instead.
4. **Bring your own Studio key — set up by a human.** This server never ships or
   shares a key. Studio keys belong to a Studio account managed by a person, so
   agents should hand this step to their operator rather than sign up or mint
   keys. The operator creates a key at [Studio API Keys](https://thegraph.com/studio/apikeys/),
   stores it via the host's secret manager or environment as
   `THE_GRAPH_STUDIO_API_KEY` and restarts the server; never paste it in chat,
   source, tool arguments or logs. [Official pricing](https://thegraph.com/studio-pricing/)
   currently advertises **100,000 free queries/month**; verify the account's plan
   and remaining allowance. It is not a new quota per key; Studio development
   endpoints have separate limits. See [host configuration](#bring-your-own-key-host-configuration).
5. **Execute only when wanted and authorized**, using an advertised execution
   tool and reviewed fields. Bearer format: `Authorization: Bearer <STUDIO_API_KEY>`.
   Read GraphQL `errors` and partial `data` even on HTTP 200. On missing
   credentials/quota, stop and resolve that issue; never silently switch to x402.

### What 0.12.0 adds

**npm/ClawHub 0.12.0** adds goal-specific `query_for_goal` planning (entity
mapping, confidence, `unmet`/`filters_not_applied`, alternatives, optional
`validate_schema`) and human-handoff bring-your-own-key onboarding. It also ships
the discovery fixes merged after 0.11.0: chain-only inference, empty-result
`diagnostics`, strict search validation and structured `next_action` hints. The
bundled registry database is unchanged from 0.11.0. A mounted connector keeps its
own pinned runtime until it is updated. See [the discovery audit](docs/DISCOVERY_AUDIT.md).

## The Problem

Agents querying The Graph need to discover and select the right subgraph before they can query data. Search results include snapshot query volume, classification, entities and starter queries to reduce extra discovery steps. Live schema relevance, health and successful execution still require separate checks when needed.

## What It Does

1. **Builds a snapshot** from active published subgraphs in the configured Graph Network meta-subgraph; it does not enumerate all private/Studio deployments
2. **Attempts to fetch** schema metadata for indexed deployments; missing data remains a coverage limitation
3. **Extracts contract addresses** from each manifest's `dataSources` and `templates` — agents can answer "which subgraph indexes contract 0x… on chain X?"
4. **Stores a starter GraphQL query** from parsed schema metadata where available; it is an example, not a live validation or a goal-specific answer
5. **Classifies** each subgraph by domain, protocol type, canonical entities, and schema family
6. **Scores** reliability using on-chain signals (query fees, volume, curation, stake)
7. **Returns keyed gateway and optional paid x402 routes** — the MCP never signs payments or auto-pays; see the explicit payment-approval warning below
8. **Publishes** as SQLite database + REST API + MCP server + **per-subgraph JSON-LD at `/.well-known/subgraph/{id}.jsonld`** for ecosystem crawlers
9. **Generates** visual dashboards and bot-readable category files (auto-updated with each sync)

---

## Contract lookup, measured freshness, and goal-to-starter workflow

Released in **0.11.0**, the **Node MCP server** (stdio and SSE) implements three complementary tools. Health is advertised only when a Studio key is configured; the other two are keyless preparation/discovery tools.
Existing search/recommend/detail calls remain discovery-only; they never probe or
execute. No crawler/database migration or Python API change is required.

### `find_by_contract(address, chain?, limit=3)`

JavaScript examples use a host-provided `mcp.call(name, args)` adapter. For the
actual MCP SDK `Client.callTool({name, arguments})` flow, see
[`scripts/audit-discovery.mjs`](scripts/audit-discovery.mjs).

```js
await mcp.call("find_by_contract", {
  address: "0x1F98431c8aD98523631AE4a59f267346ea31F984",
  chain: "ethereum", // normalized to mainnet; omit to search all networks
  limit: 3,         // integer 1–20
});
```

Matches exact, case-insensitive EVM addresses from crawled manifests, checking
**each manifest record's network** (falling back to the deployment network).
Ranks allocated, non-denied snapshot deployments by reliability then 30-day
volume; de-duplicates before limiting. `get_top_subgraph_deployments` keeps its
existing `(contract_address, chain)` interface and uses the same implementation.

Results include matched manifest records, starters, and `schema_entities` for the
**whole deployment**. Current registry data does not map a contract to particular
entities/fields, so `coverage.contract_to_entity_mapping` is explicitly null.
Dynamic template instances and substreams may be missing. No match is not proof
that no subgraph indexes the contract; allocation/reliability remain snapshot signals.

### `check_subgraph_health(id | subgraph_id | ipfs_hash | deployment_id)`

Explicitly opts into **one** Studio-key gateway request for:

```graphql
{ _meta { deployment hasIndexingErrors block { number timestamp } } }
```

Known subgraph IDs are pinned to the crawled deployment. Returns `freshness.live`
with measured `observed_at` (Unix seconds), indexed block/timestamp, indexing-error
flag, HTTP status, and one of `serving`, `indexing_errors`, `metadata_unavailable`,
or `query_failed`. A successful metadata query **does not prove chain-head sync**;
`synced_to_chain_head` remains null. Unsupported metadata is unknown, not fabricated.

Search, recommendation, detail, contract results, and JSON-LD manifests expose
cached freshness without making calls. Before a probe, `live` is null. Observations
are process-local (maximum 500), become `stale: true` after 300 seconds, and disappear
on restart. There is no background check or new reliability-score interpretation.
`registry_updated_at` is the upstream metadata update, **not** a crawl/health timestamp.
This credential-only tool is not advertised on keyless servers.

### `query_for_goal(goal, chain?, first?, execute=false, validate_schema=false)`

**Since 0.12.0:** goal-specific planning. Earlier releases return the first
recommendation's stored starter instead.

```js
// Keyless and local: no network call.
const prepared = await mcp.call("query_for_goal", {
  goal: "Uniswap V4 pool IDs on Arc", chain: "arc", first: 3,
});
// prepared.query            -> { _meta {…} pools(first: 3) { id } }
// prepared.goal_mapping     -> entity "Pool", confidence "medium", rationale,
//                              unmet, alternatives
// prepared.onboarding       -> human-handoff key setup (keyless servers only)

// With the operator's own key: one scoped schema check + one query.
const fetched = await mcp.call("query_for_goal", {
  goal: "latest Uniswap v3 swaps on Ethereum in the last 7 days", first: 3,
  validate_schema: true, execute: true,
});
```

How it maps a goal:

1. Parses entity intent (pool IDs, swaps, candles/OHLCV, daily/hourly data,
   positions, liquidations, borrows, mints, tokens, domains…), ordering
   (latest/top), `top N`, 0x addresses and time ranges (`last 7 days`).
2. Scores recommended deployments plus an entity-aware candidate search by
   whether their crawled entity names contain the requested entity, protocol
   text match and recommendation rank, within the inferred chain.
3. **Keyless:** derives the collection with graph-node's pluralisation, selects
   `id` (plus stored-starter fields only when the starter targets the same
   entity), and filters by `id` when an address names that entity. Anything
   that needs field types (ordering, time filters, relation filters, aggregation
   intervals) goes into `goal_mapping.unmet` instead of being guessed.
   Confidence is at most `medium` and `validation.live_schema` is `not_checked`.
4. **`validate_schema:true` with a key:** one aliased introspection request
   scoped to the chosen entity (`Query` fields, entity fields, `_orderBy`,
   `_filter`, aggregation intervals). Fields, `orderBy`, `where` and required
   arguments are emitted only if present; confidence becomes `high`. Address
   context maps to relation filters (`owned by` → `owner`, `token` →
   `token0` OR `token1` when the schema has `or`). If a requested address or
   time filter cannot be applied, it is listed in
   `goal_mapping.filters_not_applied` and execution is skipped
   (`requested_filter_not_applied`) rather than returning unfiltered rows. Probe
   errors (including auth/quota bodies on HTTP 200) mark validation `failed`,
   return `query:null` and block execution.
5. **No confident mapping** returns `query:null`, `confidence` `low`/`none`, and
   ranked `alternatives`. Matching deployments hidden by default filters appear
   in `hidden_candidates`; `include_denied` / `include_unserved` opt them in
   (neither denied rewards nor zero allocations proves a deployment is
   unqueryable). Goals with no entity intent keep the stored starter, labelled
   `confidence: "generic_starter"`.

Rows are 1–10 (`first` defaults to a number in the goal or 5); selections are
flat scalars plus single relations as `{ id }`. Mutations, variables, fragments
and nested lists are never generated. `execute` defaults to false and needs an
explicit call **and** `THE_GRAPH_STUDIO_API_KEY`; keyless execution returns
`credentials_required`, the unsigned request and `onboarding`. Gateway success is
reported separately: GraphQL/auth errors (even HTTP 200), partial data,
malformed responses and transport failures never become a success claim. No
retries, fallbacks, arbitrary endpoints or x402 payments.

With a key configured, preparation results include
`next_action.execute_call` (the same goal with `validate_schema` and `execute`
set) so the explicit next step is one call away. Without a key, `onboarding`
contains `relay_to_human` (a short message for the agent's operator), steps,
a placeholder-only MCP config and a `curl` command that reads
`$THE_GRAPH_STUDIO_API_KEY` from the environment. Tool output never contains
the key.

### Bring your own key: host configuration

The server reads the key only from its process environment
(`THE_GRAPH_STUDIO_API_KEY`, or `GATEWAY_API_KEY`). Prefer interpolation or a
secret manager over a literal value in a config file, never commit a key, and
restart the server afterwards: `tools/list` grows from 10 to 19 tools.

Cursor (`~/.cursor/mcp.json` or `.cursor/mcp.json`; `${env:NAME}` resolves from
the environment Cursor was started with):

```json
{"mcpServers":{"subgraph-registry":{"command":"npx","args":["-y","subgraph-registry-mcp@0.12.0"],"env":{"THE_GRAPH_STUDIO_API_KEY":"${env:THE_GRAPH_STUDIO_API_KEY}"}}}}
```

Claude Code (`.mcp.json` supports `${VAR}` expansion):

```json
{"mcpServers":{"subgraph-registry":{"command":"npx","args":["-y","subgraph-registry-mcp@0.12.0"],"env":{"THE_GRAPH_STUDIO_API_KEY":"${THE_GRAPH_STUDIO_API_KEY}"}}}}
```

Claude Desktop and other stdio hosts use the same `mcpServers` shape. Without
interpolation, the `env` value is plain text in that local file — use it only on
a machine you control and keep the file out of version control:

```json
{"mcpServers":{"subgraph-registry":{"command":"npx","args":["-y","subgraph-registry-mcp@0.12.0"],"env":{"THE_GRAPH_STUDIO_API_KEY":"<your Studio API key>"}}}}
```

Goal-specific planning requires 0.12.0 or later.

---

## Agent usability and discovery diagnostics

The canonical shareable agent guide is [SKILL.md](SKILL.md): pinned installation,
capability discovery, chain/protocol lookup, human-assisted Studio key setup,
bounded preparation, opt-in execution and error handling. See the reproducible
[discovery audit](docs/DISCOVERY_AUDIT.md) for measured results against the
earlier 0.11.0 package.

Search recognizes a standalone known chain/alias (for example `query:"arc"`) as
a network filter and returns `inferred_network`; an explicit `network` always
wins. Use `network:"arc"` for mainnet and `network:"arc-testnet"` for testnet.
Empty searches explain matching snapshot records and overlapping exclusions in
`diagnostics`. Default allocation/denied/testnet filters remain unchanged;
`include_unserved:true` deliberately includes zero-allocation records for discovery.

**Rewards, curation and queryability are not interchangeable.** A chain can be
live and queried before rewards or curation signaling is enabled. Zero
allocations is not proof of unavailable queries, and positive allocations is not
a live health check. Reward denial is not proof of spam or query failure.
Reliability is a traction-weighted ranking input, not a measured uptime or
reward-eligibility score. Unknown health remains unknown; no discovery probe is
performed. The published-network corpus cannot include all Studio-only deployments.

Search/recommend/goal responses provide a structured `next_action`: reuse a
configured key (not assumed valid), or have a human create one at
[Studio API Keys](https://thegraph.com/studio/apikeys/), then store it in the MCP
host's secret manager as `THE_GRAPH_STUDIO_API_KEY`. Never paste it in chat or
logs. [Official Studio pricing](https://thegraph.com/studio-pricing/) currently
advertises **100,000 free monthly queries**; check the account's remaining quota
and plan, not a fictitious per-key allowance. Studio development endpoints have
separate limits. These hints never create a key, execute GraphQL, or auto-pay.

Search `limit` is an integer 1–100 (semantic: 1–50); booleans must be JSON
booleans. Unsupported offset/cursor arguments are rejected, not silently ignored.
`total` remains the number returned, not a total-match or pagination promise.

## Querying with x402 (no API key)

Discovery hits include `query_url_x402` alongside the keyed `query_url`. The returned pricing manifest advertises **$0.01 USDC on Base** per query; a separate external client must validate the gateway's actual payment request and obtain approval before signing. No wallet is needed for discovery or the keyed route.

**Financial capability warning:** this optional external client signs a USDC
payment authorization and may retry automatically. It is not the registry server.
Use it only after explicit owner approval of the payment/amount and review of
the signing client and query. Never fall back to payment on auth/quota failure.
The example is disabled by default; the keyed Studio route above needs no wallet.

```js
// Requires a separately configured, reviewed external x402 client.
const ownerApprovedPaidQuery = false; // set only after explicit payment approval
if (!ownerApprovedPaidQuery) throw new Error("Payment approval required");
// Optional paid example, not an automatic discovery-to-payment path.
const { recommendations } = await mcp.call("recommend_subgraph", {
  goal: "find DEX trades on Arbitrum",
});
const top = recommendations[0];
if (!top?.example_query) throw new Error("No starter; inspect schema first");
// Inspect the starter against schema and goal before signing any payment.

// POST your GraphQL query. The first call returns HTTP 402 with a
// base64 `payment-required` header; the x402 client signs the
// EIP-3009 USDC transfer on Base and retries automatically.
const data = await x402Fetch(top.query_url_x402, {
  method: "POST",
  body: JSON.stringify({ query: top.example_query }),
});
```

Pricing manifest returned per subgraph:

```json
{
  "amount_usd": 0.01,
  "asset": "USDC",
  "asset_contract": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "chain": "base",
  "network": "eip155:8453",
  "pay_to": "0x79DC34E41B2b591078d3dE222C43EcaaBD52FcCB",
  "scheme": "exact",
  "asset_transfer_method": "eip3009"
}
```

Client libraries: [`@graphprotocol/client-x402`](https://www.npmjs.com/package/@graphprotocol/client-x402), `x402-fetch`, or any generic x402 wrapper.

---

## Registry at a Glance

<p align="center">
  <img src="docs/charts/domains.svg" alt="Subgraphs by Domain" width="480"/>
</p>

<p align="center">
  <img src="docs/charts/networks.svg" alt="Subgraphs by Network" width="600"/>
</p>

<p align="center">
  <img src="docs/charts/protocol-types.svg" alt="Subgraphs by Protocol Type" width="600"/>
</p>

<p align="center">
  <img src="docs/charts/reliability-dist.svg" alt="Reliability Distribution" width="480"/>
</p>

> Generated charts/category files retain their own snapshot dates and may lag the bundled database. They are not live serving metrics. The counts below were read from the bundled 0.11.0 database; use `list_registry_stats` to inspect the connected runtime. See [`python/generate_docs.py`](python/generate_docs.py).

---

## Browse by Category

### Domains

Explore subgraphs by use case — each file lists the top 25 subgraphs ranked by reliability score.

| Domain | Count | File |
|--------|-------|------|
| [DeFi](docs/domains/defi.md) | 7,927 | Swaps, pools, lending, vaults, yield |
| [NFTs](docs/domains/nfts.md) | 1,611 | Collections, marketplaces, sales |
| Unclassified | 1,325 | Not confidently classified |
| [Infrastructure](docs/domains/infrastructure.md) | 1,255 | Indexers, oracles, registries |
| [Identity](docs/domains/identity.md) | 1,065 | ENS, name services, resolvers |
| [Analytics](docs/domains/analytics.md) | 755 | Snapshots, metrics, historical data |
| [DAO](docs/domains/dao.md) | 762 | Governance, proposals, voting |
| [Gaming](docs/domains/gaming.md) | 594 | Players, quests, items, worlds |
| [Social](docs/domains/social.md) | 158 | Profiles, posts, follows |

Full index: [`docs/DOMAINS.md`](docs/DOMAINS.md)

### Networks

Explore subgraphs by blockchain — each file lists the top 25 subgraphs on that chain.

| Network | Count | File |
|---------|-------|------|
| [Ethereum](docs/networks/mainnet.md) | 2,502 | Ethereum mainnet |
| [Base](docs/networks/base.md) | 1,855 | Base mainnet |
| [BSC](docs/networks/bsc.md) | 1,709 | BNB Chain |
| [Arbitrum](docs/networks/arbitrum-one.md) | 1,456 | Arbitrum One |
| [Polygon](docs/networks/matic.md) | 1,314 | Polygon PoS |
| [Optimism](docs/networks/optimism.md) | 587 | OP Stack L2 |
| [Avalanche](docs/networks/avalanche.md) | 456 | C-Chain |

Full index: [`docs/NETWORKS.md`](docs/NETWORKS.md)

### Protocol Types

| Type | Count | Description |
|------|-------|-------------|
| DEX | 4,444 | Uniswap, Sushi, Curve, Balancer, PancakeSwap |
| Lending | 1,494 | Aave, Compound, Morpho, Spark, Silo |
| Staking | 928 | Lido, Rocket Pool, EigenLayer, Graph Network |
| Bridge | 839 | Hop, Stargate, Across, Wormhole, LayerZero |
| NFT Marketplace | 454 | OpenSea, Blur, Rarible, Foundation |
| Yield Aggregator | 431 | Yearn, Beefy, Harvest, Convex |
| Governance | 425 | Snapshot, Tally, Compound Governor |
| Perpetuals | 276 | GMX, Gains, dYdX, Hyperliquid |
| Name Service | 232 | ENS, Space ID, Unstoppable Domains |
| Options | 196 | Premia, Dopex, Lyra, Hegic |

---

## Reliability Score

Each subgraph gets a composite reliability score (0-1) based on four on-chain signals:

| Signal | Weight | What it measures |
|--------|--------|------------------|
| **Query Fees** | 30% | GRT fees earned from actual usage |
| **Query Volume** | 30% | 30-day query count |
| **Curation Signal** | 20% | GRT tokens curated by the community |
| **Indexer Allocation** | 20% | GRT allocated to this subgraph by indexers |

All values are log-scaled and capped at 1.0. A 0.5 penalty is applied when the snapshot records denied indexing rewards. This does not establish deprecation, safety, reward eligibility for a whole chain, or query availability.

Higher scores mean larger combined ranking inputs, not calibrated confidence. No score establishes functionality, safety, testnet status, rewards eligibility or current query availability.

### Traction-weighted ranking can favor older deployments

Lifetime fees accumulate, curation/stake are snapshots, and 30-day volume is a
rolling window (it does not require waiting 30 days to register traffic). Older
deployments can have a ranking advantage; this is not an uptime or quality test.
For context, a historical 2026-08-25 snapshot with positive allocations and no
denied rewards showed:

| Age | Count | Avg reliability |
|-----|-------|-----------------|
| < 30 days | 64 | 0.107 |
| 30–90 days | 227 | 0.143 |
| 90–365 days | 1,100 | 0.225 |
| > 1 year | 4,034 | 0.313 |

These are dated observations, not current corpus or health measurements. The
runtime caveat deliberately avoids frozen claims about the youngest top-ranked
entry. New networks may serve traffic before rewards or curation are enabled.

Rather than reweight the score and trade a measurable signal for a guess,
`search_subgraphs` returns young matches in a **separate `emerging` list**
alongside an `emerging_caveat` explaining that a low score at that age is
expected rather than damning. Every result also carries `age_days` and
`maturity` (`new` < 30d, `emerging` < 90d, `established`). This matters most
for new chains and new protocols, where no mature deployment *can* exist —
newer matching deployments can appear separately without being mislabelled as
bad or unavailable merely because their traction score is lower.

`semantic_search_subgraphs` combines cosine similarity with the reliability
weight below. It is **not age-neutral**: traction can influence the order. It
carries maturity labels but no separate `emerging` list; relevance still needs
review, and neither semantic score nor age establishes health.

### Ranking

Three tools rank, and each ranks differently on purpose:

- **`search_subgraphs`** — re-ranks candidates using word boundaries and exact
  distinctive-name preference, then reliability (0.12.0 adds the exact-name boost
  and standalone-chain inference). OR-ing the terms and ordering on reliability alone meant a
  popular subgraph matching one incidental word beat a precise match on all
  three, so being *more* specific returned worse answers. Version tokens
  (`v2`, `v3`, `v4`) are kept rather than dropped as too short.
- **`semantic_search_subgraphs`** — orders by `semantic_score × (0.5 + 0.5 ×
  reliability)`. Pure cosine put testnets first, since their text is nearly
  identical to mainnet's. The 0.5 floor keeps new subgraphs competitive.
- **`recommend_subgraph`** — infers domain and protocol type from the goal, but
  as a *ranking bonus*, never a filter. As a filter, one bad keyword collapsed
  the candidate pool to nothing.

A term matching a subgraph's **name** counts for more than one matching its
description — `%ens%` also matches "tok**ens**", so equal weighting handed a
search for `ens` to four Uniswap subgraphs.

Chain names are aliased, so `ethereum`, `arbitrum`, `polygon` and `bnb` resolve
to the corpus values `mainnet`, `arbitrum-one`, `matic` and `bsc`.

### Testnets

Testnet deployments can resemble mainnet twins and compete for the top slot.
In keyword/semantic search they are
**excluded by default** and every result carries `testnet: true|false`. Pass
`include_testnets: true` to see them — and an explicit request for a testnet
network (`network: "sepolia"`) always wins over the default, so that still
returns exactly what you asked for.

## Using the registry from payql

The optional `payql@0.1.5` pin below prevents floating installs; it is not an audit
or a safety endorsement of that external package. Review it before running, and
require explicit approval before enabling any funded payment/signing path.

[`payql`](https://www.npmjs.com/package/payql) can use this registry as its
free discovery source instead of paying for a network-subgraph query. Run the
registry's HTTP transport and point payql at it:

```bash
npx subgraph-registry-mcp@0.12.0 --http-only          # serves :3848
PAYQL_REGISTRY_URL=http://127.0.0.1:3848/graphql npx -y payql@0.1.5
```

`POST /graphql` answers in the Graph network subgraph's `subgraphMetadataSearch`
shape, which is what payql already parses — so this needs no change on payql's
side, and discovery becomes free and locally-ranked.

### Denied deployments

Curation-denied deployments (`deniedAt > 0` — denied indexing rewards, not proof
of spam, deprecation or query failure) are **excluded by default** from
`search_subgraphs`, `semantic_search_subgraphs` and `recommend_subgraph`. Pass
`include_denied: true` to the two search tools to see them; every result then
carries `denied: true|false` so the choice stays visible.

---

## MCP Server

The registry is available as an MCP server with **dual transport** — stdio for local clients and SSE/HTTP for remote agents.

The Node server provides official-name schema, execute, contract-lookup and
30-day-count aliases for clients using [graphops/subgraph-mcp](https://github.com/graphops/subgraph-mcp).
Its discovery names are `search_subgraphs`, `recommend_subgraph` and
`semantic_search_subgraphs`. Interchangeability is not a guarantee of identical
ranking, corpus coverage or every remote connector capability.

Every search/recommend hit carries the snapshot's `query_volume_30d`, so a
separate registry counts call is usually unnecessary. It is historical demand,
not current serving health; no live volume measurement is performed by discovery.

> The shipped server is the Node implementation in [`src/index.js`](src/index.js); that's what `npx subgraph-registry-mcp` runs and what's published to npm. A Python equivalent in [`python/mcp_server.py`](python/mcp_server.py) is kept for local development against the same SQLite database — bug fixes and new tools should land in the Node version first.

**Ten keyless discovery/preparation tools** (inspect `tools/list` on your actual host; no automatic GraphQL execution or live schema introspection):
- **search_subgraphs** — filter by domain, network, protocol type, entity, or keyword. Ranked by matched terms, reliability and real `query_volume_30d`.
- **recommend_subgraph** — natural language goal to best subgraphs (includes `schema_stable_days`)
- **semantic_search_subgraphs** — vector-similarity search over precomputed embeddings (sentence-transformers/all-MiniLM-L6-v2, 384-dim). Use for fuzzy/paraphrased goals where literal keyword match would miss.
- **get_subgraph_detail** — full classification for a specific subgraph (includes `schema_changed_at` and crawled `contract_addresses`)
- **list_registry_stats** — registry overview (domains, networks, counts)
- **get_schema_changes** — chronological fingerprint history. Fingerprints use entity names/field counts, not a full semantic schema diff.
- **find_by_contract** and **get_top_subgraph_deployments** — exact manifest-address discovery, not live contract-to-entity validation
- **get_deployment_30day_query_counts** — snapshot volumes for known IDs/hashes, not a live volume probe
- **query_for_goal** — goal-to-query planning (0.12.0+) with rationale/confidence; keyless by default; `validate_schema` / `execute` are separately credential-gated

**Nine additional keyed tools** (19 total). Caller must invoke them; discovery never auto-queries:
- **execute_query_by_subgraph_id** / **execute_query_by_deployment_id** / **execute_query_by_ipfs_hash** — POST GraphQL to The Graph gateway. Same routing as official (`subgraphs/id` vs `deployments/id`). Requires `THE_GRAPH_STUDIO_API_KEY` (or `GATEWAY_API_KEY`). Without a key, returns `{error: credentials_required, query_url, query_url_x402, hint}` immediately — no hang, no x402 auto-pay. Convenience superset: **execute_query** accepts `id` OR `deployment_id` OR `ipfs_hash`.
- **get_schema_by_subgraph_id** / **get_schema_by_deployment_id** / **get_schema_by_ipfs_hash** — local `registry_schema` (entities, example_query, fingerprint) with no network when the subgraph is in the corpus; live `__schema` introspection only when a Studio key is set. Convenience superset: **get_schema**.
- **check_subgraph_health** — one fixed, opt-in `_meta` request; cache evidence does not prove chain-head sync.

Set `THE_GRAPH_STUDIO_API_KEY` via the MCP host's secret manager to enable execute/live-schema/health. No private key is bundled. The keyed gateway often returns HTTP 200 with a GraphQL error body when auth is missing — `execute_query` surfaces `http_status` and `errors` honestly.

### Install

Node 20 is CI-tested. Pin a reviewed release rather than floating to latest.

Claude Code:

```bash
claude mcp add subgraph-registry -- npx subgraph-registry-mcp@0.12.0
```

A JSON MCP host configuration (keyless discovery):

```json
{
  "mcpServers": {
    "subgraph-registry": {
      "command": "npx",
      "args": ["subgraph-registry-mcp@0.12.0"]
    }
  }
}
```

For a trusted local HTTP/SSE client:

```bash
npx subgraph-registry-mcp@0.12.0 --http-only
# Connect to http://localhost:3848/sse; keep the listener firewalled/trusted.
```

The npm package bundles the SQLite registry and offline model. The server downloads the registry from GitHub only if the bundled file is missing, and verifies its pinned hash. The example configuration is keyless; see [host configuration](#bring-your-own-key-host-configuration) to add your own Studio key for opt-in execution.

---

## Well-Known JSON-LD Manifest

Stable, machine-readable per-subgraph manifest that other crawlers and agent frameworks can index without going through MCP. Served by the Node MCP HTTP transport:

```
GET /.well-known/subgraph/{id}.jsonld     Full per-subgraph manifest (JSON-LD)
GET /subgraphs/{id}.jsonld                 Alias (same payload)
GET /.well-known/subgraph-index.jsonld     Discovery list — top 100 by reliability with @id links
```

Each manifest includes classification, parsed entities, contract addresses (from the indexed `dataSources`), endpoints (x402 + API-key), a per-subgraph starter query generated from the actual schema, pricing, and metadata. The `@context` + `@type` make the shape auto-discoverable.

```bash
# Start the HTTP transport
npx subgraph-registry-mcp@0.12.0 --http-only

# Fetch the manifest for Uniswap V3 Mainnet
curl http://localhost:3848/.well-known/subgraph/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV.jsonld
```

---

## Semantic Search

Indexed deployments with embeddings have a precomputed 384-dim vector from `sentence-transformers/all-MiniLM-L6-v2`, built from its display name, description, canonical entities, top schema entity names, and protocol metadata. At MCP-tool-call time the Node server embeds the query string with the same model (via [@xenova/transformers](https://github.com/xenova/transformers.js), quantized ONNX bundled in the npm package — no first-call download) and ranks by cosine similarity weighted by snapshot reliability, as described above.

```js
const { subgraphs } = await mcp.call("semantic_search_subgraphs", {
  query: "lending positions near liquidation on a Layer 2",
  limit: 5,
});
// semantic_score is raw cosine similarity, not calibrated confidence or live health.
```

Use it when:
- The goal is paraphrased or use-case-shaped (`search_subgraphs` is keyword-only).
- You're exploring "what data exists for X?" rather than fetching a specific protocol's subgraph.

Python crawl-time (`fastembed`) and JS runtime (`@xenova/transformers`) use the
same model architecture. Float32 versus quantized ONNX inference is **not
bitwise-identical**, and scores/rankings can differ. If the bundled model is
missing, the runtime can download from Hugging Face; a normal published package
bundles it. Do not invoke semantic search in a strictly offline checkout without
confirming the model files exist.

Embeddings and the model increase package size; inspect the actual tarball rather
than treating historical size estimates as a current download guarantee.

---

## Schema Evolution

Each crawl computes a `schema_fingerprint` (MD5 of sorted `entity:field_count` pairs) per subgraph. Whenever the fingerprint changes from the previous sync, an immutable row is written to `schema_history`. The table is append-only and survives full DB rebuilds.

Illustrative output shape below; the sample counts/timestamps are not live measurements.

```js
const history = await mcp.call("get_schema_changes", {
  subgraph_id: "5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV",
});
// {
//   total_changes: 3,
//   stable_days: 47.2,
//   changed_within_24h: false,
//   changed_within_7d: false,
//   changes: [
//     { fingerprint: "abc123...", prev_fingerprint: "def456...", detected_at: 1717... },
//     ...
//   ]
// }
```

`recommend_subgraph` and `get_subgraph_detail` results now also include `schema_changed_at` (unix seconds of last detected change) and `schema_stable_days` so agents can prefer subgraphs whose data contract has been stable longer — useful when a query needs to keep working across the agent's planning horizon.

---

## OpenAPI

The full API surface (MCP tools + REST routes) is published as OpenAPI 3.1:

- `openapi.yaml` — checked-in generated specification
- `data/openapi.json` — bundled with the npm tarball
- `GET /.well-known/openapi.json` — served by the HTTP transport for live discovery

The spec is regenerated on every release from the declarative `TOOLS[]` + `REST_ROUTES[]` exports in [`src/index.js`](src/index.js) via [`scripts/gen-openapi.js`](scripts/gen-openapi.js). CI fails any PR that touches `src/index.js` without regenerating the spec.

---

## Python REST API (separate local-development service)

These routes belong to `python/server.py` on port 3847, not the Node MCP
HTTP transport on 3848. The new Node discovery diagnostics/validation are not
implemented here; for example this Python API has its own offset pagination.

```
GET /summary                    Registry overview and stats
GET /domains                    Domain breakdown
GET /networks                   Network breakdown
GET /families                   Schema family groups (fork/clone detection)
GET /subgraphs                  Filter subgraphs
GET /subgraphs/{id}             Full detail for one subgraph (now includes contract_addresses and example_query)
GET /search?q=uniswap           Free-text search
GET /recommend?goal=...&chain=  Agent-optimized recommendation
```

```bash
# Start API server
cd python && python server.py

# Example: find DEX subgraphs on Arbitrum
curl "http://localhost:3847/recommend?goal=query+DEX+trades+on+Arbitrum&chain=arbitrum-one"

# Example: filter by entity type
curl "http://localhost:3847/subgraphs?entity=liquidity_pool&network=base&min_reliability=0.5"
```

---

## Bot-Readable Category Files

The `docs/` directory contains structured `.md` files with YAML frontmatter designed for AI agents and bots to consume:

```
docs/
├── DOMAINS.md           # Index of all domains with counts
├── NETWORKS.md          # Index of all networks with counts
├── charts/              # Auto-generated SVG visualizations
│   ├── domains.svg
│   ├── networks.svg
│   ├── protocol-types.svg
│   └── reliability.svg
├── domains/             # One file per domain
│   ├── defi.md          # Top 25 DeFi subgraphs by reliability
│   ├── nfts.md
│   ├── dao.md
│   └── ...
└── networks/            # One file per network
    ├── mainnet.md       # Top 25 Ethereum subgraphs by reliability
    ├── base.md
    ├── arbitrum-one.md
    └── ...
```

Each category file includes:
- YAML frontmatter (domain/network, count, percentage, last updated)
- Top 25 subgraphs ranked by reliability score
- MCP tool and REST API query examples

---

## Architecture

```
Configured Graph Network meta-subgraph (published-network metadata)
    |
    v
crawler.py ---- async httpx, ID-based cursor pagination
    |
    v
classifier.py - rule-based domain/protocol classification + schema fingerprinting
    |
    v
registry.py --- builds SQLite + indices
    |
    ├── server.py ------ FastAPI REST API (:3847)
    ├── generate_docs.py SVG charts + category .md files
    └── scheduler.py --- weekly incremental sync

MCP Server (src/index.js, published to npm)
    ├── stdio   ←── Claude Desktop / Claude Code
    └── SSE     ←── OpenClaw / remote agents (:3848)

python/mcp_server.py — local-dev MCP server hitting the same SQLite DB
```

## Maintainer-only: optional data rebuilds and publication

Normal agent use runs the bundled snapshot; **do not crawl to install or query**.
The Python crawler/rebuild workflow is separate maintenance: it can make network
requests, consume gateway allowance, rewrite the database and publish updates.
Only run it with explicit authorization, suitable credentials and a query budget.
Keep real credentials in a secret manager; do not paste them into shell history
or commit a `.env` file. After an intentional rebuild, synchronize the pinned
hash, package/skill metadata and reviewed release artifacts; do not disable hash
verification to distribute a changed database.

Inspect maintenance options without starting a crawl:

```bash
cd python
python registry.py --help
```

The [update workflow](.github/workflows/update-registry.yml) currently schedules
incremental maintenance with a five-day day-of-month cron step and a monthly
full refresh. It also supports manual dispatch; this is not proof a
particular connected runtime received an update. Generated category files/charts
can have different snapshot dates. The standalone Python scheduler's default
weekly loop is separate from the GitHub Actions schedule.

For publication without a crawl or data rebuild, use the
[publish-only release guide](docs/RELEASING.md). Its main-only manual workflow uses
repository secrets and does not write main. Neither this README update nor
merging these fixes publishes a new npm/ClawHub version.

## License

MIT
