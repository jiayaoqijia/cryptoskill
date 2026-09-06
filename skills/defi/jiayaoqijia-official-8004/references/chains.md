# Supported Chains

ERC-8004 contracts are deployed on 45+ chains using deterministic vanity addresses via CREATE2.

Live chain data: `https://www.8004scan.io/api/v1/public/chains`

## Contract Addresses

### Identity Registry

| Network Type | Address |
|-------------|---------|
| Testnets | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| Mainnets | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |

### Reputation Registry

| All networks | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

### Validation Registry

| All networks | `0x8004Cb1BFb31DAf7788923b405b754f57acEB4272` |

## Mainnet Chains (23)

| Chain | Chain ID | Key | Registry |
|-------|----------|-----|----------|
| Ethereum Mainnet | 1 | `eth_mainnet` | Yes |
| Monad | 143 | `monad_mainnet` | Yes |
| Gnosis | 100 | `gnosis_mainnet` | Yes |
| Linea | 59144 | `linea_mainnet` | Yes |
| Celo | 42220 | `celo_mainnet` | Yes |
| Arbitrum One | 42161 | `arbitrum_mainnet` | Yes |
| BSC | 56 | `bsc_mainnet` | Yes |
| Base | 8453 | `base_mainnet` | Yes |
| Taiko | 167000 | `taiko_mainnet` | Yes |
| Plasma | 9745 | `plasma_mainnet` | No |
| Scroll | 534352 | `scroll_mainnet` | Yes |
| Avalanche C-Chain | 43114 | `avalanche_mainnet` | Yes |
| Optimism | 10 | `optimism_mainnet` | Yes |
| MegaETH | 4326 | `megaeth_mainnet` | Yes |
| Abstract | 2741 | `abstract_mainnet` | Yes |
| SKALE Base | 1187947933 | `skale_base_mainnet` | Yes |
| X Layer | 196 | `xlayer_mainnet` | Yes |
| Mantle | 5000 | `mantle_mainnet` | Yes |
| Soneium | 1868 | `soneium_mainnet` | Yes |
| Metis Andromeda | 1088 | `metis_mainnet` | Yes |
| Polygon | 137 | `polygon_mainnet` | Yes |
| Shape | 360 | `shape_mainnet` | Yes |
| Solana Mainnet | 101 | `solana_mainnet` | Yes |

## Testnet Chains (24)

| Chain | Chain ID | Key | Registry |
|-------|----------|-----|----------|
| Ethereum Sepolia | 11155111 | `eth_sepolia` | Yes |
| Base Sepolia | 84532 | `base_sepolia` | Yes |
| Monad Testnet | 10143 | `monad_testnet` | Yes |
| Gnosis Chiado | 10200 | `gnosis_chiado` | No |
| Linea Sepolia | 59141 | `linea_sepolia` | Yes |
| Celo Sepolia | 11142220 | `celo_sepolia` | Yes |
| Arbitrum Sepolia | 421614 | `arbitrum_sepolia` | Yes |
| BSC Testnet | 97 | `bsc_testnet` | Yes |
| Taiko Hoodi | 167013 | `taiko_hoodi` | Yes |
| Plasma Testnet | 9746 | `plasma_testnet` | No |
| Scroll Sepolia | 534351 | `scroll_sepolia` | Yes |
| Avalanche Fuji | 43113 | `avalanche_fuji` | Yes |
| Optimism Sepolia | 11155420 | `optimism_sepolia` | Yes |
| MegaETH Testnet | 6343 | `megaeth_testnet` | Yes |
| Abstract Testnet | 11124 | `abstract_testnet` | Yes |
| Polygon Amoy | 80002 | `polygon_amoy` | Yes |
| X Layer Testnet | 1952 | `xlayer_testnet` | Yes |
| Mantle Sepolia | 5003 | `mantle_sepolia` | Yes |
| Metis Sepolia | 59902 | `metis_sepolia` | Yes |
| Shape Sepolia | 11011 | `shape_sepolia` | Yes |
| Solana Devnet | 103 | `solana_devnet` | Yes |
| SKALE Base Sepolia | 324705682 | `skale_base_sepolia` | Yes |
| Hedera Testnet | 296 | — | Disabled |
| HyperEVM Testnet | 998 | — | Disabled |

## Chain Resolution Rules

When resolving which chain to use:

1. **Agent ID prefix**: `11155111:42` → chain 11155111 (Ethereum Sepolia)
2. **Config file**: `~/.8004skill/config.json` → `activeChain` field
3. **Ask the user**: Never default silently — wrong chain = wrong registry

**Disambiguation**: "Sepolia" alone is ambiguous — could be Ethereum Sepolia (11155111), Base Sepolia (84532), or others. Always ask.

## Top Chains by Agent Count

Based on live stats from the 8004scan API:

| Chain | Agents | Daily New | Feedbacks |
|-------|--------|-----------|-----------|
| BSC | 38,394 | 1,273 | 11,675 |
| Base | 18,874 | 388 | 40,127 |
| Ethereum | 14,458 | 62 | 2,795 |
| Monad | 8,339 | — | 9,045 |
| MegaETH | 8,131 | 1 | 22 |
| Gnosis | 3,193 | 2 | 4,025 |
| Celo | 1,884 | 25 | 4,102 |
| Solana Devnet | 1,275 | 13 | 250 |
| Solana Mainnet | 1,063 | 2 | 250 |

**Total across all chains**: 103,599 agents, 86,897 feedbacks, 80,592 users.
