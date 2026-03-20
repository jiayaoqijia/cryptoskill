---
name: elizacloud
description: Manage elizaOS Cloud - deploy AI agents, chat completions, image/video generation, voice cloning, knowledge base, containers, and marketplace. Use when interacting with elizaOS Cloud, elizacloud.ai, deploying eliza agents, or managing cloud-hosted AI agents. Requires ELIZACLOUD_API_KEY environment variable.
metadata:
  openclaw:
    requires:
      env: [ELIZACLOUD_API_KEY]
---

# elizaOS Cloud

elizaOS Cloud is a platform for building, deploying, and scaling intelligent AI agents. This skill provides access to the complete elizaOS Cloud API for managing agents, generating content, and building AI-powered applications.

## Quick Start

Set your API key as an environment variable:

```bash
export ELIZACLOUD_API_KEY="your_api_key_here"
```

Use the included bash client for common operations:

```bash
./scripts/elizacloud-client.sh status
./scripts/elizacloud-client.sh agents list
./scripts/elizacloud-client.sh chat agent-id "Hello!"
```

## API Configuration

- **Base URL**: `https://elizacloud.ai/api/v1`
- **Authentication**: 
  - `Authorization: Bearer $ELIZACLOUD_API_KEY`
  - `X-API-Key: $ELIZACLOUD_API_KEY`
- **Content-Type**: `application/json`

## Core Endpoints

### Chat Completions (OpenAI-Compatible)

```bash
curl https://elizacloud.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-agent-id",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

**Features**: Streaming, function calling, structured outputs

### Agent Management

**List Agents**
```bash
GET /api/my-agents/characters
```

**Create Agent**
```bash
POST /api/v1/app/agents
{
  "name": "My Assistant",
  "bio": "A helpful AI assistant"
}
```

**Get Agent**
```bash
GET /api/my-agents/characters/{id}
```

**Delete Agent**
```bash
DELETE /api/my-agents/characters/{id}
```

### Image Generation

```bash
POST /api/v1/images/generate
{
  "prompt": "A futuristic city at sunset",
  "model": "flux-pro",
  "width": 1024,
  "height": 1024
}
```

**Models**: FLUX Pro, FLUX Dev, Stable Diffusion

### Video Generation

```bash
POST /api/v1/video/generate
{
  "prompt": "A peaceful lake with mountains in the background",
  "duration": 5,
  "model": "minimax-01"
}
```

**Models**: MiniMax, Runway

### Voice Cloning (ElevenLabs)

```bash
POST /api/v1/voice/clone
{
  "text": "Hello, this is a test of voice cloning",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "model": "eleven_turbo_v2"
}
```

### Knowledge Base

**Upload Document**
```bash
POST /api/v1/knowledge/upload
```

**Query Knowledge**
```bash
POST /api/v1/knowledge/query
{
  "query": "How do I deploy an agent?",
  "limit": 5
}
```

### Containers

**Deploy Container**
```bash
POST /api/v1/containers
{
  "name": "my-app",
  "image": "nginx:latest",
  "ports": [{"containerPort": 80}]
}
```

### A2A Protocol (Agent-to-Agent)

**Discover Agents**
```bash
GET /api/v1/discovery
```

**Send Task**
```bash
POST /api/a2a
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "params": {
    "id": "task_123",
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "Analyze this data"}]
    }
  },
  "id": 1
}
```

## API Keys

**Create API Key**
```bash
POST /api/v1/api-keys
{
  "name": "Production Key",
  "permissions": ["chat", "agents", "images"]
}
```

**Available Permissions**: `chat`, `embeddings`, `images`, `video`, `voice`, `knowledge`, `agents`, `apps`

## Error Handling

All errors follow this format:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request body is invalid",
    "details": "Field 'model' is required"
  }
}
```

**Common Error Codes**:
- `UNAUTHORIZED` (401): Invalid/missing authentication
- `FORBIDDEN` (403): Insufficient permissions
- `NOT_FOUND` (404): Resource not found
- `RATE_LIMITED` (429): Too many requests
- `INSUFFICIENT_CREDITS` (402): Not enough credits

## Rate Limits

| Endpoint         | Rate Limit  |
|------------------|-------------|
| Chat completions | 60 req/min  |
| Embeddings       | 100 req/min |
| Image generation | 20 req/min  |
| Video generation | 5 req/min   |

## Example Workflows

### Deploy a Customer Support Agent

```bash
# 1. Create agent
curl -X POST https://elizacloud.ai/api/v1/app/agents \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"name": "Support Bot", "bio": "Customer support specialist"}'

# 2. Chat with agent
curl https://elizacloud.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"model": "agent-id", "messages": [{"role": "user", "content": "Help me"}]}'
```

### Generate Marketing Assets

```bash
# 1. Generate image
curl -X POST https://elizacloud.ai/api/v1/images/generate \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"prompt": "Modern tech startup logo", "model": "flux-pro"}'

# 2. Generate video
curl -X POST https://elizacloud.ai/api/v1/video/generate \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"prompt": "Product demo animation", "duration": 10}'
```

### Build Agent Network with A2A

```bash
# 1. Discover available agents
curl https://elizacloud.ai/api/v1/discovery \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY"

# 2. Delegate task to specialist agent
curl -X POST https://elizacloud.ai/api/a2a \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"jsonrpc": "2.0", "method": "tasks/send", "params": {"message": {"role": "user", "parts": [{"type": "text", "text": "Analyze financial data"}]}}}'
```

## Onboarding

### Sign Up
Register at [elizacloud.ai/login](https://elizacloud.ai/login) (Privy auth — browser required).
New accounts receive **1,000 free credits** — enough to test chat, image gen, and more.

### Get API Key
```bash
# After signing up, create a key at Dashboard → API Keys
# Or via API (once authenticated):
POST /api/v1/api-keys
{
  "name": "My OpenClaw Agent",
  "permissions": ["chat", "agents", "images", "video", "voice", "knowledge"]
}
```

### Install CLI (Optional)
```bash
bun add -g @elizaos/cli
elizaos login
```

## Payments & Credits

### Check Balance
```bash
GET /api/v1/credits/balance
```

### Purchase Credits (Stripe)
```bash
POST /api/v1/credits/checkout
{ "amount": 5000 }
# Returns a Stripe checkout URL — redirect to complete payment
```

### x402 Crypto Payment (USDC)
Pay per-request with cryptocurrency — no pre-purchased credits needed:
```bash
# Include x402 payment header with any API request
curl -X POST "https://elizacloud.ai/api/v1/chat/completions" \
  -H "X-PAYMENT: <x402-payment-header>" \
  -H "Content-Type: application/json" \
  -d '{"model": "agent-id", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Auto Top-Up
```bash
PUT /api/v1/billing/settings
{
  "autoTopUp": true,
  "threshold": 100,
  "amount": 1000
}
```

### Credit Transactions
```bash
GET /api/credits/transactions?limit=50
```

### Usage Summary
```bash
GET /api/v1/credits/summary
# Returns: org balance, agent budgets, app earnings, redeemable earnings
```

## Wallet & Crypto RPCs

### Create Crypto Payment
```bash
POST /api/crypto/payments
```

### Check Payment Status
```bash
GET /api/crypto/status
```

### Authentication Methods
| Method | Header | Use Case |
|--------|--------|----------|
| API Key | `Authorization: Bearer ek_xxx` | Server-to-server |
| X-API-Key | `X-API-Key: ek_xxx` | Alternative header |
| x402 | `X-PAYMENT: <header>` | Pay-per-request with USDC |
| Session | Cookie-based | Browser apps |

## Additional Resources

- **Full API Documentation**: See `references/api-reference.md` for complete endpoint details
- **Dashboard**: https://elizacloud.ai/dashboard for visual management
- **OpenAPI Spec**: https://elizacloud.ai/api/openapi.json
- **SDKs**: TypeScript, Python clients available
- **Community**: Discord at https://discord.gg/elizaos

## Environment Variables

- `ELIZACLOUD_API_KEY`: Your elizaOS Cloud API key (required)
- `ELIZACLOUD_BASE_URL`: API base URL (default: https://elizacloud.ai/api/v1)

## Security Notes

- Never commit API keys to version control
- Use separate keys for development/production
- Rotate keys regularly
- Limit permissions to minimum required scope
- Monitor usage in the dashboard for anomalies