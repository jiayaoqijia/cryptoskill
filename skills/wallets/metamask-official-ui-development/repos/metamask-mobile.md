---
repo: metamask-mobile
parent: ui-development
---

# MetaMask Mobile overlay

Platform rules for React Native UI in `metamask-mobile`. The base above covers
sources, component choice, foundations, typography, migration, and the shared
accessibility rules.

## Packages and paths

- Components and enums: `@metamask/design-system-react-native`. Do not import
  enums from `@metamask/design-system-shared`, and never import MMDS through a
  repository-relative path.
- Tailwind: `@metamask/design-system-twrnc-preset`, through `useTailwind()`.
- Inventory: the
  [React Native components manifest](https://metamask.github.io/metamask-design-system/react-native/manifests/components.json),
  confirmed against `node_modules/@metamask/design-system-react-native/dist/components/index.d.cts`.
- Deprecation: follow the base Deprecated APIs rule, searching
  `node_modules/@metamask/design-system-react-native/dist/components/<Name>/`.
- README: read the component README on GitHub at the release tag (READMEs
  are not in the npm package). Take `<installed version>` from
  `node_modules/@metamask/design-system-react-native/package.json`:
  `https://github.com/MetaMask/metamask-design-system/blob/@metamask/design-system-react-native@<installed version>/packages/design-system-react-native/src/components/<Component>/README.md`
- Existing app-level components: use one only when
  `@metamask/design-system-react-native` has no equivalent. Search the repo
  for a component that already covers the need, and apply the base
  Deprecated APIs rule to it. Prefer MMDS first.
- Search the repo for existing MMDS usage before building custom UI.

Do not apply React web guidance (`className`, HTML tags, `aria-*` props) to
Mobile.

## Styling surface

- Use `const tw = useTailwind();`. Never `import tw from 'twrnc'`.
- `Box` is the default for layout. Using it makes code easier to move between
  Mobile and Extension. Use the MMDS `Text` component for text.
- Either `Box` utility props or `twClassName` is fine. The utility props exist
  only on `Box`, they only apply Tailwind class names, and they are easier to
  share across platforms. Read which props exist from `Box`'s installed types.
  When a style has no utility prop (radius, for example), use a class such as
  `twClassName="rounded-xl"`.
- Outside Tailwind, read a semantic token in JS from the installed `@metamask/design-tokens` package, through the app theme. How Mobile reads one is in the README at `https://github.com/MetaMask/metamask-design-system/blob/@metamask/design-tokens@<installed version>/packages/design-tokens/README.md` (version from `node_modules/@metamask/design-tokens/package.json`).
- No `StyleSheet.create()` and no new `.styles.ts` files. Inline style objects
  only for truly dynamic values.
- When you change a component that uses `useStyles` with a `*.styles.ts`
  file, move its styles to `Box` utility props or `twClassName`, then delete
  the styles file and the `useStyles` call.
- Pressed state: the design-system base button takes a function in
  `twClassName` that receives the pressed flag. Its `style` prop is a plain
  style, so a `style={({ pressed }) => ...}` function does not type-check.
  Look the base button up in the installed exports. For a custom `Pressable`,
  use `tw.style()` in its style function.

```tsx
// On the design-system base button:
twClassName={(pressed) => `w-full ${pressed ? 'bg-pressed' : 'bg-default'}`}

// On a custom Pressable:
<Pressable
  style={({ pressed }) => tw.style('w-full flex-row', pressed && 'bg-pressed')}
/>
```

- Interactive list rows: when the design-system list item component exposes
  an interactive mode, it applies the pressed background itself, so do not add
  `bg-pressed` again. Read the mode from its installed types. Keep the row's
  own horizontal padding; do not add an outer pad that double-indents it.

## Sheets

- Use the design-system bottom sheet and its header and footer parts. Look
  them up in the installed exports or the manifest. The sheet already sets its
  surface token; override it only when the design puts the sheet on another
  surface.
- A `ScrollView` inside a design-system bottom sheet must come from
  `react-native-gesture-handler`. The React Native `ScrollView` does not scroll
  inside the sheet on Android.
- Use the full sheet composition (overlay, container, header, footer, safe
  areas, drag, keyboard, accessibility). In nested sheet flows, keep the
  container stable, move content directionally, use back for the child and
  close for the whole flow, and avoid two systems fighting over height or drag.
- Mobile mounts a single design-system toaster at the app root; search the
  repo for it. Show toasts through the API that toaster exposes (look it up
  in the installed exports); do not mount another toaster.

## Mobile accessibility mechanics

- Custom pressables set `accessibilityRole`, `accessibilityState` (`disabled`,
  `selected`, `checked`, `busy`, `expanded`), and an `accessibilityLabel` or
  `accessibilityHint` when visible text is not enough. Prefer design-system
  controls over a `View` with `onPress`.
- Headings pass `accessibilityRole="header"`. Check the default role on the
  MMDS `Text` component's installed types instead of assuming one. A
  tappable heading is a button.
- Tabs use `accessibilityRole="tab"` with `accessibilityState={{ selected }}`.
- Announce async errors and status with
  `AccessibilityInfo.announceForAccessibility` (iOS VoiceOver ignores
  `accessibilityLiveRegion`), and give inline error text
  `accessibilityRole="alert"`.
- Touch targets are about 44×44 (minimum 24×24). Use `hitSlop` or padding when
  the visible control is smaller.
- Support Dynamic Type: no fixed-height text boxes or absolute layouts that
  clip or overlap as text grows.
- Wire skeletons and other motion to `useReducedMotion()` so they stop when
  Reduce Motion is on.

## Incremental migration paths

Legacy app-level components have no single barrel. Each is a default export
from its own folder. Search the repo for the existing import. Apply the base
`Legacy*` rule to a default export whose name MMDS also exports, and to named
enums whose names are identical in both. Similar but different names do not
clash, so do not alias them. Check the installed MMDS exports to decide.
Adjust the `../` depth to the file.

```tsx
// Do: MMDS keeps the plain names. Legacy gets the prefix.
// `Component` and `EnumName` stand for names the file imports from both places.
import { Component, EnumName } from '@metamask/design-system-react-native';
import LegacyComponent, {
  EnumName as LegacyEnumName,
} from '../../../<existing-app-component>';
```

Prop mapping from legacy to MMDS components is in `MIGRATION.md` at the installed tag. Take `<installed version>` from `node_modules/@metamask/design-system-react-native/package.json`:
`https://github.com/MetaMask/metamask-design-system/blob/@metamask/design-system-react-native@<installed version>/packages/design-system-react-native/MIGRATION.md`

## Mobile checklist

- [ ] `useTailwind()`; no `twrnc` import, `StyleSheet.create()`, or new
      `.styles.ts`.
- [ ] `Box` for layout and the MMDS `Text` component for text.
- [ ] Pressed styles via the base button's `twClassName={(pressed) => ...}` or
      `Pressable` + `tw.style()`.
- [ ] `ScrollView` inside a design-system bottom sheet comes from
      `react-native-gesture-handler`.
- [ ] Controls, headings, and tabs expose roles and state; errors are
      announced; touch targets are large enough.
