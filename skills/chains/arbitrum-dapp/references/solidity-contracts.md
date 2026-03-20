# Solidity Contracts on Arbitrum

## Prerequisites

- Foundry: `curl -L https://foundry.paradigm.xyz | bash && foundryup`
- Solidity 0.8.x (managed by Foundry)

## Project Setup

```bash
forge init my-solidity-contracts
cd my-solidity-contracts
```

This creates:

```
my-solidity-contracts/
├── src/           # Contract source files
├── test/          # Test files
├── script/        # Deployment scripts
├── lib/           # Dependencies (git submodules)
└── foundry.toml   # Configuration
```

## foundry.toml for Arbitrum

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc = "0.8.28"
optimizer = true
optimizer_runs = 200

[rpc_endpoints]
local = "http://localhost:8547"
arbitrum_sepolia = "${ARBITRUM_SEPOLIA_RPC_URL}"
arbitrum_one = "${ARBITRUM_ONE_RPC_URL}"
```

## Contract Example

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract Counter {
    uint256 public number;

    event NumberSet(uint256 newNumber);

    function setNumber(uint256 newNumber) public {
        number = newNumber;
        emit NumberSet(newNumber);
    }

    function increment() public {
        number++;
    }
}
```

## Arbitrum-Specific Considerations

### Gas and Fees

- Arbitrum uses a two-component fee model: L2 execution gas + L1 calldata posting cost.
- `block.basefee` on Arbitrum reflects the L2 base fee only.

### Block Properties

- `block.number` returns an **approximate** L1 block number, not the L2 block number. It syncs with Ethereum's block number roughly every 13-15 seconds.
- `block.timestamp` reflects the time the sequencer received the transaction. Reliable over hours, but not precise to the minute.

## Testing

```solidity
// test/Counter.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "forge-std/Test.sol";
import "../src/Counter.sol";

contract CounterTest is Test {
    Counter public counter;

    function setUp() public {
        counter = new Counter();
        counter.setNumber(0);
    }

    function test_Increment() public {
        counter.increment();
        assertEq(counter.number(), 1);
    }

    function testFuzz_SetNumber(uint256 x) public {
        counter.setNumber(x);
        assertEq(counter.number(), x);
    }
}
```

```bash
forge test
forge test -vvvv   # verbose with traces
forge test --gas-report
```

## Deployment

### Deploy script

```solidity
// script/Deploy.s.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "forge-std/Script.sol";
import "../src/Counter.sol";

contract DeployScript is Script {
    function run() external {
        vm.startBroadcast();
        Counter counter = new Counter();
        vm.stopBroadcast();
    }
}
```

### Run deployment

```bash
# Local devnode
forge script script/Deploy.s.sol --rpc-url http://localhost:8547 \
  --broadcast --private-key 0x...

# Arbitrum Sepolia
forge script script/Deploy.s.sol --rpc-url $ARBITRUM_SEPOLIA_RPC_URL \
  --broadcast --private-key $PRIVATE_KEY --verify

# Arbitrum One (mainnet)
forge script script/Deploy.s.sol --rpc-url $ARBITRUM_ONE_RPC_URL \
  --broadcast --private-key $PRIVATE_KEY --verify
```

## Interacting with Stylus Contracts

Solidity contracts can call Stylus contracts using standard interfaces. From the Solidity side, a Stylus contract looks like any other contract:

```solidity
interface IStylusCounter {
    function number() external view returns (uint256);
    function increment() external;
}

contract MyContract {
    IStylusCounter public stylusCounter;

    constructor(address _stylusCounter) {
        stylusCounter = IStylusCounter(_stylusCounter);
    }

    function readStylusCounter() external view returns (uint256) {
        return stylusCounter.number();
    }
}
```

## Extracting ABI for Frontend

```bash
# Full ABI JSON
forge inspect src/Counter.sol:Counter abi

# Save to file for frontend import
forge inspect src/Counter.sol:Counter abi > ../frontend/src/abi/Counter.json
```
