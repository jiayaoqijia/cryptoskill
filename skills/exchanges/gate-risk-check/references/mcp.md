---
name: gate-info-riskcheck-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for token/address risk checking in Gate-Info domain, including degraded address-risk handling and structured reporting."
---

# Gate Info RiskCheck MCP Specification

> Authoritative MCP execution document for `gate-info-riskcheck`.

## 1. Scope and Trigger Boundaries

In scope:
- Token/contract security checks
- Address safety checks (degraded mode currently)

Out of scope / route elsewhere:
- Multi-dimension research (fundamental + technical + news + risk) -> `gate-info-research`
- Address flow tracing -> `gate-info-addresstracker`
- General coin analysis without security focus -> `gate-info-coinanalysis`

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate-Info MCP is available.
2. Probe with read tool (`info_coin_get_coin_info` or `info_compliance_check_token_security`).

Fallback:
- MCP unavailable: show setup guidance and return no-fabrication notice.
- Address-risk tool unavailable: use degraded mode with `info_onchain_get_address_info` only.

## 3. Authentication

- API key not required for this skill.
- If service-level auth errors occur, return transparent error and stop execution.

## 4. MCP Resources

No MCP Resources required.

## 5. Tool Calling Specification

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `info_compliance_check_token_security` | `token` or `address`, `chain` | risk level, risk items, tax, holder concentration, honeypot, open-source flags | unsupported chain/token |
| `info_coin_get_coin_info` | symbol/query | project metadata, market context | ambiguous symbol |
| `info_onchain_get_address_info` | `address`, `chain` | basic address state, balances, tx count | address invalid |
| `info_compliance_check_address_risk` | address payload (when available) | compliance risk labels | currently degraded/unavailable |

## 6. Execution SOP (Non-Skippable)

### 6.1 Intent gate
1. If request includes non-risk analysis dimensions, route to `gate-info-research`.
2. If request is strictly security-focused, continue.

### 6.2 Token security mode
1. Normalize input (`token` or `address`) and require `chain`.
2. Run in parallel:
   - `info_compliance_check_token_security`
   - `info_coin_get_coin_info`
3. Aggregate into standardized risk report.
4. Highlight high-risk items first.

### 6.3 Address risk degraded mode
1. Call `info_onchain_get_address_info` for baseline context.
2. If `info_compliance_check_address_risk` unavailable, clearly disclose degradation.
3. Provide safe next actions (manual verification + alternate checks).

## 7. Output Templates

```markdown
## Token Security Report
- Input: {token_or_address} on {chain}
- Overall Risk: {risk_level}
- High-Risk Count: {high_count}
- Honeypot: {yes_or_no}
- Tax Risk: {tax_summary}
- Holder Concentration: {holder_summary}
- Recommendation: {actionable_next_step}
```

```markdown
## Address Safety (Degraded)
- Address: {address}
- Chain: {chain}
- Basic State: {summary_from_onchain_info}
- Compliance Risk Label: {not_available_or_value}
- Note: Address compliance risk engine is currently degraded.
```

## 8. Safety and Degradation Rules

1. Never present a token/address as absolutely safe; use risk levels with evidence.
2. If a required field (`chain`) is missing, block execution and request completion.
3. Clearly separate observed facts from model inference.
4. In degraded mode, explicitly state unavailable checks and avoid false confidence.
5. Preserve critical warnings (honeypot/high tax/high concentration) at top of report.
