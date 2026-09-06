# DAO Governance Intelligence

**Comprehensive DAO governance analytics for 20,000+ Snapshot spaces — scan proposals, analyze voting patterns, profile delegates, and measure DAO health. Zero configuration, no API keys required.**

---

## Why Governance Intelligence?

| Feature | Snapshot UI | Tally | Manual Research | **Governance Intel** |
|---------|-------------|-------|-----------------|----------------------|
| Active proposal scanning | Single space | Limited DAOs | Time-consuming | **Multi-DAO scanning** |
| Whale voting analysis | Not available | Basic | Spreadsheet work | **Automated detection** |
| Delegate profiling | View-only | Basic profiles | Manual tracking | **Cross-DAO profiles** |
| DAO health scoring | Not available | Not available | Subjective | **Quantified 0-100 score** |
| Voting concentration | Not shown | Not shown | Manual calc | **Gini coefficient** |
| Quorum tracking | Per-proposal | Per-proposal | Manual | **Aggregate rates** |
| Cross-DAO comparison | Not available | Limited | Very difficult | **Side-by-side comparison** |
| API key required | No (UI only) | Yes | N/A | **No** |
| Programmatic access | GraphQL | REST API | N/A | **JSON stdin/stdout** |
| Integration ready | No | Limited | No | **SpoonOS composable** |

---

## Quick Start

### Scan Active Proposals

```bash
echo '{"space_id": "aave.eth", "state": "active"}' | python3 scripts/proposal_scanner.py
```

### Scan Top DAOs

```bash
echo '{"top_daos": true}' | python3 scripts/proposal_scanner.py
```

### Analyze Voting on a Proposal

```bash
echo '{"space_id": "aave.eth", "proposal_index": 0}' | python3 scripts/voting_analyzer.py
```

### Profile a Delegate

```bash
echo '{"voter_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "space_id": "ens.eth"}' | python3 scripts/delegate_profiler.py
```

### DAO Health Check

```bash
echo '{"space_id": "aave.eth"}' | python3 scripts/dao_health.py
```

### Compare DAOs

```bash
echo '{"compare": ["aave.eth", "uniswapgovernance.eth", "ens.eth"]}' | python3 scripts/dao_health.py
```

---

## Scripts

### 1. Proposal Scanner (`proposal_scanner.py`)

Scans active and recent governance proposals across one or multiple DAOs using the Snapshot GraphQL API.

#### Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `space_id` | string | No | Snapshot space ID (e.g., `aave.eth`) |
| `top_daos` | boolean | No | Scan all major DAOs (12 top spaces) |
| `state` | string | No | Filter by proposal state: `active`, `closed`, `pending` |
| `limit` | integer | No | Max proposals per space (default: 10) |

#### Output

```json
{
  "status": "success",
  "space": "aave.eth",
  "proposals": [
    {
      "id": "0xabc...",
      "title": "AIP-42: Risk Parameter Updates",
      "state": "active",
      "author": "0x1234...abcd",
      "start": "2025-01-15T00:00:00Z",
      "end": "2025-01-20T00:00:00Z",
      "votes": 342,
      "scores_total": 1250000.5,
      "choices": ["For", "Against", "Abstain"],
      "scores": [980000.0, 200000.5, 70000.0],
      "quorum": 320000,
      "quorum_reached": true,
      "leading_choice": "For",
      "leading_pct": 78.4,
      "time_remaining": "2d 5h"
    }
  ],
  "summary": {
    "total": 5,
    "active": 2,
    "closed": 3,
    "pending": 0
  }
}
```

#### Modes

- **Single space**: Pass `space_id` to scan one DAO's proposals.
- **Top DAOs**: Pass `top_daos: true` to scan 12 major DAOs simultaneously.
- **State filter**: Combine with `state` to focus on active, closed, or pending proposals.

---

### 2. Voting Analyzer (`voting_analyzer.py`)

Analyzes voting patterns for a specific proposal, including whale influence, vote distribution, and concentration metrics.

#### Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `proposal_id` | string | No | Direct Snapshot proposal ID |
| `space_id` | string | No | Space ID (used with `proposal_index`) |
| `proposal_index` | integer | No | 0-based index of recent proposals (0 = most recent) |

Either provide `proposal_id` directly, or use `space_id` + `proposal_index` to auto-resolve.

#### Output

```json
{
  "status": "success",
  "proposal": {
    "id": "0xabc...",
    "title": "AIP-42: Risk Parameter Updates",
    "space": "aave.eth",
    "state": "active",
    "choices": ["For", "Against", "Abstain"]
  },
  "vote_distribution": {
    "For": { "votes": 280, "vp": 980000.0, "pct": 78.4 },
    "Against": { "votes": 45, "vp": 200000.5, "pct": 16.0 },
    "Abstain": { "votes": 17, "vp": 70000.0, "pct": 5.6 }
  },
  "whale_analysis": {
    "top_10_share_pct": 62.3,
    "whale_dominant": true,
    "top_voters": [
      { "voter": "0x1234...abcd", "vp": 150000.0, "choice": "For", "pct_of_total": 12.0 }
    ]
  },
  "participation": {
    "total_voters": 342,
    "total_vp": 1250000.5
  },
  "concentration": {
    "gini_coefficient": 0.82,
    "top_10_pct": 62.3,
    "top_25_pct": 78.1
  },
  "timing": {
    "early_voters_pct": 45.2,
    "late_voters_pct": 54.8,
    "early_vp_pct": 38.0,
    "late_vp_pct": 62.0
  }
}
```

#### Key Metrics

- **Whale Dominance**: Flagged when top-10 voters control more than 50% of voting power.
- **Gini Coefficient**: 0 = perfect equality, 1 = one voter holds all power.
- **Early vs Late Voting**: Detects whether whales vote early (signaling) or late (sniping).

---

### 3. Delegate Profiler (`delegate_profiler.py`)

Profiles a delegate or voter's governance participation across one or multiple DAOs.

#### Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `voter_address` | string | Yes | Ethereum address (0x...) |
| `space_id` | string | No | Specific Snapshot space to analyze |
| `top_daos` | boolean | No | Profile across all major DAOs |
| `limit` | integer | No | Max votes to fetch (default: 100) |

#### Output

```json
{
  "status": "success",
  "voter": "0x1234...abcd",
  "space": "aave.eth",
  "summary": {
    "total_votes": 47,
    "unique_spaces": 1,
    "avg_voting_power": 125000.5,
    "total_voting_power_used": 5875023.5
  },
  "participation": {
    "proposals_voted": 47,
    "proposals_available": 55,
    "participation_rate": 0.85
  },
  "choice_distribution": {
    "For": 35,
    "Against": 8,
    "Abstain": 4
  },
  "alignment": {
    "aligned_with_outcome": 43,
    "total_decided": 47,
    "alignment_rate": 0.91
  },
  "recent_votes": [
    {
      "proposal": "AIP-42: Risk Parameter Updates",
      "space": "aave.eth",
      "choice": "For",
      "vp": 125000.0,
      "date": "2025-01-15"
    }
  ]
}
```

#### Modes

- **Single space**: Detailed participation analysis within one DAO.
- **Cross-DAO**: Set `top_daos: true` to see governance activity across 12 major DAOs.

---

### 4. DAO Health (`dao_health.py`)

Calculates comprehensive DAO health metrics with a 0-100 health score.

#### Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `space_id` | string | No | Single DAO to analyze |
| `compare` | array | No | List of space IDs for comparison |

#### Output

```json
{
  "status": "success",
  "space": "aave.eth",
  "space_name": "Aave",
  "health_score": 78,
  "rating": "HEALTHY",
  "breakdown": {
    "activity": { "score": 82, "proposals_per_month": 4.2, "total_proposals": 55 },
    "participation": { "score": 71, "avg_voters": 312, "members": 12500 },
    "decentralization": { "score": 65, "top_10_concentration": 58.3 },
    "quorum_achievement": { "score": 88, "quorum_rate": 0.88 },
    "proposal_success": { "score": 84, "success_rate": 0.84 }
  },
  "metadata": {
    "followers": 45000,
    "strategies_count": 3,
    "voting_delay": 86400,
    "voting_period": 432000
  }
}
```

#### Health Score Ratings

| Score Range | Rating | Interpretation |
|-------------|--------|----------------|
| 80-100 | EXCELLENT | Highly active, decentralized, strong participation |
| 60-79 | HEALTHY | Good governance with room for improvement |
| 40-59 | MODERATE | Some governance concerns, needs attention |
| 20-39 | WEAK | Low participation or high concentration |
| 0-19 | CRITICAL | Governance is largely inactive or centralized |

#### Health Metric Weights

| Metric | Weight | What It Measures |
|--------|--------|------------------|
| Activity | 20% | Proposals created per month (last 3 months) |
| Participation | 25% | Average voter turnout relative to member count |
| Decentralization | 25% | Inverse of top-10 voter voting power concentration |
| Quorum Achievement | 15% | Percentage of proposals that reached quorum |
| Proposal Success | 15% | Percentage of proposals that passed |

#### Comparison Mode

Pass `compare` with multiple space IDs to generate a side-by-side comparison table:

```bash
echo '{"compare": ["aave.eth", "uniswapgovernance.eth", "ens.eth"]}' | python3 scripts/dao_health.py
```

---

## Composability

This skill is fully composable with other SpoonOS skills:

| Combination | Use Case |
|-------------|----------|
| Governance Intel + DeFi Safety Shield | Check if a DAO-governed protocol is safe before investing |
| Governance Intel + Market Intelligence | Correlate governance decisions with token price movements |
| Governance Intel + Smart Contract Auditor | Audit contracts that governance proposals aim to deploy |

### Chaining Example

```bash
# Step 1: Scan for active proposals
PROPOSALS=$(echo '{"space_id": "aave.eth", "state": "active"}' | python3 proposal_scanner.py)

# Step 2: Analyze the top proposal's voting
PROPOSAL_ID=$(echo "$PROPOSALS" | python3 -c "import json,sys; print(json.load(sys.stdin)['proposals'][0]['id'])")
echo "{\"proposal_id\": \"$PROPOSAL_ID\"}" | python3 voting_analyzer.py
```

---

## Use Cases

### 1. Governance Researcher
Monitor active proposals across top DAOs, identify controversial votes, and track governance trends over time.

### 2. DAO Delegate
Profile your own voting history, check participation rates, and ensure you are meeting your delegation responsibilities.

### 3. Protocol Investor
Assess DAO health before investing in governance tokens. Compare DAOs to find the most decentralized and active communities.

### 4. Governance Attacker Detection
Detect potential governance attacks by monitoring whale concentration, unusual voting patterns, and last-minute vote swings.

### 5. DAO Operator
Benchmark your DAO against competitors. Identify areas for improvement in participation, decentralization, or proposal activity.

### 6. Academic Researcher
Study decentralized governance dynamics, voting behavior, and the effectiveness of different governance frameworks.

### 7. Community Member
Stay informed about governance decisions that affect protocols you use. Know when important votes are happening and who is influencing outcomes.

---

## Top DAOs Supported

The `top_daos` scanning mode covers these 12 major governance spaces:

| Space ID | DAO | Category | Est. Members |
|----------|-----|----------|-------------|
| `aave.eth` | Aave | DeFi Lending | 12,000+ |
| `uniswapgovernance.eth` | Uniswap | DEX | 10,000+ |
| `ens.eth` | ENS | Infrastructure | 30,000+ |
| `gitcoindao.eth` | Gitcoin | Public Goods | 8,000+ |
| `safe.eth` | Safe (Gnosis Safe) | Multisig Wallet | 5,000+ |
| `arbitrumfoundation.eth` | Arbitrum | Layer 2 | 50,000+ |
| `opcollective.eth` | Optimism | Layer 2 | 20,000+ |
| `lido-snapshot.eth` | Lido | Liquid Staking | 6,000+ |
| `balancer.eth` | Balancer | DEX | 4,000+ |
| `curve.eth` | Curve Finance | DEX | 3,000+ |
| `sushigov.eth` | SushiSwap | DEX | 5,000+ |
| `compound-governance.eth` | Compound | DeFi Lending | 3,000+ |

Any Snapshot space can be queried by passing its `space_id` directly.

---

## Technical Details

### API

All data is sourced from the **Snapshot GraphQL API** at `https://hub.snapshot.org/graphql`. This API is:

- Completely free and public
- No API key required
- No rate limit for reasonable usage
- Covers 20,000+ governance spaces

### Dependencies

- Python 3.8+
- Standard library only (`json`, `sys`, `urllib`, `time`, `math`)
- No external packages required

### Error Handling

All scripts return structured error responses:

```json
{
  "status": "error",
  "error": "Description of what went wrong",
  "details": "Additional context or suggestions"
}
```

Common error scenarios:
- Invalid space ID: Returns suggestion to check the space ID on Snapshot
- Network timeout: Automatic retry with exponential backoff (up to 3 attempts)
- Empty results: Returns empty arrays with a descriptive message
- Invalid address format: Returns validation error with expected format

---

## License

MIT License. Free to use, modify, and distribute.
