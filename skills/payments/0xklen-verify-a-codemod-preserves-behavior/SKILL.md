---
name: verify-a-codemod-preserves-behavior
description: Use when applying a mechanical rewrite across many files (renames, API migrations, syntax upgrades) — gate the codemod so every touched file still builds and tests green before commit.
---

# Verify a codemod preserves behavior

A codemod edits hundreds of files in one pass, so one bad pattern affects all of them. Run it on a clean tree, require the build and tests green on the result, and make the transformation reproducible.

## Procedure

1. Start from a clean committed tree so the codemod's effect is exactly `git diff`:
```
git status --porcelain    # must be empty
```
2. Dry-run first and count the blast radius:
```
npx jscodeshift -t codemods/rename-call.js --dry --print src/ | rg -c 'rename_call'
```
Refuse to proceed if the file count is far above expectation.
3. Apply to one directory, build, and run that package's tests before the rest:
```
npx jscodeshift -t codemods/rename-call.js src/billing/ && npm run build && npx jest src/billing
```
4. Apply repo-wide, then make the compiler/type checker the gate — it catches the mechanical breaks:
```
npx jscodeshift -t codemods/rename-call.js src/ && npx tsc --noEmit && npm test
```
Python: `python -m compileall -q . && mypy . && pytest -q`.
5. Grep for stragglers the AST rewrite cannot see — string references, dynamic imports, template literals:
```
rg "old_symbol_name" src/    # must return only intended occurrences
```
6. Review the diff statistically: `git diff --stat | tail -1` shows files/lines; `git diff | rg '^[-+]' | wc -l` should be about 2× the edit count. A much larger diff means a formatter or unrelated rule fired.
7. Commit the codemod script and the transformed files together so the change is reproducible; put the exact command in the commit message.

## Pitfalls

- Running a formatter during the rewrite turns a 200-file rename into a 2000-file diff and hides the change. Disable formatting during the rewrite; format in a separate commit.
- Codemods that rewrite strings do not understand reflection. Grep the old name everywhere afterward.
- Skipping the build between directory batches means you discover whole-repo breakage at once with no bisect point.
- A codemod that is not committed cannot be re-run or audited. The script is part of the deliverable.

## Verification

```
npx tsc --noEmit && npm test && git diff --stat | tail -1
```
Passes = `tsc` clean, tests green, and `git diff --stat` lines are about 2× the edits. Report: "codemod touched 148 files, tsc --noEmit clean, suite green, diff stat ≈ 2× edits, script committed."
