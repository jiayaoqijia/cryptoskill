# Changelog

All notable changes to the Gate Exchange Staking skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2026.3.16-1] - 2026-03-16

### Added
- **GUSD / multi-currency coin selection**: When staking, redeeming, or minting GUSD (or any product with `currency` / `mortgage_coin` = `"USDT,USDC"`), the agent must prompt the user to choose **USDT** or **USDC** and pass the choice as the **`coin`** parameter to `cex_earn_swap_staking_coin`. Only USDT and USDC are supported.

### Changed
- **SKILL.md**: New Domain Knowledge section "GUSD / multi-currency products (USDT or USDC)" with prompt wording and rule to not call the swap/mint tool until the user has selected a coin. Mint section notes that when mint is supported, the same `coin` rule applies.
- **references/staking-swap.md**:
  - MCP tools table: documented **`coin`** for `cex_earn_swap_staking_coin` (required for GUSD).
  - Workflow **Stake**: New step for GUSD — ask "USDT or USDC?" and pass `coin`; single/multiple protocol steps updated to pass `coin` when product is GUSD.
  - Workflow **Redeem**: New step for GUSD — ask which coin to receive (USDT or USDC) and pass `coin` on swap call.
  - Error handling: New case for user choosing a coin other than USDT or USDC for GUSD → reply that only USDT and USDC are supported.
  - Report templates: Added "Stake — GUSD / multi-currency" and "Redeem — GUSD / multi-currency" confirmation prompts.

## [2026.3.12-1] - 2026-03-12

### Added
- Initial release of Gate Exchange Staking skill
- Query staking positions functionality
- Staking rewards tracking
- Available products discovery
- Transaction history viewing
- Support for multiple staking types (flexible, locked, DeFi, treasury)
- Multilingual support (English)
- Comprehensive error handling
- Detailed documentation and examples

### Features
- Real-time position monitoring
- Historical reward analysis
- APY comparison tools
- Portfolio value calculations
- Smart intent detection
- Natural language query processing

### Supported Operations
- `cex_earn_asset_list`: Query current staking positions
- `cex_earn_award_list`: Retrieve reward history
- `cex_earn_find_coin`: Discover available products
- `cex_earn_order_list`: View transaction history

### Security
- Read-only access implementation
- User authentication requirement
- Rate limiting compliance
- Data privacy protection