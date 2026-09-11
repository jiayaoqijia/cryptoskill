---
repo: metamask-mobile
parent: selector-patterns
---

# Selector patterns — MetaMask Mobile

Copy from `app/selectors/tokensController.ts` (`EMPTY_TOKENS_BY_ADDRESS`, `EMPTY_TOKENS`, `selectTokensByAddress`, `selectAllTokensFlat`, `selectTokensLength`). Tests: `yarn jest app/selectors/<feature>.test.ts --no-coverage` (shape: `app/selectors/tokensController.test.ts`; unit-test skill: `mobile-testing`). Opt in: `yarn skills --include coding/selector-patterns --save`. Engine wiring: `controller-integration`. Memoization audits: `performance` (`mm-selector-memoization.md`). Version-gated flags: `feature-flags`.

## Paths

| Role | Path |
|------|------|
| Default selectors | `app/selectors/<feature>.ts` (or `app/selectors/<feature>/index.ts`) |
| Feature-private selectors | `app/components/UI/<Feature>/selectors/` |
| Deep-equal helper | `app/selectors/util.ts` → `createDeepEqualSelector` |
| Collocated tests | `app/selectors/<feature>.test.ts` |

New selectors use `select<Feature><Thing>` (e.g. `selectTokensByChainIdAndAddress`). Existing `get*` names stay; do not rename them in this change.

## Leaf vs derived

Only leaf input selectors read `state.engine.backgroundState`. Use `?? getDefault<Name>State()` when that helper exists. Illustrative leaf (plain function, not a file to copy):

```ts
export const selectFooControllerState = (state: RootState) =>
  state.engine.backgroundState.FooController ?? getDefaultFooControllerState();
```

Derived selectors compose on a named, narrowed input. From `tokensController.ts`:

```ts
import { Token, TokensControllerState } from '@metamask/assets-controllers';
import { createSelector } from 'reselect';
import { createDeepEqualSelector } from './util';

const EMPTY_TOKENS_BY_ADDRESS: Readonly<Record<string, never>> = Object.freeze(
  {},
);

const EMPTY_TOKENS: Token[] = Object.freeze([] as Token[]) as Token[];

export const selectTokensByAddress = createDeepEqualSelector(
  selectTokens,
  (tokens: Token[]): { [address: string]: Token } => {
    if (!tokens?.length) {
      return EMPTY_TOKENS_BY_ADDRESS;
    }

    return tokens.reduce<Record<string, Token>>((tokensMap, token) => {
      tokensMap[token.address] = token;
      return tokensMap;
    }, {});
  },
);

export const selectAllTokensFlat = createDeepEqualSelector(
  getTokensControllerAllTokens,
  (tokensByAccountByChain: TokensControllerState['allTokens']): Token[] => {
    const groups = Object.values(tokensByAccountByChain);
    if (groups.length === 0) {
      return EMPTY_TOKENS;
    }

    return groups.reduce<Token[]>((acc, tokensByAccount) => {
      const tokensArray = Object.values(tokensByAccount).flat();
      return acc.concat(...tokensArray);
    }, []);
  },
);

export const selectTokensLength = createSelector(
  selectTokens,
  (tokens: Token[]) => tokens.length,
);
```

`EMPTY_TOKENS` / `EMPTY_TOKENS_BY_ADDRESS` are module-level constants. Inline `?? {}` / `?? []` on a plain `createSelector` allocates a new ref every call.

## Factory choice

Narrow the input to the smallest slice first (`performance` / `mm-selector-memoization.md`). Then:

| Output | Factory |
|--------|---------|
| boolean, number, string | `createSelector` from `reselect` |
| object, array, Map, Set | `createDeepEqualSelector` from `app/selectors/util.ts` when the narrowed input still churns (fresh ref every dispatch) and the payload is small enough to deep-compare |

A sub-key read plus a module-level empty constant may stay on `createSelector`.

## UI

```ts
const tokensByAddress = useSelector(selectTokensByAddress);
```

## Tests

Collocate `app/selectors/<feature>.test.ts`. At least two state variants per new selector (populated + empty/missing). Present tense, AAA, no "should". `yarn jest app/selectors/<feature>.test.ts --no-coverage`. Fixtures (`mockRootState`, `mockToken`, `mockTokensControllerState`) live in `tokensController.test.ts`:

```ts
describe('selectTokensByAddress', () => {
  it('returns tokens mapped by address', () => {
    expect(selectTokensByAddress(mockRootState)).toStrictEqual({
      '0xToken1': mockToken,
    });
  });

  it('handles an empty tokens array', () => {
    const stateWithoutTokens = {
      ...mockRootState,
      engine: {
        backgroundState: {
          TokensController: {
            ...mockTokensControllerState,
            allTokens: {
              '0x1': {
                '0xAddress1': [],
              },
            },
            tokens: [],
          },
          AccountsController: {
            internalAccounts: {
              selectedAccount: '0xAddress1',
              accounts: {
                '0xAddress1': {
                  address: '0xAddress1',
                },
              },
            },
          },
        },
      },
    } as unknown as RootState;

    expect(selectTokensByAddress(stateWithoutTokens)).toStrictEqual({});
  });
});
```

## Requirements

- New and changed selectors live under `app/selectors/<feature>.ts` (or the feature’s `selectors/` folder), named `select<Feature><Thing>`.
- Only leaf input selectors read `state.engine.backgroundState` (with `?? getDefault<Name>State()` when that helper exists).
- Narrow the input first. Derive with `createSelector` (primitives) or `createDeepEqualSelector` (object / array when the narrowed input still churns and the payload is small enough to compare). Stable module-level empty constants instead of inline `?? {}` / `?? []` on plain `createSelector`.
- Collocated unit tests with at least two state variants.
- Components and hooks use `useSelector(selectX)` with the named selector.

## Reject

- New and changed UI: `state.engine.backgroundState` in components, hooks, or other UI
- Inline `useSelector((state) => …)` derivation
- `useSelector(x, isEqual)` as a substitute for a stable selector
- Version-gated flag evaluation outside `feature-flags`
- Selector memoization (identity wrappers, new refs in result functions, mutation, huge inputs): `performance` (`mm-selector-memoization.md`)
