---
name: secrets-detection
description: Finds hardcoded secrets in any project — API keys (AWS, GitHub, Google, Stripe, Slack), passwords, tokens, private keys, JWTs, database URLs with credentials. Runs a fast regex scan, then triages matches to remove false positives and checks .env/git hygiene. Use when auditing a codebase for leaked credentials or before committing/publishing a repo.
license: MIT
---

# Secrets Detection

## Step 1 — Fast regex scan

```bash
bash scripts/scan.sh <project_root>
```

The script greps the pattern set in `references/patterns.txt` (one ERE regex per line — edit that file to tune, not the script). Output: `file:line:matched line`.

If `grep -rE` is unavailable, replicate manually with `rg -n` using the same patterns file.

## Step 2 — Triage (kill false positives)

For each hit, read the surrounding code and drop it if the value is:

- A placeholder: `example`, `test`, `dummy`, `sample`, `changeme`, `placeholder`, `xxx`, `your_...`, `todo`, `<...>`, `***`, `...`
- In an obvious fixture/mock: paths containing `test/`, `__tests__/`, `fixtures/`, `examples/`, `docs/`, `*.md` code blocks
- A variable reference, not a literal: `API_KEY=$API_KEY`, `password: process.env.PW`
- An intentional canary/honeypot token (look for comments like `canary`, `honeypot`, or a monitoring URL)

Keep — and flag as CRITICAL — anything that looks real: correct prefix + realistic entropy + committed to git history.

## Step 3 — Hygiene checks

```bash
git ls-files | rg -i '\.env($|\.)'          # .env files tracked?
cat .gitignore 2>/dev/null | rg -i 'env|secret|key|pem'   # .env ignored?
git log --all --oneline -S 'AKIA' -- '*.py' 2>/dev/null | head  # leaked keys in history?
rg -n --hidden -g '!*.lock' -g '!package-lock.json' '(BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY)' <root>
```

Report:

1. **Committed real secrets** → CRITICAL. Fix: rotate/revoke immediately (a removed file is not a revoked key), then scrub history (`git filter-repo` / BFG).
2. **Tracked `.env` files** → CRITICAL regardless of content.
3. **Secrets in git history but not HEAD** → HIGH (history is forever on clones/forks).
4. **Placeholder secrets in prod-looking config** → MEDIUM (someone will "temporarily" deploy them).
5. **Secrets handling patterns** — note whether the project uses env vars / secret manager properly, and whether secrets can leak into logs (see also `../data-exposure/SKILL.md`).

## Notes

- Scan binary-free (`-I`) and exclude vendored dirs — the script does this already.
- Encoded secrets (base64, hex blobs near words like `key`, `token`, `secret`) deserve a look: decode and judge.
- `references/patterns.md` documents each pattern, its false-positive profile, and how to add new ones.
