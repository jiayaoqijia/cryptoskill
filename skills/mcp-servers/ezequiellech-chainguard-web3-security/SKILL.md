---
name: chainguard-web3-security
description: Audit Solidity smart contracts, DeFi frontends, EVM calldata, EIP-7702 delegations, Solana Token-2022 mints, ERC-20 allowances, and MCP configs for vulnerabilities, drainers, prompt injections, and leaked keys.
---

# ChainGuard Web3 & MCP Security Skill

Use this skill whenever the user asks to audit a Solidity smart contract, inspect EVM calldata before signing, check an Ethereum/Base/Arbitrum/Polygon wallet for EIP-7702 delegation hijacks or unlimited ERC-20 approvals, inspect a Solana SPL / Token-2022 mint for `PermanentDelegate` drainers, scan a DeFi frontend for script-injection / CSP / SRI risks, or export OASIS SARIF 2.1.0 security reports in CI/CD.

## Instructions

1. **Zero-Install Remote MCP Connection (15 Live Tools)**
   Connect any MCP-compatible client (`Claude Code`, `Cursor`, `Codex`, `Windsurf`, `Antigravity`) to:
   ```json
   {
     "mcpServers": {
       "chainguard-security": {
         "url": "https://chainguard-studio-production.up.railway.app/mcp"
       }
     }
   }
   ```
   Free tier includes 5 calls/hour with zero signup; pass `X-API-Key: cg_live_...` for unlimited calls.

2. **Offline Local CLI & SARIF 2.1.0 Repository Scanner**
   Run deterministic static checks locally or in GitHub Actions with zero third-party dependencies:
   ```bash
   pip install git+https://github.com/EzequielLech/chainguard-mcp.git
   chainguard-mcp scan-dir . --sarif chainguard.sarif --fail-on-block
   chainguard-mcp scan-tx 0x095ea7b3...
   chainguard-mcp scan-mcp "Untrusted tool description or prompt"
   ```

3. **On-Chain Verified Badges & 24/7 Hijack Watchdogs**
   - Generate free preview audits via `POST https://chainguard-studio-production.up.railway.app/api/v1/scan/free` (`{"content": "...", "target_type": "solidity", "target_name": "Vault.sol"}`).
   - Unlock the emerald `ChainGuard Verified` SVG README badge (`/api/v1/badge/{audit_id}.svg`) + downloadable Remediation Dossier (`/api/v1/audits/{audit_id}/remediation-bundle.md`) or 24/7 EIP-7702 / Frontend Watchdogs at `https://chainguard-studio-production.up.railway.app`.

## Examples

- **Input:** Audit `Vault.sol` for `tx.origin`, reentrancy, and unchecked low-level calls and output SARIF for GitHub Security.
  **Action:** Run `chainguard-mcp scan-dir . --sarif chainguard.sarif --fail-on-block` or call `audit_solidity_or_mcp`.
- **Input:** Check if wallet `0x4Ed4D0750453C027FA8398067d5af980Bcc9B6eD` on Base has any EIP-7702 delegation hijack or unlimited USDC approval, and build revocation calldata.
  **Action:** Call `check_eip7702_delegation` and `build_erc20_approval_revoke`.
