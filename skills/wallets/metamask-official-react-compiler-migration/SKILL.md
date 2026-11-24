---
name: react-compiler-migration
description: Migrate existing files so the React Compiler can optimize them, using react-compiler-marker output as the source of truth. Use when fixing React Compiler bail-outs, working through a react-compiler-marker report, or when the user mentions rcm, compiler failures, "Cannot access refs during render", "Existing memoization could not be preserved", or other compiler diagnostics.
maturity: experimental
---

# React Compiler Migration

Make a file compile. Nothing else. The marker tells you what is broken and, after the edit, whether you actually fixed it.

## When To Use

- A file or directory shows up in a `react-compiler-marker` report, a compiler scan, or a ticket asking to fix its bail-outs.
- A compiler diagnostic such as `Cannot access refs during render` or `Existing memoization could not be preserved` needs fixing.
- The repo has a React Compiler burndown check (such as `yarn lint:react-compiler`) and it fails on your branch.

Not for deciding whether manual memoization is still needed in compiled code; that is a performance question, not a migration.

## Rule

**`react-compiler-marker` is the source of truth.** Run it before the first edit and after every edit. A fix is not done because the reasoning is sound; it is done because the failure count dropped.

It earns that status: it loads the workspace's own `babel-plugin-react-compiler` and runs a real `transformFromAstSync` with `noEmit: false`, failing if codegen fails. It is not a lint pass or a heuristic. It also runs with `compilationMode: "infer"` and `panicThreshold: "none"` — the plugin defaults most apps build with (check your Babel config) — plus `enableTreatRefLikeIdentifiersAsRefs: true`, which the build does not set. That last flag makes the marker stricter than a build using the same `compilationMode` and `panicThreshold`, so a marker-clean file is build-clean when those two match. A build set to `compilationMode: "all"` can still fail a file the marker skipped.

Know the one thing it cannot tell you: the compiled output is generated and thrown away, never executed. If the repo disables the compiler under Jest (metamask-mobile does — see Repo notes), a green test run proves the *source* still behaves, not the compiled version. Codegen is verified; runtime behavior of the memoized output is not. Say so when reporting anything beyond a trivial fix.

Never fix a bail-out by suppressing it. `"use no memo"`, a fresh `eslint-disable`, or deleting the behavior that failed are all non-fixes.

## Workflow

### 1. Baseline

The CLI scans directories, not files, and resolves `babel-plugin-react-compiler` relative to the scanned path — so pass the plugin path explicitly and run from the repo root:

```bash
npx -y react-compiler-marker@0.2.0 \
  --babel-plugin-path node_modules/babel-plugin-react-compiler \
  app/path/to/containing/dir
```

On a checkout whose `.npmrc` sets `offline = true` (metamask-mobile does), `npx -y` fails with `ENOTCACHED`. Install the marker outside the repo and invoke it from there, pinned to one version for the whole migration so counts stay comparable (the patterns here were validated on 0.2.0):

```bash
npm install react-compiler-marker@0.2.0 --offline=false --no-fund --no-audit --prefix /tmp/rcm
node /tmp/rcm/node_modules/react-compiler-marker/bin/cli.js \
  --babel-plugin-path <repo>/node_modules/babel-plugin-react-compiler \
  app/path/to/containing/dir
```

The 0.2.0 entry point is `bin/cli.js`; `dist/cli.js` does not exist and fails with `MODULE_NOT_FOUND`.

Record the failing lines for the target file. If the file does not appear in the failures, there is nothing to do — say so and stop.

Capture the same run with `--format json ... 2>/dev/null` now if you intend to report before/after memo metrics (step 4). A failing file has no `success` entry to compare against later, and reconstructing a baseline afterwards means stashing your work in a dirty tree — not worth it.

The reported count is a **lower bound**, in two ways. A component skipped wholesale (see the ESLint-disable pattern) hides every other diagnostic inside it. One marker pass lists every `finally` and every `throw` in a function, but a value block in the same `try` shows up only on the next run, and so does any construct hidden behind a skipped component.

When a ticket names a line the marker does not flag, trust the marker and say in the report where ticket and compiler disagreed. Counts often *rise* on the next run, and a "2 failure" file can take four rounds. That is progress, not regression; report it as such.

The converse is equally normal: plenty of files are one edit and done. Stop when the marker says zero — do not keep digging for a cascade because this section warned you one was possible.

When a fix reveals a new reason, grep the file for the construct you just fixed before re-running. Sibling copies are the common case, and knowing they exist tells you whether you are two edits from done or twenty.

### 2. Understand before editing

Read the failing lines *and* the code that made someone write them. Suppressions and defensive `try`/`finally` blocks usually encode a real bug someone hit. Preserve that behavior; change only the shape the compiler cannot digest.

Look up the failure in [references/patterns.md](references/patterns.md). Each entry has a validated before/after.

**Some failures should not be fixed, and saying so is a successful outcome.** Check these before editing:

- **Test files.** `*.test.tsx` shows up in reports and gains nothing where the compiler is off under Jest (see Repo notes) — migrating a test optimizes code that never runs compiled. They are also the files most likely to show pruned memo blocks. Skip them.
- **False positives.** Some diagnostics name a rule of React rather than a syntax the compiler cannot lower. Establish the code actually breaks the rule before restructuring anything — `Hooks may not be referenced as normal values` fires on any `use[A-Z]` identifier, including a plain boolean prop.
- **Stale findings.** A row in a scan report can outlive the code it names: the file may already compile. Before editing, re-run the marker on the file's directory (see Baseline for the offline-checkout invocation). If the target file has zero failures and is unchanged since the scan commit, do not edit it and do not open a PR — first confirm the marker still flags a known-bad sibling in the same directory, then report the CompileSuccess counts on the ticket and leave it for a human to close or rescan.
- **Refs read during render to produce output.** A "last good value" ref (keep showing the previous price while the new one loads) or a `useRef(PanResponder.create(...))` read as `.current` in JSX has no behavior-preserving rewrite in a migration pass. Report it for a human. Both shapes still fail with `Cannot access refs during render` on a minimal reproduction with marker 0.2.0 and compiler 1.0.0.
- **Fixes that live outside the file.** If the only real fix is renaming an export, changing a shared hook, or editing another team's module, stop and report it with the suggested change. A local workaround for a non-local cause is worse than the bail-out.

Report these as findings with the reason and the suggested owner, and move to the next file.

### 3. Edit

Follow the principles below. Make **one** change at a time and re-run — the marker is cheap, and it is the only way to learn which specific construct the compiler objected to. Guessing at two fixes at once wastes the signal.

### 4. Verify

Re-run the exact command from step 1. Confirm the file's failures are gone and no new failures appeared elsewhere in the directory.

Zero failures is necessary, not sufficient. Add `--format json` and read the per-function counts: `memoBlocks` and `memoValues` are what the compiler managed to memoize, and `prunedMemoBlocks` / `prunedMemoValues` are what it had to discard. A file can compile with zero failures and still be partly de-optimized, which is the actual thing the migration is for.

The CLI writes progress to stderr, so redirect it or the output will not parse:

```bash
npx -y react-compiler-marker@0.2.0 \
  --babel-plugin-path node_modules/babel-plugin-react-compiler \
  --format json app/path/to/dir 2>/dev/null
```

Expect `prunedMemoBlocks` and `prunedMemoValues` to be `0` on a finished file — a fix that clears the failure while pruning memo blocks is not a win.

A file that was failing has **no** `success` entry, so its "before" `memoBlocks` is undefined rather than zero. Do not go stashing changes to reconstruct it: either capture the JSON in step 1 before your first edit, or report before-metrics as N/A and give the after-figures alone. Ignore test files here; they routinely show pruning and gain nothing from being migrated. Then:

```bash
yarn prettier --write <file> && yarn eslint <file> && yarn jest <dir>
```

Add the project type check (`yarn lint:tsc` in metamask-mobile) when the change has type surface — a new helper signature, a changed parameter type, a `Pick<...>`. It checks the whole project and takes about a minute, so skip it when the diff is purely statement-level (relocating a `finally`, hoisting a `const`) and say that you did.

Lint passing does not mean types pass, so do not let ESLint stand in for the type check. All three matter. A compiler-clean file with a new ESLint error is not done — if the repo still enforces `react-hooks` rules, keep the `useMemo`/`useCallback` the linter asks for even where the compiler makes them redundant. Stripping manual memoization is a separate codemod for after the migration, not part of it.

If failures remain, go back to step 2 — do not report a partial fix as done.

### 5. Report

State the diff, why the original code existed, what behavior is preserved, and the before/after failure counts. Flag any new type assertion or behavioral risk for review rather than burying it.

Give the change a risk tier, because a reviewer cannot infer it from a green checklist — every fix in this skill produces the same "0 failures, tests pass" line regardless of blast radius:

- **Rename-level** — a swap to an existing API, or hoisting an expression into a `const`. Behavior is unchanged by construction.
- **Structural** — control flow moved: `finally` relocated, a `try` reshaped, a helper extracted from a hook. Behavior is preserved by an argument you should state, and the argument is what the reviewer checks.
- **Stateful** — anything touching a cache, a ref's lifetime, or memo dependencies that decide when work re-runs. Name the screen to smoke-test, and remember Jest ran this code *un*compiled.

## Principles

These outrank compiler-satisfaction. A file that compiles but reads worse is a failed migration.

1. **`let` is a smell.** Reassignment means the reader has to track a variable through the function. Prefer a `const` with a ternary, an extracted function with early returns, or a derived value.
2. **Minimum diff.** Change the lines the compiler objects to. Do not reformat, rename, reorder imports, or "improve" untouched code in the same pass. Most of the compiler's restrictions are lexical — they care where a construct is *written*, not what runs — so the fix is usually to move that construct behind a helper, not to restructure the logic around it. A new branch the pattern entry does not prescribe means you took the wrong route. The run-once guard and the render-time previous-key check are prescribed branches; leave them.
3. **Look for the existing API before writing one.** The construct the compiler rejected is rarely unique to this file, and the library that supplied it often ships a hook that already hides it (`useAnimatedValue` for `useRef(new Animated.Value(x)).current`). Grep for the candidate first: with precedent in the repo it is a one-line rename and the smallest possible diff; without precedent, it is a new API in a migration pass and belongs in the report.
4. **Extract freely.** A closure or a plain function above/below the component is cheap and usually clearer than inlined branching. Module scope is also outside the compiler's analysis, which makes it the escape hatch for syntax the compiler rejects. Split at a seam that already exists — a helper needing ten parameters means you cut in the wrong place. Match the file's existing naming; a fresh `alert` or `data` parameter can trip lint rules the file was already avoiding. A helper that calls a hook is a hook: name it `use...`. Reuse the existing props type for its parameters instead of inventing an interface, and check the name does not shadow an import or an existing helper. Move the body verbatim so the diff reads as a relocation. Before extracting, search the file for `ONLY_INCLUDE_IF`. If the code you are moving sits inside one of those fences, keep the helper inside the same fence (metamask-mobile strips them; see Repo notes).
5. **Stay in the file.** No new files unless the user asks. Do not edit the upstream hook or shared util to fix a local bail-out.
6. **No comments by default.** No JSDoc on new functions, no comment restating the next line, and no comment on a helper saying it exists for the compiler or naming the diagnostic. Put that context — why the helper was extracted, which diagnostic forced it — in the commit message and PR body, where reviewers read it and it does not rot. Delete comments that described a suppression you removed. Keep a comment only when deleting it would make a correct-looking simplification wrong. A comment that a helper exists for the compiler does not qualify.
7. **Extraction moves code out of a restricted region; it never changes what that region covers.** Shrinking the span of a `try`, a `catch`, or an effect is a behavior change wearing a refactor's clothes. If the compiler-friendly shape genuinely cannot cover the same span, say so instead of shipping it quietly. There is exactly one enumerated exception: converting a `finally` into a trailing statement, which *does* shrink a protected region and is permitted only when both preconditions in the try/catch pattern entry are cleared and stated. Anything else that narrows a protected span is a finding, not a fix.

## When `yarn lint:react-compiler` fails

Some repos gate compiler regressions in CI with a checked-in burndown baseline of known failures per file (proposed for metamask-mobile as `yarn lint:react-compiler`; check `package.json`). If the repo has one:

- A new failing file, or a higher count for a listed file, fails the check. Fix it with this skill; do not suppress it.
- A file you improved must leave the baseline: run `yarn lint:react-compiler --update` and commit the shrunk baseline with the fix.
- Never grow the baseline to make the check pass. After `--update`, read the baseline diff. Commit it only when every changed count went down or a file disappeared. If any count rose or a new file appeared, revert the baseline and fix that file instead.

If the repo has no such script, the marker run in step 4 is the check.

## Repo notes: metamask-mobile

- The compiler is off under Jest: `scripts/react-compiler.js` gates on `NODE_ENV === 'test'`.
- `.npmrc` sets `offline = true`; use the temp-prefix marker install from step 1.
- ESLint still enforces `react-hooks`, so keep the `useMemo`/`useCallback` deps it asks for.
- Code inside `///: BEGIN:ONLY_INCLUDE_IF(...)` fences is stripped in some builds; keep extracted helpers inside the fence their imports live in.
- Type check: `yarn lint:tsc` (whole project, about a minute).

## Patterns

One entry per validated failure reason, with before/after: [references/patterns.md](references/patterns.md).

Append a new entry only after a fix has been verified by the marker and accepted in review. An unvalidated pattern is worse than no pattern.
