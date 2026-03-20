# Changelog

All notable changes to `gate-dex-trade` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.3.11-1] - 2026-03-11

### Added

- **Dual mode architecture**: Integrated MCP and OpenAPI two trading methods into single Skill entry
- **Smart routing system**: Automatically select best trading mode based on environment and user preferences
  - `references/openapi.md` — OpenAPI mode complete specification (AK/SK + complete lifecycle)
  - `references/README-openapi.md` — OpenAPI mode usage guide
- **MCP trading tools** (5 tools): Quote, execution, status query, balance verification, address retrieval
- **OpenAPI trading tools** (9 tools): Chain query, Gas price, quote, build, sign, submit, status etc
- **Unified connection detection**: First session detection + runtime error fallback
- **Dual security mechanism**: MCP three-step confirmation gating + OpenAPI private key protection
- Multi-chain support: EVM (14 chains) + Solana + SUI + Tron + Ton

### Changed

- **Architecture upgrade**: From single MCP Swap upgraded to MCP + OpenAPI dual mode trading support
- **Routing optimization**: Main SKILL.md as intelligent distribution center, supports automatic mode switching
- **User experience**: Automatically select most suitable trading method based on user needs and environment

---

## [2026.3.6-1] - 2026-03-06

### Added

- 5 MCP Swap tools: Quote, execution, status query etc
- 4 operation processes: Standard Swap, modify slippage, query status, cross-chain Swap
- Mandatory three-step confirmation gating: Trading pair confirmation → quote display → signature authorization confirmation
- Exchange value difference calculation and tiered warnings (> 5% mandatory warning)