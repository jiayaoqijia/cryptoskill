---
repo: core
parent: add-evm-network-bridge-controller
---

# Add an EVM Network to Bridge Controller

Add the chain as an additive public contract in `packages/bridge-controller`.
Do not change quote, transaction, or controller behavior unless the task
explicitly requires it.

## Gather authoritative inputs

Before editing, confirm these implementation inputs:

- canonical network name and the uppercase TypeScript identifier;
- decimal chain ID, lowercase `0x` chain ID, and `eip155:<decimal>` CAIP ID;
- user-facing display name and desired picker rank;
- native gas token symbol, name, decimals, and representation used by Bridge;
- whether the zero address represents the native asset for this chain;
- whether a nonstandard native symbol needs a `SYMBOL_TO_SLIP44_MAP` entry.

Also identify the downstream Mobile and Extension rollout owners and intended
package release when known. Missing handoff ownership or release timing does
not block the additive Core implementation; record it as a remaining gap.

Derive the hex and CAIP forms from the decimal chain ID and verify the round
trip. Use authoritative network/token data; do not copy token decimals or an
address from another network merely because its integration is structurally
similar. Stop and report missing product or token metadata rather than inventing
it. Picker rank and native-token representation are implementation inputs;
downstream scheduling is not.

## Review reference implementations

Read the current files before editing because names and types evolve. Compare:

- [MetaMask/core#9007 — ARC](https://github.com/MetaMask/core/pull/9007),
  including its non-ETH native/default token.
- [MetaMask/core#9459 — Robinhood Chain](https://github.com/MetaMask/core/pull/9459),
  including an ETH-native chain.

Use the newest adjacent EVM entry in each target file as the formatting and
ordering reference.

## Implement every registration point

1. In `packages/bridge-controller/src/constants/chains.ts`:
   - add the lowercase hex value to `CHAIN_IDS`;
   - add a display-name constant;
   - add the chain to `NETWORK_TO_NAME_MAP`.
2. In `packages/bridge-controller/src/constants/bridge.ts`:
   - add the hex chain ID to `ALLOWED_BRIDGE_CHAIN_IDS`;
   - add `{ chainId: 'eip155:<decimal>', name: '<display name>' }` to
     `DEFAULT_CHAIN_RANKING` at the intended picker position.
3. In `packages/bridge-controller/src/constants/tokens.ts`:
   - register the native currency symbol if the current file maintains a
     currency-symbol map;
   - define a dedicated swaps token object and add it to
     `SWAPS_CHAINID_DEFAULT_TOKEN_MAP`;
   - reuse the existing ETH token metadata for an ETH-native chain;
   - for a non-ETH native asset, provide the exact symbol, name, address,
     decimals, and icon behavior expected by consumers;
   - update `SYMBOL_TO_SLIP44_MAP` only when the symbol is new and a valid
     asset identifier is known.
4. In `packages/bridge-controller/src/types.ts`, add the decimal member to the
   public `ChainId` enum.
5. Add an `Unreleased` entry to
   `packages/bridge-controller/CHANGELOG.md` and link the PR when its number is
   available.

Preserve the three representations deliberately: `CHAIN_IDS` and allowlists
use hex, `ChainId` uses decimal, and rankings use CAIP IDs. Search for the
identifier, decimal ID, hex ID, and CAIP ID after editing to catch omissions or
collisions.

## Validate the package contract

Use existing focused tests when the package already covers the changed maps.
For each invariant below, either cite an existing or new assertion or record a
static inspection backed by the package build and typecheck:

- the chain is in `ALLOWED_BRIDGE_CHAIN_IDS`;
- its default ranking uses the correct CAIP ID;
- `NETWORK_TO_NAME_MAP` resolves its display name;
- `SWAPS_CHAINID_DEFAULT_TOKEN_MAP` resolves correct token metadata;
- the public enum value equals the decimal chain ID.

Do not create a new low-value suite solely to restate additive constant entries.
Add tests when an established seam exists or behavior, validation, or public
serialization changes.

Run the checks supported by the checkout:

```bash
yarn workspace @metamask/bridge-controller run test
yarn workspace @metamask/bridge-controller run build
yarn workspace @metamask/bridge-controller run changelog:validate
yarn build
yarn lint:misc:check
```

If invoking Jest directly, include `--collectCoverage=false`. Report unavailable
or unrelated failing checks instead of masking them.

## Hand off downstream rollout

State that Core support is only the hard allowlist layer. Mobile and Extension
must consume a released `@metamask/bridge-controller` version and their remote
`bridgeConfigV2.chainRanking` must include the CAIP chain ID before the network
can surface. Report the package release requirement, default token decision,
tests run, and any downstream gaps.
