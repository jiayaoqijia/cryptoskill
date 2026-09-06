---
name: acton
description: "Acton CLI workflow for TON smart contract development in Tolk: install/update, project bootstrap, Acton.toml configuration, build/compile/wrapper generation, tests with coverage/gas/fuzz/mutation/UI, scripts and deployment, wallets, verification, RPC inspection, libraries, lint/format/hooks, LSP/completions, and troubleshooting."
---

# Acton TON CLI Workflow

## Source of truth

- Prefer the exact installed binary for command spelling and behavior:
  - `acton --version`
  - `acton --help`
  - `acton help <command>`
  - `acton <command> --help`
- Use official hosted docs for current concepts, tutorials, and full reference:
  - `https://ton-blockchain.github.io/acton/docs/welcome/`
  - `https://ton-blockchain.github.io/acton/docs/commands/`
  - `https://ton-blockchain.github.io/acton/llms-full.txt`
- Use the official examples repo for real project patterns and reference contracts:
  - `https://github.com/ton-blockchain/acton-contracts`
- Read bundled references only when needed:
  - `references/command-map.md` for fast command selection
  - `references/troubleshooting.md` for common failure modes
- Do not assume local paths, private checkouts, or a specific developer machine.
- Use GitHub source only when the user explicitly asks to inspect upstream implementation. Treat `acton-contracts` as examples of project structure and contract patterns, not as the source of truth for CLI flags.
- If docs and the installed CLI disagree, state the Acton version and follow the installed CLI for that local workflow. If the user wants latest behavior, suggest `acton up` or the install/update flow first.

## First-release exclusions

- Do not recommend `acton localnet` or `--net localnet`. That feature may remain visible in source or trunk help, but it is excluded from the first release and should be treated as unavailable in public workflows.

## Install or update Acton

If `acton` is missing and the task requires running it, install the public binary:

```bash
curl -LsSf https://github.com/ton-blockchain/acton/releases/latest/download/acton-installer.sh | sh
```

Then open a fresh shell or reload the updated shell profile if needed, and verify:

```bash
acton --version
acton --help
```

Update and version management:

- `acton up` installs the latest stable release.
- `acton up --list` lists available versions.
- `acton up <version>` installs a specific version.
- `acton up --trunk` installs the latest trunk build when supported by the installed CLI.
- In CI, prefer `ton-blockchain/setup-acton@master` or the published `ghcr.io/ton-blockchain/acton:<version>` image.

## First checks in any project

1. Confirm tool and project context:
   - `acton --version`
   - `acton doctor`
   - `pwd`
2. If running from outside the project, select context explicitly:
   - `acton --project-root <PATH> ...`
   - `acton --manifest-path <PATH>/Acton.toml ...`
3. Inspect the relevant command help before relying on memory:
   - `acton help build`
   - `acton help test`
   - `acton help script`
4. Inspect `Acton.toml` for the sections that matter:
   - `[package]`
   - `[contracts]`
   - `[build]`
   - `[wrappers.tolk]`
   - `[wrappers.typescript]`
   - `[fmt]`
   - `[test]`
   - `[lint]`
   - `[networks]`
   - `[scripts]`
   - `[import-mappings]`

Project-root rule: config-relative paths are resolved from the project root. Relative CLI path flags are resolved from the current working directory unless passed as absolute paths.

## Project bootstrap

- Use `acton new [path] --template empty|counter|jetton|nft` for a fresh project.
- Useful `acton new` flags:
  - `--name`, `--description`, `--license`
  - `--app` for the TypeScript/Vite app scaffold when the template supports it
  - `--hooks` for default project Git hooks
  - `--agents` for generated coding-agent guidance
- Use `acton init` to add Acton support to an existing directory.
- Useful `acton init` modes:
  - `acton init --create-app [path]` creates only the TypeScript app scaffold
  - `acton init --stdlib-only` refreshes only the bundled standard library
- `acton init` can patch default `[import-mappings]` into an existing manifest, but that rewrite may drop TOML comments and unknown keys.

## Build, compile, and wrappers

- `acton build [contract-name]`
  - Builds all contracts, or one contract plus transitive dependencies.
  - Common flags: `--clear-cache`, `--graph <path>`, `--out-dir <dir>`, `--gen-dir <dir>`, `--output-fift <dir>`, `--info`.
- `acton compile <file.tolk>`
  - Single-file compiler entrypoint.
  - Common flags: `--json`, `--base64-only`, `--boc <file>`, `--fift <file>`, `--source-map <file>`, `--abi <file>`, `--allow-no-entrypoint`, `--clear-cache`.
- `acton wrapper <contract-name>`
  - Generates Tolk wrappers from contract ABI.
  - Use `--test`, `--test-output`, or `--test-output-dir` for test stubs.
  - Use `--ts` for TypeScript wrappers via `gen-typescript-from-tolk`.
  - Do not combine `--ts` with test-stub generation.
- If ABI, storage, or message types changed, regenerate wrappers instead of hand-editing generated files.
- Wrapper output defaults come from `[wrappers.tolk]`, `[wrappers.typescript]`, and the `@wrappers` import mapping.

## Tests and quality gates

- Core entrypoint: `acton test [path]`.
- Common test flags:
  - `--filter <regex>`, `--include <glob>`, `--exclude <glob>`
  - `--fail-fast`
  - `--fuzz-seed <seed>`
  - `--verbose` for low-level executor logs
  - `--debug --debug-port <port>`
  - `--backtrace full`
  - `--reporter console|dot|teamcity|junit` or comma-separated combinations
  - `--junit-path <dir>`, `--junit-merge`
  - `--show-bodies`
  - `--clear-cache`
- Coverage:
  - `acton test --coverage --coverage-format lcov`
  - `acton test --coverage --coverage-format text`
  - `--coverage-file <path>`
  - `--coverage-minimum-percent <percent>`
  - `--coverage-include-wrappers`
  - `--coverage-include-tests`
- Gas profiling:
  - `acton test --snapshot build/gas-baseline.json`
  - `acton test --baseline-snapshot build/gas-baseline.json`
  - `acton test --baseline-snapshot build/gas-baseline.json --fail-on-diff`
- Mutation testing:
  - `acton test --mutate --mutate-contract <contract-name>`
  - `--mutation-diff worktree|ref|branch`
  - `--mutation-diff-ref <ref>`
  - `--mutation-levels critical,major,minor`
  - `--mutation-disable-rules <rule>`
  - `--mutation-rules-file <path>`
  - `--mutation-session-id <id>`
  - `--mutation-id <id>`
  - `--mutation-workers <n>`
  - `--mutation-minimum-percent <percent>`
- Fork tests:
  - `acton test --fork-net testnet|mainnet|custom:<name>`
  - `acton test --fork-net testnet --fork-block-number <seqno>`
- Test UI and traces:
  - `acton test --ui`
  - `acton test --ui --ui-port <port>`
  - `acton test --save-test-trace`
  - `acton test --save-test-trace <dir>`
- Defaults live in `[test]`, `[test.coverage]`, `[test.fuzz]`, and `[test.mutation]`. CLI flags override config for the current run.

## Linting, formatting, and hooks

- `acton check [target]`
  - Checks a project, contract name, or `.tolk` file.
  - Common flags: `--fix`, `--output-format plain|json|sarif|github|gitlab`, `--output-file <path>`, `--enable-only <code[,code...]>`, `--explain <rule>`.
- Lint config lives in `[lint]`, `[lint.rules]`, and `[lint.rules.<contract-name>]`.
- Inline suppressions use `// check-disable-next-line ...`.
- `acton fmt [paths...]`
  - Formats sources.
  - Use `acton fmt --check` in CI.
  - Defaults live in `[fmt]`.
- `acton hooks new|install|status|uninstall`
  - Manages project-local Git hooks under `.githooks`.
- Typical CI gates:
  - `acton build`
  - `acton test --reporter console,junit`
  - `acton check --output-format github`
  - `acton fmt --check`

## Scripts, deployment, and network reads

- `acton script <path> [args...]` runs a standalone Tolk script.
- There is no `acton deploy` command. Deployment is script-driven.
- Safe execution sequence for state-changing scripts:
  1. `acton build`
  2. `acton test`
  3. `acton script <path>` to emulate locally
  4. `acton script <path> --net testnet`
  5. only after testnet validation, `acton script <path> --net mainnet`
- `--net <network>` broadcasts real transactions to `testnet`, `mainnet`, or `custom:<name>`. If `--net` is omitted, execution stays local.
- `--fork-net <network>` reads remote state while executing locally. When `--net` is set, omitted `--fork-net` defaults to the selected network for reads.
- Common script flags: `--debug`, `--debug-port`, `--backtrace full`, `--verbose`, `--clear-cache`, `--fork-net`, `--fork-block-number`, `--net`, `--explorer tonscan|toncx|dton|tonviewer`, `--show-bodies`.
- `acton run <script-name> [args...]` runs entries from `[scripts]` in `Acton.toml`.
- Script arguments are parsed against `main()` ABI. Use `--` before forwarded args that look like Acton flags.
- Built-in network API keys are environment variables, usually loaded from `.env`:
  - `TONCENTER_TESTNET_API_KEY`
  - `TONCENTER_MAINNET_API_KEY`
  - `<NORMALIZED_NAME>_API_KEY` for `custom:<name>`

## Wallets, verification, and inspection

- Wallets:
  - `acton wallet new`
  - `acton wallet import`
  - `acton wallet list`
  - `acton wallet export-mnemonic`
  - `acton wallet sign`
  - `acton wallet remove`
  - `acton wallet airdrop`
- Prefer secure keyring storage when available. Use `mnemonic-env` for CI and never commit plaintext wallet files or mnemonics.
- Verification:
  - `acton verify [contract-name] --address <addr> --net testnet|mainnet`
  - Useful flags: `--wallet <name>`, `--compiler-version <version>`, `--dry-run`.
- RPC inspection:
  - `acton rpc info <address>`
  - `acton rpc block`
  - `acton rpc block-number`
  - `acton rpc trace <hash>`
- On-chain libraries:
  - `acton library publish`
  - `acton library fetch`
  - `acton library info`
  - `acton library topup`
- Low-level tools:
  - `acton disasm [boc-file]`
  - `acton retrace <tx-hash>`
  - `acton doc tvm <query...>`
  - `acton func2tolk <path>`
  - `acton ls --stdio` or `acton ls --port <port>`
  - `acton completions bash|elvish|fish|powershell|zsh|nushell`

## Safety and correctness rules

- Warn once before `acton script --net mainnet`, `acton verify`, `acton library publish`, or `acton library topup`.
- State wallet, network, project-root, and Acton version assumptions explicitly when they affect the result.
- Do not invent commands or flags. Verify with `acton help <command>` when unsure.
- Do not use old examples with `acton litenode`, `[mappings]`, `--broadcast`, `--api-key`, or `acton up --canary` unless the user's installed binary explicitly supports them.
- Use TON docs for blockchain concepts that Acton docs do not cover; use Acton docs for CLI behavior.
