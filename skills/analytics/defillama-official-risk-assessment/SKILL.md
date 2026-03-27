---
name: risk-assessment
description: >
  Protocol and DeFi risk evaluation covering hack history, oracle dependencies,
  treasury health, TVL concentration, and yield sustainability. Use when the
  user asks "is X safe", "how risky is", protocol security, risk analysis, or
  wants to evaluate risk before investing or depositing funds.
---

# Risk Assessment

Evaluate the risk profile of a DeFi protocol by examining its security
history, oracle dependencies, treasury, fundamentals, and yield levels.

## Workflow

### Step 1 - Resolve the protocol entity

```
defillama:resolve_entity
  entity_type: "protocol"
  name: "<user-provided name>"
```

### Step 2 - Hack history

Check whether the protocol has been exploited before.

```
defillama:get_events
  protocol: "<slug>"
  event_type: "hacks"
```

Any past hacks are a significant risk signal. Note the date, amount lost,
and whether funds were recovered.

### Step 3 - Oracle dependencies

Identify which oracle the protocol relies on and how much value it secures.

```
defillama:get_oracle_metrics
```

Filter results for the protocol's oracle. Oracle metrics automatically
filter to `tvl_component = 'base'` and aggregate with SUM/GROUP BY to
exclude double-counted TVL. A protocol using a small or unproven oracle
has higher risk than one using Chainlink or Pyth.

### Step 4 - Treasury health

Assess the protocol's financial reserves.

```
defillama:get_treasury
  treasury: "<slug>"
```

A healthy treasury provides a safety net for bug bounties, insurance,
and continued development.

### Step 5 - Protocol fundamentals

Check TVL, revenue, and trends to evaluate sustainability.

```
defillama:get_protocol_metrics
  protocol: "<slug>"
```

Key signals: Is TVL growing or declining? Is the protocol generating
real revenue?

### Step 6 - Yield analysis

Examine pool APYs for sustainability red flags.

```
defillama:get_yield_pools
  protocol: "<slug>"
```

## Risk Signals

Evaluate each factor and assign a risk level:

| Signal | Risk Level | Explanation |
|--------|-----------|-------------|
| Recent hack (< 1 year) | HIGH | Protocol was recently exploited |
| Past hack (> 1 year), no recurrence | MODERATE | Was exploited but has since hardened |
| No hack history | LOW | No known exploits |
| No oracle or small oracle TVS | MODERATE | Oracle risk, potential manipulation |
| Uses Chainlink/Pyth with high TVS | LOW | Battle-tested oracle infrastructure |
| Treasury < $1M | HIGH | No meaningful safety net |
| Treasury > $10M | LOW | Strong financial reserves |
| APY > 100% from rewards only | HIGH | Likely unsustainable, token emissions |
| APY from real yield (fees) | LOW | Sustainable yield source |
| TVL declining > 20% in 30d | MODERATE | Users are leaving |
| Revenue declining with TVL | HIGH | Fundamentals deteriorating |

## Output Format

Present the report with these sections:

1. **Risk Summary** - Overall risk rating (LOW / MODERATE / HIGH) with
   a one-sentence justification.
2. **Security History** - Hack incidents, amounts, and outcomes.
3. **Oracle Risk** - Which oracle is used, TVS secured, reliability.
4. **Treasury Health** - Total treasury value, composition, runway.
5. **Fundamental Health** - TVL trend, revenue, user activity direction.
6. **Yield Sustainability** - Are yields from real fees or emissions?
7. **Risk Factors** - Bullet list of all identified risk signals with
   their severity level.

## Tips

- No data from `get_events` for hacks is a positive signal, not missing data.
- A protocol with high TVL but zero revenue may be subsidizing usage
  with token emissions - flag this.
- Compare treasury value to TVL: treasury < 1% of TVL means limited
  ability to cover losses.
- Multiple past hacks on the same protocol is a stronger negative signal
  than a single incident.
