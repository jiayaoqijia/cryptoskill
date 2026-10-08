---
name: scope-tool-permissions-to-least-privilege
description: Use when you grant an agent or tool access to files, shell, network, or APIs. Give each capability the narrowest scope that completes the task, default-deny, and verify the grant is not wider than it reads.
---

# Scope tool permissions to least privilege

An injected instruction can only act through the permissions you already hold. This skill shrinks every grant to the task at hand so a successful injection finds the doors locked, and makes over-granting visible.

## Procedure

1. Enumerate the task's actual capabilities in one list: read these files, run this command shape, call this host, write that directory. Everything else is revoked.

2. Default-deny. Start from nothing and add: file paths as explicit prefixes (`/Users/jay/project/data/`), commands as an allowlist (`git`, `pytest`), hosts as a set, never a wildcard.

3. Prefer read to write where both would work. A tool that only reads cannot exfiltrate by overwriting a cron job or `authorized_keys`.

4. Constrain shell by shape, not by blocklist: allow `git status`/`git diff` rather than any `git`, and never `sh -c "$UNTRUSTED"`.

5. Scope credentials: a token should carry the minimum scope and shortest TTL. A read-scoped token turns an exfil attempt into a 403 rather than a dump.

       curl -s -H "Authorization: Bearer $TOK" "$API/self" | jq '{scopes,exp}'

6. Re-verify the effective permission set, not the intended one: `ls -la` on the target dirs, `sudo -l` for privilege, and the token's own introspection endpoint.

7. Review on a cadence; access that outlives a task is over-grant. Log every elevation with who, why, and the expiry.

## Pitfalls

- `chmod 777` and "just add sudo" are the fastest way to make an injection powerful.
- Path prefix logic without a trailing separator (`/data` matching `/database`) grants more than intended.
- API keys with full scopes pasted into a tool config are a standing grant to any injection.
- Blocklisting dangerous commands fails on encodings; allowlisting the permitted ones does not.

## Verification

    sudo -lN && ls -ld "$TARGET_DIR" && curl -s -H "Authorization: Bearer $TOK" "$API/self" | jq -r .scopes

Report: "granted scopes <list>; effective check shows no wider than <list>; denied-by-default confirmed for <capabilities>."
