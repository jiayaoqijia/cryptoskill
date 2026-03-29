# Wallets

Create and manage agent-controlled wallets.

## Create Wallet

```bash
POST /v1/wallets
```

### Request

```json
{
  "chain_type": "ethereum",
  "policy_ids": ["<policy_id>"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain_type` | string | Yes | `ethereum`, `solana`, or extended chain |
| `policy_ids` | string[] | No | Policy IDs to enforce (max 1) |
| `owner` | object | No | Owner config (public_key or user_id) |

### Response

```json
{
  "id": "id2tptkqrxd39qo9j423etij",
  "address": "0x...",
  "chain_type": "ethereum",
  "policy_ids": [],
  "owner_id": "rkiz0ivz254drv1xw982v3jq",
  "created_at": 1741834854578
}
```

## List Wallets

```bash
GET /v1/wallets
```

Query parameters:
- `chain_type` — Filter by chain
- `limit` — Max results (default 100)
- `cursor` — Pagination cursor

## Get Wallet

```bash
GET /v1/wallets/{wallet_id}
```

## Update Wallet

```bash
PATCH /v1/wallets/{wallet_id}
```

Update policy assignment:

```json
{
  "policy_ids": ["<new_policy_id>"]
}
```

## Delete Wallet

```bash
DELETE /v1/wallets/{wallet_id}
```

## Get Balance

```bash
GET /v1/wallets/{wallet_id}/balance
```

Returns native token balance for the wallet's chain.

## Wallet Chain Types

### First-Class Support
- `ethereum` — EVM chains (ETH, Base, Polygon, Arbitrum, etc.)
- `solana` — Solana mainnet/devnet

### Extended Support
- `cosmos` — Cosmos ecosystem
- `stellar` — Stellar network
- `sui` — Sui blockchain
- `aptos` — Aptos blockchain
- `tron` — Tron network
- `bitcoin-segwit` — Bitcoin SegWit
- `near` — NEAR Protocol
- `ton` — TON blockchain
- `starknet` — StarkNet L2
