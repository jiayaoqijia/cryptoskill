---
name: ui-development
description: >-
  UI component development standards for MetaMask clients: the strict
  design-system-first component hierarchy, availability checks before
  building custom components, styling with design tokens, and required
  imports. Use when building, restyling, or reviewing any UI component, or
  when choosing between a design-system, component-library, or custom
  component.
base: true
---

# MetaMask UI Development — MMDS Guidance

Strategy context: [Agentic Design System Strategy](https://github.com/MetaMask/skills/blob/main/domains/ui/knowledge/agentic-design-system-strategy.md)

The MetaMask Design System (MMDS) is the default for MetaMask product UI. This
base holds the rules shared by every client. The repository overlay below it
adds platform paths, the styling surface, and platform-only rules.

## When to use

Use this skill when you create, change, restyle, or review UI in a MetaMask
client: components, screens, sheets, modals, stories, styles, tokens, themes,
and UI behavior. Use it to decide between an MMDS component, a legacy
component-library component, a feature component, and custom UI.

Copy and wording rules live in `content-guidelines`, and file layout and test
setup live in `component-scaffold`, where the repository has them.

## Sources, in order

Work from them in this order. None of these needs an MCP server. The Design
Brain step uses a Notion connector when one can reach the MetaMask workspace.

1. **Installed package types (`node_modules`).** The installed version is the
   contract for the code you are changing. Read the export index and the
   component's `.types` file (with its JSDoc) under
   `node_modules/@metamask/<platform package>/dist/`. Shared prop and enum
   types are declared in
   `node_modules/@metamask/design-system-shared/dist/types/`. Read them
   there, but import components and enums from the platform package. When
   the types disagree with anything else on this list, the types win.
2. **Hosted Storybook components manifest**, for discovery and story
   snippets:
   - React (Extension): <https://metamask.github.io/metamask-design-system/manifests/components.json>
   - React Native (Mobile): <https://metamask.github.io/metamask-design-system/react-native/manifests/components.json>

   The manifests are built from MMDS `main`, so they can list components or
   props that are newer than the version the consumer repo installs. Confirm
   anything you find there against the installed types before you use it.
   Story `import` snippets sometimes pull enums from
   `@metamask/design-system-shared`; in product code, import them from the
   platform package (`@metamask/design-system-react` or
   `@metamask/design-system-react-native`). How to read a manifest:
   [references/reading-mmds-manifests.md](references/reading-mmds-manifests.md).
3. **Design Brain, when Notion is available.** Query
   [Design Brain — Lessons & Rules](https://www.notion.so/b71f86d67d68827395a001f7ee7a8a86)
   for the area you are changing. Apply Active rules (P0 must, P1 should).
   Treat Proposed rules as guidance only. Cite the rule you applied in the PR
   or review, and check the Brain for patterns too. Installed types still win
   on what exists in code. If you have no Notion access, write "Design Brain
   not checked" in the PR or review. Do not skip it silently.
4. **Component README at the installed version's tag.** READMEs are not in the
   npm tarball. Read the installed version from
   `node_modules/@metamask/<package>/package.json` (or the lockfile), then open
   the README on GitHub at the per-package tag
   `@metamask/<package>@<version>`. The package `CHANGELOG.md` compare links
   use the same tag names. Never hard-code a release in code comments or
   skills.
5. **Existing repository usage and stories.** Search the consumer repo for the
   component or token. Treat examples as usage evidence, not as the contract.
6. **Figma MCP and Code Connect, when connected.** Use them to read the design
   and its component mapping. If they are not connected, carry on without them.

## Workflow

**Create:** read the installed types (and README when behavior is unclear)
for each building block, choose the component as below, style with preset
classes and tokens, then run the review checklist on your own diff.

**Review:** list the changed UI, check each MMDS usage for deprecation (see
[Deprecated APIs](#deprecated-apis)), then report component choice, deprecated
usage, tokens, typography, and accessibility findings with file, line,
evidence, and a recommended fix. Say whether Design Brain was checked, or
write "Design Brain not checked".
Custom UI without a recorded reason is a finding, not an automatic failure.

## Choosing a component

- Before building anything, look up the component by name in the manifest
  and the installed exports. For a pattern, use the first place that has it:
  Storybook or the manifest docs, then the Design Brain when Notion is
  available, then the component README at the installed tag, then existing
  repository usage. Never invent a component, a prop, or a variant, and never
  port an API from the other platform or another UI library.
- Choose in this order, and record the reason whenever you go past step 1:
  1. An MMDS component exported by the installed platform package.
  2. A non-deprecated legacy component-library component, only when MMDS does
     not cover the need.
  3. An existing feature component that already solves it.
  4. Custom UI composed from MMDS primitives and tokens, with the reason
     recorded in the PR or the repository's exception format.
- Do not invent button or control chrome that MMDS does not have. Keep
  single-select (checkmark) and multi-select (checkbox) patterns distinct.
- If an MMDS layout makes a primary data point read as secondary, compose a
  stronger treatment instead of forcing the wrong primitive.

## Deprecated APIs

This rule applies to every client. Repository overlays and scaffolds defer to
it.

- Do not add new usage of anything marked `@deprecated` (a component, prop,
  or enum value). Use the replacement its JSDoc or README names when the
  installed platform package exports it, even if the repository still uses
  the deprecated one. If no replacement is exported, keep existing usage and
  record the gap.
- To check, search the component's whole installed folder:
  `grep -rn @deprecated node_modules/@metamask/<platform package>/dist/components/<Name>/`.
  The tag is often on the component declaration (`<Name>.d.cts`), and the
  `.types` file can omit it. A non-empty manifest `jsDocTags.deprecated`, or
  `@deprecated` in the README at the installed tag, is the same signal. An
  empty `jsDocTags` is not evidence that it is current.

## Foundations

- Use preset Tailwind classes first for color, type, shadows, motion, spacing,
  and radius. Tailwind comes from the MMDS presets configured in the consumer
  repo. Use only class names those presets generate, including the 4px spacing
  scale (`p-4`, `gap-2`) and the default radii (`rounded-lg`, `rounded-xl`,
  `rounded-2xl`, `rounded-full`). Do not use default Tailwind colors.
- When Tailwind does not make sense or is not possible (a prop or style
  object, a third-party component, a chart, an animation, or a place that
  needs a CSS variable or theme value), use a semantic token from the
  installed `@metamask/design-tokens` package, in JS or CSS. No recorded
  reason is needed. The overlay says how this platform reads one. Read the
  package README at the installed tag
  `@metamask/design-tokens@<version>`.
- Never use a raw palette value, a hex value, or an arbitrary value
  (`bg-[#...]`, `p-[15px]`, `rounded-[16px]`, `text-[14px]`,
  `borderRadius: 16`).
- Meet WCAG AA contrast (normal text 4.5:1, large text and UI graphics 3:1)
  and check dark mode.
- Layouts must survive longer translated strings and future RTL without
  clipping or overlap. Avoid fixed-width text boxes.

## Typography

- Set type with the design-system text component. Use the font family and
  variant options the installed types expose, and follow the hosted manifest
  and the component README at the installed tag for when each applies. Never
  hand-set font sizes, line heights, or arbitrary text classes.
- Amount inputs have no settled typography pattern yet. Use the font family
  and variant options the installed types expose, and do not invent a
  dedicated amount style.

## Incremental migration: `Legacy*` aliases

When a file imports the same name from a legacy source and from the MMDS
platform package, alias the legacy import with a `Legacy` prefix and keep the
MMDS import on the plain name. Do the same for clashing enums. Leave legacy
imports that have no MMDS counterpart in the same file on their plain names
until that step migrates them. Do not alias legacy names that MMDS does not export, and never put the
prefix on the MMDS import. Finishing the migration is deleting the `Legacy*`
import and its usages. The overlay gives the platform's import paths and an
example.

## Accessibility

A short floor of plain WCAG basics. Design Brain rules are not copied here;
read them from the Design Brain source above.

- Every input has a persistent label. A placeholder is not a label.
  Meaningful icons and icon-only buttons have an accessible name, and
  decorative icons are hidden.
- Never show state with color alone, and expose that state to assistive tech.
  Do not nest interactive controls.
- Announce async status and errors. Overlays and sheets manage focus and keep
  close or back available.
- Respect reduced motion, and meet WCAG AA contrast.

## MMDS agent docs

Read these in the MMDS repository instead of copying them into skills:

- [`.cursor/rules/styling.md`](https://github.com/MetaMask/metamask-design-system/blob/main/.cursor/rules/styling.md)
- [`.cursor/rules/figma-integration.md`](https://github.com/MetaMask/metamask-design-system/blob/main/.cursor/rules/figma-integration.md)
- [`.cursor/rules/component-migration.md`](https://github.com/MetaMask/metamask-design-system/blob/main/.cursor/rules/component-migration.md)

These track MMDS `main`. Where they disagree with the installed types, the
installed types win.

## Review checklist

- [ ] Installed types were read.
- [ ] Every MMDS building block was checked for deprecation, and the
      [Deprecated APIs](#deprecated-apis) rule holds.
- [ ] MMDS was used wherever it covers the need; any step past MMDS has a
      recorded reason.
- [ ] No invented components, props, or variants, and no cross-platform ports.
- [ ] Preset Tailwind classes first. Where Tailwind does not apply, a semantic
      token from the installed design-tokens package. No raw palette values,
      hex, or arbitrary values.
- [ ] Typography uses the design-system text component and the font family
      and variant options from the installed types.
- [ ] Clashing legacy imports are aliased `Legacy*`; MMDS keeps plain names.
- [ ] The accessibility floor above holds for the changed UI.
- [ ] Design Brain was checked for the area that changed, or the PR or review
      says "Design Brain not checked".
