# Changelog

All notable changes to `gate-dex-market` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.12-1] - 2026-03-12

### Changed

- **Architecture Simplification**: Removed MCP mode, now uses OpenAPI mode only
- **Cleaner Configuration**: Single mode reduces complexity and configuration burden

---

## [2026.3.11-1] - 2026-03-11

### Added

- **OpenAPI Integration**: AK/SK authentication for direct API calls
  - `references/openapi.md` — OpenAPI complete specification
  - `references/README-openapi.md` — OpenAPI usage guide
- **OpenAPI Tool Integration** (9 actions): Token lists, basic info, holder analysis, risk detection, K-line, etc.
- **Environment Detection**: Auto-detect and create config file on first use
- Support for 8 chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base, Solana)

### Changed

- **Routing Optimization**: Main SKILL.md serves as entry point, detailed specifications in references/
- **User Experience**: Auto-creates config with default credentials, reducing initial setup burden

---

## [2026.3.10-1] - 2026-03-10

### Added

- 9 market data query actions (all read-only)
- 5 operation flows: quote viewing, token details, rankings, security audit, new token discovery
- Cross-Skill collaboration: provides token information and security audit for swap, dapp