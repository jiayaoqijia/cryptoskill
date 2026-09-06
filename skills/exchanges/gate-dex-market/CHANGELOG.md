# Changelog

All notable changes to `gate-dex-market` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.24-1] - 2026-03-24

### Changed

- **SKILL.md streamlined**: Removed Auto-Update section (now handled by `gate-runtime-rules.md` §1); removed Cross-Skill Collaboration (non-actionable); consolidated Security Rules (credential handling defers to runtime-rules §3)
- **General Rules**: Added mandatory reference to `gate-runtime-rules.md` before any tool call


## [2026.3.18-1] - 2026-03-18

### Changed

- **SKILL.md Streamlined**: Removed verbose routing logic, priority system, OpenClaw integration examples; converted to pure routing layer pointing to `references/`
- **MCP Tool Naming**: Restored `dex_` prefix for all MCP tools (dex_market_get_kline, dex_token_get_coin_info, etc.)

### Fixed

- **Cross-Reference Paths**: Added missing `.md` extensions to `gate-dex-wallet/references/transfer` references
- **Legacy Skill Identifiers**: Renamed `gate-dex-openmarket` metadata to `gate-dex-market-openapi` in openapi.md
- **Install Script**: Corrected echo'd documentation path in install.sh

## [2026.3.17-1] - 2026-03-17

### Fixed

- **Cross-Reference Paths**: Added missing `.md` extensions to `gate-dex-wallet/references/transfer` references in SKILL.md and mcp.md
- **Legacy Skill Identifiers**: Renamed `gate-dex-openmarket` metadata to `gate-dex-market-openapi` in openapi.md
- **Install Script**: Corrected echo'd documentation path in install.sh

## [2026.3.14-3] - 2026-03-14

### Changed

- **MCP Tool Naming Convention**: Added `dex_` prefix to all `market_` and `token_` prefixed tools for namespace clarity
  - `market_get_kline` → `dex_market_get_kline`
  - `market_get_tx_stats` → `dex_market_get_tx_stats`
  - `market_get_pair_liquidity` → `dex_market_get_pair_liquidity`
  - `token_get_coin_info` → `dex_token_get_coin_info`
  - `token_ranking` → `dex_token_ranking`
  - `token_get_coins_range_by_created_at` → `dex_token_get_coins_range_by_created_at`
  - `token_get_risk_info` → `dex_token_get_risk_info`
  - `token_list_swap_tokens` → `dex_token_list_swap_tokens`
  - `token_list_cross_chain_bridge_tokens` → `dex_token_list_cross_chain_bridge_tokens`

### Added

- **MCP Tool Expansion**: Added 3 missing MCP tools to match full specification
  - `dex_market_get_tx_stats` — Trading statistics (buy/sell count, volume, unique traders)
  - `dex_market_get_pair_liquidity` — Trading pair liquidity pool info
  - `dex_token_get_coins_range_by_created_at` — New token discovery
- MCP mode tool count updated from 6 to 9

## [2026.3.14-2] - 2026-03-14

### Fixed

- **Version Check Logic Enhancement**: Fixed critical version checking logic to use dynamic metadata reading
  - Added `getCurrentSkillVersion()` function to dynamically read version and updated date from SKILL.md
  - Replaced hardcoded version constants with real-time file metadata extraction
  - Resolved infinite update loop issue where updated skills would still use old hardcoded versions
  - Enhanced dual-field version checking (both `version` and `updated` fields)
- **OAuth Authentication Documentation**: Updated authentication descriptions to support both Google OAuth and Gate OAuth
- **URL Display Format**: Standardized MCP login URL display format without decorative quotes or brackets
- **Auto-update System Optimization**: 
  - Fresh installation detection (24-hour window) to skip redundant initial checks
  - Session-based update checking with 1-hour cooldown mechanism
  - Support for same-session re-checking after cooldown period expires

### Enhanced

- **Version Comparison Logic**: Now supports both version number comparison and updated date comparison
- **User Experience**: Dynamic version display in messages instead of static hardcoded values
- **Error Handling**: Robust fallback mechanisms for version reading failures
- **Performance Optimizations**: Reduced redundant version checks through intelligent caching

### Technical

- All skill components updated: `SKILL.md`, `references/mcp.md`, `references/openapi.md`
- Version metadata synchronized across all files
- Comprehensive logging and status reporting for update operations

## [2026.3.14-1] - 2026-03-14

### Added

- **Complete English Version**: Full English translation of Gate DEX Market skill package
  - `README.md` (92 lines) — Comprehensive installation and usage guide
  - `SKILL.md` (269 lines) — Intelligent routing and unified entry point
  - `references/mcp.md` (934 lines) — Complete MCP mode detailed specifications
  - `references/openapi.md` (531 lines) — Complete OpenAPI mode detailed specifications
  - `install.sh` (188 lines) — Automated installation and configuration script
- **Professional Technical Documentation**: 2,063 lines of professionally translated technical content
- **Dual-language Support**: Parallel Chinese (`gate-dex-market-test`) and English (`gate-dex-market`) versions
- **Complete Technical Preservation**: All API specifications, parameters, HMAC-SHA256 algorithms, and MCP tool formats maintained

### Changed

- **Path References**: All internal document references updated to `gate-dex-market` path structure
- **Metadata Updates**: Skill names and identifiers properly localized for English version
- **Documentation Structure**: Optimized file organization with proper cross-references

### Removed

- **Redundant Documentation**: Eliminated duplicate README files that caused content overlap
- **Obsolete References**: Cleaned up outdated file structure references

---

## [2026.3.11-1] - 2026-03-11

### Added

- **Dual-mode Architecture**: Integrated MCP and OpenAPI two calling methods into single Skill entry
- **Intelligent Routing System**: Automatically select optimal calling mode based on environment and user intent
  - `references/openapi.md` — OpenAPI mode complete specification (AK/SK direct calls)
  - `references/mcp.md` — MCP mode detailed specification  
- **MCP Tool Integration** (6 tools): K-line, token info, rankings, security audit, etc.
- **OpenAPI Tool Integration** (9 actions): Token list, basic info, holder analysis, risk detection, etc.
- **Unified Connection Detection**: First session detection + runtime error fallback
- Support for 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)

### Changed

- **Architecture Upgrade**: Upgraded from single MCP mode to dual MCP + OpenAPI mode support
- **Routing Optimization**: Main SKILL.md serves as intelligent distribution center, sub-module specifications maintained independently
- **User Experience**: Automatically select most suitable calling method based on environment, reducing configuration burden

---

## [2026.3.10-1] - 2026-03-10

### Added

- 9 market data query tools (all require no authentication)
- 5 operation workflows: quote viewing, token details, rankings, security audit, new token discovery  
- MCP Server connection detection (first session detection + runtime error fallback)
- Cross-Skill collaboration: Provide token information and security audit for swap, dapp