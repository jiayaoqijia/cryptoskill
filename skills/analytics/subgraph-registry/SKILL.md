# Subgraph Registry

Agent-friendly discovery of 15,500+ classified subgraphs on The Graph Network. Search by domain, network, protocol type, or natural language goal — get reliability-scored results with query URLs.

## Tools

- **search_subgraphs** — Filter by domain (defi, nfts, dao, gaming), network (ethereum, arbitrum, base), protocol type (dex, lending, bridge), entity type, or keyword
- **recommend_subgraph** — Natural language goal like "find DEX trades on Arbitrum" returns the best matching subgraphs
- **get_subgraph_detail** — Full classification, entities, reliability score, and query instructions for a specific subgraph
- **list_registry_stats** — Registry overview with available domains, networks, and protocol types

## Install

```bash
npx subgraph-registry-mcp
```

## Use Cases

- Discover the right subgraph before querying The Graph
- Find high-reliability DeFi, NFT, DAO, or governance subgraphs by chain
- Get query URLs and entity schemas without manual exploration
- Compare subgraphs by reliability score (query fees, curation signal, indexer stake)
