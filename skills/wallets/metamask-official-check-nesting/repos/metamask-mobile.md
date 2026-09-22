---
repo: metamask-mobile
parent: check-nesting
---

Audit the target component(s) for unnecessary wrapper nesting in JSX. The goal is to reduce native view depth without changing visual output or behavior.

## Input

The user may provide:
- A file path (e.g. `app/components/UI/Bridge/components/TokenSelectorItem.tsx`)
- A component name (e.g. `TokenSelectorItem`) — search for it with Glob
- A folder path (e.g. `app/components/UI/Bridge/`) — audit all `.tsx`/`.jsx` files in that folder recursively
- `--all` or `.` — audit every `.tsx`/`.jsx` file in the entire project
- No argument — audit all files touched in the current git diff (`git diff --name-only HEAD`; compares to last commit only — does not include untracked files)

## Step 1: Locate the file(s)

If a file path was given, read it directly.

If a component name was given, use Glob to find it.

If a **folder path** was given, use Glob with the pattern `<folder>/**/*.{tsx,jsx}` to collect all matching files. If the folder yields more than 20 files, print a warning:
> "Found N files — this may take a while. Auditing in batches of 10. Press Ctrl-C to stop at any time."
Then process them in batches of 10, reading each file before analysing it. After each batch, print a progress line: `[batch X/Y done — N findings so far]`.

If `--all` or `.` was given, use Glob with `**/*.{tsx,jsx}` from the project root. Apply the same batching strategy as the folder mode.

If nothing was given, run `git diff --name-only HEAD` and filter for `.tsx`/`.jsx` files.

Read each file fully before proceeding.

## Step 2: Identify wrapper issues

For each layout wrapper (`<View>`, `<Box>`, or design-system layout components — prioritize these over interactive wrappers like `<Pressable>` unless the user scoped a specific subtree), evaluate **removable patterns** (A–E) and **accessibility pattern** (F) separately.

**Output rules (one finding per wrapper):**
- Among A–E, if multiple patterns match, report only the **most specific** one (e.g. **D** for nested duplicate wrappers; **C** over **A** when only layout props are involved; **B** for empty wrappers).
- Between A–E and F: if the wrapper qualifies under A–E, report only the removal finding; report Pattern F only when it does not qualify under A–E.

### Removable patterns (A–E)

These wrappers can be eliminated or flattened to reduce native view depth:

### Pattern A — Passthrough style wrapper
A wrapper whose only purpose is to apply `style`, `twClassName`, or `className` to a single child, when that child already accepts those props.

```tsx
// BAD — Box only adds flex-row, Pressable accepts style prop directly
<Box twClassName="flex-row items-center gap-1">
  <Pressable onPress={...}>...</Pressable>
</Box>

// GOOD — move style to Pressable
<Pressable onPress={...} style={tw.style('flex-row items-center gap-1')}>
  ...
</Pressable>
```

### Pattern B — Empty or transparent wrapper
A wrapper with no props (or only `key`) that wraps a single child. It adds a native view layer with zero benefit.

```tsx
// BAD
<View>
  <TokenBalance ... />
</View>

// GOOD
<TokenBalance ... />
```

### Pattern C — Layout-only wrapper around a single child that accepts layout props
A wrapper that only sets `flexDirection`, `alignItems`, `justifyContent`, `gap`, `flex`, `padding`, `margin` — and the single child is a design-system component that accepts `style` or `twClassName`.

### Pattern D — Redundant double wrapper
Two consecutive wrappers of the same type where the outer one contributes nothing the inner doesn't already handle (e.g. two nested `<Box>` where the outer has no unique props).

### Pattern E — Wrapper added solely to position sibling-less content
A `<View style={{ position: 'absolute' }}>` or similar wrapping a single absolutely-positioned child when the child itself accepts `style`.

### Accessibility pattern (F)

Pattern F is **not** a removal pattern — it keeps the wrapper and adds `accessible={false}` to reduce accessibility node count.

#### Pattern F — Non-interactive container missing `accessible={false}`
A layout-only wrapper (`<View>`, `<Box>`, or similar) that has no `accessible` prop and is not itself interactive. Adding `accessible={false}` prevents the accessibility tree from treating it as a focusable node, reducing the number of accessibility nodes the screen reader must traverse.

```tsx
// BAD — View is a non-interactive container, adds an unnecessary a11y node
<View style={styles.row}>
  <TokenIcon ... />
  <Text>{label}</Text>
</View>

// GOOD — explicitly excluded from the accessibility tree
<View style={styles.row} accessible={false}>
  <TokenIcon ... />
  <Text>{label}</Text>
</View>
```

Flag a container for Pattern F when **all** of the following are true:
- It has no `testID`, `accessible`, or any `accessibility*` prop (e.g. `accessibilityLabel`, `accessibilityRole`, `accessibilityHint`, `accessibilityState`, `accessibilityValue`, `accessibilityActions`) — these indicate intentional testing/a11y semantics.
- It has no interactive handler (`onPress`, `onLongPress`, etc.).
- It contains child elements with their own accessibility semantics: `<Text>` elements (inherently readable by screen readers), interactive components (`Pressable`, `TouchableOpacity`, buttons, links, or anything with `onPress`/`onLongPress`), or elements with explicit `accessibilityLabel`, `accessibilityRole`, or `accessibilityHint`. Do **not** flag wrappers whose children are purely decorative (e.g. icon-only `<Image>` with no label, `<View>` spacers) and carry no accessible content.
- Multi-child layout containers are a **primary** target for Pattern F (e.g. a row `<View>` with icon + label) — do not skip them because they have more than one direct child.

---

## Step 3: Identify wrappers that MUST stay

### For removable patterns (A–E)

Do NOT flag a wrapper as **removable** if any of the following are true:

- It has `testID`, `accessible`, `accessibilityLabel`, `accessibilityRole`, `accessibilityHint`, or any `accessibility*` prop — these are intentional for testing/a11y.
- It renders **more than one direct child** — removing it would change layout.
- Its style includes properties the child cannot accept (e.g. `borderRadius` on a `Text`, `overflow: hidden` on a `FlatList`).
- The child is a third-party component that does not accept `style` or `twClassName`.
- It is needed for event handling (`onLayout`, `onPress`, `pointerEvents`) that cannot be moved to the child.
- Removing it would change touch target area, z-index, or shadow behavior.
- It applies `marginHorizontal`/`padding` to multiple sibling children (i.e. it is a shared layout container for a subtree with multiple children).

### For Pattern F

Do NOT suggest `accessible={false}` if any Step 2 Pattern F criterion is not met, or if the wrapper qualifies under Patterns A–E (report removal only — see output rules in Step 2).

---

## Step 4: Format findings

Follow the **output rules in Step 2** — one finding per wrapper, using the templates below.

**Patterns A–E (removal) — patterns A, B, C, E:**

```
[PATTERN X] file_path:line_number
  Wrapper: <ElementName prop1 prop2 ...>
  Child: <ChildName ...>
  Why removable: <one sentence>
  Suggested fix: <concise description of what to move where>
```

**Pattern D (redundant double wrapper):**

```
[PATTERN D] file_path:line_number
  Outer wrapper: <ElementName ...>  (the one to remove or flatten)
  Inner wrapper: <ElementName ...>
  Why removable: <one sentence>
  Suggested fix: <remove outer wrapper; what happens to its props>
```

**Pattern F (accessibility):**

```
[PATTERN F] file_path:line_number
  Wrapper: <ElementName prop1 prop2 ...>
  Children: <ChildName ...>, <ChildName ...> (list direct children)
  Why flagged: <one sentence — e.g. non-interactive layout container with no accessible prop; children carry their own a11y semantics>
  Suggested fix: Add accessible={false} to the wrapper (keep the wrapper)
```

Group findings by file. At the end, show a summary table:

```
Files audited:  N
Files with issues: N
Total removable wrappers found (A–E): N
Total accessible={false} suggestions (F): N
Estimated native view depth reduction (A–E removals only; Pattern F does not reduce depth): N levels
```

For folder/project-wide runs, also list the top offending files sorted by finding count:

```
Top files by finding count:
  3 findings — app/components/UI/Foo/Bar.tsx
  2 findings — app/components/UI/Baz/Qux.tsx
  ...
```

If no issues are found in any file, say so clearly — do not invent findings.

---

## Step 5: Ask before fixing

After showing the findings (Steps 1–4), ask the user:
- "Fix all automatically?" → apply all safe fixes, then continue to Steps 6–8
- "Fix one by one?" → walk through each finding interactively, then continue to Steps 6–8
- "Just the report" → **stop here; do not run Steps 6–8**

When fixing, use the Edit tool. Preserve all existing formatting, indentation, and comments. Do not change anything outside the identified wrapper.

**Per-file test gate (during fixing):** After editing a file, run the Step 6 test command for that file and confirm it passes before editing the next file.

**Important constraints when applying fixes:**
- Never replace a named component (e.g. `<Box>`, `<View>`, `<Card>`) with a React fragment (`<>` / `</>`). Fragments do not render a native view and cannot accept style or layout props — replacing a layout component with a fragment changes behavior. If the wrapper must be removed, move its props to the child; if that is not possible, keep the wrapper.
- Only remove a wrapper when the child can fully absorb its props. Otherwise, preserve the wrapper and apply only the safe partial fix (e.g. add `accessible={false}`).

---

## Step 6: Verify tests after fixing

Run this step **only if fixes were applied in Step 5** (skip entirely for "Just the report").

Confirm every modified file passes before Step 7 or Step 8. If you already ran tests per file during Step 5, re-run once for all modified files to confirm nothing regressed.

1. Run the tests scoped to each changed file:
   ```bash
   yarn jest --findRelatedTests <file_path> --coverage --collectCoverageFrom='<file_path>'
   ```

2. Check the results:
   - All existing tests must **pass** — if any test fails, revert the fix for that file and report the failure to the user before continuing.
   - Lines **added or modified in the source file** by the fix should reach **80% line coverage** on those lines. If coverage is below 80%, report it and suggest test cases, but do not write tests unless the user asks. A change that only adds `accessible={false}` may not move coverage — note it and do not block the workflow on coverage for that line alone.
   - Do not proceed to Step 7 (PR) until all modified files pass tests.

3. If a file has no test file yet, report it:
   > "No test file found for `<file_path>` — coverage cannot be verified. Skipping coverage check."

---

## Step 7: Create a pull request

Run this step **only if fixes were applied in Step 5** and the user asks to open a PR. Do so **only after Step 6 passes** for every modified file:

1. **Find the PR template.** Look for it in the standard locations:
   ```
   .github/PULL_REQUEST_TEMPLATE.md
   .github/PULL_REQUEST_TEMPLATE/*.md
   PULL_REQUEST_TEMPLATE.md
   ```
   Read the template file before drafting the PR body.

2. **Fill in every section of the template** using the actual changes made:
   - Reference the ticket/issue if one was mentioned (e.g. `Fixes #<issue>`).
   - In the description section, summarize which wrappers were removed or modified and why (e.g. "Removed 3 unnecessary `<Box>` wrappers in `TokenSelectorItem.tsx`; moved flex layout props directly onto inner components to reduce native view depth.").
   - In the testing section, describe how the changes were verified using the **actual Step 6 results**: tests run, pass/fail status, coverage percentages, and manual smoke-test steps if applicable.
   - Leave sections that are genuinely not applicable marked as `N/A` — do not delete them, as reviewers expect the full template.

3. **Do not invent content.** Only include information that reflects the actual changes in the branch. If a section cannot be filled accurately, mark it `N/A`.

4. Create the PR with:
   ```bash
   gh pr create --title "<title>" --body "<filled template>"
   ```

---

## Step 8: Final summary and risk analysis

Run this step **only if fixes were applied in Step 5**, after Step 6 passes. Run after Step 7 if a PR was created (include the PR URL in the summary). Skip entirely for "Just the report".

Output a structured closing report:

### Changes summary

List every file that was modified with a one-line description of what changed:

```
Modified files:
  app/components/UI/Bridge/components/TokenSelectorItem.tsx
    → Removed 2 passthrough <Box> wrappers; merged flex props onto inner <Pressable>
    → Added accessible={false} to 1 non-interactive <View>
  app/components/UI/Rewards/CampaignsPreview.tsx
    → Removed 1 redundant <Box> inside <Pressable>; moved tw.style() directly onto <Pressable>

Total files modified: N
Total wrappers removed (A–E): N
Total accessible={false} added (F): N
Estimated native view depth reduction (A–E only): N levels
```

### Risk analysis

For each modified file, assess what could be affected and assign a risk level (Low / Medium / High). Use the **highest** applicable level when a file has multiple change types:

```
Risk analysis:
  app/components/UI/Bridge/components/TokenSelectorItem.tsx — MEDIUM
    - Visual: flex layout props moved to child; no change in rendered output expected.
    - Touch: no touch handlers were moved or removed.
    - Accessibility: accessible={false} added to a container with interactive children — verify screen reader focus order.
    - Tests: all passing, 83% line coverage on modified lines.

  app/components/UI/Rewards/CampaignsPreview.tsx — MEDIUM
    - Visual: style merged onto <Pressable>; verify ripple/highlight area matches original.
    - Touch: onPress handler preserved on <Pressable>; touch target area unchanged.
    - Accessibility: no accessibility props were touched.
    - Tests: all passing, 91% line coverage on modified lines.
```

Risk level criteria:
- **Low** — only style/layout props moved to a child that already accepted them; no interactive handlers moved; no accessibility props added or changed.
- **Medium** — props moved onto an interactive element (`<Pressable>`, `<TouchableOpacity>`), or `accessible={false}` added to a container with interactive or labeled children — verify visually and with a screen reader.
- **High** — any change near event handlers, gesture responders, animated values, or components known to be fragile in this codebase.

Always close with:
> "Please do a visual smoke-test of the affected screens before merging."

---

## Context: patterns seen in this codebase

These are real examples of issues fixed in previous PRs for reference:

**perf/bridge-accessibility** — `TokenSelectorItem.tsx`:
- Removed intermediate `<Box>` containers around balance rows; moved flex layout props directly onto the `<View>` or inner component.

**perf/rewards-accessibility** — `CampaignsPreview.tsx`:
- Removed inner `<Box style={...}>` inside `<Pressable>`; moved `tw.style('flex-row items-center gap-1')` to `<Pressable style={...}>` directly.

**perf/assets-accessibility** — `AccountGroupBalance.tsx`:
- A wrapper `<View style={styles.accountGroupBalance}>` was mistakenly removed; it was needed because its children (`WalletHomeOnboardingSteps`, `BalanceEmptyState`) do not accept a `style` prop for horizontal margin.

Use these as calibration: the goal is fewer native view layers, but only where it is safe and the child can absorb the props.
