# Publishing x402-agent-free to ClawHub

## Prerequisites

1. **ClawHub CLI** installed:
   ```bash
   npm install -g clawhub
   ```

2. **GitHub account** linked to ClawHub (Tara Quinn AI / tara-quinn-ai)

3. **Authenticate** with ClawHub:
   ```bash
   clawhub login
   ```

## Skill Folder Structure

```
x402-agent-free/
  SKILL.md                         # Stripped-down skill (detect+pay only)
  VERSION                          # Semver version (1.0.0)
  references/
    basic-setup.example.ts         # Basic setup using @x402/fetch directly
```

## What's Different from the Full Version

| Feature | Free (this) | Paid (x402-agent) |
|---------|:-----------:|:-----------------:|
| 402 detection + auto-pay | Yes | Yes |
| Policy engine (spending limits) | No | Yes |
| Domain filtering | No | Yes |
| Payment logging | No | Yes |
| Express middleware | No | Yes |
| Demo app | No | Yes |
| Uses | `@x402/fetch` directly | `@x402-kit/agent` |

## Publish

From the repo root:

```bash
cd x402-agent-free
clawhub publish
```

## Verify

After publishing:

1. Visit https://clawhub.ai and search for "x402-agent-free"
2. Verify the skill page shows:
   - Name: `x402-agent-free`
   - Version: `1.0.0`
   - Requirements: `X402_WALLET_PRIVATE_KEY` env var, `node` binary
3. Verify the upsell link to ClawMart works
4. Test installation:
   ```bash
   clawhub install x402-agent-free
   ```

## Strategy

- Free skill on ClawHub drives awareness and installs
- Users who need policy controls, logging, or Express middleware upgrade to the paid kit
- Upsell link at the bottom of SKILL.md points to ClawMart listing
