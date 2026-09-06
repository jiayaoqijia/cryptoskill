# DAO Proposal Starter

Create fully functional DAO governance proposals with function encoding, voting parameters, and execution timelines.

## Features
- **Function Encoding**: Encodes contract calls with selectors and ABI parameters
- **Multi-Action Support**: Support for multiple target contracts and functions in single proposal
- **DAO Type Support**: Compound, Aave, Uniswap, and generic governance models
- **Voting Parameters**: Automatic voting period calculation based on DAO type
- **Timelock Support**: 3-day execution delay for security
- **IPFS Hashing**: Generates IPFS hashes for proposal descriptions
- **Address Validation**: Validates all target contract addresses

## Usage

```bash
# Create a simple proposal
echo '{
  "title": "Increase Protocol Fee to 0.05%",
  "description": "This proposal increases the protocol fee from 0.03% to 0.05% to enhance treasury sustainability. The fee increase will be implemented through the FeeCollector contract upgrade.",
  "targets": ["0x1234567890123456789012345678901234567890"],
  "functions": ["setFee(uint256)"],
  "params": [[50000000000000000]],
  "values": [0],
  "dao_type": "compound"
}' | python3 scripts/main.py
```

## Parameters
- `title` (required): Proposal title (min 5 chars)
- `description` (required): Detailed description (min 20 chars)
- `targets` (array): Contract addresses to call
- `functions` (array): Function signatures (e.g., "setFee(uint256)")
- `params` (array): Function parameters as arrays
- `values` (array): ETH values to send with each call
- `dao_type` (string): "compound", "aave", "uniswap", or "generic"
- `proposer` (optional): Proposer address, auto-generated if omitted
- `voting_power` (optional): Required voting power, default 1000000

## Response
Returns complete proposal object with:
- Proposal ID (derived from proposal hash)
- Voting timeline based on DAO type
- Encoded function calls (calldatas)
- Voting parameters
- Execution timeline with timelock delay
