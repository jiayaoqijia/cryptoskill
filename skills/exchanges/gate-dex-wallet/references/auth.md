---
name: gate-dex-auth
version: "2026.3.25-1"
updated: "2026-03-25"
description: "Gate Wallet authentication module. Manages Google OAuth and Gate OAuth login, and logout. Use when the user needs to log in, log out, or refresh an expired session, or when another skill detects a missing mcp_token."
---

# Gate DEX Auth

> Authentication module — manages Google OAuth and Gate OAuth login, token refresh, and logout. 7 MCP tools.

## Applicable Scenarios

Use when the user wants to authenticate or manage their session, or when another skill detects a missing or expired `mcp_token`:

- Direct login request: "login", "sign in", "authenticate", "connect my wallet account"
- Logout: "logout", "sign out", "disconnect", "end session"
- Token/session issues: "session expired", "not logged in", "token invalid", "I can't access my wallet"
- Account switching: "switch account", "login with a different account", "use another wallet"
- Routed from other modules: any tool returns 401/unauthorized or missing `mcp_token`
- OAuth-specific: "Google login", "Gate login", "use my Gate account", "login via Google"

## Capability Boundaries

- Login itself does **not** require `mcp_token` — this is the entry point for obtaining one.
- `dex_auth_logout` requires an existing token.
- After successful login, `mcp_token` and `account_id` are passed to all other skills that require authentication.

**Prerequisites**: MCP Server must be available. If not configured, see parent SKILL.md for the setup guide.

---

## MCP Tools

### 1. `dex_auth_google_login_start` — Start Google OAuth Login

Initiates Google Device Flow login and returns a verification URL.


| Field          | Description                                     |
| -------------- | ----------------------------------------------- |
| **Parameters** | None                                            |
| **Returns**    | `{ verification_url: string, flow_id: string }` |


Agent behavior: Display `verification_url` directly to the user. The link must be complete, copyable, and clickable — do not add quotes, parentheses, or escape characters.

### 2. `dex_auth_google_login_poll` — Poll Google Login Status

Polls Google OAuth login results using `flow_id`.


| Field          | Description                                                                           |
| -------------- | ------------------------------------------------------------------------------------- |
| **Parameters** | `{ flow_id: string }`                                                                 |
| **Returns**    | `{ status: string, mcp_token?: string, refresh_token?: string, account_id?: string }` |



| status    | Meaning                              | Next Action                                        |
| --------- | ------------------------------------ | -------------------------------------------------- |
| `pending` | User has not completed authorization | Wait a few seconds, then retry                     |
| `success` | Login successful                     | Extract `mcp_token`, `refresh_token`, `account_id` |
| `expired` | Login flow timed out                 | Prompt user to initiate login again                |
| `error`   | Login error                          | Display error message                              |


### 3. `dex_auth_login_google_wallet` — Google Authorization Code Login

Direct login using an existing Google OAuth authorization code.


| Field          | Description                                                              |
| -------------- | ------------------------------------------------------------------------ |
| **Parameters** | `{ code: string, redirect_url: string }`                                 |
| **Returns**    | `MCPLoginResponse` (contains `mcp_token`, `refresh_token`, `account_id`) |


### 4. `dex_auth_gate_login_start` — Start Gate OAuth Login

Initiates Gate OAuth Device Flow login and returns a verification URL.


| Field          | Description                                     |
| -------------- | ----------------------------------------------- |
| **Parameters** | None                                            |
| **Returns**    | `{ verification_url: string, flow_id: string }` |


Agent behavior: Same as Google login — display `verification_url` directly to the user.

### 5. `dex_auth_gate_login_poll` — Poll Gate Login Status

Polls Gate OAuth login results using `flow_id`.


| Field          | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| **Parameters** | `{ flow_id: string }`                                               |
| **Returns**    | `{ status: string, login_result?: { mcp_token, account_id, ... } }` |



| status    | Meaning                        | Next Action                                           |
| --------- | ------------------------------ | ----------------------------------------------------- |
| `pending` | Waiting for user authorization | Wait a few seconds, then retry                        |
| `ok`      | Login successful               | Extract `mcp_token`, `account_id` from `login_result` |
| `error`   | Login failed                   | Display error message                                 |


**CRITICAL**: When status is `ok`, you MUST immediately replace any previously stored `mcp_token` with the NEW `mcp_token` from `login_result`. The new token is associated with a different account and wallet addresses.

### 6. `dex_auth_login_gate_wallet` — Gate Authorization Code Login

Direct login using an existing Gate OAuth authorization code.


| Field          | Description                                             |
| -------------- | ------------------------------------------------------- |
| **Parameters** | `{ code: string, redirect_url: string }`                |
| **Returns**    | `MCPLoginResponse` (contains `mcp_token`, `account_id`) |


**CRITICAL**: After successful login, immediately replace stored `mcp_token` with the new one.

### 7. `dex_auth_logout` — Logout

Revokes the current session and invalidates `mcp_token`.


| Field          | Description             |
| -------------- | ----------------------- |
| **Parameters** | `{ mcp_token: string }` |
| **Returns**    | `"session revoked"`     |


---

## Operation Flows

### Flow A: Google Device Flow Login (Default)

```
Step 1: Determine user needs to login (direct request or routed from another skill)
  |
Step 2: Call dex_auth_google_login_start -> get verification_url + flow_id
  |
Step 3: Display verification link to user
  "Please open the following link in your browser to complete Google login:
   {verification_url}
   After completion, let me know and I'll confirm the login status."
  |
Step 4: After user confirms, call dex_auth_google_login_poll({ flow_id })
  |- pending  -> Ask user to confirm completion; retry (max 10 times, 3s intervals)
  |- success  -> Extract mcp_token, refresh_token, account_id -> Step 5
  |- expired  -> Notify timeout; suggest re-initiating login
  |- error    -> Display error message
  |
Step 5: Login success
  Record mcp_token, refresh_token, account_id internally (never display tokens).
  If user had a prior intent -> return to that operation.
  If no prior intent -> display available actions (see Post-Auth template).
```

### Flow B: Gate OAuth Device Flow Login

```
Step 1: User requests Gate login (e.g., "use Gate account", "Gate OAuth login")
  |
Step 2: Call dex_auth_gate_login_start -> get verification_url + flow_id
  |
Step 3: Display verification link to user
  "Please open the following link in your browser to complete Gate login:
   {verification_url}
   After completion, let me know and I'll confirm the login status."
  |
Step 4: After user confirms, call dex_auth_gate_login_poll({ flow_id })
  |- pending  -> Retry (max 10 times, 3s intervals)
  |- ok       -> Extract mcp_token, account_id from login_result -> Step 5
  |- error    -> Display error message
  |
Step 5: Same as Flow A Step 5.
```

### Flow C: Logout

```
Step 1: User requests logout
  |
Step 2: Call dex_auth_logout({ mcp_token })
  |
Step 3: Clear internally held mcp_token, refresh_token, account_id
  |
Step 4: Confirm: "Successfully logged out. To use wallet functions again, please re-login."
```

### Flow D: Authorization Code Login (Alternative)

```
Step 1: User provides a Google or Gate authorization code
  |
Step 2: Call dex_auth_login_google_wallet or dex_auth_login_gate_wallet
         ({ code, redirect_url })
  |
Step 3: On success -> same as Flow A Step 5
```

---

## Post-Auth Routing

After authentication, if the user was routed here from another module, return them to their original operation silently.

If the user logged in directly (no prior intent), **proactively display available actions**:

```
Login successful! Account: {account_id (masked)}.

You can now:
- Check your wallet balance and assets
- Transfer or send tokens
- Swap or exchange tokens
- Interact with DApps
- View market data and token info
- Pay for 402 resources (x402)

What would you like to do?
```


| User Follow-up Intent             | Route Target                       |
| --------------------------------- | ---------------------------------- |
| Check balance, assets, address    | [asset-query.md](./asset-query.md) |
| Transfer or send tokens           | [transfer.md](./transfer.md)       |
| Swap or exchange tokens           | `gate-dex-trade`                   |
| Pay for a 402 resource            | [x402.md](./x402.md)               |
| DApp interaction or sign messages | [dapp.md](./dapp.md)               |
| Check token prices or info        | `gate-dex-market`                  |


---

## Conversation Examples

**Example 1: First-time login (Google — default)**
User: "Help me login to Gate wallet"
Agent:

1. Call `dex_auth_google_login_start` to get verification URL.
2. Display URL to user.
3. After user confirms, poll with `dex_auth_google_login_poll`.
4. On success, confirm login and ask what the user wants to do next.

**Example 2: Gate OAuth login**
User: "Login with my Gate account"
Agent:

1. Call `dex_auth_gate_login_start` to get verification URL.
2. Display URL to user.
3. After user confirms, poll with `dex_auth_gate_login_poll`.
4. On success, confirm login.

**Example 3: Token expired during operation**
User: "Check my ETH balance" (but mcp_token is expired)
Agent:

1. Attempt silent token refresh.
2. On success, proceed with balance query transparently.
3. On failure, notify user and initiate re-login flow.

**Example 4: Implicit login need — vague request**
User: "I can't access my wallet" / "something is wrong with my session"
Agent:

1. Check current auth status.
2. If no valid `mcp_token`, initiate login flow.
3. If token exists but is expired, attempt refresh first.

**Example 5: Account switch**
User: "I want to switch to a different account"
Agent:

1. Call `dex_auth_logout` to revoke current session.
2. Confirm logout success.
3. Initiate new login flow (ask user: Google or Gate).

**Example 6: Logout**
User: "Log me out" / "disconnect my wallet"
Agent:

1. Call `dex_auth_logout({ mcp_token })`.
2. Clear local state.
3. Confirm: "Successfully logged out."

**Example 7: Re-login after failure**
User: "Login failed, try again"
Agent:

1. Start a fresh login flow (do not retry the old flow_id).
2. Call `dex_auth_google_login_start` for a new verification URL.

**Example 8: Not this module**
User: "What is ETH price?"
Agent: Route to `gate-dex-market` — this is a market data query, not authentication.

**Example 9: Not this module — transfer**
User: "Send 1 ETH to 0xABC..."
Agent: Route to [transfer.md](./transfer.md) — this is a transfer, not authentication. (If auth is needed, the transfer module will route back here.)

---

## Error Handling


| Scenario                            | Handling                                                                          |
| ----------------------------------- | --------------------------------------------------------------------------------- |
| `dex_auth_google_login_start` fails | Display error; suggest retry or check MCP Server status                           |
| `dex_auth_gate_login_start` fails   | Display error; suggest retry or check MCP Server status                           |
| User hasn't completed browser auth  | Poll returns `pending`; prompt user to complete browser operation first           |
| Login flow timeout (`expired`)      | Notify timeout; automatically call login_start to start a new flow                |
| Consecutive poll failures           | Max 10 retries at 3s intervals; after that, prompt user to check network or retry |
| Token refresh fails                 | Guide through full re-login (Flow A or B)                                         |
| `dex_auth_logout` fails             | Display error; still clear local token state                                      |
| User already logged in              | Notify already logged in; ask if they want to switch accounts                     |
| Invalid authorization code          | Display error; suggest re-obtaining the code or using Device Flow                 |


---

## Security Rules

1. **Token confidentiality**: Never display `mcp_token` or `refresh_token` in plaintext. Use placeholders like `<mcp_token>`.
2. **Account masking**: When displaying `account_id`, show only partial characters (e.g., `acc_12...89`).
3. **Silent refresh**: Prioritize silent token refresh; only require re-login if refresh fails.
4. **No silent login retry**: After login failure, clearly display the error — do not retry in the background.
5. **MCP Server required**: If connection detection fails, abort all operations.
6. **Single session**: Maintain only one active `mcp_token` at a time. Switching accounts requires logout first.
7. **Transparent errors**: Display all MCP Server error messages to users truthfully.
8. **Immediate token replacement**: When Gate OAuth returns a new `mcp_token`, immediately replace the old one — the new token is associated with a different account.

