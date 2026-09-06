---
name: sui-install
description: >
  Installing, updating, and managing Sui CLI versions with suiup. Use this skill
  when the user needs to install Sui, update to a newer version, switch between
  network-specific versions, resolve "command not found" or version mismatch errors,
  install additional toolchain components (Walrus, MVR, Move Analyzer), or
  troubleshoot suiup commands. Also use when the user sees "client/server api
  version mismatch" warnings or asks about suiup install, update, switch, or show.
---

# Setup & Installation

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information sourced exclusively from [docs.sui.io](https://docs.sui.io).

## System requirements

Sui supports:

- **Linux:** Ubuntu 22.04 (Jammy Jellyfish) or newer
- **macOS:** Monterey or newer
- **Windows:** Windows 10 or 11

## Installing Sui

### suiup (recommended)

`suiup` is the official installer and version manager for the Sui toolchain. It supports installing and switching between different versions of the Sui CLI and other Sui Stack components (Walrus, MVR).

```bash
curl -sSfL https://raw.githubusercontent.com/MystenLabs/suiup/main/install.sh | sh
```

**Windows note:** The `curl | sh` command requires a Unix shell. On Windows, use WSL (Windows Subsystem for Linux) to run the command above, or install through Chocolatey instead (see alternative methods below).

After installing suiup, install the Sui CLI targeting a specific network. The CLI version must match the target network — each network runs a specific protocol version, and a mismatched CLI can cause build failures, transaction errors, or unexpected behavior:

```bash
suiup install sui@testnet    # install the Testnet-compatible version
suiup install sui@mainnet    # install the Mainnet-compatible version
```

Update to the latest version:

```bash
suiup update sui@testnet
```

**Important:** `suiup update` downloads the new version but does not automatically make it the active default. After updating, you must switch to the new version:

```bash
suiup switch sui@testnet     # set the latest installed testnet version as default
```

To verify which versions are installed and which is active:

```bash
suiup show                   # list all installed binaries and their default status
```

### suiup command reference

| Command | Syntax | What it does |
|---|---|---|
| `install` | `suiup install sui@testnet` | Download and install a binary for a network |
| `update` | `suiup update sui@testnet` | Download the latest version (does NOT switch to it) |
| `switch` | `suiup switch sui@testnet` | Set the latest installed version for a network as the active default |
| `show` | `suiup show` | List all installed binaries with versions and defaults |
| `status` | `suiup status` | Show which installed binaries have updates available and the command to update them |
| `self update` | `suiup self update` | Update suiup itself |

The `switch` command takes a `binary@network` argument (for example, `sui@testnet`, `walrus@testnet`, `move-analyzer@testnet`). It does not accept separate positional arguments like `suiup switch sui testnet v1.70.2`.

### Alternative methods

- **Homebrew (macOS/Linux):** `brew install sui`
- **Chocolatey (Windows):** `choco install sui`

These alternatives do not support installing additional Sui Stack components like Walrus or MVR and might take several minutes if prerequisites are not already installed.

### Verify installation

```bash
sui --version
```

If the command returns "sui not found", run `suiup switch sui@testnet` to set the active default. Do **not** suggest manual PATH manipulation (`export PATH=...`) or reinstalling — `suiup switch` is the correct fix.

## Version management

### Keeping Sui up to date

The CLI version should match the target network — each network runs a specific protocol version, and a mismatched CLI can cause build failures or transaction errors. Use the `@network` suffix to update to the correct version:

```bash
suiup update sui@testnet     # update to latest Testnet version
suiup update sui@mainnet     # update to latest Mainnet version
```

### Version mismatches

The CLI version must match the network you are targeting. Common symptoms of a mismatch:

- Build errors mentioning "old dependencies"
- Transaction failures on publish
- Unexpected behavior after network upgrades

Check your version against the network:

```bash
sui --version                 # your installed version
sui client active-env         # which network you are targeting
```

If the version is out of date, update and switch:

```bash
suiup update sui@testnet      # download the latest version
suiup switch sui@testnet      # make it the active default
suiup show                     # verify which version is now active
```

The `client/server api version mismatch` warning in CLI output means your local CLI is older than the network. **Do not ignore this warning** — version mismatches can cause build failures and unexpected behavior. Update and switch to fix it.

### Optional additional tools

Install these only when the user explicitly asks for the tool. They are not part of default setup.

```bash
suiup install move-analyzer   # Move Language Server
suiup install mvr             # Move Registry CLI (onchain package manager)
suiup install walrus          # Walrus CLI for decentralized storage
suiup install site-builder    # Walrus site builder
```

After installing, switch each tool to make it the active default:

```bash
suiup switch move-analyzer@testnet
suiup switch walrus@testnet
```
