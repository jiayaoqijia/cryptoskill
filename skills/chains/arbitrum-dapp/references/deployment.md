# Deployment

## Networks

| Network | Chain ID | RPC | Explorer |
|---------|----------|-----|----------|
| Local devnode | 412346 | http://localhost:8547 | — |
| Arbitrum Sepolia | 421614 | https://sepolia-rollup.arbitrum.io/rpc | https://sepolia.arbiscan.io |
| Arbitrum One | 42161 | https://arb1.arbitrum.io/rpc | https://arbiscan.io |

## Environment Setup

```bash
# .env (never commit this file)
PRIVATE_KEY=0x...
ARBITRUM_SEPOLIA_RPC_URL=https://sepolia-rollup.arbitrum.io/rpc
ARBITRUM_ONE_RPC_URL=https://arb1.arbitrum.io/rpc
```

## Deploying Stylus Contracts

### To testnet

```bash
cargo stylus deploy \
  --endpoint $ARBITRUM_SEPOLIA_RPC_URL \
  --private-key $PRIVATE_KEY
```

### To mainnet

```bash
cargo stylus deploy \
  --endpoint $ARBITRUM_ONE_RPC_URL \
  --private-key $PRIVATE_KEY
```

### Deployment output

A successful deploy prints:

```
Deploying program to address: 0x...
Program activated and ready.
```

Save this address — you need it for frontend configuration and contract interaction.

### Activation

Stylus contracts require an activation step after deployment. `cargo stylus deploy` handles this automatically. If deploying manually, activate with:

```bash
cargo stylus activate \
  --address 0xYOUR_CONTRACT \
  --endpoint $ARBITRUM_SEPOLIA_RPC_URL \
  --private-key $PRIVATE_KEY
```

## Deploying Solidity Contracts

### Forge script deployment

```bash
# Testnet
forge script script/Deploy.s.sol \
  --rpc-url $ARBITRUM_SEPOLIA_RPC_URL \
  --broadcast \
  --private-key $PRIVATE_KEY \
  --verify \
  --etherscan-api-key $ARBISCAN_API_KEY

# Mainnet
forge script script/Deploy.s.sol \
  --rpc-url $ARBITRUM_ONE_RPC_URL \
  --broadcast \
  --private-key $PRIVATE_KEY \
  --verify \
  --etherscan-api-key $ARBISCAN_API_KEY
```

### Direct deployment with forge create

```bash
forge create src/Counter.sol:Counter \
  --rpc-url $ARBITRUM_SEPOLIA_RPC_URL \
  --private-key $PRIVATE_KEY
```

## Contract Verification

### Solidity (Arbiscan)

Verification happens automatically with the `--verify` flag during deployment. For manual verification:

```bash
forge verify-contract 0xYOUR_CONTRACT src/Counter.sol:Counter \
  --chain arbitrum-sepolia \
  --etherscan-api-key $ARBISCAN_API_KEY
```

### Stylus (Arbiscan)

Arbiscan supports Stylus contract verification for contracts deployed with `cargo-stylus` v0.5.0+. On deployment, a keccak256 hash is created from all Rust source files (sorted by path), `rust-toolchain.toml`, `Cargo.toml`, and `Cargo.lock`, and injected into the WASM binary. Verification rebuilds the project and checks for a match.

Verify through Arbiscan's web interface:

1. Navigate to your contract's page on Arbiscan
2. Go to the **Contract** tab and click **Verify & Publish**
3. Select **Stylus** as the compiler type
4. Upload your source files or provide the repository

See the [official verification guide](https://docs.arbitrum.io/stylus/how-tos/verifying-contracts-arbiscan) for full details.

> **Tip:** Deploy and verify on Arbitrum Sepolia first before going to mainnet. All data in source files — including comments — is used for the reproducible hash.

## Gas Estimation

### Stylus

```bash
cargo stylus deploy \
  --endpoint $ARBITRUM_SEPOLIA_RPC_URL \
  --private-key $PRIVATE_KEY \
  --estimate-gas
```

### Solidity

```bash
forge script script/Deploy.s.sol \
  --rpc-url $ARBITRUM_SEPOLIA_RPC_URL \
  --private-key $PRIVATE_KEY
# (without --broadcast, this simulates and shows gas estimates)
```

## Post-Deployment Checklist

1. Save deployed contract addresses to environment config
2. Export ABIs and update frontend imports
3. Verify contracts on block explorer
4. Test basic read/write operations via `cast`
5. Update frontend contract addresses for the target network
6. Test the full frontend flow against the deployed contracts
