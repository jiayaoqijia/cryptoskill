<!--
  Imported from: https://github.com/saksham10arora-dotcom/quant-skills
  Source Path: skills/data-quality-audit/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: data-quality-audit
description: Systematically audit a dataset before modeling: nulls, leakage, duplicates, dtype lies, target contamination. Use when the user loads a new dataset, mentions cleaning data, or before any ML/analysis task on unfamiliar data.
---

# Data Quality Audit

Run this audit BEFORE any modeling conversation gets serious. Work through the phases; report findings as a table at the end.

## Phase 1: Shape and identity

- Rows x columns; do they match the user's expectation?
- Primary key exists? Duplicated keys?
- Date ranges: gaps, duplicates, future dates
- Grain check: is each row really one entity-time unit? Aggregate and count to verify

## Phase 2: Dtype lies

Print `dtypes` and challenge them:
- Numeric columns loaded as object (commas, currency symbols, whitespace)
- IDs and zip codes as integers (leading zeros destroyed)
- Dates as strings with mixed formats in one column
- Booleans as 0/1/2

Fix dtype issues before computing anything else; null-rate statistics lie otherwise.

## Phase 3: Missingness forensics

For every column with any nulls:
- Null rate
- Is missingness correlated with the target? (compute it; if yes, the missingness IS signal)
- Structured missing vs random: sort by another column and look for runs

Never silently drop or impute without reporting which rows/columns were affected.

## Phase 4: Leakage scan

The highest-value phase:
- Any column that could not be known at prediction time? Flag it
- Aggregates computed over periods overlapping the label window?
- Target-derived features disguised (ratios containing the outcome)?
- Post-outcome statuses (charge-offs, cancellations) present as features?

## Phase 5: Distribution shocks

- Train/test drift on numeric features (report top 5 by KS-statistic)
- Categorical cardinality explosions between splits
- Constant or near-constant columns
- Extreme outliers: count beyond 5 sigma per column; ask if they are errors before winsorizing

## Report format

```
AUDIT: <dataset name>
Rows: N | Cols: M | Memory: X
BLOCKERS: [issues that invalidate modeling until fixed]
WARNINGS: [issues that bias results]
OK: [what was checked and passed]
```
