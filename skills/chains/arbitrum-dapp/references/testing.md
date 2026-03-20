# Testing

## Stylus Rust Testing

### Unit tests with stylus-test

Add the test feature to `Cargo.toml`:

```toml
[dev-dependencies]
stylus-sdk = { version = "0.10.0", features = ["stylus-test"] }
```

### Basic test

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_counter_operations() {
        let mut contract = Counter::default();

        // Initial state
        assert_eq!(contract.number(), U256::from(0));

        // Set and read
        contract.set_number(U256::from(42));
        assert_eq!(contract.number(), U256::from(42));

        // Increment
        contract.increment();
        assert_eq!(contract.number(), U256::from(43));
    }
}
```

### Testing with transaction context

The `stylus-test` feature lets you simulate `msg::sender()`, `msg::value()`, and other context values:

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use stylus_sdk::msg;

    #[test]
    fn test_with_sender() {
        let mut contract = Counter::default();
        // stylus-test provides simulated context
        // msg::sender() returns a default test address
        contract.increment();
        assert_eq!(contract.number(), U256::from(1));
    }
}
```

### Running Stylus tests

```bash
cargo test
cargo test -- --nocapture    # with println! output
cargo test test_name         # run specific test
```

## Solidity Testing with Foundry

### Basic test

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
    }

    function test_InitialValue() public view {
        assertEq(counter.number(), 0);
    }

    function test_SetNumber() public {
        counter.setNumber(42);
        assertEq(counter.number(), 42);
    }

    function test_Increment() public {
        counter.setNumber(0);
        counter.increment();
        assertEq(counter.number(), 1);
    }
}
```

### Fuzz testing

```solidity
function testFuzz_SetNumber(uint256 x) public {
    counter.setNumber(x);
    assertEq(counter.number(), x);
}
```

### Testing with cheatcodes

```solidity
function test_OnlyOwner() public {
    // Impersonate a different address
    vm.prank(address(0xdead));
    vm.expectRevert("Unauthorized");
    counter.setNumber(999);
}

function test_WithValue() public {
    // Send ETH with call
    vm.deal(address(this), 1 ether);
    payableContract.deposit{value: 1 ether}();
}

function test_EventEmission() public {
    vm.expectEmit(true, true, false, true);
    emit NumberSet(42);
    counter.setNumber(42);
}
```

### Running Solidity tests

```bash
forge test                    # run all tests
forge test -vvvv              # verbose with full traces
forge test --match-test test_Increment   # specific test
forge test --match-contract CounterTest  # specific contract
forge test --gas-report       # with gas usage report
forge test --fork-url $ARBITRUM_SEPOLIA_RPC_URL  # fork testing
```

## Integration Testing

### Testing Stylus + Solidity interop

Deploy both contracts to the local devnode and test cross-contract calls:

```bash
# 1. Start devnode
cd apps/nitro-devnode && ./run-dev-node.sh

# 2. Deploy Stylus contract
cd apps/contracts-stylus
cargo stylus deploy --endpoint http://localhost:8547 \
  --private-key 0xb6b15c8cb491557369f3c7d2c287b053eb229daa9c22138887752191c9520659
# Note the deployed address

# 3. Deploy Solidity contract (passing Stylus address as constructor arg if needed)
cd apps/contracts-solidity
forge script script/Deploy.s.sol --rpc-url http://localhost:8547 \
  --broadcast --private-key 0xb6b15c8cb491557369f3c7d2c287b053eb229daa9c22138887752191c9520659

# 4. Test interactions via cast
cast call --rpc-url http://localhost:8547 $STYLUS_ADDRESS "number()(uint256)"
cast send --rpc-url http://localhost:8547 \
  --private-key 0xb6b15c8cb491557369f3c7d2c287b053eb229daa9c22138887752191c9520659 \
  $STYLUS_ADDRESS "increment()"
```

## Coverage

### Solidity

```bash
forge coverage
forge coverage --report lcov  # for IDE integration
```

### Stylus

Stylus unit tests compile for the native host target (not WASM), so standard Rust coverage tools work. `cargo tarpaulin` requires Linux — on macOS, use LLVM source-based coverage instead:

```bash
# Linux
cargo tarpaulin --out Html

# macOS / cross-platform (LLVM source-based coverage)
RUSTFLAGS="-C instrument-coverage" cargo test
grcov . -s . --binary-path ./target/debug/ -t html --branch -o ./coverage/
```

## Test Strategy Recommendations

1. **Unit tests** — test individual contract functions in isolation (both Rust and Solidity)
2. **Fuzz tests** — use Foundry fuzz testing for Solidity; proptest or quickcheck for Rust
3. **Integration tests** — deploy to local devnode and test cross-contract interactions
4. **Fork tests** — use `forge test --fork-url` to test against real testnet state
5. **Frontend tests** — mock viem clients for component testing
