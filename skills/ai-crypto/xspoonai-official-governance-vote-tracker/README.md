# governance-vote-tracker

Track DAO governance votes with real Snapshot API integration for live voting data. Supports both parameter-based analysis and direct API data fetching.

## Overview

This skill analyzes DAO governance votes with real-time data from Snapshot GraphQL API or custom parameters. Provides voting power distribution, quorum verification, and automated outcome prediction with support for major DAOs.

## Features

- ✅ **Snapshot GraphQL API Integration**: Fetch real live voting data from Snapshot Hub
- ✅ Real voting power analysis with dual-mode operation (API + parameter modes)
- ✅ Support for 6 major DAOs (Aave, Uniswap, Compound, MakerDAO, Curve, Balancer)
- ✅ Quorum reached verification with DAO-specific thresholds
- ✅ Vote percentage calculation (For/Against/Abstain)
- ✅ Proposal outcome prediction with winning margins
- ✅ Voting power distribution analysis
- ✅ Real-time proposal state tracking (active/closed/canceled)

## Usage

### Fetch Real Data from Snapshot API
```bash
python scripts/main.py --params '{"use_api":true,"dao":"aave","proposal_id":"123"}'
```

Returns live proposal data including voting state, voter counts, and real voting power distributions from Snapshot Hub.

### Analyze Custom Vote Data
```bash
python scripts/main.py --params '{"dao":"aave","votes_for":8000000,"votes_against":2000000,"quorum":5000000}'
```

### With Abstentions
```bash
python scripts/main.py --params '{"dao":"compound","votes_for":50000,"votes_against":15000,"votes_abstain":5000,"quorum":40000}'
```

## API Integration

The skill uses **Snapshot GraphQL API** (`hub.snapshot.org/graphql`) for real voting data:

- Fetches live proposal details: title, state, vote counts, voting power
- Supports proposals from Snapshot spaces for all major DAOs
- Returns source indicator: `snapshot_api` (live) or `parameters` (custom)
- Includes proposal state: active, closed, or canceled

## Parameters

### API Mode
- `use_api` (boolean, required): Set to true to fetch from Snapshot
- `dao` (string, required): DAO name (aave, uniswap, compound, makerdao, curve, balancer)
- `proposal_id` (string, required): Snapshot proposal ID

### Parameter Mode
- `dao` (string, required): DAO name
- `votes_for` (number, required): Total votes in favor
- `votes_against` (number, required): Total votes opposed
- `votes_abstain` (number, optional): Votes abstaining (default: 0)
- `quorum` (number, optional): Quorum requirement
- `top_voters` (array, optional): List of voters with votes and direction

## Output

Returns JSON with:
- `source`: Data source (snapshot_api or parameters)
- `votes_for/against/abstain`: Vote counts or percentages
- `quorum_reached`: Boolean quorum status  
- `quorum_percentage`: Quorum fulfillment percentage
- `for_percentage`: Percentage voting in favor
- `support_percentage`: Support excluding abstentions
- `predicted_outcome`: passes/fails/pending
- `winning_margin`: Margin above/below pass threshold
- `proposal_state`: Current state (active/closed/canceled)
- `recommendation`: Actionable guidance

## Examples

### Real Aave Proposal via Snapshot API
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
    "predicted_outcome": "passes"
  }
}
```

### Aave Proposal Passing with Custom Data
```bash
python scripts/main.py --params '{"dao":"aave","votes_for":8000000,"votes_against":2000000,"quorum":5000000}'
```

### Uniswap Proposal Failing
```bash
python scripts/main.py --params '{"dao":"uniswap","votes_for":2000000,"votes_against":3000000,"quorum":4000000}'
```

### Compound Without Quorum
```bash
python scripts/main.py --params '{"dao":"compound","votes_for":20000,"votes_against":10000,"quorum":40000}'
```

## Supported DAOs

- **Aave** (aave.eth): 4% quorum, 50% pass threshold
- **Uniswap** (uniswap): 4% quorum, 50% pass threshold
- **Compound** (compound): 4% quorum, 50% pass threshold
- **MakerDAO** (makerdao): 40% quorum, 50% pass threshold
- **Curve** (snapshot.curve.eth): Standard thresholds
- **Balancer** (balancer): Standard thresholds

## Track

web3-data-intelligence
