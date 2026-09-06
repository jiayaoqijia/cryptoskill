# Setup — Authentication Workflow

### Step 1: Check Session
`restoreSession()` only loads tokens from the store — it succeeds even for tokens the server has already killed. Probe the API to know the truth:
```bash
bun -e '
import { getClient, AuthenticationError } from "robinhood-for-agents";
const rh = getClient();
try {
  await rh.restoreSession();
  const acct = await rh.getAccountProfile();       // the probe
  console.log("logged_in", `...${String(acct.account_number).slice(-4)}`);
} catch (e) {
  if (e instanceof AuthenticationError) console.log(e.name === "TokenExpiredError" ? "expired" : "not_authenticated");
  else console.log("unknown:", String(e));
}
'
```
| Result | Meaning | Do |
|---|---|---|
| `logged_in` | verified working (account hint shown) | stop — already authenticated |
| `expired` | tokens exist but are dead and could not be refreshed | Step 2 |
| `not_authenticated` | no tokens in the store at all | Step 2 |
| `unknown` | transient/network failure — the session may well be fine | retry once; **do not** re-login on this alone |

`restoreSession()` loads tokens from the configured TokenStore (OS keychain by default), injects Bearer auth directly into API requests, and registers both refresh paths: a pre-request hook that renews ~24h before expiry, and a 401 handler that renews reactively.

> **MCP mode:** call `robinhood_check_session` — it performs this probe server-side and returns the same four statuses (`logged_in` / `expired` / `unknown` / `not_authenticated`) plus a masked `account_hint`. Remedy for `expired` / `not_authenticated` is `robinhood_browser_login`.

### Step 2: Browser Login
```bash
bunx robinhood-for-agents onboard
```
This runs the interactive setup — it will open Google Chrome (via Playwright's `channel: "chrome"`; Chrome must be installed — no Brave/Chromium fallback or `BROWSER_PATH` override exist yet) to the real Robinhood website for login:
1. Browser opens to robinhood.com/login
2. User enters email and password
3. Robinhood handles MFA natively (push notification, SMS, etc.)
4. Token captured automatically and saved to the configured token store (OS keychain by default, or an encrypted file if `ROBINHOOD_TOKENS_FILE` is set)
5. Browser closes when login is complete

### Step 3: Verify
```bash
bun -e '
import { getClient } from "robinhood-for-agents";
const rh = getClient();
await rh.restoreSession();
const acct = await rh.getAccountProfile();
console.log(JSON.stringify(acct, null, 2));
'
```
This call is the actual verification — reaching the account profile is what proves the token works. If it throws `TokenExpiredError` immediately after a successful browser login, suspect a second client (an MCP server, another Claude Code session) that rotated the refresh token out from under this one; close the other process and re-run Step 2.

Confirm to the user that authentication is complete.

## Token Stores

| Store | When to use | Config |
|---|---|---|
| `KeychainTokenStore` (default) | Local dev, macOS/Linux with desktop | Nothing — works out of the box |
| `EncryptedFileTokenStore` | Docker, headless servers, CI, cloud | Set `ROBINHOOD_TOKENS_FILE` + `ROBINHOOD_TOKEN_KEY` env vars |
| Direct `accessToken` | Serverless, testing, short-lived scripts | Pass `accessToken` to constructor — **no refresh at all** (neither proactive nor on 401); the first 401 raises `TokenExpiredError` |

## Troubleshooting
- **`not_authenticated`**: no tokens in the store — run `bunx robinhood-for-agents onboard`
- **`expired` / `TokenExpiredError`**: tokens exist but are dead and automatic refresh could not recover them. Re-run `onboard` (MCP: `robinhood_browser_login`) — there is no other remedy
- **`unknown`**: the probe failed for a transient/network reason. The session is probably fine — retry before re-authenticating; never re-login on `unknown` alone
- **Worked a minute ago, now 401s**: refresh tokens are **single-use** — each renewal issues a new one and instantly kills the old (and revokes the previous access token). Two clients sharing one session (MCP server + a CLI script, or two Claude Code sessions) will poison each other. The client self-heals by re-reading the token store and adopting whatever the other process persisted, but there is no cross-process lock — close the second process, then re-run `onboard` if it stays broken
- **Back after days away**: renewal only runs while the client is in use. Idle longer than the refresh-token lifetime and the chain lapses — a **new browser login** is required
- **`CRITICAL: refreshed tokens could not be persisted`** in stderr: the rotated refresh token exists only in memory and dies with the process. Fix keychain/`ROBINHOOD_TOKENS_FILE` access, then re-run `onboard`
- **Docker/headless**: Set `ROBINHOOD_TOKENS_FILE` and `ROBINHOOD_TOKEN_KEY` env vars

## Notes
- No credentials (username/password) pass through the tool layer — login happens on the real Robinhood website
- Tokens are stored in the OS keychain via `Bun.secrets` (default) — never on disk in plaintext
- Access-token TTL varies (~6-8.5 days observed) — never assume a fixed number. The client renews twice over: proactively via a pre-request hook ~24h before expiry, and reactively on a 401
- Each renewal rotates the refresh token (single-use) and revokes the previous access token, so a session in regular use keeps rolling forward — but only one client may drive it, and only while it is being used
- The client injects `Authorization: Bearer` headers directly into API requests
