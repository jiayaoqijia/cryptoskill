---
name: verify-a-write-actually-landed
description: Use when you changed an external system, file, or remote record. Read the exact target back and compare byte for byte before claiming the change succeeded.
---

# Verify a write actually landed

A successful tool call is not a successful change. This skill reads the target back after every mutation, so "I updated it" means the new value is really on disk or in the remote.

## Procedure

1. Before writing, note the target's identity: file path, row key, URL, or commit sha.

2. Note the prior value so a no-op write is detectable: `git rev-parse HEAD`, or `psql -c "select count(*) from users"`.

3. Perform the write with one tool call.

4. Read the same target back immediately, by a fresh route if possible:
   - file: `read_file(path)` and confirm the exact line.
   - git: `git log --oneline -1` and `git show --stat HEAD`.
   - HTTP: `curl -s https://host/resource | jq .field`.
   - database: `psql -c "select field from t where id=42"`.

5. Compare the read-back to the intended value byte for byte. Report the read-back, not the write tool's own success message.

6. For a pushed commit, confirm the remote moved: `git push` then `git ls-remote origin main`.

7. If the read-back does not match, treat the write as failed and retry or investigate; never report done on the write's echo alone.

## Pitfalls

- Caches and replicas serve stale reads; read from the primary or add a cache-busting query parameter.
- A write to staging does not prove production changed; verify the same identity you meant to touch.
- Eventual consistency means one immediate read may lag; re-read after the documented propagation delay.
- A commit without a push leaves the remote unchanged; always confirm with `git ls-remote`.
- Some APIs return 200 and still reject the payload; only the read-back tells you.

## Verification

    git ls-remote origin main | cut -c1-7   # must equal local `git rev-parse --short main`

Report the read-back value and the command that produced it; never the write tool's echo alone.
