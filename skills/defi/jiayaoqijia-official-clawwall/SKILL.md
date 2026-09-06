---
name: clawwall
version: 0.2.1
description: "Outbound DLP for OpenClaw — hard regex blocks secrets & PII from leaving the machine. Domain control, no LLM."
author: Stanxy
openclaw:
  requires:
    bins:
      - python3
      - pip
      - git
      - node
      - npm
    envs: []
---

# ClawWall — Outbound DLP for OpenClaw

**GitHub:** https://github.com/Stanxy/clawguard
**Release:** https://github.com/Stanxy/clawguard/releases/tag/v0.2.1
**PyPI:** https://pypi.org/project/clawwall

ClawWall sits between your AI agent and the outside world. Every outbound tool call is intercepted and scanned against 60+ hard-coded patterns before anything leaves the machine. If content matches — it is blocked or redacted. No LLM, no approximation: regex and entropy only.

## Trust & Permissions

**Be aware of what this installs:**
- A **local Python service** (port 8642) that receives every outbound tool call for scanning
- An **OpenClaw plugin** that hooks `before_tool_call` — all outbound content passes through it
- A **local SQLite database** that stores scan findings metadata

**What the database stores:** finding type, severity, position offsets, action taken, and duration. It never stores raw content, secrets, or PII values.

**What it does NOT do:** no telemetry, no external connections, no data leaves the machine. The service is fully local.

Plugin registration is **manual** — nothing is auto-installed into OpenClaw. You must explicitly add the plugin to your config (see below).

## Installation

### Prerequisites

- Python 3.10+, pip
- Node.js + npm (for the OpenClaw plugin only)

### 1. Install the ClawWall service (PyPI)

```bash
pip install clawwall==0.2.1
```

Verify the SHA256 of the downloaded wheel if you want to confirm integrity:
```
5939d375c724771931e92e88be2b2f11cd27a4eec095af95cb6923b61220c65f  clawwall-0.2.1-py3-none-any.whl
1e1ecae39bb4d351f0e503501e2615814c5c0cd0f822998f5648fa74eb1de5c2  clawwall-0.2.1.tar.gz
```

Or clone at the pinned release tag:
```bash
git clone --branch v0.2.1 https://github.com/Stanxy/clawguard.git
cd clawguard && pip install .
```

### 2. Start the service

```bash
clawwall
```

Or via Python:
```bash
python -m clawguard
```

Service starts on **http://localhost:8642**.
Dashboard at **http://localhost:8642/dashboard**.

### 3. Install the OpenClaw plugin (manual)

```bash
git clone --branch v0.2.1 https://github.com/Stanxy/clawguard.git
cd clawguard/openclaw-integration/clawguard-plugin
npm install && npm run build
```

Then **manually** add to your OpenClaw config:
```json
{
  "plugins": {
    "clawwall": {
      "path": "/path/to/clawguard/openclaw-integration/clawguard-plugin/dist/index.js",
      "config": {
        "serviceUrl": "http://127.0.0.1:8642",
        "blockOnError": false,
        "timeoutMs": 5000
      }
    }
  }
}
```

> Set `blockOnError: true` to fail-closed (block all tool calls if the service is unreachable).
> Set `blockOnError: false` (default) to fail-open (allow calls through if the service is down).

### 4. (Optional) Install this skill

```bash
clawhub install clawwall
```

## Configuration

Environment variables (all prefixed `CLAWGUARD_`):

| Variable | Default | Description |
|---|---|---|
| `CLAWGUARD_HOST` | `0.0.0.0` | Bind address |
| `CLAWGUARD_PORT` | `8642` | Port |
| `CLAWGUARD_DATABASE_URL` | `sqlite+aiosqlite:///clawwall.db` | Database path |
| `CLAWGUARD_POLICY_PATH` | `config/default_policy.yaml` | Policy file |
| `CLAWGUARD_LOG_LEVEL` | `INFO` | Log verbosity |

## What ClawWall Detects

- **Secrets (51 patterns):** AWS, GCP, Azure, GitHub, Stripe, Slack, PayPal, Square, SSH/PGP private keys, database URIs, JWT tokens, and more
- **PII (10 patterns):** SSNs, credit cards (Luhn-validated), emails, phone numbers, IP addresses
- **Entropy analysis:** high-entropy strings that don't match any known pattern

## Policy

Default policy (`config/default_policy.yaml`) blocks all findings:

```yaml
default_action: BLOCK      # BLOCK | REDACT | ALLOW
redaction:
  strategy: mask           # mask | hash | remove
  mask_char: "*"
  mask_preserve_edges: 4
destination_allowlist: []  # bypass scanning for trusted destinations
destination_blocklist: []  # always reject these destinations
custom_patterns: []        # add your own regex patterns
disabled_patterns: []      # disable specific built-in patterns by name
```

## API Quick Start

```bash
curl -s -X POST http://localhost:8642/api/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"content": "key=AKIAIOSFODNN7EXAMPLE", "destination": "api.example.com"}'
```

Response:
```json
{
  "action": "BLOCK",
  "findings": [{
    "finding_type": "aws_access_key_id",
    "severity": "CRITICAL",
    "redacted_snippet": "AKIA************MPLE"
  }],
  "duration_ms": 2.1
}
```

## Agent Instructions

You are operating behind **ClawWall**. All outbound tool calls are scanned before leaving the machine using hard pattern matching — not an LLM.

| Result | Meaning |
|--------|---------|
| `ALLOW` | No sensitive data detected — call went through |
| `REDACT` | Sensitive portions were masked before sending |
| `BLOCK` | Call rejected — nothing was sent |

**Best practices:**
- Never include raw API keys, tokens, or PII in outbound calls
- Reference credentials by name (`$OPENAI_API_KEY`), not by value
- If blocked, check `findings` to see what matched, remove it, and retry
- False positive? Tell the user to adjust the policy via the dashboard at http://localhost:8642/dashboard
