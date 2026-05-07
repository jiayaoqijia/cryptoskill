---
name: flow-official-mcp
description: "The Flow network tools for Model Context Protocol (MCP). This package provides a set of tools for interacting with the Flow network through the Model Context Protocol."
---

# flow-official-mcp

_Source: [github.com/onflow/flow-mcp](https://github.com/onflow/flow-mcp). The body below is the upstream README.md captured at the time of registration._

---

# flow-mcp — Model Context Protocol Server for the Flow Network

The Flow network tools for Model Context Protocol (MCP). This package provides a set of tools for interacting with the Flow network through the Model Context Protocol.

<a href="https://glama.ai/mcp/servers/@Outblock/flow-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@Outblock/flow-mcp/badge" alt="Flow MCP server" />
</a>

## Features

- Get FLOW balance for any address
- Get token balance for any Flow token
- Get COA account information
- Get contract source code
- Get detailed account information including storage stats

## Installation

```bash
# Using npm
npm install @outblock/flow-mcp

# Using bun
bun add @outblock/flow-mcp
```

## MCP Configuration

To use this tool with Claude, add the following to your MCP configuration:

```json
{
  "mcpServers": {
    "flow": {
      "command": "npx",
      "args": ["-y", "@outblock/flow-mcp"]
    }
  }
}
```

You can find your MCP configuration at:

- macOS: `~/Library/Application Support/Claude/mcp.json`
- Windows: `%APPDATA%/Claude/mcp.json`
- Linux: `~/.config/Claude/mcp.json`

After adding the configuration, restart Claude to load the new MCP server.

## Tools

### Flow Balance

Get the FLOW balance for any address:

```ts
{
  name: 'get_flow_balance',
  input: {
    address: string,
    network?: 'mainnet' | 'testnet'
  }
}
```

### Account Info

Get detailed account information:

```ts
{
  name: 'get_account_info',
  input: {
    address: string,
    network?: 'mainnet' | 'testnet'
  }
}
```

### Token Balance

Get balance for any Flow token:

```ts
{
  name: 'get_token_balance',
  input: {
    address: string,
    network?: 'mainnet' | 'testnet'
  }
}
```

### COA Account

Get COA account information:

```ts
{
  name: 'get_coa_account',
  input: {
    address: string,
    network?: 'mainnet' | 'testnet'
  }
}
```

### Get Contract

Get contract source code:

```ts
{
  name: 'get_contract',
  input: {
    address: string,
    contractName: string,
    network?: 'mainnet' | 'testnet'
  }
}
```

## 📂 Project Structure

```text
flow-mcp/
├── src/
│   ├── tools/          # MCP tools implementation
│   │   ├── flowBalance/    # Flow balance tool
│   │   ├── accountInfo/    # Account info tool
│   │   ├── tokenBalance/   # Token balance tool
│   │   ├── coaAccount/     # COA account tool
│   │   └── getContract/    # Contract source tool
│   ├── utils/          # Shared utilities
│   ├── prompts/        # MCP prompts
│   ├── types/          # Type definitions
│   └── bin/           # CLI implementation
├── biome.json         # Linting configuration
├── tsconfig.json      # TypeScript configuration
└── package.json       # Project dependencies
```

## 🛠️ Development

This project uses FastMCP for development and testing. FastMCP provides a streamlined development experience for MCP servers.

```bash
# Install dependencies
bun install

# Format code
bun run format

# Run tests
bun test

# Run development server
bun run dev

# Inspect the server
bun run inspect

# Build
bun run build
```

To add your development MCP server to Claude Desktop:

1. Build the project:

   ```bash
   bun run build
   ```

2. Add to your Claude Desktop config:

   ```json
   // You only need the argument if you need to pass arguments to your server
   {
     "mcpServers": {
       "your-server-name": {
         "command": "node",
         "args": ["/path/to/your/project/dist/main.js", "some_argument"]
       }
     }
   }
   ```

### Creating New Tools

The project includes a script to help create new MCP tools:

```bash
bun run scripts/create-tool.ts <tool-name>
```

This will:

1. Create a new tool directory under `src/tools/<tool-name>`
2. Generate the basic tool structure including:
   - index.ts (main implementation)
   - schema.ts (JSON schema for tool parameters)
   - test.ts (test file)
3. Update the tools index file to export the new tool

Example:

```bash
bun run scripts/create-tool.ts weather
```

### Commit Message Format

- `feat`: New feature (bumps minor version)
- `fix`: Bug fix (bumps patch version)
- `BREAKING CHANGE`: Breaking change (bumps major version)

## 📜 Version Management

This project uses [standard-version](https://github.com/conventional-changelog/standard-version) for automated version management. Run `bun run release` to create a new version.

## 📦 Publishing to npm

1. Ensure you're logged in to npm:

   ```bash
   npm login
   ```

2. Build the project:

   ```bash
   bun run build
   ```

3. Publish the package:

   ```bash
   npm publish
   ```

Remember to update the version number using `bun run release` before publishing new versions.

## License

MIT License - see LICENSE for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## About Flow

This repo is part of the [Flow network](https://flow.com), a Layer 1 blockchain built for consumer applications, AI agents, and DeFi at scale.

- Developer docs: https://developers.flow.com
- Cadence language: https://cadence-lang.org
- Community: [Flow Discord](https://discord.gg/flow) · [Flow Forum](https://forum.flow.com)
- Governance: [Flow Improvement Proposals](https://github.com/onflow/flips)
