# near-tools — NEAR Protocol CLI Skill

> **Install and use the NEAR Protocol CLI (`near-cli-rs`) with OpenClaw AI agents**

## 🎯 What It Does

Helps AI agents install, configure, and use the NEAR CLI to interact with the NEAR Protocol blockchain:

- ✅ Multi-platform installation (Linux, macOS, Windows, WSL)
- ✅ Account management (view, create, import/export)
- ✅ Token operations (NEAR, FT, NFT)
- ✅ Staking management
- ✅ Smart contract deployment and interaction
- ✅ Transaction operations

## 📦 Installation

### For Users

No installation needed! This is a reference skill that provides installation instructions for the NEAR CLI itself.

### For AI Agents

**Critical**: Before calling any `near` command, agents MUST get the absolute path:

```bash
# Find the absolute path
which near
# or
whereis near

# Use the absolute path in commands
/root/.cargo/bin/near account view-account-summary cuongdcdev.near network-config mainnet now
```

## 🚀 Quick Start

### Install NEAR CLI

**Linux/macOS/WSL (recommended):**
```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/near/near-cli-rs/releases/latest/download/near-cli-rs-installer.sh | sh
```

**npm/npx (any platform with Node.js):**
```bash
# Run without installing
npx near-cli-rs

# Or install globally
npm install -g near-cli-rs
```

**Windows:**
Download the MSI installer from [GitHub Releases](https://github.com/near/near-cli-rs/releases/latest)

### Verify Installation

```bash
near --version
# Expected: near-cli-rs 0.23.6 or newer
```

### View Account Balance

```bash
near account view-account-summary <account-id> network-config mainnet now

# Example
near account view-account-summary cuongdcdev.near network-config mainnet now
```

## 📖 Common Commands

### Account Operations
```bash
# View account details
near account view-account-summary <account-id> network-config mainnet now

# Import existing account
near account import-account

# Create new account
near account create-account

# Export account credentials
near account export-account
```

### Token Operations
```bash
# View NEAR balance
near tokens <account-id> network-config mainnet now

# Send NEAR tokens
near tokens <sender-account> send-near <receiver-account> <amount> network-config mainnet sign-with-keychain send
```

### Staking
```bash
# View staking info
near staking <account-id> network-config mainnet now

# Stake NEAR
near staking <account-id> stake-with <validator-id> <amount> network-config mainnet sign-with-keychain send
```

### Smart Contracts
```bash
# Deploy contract
near contract deploy <account-id> use-file <wasm-file> network-config mainnet sign-with-keychain send

# Call contract method
near contract call-function as-transaction <contract-id> <method-name> json-args '<args>' prepaid-gas '100.0 Tgas' attached-deposit '0 NEAR' network-config mainnet sign-with-keychain send
```

## 🛠️ Configuration

### Config Location
- **Linux/macOS**: `~/.config/near-cli/config.toml`
- **Windows**: `%APPDATA%\near-cli\config.toml`

### Add to PATH (if needed)

**Shell script installation:**
```bash
export PATH="$HOME/.cargo/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
```

**npm global installation:**
```bash
export PATH="$(npm config get prefix)/bin:$PATH"
```

## 🐛 Troubleshooting

### "near: command not found"

**Check installation location:**
```bash
which near
whereis near
```

**Add to PATH:**
```bash
# For cargo install
export PATH="$HOME/.cargo/bin:$PATH"

# For npm install
export PATH="$(npm config get prefix)/bin:$PATH"
```

### Permission denied

```bash
chmod +x ~/.cargo/bin/near
```

### Slow installation

```bash
# Use longer timeout
curl --proto '=https' --tlsv1.2 -LsSf --connect-timeout 30 --max-time 300 \
  https://github.com/near/near-cli-rs/releases/latest/download/near-cli-rs-installer.sh | sh
```

## 📚 Resources

- **Official Docs**: https://docs.near.org/
- **GitHub**: https://github.com/near/near-cli-rs
- **NEAR Explorer**: https://nearblocks.io/
- **Discord**: https://discord.gg/near
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/nearprotocol

## 🔗 Related Skills

- **near-intents**: Universal cross-chain swap & bridge
- **near-getpay**: Accept crypto payments via beautiful payment pages

## 📝 License

MIT — This skill is documentation-only and references the official NEAR CLI project.

## 🤝 Contributing

Found an issue or want to improve this skill?

1. Check existing issues at the [NEAR CLI repo](https://github.com/near/near-cli-rs/issues)
2. For this skill specifically, open an issue or PR in your skill repository

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-15  
**Compatible with**: NEAR CLI v0.23.6+
