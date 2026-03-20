# Gate Exchange Assets

## Overview

A read-only skill for Gate Exchange asset and balance queries. Covers total balance, spot holdings, account valuation, and account book.

### Core Capabilities

- Total account balance across all wallets (spot, margin, futures)
- Spot account balances and holdings by currency
- Account valuation in USDT terms
- Account book and ledger flow

### Read-Only Guarantee

This skill performs **no trading, transfers, or order placement**. All operations are query-only. For trading, use `gate-exchange-spot` or `gate-exchange-futures`.

## Architecture

```
gate-exchange-assets/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Usage Examples

```
"How much is my account worth?"
"Check my USDT balance."
"Show my total assets."
"What's my BTC balance?"
"Show recent BTC account book and current balance."
```

## Trigger Phrases

- check balance / total assets / account value
- how much do I have / account worth
- ledger / account book / balance summary

## Prerequisites

- Gate MCP configured and connected
- Authentication (OAuth) for balance and history queries
