# x402 Payment Details

Technical details for manual x402 integration or debugging payment issues.

## How Payment Works

1. Make a request to any x402 endpoint
2. Server responds with HTTP 402 and a Payment-Required header
3. Your wallet signs a USDC transferWithAuthorization (EIP-3009) message
4. Resend the request with the signed PAYMENT-SIGNATURE header
5. Server verifies signature, processes request, returns data
6. On-chain USDC transfer executes only upon successful delivery

## Payment Configuration

| Field | Value |
|-------|-------|
| Network | Base (Chain ID: 8453) |
| Asset | USDC |
| USDC Contract | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Payment Recipient | `0x271189c860DB25bC43173B0335784aD68a680908` |
| Amount | 10000 (= $0.01 USDC, 6 decimals) |
| Method | EIP-3009 transferWithAuthorization |

## 402 Response Format

When a request lacks a valid PAYMENT-SIGNATURE, the server returns HTTP 402 with a base64-encoded Payment-Required header:

```json
{
  "x402Version": 2,
  "error": "Payment required",
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "amount": "10000",
      "payTo": "0x271189c860DB25bC43173B0335784aD68a680908",
      "maxTimeoutSeconds": 30,
      "extra": {
        "name": "USD Coin",
        "version": "2"
      }
    }
  ]
}
```

### Field Descriptions

| Field | Description |
|-------|-------------|
| scheme | Payment scheme. "exact" means EIP-3009 transferWithAuthorization |
| network | Target chain in CAIP-2 format. eip155:8453 = Base Mainnet |
| asset | USDC contract address on Base |
| amount | Payment in smallest unit (10000 = $0.01 with 6 decimals) |
| payTo | Recipient address for payment |
| maxTimeoutSeconds | Validity window for signed authorization (typically 30s) |
| extra.name | EIP-712 domain name for the token |
| extra.version | EIP-712 domain version |

## EIP-712 Domain

When constructing the transferWithAuthorization signature for USDC on Base:

```
name: "USD Coin"
version: "2"
```

## Manual Flow with curl

```bash
# Step 1: Get the 402 response with payment requirements
curl -s -D - 'https://pro.coinmarketcap.com/x402/v1/dex/search?q=bnb'

# Step 2: Sign the payment using your x402 client or custom implementation

# Step 3: Retry with the payment signature
curl --request GET \
  --url 'https://pro.coinmarketcap.com/x402/v1/dex/search?q=bnb' \
  -H 'PAYMENT-SIGNATURE: <base64-encoded-payment-payload>'
```

## Important Notes

1. **Pay only on success** - On-chain transfer executes only when server returns data successfully
2. **Authorization expiry** - Signed authorizations expire after maxTimeoutSeconds. Unused authorizations are never submitted on-chain
3. **No API key** - x402 payment replaces traditional API key authentication
