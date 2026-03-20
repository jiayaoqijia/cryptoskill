# x402 Endpoints

## Discovery Endpoints (Free)

These endpoints require no payment and help agents explore available x402 endpoints.

### List All Available Endpoints

**Endpoint:** `GET /v1/x402/endpoints`
**Cost:** Free

```bash
curl https://x402.goldrush.dev/v1/x402/endpoints | jq
```

### Search Endpoints by Keyword

**Endpoint:** `GET /v1/x402/search?q={query}`
**Cost:** Free

```bash
curl https://x402.goldrush.dev/v1/x402/search?q=balance | jq
```

### Get Endpoint Details

**Endpoint:** `GET /v1/x402/endpoints/{endpoint-name}`
**Cost:** Free

```bash
curl https://x402.goldrush.dev/v1/x402/endpoints/get-token-balances-for-address | jq
```

---

## Data Endpoints (Paid via x402)

All 60+ Foundational API endpoints are available through the x402 proxy. Endpoint paths mirror the Foundational API.

**Base URL:** `https://x402.goldrush.dev/v1` (replaces `https://api.covalenthq.com/v1`)

### Key Data Endpoints

| Endpoint | Path | Pricing |
|----------|------|---------|
| Token Balances | `/v1/{chain}/address/{wallet}/balances_v2/` | Fixed |
| Native Balance | `/v1/{chain}/address/{wallet}/balances_native/` | Fixed |
| Transaction History | `/v1/{chain}/address/{wallet}/transactions_v3/?tier={tier}` | Tiered |
| Recent Transactions | `/v1/{chain}/address/{wallet}/transactions_v3/?tier=small` | Tiered |
| Single Transaction | `/v1/{chain}/transaction_v2/{txHash}/` | Fixed |
| NFT Holdings | `/v1/{chain}/address/{wallet}/balances_nft/` | Fixed |
| Token Prices | `/v1/pricing/historical_by_addresses_v2/{chain}/{currency}/{contract}/` | Fixed |
| Block Details | `/v1/{chain}/block_v2/{blockHeight}/` | Fixed |
| Token Approvals | `/v1/{chain}/approvals/{wallet}/` | Fixed |
| ERC20 Transfers | `/v1/{chain}/address/{wallet}/transfers_v2/` | Tiered |
| Cross-Chain Activity | `/v1/address/{wallet}/activity/` | Fixed |
| Multi-Chain Balances | `/v1/address/{wallet}/balances_multi/` | Fixed |

For the complete list, use: `GET /v1/x402/endpoints`

---

> **Note:** For detailed endpoint documentation (parameters, response schemas, use cases),
> see the **GoldRush Foundational API** skill reference files. The x402 proxy serves the
> exact same endpoints with the same parameters and response format.