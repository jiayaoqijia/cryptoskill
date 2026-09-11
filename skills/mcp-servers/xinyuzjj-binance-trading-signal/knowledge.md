# Trading Signal Parameter Knowledge Base

Domain knowledge for meme-rush and fomo-call strategy configuration. Use this when explaining parameters to users, suggesting values, or assessing risk.

All field names below have been verified against the live `count-signals` API (BSC + Solana). Fields not listed here are rejected by the backend (`13323002 Invalid strategy params`).

---

## 1. meme-rush Parameters

meme-rush monitors on-chain token metrics and triggers a signal when a token's metrics satisfy the configured conditions. It has the most parameters of all signal types (20+ fields).

### Token Market & Liquidity

| Parameter | Unit | Description |
|-----------|------|-------------|
| `market_cap` | K (10 = $10K) | Token market capitalization. Higher = more mature, lower = more speculative |
| `liquidity` | K (10 = $10K) | DEX pool liquidity. Higher = lower slippage, easier exits |
| `volume` | K (1 = $1K) | 24-hour trading volume. Reflects trading activity and attention |
| `tx_count` | count | 24-hour total transaction count. Reflects trading frequency |
| `buy_tx_count` | count | 24-hour buy transaction count. More buys than sells may indicate accumulation |
| `sell_tx_count` | count | 24-hour sell transaction count. More sells may indicate selling pressure |

### Holder Structure

| Parameter | Unit | Description |
|-----------|------|-------------|
| `holders` | count | Unique holder count. More holders = wider distribution, lower manipulation risk |
| `binance_holders` | count | Binance user holders. Can be considered "smart money" indicator |
| `pro_traders` | count | Professional trader holders. May indicate higher token quality |
| `kol_holders` | count | KOL holders. KOL accumulation is a strong bullish signal |

### Holding Concentration

All `*_percentage` fields use 0-100 range. `min: null` means no lower bound, `max: null` means no upper bound.

| Parameter | Risk Implication |
|-----------|------------------|
| `top10_holders_percentage` | High = whale dominance, high dump risk |
| `dev_holding_percentage` | High = developer may sell at any time |
| `sniper_holding_percentage` | High = unhealthy token structure |
| `bundler_holding_percentage` | High = possible manipulation |
| `insider_holding_percentage` | High = insider trading risk |
| `new_wallet_holding_percentage` | High = possible wash trading or Sybil attacks |
| `kol_holding_percentage` | Evaluate together with `kol_holders` count |
| `binance_holders_percentage` | Binance holder percentage |

### Token Attributes

| Parameter | Type | Description |
|-----------|------|-------------|
| `age` | `[{min, max}]` minutes | Minutes since token creation. <10min = highest risk/highest potential |
| `bonding_curve` | `[{min, max}]` % | Bonding curve progress (0-100). For bonding curve tokens |
| `single_attributes` | `string[]` | Special attributes: `"x"` (has X/Twitter), `"website"` (has official site), `"dexScreen"` (DexScreener paid ad) |
| `dev_address` | `string[][]` | Developer wallet address (2D array, same OR/AND logic as protocol_code) |

### Chain-Specific Fields

| Parameter | Type | Description |
|-----------|------|-------------|
| `protocol_code` | `number[][]` | Launch platform code. 2D array — outer = AND (Cartesian), inner = OR. 1xxx = Solana, 2xxx = BSC |
| `pair_anchor_address` | `string[]` | Anchor token symbols for trading pairs. Chain-specific values |

#### protocol_code by chain

| Chain | chainId | Codes |
|-------|---------|-------|
| BSC | `56` | `2001` (FourMeme), `2002` (Flap) |
| Solana | `CT_501` | `1001` (PumpFun), `1003` (PumpSwap), `1004` (LaunchLab), `1005` (RaydiumAMM), `1006` (RaydiumCPMM), `1007` (RaydiumCLMM), `1008` (Bonk), `1009` (DynamicBC), `1010` (Moonshot), `1011` (JupiterStudio), `1012` (Bags), `1013` (Believe), `1014` (MeteoraAMMV2), `1015` (MeteoraAMM), `1016` (Orca) |

> Protocol codes may be updated by the backend. To discover currently valid codes, run `baw signal explore -c <chainId> --json` and inspect existing strategies. The backend does not validate specific code values — unknown codes are accepted but will match zero tokens.

#### pair_anchor_address by chain

| Chain | Valid anchor tokens |
|-------|---------------------|
| BSC (`56`) | `BNB`, `USD1`, `USDT`, `ASTER`, `CAKE`, `U`, `FORM`, `OTHER` |
| Solana (`CT_501`) | `SOL`, `USD1`, `USDT`, `USDC`, `OTHER` |

### Backtest Config

| Field | Type | Description |
|-------|------|-------------|
| `backtest.enabled` | boolean | Whether to enable backtest |
| `backtest.time_range` | string | `"7d"` or `"30d"` |

> **fomo-call does not support backtesting.** Do not set `backtest.enabled = true` for fomo-call strategies.

---

## 2. fomo-call Parameters

fomo-call detects herd buying behavior: within X minutes, more than Y addresses each spend at least Z USD buying the same token.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `selectedGroups` | object (single) | yes | Monitored wallet group. Use `presetGroup: "KOL"` / `"SMY"` or `customGroupId: <id>` |
| `strategy` | object (single) | yes | Detection thresholds |
| `tokenMarketCapRange` | object (single) | no | Token market cap filter |
| `signalName` | string | no | Custom signal name |
| `isOpen` | boolean | no | Whether signal is active |

### strategy object

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `"loose"` / `"moderate"` / `"strict"` / `"custom"` |
| `minWallets` | integer | Minimum number of addresses |
| `timeWindowMinutes` | integer | Detection time window (minutes) |
| `minBuyAmountPerWalletUSD` | number | Minimum buy amount per wallet (USD) |

### tokenMarketCapRange object

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `"low"` / `"mid"` / `"large"` / `"custom"` (case-insensitive) |
| `minUSD` | number | Minimum market cap |
| `maxUSD` | number | Maximum market cap |

---

## 3. Safety Considerations

These are recommended thresholds, not backend-enforced limits. Warn users proactively when they relax safety parameters.

| Parameter | Safety Concern | Recommended Threshold |
|-----------|----------------|----------------------|
| `holders` | Too few (<100) = low popularity, easy manipulation | min >= 100 |
| `liquidity` | Too low (<$5K) = high slippage, difficult exits | min >= $5K-$10K (config value 5-10) |
| `top10_holders_percentage` | Too high (>70%) = whale dominance, dump risk | max <= 60-70 |
| `dev_holding_percentage` | Too high (>10%) = developer can sell anytime | max <= 10-15 |
| `sniper_holding_percentage` | Too high (>10%) = unhealthy structure | max <= 10 |
| `bundler_holding_percentage` | Too high (>10%) = possible manipulation | max <= 10 |
| `new_wallet_holding_percentage` | Too high (>20%) = wash trading/Sybil risk | max <= 20-25 |
| `age` | Very young (<5min) = extremely high risk | Warn user |
| `market_cap` | Very small (<$10K) = extremely volatile | Warn user |

### Safety Principles

1. **Must warn when users relax safety parameters**: If user sets `holders` min to 10 or `top10_holders_percentage` max to 90%, communicate the risk clearly.
2. **Escalate when multiple high-risk parameters overlap**: Low holders + high dev holdings + low liquidity = extreme Rug Pull risk.
3. **Do not block user actions**: After warning, still execute the user's configuration request.

---

## 4. Parameter Correlations

### Positive Correlations

- **market_cap ↔ liquidity**: High market cap tokens usually have high liquidity. High cap + low liquidity = anomalous, warrants caution.
- **market_cap ↔ holders**: More holders usually means higher market cap. Very high cap but few holders = highly concentrated.
- **kol_holders ↔ pro_traders**: Both represent "smart money." Simultaneous threshold hits = stronger signal.

### Negative Correlations

- **holders ↔ top10_holders_percentage**: Expected inverse. Many holders but still high top10% = extremely uneven distribution.

### Ratio Analysis

- **volume ↔ tx_count**: High volume + low tx_count = few large orders (whale activity). High tx_count + low volume = many small orders (retail).
- **buy_tx_count vs sell_tx_count**: More buys = capital accumulation. More sells = capital flight.

### Attribute Correlations

- **age ↔ holders**: Older tokens typically have more holders. Very young but many holders = possible airdrop or bot activity.
- **protocol_code ↔ chainId**: 1xxx = Solana (`CT_501`), 2xxx = BSC (`56`). Must be consistent — do not mix codes from different chains.

---

## 5. Risk Profile Presets

### Conservative (Low Risk, Fewer Signals)

```
holders:                    min >= 500
liquidity:                  min >= $50K (config: 50)
market_cap:                 min >= $100K (config: 100)
top10_holders_percentage:   max <= 50
dev_holding_percentage:     max <= 5
sniper_holding_percentage:  max <= 5
age:                        min >= 60 minutes
```

Characteristics: Filters for mature tokens with established holder base. Fewer signals but higher quality. Suitable for risk-averse users.

### Balanced (Medium Risk)

```
holders:                    min >= 100-500
liquidity:                  min >= $10K-$50K (config: 10-50)
market_cap:                 min >= $20K (config: 20)
top10_holders_percentage:   max <= 60-70
dev_holding_percentage:     max <= 10
sniper_holding_percentage:  max <= 10
kol_holders:                min >= 1
age:                        min >= 10 minutes
```

Characteristics: Balance between safety and opportunity. Requires some KOL participation as quality filter. Suitable for most users.

### Aggressive (High Risk, More Signals)

```
holders:                    min >= 20-50
liquidity:                  min >= $2K-$5K (config: 2-5)
market_cap:                 min >= $5K (config: 5)
top10_holders_percentage:   max <= 80
age:                        min >= 2 minutes
```

Characteristics: Aims to get in early before widespread attention. More signals but significantly higher Rug Pull risk. Only suitable for experienced users who can afford losses. **Must explicitly warn about risks.**

---

## 6. Configuration Format Notes

### Range Fields

All range parameters use `[{min, max}]` array format. `max: null` means no upper limit:

```json
"holders": [{"min": 100, "max": null}]
```

Multiple ranges in the array use OR logic: `[{"min":0,"max":100}, {"min":500,"max":null}]` = "<100 OR >500".

### protocol_code 2D Array

Outer array = Cartesian product (AND), inner array = OR:

```json
"protocol_code": [[1001, 1003], [2001]]
```

This generates 2 sub-strategies: (PumpFun OR PumpSwap) AND (FourMeme). Cross-chain combinations are valid syntactically but will match zero tokens.

### Unit Conversion

meme-rush config values use K units for monetary fields — the backend converts internally:

| Field | Config value | Actual USD |
|-------|-------------|------------|
| `liquidity` | 10 | $10,000 |
| `volume` | 1 | $1,000 |
| `market_cap` | 100 | $100,000 |

`age` is in minutes. All `*_percentage` fields are 0-100. `tx_count` / `buy_tx_count` / `sell_tx_count` / `holders` / `kol_holders` etc. are raw counts.

fomo-call uses direct USD values (not K): `minBuyAmountPerWalletUSD: 200` = $200.

### Fields Not Supported by Backend

The following fields from older reference docs are **rejected** by the backend (`13323002`):

| Removed Field | Status |
|---------------|--------|
| `volume_24h` | Use `volume` instead |
| `pump_live_start` | Removed — do not use |
| `price_percent_change_24h` | Removed — do not use |
| `notify_on_complete` | Removed — do not use |

The backend performs strict schema validation — unknown fields cause `13323002`. Only use the fields documented above.
