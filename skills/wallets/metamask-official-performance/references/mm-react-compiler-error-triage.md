---
title: React Compiler Error Triage & Coverage Accounting (MetaMask)
impact: HIGH
tags: react-compiler, panicThreshold, error-triage, coverage, babel, build
---

# Skill: React Compiler Error Triage & Coverage Accounting

The React Compiler **fails open**: when it can't compile a component, it silently skips it and ships the unoptimized original. The build stays green, DevTools shows no warning — you just don't get the memoization. Once the compiler is enabled broadly (metamask-mobile#31171 enabled v1.0.0 app-wide), the question stops being "is it on?" and becomes **"what is it actually compiling, and which of its errors are worth fixing?"** This file is the triage playbook. Extension PR metamask-extension#38007 is the reference implementation.

## The `panicThreshold` ladder

`panicThreshold` controls when a compiler diagnostic fails the build instead of silently skipping the file:

| Setting | Build fails on | Use for |
|---|---|---|
| `'none'` (default) | never — every failed file is **silently skipped** | production builds, always |
| `'critical_errors'` | only critical errors (compiler-internal invariant violations) | CI / debug builds, first ratchet target |
| `'all_errors'` | every diagnostic, including unsupported syntax | CI / debug builds, end-state ratchet |

**The ratchet strategy** (extension roadmap): keep production at `'none'` permanently; aim for a *non-production* build that passes at `'critical_errors'`, then at `'all_errors'`. Each ratchet step turns a class of silent skips into a visible, fixable error list. Never enable a non-`'none'` threshold in a release build — one un-compilable file would block the release for an optimization that is optional by design.

## Triage: unsupported syntax vs. legitimate errors

Compiler diagnostics are **not one bucket**. The logger event's `category` field separates them, and the distinction decides whether you act:

- **`category === 'Todo'` → "unsupported."** Syntax or a pattern the compiler *itself* has not implemented yet. There is **no actionable fix on our side** — rewriting working code to appease an unimplemented compiler path is wasted effort and churn. Count these separately, leave the code alone, and re-check after compiler upgrades.
- **Any other category (e.g. `InvalidReact`, `InvalidJS`) → legitimate, actionable.** A real Rules-of-React violation in our code (mutation during render, conditional hooks, side effects in render). Fixing it both unlocks compilation *and* removes a latent correctness bug.

A healthcheck that doesn't make this split is noise: the `Todo` count swamps the actionable list and the team learns to ignore the output. The extension's verbose run at enablement (metamask-extension#38007) is the canonical illustration — of 7,308 files processed: 253 compiled, **31 actionable errors**, **7,024 unsupported** (`Todo`). Without the split that reads as ~7,000 hopeless errors; with it, the team's backlog is 31 files and the rest is the compiler's to burn down across upgrades. The extension's webpack wrapper makes the split in ~10 lines:

```ts
// adapted from metamask-extension development/webpack/utils/loaders/reactCompilerLoaderWrapper.ts
// (mobile equivalent: pass a `logger` in babel-plugin-react-compiler options)
logger: {
  logEvent(filename, event) {
    switch (event.kind) {
      case 'CompileSuccess': record(filename, 'compiled'); break;
      case 'CompileSkip':    record(filename, 'skipped'); break;
      case 'CompileError': {
        const category = event.detail?.options?.category ?? event.detail?.category;
        // 'Todo' = not yet supported by the compiler — no actionable fix on our side
        record(filename, category === 'Todo' ? 'unsupported' : 'error');
        break;
      }
    }
  },
}
```

The extension exposes this as `yarn webpack --reactCompilerVerbose` (per-file ✅/⏭️/🔍/❌ output + summary stats) and `--reactCompilerDebug={all|critical|none}` (maps to `panicThreshold: '<value>_errors'`). On mobile the same taxonomy is available through the Babel plugin's `logger` option or `eslint-plugin-react-compiler` (the lint rule runs the same analysis the compiler does).

## Coverage accounting

Track four buckets — **compiled / skipped / errors / unsupported** — at file and component granularity, with **worst-status-wins per file** (`error > unsupported > skipped > compiled`): a file with five compiled components and one error is an *error file*, otherwise mixed files inflate the compiled count and the number lies to you.

What the buckets tell you:

- **compiled** — your real optimization coverage, minus one gap: a module-scope `'use no memo'` directive still logs `CompileSuccess` for every function in the file before the directive discards the transform, so those files land here too, not in `skipped`. "The compiler is enabled" claims nothing; this number does.
- **errors** — the actionable backlog. Each is a Rules-of-React fix.
- **unsupported** — the compiler's backlog, not yours. Trend it across compiler upgrades.
- **skipped** — intentional exclusions: test/story files and **class components** (never compiled — metamask-mobile#30919 counted 53 at full enablement; migration to function components is the only way to move them into the compiled bucket). A `'use no memo'` directive lands here only when it sits inside one function's body, logging `CompileSkip`. A module-scope one, at the top of the file, logs as `compiled` instead.

## Staged adoption roadmap

The extension's sequence generalizes to any repo:

1. **Lint clean:** update `eslint-plugin-react-hooks` / `eslint-plugin-react-compiler` to latest; fix violations — these are exactly what the compiler will refuse to compile.
2. **Audit opt-outs:** every `'use no memo'` carries a reason + TODO; the count only goes down. `grep -rn "use no memo" app --include="*.ts*"`. A directive can be masking nothing: remove it and re-run the compiler, and zero new errors means it was not load-bearing.
3. **Ratchet `critical_errors`:** non-prod build passes; fix what surfaces.
4. **Ratchet `all_errors`:** remaining actionable errors fixed; what's left is the `Todo` (unsupported) set, which you wait out.

## Verify

- Per component: `Memo ✨` badge in React DevTools (see [js-profile-react.md](js-profile-react.md)).
- Per repo: the compiled-files count from the logger stats rises (or at least doesn't silently fall) release over release, read against the `'use no memo'` opt-out count from the roadmap's audit step. A module-scope directive still logs as `compiled`, so the raw count alone can rise while real coverage doesn't. Silent coverage regressions are the failure mode this file exists to catch.
- After a compiler version bump: re-run the verbose build and diff the `unsupported` list — `Todo`s that became `compiled` are free wins; new `error`s are regressions to triage.

## Don't over-correct

- **Never "fix" a `Todo`.** Rewriting working code around an unimplemented compiler feature is churn with no perf evidence; the next compiler release may compile it as-is.
- Don't gate releases on compiler errors (`panicThreshold` stays `'none'` in production builds).
- Don't treat `skipped` as a problem — tests, stories, and function-body opt-outs belong there (a module-scope `'use no memo'` counts as `compiled`, not `skipped`). The smell is *unexplained* `'use no memo'` directives, not the bucket itself.
- A component without `Memo ✨` is not automatically a bug to chase — check the buckets first; it may be `unsupported`.

## Related

- [mm-react-compiler.md](mm-react-compiler.md) — enabling the compiler in this repo (Babel config, Metro cache, ESLint healthcheck)
- [js-react-compiler.md](js-react-compiler.md) — how the compiler transforms code; Rules-of-React background
- [mm-selector-cascade.md](mm-selector-cascade.md) — what the compiler **cannot** fix: unstable values crossing file boundaries (selectors, imported hooks)
