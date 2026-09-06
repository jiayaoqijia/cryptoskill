---
repo: metamask-extension
parent: add-evm-network
---

# Add EVM Swaps/Bridge Network

`docs/add-evm-swaps-bridge-network.md` is the single source of truth.

## How to use

1. Read `docs/add-evm-swaps-bridge-network.md` in full before editing.
2. Follow its `Agent Execution Standard (SSOT)` workflow exactly.
3. Return the `Required Agent Response Sections` listed at the end of that doc.

## Layers at a glance (details in the doc)

- Upstream hard allowlist: `@metamask/bridge-controller` → `ALLOWED_BRIDGE_CHAIN_IDS`.
- Extension constants: `shared/constants/bridge.ts` → `ALLOWED_EVM_BRIDGE_CHAIN_IDS`, `NETWORK_TO_SHORT_NETWORK_NAME_MAP`, `BRIDGE_CHAINID_COMMON_TOKEN_PAIR`.
- Stablecoins: `ui/pages/bridge/utils/stablecoins.ts` → `STABLECOIN_ASSET_IDS`.
- Remote feature flag: `bridgeConfigV2` → `chains`, `chainRanking`, top-level `stablecoins`.
- Tests: `ui/ducks/bridge/selectors.test.ts`, `ui/hooks/bridge/useSmartSlippage.test.ts`.

Prerequisite: the chain must already exist in `shared/constants/network.ts` and in the installed `@metamask/bridge-controller` hard allowlist. If either is missing, stop and report the blocker.
