# Aave V3 GraphQL API Reference

## Endpoint

**URL:** `https://api.v3.aave.com/graphql`

**Method:** POST

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

## Query: User Account & Position Data

### Query Definition

```graphql
query GetUserPosition($address: String!) {
  userAccount(id: $address) {
    id
    healthFactor
    totalCollateralBase
    totalDebtBase
    reserves(where: { currentTotalDebt_gt: "0" }) {
      reserve {
        symbol
        decimals
        price {
          priceInEth
        }
        baseLTVasCollateral
        liquidationThreshold
      }
      currentTotalDebt
      currentVariableDebt
      currentStableDebt
      scaledVariableDebt
      scaledStableDebt
    }
    supplies(where: { scaledBalance_gt: "0" }) {
      reserve {
        symbol
        decimals
        price {
          priceInEth
        }
      }
      scaledBalance
      balance
    }
  }
}
```

### Variables

```json
{
  "address": "0x1234567890abcdef1234567890abcdef12345678"
}
```

**Note:** Address is automatically converted to lowercase in the query.

### Response Structure

#### Root: `userAccount`

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Wallet address (lowercase) |
| `healthFactor` | String (Ray: 10^27) | Health factor. 1.0 = liquidation threshold. Values >1 = safe. |
| `totalCollateralBase` | String (Ray: 10^27) | Total supplied assets value in ETH (base currency). Can be used as collateral. |
| `totalDebtBase` | String (Ray: 10^27) | Total borrowed assets value in ETH (base currency). Subject to interest. |

#### Sub-field: `reserves` (Borrowed Assets)

Array of assets with active debt. Each reserve contains:

| Field | Type | Description |
|-------|------|-------------|
| `reserve.symbol` | String | Asset symbol (e.g., "USDC", "WETH", "USDT") |
| `reserve.decimals` | Int | Decimal places for this asset (e.g., 6 for USDC, 18 for WETH) |
| `reserve.price.priceInEth` | String (Ray) | Price of 1 unit in ETH |
| `reserve.baseLTVasCollateral` | String (percentage, 1-100) | Base LTV % for collateral (e.g., 75 = 75% LTV) |
| `reserve.liquidationThreshold` | String (percentage, 1-100) | Liquidation threshold % (e.g., 80 = liquidation at 80% debt ratio) |
| `currentTotalDebt` | String (in asset decimals) | Total debt (variable + stable) |
| `currentVariableDebt` | String (in asset decimals) | Variable-rate debt (interest accrues) |
| `currentStableDebt` | String (in asset decimals) | Stable-rate debt (fixed interest) |
| `scaledVariableDebt` | String | Internal representation (for calculations) |
| `scaledStableDebt` | String | Internal representation (for calculations) |

**Example:**
```json
{
  "symbol": "USDC",
  "decimals": 6,
  "currentTotalDebt": "15000000000",  // 15,000 USDC (6 decimals)
  "currentVariableDebt": "10000000000",  // Variable
  "currentStableDebt": "5000000000"   // Stable
}
```

To convert: `15000000000 / (10 ^ 6) = 15000 USDC`

#### Sub-field: `supplies` (Supplied Assets / Collateral)

Array of assets you've supplied to Aave. Each supply contains:

| Field | Type | Description |
|-------|------|-------------|
| `reserve.symbol` | String | Asset symbol (e.g., "WETH", "USDC", "aEth") |
| `reserve.decimals` | Int | Decimal places |
| `reserve.price.priceInEth` | String (Ray) | Price in ETH |
| `scaledBalance` | String | Scaled balance (interest-bearing) |
| `balance` | String | Actual balance in asset units |

**Example:**
```json
{
  "symbol": "WETH",
  "decimals": 18,
  "balance": "10000000000000000000"  // 10 WETH (18 decimals)
}
```

To convert: `10000000000000000000 / (10 ^ 18) = 10 WETH`

---

## Key Calculations

### Health Factor (HF)

**Formula:**
```
HF = Total Collateral × Avg Liquidation Threshold / Total Debt
```

Aave returns `healthFactor` directly as a Ray (10^27). To convert to decimal:

```javascript
const hfDecimal = parseInt(healthFactor) / 1e27;
```

**Examples:**
- HF = 2.0 → Safe (20% buffer above liquidation)
- HF = 1.2 → Warning (only 20% buffer)
- HF = 1.05 → Critical (5% buffer)
- HF = 1.0 → Liquidation threshold (liquidators can seize)
- HF < 1.0 → Liquidation in progress

### Debt Ratio

```javascript
const totalDebtEth = parseInt(totalDebtBase) / 1e27;
const totalCollateralEth = parseInt(totalCollateralBase) / 1e27;
const debtRatio = (totalDebtEth / totalCollateralEth) * 100;
```

Example: 60% debt ratio = you borrowed 60% of your collateral value.

### Converting Ray Values to Decimals

Aave uses Ray (10^27) for large precision. To convert:

```javascript
// For totalCollateralBase, totalDebtBase (already in base currency, ETH)
const valueInEth = parseInt(valueString) / 1e27;

// For asset amounts (use decimals)
const valueInAsset = parseInt(valueString) / (10 ** decimals);

// For healthFactor
const hf = parseInt(healthFactor) / 1e27;
```

---

## Chain Configuration

### Ethereum Mainnet

```
Endpoint: https://api.v3.aave.com/graphql
Chain ID: 1
```

### Polygon

```
Endpoint: https://api.v3.aave.com/graphql?chainId=137
Chain ID: 137
```

### Arbitrum

```
Endpoint: https://api.v3.aave.com/graphql?chainId=42161
Chain ID: 42161
```

### Other Chains

- Optimism (10)
- Base (8453)
- Avalanche (43114)
- Gnosis (100)

Append `?chainId=<chainId>` to the base endpoint.

---

## Error Responses

### GraphQL Error: Invalid Address

```json
{
  "errors": [
    {
      "message": "Invalid user address format"
    }
  ]
}
```

**Solution:** Ensure address is `0x` + 40 hex chars.

### GraphQL Error: User Not Found

```json
{
  "data": {
    "userAccount": null
  }
}
```

**Meaning:** Wallet has no Aave position on this chain. Either:
- No supplies/borrows
- Wrong chain selected
- Wrong wallet address

### HTTP Error: 503 Service Unavailable

```
Status: 503
Body: Service temporarily unavailable
```

**Handling:** Retry with exponential backoff. Aave API is generally reliable (99.9% uptime).

---

## Example Request/Response

### Request

```bash
curl -X POST https://api.v3.aave.com/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query GetUserPosition($address: String!) { userAccount(id: $address) { healthFactor totalCollateralBase totalDebtBase } }",
    "variables": {
      "address": "0x1234567890abcdef1234567890abcdef12345678"
    }
  }'
```

### Response (200 OK)

```json
{
  "data": {
    "userAccount": {
      "healthFactor": "2310000000000000000000000000",
      "totalCollateralBase": "50342120000000000000000000000",
      "totalDebtBase": "21804000000000000000000000000"
    }
  }
}
```

**Converted to decimals:**
- HF: 2.31
- Total Collateral: $50,342.12 (in ETH equivalent)
- Total Debt: $21,804 (in ETH equivalent)

---

## Performance Notes

- **Latency:** Typically 200–500ms per request
- **Rate Limits:** No strict public rate limits; but don't spam (>1000 req/min flagged)
- **Caching:** Aave data updates on-chain every block (~12 seconds on Ethereum)
- **Recommendations:**
  - Check every 6 hours for stable positions
  - Check every 2–4 hours for leveraged positions
  - Cache results for 1–5 minutes if querying frequently

---

## Future Enhancements

Aave GraphQL API support for:
- eMode status and LTV
- Isolated collateral info
- Flash loan eligibility
- Interest rate mode details
- Cooldown periods on collateral

Check Aave docs for latest schema: https://aave.com/docs

