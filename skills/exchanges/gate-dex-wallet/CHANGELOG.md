# Changelog

All notable changes to `gate-dex-wallet` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Unreleased

### Changed

- **tools/tx-checkin**: Fixed gateway base URL to **`https://webapi.w3-api.com/api/web/v1/web3-gv-api`** (check-in POST: **`.../api/v1/tx/checkin`**). Prebuilt binaries in **`tools/tx-checkin/bin/`** rebuilt.
- **tools/tx-checkin**: Optional **`TX_CHECKIN_GATEWAY_BASE`** env (automation/CI only; not user-facing in skill docs) overrides the gateway URL prefix.
- **references/cli.md**: version `2026.4.3-1`; tx-checkin integrated as mandatory step in On-Chain Operation Flow (preview → confirm → tx-checkin → execute); `send`, `swap`, `openapi-swap` commands annotated with tx-checkin requirement; new "tx-checkin Binary for CLI Operations" section with step-by-step flows; Security Rules updated (rule 3: terminal tx-checkin before signing); Common Pitfall #24 added; Capability Boundaries updated with signing prerequisite note
- **install.sh**: Removed misleading placeholder Bearer token from Cursor and Codex MCP configs (OAuth login populates at runtime); Claude Code install now appends to existing CLAUDE.md instead of overwriting; Codex config.toml checks for existing gate-dex entry before appending; AGENTS.md uses same append-not-overwrite logic; OpenClaw removed hardcoded default API key and unused key prompt
- **install_cli.sh**: OpenAPI credential input now escaped via `jq` (with `sed` fallback) to prevent JSON injection from special characters in API keys

## [2026.3.31-2] - 2026-03-31

### Added

- **references/tx-checkin.md**: New mandatory terminal tx check-in module — documents CLI usage (`-tx-bundle-file`, `-message`, `-intent-file`, `-body-file`), `txBundle` preview field flow, `checkin_token` session binding, OTP handling, and credential auto-discovery from `~/.cursor/mcp.json`
- **tools/tx-checkin/**: Pre-built `tx-checkin` binary (Go); gateway URL fixed to `https://test-api.web3gate.io/api/app/v1/web3-gv-api`

### Changed

- **SKILL.md**: version `2026.3.31-2`; description updated to mention mandatory tx-checkin; new "Signing gate — terminal tx-checkin (mandatory)" section; routing table transfer row adds tx-checkin; new any-signing routing row added; DApp row adds tx-checkin; Follow-up routing adds tx-checkin row
- **references/transfer.md**: version `2026.3.31-2`; `dex_tx_transfer_preview` return fields updated (`unsigned_tx_hex`, `txBundle`); tool call chain adds step 6 tx-checkin; Flow A Step 9 tx-checkin mandatory before sign; all happy-path examples and batch flow updated
- **references/withdraw.md**: version `2026.3.31-1`; tool call chain adds step 12 tx-checkin; Flow A adds Step 10 mandatory tx-checkin; `dex_wallet_sign_transaction` table entry updated; Flow B step references updated to 3-12; relationship-to-modules line adds tx-checkin.md
- **references/dapp.md**: version `2026.3.31-1`; description updated; "Signing prerequisite" block added after prerequisites; `dex_wallet_sign_message` and `dex_wallet_sign_transaction` descriptions updated; Flow B Step 4, Flow C Step 9, Flow D Step 5, Flow E Step 6 all add mandatory tx-checkin; confirmation template note and security rule 4 updated
- **references/x402.md**: version `2026.3.31-1`; signing/check-in note added to Prerequisites section for `dex_tx_x402_fetch` internal-signing flows

---

## [2026.3.26-1] - 2026-03-26

### Changed

- **gate-runtime-rules.md** and **gate-skills-disambiguation.md**: Removed per-skill duplicate copies from `gate-dex-wallet/`; SKILL.md updated to reference shared root-level files via GitHub URL
- **gate-skills-disambiguation.md**: Simplified domain definition table; consolidated signal word routing; added DEX withdraw-to-exchange / UID binding routing entries; Scenario 9 (DEX withdraw-to-exchange) added; Scenario 13 updated with UID binding trigger and confirmation prompt; Scenario 14 updated with ETH2 staking note; updated link references from GitHub URLs to relative paths

---

## [2026.3.25-1] - 2026-03-25

### Added

- **references/withdraw.md**: New on-chain withdraw module — exchange binding (`dex_wallet_get_wallet_type`, `dex_wallet_get_bindings`, `dex_wallet_bind_exchange_uid`, `dex_wallet_replace_binding`, `dex_wallet_google_gate_bind_start`), deposit-address resolution with min-deposit enforcement (`dex_withdraw_deposit_address`), mandatory destination disambiguation (Flow 0), Flow A (withdraw to Gate Exchange), Flow B (withdraw to custom address)

### Changed

- **SKILL.md**: version `2026.3.25-1`; withdraw module added to routing table and Applicable Scenarios; link format updated to `references/` subdirectory style
- **references/withdraw.md**: Added destination switch flow (Flow 0) for disambiguation before execution; removed Chinese text from field descriptions
- **All `references/*.md` frontmatter**: Normalized from nested `metadata: {version, updated}` or `## name:` heading syntax to top-level `version` / `updated` YAML fields; description converted from multi-line `>` blocks to single-line quoted strings

### Fixed

- **gate-skills-disambiguation.md**: Relative path reference for `gate-runtime-rules.md` link updated

---

## [2026.3.24-1] - 2026-03-24

### Changed

- **SKILL.md streamlined**: Removed redundant sections already covered by `gate-runtime-rules.md` (Auto-Update, Authentication State); removed Cross-Skill Collaboration (covered in `references/asset-query.md`); merged Security Rules from 6 to 3 (auth routing now defers to runtime-rules §3)
- **SKILL.md frontmatter**: Flattened nested `metadata` structure to top-level `version`/`updated` fields
- **Supported Chains**: Condensed from full table to single-line summary
- **Setup Guide**: Normalized MCP server name from `gate-wallet` to `gate-dex` in CLI examples
- **gate-runtime-rules.md**: Minor formatting fixes
- **gate-skills-disambiguation.md**: Minor formatting fixes

## [2026.3.19-2] - 2026-03-19

### Changed

- **x402 documentation** ([references/x402.md](./references/x402.md)): Align with wallet MCP behavior — **accept priority** (Solana exact → EVM exact → Solana upto → EVM upto), **EVM upto** (Permit2, `extra.facilitator`), **Solana upto** (max-amount SPL signing note), error-handling table; document **English** `dex_tx_x402_fetch` tool description as returned by MCP
- **SKILL.md** frontmatter: x402 capability line updated to mention exact/upto and `dex_tx_x402_fetch`

## [2026.3.19-1] - 2026-03-19

### Added

- **x402 Payment Skill**: New sub-module [references/x402.md](./references/x402.md) for HTTP 402 Payment Required flows
  - Trigger: "402 payment", "x402 pay", "payment required", "pay for API/URL"
  - Tool: `dex_tx_x402_fetch` — request URL; on 402, pay with wallet (EVM EIP-3009 or Solana SPL) and retry
  - Routing: SKILL.md and README.md updated with x402 module and follow-up routing
- **Token list balance fields**: Documented use of `orignCoinNumber` (raw amount) instead of `coinNumber` (display-formatted) for `dex_wallet_get_token_list` parsing; updated `references/dapp.md` balance step

## [2026.3.18-1] - 2026-03-18

### Changed

- **SKILL.md Streamlined**: Removed verbose MCP detection logic, OpenClaw integration, and Claude Code specific sections; converted to pure routing layer pointing to `references/`
- **MCP Tool Naming**: Restored `dex_` prefix for all tool references across SKILL.md and references/

### Fixed

- **Tool Naming Alignment**: Renamed legacy `auth.refresh_token` → `dex_auth_refresh_token`, `tx.history_list` → `dex_tx_history_list`, `tx.swap_detail` → `dex_tx_swap_detail` across SKILL.md, auth.md, transfer.md, dapp.md, cli.md
- **Cross-Reference Paths**: Replaced stale standalone skill names (`gate-dex-auth`, `gate-dex-transfer`, `gate-dex-dapp`) with current file-based paths (`gate-dex-wallet/references/auth.md`, etc.)
- **Legacy Skill Identifiers**: Renamed `gate-dex-cli` metadata to `gate-dex-wallet-cli` in cli.md

## [2026.3.17-1] - 2026-03-17

### Fixed

- **Tool Naming Alignment**: Renamed legacy `auth.refresh_token` → `dex_auth_refresh_token`, `tx.history_list` → `dex_tx_history_list`, `tx.swap_detail` → `dex_tx_swap_detail` across SKILL.md, auth.md, transfer.md, dapp.md, cli.md
- **Cross-Reference Paths**: Replaced stale standalone skill names (`gate-dex-auth`, `gate-dex-transfer`, `gate-dex-dapp`) with current file-based paths (`gate-dex-wallet/references/auth.md`, etc.)
- **Legacy Skill Identifiers**: Renamed `gate-dex-cli` metadata to `gate-dex-wallet-cli` in cli.md

## [2026.3.14-3] - 2026-03-14

### Changed

- **MCP Tool Cross-References**: Updated market tool references in `references/dapp.md` and `references/cli.md` to use new `dex_` prefixed names
  - `token_get_risk_info` → `dex_token_get_risk_info`
  - `market_get_kline` → `dex_market_get_kline`
  - `token_list_swap_tokens` → `dex_token_list_swap_tokens`

## [2026.3.14-2] - 2026-03-14

### Added

- **Auto-Update System**: Comprehensive version management and automatic updates
  - **Dynamic Version Reading**: Auto-update system now dynamically reads current skill version from SKILL.md metadata instead of hardcoded values
  - **Enhanced Update Logic**: Added support for same-version updates when remote updated date is newer than local
  - **Improved Accuracy**: Version comparison now considers both version number and updated date for comprehensive update detection
  - **Better Error Handling**: Fallback mechanisms ensure system stability when version reading fails
  - **Session-Based Checking**: Intelligent version checks only at session start with 1-hour cooldown
  - **Fresh Install Detection**: Skip version checks for recently installed skills (< 24h) for optimal first-time experience
  - **Performance Optimized**: No version checks during normal user interactions to maintain response speed
  - **Remote Source**: Updates from official Gate Skills repository on GitHub

### Enhanced

- **Auto-Update Feature Documentation**: Added comprehensive auto-update feature description in README.md
  - Performance optimization details and smart cooldown mechanisms
  - Session caching and stable operation guarantees
  - Update timing and rules clearly explained
  - User-friendly update notifications and status messages

### Technical Changes
- Added `getCurrentSkillVersion()` function for dynamic version detection
- Added `isUpdatedDateNewer()` function for date-based update comparison  
- Enhanced update conditions to support secondary criterion (updated date comparison)
- Improved update system robustness and reliability with comprehensive error handling
- Updated file list for wallet skill updates: includes all core files and references

## [2026.3.12-1] - 2026-03-12

### Added

- **CLI Command Line Module**: `references/cli.md` — gate-wallet dual-channel CLI complete specification
  - MCP channel (OAuth managed signing) + OpenAPI hybrid mode (AK/SK + MCP signing)
  - Covers authentication, asset query, transfer, swap, market data, and approval full functionality
  - Dual-channel routing rules (explicit specification / login status determination / automatic selection)
  - Hybrid Swap (`openapi-swap`) supports EVM + Solana
  - 23 common pitfalls and best practices
- **CLI Installation Script**: `install_cli.sh` — One-click installation of gate-wallet CLI
  - Detects Node.js / npm environment
  - Global installation of `gate-wallet-cli` via npm
  - Optional OpenAPI credential configuration (`~/.gate-dex-openapi/config.json`)
  - Automatic update of CLAUDE.md / AGENTS.md routing files

### Changed

- **Routing File Template**: `install.sh` generated CLAUDE.md / AGENTS.md adds CLI routing entries
- **Cross-Skill Collaboration Table**: CLI caller name in SKILL.md corrected to `gate-dex-wallet-cli`
- **npm Package Name Unification**: All files unified to use `gate-wallet-cli`

## [2026.3.11-1] - 2026-03-11

### Added

- **One-Click Installation Script**: `install.sh` supports multi-platform automatic configuration
  - Auto-detects AI platforms (Cursor, Claude Code, Codex CLI, OpenCode, OpenClaw)
  - Creates corresponding MCP configuration and Skill routing files for each platform
  - Unified configuration of `gate-wallet` MCP Server connection
- **Unified Wallet Skill Architecture**: Integrates authentication, assets, transfer, and DApp four modules into a single Skill entry point
- **Sub-function Routing System**: Organizes complete implementation specifications for each module through `references/` directory
  - `references/auth.md` — Authentication module (Google OAuth, Token management)
  - `references/transfer.md` — Wallet comprehensive (authentication, assets, transfer, DApp) module (Gas estimation, signing, broadcasting)
  - `references/dapp.md` — DApp module (wallet connection, message signing, contract interaction)
- **Asset Query Tools** (7 tools): balance, total assets, address, chain configuration, transaction history, etc.
- **Smart Route Dispatch**: Automatically routes to corresponding sub-module implementation based on user intent
- **Unified Authentication Management**: All modules share MCP token and session state
- **MCP Server Connection Detection**: First session detection + runtime error fallback
- Supports 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)

### Changed

- **Architecture Refactoring**: From scattered 4 independent Skills (auth/wallet/transfer/dapp) integrated into a single unified Skill
- **Directory Structure**: Adopts `gate-dex-wallet/references/` pattern, referencing [gate-skills](https://github.com/gate/gate-skills/tree/master/skills/gate-exchange-futures) project architecture
- **Routing Optimization**: Main SKILL.md serves as dispatch center, sub-module specifications maintained independently

### Deprecated

- Independent `gate-dex-wallet/references/auth.md`, `gate-dex-wallet/references/transfer.md`, `gate-dex-wallet/references/dapp.md` Skill directories
- Cross-Skill complex routing, simplified to single Skill internal module routing