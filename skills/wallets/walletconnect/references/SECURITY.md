# Security Model

## Overview

WalletConnect Requester implements a **non-custodial** security model where the AI agent never handles private keys.

## Key Principles

### 1. Zero Private Key Exposure

```
┌─────────────────┐                    ┌─────────────────┐
│   AI Agent      │                    │   User Wallet   │
│   (Requester)   │ ◄──────────────► │   (Signer)      │
│                 │   WalletConnect    │                 │
│  NO PRIVATE     │      v2            │  PRIVATE KEYS   │
│  KEYS EVER      │                    │  STORED HERE    │
└─────────────────┘                    └─────────────────┘
```

### 2. Every Transaction Requires User Approval

| Action | Agent Can Do | User Must Approve |
|--------|-------------|-------------------|
| Request transaction | ✅ | ✅ (in wallet) |
| Request signature | ✅ | ✅ (in wallet) |
| View wallet address | ✅ | ❌ |
| Execute transaction | ❌ | User only |
| Sign message | ❌ | User only |

### 3. Session-Based Access Control

- Sessions expire after 7 days (WalletConnect default)
- User can disconnect session anytime
- Agent cannot force any action

## Attack Scenarios

### Scenario: Agent is Compromised

```
Attacker gains control of the AI agent
         ↓
Attacker tries to steal funds
         ↓
Attacker CANNOT:
  - Access private keys (agent never has them)
  - Auto-sign transactions (not possible)
  - Execute transactions without approval
         ↓
Attacker CAN ONLY:
  - Request transactions (user must approve)
  - Request signatures (user must approve)
  - View wallet address (non-sensitive)
         ↓
Result: FUNDS ARE SAFE
```

### Scenario: Session Token Stolen

```
Attacker obtains session token
         ↓
Attacker can only:
  - Request transactions (user still must approve)
  - Cannot auto-sign
  - Cannot access private keys
         ↓
Result: FUNDS ARE SAFE
```

## Comparison with Custodial Solutions

| Risk | walletconnect-agent (Custodial) | walletconnect-requester (Non-Custodial) |
|------|--------------------------------|----------------------------------------|
| Private key theft | ⚠️ All funds lost | ✅ Impossible - no keys |
| Agent compromised | ⚠️ Attacker can drain funds | ✅ User must approve |
| Malicious code | ⚠️ Can steal keys | ✅ Can only request |
| Session hijack | ⚠️ Auto-sign available | ✅ Still needs approval |

## Audit Trail

All requests are logged to `~/.walletconnect-requester/audit.log`:

```json
{
  "timestamp": "2026-03-09T02:00:00Z",
  "action": "transaction_request",
  "chain": 8453,
  "to": "0x8335...",
  "status": "approved",
  "tx_hash": "0xabc123..."
}
```

**Sensitive data is masked** - full addresses and keys are never logged.

## Best Practices

### For Users

1. **Review every request** - Check transaction details before approving
2. **Use dedicated wallet** - Separate wallet for agent interactions
3. **Disconnect when done** - End sessions when not needed
4. **Check audit logs** - Review `~/.walletconnect-requester/audit.log`

### For Developers

1. **Never ask for private keys** - This defeats the purpose
2. **Display transaction details** - Show user what they're signing
3. **Implement rate limiting** - Don't spam user with requests
4. **Handle rejections gracefully** - User may decline any request

## Supported Methods

### Safe Methods (Always Allowed)

| Method | Risk Level | Description |
|--------|-----------|-------------|
| `personal_sign` | ✅ Low | User signs readable message |
| `eth_signTypedData_v4` | ✅ Low | User signs structured data |
| `eth_sendTransaction` | ⚠️ Medium | User must verify transaction |

### Blocked Methods

| Method | Reason |
|--------|--------|
| `eth_sign` | ⚠️ Dangerous - allows signing arbitrary data |

**Why `eth_sign` is blocked:** This method allows signing any arbitrary data, which can be used in phishing attacks to trick users into signing transactions. Use `personal_sign` instead.

## Network Security

- All communication is end-to-end encrypted (WalletConnect v2)
- Messages relay through decentralized Waku network
- Private keys never transmitted

## Conclusion

**This skill is designed for maximum security.** By never handling private keys and requiring user approval for every action, it provides the safest way for AI agents to interact with Web3.