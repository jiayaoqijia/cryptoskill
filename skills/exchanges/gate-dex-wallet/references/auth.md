---
name: gate-dex-auth
description: "Gate Wallet authentication. Use when users need to login, logout, refresh session, or other Skills detect no login (no mcp_token). Supports Google OAuth login. First-time use will detect if MCP Server connection is configured."
---

# Gate DEX Auth

> Authentication domain — Manage Google OAuth login, Token refresh and logout. 5 MCP tools.

**Trigger Scenarios**: When users mention "login", "logout", "auth", "login", "logout", "sign in", or other Skills detect no `mcp_token`.

## MCP Server Connection Detection

### Initial Session Detection

**Execute connection probe once before first MCP tool call in session to confirm Gate Wallet MCP Server availability. No need to repeat detection for subsequent operations.**

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Handling |
|------|------|
| Success | MCP Server available, subsequent operations call business tools directly without re-detection |
| Failure | Show configuration guidance based on error type (see error handling below) |

### Runtime Error Fallback

For subsequent operations, if business tool calls fail (connection error, timeout, etc.), handle according to the following rules:

| Error Type | Keywords | Handling |
|---------|--------|------|
| MCP Server not configured | `server not found`, `unknown server` | Show MCP Server configuration guidance |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Suggest checking server status and network connection |
| Authentication failure | `401`, `unauthorized`, `x-api-key` | Suggest contacting administrator for API Key |

## MCP Server Configuration Instructions

**Complete configuration format**:

```json
{
  "mcpServers": {
    "gate-wallet": {
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "x-api-key": "MCP_AK_8W2N7Q",
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
```

**Configuration explanation**:
- `x-api-key`: Fixed value `MCP_AK_8W2N7Q`, used for MCP Server identity recognition
- `Authorization`: Dynamic value, containing `mcp_token` obtained after Google OAuth or Gate OAuth login
- `<your_mcp_token>` is placeholder during initial configuration, automatically updated after successful login

**Token acquisition process**:
1. User logs in through authentication module (Google OAuth / Gate OAuth)
2. Get `mcp_token` after successful login
3. Agent automatically updates Authorization header in MCP configuration
4. All subsequent MCP calls use updated token

## Authentication Instructions

This Skill is the authentication entry point, **executing login operations itself does not require `mcp_token`**. `auth.refresh_token` and `auth.logout` require existing token.

The `mcp_token` and `account_id` obtained after successful login will be passed to other Skills that require authentication (portfolio, transfer, swap, dapp).

## MCP Tool Call Specifications

### 1. `auth.google_login_start` — Start Google OAuth Login

Initiate Google Device Flow login, return verification URL user needs to visit.

| Field | Description |
|------|------|
| **Tool Name** | `auth.google_login_start` |
| **Parameters** | None |
| **Return Value** | `{ verification_url: string, flow_id: string }` |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.google_login_start",
  arguments={}
)
```

Return example:

```json
{
  "verification_url": "https://accounts.google.com/o/oauth2/device?user_code=ABCD-EFGH",
  "flow_id": "flow_abc123"
}
```

Agent behavior: Display `verification_url` to user, guide them to complete Google authorization in browser.

---

### 2. `auth.google_login_poll` — Poll Login Status

Use `flow_id` to poll Google OAuth login result, determine if user has completed browser-side authorization.

| Field | Description |
|------|------|
| **Tool Name** | `auth.google_login_poll` |
| **Parameters** | `{ flow_id: string }` |
| **Return Value** | `{ status: string, mcp_token?: string, refresh_token?: string, account_id?: string }` |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.google_login_poll",
  arguments={ flow_id: "flow_abc123" }
)
```

Return value `status` meanings:

| status | Meaning | Next Action |
|--------|------|---------|
| `pending` | User has not completed authorization yet | Wait a few seconds then retry |
| `success` | Login successful | Extract `mcp_token`, `refresh_token`, `account_id` |
| `expired` | Login process timed out | Prompt user to restart login |
| `error` | Login error | Display error message |

---

### 3. `auth.login_google_wallet` — Google Authorization Code Login

Use Google OAuth authorization code to login directly (suitable for scenarios with existing code).

| Field | Description |
|------|------|
| **Tool Name** | `auth.login_google_wallet` |
| **Parameters** | `{ code: string, redirect_url: string }` |
| **Return Value** | `MCPLoginResponse` (contains `mcp_token`, `refresh_token`, `account_id`) |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.login_google_wallet",
  arguments={ code: "4/0AX4XfW...", redirect_url: "http://localhost:8080/callback" }
)
```

---

### 4. `auth.refresh_token` — Refresh Token

When `mcp_token` expires, use `refresh_token` to get new valid token.

| Field | Description |
|------|------|
| **Tool Name** | `auth.refresh_token` |
| **Parameters** | `{ refresh_token: string }` |
| **Return Value** | `RefreshTokenResponse` (contains new `mcp_token`, new `refresh_token`) |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.refresh_token",
  arguments={ refresh_token: "rt_xyz789..." }
)
```

Agent behavior: Silently update internally held `mcp_token` after successful refresh, transparent to user.

---

### 5. `auth.logout` — Logout

Revoke current session, invalidate `mcp_token`.

| Field | Description |
|------|------|
| **Tool Name** | `auth.logout` |
| **Parameters** | `{ mcp_token: string }` |
| **Return Value** | `"session revoked"` |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.logout",
  arguments={ mcp_token: "<current_mcp_token>" }
)
```

## Skill Routing

After authentication completion, guide to corresponding Skill based on user's original intent:

| User Intent | Routing Target |
|---------|---------|
| Check balance, check assets, check address | `gate-dex-wallet` |
| Transfer, send tokens | `gate-dex-transfer` |
| Exchange, Swap tokens | `gate-dex-trade` |
| DApp interaction, sign messages | `gate-dex-dapp` |
| Check prices, check token info | `gate-dex-market` |

When other Skills detect missing or expired `mcp_token`, they will also route to this Skill to complete authentication then return to original operation.

## Operation Flows

### Flow A: Google Device Flow Login (Main Flow)

```
Initial session detection (if needed)
  ↓ Success
Step 1: Intent recognition
  Agent determines user needs to login (direct login request, or guided here by other Skills)
  ↓
Step 2: Initiate login
  Call auth.google_login_start → Get verification_url + flow_id
  ↓
Step 3: Guide user authorization
  Display verification link to user, ask user to complete Google authorization in browser:

  ────────────────────────────
  Please open the following link in browser to complete Google login:
  {verification_url}

  Please tell me after completion, I will confirm login status.
  ────────────────────────────

  ↓
Step 4: Poll login result
  After user confirms completion of authorization, call auth.google_login_poll({ flow_id })
  - status == "pending" → Ask user to confirm completion, retry later (max 10 retries, 3 second intervals)
  - status == "success" → Extract mcp_token, refresh_token, account_id, proceed to Step 5
  - status == "expired" → Prompt timeout, suggest restart login
  - status == "error" → Display error message
  ↓
Step 5: Login successful
  Internally record mcp_token, refresh_token, account_id (don't display token plaintext to user)
  Confirm login success to user:

  ────────────────────────────
  ✅ Login successful!
  Account: {account_id} (masked display)

  You can now:
  - View wallet balances and assets
  - Transfer and send tokens
  - Swap and exchange tokens
  - Interact with DApps
  - View market data

  Please tell me what you want to do?
  ────────────────────────────

  ↓
Step 6: Route to user's original intent
  Guide to corresponding Skill based on user's initial request or subsequent instructions
```

### Flow B: Token Refresh (Auto-triggered)

```
Trigger condition: Other Skills return token expired error when calling MCP tools
  ↓
Step 1: Auto refresh
  Call auth.refresh_token({ refresh_token })
  ↓
Step 2a: Refresh successful
  Silently update mcp_token, retry original operation, transparent to user
  ↓
Step 2b: Refresh failed
  refresh_token also expired → Guide user to re-login (Flow A)

  ────────────────────────────
  ⚠️ Session has expired, need to re-login.
  Starting Google login for you...
  ────────────────────────────
```

### Flow C: Logout

```
Initial session detection (if needed)
  ↓ Success
Step 1: Intent recognition
  User requests logout / exit
  ↓
Step 2: Execute logout
  Call auth.logout({ mcp_token })
  ↓
Step 3: Clean state
  Clear internally held mcp_token, refresh_token, account_id
  ↓
Step 4: Confirm logout

  ────────────────────────────
  ✅ Successfully logged out.
  To use wallet functionality again, please re-login.
  ────────────────────────────
```

### Flow D: Authorization Code Login (Alternative)

```
Initial session detection (if needed)
  ↓ Success
Step 1: User provides Google authorization code
  ↓
Step 2: Execute login
  Call auth.login_google_wallet({ code, redirect_url })
  ↓
Step 3: Login successful
  Extract mcp_token, refresh_token, account_id → Same as Flow A Step 5
```

## Cross-Skill Workflows

### Called by Other Skills (Authentication Prerequisites)

All Skills requiring `mcp_token` should guide to this Skill when detecting no login:

```
Any Skill operation (requires mcp_token)
  → Detect no mcp_token or token expired
    → Auto try auth.refresh_token (if have refresh_token)
      → Refresh success → Return to original Skill continue operation
      → Refresh failed → gate-dex-auth Flow A (login)
        → Login success → Return to original Skill continue operation
```

### Typical Workflows After Login

```
gate-dex-auth (login)
  → gate-dex-wallet (check balance/assets)        # Most common subsequent operation
  → gate-dex-transfer (transfer)                # User explicitly wants to transfer
  → gate-dex-trade (Swap)                    # User explicitly wants to exchange
  → gate-dex-dapp (DApp interaction)               # User explicitly wants DApp interaction
```

## Edge Cases and Error Handling

| Scenario | Handling Method |
|------|---------|
| MCP Server not configured | Abort all operations, show Cursor configuration guidance |
| MCP Server unreachable | Abort all operations, show network check tips |
| `auth.google_login_start` fails | Display error message, suggest retry later or check MCP Server status |
| User did not complete authorization in browser | Poll returns `pending`, prompt user to complete browser-side operation first |
| Login process timeout (`expired`) | Prompt timeout, auto restart by calling `auth.google_login_start` for new process |
| `auth.google_login_poll` consecutive failures | Max 10 retries (3 second intervals), prompt user to check network or retry after exceeding |
| `auth.refresh_token` fails | refresh_token expired or invalid → Guide to complete full login process |
| `auth.logout` fails | Display error message, still clear local token state |
| User repeated login | If already holding valid `mcp_token`, prompt currently logged in, ask if need to switch accounts |
| `auth.login_google_wallet` invalid code | Display error, suggest user re-obtain authorization code or use Device Flow instead |
| Network interruption | Display network error, suggest check network then retry |

## Security Rules

1. **`mcp_token` confidentiality**: Never display `mcp_token` or `refresh_token` in plaintext to user, only use placeholder `<mcp_token>` in conversations.
2. **`account_id` masking**: Display only partial characters when showing (like `acc_12...89`).
3. **Token auto refresh**: Prioritize silent refresh when `mcp_token` expires, only require re-login if failed.
4. **No silent retry login**: Display error clearly to user after login failure, don't repeatedly retry in background.
5. **Abort operation when MCP Server not configured or unreachable**: Abort all subsequent steps if Step 0 connection detection fails.
6. **Single session single account**: Maintain only one active `mcp_token` at same time, switching accounts requires logout first.
7. **MCP Server error transparency**: Display all MCP Server returned error messages truthfully to user, don't hide or tamper.