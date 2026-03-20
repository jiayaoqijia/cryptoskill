---
name: x402_payment_tron
description: "Pay for x402-enabled Agent endpoints using USDT on TRON"
version: 1.0.0
author: x402-protocol
homepage: https://x402.org
metadata: {"clawdbot":{"emoji":"💳","env":["TRON_PRIVATE_KEY"]}}
tags: [crypto, payments, x402, agents, api, usdt, tron]
requires_tools: [x402_tron_invoke]
arguments:
  agent_url:
    description: "Base URL of the x402 agent"
    required: false
  endpoint:
    description: "Entrypoint name to invoke (e.g., 'chat', 'search')"
    required: false
---

# x402 Payment Protocol for TRON Agents

Invoke x402-enabled AI agent endpoints with automatic USDT micropayments on TRON.

## Quick Start

### Option 1: Run Pre-built (Recommended for Agents)
The skill is pre-bundled into a single file. No installation required.
```bash
node dist/index.js --url <URL> [options]
```

### Option 2: Development
```bash
npm install
npm start -- --url <URL>
```

## Tool Reference

- **Wallet**: A TRON private key must be available. The skill automatically looks for it in:
  1. `TRON_PRIVATE_KEY` environment variable.
  2. `~/.mcporter/mcporter.json` (AIBank standard configuration).
  3. `x402-config.json` in the current directory.
  4. `~/.x402-config.json` in the home directory.
- **USDT on TRON**: Wallet needs USDT and some TRX for gas.

---

## Tool Reference

### x402_tron_invoke

Invokes an HTTP endpoint. If payment is required (402), it automatically:
1. Negotiates payment requirements.
2. Checks USDT allowance. If insufficient, it performs an **infinite approval** (MAX_UINT256) to minimize future transactions.
3. Signs the payment permit (EIP-712).
4. Retries the request with the payment signature.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | Full URL to invoke |
| `method` | string | No | HTTP method (GET, POST, etc.) Default: GET |
| `body` | object | No | JSON body for the request |
| `network` | string | No | `mainnet`, `nile`, `shasta` (Default: `nile`) |

### Example: Chat with Agent

```tool:x402_tron_invoke
url: https://api.example.com/chat
method: POST
body: {"prompt": "Tell me a joke"}
```

---

## Agent Discovery

You can discover available endpoints and their pricing by checking the agent's manifest.

### Fetch Agent Manifest

```tool:x402_tron_invoke
url: https://api.example.com/.well-known/agent.json
method: GET
```

---

## Security Rules for Agents

- **No Private Key Output**: The Agent MUST NOT print, echo, or output the `TRON_PRIVATE_KEY` or any other signing secret to the dialogue context.
- **Internal Loading Only**: The Agent should rely on the skill or underlying scripts to load the key internally.
- **No Export Commands**: The Agent MUST NOT execute shell commands that contain the private key as a literal string (e.g., `export TRON_PRIVATE_KEY=...`).
- **Sanitized Logs**: Ensure that logs or error messages do not leak the key.

## Troubleshooting

### "Private key not found"
Ensure the `TRON_PRIVATE_KEY` environment variable is set or a valid `x402-config.json` exists in the expected locations. 
**Agent Note**: If this error occurs, simply inform the user that the environment is not configured. DO NOT attempt to search for or read private keys from files yourself.

### "Insufficient Allowance"
The tool will attempt to broadcast an **infinite approve** transaction. This requires TRX for gas. Ensure your wallet has TRX.

### "Transaction Failed"
Check if you have enough USDT and TRX.

---

## Binary and Image Handling

If the endpoint returns an image (Content-Type: `image/*`) or binary data (`application/octet-stream`):
1. The data is automatically saved to a temporary file (e.g., `/tmp/x402_image_...` or `/tmp/x402_binary_...`).
2. The tool returns a JSON object with:
    - `file_path`: Path to the temporary file.
    - `content_type`: The MIME type of the content.
    - `bytes`: File size in bytes.
3. **Important**: The Agent is responsible for deleting the temporary file after it has been used or processed.

---

## Network Reference

| Network | Chain ID | CAIP-2 | USDT Contract |
|---------|----------|--------|---------------|
| TRON Mainnet | 0x2b6653dc | `eip155:728126428`, `tron:mainnet` | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` |
| TRON Nile | 0xcd8690dc | `eip155:3448148188`, `tron:nile` | `TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf` |
| TRON Shasta | 0x94a9059e | `eip155:2494104990`, `tron:shasta` | - |
