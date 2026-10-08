---
name: scan-git-history-for-secrets
description: Use when a credential may have been committed, even if it was later deleted. Scans history with gitleaks and trufflehog, rotates first, and only then rewrites history.
---

# Scan git history for secrets

Deleting a secret in a later commit does not remove it from history — anyone who cloned keeps it.
Treat a committed secret as compromised the moment it lands, because the clock on rotation starts at
that commit, not at the cleanup.

## Procedure

1. Scan the working tree and the full history with two independent tools so their rule sets differ:

       gitleaks detect --source . --redact --report-format json --report-path /tmp/gitleaks.json
       trufflehog git file://. --only-verified --json > /tmp/trufflehog.json

2. Search history for a known string directly when you suspect a specific value:

       git log -p -S 'AKIA' --all -- . | rg -n 'AKIA[0-9A-Z]{16}'
       git rev-list --all | xargs -n1 git grep -l 'PRIVATE KEY' 2>/dev/null | sort -u

3. Triage each hit: tool, file, commit, value type, and whether the value is still live.

4. Rotate or revoke the credential *before* touching history. A rewrite that runs first leaves the
   old value valid and un-scanned clones intact:

       aws iam delete-access-key --user-name "$USER" --access-key-id "$KEY"

5. Rewrite history only after rotation, using `git filter-repo` (preferred over `filter-branch`):

       git filter-repo --path env/.env --invert-paths
       # or, for a single string in all files:
       git filter-repo --replace-text <(echo 'literal:OLD_SECRET==>REDACTED')

6. Force-push the rewritten history and have every collaborator re-clone; a stale clone can re-push
   the secret.

7. Prevent recurrence with a pre-commit hook and a server-side check:

       printf '#!/bin/sh\ngitleaks protect --staged --redact\n' > .git/hooks/pre-commit
       chmod +x .git/hooks/pre-commit

## Pitfalls

- `git rm` and a new commit leave the value in `git log -p` forever.
- Rotating the secret but leaving it in an old tag or a fork's `main` still leaks it.
- Secrets baked into CI logs, container layers, or an S3 backup survive a repo rewrite.
- A `.env.example` with real values, or a test fixture with a live key, is a common miss.
- High-entropy false positives (hashes, base64 fixtures) waste rotation effort — check
  `--only-verified` output first.
- Rewriting shared history without coordinating breaks every open branch; announce it first.

## Verification

    gitleaks detect --source . --redact --report-format json --report-path /tmp/g2.json; jq 'length' /tmp/g2.json
    git log --all -p -S "OLD_SECRET" | wc -l

Pass: the gitleaks report is empty and the history search returns 0 lines. Report each secret
found, the commit that introduced it, whether it was rotated, and the hooks now blocking recurrence.
