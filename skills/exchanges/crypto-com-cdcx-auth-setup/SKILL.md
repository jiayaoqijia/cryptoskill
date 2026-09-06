---
name: cdcx-auth-setup
description: Credential and profile management — configure API keys via the setup wizard, environment variables, or config file. Resolution order and troubleshooting.
---

# Auth & Profile Setup

## When to Use

- First-time cdcx setup
- Configure multiple profiles (e.g. production + UAT)
- Verify credentials work
- Troubleshoot authentication errors

## Resolution Order

cdcx resolves credentials in this order (first match wins):

1. `--api-key` / `--api-secret` command-line flags
2. `CDCX_API_KEY` / `CDCX_API_SECRET` environment variables (preferred prefix)
3. `CDC_API_KEY` / `CDC_API_SECRET` environment variables (legacy prefix)
4. `~/.config/cdcx/config.toml` profile (default profile, or `--profile <name>`)

## Setup Methods

### Interactive Wizard (recommended)

```
cdcx setup
```

Prompts for API key, secret, and profile name. Writes `~/.config/cdcx/config.toml` with mode 600. Handles migration from the legacy `CDC_` variables.

### Environment Variables

```
export CDCX_API_KEY="your-key"
export CDCX_API_SECRET="your-secret"
cdcx account summary -o json
```

Prefer this for CI or containers where you don't want a config file on disk.

### Config File (manual)

`~/.config/cdcx/config.toml`:

```toml
[profiles.default]
api_key = "your-key"
api_secret = "your-secret"

[profiles.uat]
api_key = "uat-key"
api_secret = "uat-secret"
env = "uat"
```

Must be mode 600 — cdcx refuses to read world-readable credential files.

## Profiles

```
cdcx --profile uat account summary         # Use UAT profile
cdcx --profile default account summary     # Explicit default

CDCX_PROFILE=uat cdcx account summary      # Env var alternative
```

## Environment Selection

Valid `--env` values: `production` (default), `uat`.

```
cdcx --env uat market ticker BTC_USDT
cdcx --env production account summary
```

`--env` is independent of `--profile`. You can override either or both per call.

## Verify

```
# Public call (no auth)
cdcx market ticker BTC_USDT -o json

# Auth check
cdcx account summary -o json

# Verbose — shows which profile / env resolved
cdcx --verbose account summary
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "No credentials found" | No flags, env vars, or config profile | Run `cdcx setup` or export `CDCX_API_KEY`/`CDCX_API_SECRET` |
| HTTP 401 / signature invalid | Wrong key/secret or clock skew | Re-run `cdcx setup`; ensure system clock is within a few seconds of UTC |
| "Permission denied" on config | File mode not 600 | `chmod 600 ~/.config/cdcx/config.toml` or re-run `cdcx setup` (auto-fixes) |
| UAT calls hitting production | `--env` not set on the profile | Add `env = "uat"` to the profile or pass `--env uat` |
| "Withdrawal not enabled" | API key lacks withdrawal permission | Re-issue the key with withdrawal permission in the Exchange web GUI |

## Notes

- Credentials never appear in `cdcx` output or logs. Verbose mode only confirms *which* profile was resolved
- Do not commit `~/.config/cdcx/config.toml` to version control; it is explicitly not git-tracked
- UAT has its own keypair — production keys do not work against UAT and vice versa
