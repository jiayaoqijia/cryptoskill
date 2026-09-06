# Command Map

Use this file for fast command selection before opening full docs or `acton help`.

## Setup and project context

- `curl -LsSf https://github.com/ton-blockchain/acton/releases/latest/download/acton-installer.sh | sh`
- Use when `acton` is not installed and the task requires the CLI.

- `acton --version`
- Use to record the exact CLI version before diagnosing docs or behavior.

- `acton doctor`
- Use for project-root, manifest, stdlib, overlay, env-var, and writable-path diagnostics.

- `acton --project-root <PATH> ...`
- Use when command outputs and config-relative paths must resolve from a specific project root.

- `acton --manifest-path <PATH>/Acton.toml ...`
- Use when loading a specific manifest without changing project-root resolution.

## Bootstrap and config

- `acton new [PATH] [--template empty|counter|jetton|nft] [--app] [--hooks] [--agents]`
- Use for scaffolding a fresh project, optional app layout, hooks, and coding-agent guidance.

- `acton init`
- Use for adding Acton to an existing directory, discovering contracts, patching `.gitignore`, adding default `[import-mappings]`, and installing `.acton`.

- `acton init --create-app [PATH]`
- Use for creating only the TypeScript app scaffold.

- `acton init --stdlib-only`
- Use for refreshing `.acton/tolk-stdlib` without touching `Acton.toml`.

## Build and wrapper generation

- `acton build [CONTRACT_NAME] [--clear-cache] [--graph PATH] [--out-dir DIR] [--gen-dir DIR] [--output-fift DIR] [--info]`
- Use for project builds from `Acton.toml`.

- `acton compile <PATH> [--json] [--base64-only] [--boc FILE] [--fift FILE] [--source-map FILE] [--abi FILE] [--allow-no-entrypoint] [--clear-cache]`
- Use for single-file compilation and artifact extraction.

- `acton wrapper <CONTRACT_NAME> [-o PATH|--output-dir DIR]`
- Use for Tolk wrapper generation.

- `acton wrapper <CONTRACT_NAME> --test [--test-output PATH|--test-output-dir DIR]`
- Use for generating a Tolk test stub with the wrapper.

- `acton wrapper <CONTRACT_NAME> --ts [-o PATH|--output-dir DIR]`
- Use for TypeScript client wrapper generation.

## Tests and quality

- `acton test [PATH] [--filter REGEX] [--include GLOB] [--exclude GLOB] [--reporter console|dot|teamcity|junit]`
- Use for normal test runs.

- `acton test --coverage --coverage-format lcov [--coverage-file PATH] [--coverage-minimum-percent PERCENT]`
- Use for code coverage, LCOV export, and coverage gates.

- `acton test --snapshot build/gas-baseline.json`
- Use for creating gas and fee baselines.

- `acton test --baseline-snapshot build/gas-baseline.json [--fail-on-diff]`
- Use for gas regression checks.

- `acton test --mutate --mutate-contract <CONTRACT_NAME> [--mutation-diff worktree|ref|branch] [--mutation-levels critical,major]`
- Use for mutation testing, optionally scoped to changed lines or selected rule levels.

- `acton test --debug --debug-port 12345 [--backtrace full]`
- Use for debugger-based diagnosis.

- `acton test --ui [--ui-port 12344]`
- Use for browser-based inspection of failed tests, traces, transactions, logs, and coverage.

- `acton test --save-test-trace [DIR]`
- Use for offline trace bundles.

- `acton test --fork-net testnet|mainnet|custom:<name> [--fork-block-number N]`
- Use for forked-state tests against remote chain data.

- `acton check [TARGET] [--fix] [--output-format plain|json|sarif|github|gitlab] [--output-file PATH]`
- Use for linting Tolk code and CI annotations.

- `acton fmt [PATHS...] [--check]`
- Use for formatting or CI format validation.

- `acton hooks new|install|status|uninstall`
- Use for project-local Git hook scaffolding and installation.

## Scripts, deployment, and blockchain interaction

- `acton script <PATH> [ARGS...]`
- Use for local script execution and safe emulation.

- `acton script <PATH> --net testnet|mainnet|custom:<name> [--explorer tonscan|toncx|dton|tonviewer]`
- Use for network transactions. This can spend TON on real networks.

- `acton script <PATH> --fork-net testnet|mainnet|custom:<name> [--fork-block-number N]`
- Use for read paths against forked chain state without broadcasting.

- `acton run <SCRIPT_NAME> [ARGS...]`
- Use for shortcuts defined under `[scripts]` in `Acton.toml`.

## Wallets, verification, libraries, and RPC

- `acton wallet new|import|list|export-mnemonic|sign|remove|airdrop`
- Use for wallet lifecycle, signing, and testnet faucet flows.

- `acton verify [CONTRACT_NAME] --address <ADDRESS> [--net testnet|mainnet] [--wallet NAME] [--compiler-version VER] [--dry-run]`
- Use for source verification against TON Verifier.

- `acton library publish|fetch|info|topup`
- Use for on-chain library lifecycle tasks.

- `acton rpc info <ADDRESS> [--net testnet|mainnet|custom:<name>]`
- Use for remote account inspection and storage decoding when ABI is known.

- `acton rpc block|block-number [--net testnet|mainnet|custom:<name>]`
- Use for quick network liveness and current masterchain block checks.

- `acton rpc trace <HASH> [--net NET] [--summary|--tree|--verbose] [--show-bodies]`
- Use for rendering a TonCenter v3 trace as a decoded transaction tree.

## Inspection and developer tooling

- `acton disasm [BOC_FILE] [-s HEX_OR_BASE64] [-o PATH] [--json] [--address ADDRESS] [--net NET] [--source-map FILE] [--show-offsets] [--show-hashes] [--follow-libraries]`
- Use for BoC and live-code disassembly.

- `acton retrace <TX_HASH> [--net NET] [--verbose] [--logs-dir DIR] [--contract CONTRACT] [--debug] [--debug-port PORT]`
- Use for replaying on-chain transactions locally, optionally with source-level debugging.

- `acton doc tvm <QUERY...> [--find] [--description] [--json]`
- Use for TVM instruction lookup.

- `acton ls [--stdio|--port PORT] [--log-file PATH] [--no-log]`
- Use for TON/Tolk language-server workflows.

- `acton func2tolk <PATH> [--output PATH] [--warnings-as-comments] [--no-camel-case] [--version VERSION]`
- Use for quick FunC-to-Tolk conversion via the npm-based converter.

- `acton up [VERSION] [--list] [--trunk] [--stable] [--force]`
- Use for version management.

- `acton completions bash|elvish|fish|powershell|zsh|nushell`
- Use for static shell completion generation.
