# Community Sui SDKs

**None of these are maintained by Mysten Labs.** They are community-supported and may lag protocol updates. Always check the repo's last commit and whether the latest Sui protocol is supported before relying on one.

Canonical inventory: https://docs.sui.io/references/sui-sdks

## Python — `pysui`

| | |
|---|---|
| Repo | https://github.com/FrankC01/pysui |
| Install | `pip install pysui` · upgrade: `pip install -U --upgrade-strategy eager pysui` |
| Maintainer | Community (FrankC01) |
| Protocols | JSON-RPC (deprecated), GraphQL, gRPC |
| Supports PTBs | Yes — via `transaction()` with `build()`, `build_and_sign()`, `transaction_data()` |

Most mature community SDK. Sync and async clients. Supports PTB construction and execution.

```python
from pysui import SuiConfig, SyncClient
from pysui.sui.sui_txn import SyncTransaction

cfg = SuiConfig.default_config()
client = SyncClient(cfg)
txn = SyncTransaction(client=client)
txn.split_coin(coin=txn.gas, amounts=[1_000_000])
txn.transfer_objects(transfers=[...], recipient='0x...')
result = txn.execute(gas_budget='10000000')
```

Check `docs` directory and `pypi` page for current API — the surface evolves.

## Go — `block-vision/sui-go-sdk`

| | |
|---|---|
| Repo | https://github.com/block-vision/sui-go-sdk |
| Install | `go get github.com/block-vision/sui-go-sdk` |
| Maintainer | Community (BlockVision) |
| Protocols | Primarily JSON-RPC (deprecated) |

Other Go SDKs exist (SuiVision, Pattonkan). `block-vision` is the one listed on docs.sui.io; assess staleness before use.

## Dart — `mofalabs/sui`

| | |
|---|---|
| Repo | https://github.com/mofalabs/sui |
| Install | `dart pub add sui` or Flutter `flutter pub add sui` |
| Maintainer | Community (mofalabs) |
| Use case | Cross-platform Flutter apps, mobile & web |

## Kotlin — `ksui` (`mcxross/ksui`)

| | |
|---|---|
| Repo | https://github.com/mcxross/ksui |
| Maintainer | Community (mcxross) |
| Use case | Kotlin Multiplatform; JSON-RPC wrapper (deprecated) + crypto utilities |

## Swift — `SuiKit` (`opendive/suikit`)

| | |
|---|---|
| Repo | https://github.com/opendive/suikit |
| Maintainer | Community (OpenDive) |
| Use case | Native iOS / macOS apps |

## Vue/TS — `SuiFansCN/suiue`

| | |
|---|---|
| Repo | https://github.com/SuiFansCN/suiue |
| Maintainer | Community |
| Use case | Vue-based dApp Kit equivalent |

For React, use `@mysten/dapp-kit-react` instead (official, covered in the `frontend-apps` skill). The bare `@mysten/dapp-kit` package name is the deprecated JSON-RPC-only predecessor.

## Risk checklist before choosing a community SDK

1. **Last commit date** — more than a few months old is a yellow flag.
2. **Protocol version compatibility** — does it support the latest Sui release?
3. **Feature coverage** — PTBs, sponsored tx, object queries, event subscription. Many community SDKs are query-only or lack newer features (e.g., gRPC, intents).
4. **Issue tracker health** — open issues, responsive maintainer.
5. **FFI alternative** — if the language constraint is hard and the community SDK is stale, consider wrapping the Rust SDK via FFI (uniffi / pyo3 / napi) rather than relying on an unmaintained library.

## Recommendation decision tree

1. **Can you use TypeScript or Rust?** If yes — stop here, use the official SDK.
2. **Is Python / Go / Swift / Kotlin / Dart a hard requirement?** Check the relevant community SDK for recent commits + protocol support.
3. **Is the community SDK stale?** Consider FFI-wrapping the Rust SDK (`sui-rust-sdk`) in your target language.
4. **Still stuck?** Use the community SDK but flag the staleness risk to the user and be prepared to fall back to JSON-RPC (deprecated) / raw BCS construction or wrapping the Rust SDK via FFI.

Always tell the user when they're relying on a community SDK. They may prefer to switch languages for an official SDK.
