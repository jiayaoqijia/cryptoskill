# Supported Chains

All chains use the same contract addresses (deterministic deployment):
- **IdentityRegistry:** `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **ReputationRegistry:** `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

## Supported Mainnet Chains

| Chain | ID | RPC | Explorer |
|-------|-----|-----|----------|
| **Base** (default) | 8453 | https://mainnet.base.org | https://basescan.org |
| Ethereum | 1 | https://eth.llamarpc.com | https://etherscan.io |
| Polygon | 137 | https://polygon-rpc.com | https://polygonscan.com |
| BNB Chain | 56 | https://bsc-dataseed.binance.org | https://bscscan.com |
| Arbitrum | 42161 | https://arb1.arbitrum.io/rpc | https://arbiscan.io |
| Celo | 42220 | https://forno.celo.org | https://celoscan.io |
| Gnosis | 100 | https://rpc.gnosischain.com | https://gnosisscan.io |
| Scroll | 534352 | https://rpc.scroll.io | https://scrollscan.com |
| Taiko | 167000 | https://rpc.mainnet.taiko.xyz | https://taikoscan.io |

## Testnets

**Not supported.** This skill only targets mainnet networks.

## Notes

- The SDK (agent0-sdk v1.5.2) natively supports chains 1, 11155111, 137
- Base (8453) and other chains work by passing custom chainId + RPC URL
- The SDK uses standard EVM calls (ethers.js), so any EVM chain with deployed contracts works
