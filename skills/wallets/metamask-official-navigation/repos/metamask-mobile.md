---
repo: metamask-mobile
parent: navigation
---

# Navigation — MetaMask Mobile

## Canonical API

| Role | Path |
|------|------|
| Non-UI navigator | `app/core/NavigationService/` — `NavigationService.navigation` (`navigate` and `reset` are deferred with `requestAnimationFrame`) |
| Route names | `app/constants/navigation/Routes.ts` |
| Typed params | `app/core/NavigationService/types.ts` and navigator `ParamList` types under `app/components/Nav/` |
| Screens | `useNavigation` from `@react-navigation/native` (React Navigation v7: `@react-navigation/native-stack`, `@react-navigation/bottom-tabs`) |

Deeplink *parsing* is `deeplink-handler`. This skill is route names and who calls `navigate` / `reset`.

## Requirements

- Route names from `Routes`, not string literals.
- Prefer `useNavigation` in function screens. Non-UI callers (deeplinks, Engine, sagas, `Authentication`) use `NavigationService.navigation`. Components with no navigator context (for example `PerpsTutorialCarousel`) use `NavigationService`; older class screens keep `props.navigation`.
- Typed params on `useNavigation()` — checked against `RootStackParamList` via the `ReactNavigation.RootParamList` merge in `app/core/NavigationService/types.ts`. `NavigationService.navigation` is `NavigationContainerRef<ParamListBase>`; param shapes through it are unchecked. Tests mock `NavigationService` / `@react-navigation/native` as existing tests in that folder already do.

Screen:

```ts
import { useNavigation } from '@react-navigation/native';
import Routes from '../../../constants/navigation/Routes';

const navigation = useNavigation();
navigation.navigate(Routes.SETTINGS_VIEW);
```

Non-UI:

```ts
import NavigationService from '../NavigationService';
import Routes from '../../constants/navigation/Routes';

NavigationService.navigation.navigate(Routes.MODAL.ROOT_MODAL_FLOW, {
  screen: Routes.MODAL.ACCOUNT_ACTIONS,
});
```

Auth-gated flows stay on the existing onboarding / login trees. After unlock, `Authentication` calls `NavigationService.navigation.reset` with `Routes.ONBOARDING.*` (opt-in metrics, login, or root) or `navigateToPostUnlockHome`. Do not add a parallel auth navigator.

Tests: mock `NavigationService.navigation` for service callers; mock `@react-navigation/native` for screens, matching collocated tests.

## Reject

- Hardcoded route strings (`navigate('WalletView')`)
- Calling `navigate` / `reset` during render without the deferred `NavigationService` path
- Inventing a parallel navigator instead of registering on the existing trees
- Re-implementing deeplink URL parsing here (that is `deeplink-handler`)
- Importing `@react-navigation/stack` — use `@react-navigation/native-stack` and `@react-navigation/bottom-tabs`
