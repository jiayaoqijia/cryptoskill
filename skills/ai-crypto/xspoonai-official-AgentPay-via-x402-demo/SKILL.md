---
name: AgentPay-via-x402-demo
version: 1.0.0
description: AI-powered cross-chain payment automation - let your agent handle USDC payments between Solana and Base with zero human intervention
metadata: {"category":"payment","blockchains":["solana","base"],"protocol":"x402"}
---

# AgentPay via X402 - Cross-Chain Payment Automation for AI Agents

**AgentPay** enables AI agents to execute cross-chain USDC payments autonomously. No browser, no manual signing, no human intervention - just pure API-driven automation.

Your agent can:
- 💰 Send USDC from Solana or Base to any recipient
- 🔐 Generate and manage wallets locally (keys never leave your machine)
- ⚡ Sign transactions with X402 protocol authorization
- 🎯 Track payment status in real-time
- 🏆 Compete on the payment leaderboard

**Merchants always receive USDC on Base. Payers can pay from Solana or Base.**

---

## 🎬 Demo: 4-Step Payment Flow

### Step 1: Generate Wallets (One-time Setup)
Your agent creates EVM and Solana wallets locally. Private keys are stored at `~/.config/x402pay/wallets.json` and **never** sent to any API.

```python
# EVM wallet (for Base payments)
from eth_account import Account
Account.enable_unaudited_hdwallet_features()
account, mnemonic = Account.create_with_mnemonic()
print(f"Base Address: {account.address}")

# Solana wallet
from solders.keypair import Keypair
import base64
keypair = Keypair()
print(f"Solana Address: {keypair.pubkey()}")
```

**Output:**
```
Base Address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
Solana Address: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
```

---

### Step 2: Create Payment Intent
Your agent calls the API to create a payment intent. The API returns `payment_requirements` - everything needed to sign the transaction.

```bash
curl -X POST "https://api-pay.agent.tech/api/intents" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "0xReceiverBaseAddress",
    "amount": "10",
    "payer_chain": "base"
  }'
```

**Response:**
```json
{
  "intent_id": "550e8400-e29b-41d4-a716-446655440000",
  "merchant_recipient": "0xReceiverBaseAddress",
  "sending_amount": "10.00",
  "receiving_amount": "9.95",
  "estimated_fee": "0.05",
  "payer_chain": "base",
  "status": "AWAITING_PAYMENT",
  "expires_at": "2026-02-05T17:40:00Z",
  "payment_requirements": {
    "scheme": "exact",
    "network": "eip155:8453",
    "amount": "10000000",
    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "payTo": "0xFacilitatorAddress",
    "maxTimeoutSeconds": 600,
    "extra": {
      "name": "USD Coin",
      "version": "2"
    }
  }
}
```

---

### Step 3: Sign Transaction Locally
Your agent uses `payment_requirements` to build and sign the X402 authorization. For EVM chains, this is an EIP-712 signature. For Solana, it's a VersionedTransaction.

```python
# EVM (Base) - EIP-712 TransferWithAuthorization
import json, base64, time, os
from eth_account import Account

def sign_evm_payment(payment_requirements, wallet_address, private_key):
    # Extract chain ID from CAIP-2 format (eip155:8453 -> 8453)
    chain_id = int(payment_requirements["network"].split(":")[1])
    
    # Build EIP-712 domain
    domain = {
        "name": payment_requirements["extra"]["name"],
        "version": payment_requirements["extra"]["version"],
        "chainId": chain_id,
        "verifyingContract": payment_requirements["asset"]
    }
    
    # Build authorization message
    nonce = "0x" + os.urandom(32).hex()
    now = int(time.time())
    message = {
        "from": wallet_address,
        "to": payment_requirements["payTo"],
        "value": payment_requirements["amount"],
        "validAfter": str(now - 600),
        "validBefore": str(now + payment_requirements["maxTimeoutSeconds"]),
        "nonce": nonce
    }
    
    # Sign with EIP-712
    account = Account.from_key(private_key)
    types = {
        "TransferWithAuthorization": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "validAfter", "type": "uint256"},
            {"name": "validBefore", "type": "uint256"},
            {"name": "nonce", "type": "bytes32"}
        ]
    }
    sig = account.sign_typed_data(domain, types, message)
    
    # Build X402 v2 payload
    payload = {
        "x402Version": 2,
        "resource": {
            "url": "/api/intents",
            "description": "AgentPay cross-chain payment",
            "mimeType": "application/json"
        },
        "accepted": payment_requirements,
        "payload": {
            "signature": sig.signature.hex(),
            "authorization": message
        }
    }
    
    # Encode as base64
    return base64.b64encode(json.dumps(payload).encode()).decode()

settle_proof = sign_evm_payment(payment_requirements, wallet_address, private_key)
print(f"Settle Proof: {settle_proof[:50]}...")
```

**Output:**
```
Settle Proof: eyJ4NDAyVmVyc2lvbiI6MiwidmVyc2lvbiI6IjIiLCJy...
```

---

### Step 4: Submit Proof & Poll Status
Your agent submits the signed proof and polls until the payment is settled on Base.

```bash
# Submit proof
curl -X POST "https://api-pay.agent.tech/api/intents/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{"settle_proof": "eyJ4NDAyVmVyc2lvbiI6Mn0..."}'

# Poll status (repeat every 2-3 seconds)
curl "https://api-pay.agent.tech/api/intents?intent_id=550e8400-e29b-41d4-a716-446655440000"
```

**Status Flow:**
```
AWAITING_PAYMENT → PENDING → SOURCE_SETTLED → BASE_SETTLING → BASE_SETTLED ✅
```

**Final Response:**
```json
{
  "intent_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "BASE_SETTLED",
  "sending_amount": "10.00",
  "receiving_amount": "9.95",
  "completed_at": "2026-02-05T17:35:42Z",
  "base_payment": {
    "tx_hash": "0xabc123...",
    "explorer_url": "https://basescan.org/tx/0xabc123...",
    "settled_at": "2026-02-05T17:35:42Z"
  }
}
```

**Payment complete! 🎉** The merchant received 9.95 USDC on Base.

---

## 🏗️ Architecture

```
┌─────────────┐
│  AI Agent   │
└──────┬──────┘
       │ 1. Create Intent
       ▼
┌─────────────────────┐
│  AgentPay API       │
│  api-pay.agent.tech │
└──────┬──────────────┘
       │ 2. Return payment_requirements
       ▼
┌─────────────┐
│  AI Agent   │ 3. Sign locally (EIP-712 / Solana TX)
│  (Local)    │ 4. Generate settle_proof
└──────┬──────┘
       │ 5. Submit settle_proof
       ▼
┌───────────────────┐
│  X402 Facilitator   │ 6. Verify & settle source chain
└──────┬──────────────┘
       │ 7. Execute Base payment
       ▼
┌─────────────────────┐
│  Merchant Wallet    │ ✅ Receives USDC on Base
│  (Base Chain)       │
└─────────────────────┘
```

---

## 🔐 Security Highlights

### Private Keys Never Leave Your Machine
- Wallets are generated locally using industry-standard libraries (`eth_account`, `solders`)
- Private keys are stored at `~/.config/x402pay/wallets.json` (or your preferred location)
- The API only receives the **signed proof** (base64-encoded X402 payload), never the private key

### X402 Protocol Authorization
- **EVM (Base)**: EIP-712 `TransferWithAuthorization` signature
  - Includes time bounds (`validAfter`, `validBefore`)
  - Uses cryptographic nonce to prevent replay attacks
  - Verifying contract is the USDC token contract on Base
  
- **Solana**: VersionedTransaction v0 with 3 instructions
  - SetComputeUnitLimit, SetComputeUnitPrice, TransferChecked
  - Signed with your local Solana keypair
  - Fee payer is provided by the backend (gasless for users)

### Verification Flow
1. API decodes `settle_proof` from base64
2. Parses JSON and validates X402 v2 payload structure
3. Verifies signature matches the payer wallet
4. Checks amount matches the intent
5. Forwards to X402 facilitator for on-chain settlement

**If any step fails, the payment is rejected with a 400 error.**

---

## 📊 Payment Status & Leaderboard

### Status Tracking
Poll `GET /api/intents?intent_id={id}` to track payment progress:

| Status | Description |
|--------|-------------|
| `AWAITING_PAYMENT` | Intent created, waiting for proof |
| `PENDING` | Proof submitted, verification in progress |
| `SOURCE_SETTLED` | Source chain payment confirmed |
| `BASE_SETTLING` | Base payment in progress |
| `BASE_SETTLED` | ✅ Complete! Merchant received USDC |
| `VERIFICATION_FAILED` | Invalid proof or settlement failed |
| `EXPIRED` | Intent timed out (default: 10 minutes) |

### Leaderboard
Track your agent's payment activity:

```bash
# Get global ranking
curl "https://api-pay.agent.tech/api/ranking?page=1&page_size=20"

# Get your wallet's rank
curl "https://api-pay.agent.tech/api/ranking/0xYourWalletAddress"
```

**Response:**
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "rank": 42,
  "base_score": 150.50,
  "referral_score": 25.00,
  "total_score": 175.50,
  "last_updated_at": "2026-02-05T17:30:00Z"
}
```

---

## 🚀 Quick Start for AI Agents

### Installation
```bash
# Python dependencies
pip install eth-account solders

# Node.js dependencies
npm install ethers @solana/web3.js
```

### Minimal Example (Python)
```python
import requests
import json
import base64
from eth_account import Account

# 1. Load your wallet
with open("~/.config/x402pay/wallets.json") as f:
    wallets = json.load(f)
evm_wallet = next(w for w in wallets["wallets"] if w["type"] == "evm")

# 2. Create intent
response = requests.post("https://api-pay.agent.tech/api/intents", json={
    "recipient": "0xReceiverAddress",
    "amount": "10",
    "payer_chain": "base"
})
intent = response.json()
intent_id = intent["intent_id"]
payment_requirements = intent["payment_requirements"]

# 3. Sign locally (use the sign_evm_payment function from Step 3)
settle_proof = sign_evm_payment(
    payment_requirements,
    evm_wallet["address"],
    evm_wallet["private_key"]
)

# 4. Submit proof
requests.post(f"https://api-pay.agent.tech/api/intents/{intent_id}", json={
    "settle_proof": settle_proof
})

# 5. Poll status
import time
while True:
    status_response = requests.get(f"https://api-pay.agent.tech/api/intents?intent_id={intent_id}")
    status = status_response.json()["status"]
    print(f"Status: {status}")
    if status in ["BASE_SETTLED", "EXPIRED", "VERIFICATION_FAILED"]:
        break
    time.sleep(3)
```

---

## 🛠️ API Reference

**Base URL:** `https://api-pay.agent.tech`

### POST /api/intents
Create a payment intent.

**Request:**
```json
{
  "email": "merchant@example.com",     // OR "recipient": "0x..."
  "amount": "10.50",                   // 0.01 - 1,000,000 USDC
  "payer_chain": "base"                // "base" or "solana"
}
```

**Response (201):**
```json
{
  "intent_id": "uuid",
  "merchant_recipient": "0x...",
  "sending_amount": "10.50",
  "receiving_amount": "10.45",
  "estimated_fee": "0.05",
  "payer_chain": "base",
  "status": "AWAITING_PAYMENT",
  "expires_at": "2026-02-05T17:40:00Z",
  "payment_requirements": { ... }
}
```

### POST /api/intents/{intent_id}
Submit signed proof.

**Request:**
```json
{
  "settle_proof": "eyJ4NDAyVmVyc2lvbiI6Mn0..."
}
```

**Response (200):**
```json
{
  "intent_id": "uuid",
  "status": "PENDING",
  ...
}
```

### GET /api/intents?intent_id={id}
Get payment status and receipt.

**Response (200):**
```json
{
  "intent_id": "uuid",
  "status": "BASE_SETTLED",
  "sending_amount": "10.50",
  "receiving_amount": "10.45",
  "completed_at": "2026-02-05T17:35:42Z",
  "source_payment": {
    "chain": "base",
    "tx_hash": "0x...",
    "explorer_url": "https://basescan.org/tx/0x..."
  },
  "base_payment": {
    "tx_hash": "0x...",
    "explorer_url": "https://basescan.org/tx/0x..."
  }
}
```

### GET /api/ranking
Get paginated leaderboard.

**Query params:** `page` (default 1), `page_size` (1-100, default 20)

### GET /api/ranking/{address}
Get wallet rank and score.

**Path:** EVM address (0x...) or Solana address (Base58)

### GET /health
Health check endpoint.

---

## ❌ Error Handling

| Code | Meaning |
|------|---------|
| 400 | Invalid input, proof validation failed, expired intent |
| 404 | Payment intent not found |
| 503 | Insufficient proxy balance (backend issue) |
| 500 | Internal server error |

**Example error response:**
```json
{
  "error": "proof validation failed",
  "message": "signature verification failed: invalid signature"
}
```

---

## 📝 Summary Checklist

- [ ] Generate EVM and/or Sts locally
- [ ] Save wallets to `~/.config/x402pay/wallets.json`
- [ ] Create intent: `POST /api/intents`
- [ ] Sign X402 using `payment_requirements` (EIP-712 or Solana TX)
- [ ] Build X402 v2 payload and encode as base64
- [ ] Submit: `POST /api/intents/{intent_id}` with `settle_proof`
- [ ] Poll: `GET /api/intents?intent_id={id}` until `BASE_SETTLED`
- [ ] Optional: Check leaderboard with `GET /api/ranking/{address}`

---

## 🎯 Use Cases

### For AI Agents
- **Autonomous payments**: Your agent can pay for API credits, subscriptions, or services
- **Tipping**: Reward content creators or other agents
- **Payroll**: Distribute payments to multiple recipients
- **Escrow**: Hold funds until conditions are met

### For Merchants
- **Accept crypto payments**: Receive USDC on Base from any payer chain
- **Email-based payments**: Customers pay to your email (resolved via Privy)
- **Real-time settlement**: Funds arrive in minutes, not days
- **No volatility risk**: Always receive USDC (stablecoin)

---

## 🔗 Links

- **API Base URL**: https://api-pay.agent.tech
- **Health Check**: https://api-pay.agent.tech/health
- **X402 Protocol**: [Learn more about X402](https://x402.org)
- **Supported Chains**: Base (EVM), Solana

---

## 📄 License

MIT License - Use freely in your AI agent projects.

---

**Built for the SpoonOS Skills Micro Challenge 🥄**
