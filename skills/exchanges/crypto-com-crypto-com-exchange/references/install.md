# Installing cdcx CLI

The `cdcx` CLI is the Crypto.com Exchange command-line tool that handles API calls, authentication, safety enforcement, and output formatting.

## Quick Install (recommended)

```bash
npx @cryptocom/cdcx-cli@latest --version
```

This downloads and runs the latest version via npm. No global install needed — `npx` caches the binary automatically.

## Global Install via npm

```bash
npm install -g @cryptocom/cdcx-cli
cdcx --version
```

## Install via curl (direct binary)

```bash
curl -fsSL https://raw.githubusercontent.com/crypto-com/cdcx-cli/main/install.sh | sh
```

Downloads the pre-built Rust binary for your platform (macOS arm64/x64, Linux x64).

## Install from Source (Rust)

```bash
cargo install cdcx-cli
```

Requires Rust toolchain (stable).

## Verify Installation

```bash
cdcx --version
# cdcx 1.2.4

# Public endpoint (no auth needed)
cdcx market ticker BTC_USDT -o json
```

## Update

```bash
# npm
npm update -g @cryptocom/cdcx-cli

# Or just use npx (always gets latest)
npx @cryptocom/cdcx-cli@latest market ticker BTC_USDT
```

## Platform Support

| Platform | Architecture | Method |
|----------|-------------|--------|
| macOS | arm64 (Apple Silicon) | npm, curl, cargo |
| macOS | x64 (Intel) | npm, curl, cargo |
| Linux | x64 | npm, curl, cargo |
| Windows | x64 | npm, cargo |

## AI Agent Plugin Install

For AI coding tools (Claude Code, Cursor, Codex), the CLI is available as a plugin:

```bash
# Claude Code
claude plugin add @cryptocom/cdcx-cli

# Or configure manually in .claude/settings.json:
# "mcpServers": {
#   "cdcx": {
#     "command": "npx",
#     "args": ["-y", "@cryptocom/cdcx-cli@latest", "mcp"]
#   }
# }
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `command not found: cdcx` | Use `npx @cryptocom/cdcx-cli@latest` or add npm global bin to PATH |
| Permission denied | `chmod +x $(which cdcx)` or reinstall with `sudo npm i -g` |
| Old version | `npm update -g @cryptocom/cdcx-cli` or `cdcx update` |
| Network error on install | Check proxy settings; try `curl` method instead |
