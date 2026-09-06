---
repo: metamask-mobile
parent: component-scaffold
---

# Component Scaffold — MetaMask Mobile

---

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

Two systems coexist in the repo:

### Layer 1 — `@metamask/design-system-react-native` (MMDS, npm package) ✅ Always use first

The only correct choice for new component primitives. Exports `Box`, `Text`, `BottomSheet`, `BottomSheetHeader`, `BottomSheetFooter`, `ButtonBase`, `ButtonIcon`, `HeaderStandard`, `Icon`, `Skeleton`, `Tag`, and more.

Before writing any UI, verify what the installed version actually exports — the package changes frequently:

```
node_modules/@metamask/design-system-react-native/dist/components/index.d.cts
```

If the file layout differs, also try:
```
node_modules/@metamask/design-system-react-native/dist/components/index.d.ts
node_modules/@metamask/design-system-react-native/src/components/index.ts
```

The installed package is the source of truth, not this skill's examples.

For local visual testing of a component in isolation, see `docs/readme/storybook.md`.

### Layer 2 — `app/component-library/components/`

Valid second choice **only** when `@metamask/design-system-react-native` does not export an equivalent (e.g. Tabs, MetaMask-specific modal wrappers not yet migrated to MMDS).

Do not use any component in this library that carries a `@deprecated` JSDoc annotation — those have MMDS equivalents and must be replaced. For everything else in this library, prefer MMDS first; use `app/component-library` only when no MMDS primitive covers the need.

### Layer 3 — Feature-specific composites

Build from MMDS primitives when no primitive covers the use case.

### Never use
- Raw `View` from `react-native` — use `Box`
- Raw `Text` from `react-native` without variants — use `Text` with `TextVariant`
- `StyleSheet.create()` — use `twClassName` or Box layout props

---

## 4. Styling patterns

### `twClassName` string prop — for utility classes

```tsx
<Box twClassName="px-4 pb-6 w-full rounded-xl bg-muted" />
```

Use for: width/height, borders, rounded corners, shadows, opacity, overflow, z-index, absolute positioning, background colours via semantic tokens (`bg-default`, `bg-muted`, `bg-pressed`).

### Box layout enum props — preferred for flexbox

```tsx
<Box
  flexDirection={BoxFlexDirection.Row}
  alignItems={BoxAlignItems.Center}
  justifyContent={BoxJustifyContent.Between}
  gap={2}
  padding={4}
/>
```

Type-safe, prevents class-string typos. Spacing units: each unit = 4px (`padding={4}` = 16px, max `12` = 48px).

### Enum constants for props

Import from `@metamask/design-system-react-native` — never use raw strings:

```tsx
import {
  TextVariant,
  TextColor,
  FontWeight,
  ButtonBaseSize,
  BoxFlexDirection,
  BoxAlignItems,
  BoxJustifyContent,
  BoxBackgroundColor,
} from '@metamask/design-system-react-native';
```

### Interactive / pressed state

```tsx
import { useTailwind } from '@metamask/design-system-twrnc-preset';

const tw = useTailwind();

<ButtonBase
  style={({ pressed }) =>
    tw.style('w-full flex-row items-center', pressed && 'bg-pressed')
  }
/>
```

---

## 5. Bottom sheet specifics

1. Apply `useElevatedSurface()` to the `BottomSheet`'s `twClassName` — required for pure-black theme support:

```tsx
import { useElevatedSurface } from '../../../../util/theme/themeUtils'; // adjust depth

const surfaceClass = useElevatedSurface();

<BottomSheet twClassName={surfaceClass}>
```

2. `ScrollView` inside a `BottomSheet` must come from `react-native-gesture-handler` — the standard React Native `ScrollView` will not scroll on Android inside a gesture-managed bottom sheet:

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

Add new keys to `app/locales/languages/en.json` only. Crowdin picks up new English strings automatically after the PR merges — do not edit other language files manually.

---

## 7. Imports: no path aliases

`tsconfig.json` defines no `@components` or `@app` path aliases. All imports are relative. Compute the correct `../` depth based on the file's actual location.

Example from `app/components/UI/Compliance/AccessRestrictedModal/AccessRestrictedModal.tsx`:
```tsx
import { strings } from '../../../../../locales/i18n';
import { useElevatedSurface } from '../../../../util/theme/themeUtils';
```

---

## 8. ESLint import fences

| Blocked import | Use instead |
|---------------|-------------|
| `expo-haptics` | `app/util/haptics` |
| `app/util/number/index.js` | `app/util/number/bigint` |
| Sibling feature directories (route-isolation zones) | Only import from your own feature or shared `app/components/UI/` |

- One allowed `eslint-disable`: `// eslint-disable-next-line @typescript-eslint/no-require-imports` inside a `jest.mock` factory that uses `require('react-native')`

---

## 9. File templates

Replace `Foo` with the `PascalCase` component name and `foo` with its `kebab-case` form. Adjust `../` import depth to match the actual file location.

### `Foo.types.ts`

```ts
export interface FooProps {
  /**
   * Whether the component is visible.
   */
  isVisible: boolean;
  /**
   * Callback fired when the user dismisses the component.
   */
  onClose: () => void;
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
  TITLE: 'foo-title',
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

```tsx
import React from 'react';
import {
  Box,
  ButtonBase,
  Text,
  TextColor,
  TextVariant,
} from '@metamask/design-system-react-native';
import { useTailwind } from '@metamask/design-system-twrnc-preset';
import { strings } from '../../../../locales/i18n'; // adjust depth
import { FooProps } from './Foo.types';
import { FooSelectorsIDs } from './Foo.testIds';

const Foo: React.FC<FooProps> = ({
  isVisible,
  onClose,
  testID = FooSelectorsIDs.CONTAINER,
}) => {
  const tw = useTailwind();

  if (!isVisible) return null;

  return (
    <ButtonBase
      onPress={onClose}
      testID={testID}
      style={({ pressed }) =>
        tw.style('px-4 pb-6', pressed && 'bg-pressed')
      }
    >
      <Text
        variant={TextVariant.BodyMd}
        color={TextColor.TextAlternative}
        testID={FooSelectorsIDs.TITLE}
      >
        {strings('foo.title')}
      </Text>
    </ButtonBase>
  );
};

export default Foo;
```

> For a bottom sheet, add `useElevatedSurface()` — see Section 5.

### `index.ts`

```ts
export { default } from './Foo';
export type { FooProps } from './Foo.types';
export { FooSelectorsIDs } from './Foo.testIds';
```

### `Foo.test.tsx`

```tsx
import React from 'react';
import { fireEvent } from '@testing-library/react-native';
import renderWithProvider from '../../../../util/test/renderWithProvider'; // adjust depth
import Foo from './Foo';
import { FooSelectorsIDs } from './Foo.testIds';

describe('Foo', () => {
  const defaultProps = {
    isVisible: true,
    onClose: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders nothing when isVisible is false', () => {
    const { queryByTestId } = renderWithProvider(
      <Foo {...defaultProps} isVisible={false} />,
    );

    expect(queryByTestId(FooSelectorsIDs.CONTAINER)).toBeNull();
  });

  it('renders the title when visible', () => {
    const { getByTestId } = renderWithProvider(<Foo {...defaultProps} />);

    expect(getByTestId(FooSelectorsIDs.TITLE)).toBeOnTheScreen();
  });

  it('calls onClose when dismissed', () => {
    const { getByTestId } = renderWithProvider(<Foo {...defaultProps} />);

    fireEvent.press(getByTestId(FooSelectorsIDs.CONTAINER));

    expect(defaultProps.onClose).toHaveBeenCalledTimes(1);
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
- [ ] `Foo.types.ts` — recommended; `FooProps` interface with JSDoc per prop, optional `testID?: string`; inline interface acceptable only for trivial components with 1–2 props
- [ ] `Foo.testIds.ts` — recommended; `FooSelectorsIDs as const`, `SCREAMING_SNAKE` keys, `dash-case` values prefixed with kebab component name; skip only when the component has no testable elements
- [ ] `Foo.tsx` — primitives from `@metamask/design-system-react-native` (or `app/component-library` for MetaMask-specific components with no MMDS equivalent and no `@deprecated` annotation); no `View`, no `StyleSheet`; `strings()` for all user-visible copy; every asserted element has `testID` wired from the testIds constant
- [ ] `index.ts` — exports `default`, `type FooProps`, and `FooSelectorsIDs`
- [ ] `Foo.test.tsx` — colocated (not in `__tests__/`); testIds via constant (never raw strings); `toBeOnTheScreen()` for presence, `.toBeNull()` for absence; `beforeEach(jest.clearAllMocks)`
- [ ] ESLint and TypeScript pass: no `any`, no `eslint-disable`, no import fence violations
- [ ] If consumed outside the folder: parent feature `index.ts` updated (Section 10)
- [ ] If bottom sheet: `useElevatedSurface()` applied; `ScrollView` from `react-native-gesture-handler`
- [ ] All user-visible strings use `strings()` — no hardcoded copy

