---
name: near-tools
description: NEAR Protocol CLI installation and setup guide. Use when: (1) User asks how to install NEAR CLI, (2) User needs help setting up near-cli-rs, (3) User wants to verify NEAR CLI installation, (4) User needs to install near-cli-rs, (5) user wants to use near cli to perform any action on the blockchain. AGENTS MUST ALWAYS get the absolute path of the 'near' binary before execution.
---

# NEAR Tools - NEAR CLI Installation & Setup

> **CRITICAL FOR AGENTS:** Before calling any `near` command, you **MUST** find the absolute path of the `near` binary (e.g., using `which near` or `whereis near`) and use that absolute path in your commands. This ensures consistency across different shell environments.

This skill provides comprehensive guidance for installing and setting up the NEAR Protocol CLI (near-cli-rs) on any platform.

## Installation Methods

Choose the installation method that works best for your system:

### Option 1: Shell Script (Linux, macOS, WSL)

**Best for:** Most Linux and macOS users

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/near/near-cli-rs/releases/latest/download/near-cli-rs-installer.sh | sh
```

**if not add near to PATH:** 
find the near binary by `whereis near`

**Add to PATH:**

```bash
# Temporary (current session only)
export PATH="$HOME/.cargo/bin:$PATH"

# Permanent (add to your shell config)
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc  # For bash
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc   # For zsh
```

Reload your shell or run:
```bash
source ~/.bashrc   # or ~/.zshrc
```

### Option 2: npm/npx (Any Platform with Node.js)

**Best for:** JavaScript/TypeScript developers, Windows users

**Run directly without installation:**
```bash
npx near-cli-rs
```

**Install globally:**
```bash
npm install -g near-cli-rs
```

**Or add to package.json:**
```bash
npm install --save-dev near-cli-rs
```

Then use:
```bash
npx near-cli-rs
```

### Option 3: Windows Installer

**Best for:** Windows users without Node.js or Cargo

1. Visit: https://github.com/near/near-cli-rs/releases/latest
2. Download the Windows MSI installer (e.g., `near-cli-rs-installer-x64.msi`)
3. Double-click the installer and follow the wizard
4. The installer automatically adds NEAR CLI to your PATH

### Option 4: Cargo (Rust)

**Best for:** Rust developers, custom builds

**Prerequisites:** Install Rust first from https://rustup.rs/

**Install:**
```bash
cargo install near-cli-rs
```

**Or install latest from git:**
```bash
cargo install --git https://github.com/near/near-cli-rs
```

**Linux users may need:**
```bash
# Debian/Ubuntu
sudo apt install libudev-dev

# Fedora/Red Hat
sudo dnf install libudev-devel
```

## Verification

After installation, verify it's working:

```bash
near --version
```

Expected output:
```
near-cli-rs 0.23.6  # or newer version
```

**If the command is not found:**

1. Make sure the installation directory is in your PATH:
   ```bash
   echo $PATH | grep cargo  # Check if cargo/bin is in PATH
   ```

2. If not found, add it manually:
   ```bash
   export PATH="$HOME/.cargo/bin:$PATH"
   ```

3. Test again:
   ```bash
   near --version
   ```

## Configuration

### View Configuration Location

```bash
near --help
# Output will show where config is stored, typically:
# "near CLI configuration is stored in ~/.config/near-cli/config.toml"
```

### View Available Commands

```bash
near --help
```

Main command groups:
- **account** - Manage accounts (view, create, import, export)
- **tokens** - Manage token assets (NEAR, FT, NFT)
- **staking** - Manage staking (view, add, withdraw)
- **contract** - Manage smart contracts (deploy, call functions)
- **transaction** - Operate transactions
- **config** - Manage connections in config.toml

## First Steps

### View Your Account Summary

If you already have a NEAR account:

```bash
near account view-account-summary <your-account.near> network-config mainnet now
```

Example:
```bash
near account view-account-summary near network-config mainnet now
```

### Import an Existing Account

If you have a seed phrase or key:

```bash
near account import-account
```

Follow the interactive prompts to sign in.

### Create a New Account

If you don't have an account yet:

```bash
near account create-account
```

Follow the prompts to create a new account (requires existing account to fund it).

## Troubleshooting

### "near: command not found"

**Cause:** NEAR CLI is not in your PATH

**Solution:**
```bash
# For shell script installation
export PATH="$HOME/.cargo/bin:$PATH"

# For npm global installation
export PATH="$(npm config get prefix)/bin:$PATH"

# Make it permanent by adding to ~/.bashrc or ~/.zshrc
```

### "Permission denied" when running installer

**Cause:** Lack of execute permissions

**Solution:**
```bash
chmod +x near-cli-rs-installer.sh
./near-cli-rs-installer.sh
```

### "near-cli-rs-installer.sh: No such file"

**Cause:** Download didn't work or file name changed

**Solution:**
```bash
# Check the releases page manually
curl -s https://api.github.com/repos/near/near-cli-rs/releases/latest | grep "browser_download_url" | grep "installer.sh"
```

### Installation hangs or is slow

**Cause:** Network issues or slow connection

**Solution:**
```bash
# Use a longer timeout with curl
curl --proto '=https' --tlsv1.2 -LsSf --connect-timeout 30 --max-time 300 https://github.com/near/near-cli-rs/releases/latest/download/near-cli-rs-installer.sh | sh
```

## Version Information

- **Latest stable version:** 0.23.6 (as of documentation date)
- **Check for updates:** Visit https://github.com/near/near-cli-rs/releases
- **Update:** Re-run the installation command with the desired version

## Additional Resources

- **Official GitHub:** https://github.com/near/near-cli-rs
- **NEAR Protocol Docs:** https://docs.near.org/
- **NEAR Stack Overflow:** https://stackoverflow.com/questions/tagged/nearprotocol
- **NEAR Discord:** https://discord.gg/near

## Quick Reference

```bash
# Install (Shell script)
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/near/near-cli-rs/releases/latest/download/near-cli-rs-installer.sh | sh

# Install (npx)
npx near-cli-rs

# Verify installation
near --version

# View account
near account view-account-summary <account-id> network-config mainnet now

# Import account
near account import-account

# Help
near --help
near account --help
near tokens --help
```
