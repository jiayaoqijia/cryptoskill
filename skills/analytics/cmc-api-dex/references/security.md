# DEX Security API

## Security Detail

**Path:** `GET /v1/dex/security/detail`

**Description:** Get security and risk analysis for a DEX token. Returns contract audit status, risk signals, holder concentration, and potential red flags. Critical for due diligence before trading.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | Yes* | Network identifier (e.g., ethereum, solana, bsc) |
| platform_crypto_id | integer | Yes* | Alternative to network_slug, use platform's CMC ID |
| contract_address | string | Yes | Token's contract address |

*One of network_slug or platform_crypto_id is required.

### Response Fields

| Field | Description |
|-------|-------------|
| contract_address | Token contract address |
| network_slug | Network identifier |
| overall_risk_score | Aggregate risk score (0-100, higher = riskier) |
| risk_level | Risk category (low, medium, high, critical) |
| contract_verified | Whether contract source is verified |
| contract_audit | Audit information |
| contract_audit.audited | Whether contract has been audited |
| contract_audit.auditor | Auditing firm name |
| contract_audit.audit_date | Date of audit |
| contract_audit.audit_url | Link to audit report |
| ownership | Contract ownership info |
| ownership.owner_address | Owner wallet address |
| ownership.is_renounced | Whether ownership is renounced |
| ownership.can_mint | Whether owner can mint new tokens |
| ownership.can_pause | Whether owner can pause trading |
| ownership.can_blacklist | Whether owner can blacklist addresses |
| ownership.can_modify_fees | Whether owner can change fees |
| liquidity_lock | Liquidity lock information |
| liquidity_lock.is_locked | Whether liquidity is locked |
| liquidity_lock.locked_percent | Percentage of liquidity locked |
| liquidity_lock.unlock_date | When liquidity unlocks |
| liquidity_lock.lock_platform | Locking platform (UniCrypt, PinkLock, etc.) |
| holder_analysis | Token holder distribution |
| holder_analysis.total_holders | Total number of holders |
| holder_analysis.top_10_percent | % held by top 10 wallets |
| holder_analysis.top_100_percent | % held by top 100 wallets |
| holder_analysis.creator_holding_percent | % held by token creator |
| trading_flags | Trading-related red flags |
| trading_flags.has_honeypot_risk | Potential honeypot (can't sell) |
| trading_flags.has_high_tax | High buy/sell tax (>10%) |
| trading_flags.buy_tax_percent | Buy tax percentage |
| trading_flags.sell_tax_percent | Sell tax percentage |
| trading_flags.has_transfer_cooldown | Cooldown between transfers |
| trading_flags.has_max_transaction | Maximum transaction limit |
| trading_flags.has_anti_whale | Anti-whale mechanisms |
| contract_flags | Contract-related red flags |
| contract_flags.is_proxy | Uses proxy contract (upgradeable) |
| contract_flags.has_external_calls | Makes external contract calls |
| contract_flags.has_hidden_owner | Hidden owner functions |
| contract_flags.has_self_destruct | Can self-destruct |
| social_signals | Social presence indicators |
| social_signals.has_website | Whether project has website |
| social_signals.has_social_media | Whether project has socials |
| social_signals.has_whitepaper | Whether whitepaper exists |
| warnings | Array of specific warning messages |
| last_updated | When security data was last updated |

### Risk Level Interpretation

| Level | Score | Meaning |
|-------|-------|---------|
| low | 0-25 | Generally safe, standard risks |
| medium | 26-50 | Some concerns, proceed with caution |
| high | 51-75 | Significant risks, high caution advised |
| critical | 76-100 | Major red flags, avoid or extreme caution |

### Common Warning Types

1. **Honeypot**: Token may not be sellable
2. **High Tax**: Buy/sell taxes exceed normal levels
3. **Concentrated Holdings**: Top wallets hold excessive supply
4. **Unverified Contract**: Source code not verified
5. **Unlocked Liquidity**: LP tokens not locked
6. **Mintable**: Owner can create unlimited tokens
7. **Proxy Contract**: Code can be changed
8. **No Audit**: Contract has not been audited

### Example

```bash
# Check security for a token
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/security/detail?network_slug=ethereum&contract_address=0x6982508145454Ce325dDbE47a25d4ec3d2311933" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

```bash
# Check Solana token security
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/security/detail?network_slug=solana&contract_address=DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

```bash
# Check BSC token security using platform ID
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/security/detail?platform_crypto_id=1839&contract_address=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Security Check Workflow

Before trading any DEX token:

1. Get token address from search or discovery endpoints
2. Call security/detail to get risk analysis
3. Check overall_risk_score and risk_level
4. Review specific flags:
   - `has_honeypot_risk` - Critical, do not buy if true
   - `buy_tax_percent` / `sell_tax_percent` - Ensure acceptable
   - `liquidity_lock.is_locked` - Prefer locked liquidity
   - `ownership.is_renounced` - Safer if renounced
   - `holder_analysis.top_10_percent` - Watch for concentration
5. Review warnings array for specific concerns
6. Make informed decision based on risk tolerance

### Example Response Structure

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null
  },
  "data": {
    "contract_address": "0x6982508145454Ce325dDbE47a25d4ec3d2311933",
    "network_slug": "ethereum",
    "overall_risk_score": 35,
    "risk_level": "medium",
    "contract_verified": true,
    "contract_audit": {
      "audited": false,
      "auditor": null,
      "audit_date": null,
      "audit_url": null
    },
    "ownership": {
      "owner_address": "0x0000000000000000000000000000000000000000",
      "is_renounced": true,
      "can_mint": false,
      "can_pause": false,
      "can_blacklist": false,
      "can_modify_fees": false
    },
    "liquidity_lock": {
      "is_locked": true,
      "locked_percent": 85,
      "unlock_date": "2025-06-15T00:00:00.000Z",
      "lock_platform": "UniCrypt"
    },
    "holder_analysis": {
      "total_holders": 150000,
      "top_10_percent": 25.5,
      "top_100_percent": 45.2,
      "creator_holding_percent": 0
    },
    "trading_flags": {
      "has_honeypot_risk": false,
      "has_high_tax": false,
      "buy_tax_percent": 0,
      "sell_tax_percent": 0,
      "has_transfer_cooldown": false,
      "has_max_transaction": false,
      "has_anti_whale": false
    },
    "contract_flags": {
      "is_proxy": false,
      "has_external_calls": false,
      "has_hidden_owner": false,
      "has_self_destruct": false
    },
    "social_signals": {
      "has_website": true,
      "has_social_media": true,
      "has_whitepaper": false
    },
    "warnings": [
      "Contract has not been audited",
      "Top 10 holders control 25% of supply"
    ],
    "last_updated": "2024-01-15T11:30:00.000Z"
  }
}
```
