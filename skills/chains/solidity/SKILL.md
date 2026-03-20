---
name: Solidity
description: Avoid common Solidity mistakes — reentrancy, gas traps, storage collisions, and security pitfalls.
metadata: {"clawdbot":{"emoji":"⟠","os":["linux","darwin","win32"]}}
---

## Reentrancy
- External calls before state updates — attacker can re-enter before state changes
- Checks-Effects-Interactions pattern — validate, update state, THEN external call
- `ReentrancyGuard` from OpenZeppelin — use `nonReentrant` modifier on vulnerable functions
- `transfer()` and `send()` have 2300 gas limit — but don't rely on this for security

## Integer Handling
- Solidity 0.8+ reverts on overflow — but `unchecked {}` blocks bypass this
- Division truncates toward zero — `5 / 2 = 2`, no decimals
- Use fixed-point math for precision — multiply before divide, or use libraries
- `type(uint256).max` for max value — don't hardcode large numbers

## Gas Gotchas
- Unbounded loops can exceed block gas limit — paginate or limit iterations
- Storage writes cost 20k gas — memory/calldata much cheaper
- `delete` refunds gas but has limits — refund capped, don't rely on it
- Reading storage in loop — cache in memory variable first

## Visibility and Access
- State variables default to `internal` — not `private`, derived contracts see them
- `private` doesn't mean hidden — all blockchain data is public, just not accessible from other contracts
- `tx.origin` is original sender — use `msg.sender`, `tx.origin` enables phishing attacks
- `external` can't be called internally — use `public` or `this.func()` (wastes gas)

## Ether Handling
- `payable` required to receive ether — non-payable functions reject ether
- `selfdestruct` sends ether bypassing fallback — contract can receive ether without receive function
- Check return value of `send()` — returns false on failure, doesn't revert
- `call{value: x}("")` preferred over `transfer()` — forward all gas, check return value

## Storage vs Memory
- `storage` persists, `memory` is temporary — storage costs gas, memory doesn't persist
- Structs/arrays parameter default to `memory` — explicit `storage` to modify state
- `calldata` for external function inputs — read-only, cheaper than memory
- Storage layout matters for upgrades — never reorder or remove storage variables

## Upgradeable Contracts
- Constructors don't run in proxies — use `initialize()` with `initializer` modifier
- Storage collision between proxy and impl — use EIP-1967 storage slots
- Never `selfdestruct` implementation — breaks all proxies pointing to it
- `delegatecall` uses caller's storage — impl contract storage layout must match proxy

## Common Mistakes
- Block timestamp can be manipulated slightly — don't use for randomness or precise timing
- `require` for user errors, `assert` for invariants — assert failures indicate bugs
- String comparison with `==` doesn't work — use `keccak256(abi.encodePacked(a)) == keccak256(abi.encodePacked(b))`
- Events not indexed — first 3 params can be `indexed` for efficient filtering
