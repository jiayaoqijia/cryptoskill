# Changelog

All notable changes to `gate-dex-wallet` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.11-1] - 2026-03-11

### Added

- **One-click installation script**: `install.sh` supports multi-platform auto configuration
  - Auto-detect AI platforms (Cursor, Claude Code, Codex CLI, OpenCode, OpenClaw)
  - Create corresponding MCP configuration and Skill routing files for each platform
  - Unified configuration of `gate-wallet` MCP Server connection
- **Unified wallet skill architecture**: Integrated authentication, assets, transfer, DApp four major modules into single Skill entry point
- **Sub-function routing system**: Organize complete implementation specifications for each module through `references/` directory
  - `references/auth.md` — Authentication module (Google OAuth, Token management)
  - `references/transfer.md` — Comprehensive wallet (authentication, assets, transfer, DApp) module (Gas estimation, signing, broadcasting)
  - `references/dapp.md` — DApp module (wallet connection, message signing, contract interaction)
- **Asset query tools** (7 tools): Balance, total assets, addresses, chain config, transaction history, etc.
- **Smart routing distribution**: Automatically route to corresponding sub-module implementations based on user intent
- **Unified authentication management**: All modules share MCP token and session state
- **MCP Server connection detection**: Initial session detection + runtime error fallback
- Support for 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)

### Changed

- **Architecture refactor**: Integrated from scattered 4 independent Skills (auth/wallet/transfer/dapp) into single unified Skill
- **Directory structure**: Adopted `gate-dex-wallet/references/` pattern, referencing [gate-skills](https://github.com/gate/gate-skills/tree/master/skills/gate-exchange-futures) project architecture
- **Routing optimization**: Main SKILL.md serves as distribution center, sub-module specifications maintained independently

### Deprecated

- Independent `gate-dex-wallet/references/auth`, `gate-dex-wallet/references/transfer`, `gate-dex-wallet/references/dapp` Skill directories
- Cross-Skill complex routing, simplified to single Skill internal module routing