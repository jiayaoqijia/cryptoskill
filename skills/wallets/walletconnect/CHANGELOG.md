# Changelog

## [1.0.0] - 2026-03-09

### Added
- Initial release
- Non-custodial WalletConnect v2 client for AI agents
- Session management (connect, list, disconnect)
- Transaction requests (user must approve)
- Signature requests (user must approve)
- QR code generation for easy wallet scanning
- Audit logging (without sensitive data)
- Multi-chain support (Base, Ethereum, Arbitrum, Optimism, Polygon)

### Security
- **Zero private key exposure** - Keys never leave user wallet
- **User approval required** - Every transaction must be approved
- **`eth_sign` blocked by default** - Prevents phishing attacks
- **Audit trail** - All requests logged with masked sensitive data

### Differences from walletconnect-agent

| Feature | walletconnect-agent | walletconnect-requester |
|---------|---------------------|------------------------|
| Private keys | Stored in agent | **Never in agent** |
| Auto-sign | Yes | **No - user approves** |
| Security model | Custodial | **Non-custodial** |
| If compromised | Funds at risk | **Funds safe** |