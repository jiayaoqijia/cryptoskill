---
repo: metamask-mobile
parent: add-evm-network
---

# Add an EVM Network to Mobile Swaps and Bridge

Wire only the unified Swaps/Bridge flow. Do not modify legacy swaps or wrapping
logic unless the task explicitly includes them.

## Separate implementation and launch readiness

Confirm these code inputs before implementation:

- Mobile already exposes the chain through its current network constants,
  including the canonical `NETWORK_CHAIN_ID` entry and network metadata.
- A released `@metamask/bridge-controller` version contains the chain in
  `CHAIN_IDS`, `ChainId`, and `ALLOWED_BRIDGE_CHAIN_IDS`.
- The default destination token address, symbol, name, decimals, and icon URL
  are authoritative.
- Stablecoin addresses are known if stable-to-stable swaps should receive the
  reduced default slippage.

Stop and report a missing code input rather than inventing metadata or leaving
a partial implementation.

Track these separate launch requirements without blocking an otherwise valid
Mobile code change:

- the Bridge API supports at least one approved source/destination route and
  token pair for the chain;
- the `bridgeConfigV2` owner has the decimal/CAIP chain ID, display name,
  ranking position, activation direction, rollout percentage, and minimum
  Mobile version.

The network picker intersects two gates: the controller hard allowlist and the
remote `bridgeConfigV2.chainRanking`. Missing API or remote configuration blocks
claiming the network is launch-ready, not preparing the client PR. Continue with
the code when its inputs are complete and report every launch gap explicitly.

## Review reference implementations and live shapes

Inspect current types and neighboring network entries before editing; the
default-token map has changed shape over time. Use these PRs as behavioral
references, not as patches to replay:

- [MetaMask/metamask-mobile#31413 — ARC](https://github.com/MetaMask/metamask-mobile/pull/31413),
  covering the default destination token, stablecoin slippage, and network
  label.
- [MetaMask/metamask-mobile#33110 — Robinhood Chain](https://github.com/MetaMask/metamask-mobile/pull/33110),
  covering the bridge-controller upgrade, default token, and label. Treat
  dependency-driven cleanup in that PR as incidental rather than required.

## Implement the Mobile layer

1. Verify the installed `@metamask/bridge-controller` exports the chain. If it
   does not, update `package.json` to the first compatible released version and
   regenerate `yarn.lock` with the repository's package-manager workflow.
   Avoid unrelated dependency upgrades where the lockfile permits it.
2. In
   `app/components/UI/Bridge/constants/default-swap-dest-tokens.ts`, add the
   chain's default destination token. Follow the current value shape exactly
   (for example, a token entry may be nested under `'*'`). Include the canonical
   address, decimals, image URL, and chain ID. Checksum source addresses where
   current entries do so; use the lowercase address in the token-icon URL.
3. In `app/constants/bridge.ts`, add the concise UI label to
   `NETWORK_TO_SHORT_NETWORK_NAME_MAP` using the existing Mobile chain
   constant.
4. Find the current stablecoin registry used by default-slippage logic. If the
   chain supports reduced stablecoin slippage, add every approved stablecoin
   address using the registry's existing normalization and update its tests.
   Do not treat the default destination token as a stablecoin without product
   confirmation.
5. Compile after a controller upgrade. Resolve only type errors or stale
   suppressions directly caused by the new dependency version. Keep unrelated
   fee, quote, and behavior cleanup out of the network integration.

Search for the chain identifier, decimal ID, hex ID, and CAIP ID after editing.
Confirm there is no second Mobile bridge label, token map, stablecoin registry,
or test fixture that also requires the network.

## Specify the remote rollout

Record the required `bridgeConfigV2` change even when LaunchDarkly is outside
the repository:

- add `chains["<decimalChainId>"]` with the approved source/destination and
  unified-button activation fields;
- add `{ "chainId": "eip155:<decimal>", "name": "<display name>" }` to
  `chainRanking` at the intended position;
- add approved assets to `topAssets`, `batchSellDestStablecoins`, and the
  top-level `stablecoins` list only when the product configuration requires
  them;
- define percentage rollout and `minimumVersion` gating.

Do not claim the network is available in the picker until both controller and
remote gates are satisfied.

## Test and manually verify

Use established test seams for behavior that the integration changes. Add or
update focused tests for the default token, label, or stablecoin registry only
when those areas already have meaningful coverage. Verify through tests or
documented static inspection that:

- the default token resolves for the new destination chain;
- the short network label resolves;
- approved stablecoin pairs receive the intended default slippage;
- the existing bridge selector tests still enforce exclusion when either
  allowlist layer is absent and inclusion when both layers contain a chain.

Do not add a per-network copy of generic allowlist-intersection tests unless the
selector behavior itself changes. Run the existing bridge slice tests instead.

Run the narrowest relevant Jest suites with `--collectCoverage=false`, then the
repository's applicable typecheck and lint commands. Review lockfile changes
when the controller dependency changes.

Manually exercise both directions supported by the flag:

1. select the new network as a destination and confirm the intended default
   token;
2. request a real quote for an approved token pair;
3. select it as a source if source activation is enabled;
4. confirm the display label, token icon, decimals, balance, fee, and slippage;
5. repeat on iOS and Android when preparing the PR for review.

Finish with a prerequisites result, files changed, remote flag changes, tests
run, manual-test evidence, dependency/release status, and remaining gaps.
