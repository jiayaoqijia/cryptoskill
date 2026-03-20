# Supported Chains Reference

All chains supported by Alchemy APIs.

## EVM Chains

### Layer 1

| Chain | Mainnet ID | Testnet ID |
|-------|------------|------------|
| Ethereum | `eth-mainnet` | `eth-sepolia`, `eth-holesky` |
| BNB Smart Chain | `bnb-mainnet` | `bnb-testnet` |
| Avalanche | `avax-mainnet` | `avax-fuji` |
| Gnosis | `gnosis-mainnet` | `gnosis-chiado` |

### Layer 2 - Optimistic Rollups

| Chain | Mainnet ID | Testnet ID |
|-------|------------|------------|
| Arbitrum One | `arb-mainnet` | `arb-sepolia` |
| Arbitrum Nova | `arbnova-mainnet` | — |
| OP Mainnet | `opt-mainnet` | `opt-sepolia` |
| Base | `base-mainnet` | `base-sepolia` |
| Blast | `blast-mainnet` | `blast-sepolia` |
| Mode | `mode-mainnet` | — |
| Zora | `zora-mainnet` | — |
| Mantle | `mantle-mainnet` | — |
| Metis | `metis-mainnet` | — |

### Layer 2 - ZK Rollups

| Chain | Mainnet ID | Testnet ID |
|-------|------------|------------|
| Polygon zkEVM | `polygonzkevm-mainnet` | `polygonzkevm-cardona` |
| zkSync Era | `zksync-mainnet` | `zksync-sepolia` |
| Scroll | `scroll-mainnet` | `scroll-sepolia` |
| Linea | `linea-mainnet` | `linea-sepolia` |
| Starknet | `starknet-mainnet` | `starknet-sepolia` |

### Sidechains

| Chain | Mainnet ID | Testnet ID |
|-------|------------|------------|
| Polygon PoS | `polygon-mainnet` | `polygon-amoy` |

## Non-EVM Chains

| Chain | Mainnet ID | Testnet ID |
|-------|------------|------------|
| Solana | `solana-mainnet` | `solana-devnet` |
| Bitcoin | `btc-mainnet` | `btc-testnet` |
| Aptos | `aptos-mainnet` | `aptos-testnet` |
| Sui | `sui-mainnet` | `sui-testnet` |
| Flow | `flow-mainnet` | `flow-testnet` |

## URL Patterns

### Node API (JSON-RPC)
```
https://{chain-id}.g.alchemy.com/v2/{apiKey}
```

### NFT API
```
https://{chain-id}.g.alchemy.com/nft/v3/{apiKey}
```

### WebSocket
```
wss://{chain-id}.g.alchemy.com/v2/{apiKey}
```

## Feature Support by Chain

| Feature | ETH | Polygon | Arbitrum | Base | Solana |
|---------|-----|---------|----------|------|--------|
| Node API | ✅ | ✅ | ✅ | ✅ | ✅ |
| NFT API | ✅ | ✅ | ✅ | ✅ | ✅ |
| Token API | ✅ | ✅ | ✅ | ✅ | ✅ |
| Transfers | ✅ | ✅ | ✅ | ✅ | ✅ |
| Webhooks | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Debug/Trace | ✅ | ✅ | ✅ | ✅ | ❌ |

## Examples

```bash
# Ethereum Mainnet
curl https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY ...

# Polygon
curl https://polygon-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY ...

# Base
curl https://base-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY ...

# Arbitrum
curl https://arb-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY ...
```
