# Security Policy

## Non-Custodial Architecture
`chainguard-mcp` never requests, stores, or processes private keys, seed phrases, or custodial funds. All wallet scans, pre-flight firewall checks, and calldata builders (`approve(spender, 0)`, dust sweeps, Solana `CloseAccount` rent recovery) are strictly read-only and unsigned.

## Supported Versions

| Version | Supported |
| ------- | --------- |
| `1.1.x` | ✅ Active |
| `< 1.0` | ❌ Upgrade recommended |

## Reporting a Vulnerability
If you discover a security issue in our pre-flight transaction firewall, Unicode prompt-injection scanner, or MCP Streamable-HTTP endpoint:
- Email: `ezequiellich44@gmail.com`
- Canonical policy: `https://chainguard-studio-production.up.railway.app/.well-known/security.txt`
