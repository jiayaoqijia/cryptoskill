---
name: governance-vote-tracker
track: web3-data-intelligence
version: 0.2.0
summary: Real DAO vote analysis with Snapshot API integration
---

## Description

Analyze DAO governance votes with real data from Snapshot GraphQL API or custom parameters. Provides voting power distribution, quorum verification, and automated proposal outcome prediction. Supports Aave, Uniswap, Compound, MakerDAO, Curve, and Balancer.

## Inputs (API Mode)

```json
{
  "use_api": true,
  "dao": "aave",
  "proposal_id": "123"
}
```

## Inputs (Parameter Mode)

```json
{
  "dao": "aave",
  "votes_for": 8000000,
  "votes_against": 2000000,
  "quorum": 5000000,
  "votes_abstain": 500000
}
```

## Outputs (API Mode)

```json
{
  "ok": true,
  "data": {
    "source": "snapshot_api",
    "dao": "aave",
    "proposal_id": "Qm...",
    "proposal_title": "Example Proposal",
    "proposal_state": "closed",
    "votes_for": 8000000.5,
    "votes_against": 2000000.25,
    "quorum_reached": true,
    "for_percentage": 80.0,
    "predicted_outcome": "passes",
    "recommendation": "✅ PASSES: 80.0% support",
    "check_timestamp": "2026-02-07T08:30:00Z"
  }
}
```

## Usage

### Fetch from Snapshot API
```bash
python scripts/main.py --params '{"use_api":true,"dao":"aave","proposal_id":"123"}'
```

### Analyze Custom Data
```bash
python scripts/main.py --params '{"dao":"aave","votes_for":8000000,"votes_against":2000000,"quorum":5000000}'
```

## Examples

### Example 1: Real Aave Proposal (API)
```bash
$ python scripts/main.py --params '{"use_api":true,"dao":"aave","proposal_id":"123"}'
{
  "ok": true,
  "data": {
    "source": "snapshot_api",
    "dao": "aave",
    "proposal_title": "Enable Flash Loans on Aave v3",
    "proposal_state": "closed",
    "votes_for": 8500000.0,
    "votes_against": 1500000.0,
    "quorum_reached": true,
    "for_percentage": 85.0,
    "predicted_outcome": "passes",
    "recommendation": "✅ PASSES: 85.0% support"
  }
}
```

### Example 2: Custom Parameter Analysis (Uniswap)
```bash
$ python scripts/main.py --params '{"dao":"uniswap","votes_for":5000000,"votes_against":1000000,"quorum":4000000}'
{
  "ok": true,
  "data": {
    "source": "parameters",
    "dao": "uniswap",
    "votes_for": 5000000,
    "votes_against": 1000000,
    "quorum_reached": true,
    "for_percentage": 83.33,
    "predicted_outcome": "passes",
    "recommendation": "✅ PASSES: 83.33% support"
  }
}
```

### Example 3: Failing Compound Proposal
```bash
$ python scripts/main.py --params '{"dao":"compound","votes_for":2000000,"votes_against":3000000,"quorum":4000000}'
{
  "ok": true,
  "data": {
    "source": "parameters",
    "dao": "compound",
    "votes_for": 2000000,
    "votes_against": 3000000,
    "quorum_reached": true,
    "for_percentage": 40.0,
    "predicted_outcome": "fails",
    "recommendation": "❌ FAILS: 40.0% support"
  }
}
```

## Supported DAOs

- **aave** → aave.eth (4% quorum)
- **uniswap** → uniswap (4% quorum)
- **compound** → compound (4% quorum)
- **makerdao** → makerdao (40% quorum)
- **curve** → snapshot.curve.eth
- **balancer** → balancer

## Error Handling

When an error occurs:

```json
{
  "ok": false,
  "error": "Error description",
  "details": "Additional context"
}
```
