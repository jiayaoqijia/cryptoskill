---
name: monad-development
description: Builds dapps on Monad blockchain. Use when deploying contracts, setting up frontends with viem/wagmi, or verifying contracts on Monad testnet or mainnet.
license: MIT
compatibility: Requires foundry, node 18+, curl, and internet access for faucet and verification APIs
metadata:
  author: monad-skills
  version: "1.0.0"
---

# Monad Development

For questions not covered here, fetch https://docs.monad.xyz/llms.txt

## Quick Reference

### Defaults
- **Network:** Always use **testnet** (chain ID 10143) unless user says "mainnet"
- **Verification:** Always verify contracts after deployment unless user says not to
- **Framework:** Use Foundry (not Hardhat)
- **Wallet:** If you generate a wallet, MUST persist it (see Wallet Persistence section)

### Networks

| Network | Chain ID | RPC |
|---------|----------|-----|
| Testnet | 10143 | https://testnet-rpc.monad.xyz |
| Mainnet | 143 | https://rpc.monad.xyz |

Docs: https://docs.monad.xyz

### Explorers

| Explorer | Testnet | Mainnet |
|----------|---------|---------|
| Socialscan | https://monad-testnet.socialscan.io | https://monad.socialscan.io |
| MonadVision | https://testnet.monadvision.com | https://monadvision.com |
| Monadscan | https://testnet.monadscan.com | https://monadscan.com |

### Agent APIs

**IMPORTANT:** Do NOT use a browser. Use these APIs directly with curl.

**Faucet (Testnet Funding):**
```bash
curl -X POST https://agents.devnads.com/v1/faucet \
  -H "Content-Type: application/json" \
  -d '{"chainId": 10143, "address": "0xYOUR_ADDRESS"}'
```

Returns: `{"txHash": "0x...", "amount": "1000000000000000000", "chain": "Monad Testnet"}`

**Fallback (official faucet):** https://faucet.monad.xyz
If the agent faucet fails, ask the user to fund via the official faucet (do not use a browser yourself).

**Verification (All Explorers):**

ALWAYS use the verification API first. It verifies on all 3 explorers (MonadVision, Socialscan, Monadscan) with one call. Do NOT use `forge verify-contract` as first choice.

```bash
# 1. Get verification data
forge verify-contract <ADDR> <CONTRACT> \
  --chain 10143 \
  --show-standard-json-input > /tmp/standard-input.json

cat out/<Contract>.sol/<Contract>.json | jq '.metadata' > /tmp/metadata.json
COMPILER_VERSION=$(jq -r '.metadata | fromjson | .compiler.version' out/<Contract>.sol/<Contract>.json)

# 2. Call verification API
STANDARD_INPUT=$(cat /tmp/standard-input.json)
FOUNDRY_METADATA=$(cat /tmp/metadata.json)

cat > /tmp/verify.json << EOF
{
  "chainId": 10143,
  "contractAddress": "0xYOUR_CONTRACT_ADDRESS",
  "contractName": "src/MyContract.sol:MyContract",
  "compilerVersion": "v${COMPILER_VERSION}",
  "standardJsonInput": $STANDARD_INPUT,
  "foundryMetadata": $FOUNDRY_METADATA
}
EOF

curl -X POST https://agents.devnads.com/v1/verify \
  -H "Content-Type: application/json" \
  -d @/tmp/verify.json
```

**With constructor arguments:** Add `constructorArgs` (ABI-encoded, WITHOUT 0x prefix):
```bash
ARGS=$(cast abi-encode "constructor(string,string,uint256)" "MyToken" "MTK" 1000000000000000000000000)
ARGS_NO_PREFIX=${ARGS#0x}
# Add to request: "constructorArgs": "$ARGS_NO_PREFIX"
```

**Manual verification fallback (if API fails):**
```bash
forge verify-contract <ADDR> <CONTRACT> --chain 10143 \
  --verifier sourcify \
  --verifier-url "https://sourcify-api-monad.blockvision.org/"
```

## Wallet Persistence

**CRITICAL for agents:** If you generate a wallet for the user, you MUST persist it for future use.

When generating a new wallet:
1. Create wallet: `cast wallet new`
2. **Immediately save** the address and private key to a secure location
3. Inform the user where the wallet details are stored
4. Fund the wallet via faucet before deployment

**Storage options:**
- Write to `~/.monad-wallet` with chmod 600
- Store in a project-specific `.env` file (add to .gitignore)
- Return credentials to user and ask them to save securely

**Why this matters:** Users need access to their wallet to:
- Deploy additional contracts
- Interact with deployed contracts
- Manage funds
- Verify ownership

## Deployment Workflow

Use `forge script` for deployments:

```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**Deploy script template:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import "forge-std/Script.sol";
import "../src/MyContract.sol";

contract DeployScript is Script {
    function run() external {
        vm.startBroadcast();
        MyContract contract = new MyContract();
        console.log("Contract deployed at:", address(contract));
        vm.stopBroadcast();
    }
}
```

## Technical Details

### EVM Version (Critical)

Always set `evmVersion: "prague"`. Requires Solidity 0.8.27+.

**Foundry** (`foundry.toml`):
```toml
[profile.default]
evm_version = "prague"
solc_version = "0.8.28"
```

### Foundry Tips

**Flags that don't exist (don't use):**
- `--no-commit` - not a valid flag for `forge init` or `forge install`

**Deployment - use `forge script`, NOT `forge create`:**

`forge create --broadcast` is buggy and often ignored. Use `forge script` instead.

```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**Deploy script must NOT hardcode addresses:**

```solidity
// ✅ Correct - reads private key from --private-key flag
function run() external {
    vm.startBroadcast();
    new MyContract();
    vm.stopBroadcast();
}

// ❌ Wrong - hardcodes address, causes "No associated wallet" error
function run() external {
    vm.startBroadcast(0x1234...);
}
```

### Frontend

Import from `viem/chains`. Do NOT define custom chain:

```ts
import { monadTestnet } from "viem/chains";
```

Use with wagmi:

```ts
import { createConfig, http } from 'wagmi'
import { monadTestnet } from 'viem/chains'

const config = createConfig({
  chains: [monadTestnet],
  transports: {
    [monadTestnet.id]: http()
  }
})
```

## Example: Deploy ERC20

**1. Create project:**
```bash
forge init my-token
cd my-token
```

**2. Configure `foundry.toml`:**
```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
evm_version = "prague"
solc_version = "0.8.28"
```

**3. Create contract `src/MyToken.sol`:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("MyToken", "MTK") {
        _mint(msg.sender, initialSupply);
    }
}
```

**4. Install dependencies:**
```bash
forge install OpenZeppelin/openzeppelin-contracts --no-commit
```

**5. Create deploy script `script/Deploy.s.sol`:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import "forge-std/Script.sol";
import "../src/MyToken.sol";

contract DeployScript is Script {
    function run() external {
        vm.startBroadcast();
        MyToken token = new MyToken(1000000 * 10**18);
        console.log("Token deployed at:", address(token));
        vm.stopBroadcast();
    }
}
```

**6. Deploy:**
```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**7. Verify:**
```bash
# Use verification API (verifies on all explorers)
STANDARD_INPUT=$(forge verify-contract <TOKEN_ADDRESS> src/MyToken.sol:MyToken --chain 10143 --show-standard-json-input)
COMPILER_VERSION=$(jq -r '.metadata | fromjson | .compiler.version' out/MyToken.sol/MyToken.json)

curl -X POST https://agents.devnads.com/v1/verify \
  -H "Content-Type: application/json" \
  -d "{
    \"chainId\": 10143,
    \"contractAddress\": \"<TOKEN_ADDRESS>\",
    \"contractName\": \"src/MyToken.sol:MyToken\",
    \"compilerVersion\": \"v${COMPILER_VERSION}\",
    \"standardJsonInput\": $STANDARD_INPUT,
    \"constructorArgs\": \"$(cast abi-encode 'constructor(uint256)' 1000000000000000000000000 | sed 's/0x//')\"
  }"
```
