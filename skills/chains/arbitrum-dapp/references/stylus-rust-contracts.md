# Stylus Rust Contracts

## Prerequisites

- Rust 1.81+
- `wasm32-unknown-unknown` target: `rustup target add wasm32-unknown-unknown`
- `cargo-stylus` CLI: `cargo install --force cargo-stylus`
- Docker (required for `cargo stylus check` and `deploy`)

## Project Setup

```bash
cargo stylus new my-contract
cd my-contract
```

This generates a counter contract template with `Cargo.toml` pre-configured for Stylus.

## Cargo.toml

```toml
[dependencies]
stylus-sdk = "0.10.0"
alloy-primitives = "1.0"
alloy-sol-types = "1.0"

[dev-dependencies]
stylus-sdk = { version = "0.10.0", features = ["stylus-test"] }

[features]
export-abi = ["stylus-sdk/export-abi"]
```

## Storage

Use the `sol_storage!` macro to define Solidity-compatible storage layouts:

```rust
use stylus_sdk::prelude::*;

sol_storage! {
    #[entrypoint]
    pub struct Counter {
        uint256 number;
    }
}
```

### Supported storage types

- Primitives: `uint256`, `int256`, `bool`, `address`, `bytes32`
- Collections: `mapping(address => uint256)`, `address[]`
- Nested structs via composition

### Storage access

```rust
// Read
let value = self.number.get();

// Write
self.number.set(value + U256::from(1));
```

## Public Methods

Use the `#[public]` attribute to expose methods via the ABI:

```rust
#[public]
impl Counter {
    pub fn number(&self) -> U256 {
        self.number.get()
    }

    pub fn set_number(&mut self, new_number: U256) {
        self.number.set(new_number);
    }

    pub fn increment(&mut self) {
        let number = self.number.get();
        self.number.set(number + U256::from(1));
    }
}
```

## Payable Methods

```rust
#[payable]
pub fn deposit(&mut self) {
    let value = msg::value();
    // handle deposit
}
```

## Events

```rust
use alloy_sol_types::sol;

sol! {
    event Transfer(address indexed from, address indexed to, uint256 value);
}

// Emit in a method
evm::log(Transfer {
    from: caller,
    to: recipient,
    value: amount,
});
```

## Cross-Contract Calls

Stylus contracts can call Solidity contracts and vice versa:

```rust
use stylus_sdk::call::RawCall;

let result = RawCall::new()
    .call(contract_address, &calldata)?;
```

Or generate type-safe bindings using `sol_interface!`:

```rust
sol_interface! {
    interface IERC20 {
        function balanceOf(address owner) external view returns (uint256);
        function transfer(address to, uint256 amount) external returns (bool);
    }
}

let token = IERC20::new(token_address);
let balance = token.balance_of(self, owner)?;
```

## Error Handling

Return `Result` types from public methods:

```rust
#[derive(SolidityError)]
pub enum MyError {
    InsufficientBalance(InsufficientBalance),
    Unauthorized(Unauthorized),
}

sol! {
    error InsufficientBalance(uint256 available, uint256 required);
    error Unauthorized(address caller);
}
```

## Validation and Deployment

```bash
# Check contract compiles and is valid for Stylus
cargo stylus check --endpoint http://localhost:8547

# Estimate deployment gas
cargo stylus deploy --endpoint http://localhost:8547 \
  --private-key 0x... --estimate-gas

# Deploy
cargo stylus deploy --endpoint http://localhost:8547 \
  --private-key 0x...

# Export Solidity ABI
cargo stylus export-abi
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_increment() {
        let mut contract = Counter::default();
        contract.set_number(U256::from(0));
        contract.increment();
        assert_eq!(contract.number(), U256::from(1));
    }
}
```

Run with `cargo test`. The `stylus-test` feature enables simulating transaction context, msg::sender(), msg::value(), and storage operations without deployment.
