---
name: walletconnect-requester
description: Secure WalletConnect integration for AI agents. Connect to user wallets as a DApp (Proposer) without ever handling private keys. Request transactions and signatures - users approve everything in their wallet. Zero custody, maximum security. Use when you need to interact with user wallets securely via WalletConnect v2.
metadata:
  openclaw:
    requires:
      env:
        - WC_PROJECT_ID (required): WalletConnect Cloud Project ID
        - WC_METADATA_NAME (optional): DApp name shown in wallet
        - WC_METADATA_URL (optional): DApp URL
        - WC_METADATA_ICONS (optional): DApp icon URLs (comma-separated)
    persistence:
      path: ~/.walletconnect-requester/
      files:
        - sessions.json: Active WalletConnect sessions
        - audit.log: Transaction audit log (masked sensitive data)
    security_notes:
      - WalletConnect URI contains symmetric key (symKey) - treat as sensitive
      - Session tokens grant transaction request capability - protect accordingly
      - Audit logs contain masked addresses and tx hashes - review before sharing
---

# WalletConnect Requester

> **Zero custody. Maximum security. User always in control.**

## Why This Skill?

Unlike `walletconnect-agent` which **holds private keys and auto-signs**, this skill takes a fundamentally different approach:

| | walletconnect-agent | walletconnect-requester (this skill) |
|---|---|---|
| **Private Keys** | ⚠️ Stored in agent | ✅ Never touches agent |
| **Signing** | ⚠️ Auto-signs everything | ✅ User approves each tx |
| **Security Model** | Custodial (agent has full control) | **Non-custodial (user has full control)** |
| **If Agent is Compromised** | ⚠️ Funds can be stolen | ✅ Funds are safe - no keys to steal |

**This is the safest way for AI agents to interact with Web3.**

## What This Does

- **Connect to user wallets** via WalletConnect v2
- **Request transactions** - user approves in their wallet
- **Request signatures** - user signs in their wallet
- **Zero private key exposure** - keys never leave the user's wallet

## Security Guarantees

```
┌─────────────────┐                    ┌─────────────────┐
│   AI Agent      │                    │   User Wallet   │
│   (Requester)   │ ◄── WalletConnect ──► │   (Signer)      │
│                 │     Session          │                 │
└─────────────────┘                    └─────────────────┘
         │                                    │
         │  1. Request transaction            │
         │ ─────────────────────────────────► │
         │                                    │
         │  2. User reviews & approves        │
         │    (in wallet UI)                  │
         │                                    │
         │  3. Signed transaction             │
         │ ◄───────────────────────────────── │
         │                                    │
         ▼                                    ▼
    NO PRIVATE KEYS                      PRIVATE KEYS
    NO AUTO-SIGN                         USER APPROVES
    USER IN CONTROL                      EVERYTHING
```

## Installation

### Step 1: Install Dependencies

This skill requires Node.js dependencies. Install them globally or locally:

```bash
# Install dependencies
npm install @walletconnect/sign-client @walletconnect/core qrcode
```

### Step 2: Get WalletConnect Project ID

1. Go to [WalletConnect Cloud](https://cloud.walletconnect.com/)
2. Create a new project
3. Copy your **Project ID**

### Step 3: Set Environment Variable

```bash
export WC_PROJECT_ID="your_project_id_here"
```

### Step 4: Run the Skill

```bash
node scripts/wc-requester.js connect
```

---

## Quick Start

### Step 1: Create a Session

```bash
export WC_PROJECT_ID="your_project_id"
node scripts/wc-requester.js connect
```

Output:
```
WalletConnect URI: wc:abc123...@2?relay-protocol=irn&symKey=xyz

Scan this QR code with your wallet:
[QR CODE]

Waiting for wallet to connect...
```

### Step 2: Request a Transaction

```bash
node scripts/wc-requester.js request-tx \
  --to 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --data 0xa9059cbb... \
  --value 0 \
  --chain 8453
```

User sees in wallet:
```
Send 10 USDC to 0x1F3A...?
[Approve] [Reject]
```

### Step 3: Request a Signature

```bash
node scripts/wc-requester.js request-sign \
  --message "Sign this message to verify ownership" \
  --chain 8453
```

## Commands

### `connect` - Create WalletConnect Session

```bash
node scripts/wc-requester.js connect [options]

Options:
  --chains <ids>     Comma-separated chain IDs (default: 8453,1)
  --methods <list>   Comma-separated methods (default: eth_sendTransaction,personal_sign)
  --qr <path>        Generate QR code to file
  --json             Output as JSON
```

### `request-tx` - Request Transaction

```bash
node scripts/wc-requester.js request-tx --to <address> --data <hex> --value <wei> --chain <id>
```

### `request-sign` - Request Signature

```bash
node scripts/wc-requester.js request-sign --message <text> --chain <id>
# or for typed data
node scripts/wc-requester.js request-sign --typed-data <json> --chain <id>
```

### `sessions` - List Active Sessions

```bash
node scripts/wc-requester.js sessions
```

### `disconnect` - End Session

```bash
node scripts/wc-requester.js disconnect --topic <topic>
```

## Security Model

### What Agent CAN Do
- ✅ Request transactions (user must approve)
- ✅ Request signatures (user must approve)
- ✅ View connected wallet address
- ✅ View session metadata

### What Agent CANNOT Do
- ❌ Hold private keys
- ❌ Auto-sign anything
- ❌ Execute transactions without approval
- ❌ Access funds directly

### If Agent is Compromised
- ✅ Attacker cannot steal funds (no keys)
- ✅ Attacker cannot auto-sign transactions
- ✅ User can reject any suspicious request
- ✅ User can disconnect session anytime

### Local Data Persistence

This skill writes files to `~/.walletconnect-requester/`:

| File | Purpose | Sensitivity |
|------|---------|-------------|
| `sessions.json` | Active WalletConnect sessions | ⚠️ Contains session topics |
| `audit.log` | Transaction audit log | ⚠️ Contains masked tx hashes |

**Security recommendations:**
- Review `audit.log` before sharing
- Delete `sessions.json` when no longer needed
- Set appropriate file permissions: `chmod 600 ~/.walletconnect-requester/*`

### Sensitive Data Handling

| Data Type | How It's Handled |
|-----------|------------------|
| **WalletConnect URI** | Contains `symKey` - displayed once during connection, not logged |
| **Session tokens** | Stored locally in `sessions.json`, not transmitted externally |
| **Transaction hashes** | Logged in `audit.log` with masked addresses |
| **Private keys** | ❌ Never handled by this skill |

### Privacy Considerations

- WalletConnect URI (with `symKey`) is printed to stdout for QR code generation
- Audit logs mask full addresses (e.g., `0x8335...` instead of full address)
- No data is sent to external servers except WalletConnect relay network

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WC_PROJECT_ID` | Yes | WalletConnect Cloud Project ID |
| `WC_METADATA_NAME` | No | DApp name shown in wallet |
| `WC_METADATA_URL` | No | DApp URL |
| `WC_METADATA_ICONS` | No | DApp icon URL |

### Namespaces Configuration

The skill requests minimal permissions by default:

```json
{
  "eip155": {
    "chains": ["eip155:8453", "eip155:1"],
    "methods": ["eth_sendTransaction", "personal_sign"],
    "events": ["accountsChanged", "chainChanged"]
  }
}
```

## Example Workflows

### Connect and Request Payment

```bash
# 1. Create session
node scripts/wc-requester.js connect --qr /tmp/qr.png
# User scans QR with MetaMask

# 2. Request USDC transfer
node scripts/wc-requester.js request-tx \
  --to 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --data 0xa9059cbb0000... \
  --chain 8453

# User sees: "Send 10 USDC?" → Approves in wallet
# Returns: tx_hash
```

### Verify Wallet Ownership

```bash
# 1. Connect
node scripts/wc-requester.js connect

# 2. Request signature
node scripts/wc-requester.js request-sign \
  --message "I own this wallet on March 9, 2026"

# User signs in wallet
# Returns: signature
```

## Comparison with Other Solutions

| Feature | This Skill | walletconnect-agent | MetaMask SDK |
|---------|-----------|---------------------|--------------|
| Private Key Storage | ❌ Never | ⚠️ In Agent | ❌ Never |
| Auto-sign | ❌ Never | ✅ Yes | ❌ No |
| User Approval Required | ✅ Always | ❌ No | ✅ Always |
| Multi-wallet Support | ✅ Any WC wallet | ✅ Any WC wallet | ❌ MetaMask only |
| Security Level | **Highest** | Medium | High |
| Best For | User-controlled tx | Automated trading | MetaMask users |

## Supported Wallets

Any wallet that supports WalletConnect v2:
- MetaMask Mobile
- Rainbow
- Trust Wallet
- Coinbase Wallet
- Ledger Live
- And 500+ more...

## Troubleshooting

### "No active session"
Run `connect` first to create a session.

### "User rejected request"
User declined in their wallet. Ask if they want to retry.

### "Session expired"
Sessions last 7 days by default. Reconnect to create a new session.

### "Unsupported chain"
User's wallet doesn't support the requested chain. Ask them to switch networks.

## Audit Log

All requests are logged (without sensitive data):

```
~/.walletconnect-requester/audit.log

{
  "timestamp": "2026-03-09T02:00:00Z",
  "action": "request_transaction",
  "chain": 8453,
  "to": "0x8335...",
  "status": "approved",
  "tx_hash": "0xabc123..."
}
```

## When to Use This vs walletconnect-agent

| Use This Skill When | Use walletconnect-agent When |
|--------------------|------------------------------|
| User must approve every tx | Fully automated trading |
| Maximum security required | You trust the agent completely |
| One-time or occasional tx | 24/7 unattended operation |
| User wants full control | User wants set-and-forget |
| Agent runs in untrusted env | Agent runs in secure env |

**When in doubt, use this skill.** It's always safer.

---

## License

MIT — Built with security as the #1 priority.

---

**Maintainer**: Web3 Investor Team  
**Registry**: https://clawhub.com/skills/walletconnect-requester