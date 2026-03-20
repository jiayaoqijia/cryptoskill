# Smart Contract Security Checklist

## Before Deployment

### Access Control
- [ ] All sensitive functions have proper access modifiers
- [ ] Owner/admin functions use `onlyOwner` or similar modifiers
- [ ] Role-based access control is properly implemented
- [ ] No functions are accidentally left public

### Reentrancy
- [ ] State changes happen before external calls
- [ ] Use `nonReentrant` modifier for functions that transfer value
- [ ] Follow checks-effects-interactions pattern

### Integer Handling
- [ ] Solidity 0.8+ is used (built-in overflow protection)
- [ ] Unchecked blocks are used intentionally and safely
- [ ] Division by zero is prevented

### Input Validation
- [ ] All external inputs are validated
- [ ] Array lengths are checked before loops
- [ ] Address(0) checks where appropriate

### Token Handling
- [ ] Safe transfer methods used for ERC20 tokens
- [ ] Return values from token transfers are checked
- [ ] Approve race condition is handled

### Gas Considerations
- [ ] No unbounded loops over user-controlled data
- [ ] Storage operations minimized
- [ ] Events used instead of storage for historical data

### Contract Interactions
- [ ] External contract calls are minimized
- [ ] Return values from external calls are checked
- [ ] Low-level calls have proper error handling

## Testing Requirements

- [ ] Unit tests for all functions
- [ ] Edge case testing
- [ ] Access control tests
- [ ] Revert condition tests
- [ ] Integration tests with external contracts

## Pre-Mainnet

- [ ] Contract verified on block explorer
- [ ] Audit completed (for high-value contracts)
- [ ] Emergency pause mechanism if needed
- [ ] Upgrade path planned if upgradeable
