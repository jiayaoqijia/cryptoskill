# Troubleshooting

Use these checks before deeper debugging.

## Acton is missing

- Check `command -v acton`.
- If missing and the task requires the CLI, install it:
  - `curl -LsSf https://github.com/ton-blockchain/acton/releases/latest/download/acton-installer.sh | sh`
- Open a fresh shell or reload the shell profile if `acton` is still not on `PATH`.
- Verify with `acton --version`.

## Docs and CLI disagree

- Record the installed version with `acton --version`.
- Confirm the exact command syntax with `acton help <command>` or `acton <command> --help`.
- Use hosted docs for concepts and workflows, but follow the installed CLI for local execution.
- If the user wants latest behavior, update first with `acton up` or a fresh install.
- Treat these old names and flags as stale unless the installed binary explicitly supports them:
  - `acton litenode`
  - `[mappings]`
  - `--broadcast`
  - `--api-key`
  - `acton up --canary`

## Project root or manifest confusion

- Run `acton doctor`.
- Check `pwd`.
- Re-run with explicit project selection:
  - `acton --project-root /abs/path ...`
  - `acton --manifest-path /abs/path/Acton.toml ...`
- Remember:
  - project-root controls config-relative outputs like `.acton`, `build`, `gen`, traces, and configured wrapper paths
  - relative CLI path flags stay relative to the current working directory unless absolute

## Build or import resolution failures

- Run `acton build --clear-cache`.
- Confirm every `[contracts.<name>]` entry in `Acton.toml` has a valid `src`.
- Confirm dependency names in `depends` match real contract keys.
- Inspect `[import-mappings]`, not old `[mappings]`.
- If the project was added manually, run `acton init` to backfill default import mappings and `.gitignore`.
- If an existing manifest has comments or unknown keys, warn that `acton init` may rewrite `Acton.toml` and drop them.

## Wrapper generation problems

- Confirm the contract is declared in `Acton.toml`; `acton wrapper` takes a contract name, not a file path.
- Confirm the contract compiles cleanly with `acton build <contract-name>`.
- If wrapper methods are missing, inspect the contract header ABI:
  - `storage: ...`
  - `incomingMessages: ...`
- If `acton wrapper --ts` fails, verify Node.js, npm, and `npx` are installed.
- Do not combine `--ts` with `--test`, `--test-output`, or `--test-output-dir`.

## Test behavior differs from scripts

- Re-run a focused case:
  - `acton test --filter "<specific-test>" --backtrace full`
- Compare execution mode:
  - tests run locally unless they use `--fork-net`
  - scripts run locally unless they use `--net`
  - `--fork-net` reads remote state but keeps execution local
  - `--net` broadcasts transactions to the selected network
- If ABI changed, regenerate wrappers instead of debugging old generated code.

## Coverage, profiling, fuzzing, or reporter confusion

- Prefer current spellings:
  - `--coverage-format lcov|text`
  - `--coverage-file <path>`
  - `--coverage-minimum-percent <percent>`
  - `--coverage-include-wrappers`
  - `--coverage-include-tests`
  - `--reporter console|dot|teamcity|junit`
  - `--fuzz-seed <seed>`
- For gas regressions:
  - create a baseline with `acton test --snapshot build/gas-baseline.json`
  - compare with `acton test --baseline-snapshot build/gas-baseline.json`
  - enforce in CI with `--fail-on-diff`
- For mutation sessions:
  - use `--mutation-session-id <id>` to resume an interrupted run
  - use `--mutation-id <id>` to rerun specific mutants from a previous report

## Test UI will not start

- The selected port may be busy; retry with `acton test --ui --ui-port <port>`.
- If the test run fails before UI startup, run without `--ui` first to isolate compile or runtime errors.
- For coverage browsing in the UI, combine `acton test --coverage --ui`.

## Wallet, faucet, or network transaction issues

- Run `acton wallet list --balance`.
- Confirm the selected wallet exists in local or global config.
- Confirm the mnemonic source is available:
  - `mnemonic-env`
  - `mnemonic-file`
  - `mnemonic-keyring`
  - `mnemonic`
- Confirm expected addresses match the target network.
- Verify `--net` matches the funded wallet environment.
- Use `mnemonic-env` for CI instead of plaintext secrets.
- For real-network scripts, remember that `acton script <path> --net testnet|mainnet` is the broadcasting mode.

## TonCenter API keys and rate limits

- Acton reads API keys from environment variables, not `--api-key` flags:
  - `TONCENTER_TESTNET_API_KEY`
  - `TONCENTER_MAINNET_API_KEY`
  - `<NORMALIZED_NAME>_API_KEY` for `custom:<name>`
- Acton loads `.env` automatically during project work.
- Missing or rate-limited keys commonly affect:
  - `acton script --net ...`
  - `acton script --fork-net ...`
  - `acton verify`
  - `acton wallet list --balance`
  - `acton test --fork-net ...`
  - `acton disasm --address ...`
  - `acton retrace ...`
  - `acton rpc ...`

## Verification mismatch

- Rebuild locally with `acton build --clear-cache`.
- Confirm the deployed address matches the source revision you are using.
- Pass the compiler version if needed:
  - `acton verify <contract> --address <addr> --compiler-version <version>`
- Use `--dry-run` first when verifying unfamiliar deployments.

## RPC, disasm, or retrace problems

- For live-chain reads, provide the relevant API key through the environment.
- For readable disassembly, regenerate source maps:
  - `acton compile contract.tolk --source-map contract.json --boc contract.boc`
  - `acton disasm contract.boc --source-map contract.json --show-offsets`
- For source-level retrace, pass a contract name:
  - `acton retrace <tx-hash> --contract <contract-name> --debug`

## `func2tolk` or LSP failures

- `acton func2tolk` uses the npm-based converter; install Node.js/npm if conversion fails before Acton starts.
- Override converter version with `acton func2tolk <path> --version <version>` when needed.
- `acton ls` expects the project stdlib under `.acton/tolk-stdlib`; run `acton init` or `acton init --stdlib-only` if it is missing.

## Missing deploy command confusion

- Use `acton script scripts/deploy.tolk` for local emulation.
- Use `acton script scripts/deploy.tolk --net testnet|mainnet` for network deployment.
- Acton deployment is script-driven by design; there is no `acton deploy` command.
