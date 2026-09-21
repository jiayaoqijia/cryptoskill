# Pattern Reference

Each pattern in `patterns.txt`, what it catches, and its false-positive profile.

| Pattern | Catches | False positives | Notes |
|---|---|---|---|
| `AKIA[0-9A-Z]{16}` | AWS access key IDs | Rare | Verify with `aws sts get-access-key-info` if creds available; secret keys are useless alone but presence = leak |
| `gh[pousr]_...` | GitHub PATs (p=classic, o=OAuth, u=user, r=refresh) | Rare | |
| `AIza...` | Google API keys | Sometimes test keys in docs | |
| `sk_live_...` / `rk_live_...` | Stripe secret/restricted keys | Rare — `pk_live_` is publishable but flag anyway | `_test_` variants → downgrade to LOW |
| `xox[baprs]-...` | Slack tokens | Rare | |
| `SG\.\w+\.\w+` | SendGrid keys | Rare | |
| `eyJ...` | JWTs | Test tokens everywhere | Check payload (`cut -d. -f2 | base64 -d`) for real subjects/expiry |
| `-----BEGIN ... PRIVATE KEY-----` | Private keys | Test fixtures | CRITICAL if committed for real |
| `(db|proto)://user:pass@` | Creds in connection strings | docker-compose dev defaults | `postgres://postgres:postgres@` in compose = LOW; real host = HIGH |
| `APP_KEY=base64:...` | Laravel application keys | Old tutorials/tutorials-committed .env | Not a provider cred, but exposure = cookie forgery → RCE chain; Critical |
| Generic assignment | `password = "..."` style | Very noisy | Always triage; require plausible entropy + non-placeholder |

## Adding a new pattern

1. High precision beats high recall — a pattern that fires on every line trains people to ignore output.
2. Add it to `patterns.txt` with a one-line comment.
3. Add a fixture file under `evals/fixtures/` containing one true positive (and, ideally, one near-miss that must NOT match).
4. Document it in the table above.
