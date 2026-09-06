---
name: query-chain
description: >-
  Guides finding the best way to query Cardano blockchain data. Triggers: "query chain", "read UTxOs", "fetch blockchain data", "Blockfrost vs Ogmios", "chain indexer", "query Cardano", "get transaction data", "read on-chain state", "query chain from Go".
allowed-tools: Read Grep Glob
disallowed-tools: Bash Edit Write WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Query Cardano Chain Data

Help the developer choose and use the right data provider for querying the Cardano blockchain.

## When to use

- Developer needs to read UTxOs, transaction history, protocol parameters, or on-chain state
- Choosing between Blockfrost, Ogmios, Kupo, Koios, Cardano GraphQL, DB-Sync, or Oura
- Setting up a data pipeline from chain data
- Querying datum or script information attached to UTxOs
- Building a backend service that needs chain data
- Comparing hosted vs self-hosted infrastructure options

## When NOT to use

- Building or submitting transactions (use transaction-building skills instead)
- Setting up a local devnet (use `setup-devnet` skill)
- Writing smart contracts (use Aiken/Plutus skills)
- Wallet integration in a frontend (use `connect-wallet` skill)

## Key principles

1. **Match the provider to the use case.** There is no single best provider. A dApp frontend has different needs than a data pipeline.
2. **Hosted APIs are faster to start; self-hosted gives control.** Blockfrost and Koios are hosted. Ogmios, Kupo, DB-Sync require running infrastructure.
3. **Combine providers when needed.** Ogmios + Kupo is a common pairing: Ogmios for tx submission and protocol params, Kupo for UTxO queries.
4. **Consider cost at scale.** Hosted APIs have rate limits and pricing tiers. Self-hosted has infrastructure cost.
5. **Think about latency requirements.** WebSocket (Ogmios) is lower latency than REST (Blockfrost). Local node queries are fastest.

## Workflow

### Step 1: Identify the context

Ask the developer (if not already clear):

- **What are you building?** (backend-service | dapp-frontend | data-pipeline | one-off-query)
- **Do you need real-time chain-tip data or historical queries?**
- **Are you running your own Cardano node?**
- **What language/SDK are you using?**

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/ogmios/` - Ogmios WebSocket bridge docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/blockfrost-openapi/` - Blockfrost API docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/koios/` - Koios API docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-graphql/` - Cardano GraphQL docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/db-sync/` - DB-Sync docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/yaci-store/` - Yaci Store (modular JVM indexer; see `stores/`, `plugins/`, `usage/as-library/`)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/` - Evolution SDK docs (TypeScript client; see `providers/` and `querying/`)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/blockfrost-go/` - Blockfrost Go client (typed endpoint wrappers)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/utxorpc-go-sdk/` - UTxORPC Go SDK (provider-agnostic gRPC)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/gouroboros/` - gOuroboros (direct node mini-protocols)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/dingo/` - Dingo (Go node serving UTxORPC / Blockfrost-compatible / Mesh)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/adder/` - Adder (Go event pipeline; `docs/swagger.yaml` for its REST surface)

### Step 3: Evaluate providers for the context

Search the reference file for detailed provider comparisons.

```
File: skills/query-chain/references/provider-comparison.md
```

#### Quick decision guide

| Context | Recommended Primary | Alternative |
|---|---|---|
| **backend-service** | Ogmios + Kupo (self-hosted) or Blockfrost (hosted) | Koios (hosted, free tier) |
| **dapp-frontend** | Blockfrost (via SDK) or Koios | Ogmios via backend proxy |
| **data-pipeline** | Oura or Adder (streaming) or DB-Sync (SQL) | Cardano GraphQL |
| **one-off-query** | Koios (free, no signup) or Blockfrost | cardano-cli with local node |

### Step 4: Describe each viable option

For each provider that fits the developer's context, explain:

1. **How to set it up** -- installation, configuration, API keys
2. **How to make the query** -- specific API calls, endpoints, or queries
3. **Code example** -- using their SDK/language of choice
4. **Limitations** -- rate limits, missing data, latency

### Step 5: Provider-specific guidance

#### Blockfrost (Hosted REST API)

- Sign up at blockfrost.io for a project ID
- REST API with comprehensive endpoints
- SDKs: JavaScript, Python, Rust, Go, Java, Kotlin, Swift, Elixir
- Rate limits: free tier 50k requests/day, 10 req/s sustained, 500 req burst capacity
- Great for: quick prototyping, frontend dApps, moderate traffic backends

```
GET /addresses/{address}/utxos
GET /txs/{hash}
GET /epochs/latest/parameters
```

#### Ogmios (Self-hosted WebSocket)

- Requires a running cardano-node
- WebSocket JSON-RPC protocol (low latency)
- Local state queries: UTxOs, protocol parameters, chain tip
- Transaction submission and evaluation
- Best for: backends co-located with a node, tx submission workflows

#### Kupo (Self-hosted HTTP indexer)

- Indexes UTxOs by address, asset, or datum hash
- Lightweight, fast, pattern-based matching
- REST API on top of indexed data
- Often paired with Ogmios for a complete solution
- Best for: UTxO lookups, datum resolution, asset queries

#### Koios (Hosted REST API, community-run)

- Free tier with generous limits
- No API key required for basic use
- Comprehensive endpoints similar to Blockfrost
- Community-maintained, decentralized backend nodes
- Best for: open-source projects, quick queries, no-signup needs

#### Dingo (Self-hosted node with APIs built in)

A Cardano node implementation in Go that serves the query layer itself, so one
process replaces the usual node-plus-Ogmios-plus-Kupo stack:

- UTxO RPC (default port `9090`), a Blockfrost-compatible REST API (`3000`), and
  Mesh / Coinbase Rosetta (`8080`), each enabled and bound through
  `DINGO_PLUGINS_API_*_CONFIG_PORT`
- Because the REST API is Blockfrost-compatible, existing Blockfrost client code
  and the mirrored Blockfrost OpenAPI spec both apply — point the client at your
  own host instead of the hosted service
- **Storage mode is the gotcha.** The client-facing APIs require
  `storageMode: "api"` (full indexing). The lighter `"core"` mode carries only
  what consensus needs and will not serve them.
- Its own README states Dingo is pre-production: testnets and devnets only, not
  mainnet with real funds. Treat it as a development and testnet query layer,
  and keep Blockfrost, Koios, or Ogmios + Kupo for anything mainnet-facing.

#### Cardano GraphQL (Self-hosted GraphQL)

- GraphQL interface over cardano-db-sync
- Flexible queries with relationships
- Requires DB-Sync + PostgreSQL + Hasura
- Best for: complex relational queries, custom data views

#### DB-Sync (Self-hosted PostgreSQL)

- Full blockchain data in PostgreSQL
- Direct SQL access to all chain data
- Heavy resource requirements (100GB+ disk, significant RAM)
- Best for: analytics, complex historical queries, data warehousing

#### Oura (Self-hosted pipeline)

- Event-driven pipeline from cardano-node
- Outputs to Kafka, Elasticsearch, webhooks, files
- Filters and maps chain events
- Best for: real-time event processing, data pipelines, notifications

#### Adder (Self-hosted pipeline, Go)

- Same shape as Oura in a Go process: an input stage follows the chain, filters
  narrow the stream, output stages emit it
- Inputs are chainsync (over NtC or NtN), mempool, and UTxORPC, so it can follow
  a node directly or ride on a UTxORPC provider; the chainsync input emits
  `input.block`, `input.rollback`, `input.transaction`, and `input.governance`,
  each with its own payload
- Outputs include webhook, push, notify, log, and Telegram
- Filters narrow by event type, address, asset fingerprint, minting policy, pool
  ID, or DRep ID (`WithTypes`, `WithAddresses`, `WithAssetFingerprints`,
  `WithPolicies`, `WithPoolIds`, `WithDRepIds`)
- Runs standalone or embeds as a library, which is the reason to pick it over
  Oura: a Go service can consume the event stream in-process instead of
  shipping it through a broker first
- Best for: Go backends reacting to chain events, webhook fan-out, alerting

#### Evolution SDK (TypeScript client over providers)

Not a provider — a TypeScript library that wraps Blockfrost, Kupmios, Maestro, and Koios behind one query interface, so the provider becomes a config choice rather than a code rewrite. For read-only work, build a **provider-only client** (no wallet attached):

```typescript
import { Address, Client, preprod } from "@evolution-sdk/evolution"

const client = Client.make(preprod).withBlockfrost({
  baseUrl: "https://cardano-preprod.blockfrost.io/api/v0",
  projectId: process.env.BLOCKFROST_PROJECT_ID!,
}) // or .withKupmios(...) / .withMaestro(...) / .withKoios(...) — same query API

const utxos   = await client.getUtxos(Address.fromBech32("addr_test1..."))
const nftUtxo = await client.getUtxoByUnit(unit)          // the one UTxO holding an NFT
const datum   = await client.getDatum(datumHash)
const params  = await client.getProtocolParameters()
const { poolId, rewards } = await client.getDelegation(rewardAddress)
```

Query methods: `getUtxos`, `getUtxosWithUnit`, `getUtxoByUnit`, `getUtxosByOutRef`, `getDatum`, `getDelegation`, `getProtocolParameters`, `awaitTx`. Best for: TypeScript backends and dApps that want one query API independent of the underlying provider. See `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/providers/` and `.../querying/`.

#### Go clients over providers

Three Go paths, ordered by how much infrastructure you run:

- **blockfrost-go** — typed client for the hosted Blockfrost REST API. `NewAPIClient(APIClientOptions{...})`, then methods mirroring the REST surface (`Transaction`, `TransactionUTXOs`, `TransactionMetadata`, and the `Address*` / `Epoch*` / `Pool*` families). Inherits every Blockfrost trade-off above, including rate limits. Also covers IPFS and webhook signature verification.
- **UTxORPC Go SDK** — the role Evolution SDK plays for TypeScript: the provider becomes a config choice rather than a code rewrite, against any UTxORPC-compatible backend. Paging query helpers (`GetUtxosByAddressPages`, `GetUtxosByAssetPages`, tuned with `WithSearchMaxItems` / `WithSearchStartToken`); submit and mempool operations on `UtxorpcClient` (`SubmitTx`, `EvalTx`, `WaitForTx`, `ReadMempool`, `WatchMempool`). Best when you may switch providers later.
- **gOuroboros** — speaks the node's mini-protocols directly, with no intermediary. `NewConnection(...)`, then `LocalStateQuery().Client` for point-in-time state (`GetUTxOByAddress`, `GetUTxOByTxIn`, `GetCurrentProtocolParams`, `GetStakeDistribution`, `GetDRepState`, `GetProposals`) or `ChainSync().Client` to follow the chain (`GetCurrentTip`, `GetAvailableBlockRange`, `Sync`). Lowest latency and no third party, but you run the node and manage the protocol lifecycle yourself.

Runnable examples ship in the mirror: `${CLAUDE_SKILL_DIR}/../../docs/sources/gouroboros/examples/state-query/main.go` and `.../examples/chain-sync/main.go`. Because Go sources mirror `.go` files, `Grep` a method name to get its signature and doc comment.

### Step 6: Provide working code

Give the developer a working code snippet for their chosen provider and language. Always include:

- Dependency installation
- Client initialization
- The specific query they need
- Error handling
- Response parsing

### Step 7: Address common issues

- **Stale data**: Hosted APIs may lag behind chain tip by a few seconds
- **Datum resolution**: Not all providers return inline datums; may need separate lookup
- **Pagination**: Large result sets require pagination (Blockfrost pages, Kupo cursors)
- **Network selection**: Ensure provider is configured for the right network (mainnet/preprod/preview)
- **CORS**: Frontend apps need CORS-friendly endpoints or a backend proxy

## References

- `skills/query-chain/references/provider-comparison.md` -- Detailed comparison of the providers with decision matrix
- Blockfrost docs: https://docs.blockfrost.io
- Ogmios docs: https://ogmios.dev
- Kupo docs: https://cardanosolutions.github.io/kupo
- Koios docs: https://api.koios.rest
- DB-Sync docs: https://github.com/IntersectMBO/cardano-db-sync
- Oura docs: https://github.com/txpipe/oura
- UTxORPC: https://utxorpc.org
- blockfrost-go: https://pkg.go.dev/github.com/blockfrost/blockfrost-go
