# Changelog

All notable changes to the 8004-skill skill will be documented in this file.

## [1.5.0] - 2026-02-11

### Changed
- **Renamed skill**: `erc-8004` → `8004-skill` as requested
- Updated all directory names and internal references

## [1.4.0] - 2026-02-10

### Changed
- **Renamed skill**: `tron-8004` → `erc-8004` to reflect multi-chain nature
  - Skill now emphasizes ERC-8004 standard with TRON (TRC-8004) and BSC support
  - Updated all documentation and references
  - Package name changed to `erc-8004`

## [1.3.0] - 2026-02-10

### Added
- **Multi-chain support**: TRON + BSC (BNB Smart Chain) support in single codebase
- **Chain adapter**: Unified interface for TRON (TronWeb) and EVM chains (ethers.js)
- **BSC deployment**: Live contracts on BSC mainnet and testnet
- **Multi-chain scripts**: All scripts now support both TRON and BSC
  - `register.js` - Register agents on any supported chain
  - `query.js` - Query agent info and reputation
  - `feedback.js` - Submit feedback/reputation scores
  - `set-uri.js` - Update agent metadata URI
- **NPM scripts**: Added convenient npm run commands for all operations

### Updated
- **BSC contract addresses**: Updated with correct deployments
  - BSC Mainnet: Added ValidationRegistry `0x8004Cc8439f36fd5F9F049D9fF86523Df6dAAB58`
  - BSC Testnet: ReputationRegistry `0x8004B663056A597Dffe9eCcC1965A193B7388713`
  - BSC Testnet: Added ValidationRegistry `0x8004Cb1BF31DAf7788923b405b754f57acEB4272`
- **BSC ABIs**: Updated with correct contract ABIs (not proxy ABIs)
  - Added complete IdentityRegistry ABI
  - Added complete ReputationRegistry ABI with all functions
  - Added complete ValidationRegistry ABI
- **TRON ABIs**: Split into query/write subsets to avoid TronWeb tuple[] parsing issues

### Fixed
- **CRITICAL: package.json scripts**: Fixed npm run commands to use correct script names
  - Changed `register-multichain.js` to `register.js` (file was renamed but package.json wasn't updated)
  - This was causing MODULE_NOT_FOUND errors when using `npm run register`
  - Added npm scripts for query, feedback, and set-uri operations
- **Cross-chain type parameter**: Fixed `createClient` to properly receive chain type from config
- **TRON read-only calls**: Added `from` address to TRON contract calls to fix "owner_address isn't set" error
- **Contract compatibility**: Query scripts now use fallback methods (ownerOf + tokenURI) for TRON compatibility
- **ABI conversion**: Preserved tuple components when converting TRON ABI to EVM format
- **Error handling**: Improved error messages and graceful degradation for unsupported contract methods
- **Reputation queries**: Fixed "clientAddresses required" error by calling getClients() first
- **BSC queries**: All BSC queries now work correctly with proper contract interfaces

### Changed
- Simplified to single registration script (register.js) with multi-chain support
- Updated all documentation to reflect multi-chain capabilities
- Private key format: 64 hex characters (no "0x" prefix) works for both chains
- Query scripts now detect and adapt to different contract versions

### Removed
- Old TRON-only scripts (replaced with multi-chain versions)
- Test scripts and redundant documentation files
- Duplicate network configurations from contracts.json

### Contract Addresses
- **BSC Mainnet:**
  - Identity: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
  - Reputation: `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`
- **BSC Testnet:**
  - Identity: `0x8004A818BFB912233c491871b3d84c89A494BD9e`
  - Reputation: `0x8004B663056A597Dffe9eCcC1965A193B7388713`

### Compatibility Notes
- **TRON**: Scripts use compatibility mode with fallback to ERC-721 standard methods
- **BSC**: Full ERC-8004 specification support

## [1.2.0] - 2026-02-10

### Fixed
- **TronWeb compatibility**: Fixed `TronWeb is not a constructor` error
- **ABI standardization**: Converted all ABIs to standard EVM format
- **Contract initialization**: Fixed `unknown function` errors

### Changed
- ABI format changed to standard array format
- All `type: "Function"` changed to `type: "function"`
- All `stateMutability` values lowercased

## [1.1.0] - 2026-02-10

### Added
- Unified private key configuration system (compatible with ERC-8004)
- Support for file-based private key storage at `~/.clawdbot/wallets/.deployer_pk`
- New `utils.js` module for shared utility functions
- Improved error messages with detailed setup instructions

### Changed
- Private key loading now supports three methods with priority order:
  1. `TRON_PRIVATE_KEY` environment variable
  2. `PRIVATE_KEY` environment variable
  3. `~/.clawdbot/wallets/.deployer_pk` file
- Refactored all scripts to use shared utility functions
- Updated all documentation to reflect new configuration options

### Improved
- Better error handling and user feedback
- Consistent transaction result display across all scripts
- Code reusability with shared utility module

## [1.0.0] - 2026-02-10

### Added
- Initial release of TRC-8004 Trustless Agents skill for TRON
- Support for TRON Mainnet, Nile, and Shasta testnets
- Identity Registry integration (TRC-721 based)
- Reputation Registry integration with feedback system
- Validation Registry integration
- Complete contract ABIs for all three registries
- Node.js scripts for all operations:
  - `register.js` - Register new agents
  - `query.js` - Query agent info and reputation
  - `feedback.js` - Submit feedback/reputation
  - `set-uri.js` - Update agent metadata URI
- Registration template with TRON-specific format
- Comprehensive documentation (README.md, SKILL.md)
- Network configuration with all contract addresses
- Support for fixed-point reputation scores with decimals
- Automatic address format handling (Base58/Hex)

### Contract Addresses
- **Mainnet:**
  - Identity: `TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy`
  - Reputation: `TFbvfLDa4eFqNR5vy24nTrhgZ74HmQ6yat`
  - Validation: `TLCWcW8Qmo7QMNoAKfBhGYfGpHkw1krUEm`
- **Nile Testnet:**
  - Identity: `TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5`
  - Reputation: `TBVaGd6mBuGuN5ebcvPvRaJo4rtEWqsW6Y`
  - Validation: `TGGkHDHhBzhFcLNcEogAWJkvfFYy4jyrSw`
- **Shasta Testnet:**
  - Identity: `TH775ZzfJ5V25EZkFuX6SkbAP53ykXTcma`
  - Reputation: `TTkds2ZZKBTChZHho4wcWAa7eWQTxh5TUT`
  - Validation: `TQBFHtKRiaQjc1xp4LtmmXKYdA7JLN89w3`

### Features
- Full ERC-8004 compatibility adapted for TRON
- Support for multiple trust models (reputation, crypto-economic, crypto-verification)
- Flexible feedback system with tags and metadata
- Agent metadata management with IPFS support
- Transaction confirmation and explorer links
- Detailed error handling and user feedback

### Dependencies
- TronWeb for blockchain interaction
- Node.js runtime environment
- TRON_PRIVATE_KEY environment variable for signing

---

*Compatible with ERC-8004 specification v1.0*
