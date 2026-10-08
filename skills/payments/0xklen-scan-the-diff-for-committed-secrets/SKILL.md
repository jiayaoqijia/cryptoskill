---
name: scan-the-diff-for-committed-secrets
description: Use when reviewing any PR that touches config, environment, or connection setup. Scans the added lines for keys, tokens, and credentials, and requires rotation rather than deletion.
---

# Scan the diff for committed secrets

A secret pushed in a commit is compromised the moment it reaches the remote, even to a private branch, even if a later commit deletes it. Deletion hides it; only rotation fixes it.

## Procedure

1. Scan the added lines of the diff specifically, so you ignore historical noise: `git diff origin/main...HEAD | grep -nE '^\+' | gitleaks detect --no-git --pipe` — or run gitleaks across the range: `gitleaks detect --source . --log-opts origin/main..HEAD`.
2. Also read the added lines by eye for the shapes scanners miss: an `Authorization: Basic ...` header, a `postgres://user:pass@host` DSN, a private key block (`-----BEGIN ... PRIVATE KEY-----`), a `.env` file added to git.
3. If a secret is found, the required action is rotation, not removal. Removing the line leaves the value in git history and in every clone and fork.
4. Confirm the file that held it is gitignored going forward: check `.gitignore` covers `.env`, `*.pem`, `credentials.json`, and the service account directory.
5. Verify the fix moves the value to the secret store the app reads at runtime (env var injected by the platform, Vault, AWS Secrets Manager), not to another file in the repo.
6. Check CI logs and build artifacts too: `git diff -- '**/.github/**'` for echo'd secrets or a debug step printing env.
7. Block the merge and open an incident for rotation if the secret was ever pushed to a shared remote.

## Pitfalls

- Deleting the line in a follow-up commit and calling it fixed, while history keeps the key.
- A `--force` push that rewrote history but left the key valid for anyone who already fetched.
- Rotating the credential without checking who else holds it (a webhook, a mobile build), so production breaks.
- Trusting the scanner's silence: high-entropy random strings are missed, and a low-entropy password like `hunter2` is not scored at all.

## Verification

    gitleaks detect --source . --log-opts origin/main..HEAD --redact --exit-code 1
    git log --all -S 'BEGIN RSA PRIVATE KEY' --oneline   # history-wide, not just the diff

A pass is a clean gitleaks run and no key material in `git log --all`. If anything was found and pushed, report it as a rotation incident, never as a removed line.

## Worked example

A commit adds `.env` containing `STRIPE_SECRET_KEY=sk_live_...`. gitleaks flags it. Deleting the file in a new commit does not help — the key is in history and in every CI cache. The response: rotate the key in the Stripe dashboard, add `.env` to `.gitignore`, move the value into the platform secret store, and confirm the old key now returns 401.

A secret that was found in a local-only commit still needs rotation if the branch was ever shared: forks and clones carry the objects regardless of the remote.
