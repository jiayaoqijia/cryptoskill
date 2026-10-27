---
name: celo-official-mcp
description: "A Model Context Protocol (MCP) server for interacting with the Celo blockchain. This server provides comprehensive access to Celo blockchain data, token operations, NFT management, smart contract interactions, transaction handling, and governance operations."
---

# Celo MCP Server

  <!-- mcp-name: org.celo/celo-mcp -->

A Model Context Protocol (MCP) server for interacting with the Celo blockchain. This server provides comprehensive access to Celo blockchain data, token operations, NFT management, smart contract interactions, transaction handling, and governance operations.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/celo-org/celo-mcp
cd celo-mcp
```

2. Install dependencies:

```bash
pip install -e .
```

3. Set up environment variables (optional):

```bash
export CELO_MCP_RPC_URL="https://forno.celo.org"  # Default: Celo mainnet
export CELO_MCP_USE_TESTNET=true                  # Use Celo Sepolia instead
```

## MCP Integration

### Cursor IDE Integration

To use this MCP server with Cursor IDE, add the following configuration to your MCP settings file (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "celo-mcp": {
      "command": "uvx",
      "args": ["--refresh", "celo-mcp"]
    }
  }
}
```

The `--refresh` flag ensures that the latest code is always loaded when the MCP server starts.

### Claude Desktop Integration

For Claude Desktop, add this configuration to your MCP settings file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "celo-mcp": {
      "command": "uvx",
      "args": ["--refresh", "celo-mcp"]
    }
  }
}
```

### Connect remotely (Streamable HTTP)

The server can also run as a remote MCP endpoint over Streamable HTTP, so clients
connect with a single URL — no local Python install. The stdio setup above is
unchanged; this is an additional transport.

Run it in HTTP mode:

```bash
celo-mcp-server --transport http --port 3000
# or via env:
MCP_TRANSPORT=http PORT=3000 celo-mcp-server
```

Then point any remote-capable MCP client at the URL:

```json
{
  "mcpServers": {
    "celo": { "url": "https://<your-host>/mcp" }
  }
}
```

Configuration (environment variables):

| Var | Purpose | Default |
|-----|---------|---------|
| `MCP_TRANSPORT` | `stdio` or `http` | `stdio` |
| `HOST` / `PORT` | HTTP bind host / port | `127.0.0.1` / `3000` |
| `MCP_ALLOWED_HOSTS` | Hostnames accepted by the SDK's DNS-rebinding check, comma-separated. Set to your public hostname(s), or `*` to disable the check | localhost only |
| `MCP_CORS_ORIGINS` | Comma-separated allowed origins (or `*`) | `*` |
| `MCP_RATE_LIMIT` / `MCP_RATE_WINDOW` | Requests per client per window (seconds); `/health` is exempt | `60` / `60` |
| `MCP_TRUST_PROXY` | Number of `X-Forwarded-For` hops your infrastructure appends, so the rate limiter keys on the client rather than the proxy address. `1` for a single reverse proxy, `2` behind a Google external load balancer. Counted from the right — see [deployment](docs/DEPLOYMENT.md) | unset |
| `MCP_AUTH_TOKEN` | If set, requires `Authorization: Bearer <token>` on `/mcp` | unset (open) |
| `CELO_MCP_RPC_URL` | Celo RPC endpoint | Forno for the selected network |
| `CELO_MCP_USE_TESTNET` | Use Celo Sepolia (chain ID 11142220) instead of mainnet | `false` |
| `CELO_MCP_FAUCET_API_KEY` | Enables the faucet tools. Create one at [faucet.celo.org/keys](https://faucet.celo.org/keys) — see [Faucet access](#faucet-access) | unset (faucet tools disabled) |

`GET /health` returns `200` for hosting health checks. See
[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for container/hosting instructions.

## Usage

### Running the Server

```bash
# Run the MCP server
python -m celo_mcp.server

# Or use the CLI entry point
celo-mcp-server
```

### Available Tools

#### Blockchain Data Operations

1. **get_network_status**

   - Get current network status and connection information
   - No parameters required

2. **get_block**

   - Fetch block information by number, hash, or "latest"
   - Parameters: `block_identifier`, `include_transactions` (optional)

3. **get_transaction**

   - Get transaction details by hash
   - Parameters: `tx_hash`

4. **get_account**

   - Get account information including balance and nonce
   - Parameters: `address`

5. **get_latest_blocks**
   - Get information about recent blocks
   - Parameters: `count` (optional, default: 10, max: 100)

#### Token Operations

6. **get_token_info**

   - Get detailed token information (name, symbol, decimals, supply)
   - Parameters: `token_address`

7. **get_token_balance**

   - Get token balance for a specific address
   - Parameters: `token_address`, `address`

8. **get_celo_balances**
   - Get CELO and stable token balances for an address
   - Parameters: `address`

#### NFT Operations

9. **get_nft_info**

   - Get NFT information including metadata and collection details
   - Parameters: `contract_address`, `token_id`

10. **get_nft_balance**
    - Get NFT balance for an address (supports ERC721 and ERC1155)
    - Parameters: `contract_address`, `address`, `token_id` (optional for ERC1155)

#### Smart Contract Operations

11. **call_contract_function**

    - Call a read-only contract function
    - Parameters: `contract_address`, `function_name`, `abi`, `function_args` (optional), `from_address` (optional)

12. **estimate_contract_gas**
    - Estimate gas for a contract function call
    - Parameters: `contract_address`, `function_name`, `abi`, `from_address`, `function_args` (optional), `value` (optional)

#### Transaction Operations

13. **estimate_transaction**

    - Estimate gas and cost for a transaction
    - Parameters: `to`, `from_address`, `value` (optional), `data` (optional)

14. **get_gas_fee_data**
    - Get current gas fee data including EIP-1559 fees
    - No parameters required

#### Governance Operations

15. **get_governance_proposals**

    - Get Celo governance proposals with pagination support
    - Parameters: `include_inactive` (optional), `include_metadata` (optional), `page` (optional), `page_size` (optional), `offset` (optional), `limit` (optional)

16. **get_proposal_details**
    - Get detailed information about a specific governance proposal including content and voting history
    - Parameters: `proposal_id`

#### Staking Operations

17. **get_staking_balances**

    - Get staking balances for an address, including active and pending stakes broken down by validator group
    - Parameters: `address`

18. **get_activatable_stakes**

    - Get information about pending stakes that can be activated for earning rewards
    - Parameters: `address`

19. **get_validator_groups**

    - Get information about all validator groups, including their members, votes, capacity, and performance metrics
    - No parameters required

20. **get_validator_group_details**

    - Get detailed information about a specific validator group including its members and performance data
    - Parameters: `group_address`

21. **get_total_staking_info**
    - Get network-wide staking information including total votes and participation metrics
    - No parameters required

#### Faucet Operations

Both faucet tools are testnet-only and require `CELO_MCP_FAUCET_API_KEY` (see
[Faucet access](#faucet-access) below).

22. **request_faucet_funds**

    - Request testnet CELO for an address. Returns the payout transaction hash if it lands while the request is open, otherwise a `request_key` to poll with
    - Sends **3 CELO** per request, and **CELO only** — no USDm or other stablecoins
    - Parameters: `beneficiary`, optional `network` (`celo-sepolia`), optional `wait` (default `true`)

23. **get_faucet_request_status**
    - Check whether a queued faucet request has paid out
    - Parameters: `request_key`, optional `network` (`celo-sepolia`)

### Faucet access

The faucet's browser flow is gated on reCAPTCHA v3, which scores headless
callers badly, so the faucet tools use its API-key path instead. Create a key at
[faucet.celo.org/keys](https://faucet.celo.org/keys) (sign in with GitHub; up to
2 keys, 90-day expiry) and set it in your MCP client's `env` block:

```json
{
  "mcpServers": {
    "celo-mcp": {
      "command": "uvx",
      "args": ["celo-mcp"],
      "env": { "CELO_MCP_FAUCET_API_KEY": "cfk_..." }
    }
  }
}
```

The key is read from the environment and never passed as a tool argument, so it
does not enter the model's context or the conversation transcript.

Limits are set by the faucet, not by this server: **10 requests per 24 hours**,
counted per GitHub account and per beneficiary address — holding two keys does
not double the allowance. Global daily and 10-minute burst ceilings apply across
all keys on top of that. `celo-sepolia` (chain ID 11142220) is the only
supported network; there is no mainnet faucet.

The faucet publishes its API contract at
[openapi.json](https://faucet.celo.org/openapi.json) and
[llms-full.txt](https://faucet.celo.org/llms-full.txt); treat those as the source
of truth if amounts or limits change.

> **Deployment note:** the HTTP transport is open unless `MCP_AUTH_TOKEN` is
> set. Only configure a faucet key for stdio or authenticated deployments —
> otherwise anyone reaching `/mcp` can spend your daily allowance on arbitrary
> addresses, and the key can be revoked for abuse.

## Key Features

### Token Support

- **ERC20 Standard**: Full support for ERC20 tokens
- **Mento Stable Tokens**: Built-in support for USDm, EURm and BRLm (formerly cUSD, cEUR and cREAL), plus XOFm, KESm, PHPm, COPm and GHSm
- **Balance Queries**: Get token balances with proper decimal formatting
- **Token Information**: Retrieve name, symbol, decimals, and total supply

### NFT Support

- **Multi-Standard**: Support for both ERC721 and ERC1155 standards
- **Automatic Detection**: Automatically detects NFT standard using ERC165
- **Metadata Fetching**: Retrieves and parses NFT metadata from URIs
- **IPFS Support**: Built-in IPFS gateway support for metadata
- **Collection Information**: Get collection-level information

### Smart Contract Interactions

- **Function Calls**: Call read-only contract functions
- **Gas Estimation**: Estimate gas costs for contract interactions
- **ABI Management**: Parse and manage contract ABIs
- **Event Handling**: Retrieve and decode contract events
- **Transaction Building**: Build contract transactions

### Transaction Management

- **Gas Estimation**: Accurate gas estimation for transactions
- **EIP-1559 Support**: Modern fee structure with base fee and priority fee
- **Transaction Simulation**: Simulate transactions before execution
- **Fee Calculation**: Dynamic fee calculation based on network conditions

### Governance Support

- **Proposal Management**: Retrieve and analyze Celo governance proposals
- **Voting Data**: Access proposal voting history and results
- **Metadata Integration**: Fetch proposal metadata from GitHub repositories
- **Pagination Support**: Efficiently browse through large sets of proposals

### Staking Support

- **Staking Balances**: View active and pending stakes by validator group
- **Activation Tracking**: Check which pending stakes can be activated
- **Validator Information**: Comprehensive validator and validator group data
- **Performance Metrics**: Validator scores, election status, and capacity
- **Network Statistics**: Total voting power and staking participation

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=celo_mcp
```

### Code Quality

```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please:

1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Join the community discussions

## Acknowledgments

- Built on the Model Context Protocol (MCP) framework
- Uses Web3.py for Ethereum/Celo blockchain interactions
- Supports the Celo ecosystem and its stable token infrastructure
