---
repo: metamask-mobile
parent: pr-readiness-check
---

# PR Readiness Check

Scan the current branch diff for common issues that could be flagged during PR review. This is a **non-blocking** check — always report findings as warnings and let the user decide what to act on.

## Steps

1. **Collect the diff**

   ```bash
   git diff main...HEAD --name-only
   git diff main...HEAD
   ```

2. **Check for missing tests**

   For each new or modified source file with non-trivial logic changes (not just config, docs, or styles), check whether a corresponding test file was added or updated.

   Prefer layers per the Mobile testing-layers policy (testing domain `knowledge/testing-layers.md`, installed beside `mobile-testing`):
   - **Screens / views / UI behavior via app state** → prefer `Foo.view.test.tsx` (component-view). Warn if the only new coverage is a broad `Foo.test.tsx` that renders the whole screen and mocks hooks/selectors.
   - **App-to-controller flows / controller behavior with I/O isolated** → prefer `Foo.integration.test.ts` (integration) exercised through a domain harness. Warn if such a flow is only covered by mocking the controller in a CV or unit test.
   - **Pure logic / helpers / narrow contracts** → `Foo.test.ts(x)` is appropriate.
   - **CV cannot cover yet** → accept a focused unit test, but warn if the PR does not note why CV was not used.
   - **Device journeys** → Appium only (`tests/smoke-appium/`), and only when CV + integration cannot cover.

   Heuristic: a source file `Foo.ts(x)` should have matching `Foo.view.test.tsx` (for screens/views), `Foo.integration.test.ts` (for app-to-controller flows), and/or `Foo.test.ts(x)` (for allowed unit cases). Warn if:
   - New exported functions/components have no corresponding test file changes
   - Existing test files were not updated despite significant logic changes in the source
   - A new or significantly changed screen only gained a broad unit screen test instead of a component-view test

3. **Check for missing JSDoc**

   Scan new exported functions, types, and components in the diff. Warn if any lack JSDoc comments.

4. **Check for guideline violations**

   Look for obvious violations of `.github/guidelines/CODING_GUIDELINES.md` and `.cursor/rules/` patterns in the changed lines:
   - `any` type usage in TypeScript
   - `StyleSheet.create()` in new code
   - Raw `View` or `Text` imports from `react-native` instead of design system `Box`/`Text`
   - `import tw from 'twrnc'` instead of `useTailwind()` hook
   - `npx` usage in scripts

## Output

Print each finding as a warning line:

```
⚠ No tests detected for new logic in `app/core/Foo.ts`
⚠ Missing JSDoc on exported function `calculateFee` in `app/util/fees.ts`
⚠ `any` type used in `app/components/Bar.tsx:42`
⚠ `StyleSheet.create()` found in new file `app/components/Baz/Baz.tsx`
```

If no issues found, confirm:

```
✅ No readiness issues detected
```
