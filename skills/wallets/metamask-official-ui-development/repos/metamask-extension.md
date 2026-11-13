---
repo: metamask-extension
parent: ui-development
---

# MetaMask Extension overlay

Platform rules for React web UI in `metamask-extension`. The base above covers
sources, component choice, foundations, typography, migration, and the shared
accessibility rules.

## Packages and paths

- Components and enums: `@metamask/design-system-react`. Do not import enums
  from `@metamask/design-system-shared`; that package is listed in the Tailwind
  `content` globs only so its classes are generated.
- Inventory: the
  [React components manifest](https://metamask.github.io/metamask-design-system/manifests/components.json),
  confirmed against `node_modules/@metamask/design-system-react/dist/components/index.d.cts`.
- Deprecation: follow the base Deprecated APIs rule, searching
  `node_modules/@metamask/design-system-react/dist/components/<Name>/`.
- README: read the component README on GitHub at the release tag (READMEs
  are not in the npm package). Take `<installed version>` from
  `node_modules/@metamask/design-system-react/package.json`:
  `https://github.com/MetaMask/metamask-design-system/blob/@metamask/design-system-react@<installed version>/packages/design-system-react/src/components/<Component>/README.mdx`
- Legacy component library: being deprecated in favor of MMDS. Search the
  repo for the existing legacy import. Do not add new usage where MMDS covers
  the need.
- Existing app-level components: use one only when
  `@metamask/design-system-react` has no equivalent. Search the repo for a
  component that already covers the need, and apply the base Deprecated APIs
  rule to it. Prefer MMDS first.
- Search the repo for existing MMDS usage before building custom UI.

Do not apply React Native guidance or APIs (`twClassName`, twrnc,
`accessibilityRole`, or React Native-only components) to Extension.

## Styling surface

- `tailwind.config.js` uses `@metamask/design-system-tailwind-preset` and
  removes the default palette and font sizes. Use only
  classes that configuration generates. If a class is in doubt, check the
  preset source or the built CSS; do not invent one or add a safelist entry.
- Outside Tailwind, read a semantic token as a CSS variable from the installed `@metamask/design-tokens` package. How Extension reads one is in the README at `https://github.com/MetaMask/metamask-design-system/blob/@metamask/design-tokens@<installed version>/packages/design-tokens/README.md` (version from `node_modules/@metamask/design-tokens/package.json`).
- `Box` is the default for layout. Using it makes code easier to move between
  Mobile and Extension. Either `Box` utility props or `className` is fine.
  The utility props exist only on `Box`, they only apply Tailwind class names,
  and they are easier to share across platforms. Read `Box`'s props from the
  installed types.
- Do not add SASS or SCSS. Deleting SCSS rules, files, and `@import` lines
  that your change makes unused is expected.
- Set type with the MMDS `Text` component's variants. Font-size utilities do
  not exist in this config, so `text-[14px]` and similar are always wrong.

## Extension accessibility mechanics

- Icon-only controls need an accessible name. Search fields need an input
  label. Look each control up by name in the installed exports and use the
  accessible-name or label prop declared on its types.
- Announce async errors and status with `role="alert"` or
  `aria-live="polite"` on a container that is already mounted before its text
  changes.
- Expandable controls expose `aria-expanded`; toggles and tabs expose their
  selected or pressed state.
- Follow accessible web practices for anything clickable: a native
  `<button type="button">` for actions and `<a>` for navigation (for example
  through `Box`'s `asChild`), with preset state classes such as
  `hover:bg-hover active:bg-pressed`. Never put `onClick` on a `div` or `span`.
- Preserve the keyboard behavior documented in the component README and
  stories, including focus order and how popovers and modals close.

## Incremental migration paths

Search the repo for the existing legacy imports. Legacy components and legacy
enums often come from different modules. Apply the base `Legacy*` rule to any
legacy component or enum whose name MMDS also exports when the file imports
both. Check the installed MMDS exports to decide. Names MMDS does not export
keep their names. Adjust the `../` depth to the file.

```tsx
// Do: MMDS keeps the plain names. Legacy gets the prefix.
// `Component` and `EnumName` stand for names the file imports from both places.
// `LegacyOnlyEnum` stands for an enum MMDS does not export.
import { Component, EnumName } from '@metamask/design-system-react';
import { Component as LegacyComponent } from '../../<legacy-component-module>';
import {
  LegacyOnlyEnum,
  EnumName as LegacyEnumName,
} from '../../../<legacy-enum-module>';

// Don't: prefix the MMDS import, or leave both on the plain name.
import { Component as LegacyComponent } from '@metamask/design-system-react';
import { Component } from '../../<legacy-component-module>';
```

Prop mapping from legacy to MMDS components is in `MIGRATION.md` at the installed tag. Take `<installed version>` from `node_modules/@metamask/design-system-react/package.json`:
`https://github.com/MetaMask/metamask-design-system/blob/@metamask/design-system-react@<installed version>/packages/design-system-react/MIGRATION.md`

## Exceptions

When custom UI is necessary, use the repository's existing exception
documentation. Do not invent a new annotation format.

## Extension checklist

- [ ] Only classes generated by the Extension Tailwind config; no default
      palette, arbitrary values, or safelist workarounds.
- [ ] `Box` for layout and the MMDS `Text` component for text.
- [ ] No SASS or SCSS added; SCSS made unused by the change is deleted.
- [ ] No new usage of the legacy component library where MMDS covers the
      need; clashing legacy imports are aliased `Legacy*`.
- [ ] Clickable elements are native buttons or links; icon-only controls and
      search fields have accessible names; status changes are announced;
      keyboard behavior still works.
