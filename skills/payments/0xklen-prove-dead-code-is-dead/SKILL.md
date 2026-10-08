---
name: prove-dead-code-is-dead
description: Use when you want to delete code you believe is unreachable — prove it with runtime coverage plus static reachability over a full run, then delete and confirm tests stay green.
---

# Prove dead code is dead

"Nobody calls this" is a guess until you show no path reaches it. Prove unreachability with coverage over a realistic full run and static reference analysis, then delete in one commit and watch the suite.

## Procedure

1. Build a run that exercises the app broadly — the full test suite plus a short real session (`scripts/smoke.sh`). Dead-code tools only see what runs.
2. Measure coverage of the suspect module over that full run:
```
coverage run -m pytest -q && coverage run --append -m scripts.smoke && coverage report -m --include='src/legacy/*'
```
Zero covered lines in every file of the package is the first signal.
3. Confirm statically that nothing references the symbols:
```
rg -n --type py 'legacy_recompute|LegacyClient' src/ tests/ scripts/
```
Only the definition may match. Any import, string reference or reflection means it is not dead.
4. Check dynamic escape hatches: plugin registries, `getattr(mod, name)`, entry points, config-driven lookups. Search the name as a string, not just as a symbol.
5. Check other repos and services that consume the library — an external caller makes it live even with zero local coverage:
```
gh search code 'legacy_recompute' --owner myorg
```
6. Delete the module in one commit and run the whole suite plus smoke:
```
git rm src/legacy/recompute.py && pytest -q && bash scripts/smoke.sh
```
7. Record coverage of the deleted file dropping to 0 statements and a green suite — that pair is the proof.

## Pitfalls

- Deleting code covered only by tests that call it directly is safe; deleting code reached by a real smoke path is not. Distinguish test-only from production coverage.
- `# pragma: no cover` hides intent, not deadness. A module full of them still needs the reachability argument.
- Reflection and `eval` defeat static search. Grep the string literal across the repo before believing a symbol is unused.
- A feature flag defaulting to off makes code look dead. Search for the flag name and check production config before deleting.

## Verification

```
coverage report --include='src/legacy/recompute.py' && pytest -q
```
Passes = `coverage` reports `0` statements for the removed path and the suite is green. Report: "legacy/recompute.py: 0 coverage over 3400 tests + smoke, no static or org-wide references, deleted, suite green (N passed)."
