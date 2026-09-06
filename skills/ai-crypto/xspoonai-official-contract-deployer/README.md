# Smart Contract Deployer Skill

The **Smart Contract Deployer** skill allows SpoonOS agents to act as autonomous blockchain developers. It can compile Solidity code on the fly and deploy it to any EVM network.

## Features

- **Compilation**: Uses `py-solc-x` to install and use specific Solidity compiler versions.
- **Deployment**: Uses `web3.py` to sign and send deployment transactions.
- **Verification**: Returns the deployed contract address and transaction hash.

## Usage

### Parameters

- `source_code` (string, optional): Solidity source code to compile.
- `file_path` (string, optional): Path to a `.sol` file (mutually exclusive with `source_code`).
- `contract_name` (string, required): Name of the contract to deploy.
- `rpc_url` (string, optional): RPC endpoint (defaults to env `WEB3_RPC_URL`).
- `private_key` (string, optional): Signer key (defaults to env `PRIVATE_KEY`).
- `constructor_args` (list, optional): Arguments for the contract constructor.
- `solc_version` (string, optional): Solidity compiler version (default: `0.8.19`).

### Example Agent Prompts

> "Deploy a standard ERC20 token named 'MyToken' to the Sepolia testnet."
> "Compile the 'SafeVault.sol' file and deploy it to the local Anvil node."

### Output

Returns a JSON object with:
- `contract_address`: The address of the deployed contract.
- `transaction_hash`: The hash of the deployment transaction.
- `abi`: The contract ABI (for future interactions).

## Setup

Ensure you have a Python environment where `py-solc-x` and `web3` can be installed.
```bash
pip install py-solc-x web3
```
