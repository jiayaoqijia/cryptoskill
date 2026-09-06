---
name: skill-coverage-map
track: platform-challenge
version: 0.1.0
summary: Map skill coverage against track goals
---

## Description

Map skills coverage versus track goals. Analyzes which categories have sufficient skill implementations and identifies gaps.

## Inputs

```json
{
  "track": "web3-core-operations|enterprise-skills",
  "goals": ["List of category goals"]
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "coverage": "45%",
    "gaps": ["Missing category"]
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Check Coverage
```bash
echo '{"track":"web3-core-operations"}' | python3 scripts/main.py
```

## Examples

### Example 1: Coverage Analysis
```bash
$ echo '{"track":"web3-core-operations","goals":["DeFi","NFT","Bridge"]}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "coverage": "67%",
    "gaps": ["Security"]
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": {
    "track": "Unknown track"
  }
}
```
