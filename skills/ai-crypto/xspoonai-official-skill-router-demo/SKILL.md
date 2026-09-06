---
name: skill-router-demo
track: platform-challenge
version: 0.1.0
summary: Route prompt to best candidate skills
---

## Description

Route a prompt to the best candidate skills using rules-based matching. Analyzes queries to recommend relevant skills.

## Inputs

```json
{
  "prompt": "User query or request",
  "top_k": 5
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "matched_skills": [],
    "best_match": "skill-name"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Route Prompt
```bash
echo '{"prompt":"Monitor contract events","top_k":3}' | python3 scripts/main.py
```

## Examples

### Example 1: Find Relevant Skills
```bash
$ echo '{"prompt":"I need to monitor smart contract events","top_k":3}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "matched_skills": [{"name": "contract-event-tail", "score": 0.95}],
    "best_match": "contract-event-tail"
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
    "prompt": "Prompt is required"
  }
}
```
