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
| `sk-ant-api03-...` | Anthropic API keys | Notebooks, Colab exports | Billing abuse; check org spend logs after rotation |
| `hf_...` | Hugging Face tokens (fine-grained, org-scoped) | ML scripts, demo notebooks | `write` scope = model-repo poisoning, not just quota |
| `gsk_...` | Groq API keys | Config blobs | Quota theft |
| `sntrys_...` | Sentry auth tokens | CI/CD env blobs | Sentry API access (org data, releases) |
| `nfp_...` | Netlify personal access tokens | Static-site CI | Site takeover-grade |
| `sk-or-v1-...` | OpenRouter API keys | AI app configs | Spend abuse + model access |
| Generic assignment | `password = "..."` style | Very noisy | Always triage; require plausible entropy + non-placeholder |
| Unquoted key=value | `spring.datasource.password=prod-pass` in `.properties`/`.conf`/`.env` lines | Anchored (key=value at EOL), still triage | Catches properties-style creds the quoted patterns structurally cannot |

## Adding a new pattern

1. High precision beats high recall — a pattern that fires on every line trains people to ignore output.
2. Add it to `patterns.txt` with a one-line comment.
3. Add a fixture file under `evals/fixtures/` containing one true positive (and, ideally, one near-miss that must NOT match).
4. Document it in the table above.
