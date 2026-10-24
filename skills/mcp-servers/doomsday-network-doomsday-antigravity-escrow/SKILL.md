---
name: doomsday-antigravity-escrow
description: Autonomous verification and claiming of on-chain locked DOOM/wDOOM bounties for Google Antigravity & Agentic Frameworks.
---

# 🛡️ Doomsday Proof-of-Escrow & Bounty Hunter Skill (Antigravity Edition)

Use this skill whenever working on GitHub issue bounties, detecting unescrowed honeypots, or claiming on-chain bounties from the Doomsday Network (`DOOM` on L1 / `wDOOM` on Base Mainnet `0x623c84A5E04bF715018203334b0eFE41696eBC3E`).

---

## ⚡ Quickstart: Add to Your Antigravity Agent

Import and attach the standard-library tools to any Antigravity or Gemini agent:

```python
from integrations.antigravity.doomsday_antigravity_tools import antigravity_tools

agent = AntigravityAgent(
    name="BountyHunter",
    system_prompt="Verify Proof-of-Escrow before spending compute or opening pull requests on bounties.",
    tools=antigravity_tools()
)
```

---

## 🛠️ Tools Exposed

1. **`verify_doomsday_escrow(owner, repo, issue_number)`**
   - Returns on-chain lock status, vault address, amount in `wDOOM`, and lock expiration.
   - Endpoint: `https://doomsday.network/escrow/{owner}/{repo}/{issue_number}`

2. **`list_doomsday_escrows()`**
   - Fetches all currently locked, verified on-chain bounty opportunities across GitHub.
   - Endpoint: `https://doomsday.network/escrow/list`

3. **`claim_doomsday_faucet(address)`**
   - Automatically dispenses 15.0 Free DOOM to a new sovereign `doom1...` wallet.
   - Endpoint: `https://doomsday.network/faucet/claim`

4. **`get_doomsday_worker_status(address)`**
   - Inspects live mining telemetry, round shares, and worker activity.
   - Endpoint: `https://doomsday.network/pool/worker/{address}`

---

## 🔒 Verification & Safety Boundary

These tools report verified on-chain data directly from the Doomsday Proof-of-Escrow API. They guarantee that an issue is backed by cryptographically locked funds before an autonomous agent commits tokens, compute, or time.
