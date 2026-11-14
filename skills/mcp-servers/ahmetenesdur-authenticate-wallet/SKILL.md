---
name: authenticate-wallet
description: Authenticate, manage sessions, and deploy Starknet wallets with StarkFi. Handles email OTP login (two-step), session checks, address display, account deployment, and logout. Use this skill whenever the user wants to sign in, log in, check their session, see their wallet address, deploy their account, or log out — even if they don't say "authenticate" explicitly.
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: auth
allowed-tools:
    - Bash(npx starkfi@latest auth login *)
    - Bash(npx starkfi@latest auth verify *)
    - Bash(npx starkfi@latest auth logout)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest address)
    - Bash(npx starkfi@latest deploy)
---

# Authenticate Wallet

Manage authentication sessions for the StarkFi CLI. StarkFi uses a remote Auth Server with Privy TEE for email-based one-time password (OTP) authentication. A valid session is required before any transactional skill can operate.

## Prerequisites

- A running StarkFi Auth Server (`starkfi-server`). **The hosted default (`https://starkfi-production.up.railway.app`) is currently offline**, so the user must run their own from the `server/` directory of https://github.com/ahmetenesdur/starkfi and set `STARKFI_API_URL` to its URL in the environment the CLI runs in, before logging in. Guide: https://docs.starkfi.app/docs/authentication#self-hosting-the-auth-server
- An email address the user has access to (for receiving OTP codes).

## Authentication Flow

The login process is a **two-step** OTP flow:

1. **Initiate** — `auth login <email>` sends an OTP code to the email.
2. **Verify** — `auth verify <email> <code>` completes authentication.

The agent CANNOT guess or auto-fill the OTP code — it must wait for the user to provide it after checking their email.

## Rules

1. ALWAYS run `npx starkfi@latest status` first to check if the user already has an active session. If they do, skip the login flow — just inform them.
2. After `auth login`, you MUST wait for the user to provide their OTP code. Do NOT ask more than once; just say you're waiting.
3. After `auth verify`, you MUST run `npx starkfi@latest status` to confirm the session is active.
4. `deploy` is idempotent — it's safe to run multiple times. It deploys the smart account contract on-chain if not already deployed.
5. If any other skill reports `Not authenticated`, direct the user to this skill.

## Commands

```bash
# Step 1: Send OTP to email
npx starkfi@latest auth login <email>

# Step 2: Verify OTP code
npx starkfi@latest auth verify <email> <code>

# Check session status
npx starkfi@latest status

# Display wallet address
npx starkfi@latest address

# Deploy smart account on-chain
npx starkfi@latest deploy

# End session
npx starkfi@latest auth logout
```

## Parameters

| Parameter | Type   | Description                  | Required |
| --------- | ------ | ---------------------------- | -------- |
| `email`   | string | User's email address         | Yes      |
| `code`    | string | One-time password from email | Yes      |

## Examples

**User:** "Log me in with user@example.com"

```bash
npx starkfi@latest status
# If not authenticated:
npx starkfi@latest auth login user@example.com
# Wait for user to provide OTP code (e.g. "123456")
npx starkfi@latest auth verify user@example.com 123456
npx starkfi@latest status
```

**User:** "What's my wallet address?"

```bash
npx starkfi@latest address
```

**User:** "Deploy my account"

```bash
npx starkfi@latest deploy
```

**User:** "Log me out"

```bash
npx starkfi@latest auth logout
```

## Error Handling

| Error                                 | Action                                                                                                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Invalid OTP code`                    | Ask the user to check their email and retry `auth verify`.                                                                                                                |
| `Session expired` / `Session revoked` | Restart from `auth login`.                                                                                                                                                |
| `StarkFi auth server unavailable`     | Do not retry. Tell the user the auth server is down (the hosted one is offline); they must start their own `server/` and set `STARKFI_API_URL`, then log in again.        |
| `Rate limit`                          | Wait 60 seconds before retrying.                                                                                                                                          |
| `Deployment failed`    | Check balance — send ETH/STRK to the address, or enable gasfree mode first. |
| `Insufficient balance` | For deploy: `npx starkfi@latest config set-gasfree on` to bypass gas costs. |

## Related Skills

- All other skills depend on this skill — if any reports `Not authenticated`, use this.
- Use `config` to enable gasfree mode if the user can't afford deployment gas.
