# GraphQL RPC

Source: https://docs.sui.io/concepts/data-access/graphql-rpc

Generally available. Reads from three backing stores and also supports transaction submission and dry-run:
1. The **General-Purpose Indexer**'s Postgres (primary source — indexed, filterable).
2. A **full node** (live tip-of-chain reads the indexer hasn't caught up to).
3. The **Archival Store** (historical data pruned from full nodes — when operator-configured).

GraphQL RPC routes each query to whichever backing store is right. Clients don't pick.

## When to use

From the docs:
> GraphQL RPC excels for applications requiring:
> - Historical data with configurable retention or filtered queries
> - Structured results for frontends (wallets, dashboards)
> - Flexible, composable queries that reduce data overfetching
> - Multiple data entities in single or consistent multi-request patterns

Typical fit:
- Frontend dashboards with several panels fetching related data.
- Wallet history views (tx list + effects + balance changes in one query).
- NFT marketplace explorers (filter + sort by type + traits).
- Point-in-time historical reads ("what did object X look like at checkpoint Y?").

## When not to use

- Real-time / streaming subscriptions. → gRPC (GraphQL does not support subscriptions yet; this will change in the coming months).
- Ultra-low-latency trading. → gRPC.
- App-specific analytics over millions of rows. → Custom indexer (`sui-indexer-alt`).

## Endpoint URLs

| Network | GraphQL URL |
|---|---|
| Mainnet | `https://graphql.mainnet.sui.io/graphql` |
| Testnet | `https://graphql.testnet.sui.io/graphql` |
| Devnet | `https://graphql.devnet.sui.io/graphql` |

The public endpoints are rate-limited and provided as a public good. Production apps should use a provider endpoint or operate their own GraphQL stack.

## TypeScript — `SuiGraphQLClient`

```ts
import { SuiGraphQLClient } from '@mysten/sui/graphql';
import { graphql } from '@mysten/sui/graphql/schema';

const client = new SuiGraphQLClient({
  network: 'mainnet',
  url: 'https://graphql.mainnet.sui.io/graphql',
});

const query = graphql(`
  query GetOwnedNFTs($owner: SuiAddress!, $type: String!) {
    address(address: $owner) {
      objects(filter: { type: $type }) {
        nodes {
          address
          version
          asMoveObject {
            contents {
              json
            }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
`);

const result = await client.query({
  query,
  variables: { owner: '0x...', type: '0xpkg::nft::NFT' },
});
```

The `graphql()` helper provides type inference from the schema. Old code imports from `@mysten/sui/graphql/schemas/latest` — v2 is `@mysten/sui/graphql/schema` (singular).

## Rust — `sui-graphql` crate

```rust
use sui_graphql::client::Client;

let gql = Client::new("https://graphql.mainnet.sui.io/graphql")?;
// Queries are typed via sui-graphql-macros
```

## Query patterns

### Single entity

```graphql
query {
  object(address: "0x...") {
    version
    digest
    owner { ... on AddressOwner { owner } }
  }
}
```

### Owned objects with filter + pagination

```graphql
query Owned($owner: SuiAddress!, $cursor: String) {
  address(address: $owner) {
    objects(first: 50, after: $cursor, filter: { type: "0xpkg::nft::NFT" }) {
      nodes { address version }
      pageInfo { hasNextPage endCursor }
    }
  }
}
```

### Multi-entity single-request (the GraphQL advantage)

```graphql
query Profile($addr: SuiAddress!) {
  address(address: $addr) {
    balances(first: 20) { nodes { coinType { repr } totalBalance } }
    objects(first: 10, filter: { type: "0xpkg::nft::NFT" }) {
      nodes { address asMoveObject { contents { json } } }
    }
    transactionBlocks(last: 10) {
      nodes { digest effects { status } }
    }
  }
}
```

One round trip, three related entity types.

### Historical point-in-time

```graphql
query { object(address: "0x...", version: 42) { ... } }
```

For versions that full nodes have pruned, the server routes to the Archival Store when the GraphQL operator has configured it.

## Pagination — cursor-based

Connection pattern (Relay-style):
- `nodes: [...]`
- `pageInfo: { hasNextPage, endCursor, hasPreviousPage, startCursor }`

```ts
let cursor: string | null = null;
do {
  const page = await client.query({
    query,
    variables: { cursor },
  });
  processPage(page.data.address.objects.nodes);
  cursor = page.data.address.objects.pageInfo.hasNextPage
    ? page.data.address.objects.pageInfo.endCursor
    : null;
} while (cursor);
```

## Transaction execution

GraphQL is not read-only. Use `Mutation.executeTransaction` to submit transactions and `Query.simulateTransaction` to preview effects without committing.

### Execute a transaction

```graphql
mutation ($tx: String!, $sigs: [String!]!) {
  executeTransaction(txBytes: $tx, signatures: $sigs) {
    effects {
      status
      checkpoint { sequenceNumber }
    }
  }
}
```

Select fields from `effects` in the same mutation to read execution results immediately without waiting for a separate indexed query.

### Simulate a transaction

```graphql
query ($tx: JSON!) {
  simulateTransaction(transaction: $tx, checksEnabled: true, doGasSelection: true) {
    effects {
      status
      gasEffects { gasSummary { computationCost storageCost } }
    }
  }
}
```

## Read-after-write consistency

Queries nested under `executeTransaction` or `simulateTransaction` are evaluated in a special scope that exists just after the executed/simulated transaction, without requiring indexing. This means **execution-attached or simulation-attached queries can often provide consistent read-after-write results immediately**, as long as the requested fields do not require indexed history.

If you only need data returned by transaction effects, prefer selecting it in the same GraphQL request instead of submitting the transaction and then waiting for a separately indexed follow-up query.

Limitations in execution-attached scope:
- Live object set queries are not available (they rely on indexed data).
- Queries that paginate through history are not available (the system cannot determine where in the history the transaction falls before indexing).

## Operational notes

- Rate limits on public endpoints can be tight. For production-scale traffic, use a provider endpoint or operate your own GraphQL stack (which runs atop the General-Purpose Indexer). This is not the same as building a custom `sui-indexer-alt` pipeline — it's just self-hosting the standard GraphQL service.
- GraphQL currently supports filtered pagination over historical transactions and events that gRPC does not yet offer.
- Archival routing is operator-configured: the GraphQL service routes supported historical point lookups to Archival when the operator has set it up. Without archival configuration, retention is limited to the Postgres database's retention policy.

## Relationship to the indexer

GraphQL RPC doesn't exist without the General-Purpose Indexer. If you need a query that GraphQL doesn't support out of the box, two options:

1. **Extend the General-Purpose Indexer** with an additional pipeline (see `indexers.md`), then query your new tables via GraphQL.
2. **Run a custom indexer** with its own schema and query it however you like (Postgres SQL, GraphQL, your own REST).

## Common mistakes

- **Using it for real-time subscriptions.** GraphQL doesn't push (yet). Use gRPC subscriptions for streaming.
- **Importing from `@mysten/sui/graphql/schemas/latest`** — v1. v2 is `@mysten/sui/graphql/schema`.
- **Treating pagination as offset-based.** GraphQL uses cursors. Don't pass integer offsets.
- **Over-fetching by selecting every field.** GraphQL's whole point is "ask for only what you need." Trim queries to the fields actually used.
