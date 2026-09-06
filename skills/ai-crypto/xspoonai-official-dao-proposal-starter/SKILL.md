---
name: dao-proposal-starter
track: web3-core-operations
version: 1.0.0
summary: Create fully functional DAO governance proposals with function encoding and voting parameters
---

## Description

Create fully functional DAO governance proposals with function call encoding, multi-action support, and DAO-type-specific voting parameters. Encodes contract function calls with keccak256 hashing, validates addresses, and calculates voting timelines based on governance model.

## Inputs

```json
{
  "title": "Proposal title (min 5 chars)",
  "description": "Detailed proposal description (min 20 chars)",
  "targets": ["0xcontract1", "0xcontract2"],
  "functions": ["setFee(uint256)", "transferFunds(address,uint256)"],
  "params": [[50000000000000000], ["0xrecipient", 1000000000000000000]],
  "values": [0, 0],
  "dao_type": "compound|aave|uniswap|generic",
  "proposer": "0xproposer_address (optional)",
  "voting_power": 1000000
}
```

## Outputs

```json
{
  "success": true,
  "proposal": {
    "id": "0x7a2c...",
    "title": "Increase Protocol Fee to 0.05%",
    "description": "This proposal increases the protocol fee...",
    "targets": ["0x1234567890123456789012345678901234567890"],
    "functions": ["setFee(uint256)"],
    "calldatas": ["0x69d4..."],
    "values": [0],
    "voting_delay": 1,
    "voting_period": 13140,
    "proposal_threshold": 65000,
    "quorum_votes": 400000,
    "proposer": "0xproposer...",
    "for_votes": 0,
    "against_votes": 0,
    "abstain_votes": 0,
    "created_at": "2026-02-06T10:30:45.123456+00:00",
    "voting_starts": "2026-02-07T10:30:45.123456+00:00",
    "voting_ends": "2026-03-20T10:30:45.123456+00:00",
    "execution_eta": "2026-03-23T10:30:45.123456+00:00",
    "cancelled": false,
    "executed": false
  }
}
```

## Usage

### Create Compound DAO Proposal
```bash
echo '{
  "title": "Increase Protocol Fee to 0.05%",
  "description": "This proposal increases the protocol fee from 0.03% to 0.05% to enhance treasury sustainability.",
  "targets": ["0x1234567890123456789012345678901234567890"],
  "functions": ["setFee(uint256)"],
  "params": [[50000000000000000]],
  "values": [0],
  "dao_type": "compound"
}' | python3 scripts/main.py
```

### Create Multi-Action Aave Proposal
```bash
echo '{
  "title": "Update Risk Parameters",
  "description": "Proposal to update collateral and risk parameters across multiple assets.",
  "targets": ["0xaaaa...", "0xbbbb..."],
  "functions": ["setCollateralFactor(address,uint256)", "setReserveFactor(address,uint256)"],
  "params": [["0xtoken1", 750000000000000000], ["0xtoken2", 100000000000000000]],
  "values": [0, 0],
  "dao_type": "aave"
}' | python3 scripts/main.py
```

## Examples

### Example 1: Single Action Compound Proposal
```bash
$ python3 scripts/main.py < input.json
{
  "success": true,
  "proposal": {
    "id": "0x7a2c8f9e1b4d...",
    "title": "Increase Protocol Fee to 0.05%",
    "targets": ["0x1234567890123456789012345678901234567890"],
    "functions": ["setFee(uint256)"],
    "calldatas": ["0x69d427e0000000000000000000000000000000000000000000000b1a2bc2ec50000"],
    "voting_period": 13140,
    "voting_delay": 1,
    "quorum_votes": 400000,
    "proposer": "0x1111111111111111111111111111111111111111",
    "voting_starts": "2026-02-07T10:30:45+00:00",
    "voting_ends": "2026-03-20T10:30:45+00:00"
  }
}
```

### Example 2: Multi-Action Aave Proposal with Different Voting Period
```bash
$ python3 scripts/main.py < aave_proposal.json
{
  "success": true,
  "proposal": {
    "id": "0x9f8e7d6c5b4a...",
    "title": "Update Risk Parameters",
    "targets": ["0xaaaa...", "0xbbbb..."],
    "functions": ["setCollateralFactor(address,uint256)", "setReserveFactor(address,uint256)"],
    "calldatas": ["0xaabbcc11...", "0xddeeff22..."],
    "voting_period": 80000,
    "voting_delay": 1,
    "quorum_votes": 320000,
    "proposer": "0x2222222222222222222222222222222222222222",
    "voting_starts": "2026-02-07T10:30:45+00:00",
    "voting_ends": "2026-03-27T10:30:45+00:00"
  }
}
```

## Error Handling

### Validation Error
```json
{
  "ok": false,
  "error": "validation_error",
  "details": {
    "field": "title",
    "message": "Title must be at least 5 characters long"
  }
}
```

### Invalid Address
```json
{
  "ok": false,
  "error": "validation_error",
  "details": {
    "field": "targets",
    "message": "Invalid Ethereum address format: 0xinvalid"
  }
}
```

### Function Encoding Error
```json
{
  "ok": false,
  "error": "system_error",
  "details": {
    "message": "Array length mismatch: 2 targets but 3 functions provided"
  }
}
```

## Features

- **Function Encoding**: Encodes contract calls with keccak256-based selectors
- **Multi-Action Support**: Multiple targets and functions in single proposal
- **DAO Support**: Compound, Aave, Uniswap, and generic governance models
- **Address Validation**: Validates Ethereum address format (0x + 40 hex chars)
- **Voting Calculation**: DAO-specific voting blocks (Compound: 13140, Aave: 80000, Uniswap: 25200)
- **Timelock Support**: 3-day execution delay for security
- **IPFS Hashing**: Generates IPFS-style hashes for proposals
- **Error Classification**: Validation vs system errors for proper handling
