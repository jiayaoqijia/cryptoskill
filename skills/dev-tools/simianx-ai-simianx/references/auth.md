# Signing in from an agent

No key in the environment? Sign the user in from the agent. Two ways; both end in an API key for this agent and
nothing else: no website session, no cookie, never the `billing:manage` scope (subscriptions, payments and security
settings stay on the site). The user can revoke the key at any time at https://www.simianx.ai/#api, and every key
created this way is announced to the account's email and listed in its security activity.

All four endpoints are public (no `Authorization` header) and metered per IP (12 calls a minute, 150 a day; the
poll endpoint 60 a minute). Send `X-SimianX-Skill` as usual. Bodies are JSON; answers use the normal envelope.

## 1. Browser link (best when the user is at a computer)

```
POST /v1/auth/link
{"framework": "claude-code",
 "key": {"name": "Claude Code on my laptop", "scopes": ["data:read", "analysis:run", "automation:manage"],
         "daily_points_budget": 50}}
→ 201 {"link_id": "…", "user_code": "K7MP-4R2X", "url": "https://www.simianx.ai/link/K7MP-4R2X",
        "expires_in": 900, "interval": 3}
```

Show the user `url` (and the code, in case they type it). On that page the user signs in, or signs up, and sees
exactly what you asked for: name, scopes, budgets, expiry. They may trim it before approving, or decline. Poll:

```
GET /v1/auth/link/{link_id}?wait=30        # long-poll: returns at once on a decision, else after `wait` seconds
→ {"status": "pending", "user_code": "…", "url": "…", "expires_in": 842}
→ {"status": "approved", "token": "simx_live_…", "key": {…}, "account": {…}, "points": {…}, "limits": {…}, "web": {…}}
→ {"status": "denied"} · {"status": "expired"}
```

`approved` is answered once: the token is deleted the moment you read it. `expired` also covers an unknown link id
and a result that was already collected. A link lives 15 minutes.

## 2. Email code (no browser needed)

```
POST /v1/auth/code
{"email": "ada@example.com", "framework": "codex", "language": "en"}
→ 200 {"sent": true, "email": "a***@example.com", "expires_in": 600, "resend_in": 60}
```

The answer is the same whether or not the address has an account (an address without one becomes an account when
the code is used: verified email, no password; the site's "forgot password" sets one later, and Google / Microsoft /
Discord sign-in works on the same address). One code a minute and five an hour per address. Ask the user for the
6-digit code from the email, then:

```
POST /v1/auth/key
{"email": "ada@example.com", "code": "493028", "framework": "codex",
 "key": {"name": "Codex on CI", "scopes": ["data:read", "analysis:run"], "daily_points_budget": 20}}
→ 201 {"token": "simx_live_…", "key": {…}, "account": {"id", "email", "name", "plan", "created": true|false,
        "language"}, "points": {…}, "limits": {…}, "web": {"keys": "…/#api", "pricing": "…/pricing"}}
```

A wrong code answers 400 `code_invalid` with `attempts_left` (five tries, then the code dies); an old or used one
400 `code_expired`. The `key` object is validated before the code is spent, so a bad request does not cost a code.

### 2-step verification

An account with an authenticator app or a passkey answers the code step with no token:

```
→ 200 {"mfa_required": true, "ticket": "…", "methods": ["totp", "backup_code"], "expires_in": 600}
POST /v1/auth/key {"ticket": "…", "mfa": {"method": "totp", "code": "123456"}, "key": {…}}   → 201 as above
```

Wrong answers return 400 `mfa_invalid` with `attempts_left`; the ticket is single use and lives 10 minutes. An
account whose only second factor is a passkey answers 403 `mfa_unavailable`: use the browser link instead.
Email-only 2-step verification is already satisfied by the code.

### A full plan

Free accounts hold one key. When there is no room, the code step answers 403 `too_many_keys` with `keys` (the
account's active keys), `limit`, a `ticket` and `actions`. Ask the user which key to replace, then:

```
POST /v1/auth/key {"ticket": "…", "key": {"replace_key_id": "<id>", "name": "…"}}   → 201
```

or send them to `actions.change_plan.url`. The ticket lives 10 minutes.

## The `key` object

| Field | Meaning |
|---|---|
| `name` | Label shown on the site (default: the framework) |
| `scopes` | Subset of `data:read`, `analysis:run`, `automation:manage`, `keys:manage` (default: all four). `billing:manage` is refused with 403 `insufficient_scope` |
| `daily_points_budget`, `monthly_points_budget`, `max_points_per_call` | Points; the key stops at the budget, the account does not |
| `expires_at` | ISO 8601 |
| `ip_whitelist` | Up to 50 addresses that may use the key |
| `replace_key_id` | Revoke this key first (full plans) |

## After sign-in

Store `token` where this agent reads its environment: the shell profile, a git-ignored `.env`, or the agent's own
secret store. Say which file you wrote and show only the prefix (`simx_live_abc123…`). Never commit it, never log it,
never paste it into a prompt. Then continue with `GET /v1/me` as in SKILL.md.

## Why no cookie

A website session can change the subscription, the password and the security settings; an agent key cannot. That
line is the design: an agent signs in to a scoped key with budgets, visible and revocable on the site, and the human
keeps the website.
