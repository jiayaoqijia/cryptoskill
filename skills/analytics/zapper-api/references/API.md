# Zapper GraphQL API Reference

## Endpoint

```
POST https://public.zapper.xyz/graphql
Content-Type: application/json
x-zapper-api-key: <api_key>
```

## Portfolio Query

```graphql
query Portfolio($addresses: [Address!]!, $first: Int) {
  portfolioV2(addresses: $addresses) {
    tokenBalances {
      totalBalanceUSD
      byToken(first: $first) {
        totalCount
        edges {
          node {
            symbol
            name
            balance
            balanceUSD
            price
            network { name }
            onchainMarketData {
              priceChange24h
              marketCap
            }
          }
        }
      }
    }
    appBalances {
      totalBalanceUSD
      byApp(first: 10) {
        edges {
          node {
            app { displayName }
            balanceUSD
            network { name }
          }
        }
      }
    }
  }
}
```

## NFT Query

```graphql
query NFTs($addresses: [Address!]!, $first: Int) {
  portfolioV2(addresses: $addresses) {
    nftBalances {
      totalBalanceUSD
      totalTokensOwned
      byToken(first: $first, order: {by: USD_WORTH}) {
        edges {
          node {
            token {
              tokenId
              name
              estimatedValue { valueUsd }
              collection {
                name
                address
                network
              }
            }
          }
        }
      }
    }
  }
}
```

## Transaction History Query

Requires `startDate` and `endDate` in milliseconds.

```graphql
query Transactions(
  $addresses: [Address!]!,
  $first: Int,
  $startDate: Timestamp!,
  $endDate: Timestamp!
) {
  transactionHistoryV2(
    subjects: $addresses
    first: $first
    filters: {
      orderByDirection: DESC
      startDate: $startDate
      endDate: $endDate
    }
  ) {
    edges {
      node {
        ... on TimelineEventV2 {
          transaction {
            hash
            timestamp
            network
          }
          interpretation {
            processedDescription
          }
        }
      }
    }
  }
}
```

## Token Price Query

Requires token address and chainId (not symbol).

```graphql
query Price($address: Address!, $chainId: Int!) {
  fungibleTokenV2(address: $address, chainId: $chainId) {
    symbol
    name
    priceData {
      price
      priceChange24h
      marketCap
      volume24h
    }
  }
}
```

Common token addresses (Ethereum mainnet, chainId: 1):
- ETH: `0x0000000000000000000000000000000000000000`
- WETH: `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
- USDC: `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`
- USDT: `0xdac17f958d2ee523a2206206994597c13d831ec7`

## Claimables Query

Claimable rewards are in `positionBalances` with token type containing "claimable".

```graphql
query Claimables($addresses: [Address!]!) {
  portfolioV2(addresses: $addresses) {
    appBalances {
      byApp(first: 50) {
        edges {
          node {
            app { displayName }
            network { name }
            positionBalances(first: 100) {
              edges {
                node {
                  ... on AppTokenPositionBalance {
                    balanceUSD
                    tokens {
                      type
                      symbol
                      balance
                      balanceUSD
                    }
                  }
                  ... on ContractPositionBalance {
                    balanceUSD
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## curl Examples

### Portfolio
```bash
curl -s -X POST https://public.zapper.xyz/graphql \
  -H "Content-Type: application/json" \
  -H "x-zapper-api-key: $ZAPPER_API_KEY" \
  -d '{
    "query": "query($a: [Address!]!) { portfolioV2(addresses: $a) { tokenBalances { totalBalanceUSD } appBalances { totalBalanceUSD } } }",
    "variables": {"a": ["0xADDRESS"]}
  }'
```

### NFTs
```bash
curl -s -X POST https://public.zapper.xyz/graphql \
  -H "Content-Type: application/json" \
  -H "x-zapper-api-key: $ZAPPER_API_KEY" \
  -d '{
    "query": "query($a: [Address!]!) { portfolioV2(addresses: $a) { nftBalances { totalBalanceUSD totalTokensOwned } } }",
    "variables": {"a": ["0xADDRESS"]}
  }'
```

## Supported Chains

Ethereum (1), Base (8453), Arbitrum (42161), Optimism (10), Polygon (137), BNB Chain (56), Avalanche (43114), zkSync (324), Linea (59144), Scroll (534352), Blast (81457), and 40+ more.

## Rate Limits

- Avoid rapid repeated requests
- Use pagination (`first` parameter) for large result sets
- Free tier has generous limits for personal use
