---
repo: metamask-mobile
parent: component-scaffold
---

# Component Scaffold — MetaMask Mobile

## 1. Where to put the component

| Scope | Location |
|-------|----------|
| Shared across features | `app/components/UI/<Feature>/` |
| Feature-internal composite | `app/components/UI/<Feature>/components/<ComponentName>/` |
| Screen / route | `app/components/Views/<ScreenName>/` |
| Feature-internal only (not exported) | nested `components/` subdir inside the feature folder |

**Naming rules:**
- Component directory: `PascalCase` matching the component name exactly (`AccessRestrictedModal/`, `EarnHeaderSubtitle/`)
- Feature container folders are lowercase: `components/`, `hooks/`, `utils/`, `types/`
- Files: `PascalCase` prefix with a dotted role suffix (`Foo.tsx`, `Foo.types.ts`, `Foo.testIds.ts`, `Foo.test.tsx`)
- Barrel: lowercase `index.ts`

---

## 2. Required file set

Tests are **colocated** — do NOT create a separate `__tests__/` folder.

```
ComponentName/
  ComponentName.tsx             ← always required
  ComponentName.types.ts        ← recommended; inline interface only for trivial components
  ComponentName.testIds.ts      ← recommended; skip only when no testable elements exist
  ComponentName.test.tsx        ← MANDATORY, colocated next to the component
  index.ts                      ← MANDATORY
```

Optional situational files:
- `ComponentName.constants.ts` — when the component has non-trivial magic values
- Co-located `useComponentName.ts` hooks — when logic warrants extraction
- `README.md` — only for larger feature-level folders

---

## 3. Design system: which layer to use

Choose from three layers, in this order:

### Layer 1 — `@metamask/design-system-react-native` (MMDS, npm package) ✅ Always use first

The only correct choice for new component primitives: layout, text, buttons, icons, list items, sheets, and more. Look each one up by name in the [React Native components manifest](https://metamask.github.io/metamask-design-system/react-native/manifests/components.json) as described in `ui-development`, then confirm it in the installed exports.

Before writing any UI, verify what the installed version actually exports — the package changes frequently:

```
node_modules/@metamask/design-system-react-native/dist/components/index.d.cts
```

The installed package is the source of truth, not this skill's examples. Read props from `dist/components/<Component>/<Component>.types.d.cts`. For behavior and examples, read the component README on GitHub at the release tag (READMEs are not in the npm package):

```
https://github.com/MetaMask/metamask-design-system/blob/@metamask/design-system-react-native@<installed version>/packages/design-system-react-native/src/components/<Component>/README.md
```

Take `<installed version>` from `node_modules/@metamask/design-system-react-native/package.json`. When a README and the types disagree, the types win. No MCP server is needed.

For anything marked `@deprecated`, follow the Deprecated APIs rule in `ui-development`.

### Layer 2 — Existing app-level components

Use an existing app-level component only when `@metamask/design-system-react-native` has no equivalent. Search the repo for one that already covers the need, and apply the same deprecation rule to it. Prefer MMDS first.

### Layer 3 — Feature-specific composites

Build from MMDS primitives when no primitive covers the use case.

### Defaults
- `Box` is the default for layout. Using it makes code easier to move between Mobile and Extension.
- Use the MMDS `Text` component for text, with a variant from its installed types.
- Do not add `StyleSheet.create()`. Use `twClassName` or `Box` utility props.

---

## 4. Styling patterns

### `twClassName` string prop — for utility classes

```tsx
<Box twClassName="px-4 pb-6 w-full rounded-xl bg-muted" />
```

Use for: width/height, borders, rounded corners, shadows, opacity, overflow, z-index, absolute positioning, background colours via semantic tokens (`bg-default`, `bg-muted`, `bg-pressed`).

### `Box` utility props

Either `Box` utility props or `twClassName` is fine. The utility props exist only on `Box`, they only apply Tailwind class names, and they are easier to share between Mobile and Extension. Read the prop names from `Box`'s installed types. Numeric spacing props use the 4px scale (`4` = 16px).

### Enum constants for props

Import enums from `@metamask/design-system-react-native` — never pass raw strings where the type expects an enum. Read enum names and members from the installed types; do not copy them from this skill or from another platform.

### Interactive / pressed state

Use the design-system Button for actions. Confirm its export name and props in the installed package. Use the design-system base button, or a `Pressable`, only when Button cannot express the design.

When you do use the base button, it takes pressed styling through a `twClassName` function that receives the pressed flag. Its `style` prop is a plain style, so a `style={({ pressed }) => ...}` function does not type-check:

```tsx
twClassName={(pressed) => `w-full ${pressed ? 'bg-pressed' : 'bg-default'}`}
```

For a `Pressable`, use `tw.style()`:

```tsx
import { useTailwind } from '@metamask/design-system-twrnc-preset';

const tw = useTailwind();

<Pressable
  style={({ pressed }) =>
    tw.style('w-full flex-row items-center', pressed && 'bg-pressed')
  }
/>
```

---

## 5. Bottom sheet specifics

1. Use the design-system bottom sheet with its header and footer parts. Look them up in the installed exports or the manifest, and read their props from the installed types. The sheet already sets its surface token, so do not add a surface class unless the design puts the sheet on a different surface (then pass a semantic token class through `twClassName`).

2. `ScrollView` inside a design-system bottom sheet must come from `react-native-gesture-handler` — the standard React Native `ScrollView` will not scroll on Android inside a gesture-managed bottom sheet:

```tsx
// ✅ correct
import { ScrollView } from 'react-native-gesture-handler';

// ❌ will not scroll on Android
import { ScrollView } from 'react-native';
```

---

## 6. i18n

All user-visible strings must go through i18n:

```tsx
import { strings } from '../../../../locales/i18n'; // adjust depth to file location

{strings('namespace.key')}
```

Add new keys to `locales/languages/en.json` (repo root) only. Crowdin picks up new English strings automatically after the PR merges — do not edit other language files manually.

---

## 7. Imports: no path aliases

`tsconfig.json` defines no `@components` or `@app` path aliases. All imports are relative. Compute the correct `../` depth based on the file's actual location.

Example, adjusting `../` to the file:

```tsx
import { strings } from '../../../../locales/i18n';
import type { FooProps } from './Foo.types';
```

---

## 8. ESLint import fences

| Blocked import | Use instead |
|---------------|-------------|
| `expo-haptics` | `app/util/haptics` |
| `app/util/number/index.js` | `app/util/number/bigint` |
| Sibling feature directories (route-isolation zones) | Only import from your own feature or shared `app/components/UI/` |

- The only allowed `eslint-disable`: `// eslint-disable-next-line @typescript-eslint/no-require-imports` inside a `jest.mock` factory that uses `require('react-native')`. The templates below need none.

---

## 9. File templates

Replace `Foo` with the `PascalCase` component name and `foo` with its `kebab-case` form. Adjust `../` import depth to match the actual file location.

### `Foo.types.ts`

```ts
import type { ReactNode } from 'react';

export interface FooProps {
  /**
   * Content rendered inside the component.
   */
  children?: ReactNode;
  /**
   * Additional Tailwind classes applied to the component.
   */
  twClassName?: string;
  /**
   * Optional test ID for the root element.
   */
  testID?: string;
}
```

### `Foo.testIds.ts`

```ts
export const FooSelectorsIDs = {
  CONTAINER: 'foo',
} as const;
```

- Export name: `<ComponentName>SelectorsIDs`
- Keys: `SCREAMING_SNAKE_CASE`
- Values: `dash-case`, prefixed with the component's kebab-case name

**List items:** when the component renders in a list, append a unique data value at render time to avoid duplicate testIDs:

```tsx
// testIds.ts
ITEM: 'foo-item',

// usage
testID={`${FooSelectorsIDs.ITEM}-${item.id}`}
```

### `Foo.tsx`

A minimal container, in the shape of the [MMDS create-component template](https://github.com/MetaMask/metamask-design-system/blob/main/packages/design-system-react-native/scripts/create-component/ComponentName/ComponentName.tsx): it renders `children` and passes `twClassName` and `testID` through `Box`.

```tsx
import React from 'react';
import { Box } from '@metamask/design-system-react-native';
import type { FooProps } from './Foo.types';
import { FooSelectorsIDs } from './Foo.testIds';

const Foo: React.FC<FooProps> = ({
  children,
  twClassName,
  testID = FooSelectorsIDs.CONTAINER,
}) => (
  <Box twClassName={twClassName} testID={testID}>
    {children}
  </Box>
);

export default Foo;
```

### `index.ts`

```ts
export { default } from './Foo';
export type { FooProps } from './Foo.types';
export { FooSelectorsIDs } from './Foo.testIds';
```

### `Foo.test.tsx`

```tsx
import React from 'react';
import { Text } from '@metamask/design-system-react-native';
import { render, renderHook } from '@testing-library/react-native';
import { useTailwind } from '@metamask/design-system-twrnc-preset';
import Foo from './Foo';
import { FooSelectorsIDs } from './Foo.testIds';

describe('Foo', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders children', () => {
    const { getByText } = render(
      <Foo>
        <Text>Hello, World!</Text>
      </Foo>,
    );

    expect(getByText('Hello, World!')).toBeOnTheScreen();
  });

  it('applies twClassName', () => {
    const { result } = renderHook(() => useTailwind());
    const tw = result.current;

    const { getByTestId } = render(
      <Foo twClassName="bg-default" testID={FooSelectorsIDs.CONTAINER}>
        <Text>Styled Content</Text>
      </Foo>,
    );

    expect(getByTestId(FooSelectorsIDs.CONTAINER)).toHaveStyle(
      tw.style('bg-default'),
    );
  });

  it('accepts testID', () => {
    const { getByTestId } = render(
      <Foo testID={FooSelectorsIDs.CONTAINER}>
        <Text>Test Content</Text>
      </Foo>,
    );

    expect(getByTestId(FooSelectorsIDs.CONTAINER)).toBeOnTheScreen();
  });
});
```

Use `renderWithProvider` when the component:
- reads from the Redux store (selectors, hooks like `useSelector`)
- dispatches actions
- accesses theme tokens via hooks

Use `render` from `@testing-library/react-native` when the component only receives props and has no store/theme dependency.

---

## 10. Parent barrel registration

Register in the feature-level `index.ts` only when the component is consumed outside its own folder.

Add to `app/components/UI/<Feature>/index.ts`:

```ts
export { default as Foo } from './Foo';        // converts the default export to a named export
export type { FooProps } from './Foo';
export { FooSelectorsIDs } from './Foo';
```

Re-exports point at the component's own `index.ts` (`./Foo`), not directly at the implementation file.

---

## 11. Scaffold checklist

- [ ] Directory with `PascalCase` name in the correct location (Section 1)
- [ ] `Foo.types.ts` — recommended; `FooProps` interface with JSDoc per prop (`children?`, `twClassName?`, `testID?`); inline interface acceptable only for trivial components with 1–2 props
- [ ] `Foo.testIds.ts` — recommended; `FooSelectorsIDs as const`, `SCREAMING_SNAKE` keys, `dash-case` values prefixed with kebab component name; skip only when the component has no testable elements
- [ ] `Foo.tsx` — primitives from `@metamask/design-system-react-native`, or an existing app-level component when MMDS has no equivalent; `Box` for layout and the MMDS `Text` component for text; no `StyleSheet`; `strings()` for all user-visible copy; every asserted element has `testID` wired from the testIds constant
- [ ] `index.ts` — exports `default`, `type FooProps`, and `FooSelectorsIDs`
- [ ] `Foo.test.tsx` — colocated (not in `__tests__/`); testIds via constant (never raw strings); `toBeOnTheScreen()` for presence, `.toBeNull()` for absence; `beforeEach(jest.clearAllMocks)`
- [ ] ESLint and TypeScript pass: no `any`, no import fence violations, and no `eslint-disable` except the `jest.mock` one in Section 8
- [ ] If consumed outside the folder: parent feature `index.ts` updated (Section 10)
- [ ] If bottom sheet: the design-system bottom sheet parts, no extra surface class unless the design needs one; `ScrollView` from `react-native-gesture-handler`
- [ ] The `ui-development` Deprecated APIs rule holds. Actions use the design-system Button; use the base button or `Pressable` only when Button cannot express the design, with pressed styles via `twClassName={(pressed) => ...}` or `Pressable` + `tw.style()`
- [ ] All user-visible strings use `strings()` — no hardcoded copy

