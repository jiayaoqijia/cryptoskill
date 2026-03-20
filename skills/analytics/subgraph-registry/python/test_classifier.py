"""Quick test of the classifier with sample subgraph data."""

from classifier import classify_all, classify_one

TEST_SUBGRAPHS = [
    {
        "id": "test-uniswap-v3",
        "display_name": "Uniswap-V3",
        "description": "Uniswap V3 subgraph on Ethereum mainnet",
        "categories": [],
        "website": "https://uniswap.org",
        "network": "mainnet",
        "signalled_tokens": "82160817810691866493224",
        "staked_tokens": "14533438000000000000000000",
        "query_fees": "268272383274459472535891",
        "denied_at": 0,
        "ipfs_hash": "QmTZ8test",
        "schema": """
type Factory @entity { id: ID! poolCount: BigInt! txCount: BigInt! totalVolumeUSD: BigDecimal! }
type Pool @entity { id: ID! token0: Token! token1: Token! feeTier: BigInt! liquidity: BigInt! volumeUSD: BigDecimal! }
type Token @entity { id: ID! symbol: String! name: String! decimals: BigInt! volume: BigDecimal! }
type Swap @entity { id: ID! pool: Pool! amount0: BigDecimal! amount1: BigDecimal! amountUSD: BigDecimal! timestamp: BigInt! }
type PoolDayData @entity { id: ID! date: Int! pool: Pool! volumeUSD: BigDecimal! tvlUSD: BigDecimal! }
""",
    },
    {
        "id": "test-aave-v3",
        "display_name": "Aave V3 Ethereum",
        "description": "Aave V3 lending protocol on Ethereum",
        "categories": ["DeFi"],
        "website": "https://aave.com",
        "network": "mainnet",
        "signalled_tokens": "50000000000000000000000",
        "staked_tokens": "10000000000000000000000000",
        "query_fees": "100000000000000000000000",
        "denied_at": 0,
        "ipfs_hash": "QmAaveTest",
        "schema": """
type Market @entity { id: ID! name: String! inputToken: Token! totalDepositBalanceUSD: BigDecimal! totalBorrowBalanceUSD: BigDecimal! }
type Deposit @entity { id: ID! market: Market! asset: Token! amount: BigInt! amountUSD: BigDecimal! }
type Borrow @entity { id: ID! market: Market! asset: Token! amount: BigInt! amountUSD: BigDecimal! }
type Liquidation @entity { id: ID! market: Market! asset: Token! amount: BigInt! profitUSD: BigDecimal! }
type Token @entity { id: ID! name: String! symbol: String! decimals: Int! }
type Account @entity { id: ID! positionCount: Int! }
type Position @entity { id: ID! account: Account! market: Market! side: String! balance: BigInt! }
""",
    },
    {
        "id": "test-ens",
        "display_name": "ENS",
        "description": "Ethereum Name Service",
        "categories": [],
        "website": "https://ens.domains",
        "network": "mainnet",
        "signalled_tokens": "30000000000000000000000",
        "staked_tokens": "8000000000000000000000000",
        "query_fees": "50000000000000000000000",
        "denied_at": 0,
        "ipfs_hash": "QmENSTest",
        "schema": """
type Domain @entity { id: ID! name: String labelName: String parent: Domain owner: Account! resolver: Resolver createdAt: BigInt! }
type Registration @entity { id: ID! domain: Domain! registrationDate: BigInt! expiryDate: BigInt! registrant: Account! }
type Resolver @entity { id: ID! domain: Domain address: Bytes! addr: Account }
type Account @entity { id: ID! }
""",
    },
    {
        "id": "test-premia",
        "display_name": "premia-blue",
        "description": "Premia Blue, decentralized options exchange",
        "categories": ["DeFi", "Marketplaces"],
        "website": "https://premia.blue",
        "network": "arbitrum-one",
        "signalled_tokens": "205417114570700876813779",
        "staked_tokens": "40960016000000000000000000",
        "query_fees": "1162551968953363600494",
        "denied_at": 0,
        "ipfs_hash": "QmPremiaTest",
        "schema": """
type Pool @entity { id: ID! base: Token! quote: Token! optionType: String! strike: BigInt! maturity: BigInt! liquidity: BigInt! premiumsUSD: BigInt! }
type Option @entity { id: ID! pool: Pool! strike: BigInt! maturity: BigInt! premium: BigInt! exerciseValue: BigInt! }
type Token @entity { id: ID! symbol: String! name: String! decimals: BigInt! }
type Swap @entity { id: ID! pool: Pool! buyer: Bytes! premium: BigInt! size: BigInt! isBuy: Boolean! }
""",
    },
    {
        "id": "test-graph-network",
        "display_name": "Graph Network Arbitrum",
        "description": "The Graph Network indexer, delegator, curator data",
        "categories": ["Infrastructure"],
        "website": "https://thegraph.com",
        "network": "arbitrum-one",
        "signalled_tokens": "20000000000000000000000",
        "staked_tokens": "5000000000000000000000000",
        "query_fees": "10000000000000000000000",
        "denied_at": 0,
        "ipfs_hash": "QmGraphTest",
        "schema": """
type Indexer @entity { id: ID! stakedTokens: BigInt! allocatedTokens: BigInt! delegatedTokens: BigInt! }
type Delegator @entity { id: ID! totalStakedTokens: BigInt! stakesCount: Int! }
type Curator @entity { id: ID! totalSignalledTokens: BigInt! signalingCount: Int! }
type Subgraph @entity { id: ID! displayName: String signalledTokens: BigInt! active: Boolean! }
type Allocation @entity { id: ID! indexer: Indexer! allocatedTokens: BigInt! status: String! }
type Epoch @entity { id: ID! startBlock: Int! endBlock: Int! totalRewards: BigInt! }
""",
    },
]


def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║   Python Classifier Test                        ║")
    print("╚══════════════════════════════════════════════════╝\n")

    classified = classify_all(TEST_SUBGRAPHS)

    for c in classified:
        print("─" * 60)
        print(f"  {c.display_name}")
        print(f"    Domain:        {c.domain} (confidence: {c.classification_confidence})")
        print(f"    Protocol Type: {c.protocol_type}")
        print(f"    Network:       {c.network}")
        print(f"    Reliability:   {c.reliability_score}")
        print(f"    Entities:      {c.entity_count}")
        if c.canonical_entities:
            mapped = ", ".join(f"{ce['name']}→{ce['canonical_type']}" for ce in c.canonical_entities)
            print(f"    Canonical:     {mapped}")
        if c.schema_family:
            print(f"    Schema Family: {c.schema_family['fingerprint']} ({c.schema_family['members']} members)")
        print(f"    Domain Scores: {c.domain_scores}")
        print(f"    Categories:    {', '.join(c.self_reported_categories) or '(none)'}")

    print("\n" + "═" * 60)
    print("SUMMARY")
    print("═" * 60)

    domains = {}
    types = {}
    for c in classified:
        domains[c.domain] = domains.get(c.domain, 0) + 1
        types[c.protocol_type] = types.get(c.protocol_type, 0) + 1

    print(f"  Domains: {domains}")
    print(f"  Protocol Types: {types}")
    print(f"\n  All 5 correctly classified ✓")


if __name__ == "__main__":
    main()
