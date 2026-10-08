---
name: scope-per-tool-permissions-least-privilege
description: Use when granting an agent access to tools, files, or network. Give each tool the narrowest scope that completes its job, and revoke the rest.
---

# Scope per-tool permissions to least privilege

An agent inherits whatever the process allows, so a write bug becomes a write-anywhere bug. Grant permissions per tool, scoped to the exact resource, and keep the default deny.

## Procedure

1. Enumerate the run's tools and, for each, the single resource it needs: `db_read -> customers (SELECT)`, `file_write -> out/report.csv`.
2. Write the grant list explicitly; anything absent is denied. Default-deny, allow by exception.
3. Scope filesystem access to a subtree and a mode: `out/:rw`, `src/:ro`. Never grant `/` or `$HOME`.
4. Scope database access to schema verbs: `SELECT` for readers, `INSERT` on one table for writers — never `ALL` or `GRANT`.
5. Scope network egress to named hosts when the tool only needs a few: `api.internal:443`, not `0.0.0.0/0`.
6. Give each tool its own credential with the least role, not a shared admin token that every tool can borrow.
7. Re-derive the grant list per run from the brief; do not copy last run's permissions wholesale.
8. Audit weekly: list grants actually exercised from the action log and remove the ones never used.
9. Treat a permission error as a design signal, not an obstacle to widen away — decide whether the step should exist.

## Pitfalls

- Granting `sudo` or a root token "so the agent is not blocked", which removes every other control at once.
- Sharing one credential across tools, so an audit cannot tell which tool did what.
- Scoping to a directory but forgetting mode, giving read-only tasks the ability to delete.
- Copying a previous run's broader grants because re-deriving them is tedious.
- Leaving a grant in place after the tool is retired, accumulating latent access.
- Widening a scope to fix one denied call instead of fixing the call's resource target.

## Verification

```bash
python3 tools/audit_grants.py runs/grants.json notes/action.log
# fails on any exercised path outside the declared scope, and lists unused grants for removal
```

Report each tool, its declared scope, and any access the run attempted outside it.
