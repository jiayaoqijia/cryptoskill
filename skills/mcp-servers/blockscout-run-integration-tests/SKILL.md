---
name: run-integration-tests
description: >-
  Use this skill WHENEVER you are about to run the integration tests of this
  project — the whole suite, a single module, or one test. This includes any
  time you would otherwise type `pytest -m integration`, `uv run pytest -m
  integration`, run anything under `tests/integration/`, or want to check live
  Blockscout/Chainscout/BENS connectivity. Integration tests make real network
  calls with no hard HTTP timeout, so one unresponsive endpoint can hang a plain
  pytest run for an unbounded time and block you. This skill runs each test in
  an isolated subprocess with a per-test timeout, kills any hung test, and
  always returns a bounded report flagging which tests timed out or are slow.
  Prefer it over invoking pytest directly for integration tests.
---

# Run Integration Tests (timeout-protected)

## Why use this instead of plain pytest

Integration tests hit live external APIs and the HTTP client has **no hard
request timeout**. When an endpoint is slow or unresponsive, a single test can
hang indefinitely — a plain `pytest -m integration` run then blocks for an
unbounded time and so do you. (This is exactly how this project's suite started
taking 20+ minutes: a handful of tests hung for ~3 minutes each before being
killed manually.)

The bundled runner solves this by executing **each test in its own subprocess
with a per-test wall-clock timeout**. A hung test is killed and reported as
`TIMEOUT`; the run continues. You always get a complete, bounded report instead
of stalling.

## Usage

The runner lives at `scripts/run_integration_tests.py` (relative to the project
root, alongside the project's other tooling). Invoke it from the project root
with that path, or use its absolute path. The script finds the project root on
its own by walking up to the nearest `tests/integration` directory, so it can be
launched from anywhere.

Run it with the project venv (the script auto-detects whether to use `pytest`
directly inside the devcontainer or `uv run pytest` on the host):

```bash
uv run python scripts/run_integration_tests.py [TARGET ...] [--timeout N] [--slow-threshold S]
```

Inside the devcontainer (`/.dockerenv` exists) you may drop `uv run` and call
`python ...` directly — but `uv run python ...` works in both environments, so
prefer it when unsure.

### The three granularities

`TARGET` is passed straight to pytest's collector, so the same command covers
every scope:

**1. Whole suite** (no target → defaults to `tests/integration`):

```bash
uv run python scripts/run_integration_tests.py
```

**2. A single module** (a file, or a whole subdirectory):

```bash
# one file
uv run python scripts/run_integration_tests.py tests/integration/block/test_get_block_info_real.py
# a category directory
uv run python scripts/run_integration_tests.py tests/integration/transaction
```

**3. A single test** (a `file::test` node id):

```bash
uv run python scripts/run_integration_tests.py "tests/integration/block/test_get_block_info_real.py::test_get_block_info_integration"
```

You can also pass several targets at once.

### Options

- `--timeout N` — per-test wall-clock limit in seconds (default `120`). Lower it
  (e.g. `--timeout 30`) when you just want to fail fast on hangs; raise it only
  if a test legitimately needs longer.
- `--slow-threshold S` — flag completed tests slower than `S` seconds in the
  summary (default `10`).
- `--marker EXPR` — pytest marker to select (default `integration`).
- `--list` — only list the tests that would run, then exit. Useful to scope a
  run before launching it.

## Reading the output

Each test prints a live line as it finishes:

```
[  7/83] PASS         2.5s  tests/integration/...::test_x
[  8/83] TIMEOUT    120.0s  tests/integration/...::test_y
```

The summary at the end reports counts and three actionable lists:

- **TIMED OUT** — tests killed at the limit. These block the suite and are the
  first thing to investigate (usually a flaky/slow endpoint or a missing HTTP
  timeout in the tool code, not a bug in the test).
- **FAILED** — real assertion/error failures.
- **SKIPPED (reason)** — tests that skipped, each with the reason pytest reported
  (network unavailable, missing API key, external service down, …). A skip is an
  environment signal, not a pass, so read these before treating a run as clean.
- **SLOW** — tests that completed but exceeded `--slow-threshold`; candidates
  for optimization.

The script exits non-zero if anything failed or timed out, so it composes with
other tooling.

## Tips

- For routine development, scope to the module or test you're working on — it's
  much faster than the full suite and still timeout-protected.
- A `TIMEOUT` is not automatically a broken test. Live endpoints are sometimes
  temporarily slow; re-running often shows the same test passing in a couple of
  seconds. Treat persistent timeouts (across reruns) as the real signal.
- The runner isolates each test in its own pytest process, which adds a small
  per-test startup cost. That overhead is the deliberate price of guaranteed
  non-blocking behavior; it is negligible compared to a single hung test.
