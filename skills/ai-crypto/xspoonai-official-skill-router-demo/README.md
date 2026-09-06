# skill-router-demo (Track: platform-challenge)

Route and execute skill demonstrations with orchestration

## Overview

This skill provides routing and orchestration for executing skill demonstrations. It maps skill names to execution paths, handles demonstrations with different parameter sets, and coordinates skill execution flows.

## Features

- **Skill Routing**: Map skill identifiers to execution paths in repository
- **Demonstration Execution**: Run pre-configured skill demonstrations
- **Parameter Mapping**: Route parameters to correct skill handlers
- **Error Handling**: Graceful error handling for missing or failed demonstrations
- **Execution Tracking**: Track which demonstrations have been run
- **Multi-Skill Orchestration**: Execute demonstrations across multiple skills
- **Output Aggregation**: Combine results from multiple skill executions

## Usage

Route and execute skill demonstrations:

```bash
# Run demo for all configured skills
python3 scripts/main.py --demo

# Route to specific skill
python3 scripts/main.py --params '{"skill": "api-webhook-signer"}'

# Execute with custom routing
python3 scripts/main.py --params '{"route": "/skill-path", "action": "demo"}'
```

## Use Cases

- Showcase skill functionality to users
- Automated demonstration execution
- API gateway for skill demos
- Interactive skill exploration
- Batch demonstration execution

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skill | string | No | Skill name to demonstrate |
| route | string | No | Path to skill for execution |
| action | string | No | Action to perform (demo, validate, execute) |

## Example Output

Routing executed for 5 sample skills with successful demonstrations. Mapped routes: api-webhook-signer → ai-productivity, security-deps-audit → enterprise-skills, skill-ci-checklist → platform-challenge, whale-tracker → web3-data-intelligence. Execution status: 5 successful, 0 failed.
