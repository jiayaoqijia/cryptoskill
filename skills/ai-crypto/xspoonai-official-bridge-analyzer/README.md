# Cross-Chain Bridge Analyzer

**Analyze, compare, and risk-score cross-chain bridges -- the most critical infrastructure in multi-chain DeFi.**

Cross-chain bridges are the #1 target for exploits in crypto, with over **$2.5 billion** lost to bridge hacks since 2021. This skill gives you real-time intelligence on 30+ bridge protocols using free DeFiLlama APIs, helping you make informed decisions about which bridges to trust with your assets.

---

## Why Use Bridge Analyzer?

| Feature | Manual Research | Aggregator Sites | Bridge Analyzer |
|---------|----------------|-------------------|-----------------|
| Real-time volume data | Check each bridge individually | Partial coverage | All bridges, one query |
| Risk scoring | Subjective guesswork | Not available | Quantitative 0-10 scale |
| Security history | Search news manually | Incomplete | Curated exploit database |
| Route optimization | Compare 5+ sites | Basic suggestions | Priority-weighted ranking |
| Anomaly detection | Impossible in real-time | Not available | Automated threshold alerts |
| Design type analysis | Read whitepapers | Rare | Built-in classification |
| Audit status | Check each project | Inconsistent | Curated audit records |
| Cost | Hours of research | Free/paid mix | Free, instant |

---

## Quick Start

### Compare Top Bridges

```bash
echo '{"top": 10}' | python3 scripts/bridge_comparison.py
```

### Risk-Score a Bridge

```bash
echo '{"bridge_name": "stargate"}' | python3 scripts/bridge_risk_scorer.py
```

### Find Best Route

```bash
echo '{"source_chain": "ethereum", "destination_chain": "arbitrum", "priority": "safety"}' | python3 scripts/route_optimizer.py
```

### Monitor for Anomalies

```bash
echo '{"alert_threshold": 20}' | python3 scripts/bridge_monitor.py
```

---

## Script Documentation

### 1. bridge_comparison.py

Compare bridge protocols side by side using real-time DeFiLlama data.

**API Endpoint:** `https://bridges.llama.fi/bridges?includeChains=true`

#### Input Options

**Compare specific bridges:**
```json
{
  "bridges": ["stargate", "across", "hop", "wormhole"]
}
```

**Top N bridges by volume:**
```json
{
  "top": 10,
  "sort_by": "volume"
}
```

**Bridges supporting a chain:**
```json
{
  "chain": "arbitrum"
}
```

#### Output

```json
{
  "success": true,
  "data": {
    "bridges": [
      {
        "name": "Stargate",
        "display_name": "Stargate",
        "volume_24h": 15234567.89,
        "volume_1h": 634521.12,
        "chains_count": 12,
        "chains": ["Ethereum", "Arbitrum", "Optimism", "Polygon", "BSC", "Avalanche", "Base", "Fantom", "Metis", "Linea", "Kava", "Mantle"],
        "volume_rank": 1
      }
    ],
    "total_matched": 1,
    "query_type": "specific",
    "sort_by": "volume",
    "timestamp": "2024-01-15T12:00:00Z"
  }
}
```

#### Features
- Fuzzy name matching (case-insensitive, partial match)
- Sort by `volume` or `chains_count`
- Filter by chain support
- Volume ranking across all bridges

---

### 2. bridge_risk_scorer.py

Comprehensive risk scoring combining real-time metrics with curated security intelligence.

**API Endpoint:** `https://bridges.llama.fi/bridges?includeChains=true`

#### Input Options

**Score a specific bridge:**
```json
{
  "bridge_name": "stargate"
}
```

**Score top N bridges:**
```json
{
  "top": 5
}
```

#### Output

```json
{
  "success": true,
  "data": {
    "bridge": "Stargate",
    "risk_score": 1.5,
    "risk_level": "SAFE",
    "breakdown": {
      "volume_score": 1.0,
      "chain_coverage_score": 1.5,
      "security_score": 0.0,
      "design_score": 2.0,
      "audit_score": 0.0
    },
    "details": {
      "volume_24h": 15234567.89,
      "chains_count": 12,
      "design_type": "liquidity-pool",
      "exploits": [],
      "audits": ["Quantstamp", "Zokyo"],
      "status": "active"
    },
    "recommendation": "Low risk. Battle-tested with high volume and clean security record.",
    "timestamp": "2024-01-15T12:00:00Z"
  }
}
```

#### Risk Factor Weights

| Factor | Weight | Description |
|--------|--------|-------------|
| Volume | 25% | Higher 24h volume = more battle-tested and liquid |
| Chain Coverage | 15% | More chains = more established, but also more attack surface |
| Security History | 30% | Exploits, hacks, and compromises from curated database |
| Bridge Design | 15% | Architecture safety (liquidity pool vs lock-and-mint) |
| Audit Status | 15% | Reputable audit firms, number of audits |

#### Risk Scoring Scale

| Level | Score | Action |
|-------|-------|--------|
| SAFE | 0-1 | No significant risks detected |
| LOW | 2-3 | Minor concerns, generally safe |
| MEDIUM | 4-5 | Proceed with caution |
| HIGH | 6-7 | Significant risks -- not recommended |
| CRITICAL | 8-10 | Known exploits or compromised -- avoid |

#### Curated Security Database

The risk scorer includes a curated database of bridge security incidents:

| Bridge | Incident | Date | Amount Lost | Status |
|--------|----------|------|-------------|--------|
| Ronin | Validator key compromise | Mar 2022 | $624M | Recovered |
| Wormhole | Smart contract exploit | Feb 2022 | $320M | Recovered |
| Nomad | Verification bypass | Aug 2022 | $190M | Compromised |
| Multichain | Infrastructure exploit | Jul 2023 | $126M | Compromised |
| Harmony Horizon | Validator key compromise | Jun 2022 | $100M | Compromised |
| Celer cBridge | DNS hijack | Aug 2022 | $240K | Active |

#### Bridge Design Types

| Design | Risk Profile | Examples |
|--------|-------------|----------|
| Liquidity Pool | Medium -- funds locked in contracts, AMM risk | Stargate, Hop, Synapse, Connext |
| Optimistic Relay | Low-Medium -- dispute period provides safety | Across |
| Message Passing | Medium -- relies on oracle/relayer network | Wormhole, LayerZero |
| Lock-and-Mint | High -- wrapped assets create systemic risk | Multichain (compromised) |
| Maker Model | Low-Medium -- decentralized market makers | Orbiter |

---

### 3. route_optimizer.py

Find the optimal bridge route between two chains, ranked by your priority.

**API Endpoint:** `https://bridges.llama.fi/bridges?includeChains=true`

#### Input

```json
{
  "source_chain": "ethereum",
  "destination_chain": "arbitrum",
  "priority": "safety"
}
```

**Priority options:**
- `safety` (default) -- prioritize bridges with lowest risk score
- `cost` -- prioritize bridges with highest volume (proxy for better liquidity/lower slippage)
- `speed` -- prioritize bridges with design types known for faster finality

#### Output

```json
{
  "success": true,
  "data": {
    "source_chain": "Ethereum",
    "destination_chain": "Arbitrum",
    "priority": "safety",
    "routes": [
      {
        "rank": 1,
        "bridge": "Across",
        "design_type": "optimistic-relay",
        "volume_24h": 8234567.89,
        "risk_score": 1.2,
        "risk_level": "SAFE",
        "composite_score": 92.5,
        "recommendation": "Top pick for safety -- optimistic design with clean record"
      }
    ],
    "total_routes": 5,
    "timestamp": "2024-01-15T12:00:00Z"
  }
}
```

#### Chain Name Normalization

The route optimizer normalizes user input to DeFiLlama chain names:

| User Input | Normalized Name |
|------------|----------------|
| ethereum, eth, mainnet | Ethereum |
| arbitrum, arb | Arbitrum |
| optimism, op | Optimism |
| polygon, matic | Polygon |
| bsc, bnb, binance | BSC |
| base | Base |
| avalanche, avax | Avalanche |
| solana, sol | Solana |
| fantom, ftm | Fantom |
| gnosis, xdai | Gnosis |
| linea | Linea |
| zksync, zksync era | zkSync Era |
| scroll | Scroll |
| mantle | Mantle |

---

### 4. bridge_monitor.py

Monitor bridge TVL and volume changes, detecting anomalies that could indicate exploits or issues.

**API Endpoint:** `https://bridges.llama.fi/bridges?includeChains=true`

#### Input Options

**Monitor a specific bridge:**
```json
{
  "bridge_name": "stargate"
}
```

**Monitor all bridges with alert threshold:**
```json
{
  "alert_threshold": 20
}
```

The `alert_threshold` is a percentage -- bridges with volume changes exceeding this threshold will be flagged.

#### Output

```json
{
  "success": true,
  "data": {
    "summary": {
      "total_bridges_monitored": 25,
      "anomalies_detected": 2,
      "total_24h_volume": 456789012.34
    },
    "anomalies": [
      {
        "bridge": "ExampleBridge",
        "type": "volume_spike",
        "severity": "WARNING",
        "volume_24h": 50000000,
        "volume_1h": 15000000,
        "volume_ratio": 7.2,
        "message": "Hourly volume is 7.2x the daily average -- possible high demand or drainage event"
      }
    ],
    "bridges": [
      {
        "name": "Stargate",
        "volume_24h": 15234567.89,
        "volume_1h": 634521.12,
        "hourly_ratio": 1.0,
        "status": "normal",
        "security_flag": null
      }
    ],
    "timestamp": "2024-01-15T12:00:00Z"
  }
}
```

#### Anomaly Detection Rules

| Anomaly | Threshold | Severity | Possible Cause |
|---------|-----------|----------|----------------|
| Volume Spike | Hourly > 3x daily average | WARNING | High demand, airdrop farming, or exploit drainage |
| Volume Drop | 24h < 20% of typical | WARNING | Technical issues, loss of confidence, or maintenance |
| Known Exploit | In security database | CRITICAL | Historical exploit -- bridge may be compromised |
| Compromised Status | Status = compromised | CRITICAL | Bridge is no longer safe to use |

---

## Bridge Risk Classification

### By Design Architecture

**Safest to Riskiest:**

1. **Native Bridges** (e.g., Arbitrum/Optimism canonical) -- Secured by L1 validators, but slow (7-day withdrawal for optimistic rollups)
2. **Optimistic Relay** (e.g., Across) -- Fast with dispute-period safety net, UMA oracle
3. **Liquidity Pool** (e.g., Stargate, Hop) -- Capital-efficient, but smart contract risk on multiple chains
4. **Message Passing** (e.g., Wormhole, LayerZero) -- Flexible but relies on oracle/relayer trust assumptions
5. **Lock-and-Mint** (e.g., Multichain) -- Creates wrapped assets with systemic risk; multiple have been exploited

### By Track Record

**Clean Record (No Exploits):**
- Stargate (audited by Quantstamp, Zokyo)
- Across (audited by OpenZeppelin)
- Hop (audited by OpenZeppelin)
- Synapse (audited by Halborn)
- Connext (audited by Consensys Diligence)
- deBridge (audited by Halborn, Neodyme)
- LayerZero (audited by Zellic, Trail of Bits)
- Orbiter

**Recovered from Exploits:**
- Wormhole ($320M, Feb 2022 -- Jump Crypto covered losses)
- Ronin ($624M, Mar 2022 -- Axie Infinity reimbursed users)
- Celer ($240K, Aug 2022 -- minor DNS incident)

**Compromised (Avoid):**
- Multichain ($126M, Jul 2023 -- CEO arrested, funds unrecoverable)
- Nomad ($190M, Aug 2022 -- verification bypass, partial recovery)
- Harmony Horizon ($100M, Jun 2022 -- validator keys compromised)

---

## Security Incident History

Cross-chain bridges have been the single largest attack vector in DeFi. Here is a timeline of major incidents:

| Date | Bridge | Amount Lost | Attack Type | Recovery |
|------|--------|-------------|-------------|----------|
| Jul 2023 | Multichain | $126M | Infrastructure exploit / insider | None -- CEO arrested |
| Mar 2022 | Ronin | $624M | Validator key compromise (social engineering) | Full -- Sky Mavis reimbursed |
| Feb 2022 | Wormhole | $320M | Smart contract exploit (signature verification) | Full -- Jump Crypto covered |
| Aug 2022 | Nomad | $190M | Verification bypass (initialization bug) | Partial -- ~$37M recovered |
| Jun 2022 | Harmony Horizon | $100M | Validator key compromise (2-of-5 multisig) | None |
| Aug 2022 | Celer cBridge | $240K | DNS hijack (front-end attack) | Full |

### Key Takeaways

1. **Validator key management** is critical -- 2-of-5 multisigs are not secure enough
2. **Lock-and-mint** designs create systemic risk when the custodian is compromised
3. **Smart contract bugs** can drain hundreds of millions in minutes
4. **Social engineering** remains effective even against well-funded teams
5. **Recovery** depends entirely on the team's financial backing and willingness

---

## Composability

The Bridge Analyzer can be composed with other SpoonOS skills:

### With DeFi Safety Shield
```
1. Use bridge_comparison to find candidate bridges
2. Use bridge_risk_scorer to evaluate safety
3. Pass bridge contract addresses to DeFi Safety Shield for on-chain verification
```

### With Crypto Market Intelligence
```
1. Monitor bridge volumes for market sentiment (high bridge volume to L2s = bullish L2 activity)
2. Correlate bridge TVL changes with token price movements
3. Track capital flows between chains as a leading indicator
```

### With Smart Contract Auditor
```
1. Identify bridge contracts from DeFiLlama data
2. Audit bridge smart contracts for vulnerabilities
3. Verify bridge contract source code and admin functions
```

---

## Use Cases

### 1. Choosing a Bridge for a Large Transfer
You have $100K in ETH on Ethereum and need to move it to Arbitrum. Run bridge_comparison to see which bridges support this route, then bridge_risk_scorer to evaluate the safest options, and route_optimizer to get a ranked recommendation.

### 2. Monitoring Bridge Health After Bridging
After bridging assets, use bridge_monitor to track the bridge's volume and TVL for anomalies. A sudden drop in TVL or volume spike could indicate an exploit in progress.

### 3. Due Diligence on a New Bridge
A new DeFi protocol requires using a bridge you have never used before. Run bridge_risk_scorer to check its security history, audit status, and design type before committing funds.

### 4. Comparing Bridge Ecosystems for a Chain
You are deploying a dApp on a new L2 and need to understand which bridges serve it. Use bridge_comparison with a chain filter to see all bridges supporting that network.

### 5. Detecting Bridge Exploits Early
Set up periodic monitoring with bridge_monitor to watch for volume anomalies across all major bridges. A volume spike of 200%+ in an hour could indicate an active exploit.

### 6. Research for Cross-Chain Protocol Design
You are building a cross-chain application and need to choose which bridge infrastructure to integrate. Use bridge_comparison and bridge_risk_scorer to evaluate protocols by volume, design type, chain coverage, and security record.

### 7. Capital Flow Analysis
Track which chains are receiving the most bridge volume to identify emerging ecosystems. High inbound bridge volume to a chain often precedes ecosystem growth and token appreciation.

---

## Technical Details

### Dependencies
- Python 3.8+
- Standard library only (`urllib`, `json`, `sys`, `time`)
- No external packages required

### API Rate Limits
DeFiLlama APIs are free with generous rate limits. The scripts include retry logic with exponential backoff for 429 (rate limit) responses.

### Data Freshness
- Bridge volume data updates approximately every hour
- Chain support data updates daily
- Security database is curated and included in the script

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| *(none)* | -- | **No environment variables or API keys needed** |

---

## License

MIT License. Built for the SpoonOS ecosystem.
