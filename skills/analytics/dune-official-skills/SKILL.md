---
name: dune
description: "Dune CLI for querying blockchain and on-chain data via DuneSQL, searching decoded contract tables, managing saved queries, visualizations, dashboards, folders, schedules, query alerts, materialized views, contract decoding submissions, and the team's running queries, and monitoring credit usage on Dune. Use when user asks about blockchain data, on-chain analytics, token transfers, DEX trades, smart contract events, wallet balances, Ethereum/EVM chain queries, DuneSQL, visualizations, charts, dashboards, scheduling or alerting on a query, materialized views, decoding a contract, or what queries are running, or says \"query Dune\", \"search Dune datasets\", \"run a Dune query\", \"create a dashboard\", \"manage dashboard\", \"alert me\", or \"cancel my query\"."
compatibility: Requires network access and the Dune CLI (auto-installed on first use). Works on macOS, Linux, and Windows.
allowed-tools: Bash(dune:*) Bash(curl:*) Read
metadata:
  author: duneanalytics
  version: "1.1.0"
  cli_version: "0.1"
---

## Prerequisites

Assume the Dune CLI is already installed and authenticated. **Do not** run upfront install or auth checks. Just execute the requested `dune` command directly.

If a `dune` command fails, inspect the error to determine the cause and follow the recovery steps in [install-and-recovery.md](references/install-and-recovery.md):

- **"command not found"** → CLI not installed. See [CLI Not Found Recovery](references/install-and-recovery.md#cli-not-found-recovery).
- **401 / "unauthorized" / "missing API key"** → Auth failure. See [Authentication Failure Recovery](references/install-and-recovery.md#authentication-failure-recovery).
- **Unknown subcommand or flag / unexpected output** → Possible version mismatch. See [Version Compatibility](references/install-and-recovery.md#version-compatibility). This skill is written for CLI v0.1.24: if a command listed below is unknown, ask the user to update (`brew upgrade dune-cli`, or rerun the install script).
- **Credit, rate-limit, or billing error** → Show the error and the links the CLI prints after it. Do not retry until the user changes their plan or the credits renew.

# Dune CLI

A command-line interface for [Dune](https://dune.com) -- the leading blockchain data platform. Use it to write and execute DuneSQL queries against on-chain data, discover datasets, chart results, build dashboards, organize content in folders, schedule queries and alerts, materialize results into tables, submit contracts for decoding, see and cancel the team's runs, search documentation, and monitor credit usage.

Commands run as the API key's owner (a user or a team) and use its credits. New queries and dashboards are public unless created with `--private` or the team makes them private by default.

## Authentication

All commands except `docs search` require authentication via a Dune API key. The key is resolved in this priority order:

```bash
# 1. Flag (highest priority -- overrides everything)
dune query run 12345 --api-key <key>

# 2. Environment variable
export DUNE_API_KEY=<key>
dune query run 12345

# 3. Saved config file (lowest priority)
dune auth --api-key <key>        # saves to ~/.config/dune/config.yaml
dune query run 12345              # uses saved key
```

To save your key interactively (prompted from stdin):

```bash
dune auth
```

Config file location: `~/.config/dune/config.yaml`

## Global Flags

| Flag | Description |
|------|-------------|
| `--api-key <KEY>` | Dune API key (overrides `DUNE_API_KEY` env var and saved config) |

### Output Format (per-command flag)

Most commands support `-o, --output <FORMAT>` with values `text` (default, human-readable tables) or `json` (machine-readable).

> **Always use `-o json`** on every command that supports it. JSON output contains more detail than `text` (full API response objects vs. summarized tables) and is unambiguous to parse. The `text` format is for human terminal use and drops fields.

## DuneSQL

Dune uses **DuneSQL**, a Trino-based SQL dialect, as its query engine. Key points:

- All SQL passed to `--sql` flags or saved queries must be valid DuneSQL
- DuneSQL supports standard SQL with extensions for blockchain data types (addresses, hashes, etc.)
- See [dunesql-cheatsheet.md](references/dunesql-cheatsheet.md) for common types, functions, patterns, and pitfalls
- Use `dune docs search --query "DuneSQL functions"` to look up syntax and functions
- Reference docs: [Writing Efficient Queries](https://docs.dune.com/query-engine/writing-efficient-queries), [Functions and Operators](https://docs.dune.com/query-engine/Functions-and-operators)

## Key Concepts

### Performance Tiers

Available tiers: `small`, `medium`, `large`. **Do not pass `--performance` by default** — omit it and the API auto-selects. Only provide it when:

- The user explicitly requests a tier
- The query is clearly complex (heavy joins, large aggregations)
- A previous run returned a timeout or resource-limit error

Schedules, alerts, and materialized views need a tier (`schedule set` and `query alert` require `--performance`). If Dune rejects a tier ("Unsupported performance" or "not available with your subscription"), the account's plan does not include it: tell the user and offer the next tier up instead of retrying.

### Execution States

After submitting a query, the execution progresses through these states:

| State | Meaning | Action |
|-------|---------|--------|
| `QUERY_STATE_PENDING` | Queued for execution | Wait |
| `QUERY_STATE_EXECUTING` | Currently running | Wait |
| `QUERY_STATE_COMPLETED` | Results available | Fetch results |
| `QUERY_STATE_FAILED` | Execution failed | Check error message; fix SQL and retry |
| `QUERY_STATE_CANCELLED` | Cancelled by user or system | Re-execute if needed |

### Dataset Categories

| Category | Description |
|----------|-------------|
| `canonical` | Core blockchain data (blocks, transactions, traces, logs) |
| `decoded` | ABI-decoded contract data (events and function calls) |
| `spell` | Dune Spellbook transformations (curated, higher-level tables like `dex.trades`) |
| `community` | Community-contributed datasets |

### Dataset Types

| Type | Description |
|------|-------------|
| `dune_table` | Core Dune-maintained tables |
| `decoded_table` | Contract ABI-decoded tables |
| `spell` | Spellbook transformation tables |
| `uploaded_table` | User-uploaded CSV/data tables |
| `transformation_table` | Materialized transformation tables |
| `transformation_view` | Virtual transformation views |

### Query Parameters

Parameters let you create reusable queries with variable inputs. Pass them as `--param key=value` (repeatable). The API auto-detects the type, but parameters support these types: `text`, `number`, `datetime`, `enum`.

```bash
dune query run 12345 --param wallet=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --param days=30 -o json
```

## Command Overview

Aliases: `dune viz` = `dune visualization`, `dune dash` = `dashboard`, `dune mv` = `matview`. **W** marks write commands (confirm first; see [Security](#security)).

| Command | Description | |
|---------|-------------|--|
| `dune auth` | Save the API key to the config file | |
| `dune whoami` | Show the account of the current API key | |
| `dune dataset search` | Search the Dune dataset catalog | |
| `dune dataset search-by-contract` | Find decoded tables for a contract address | |
| `dune dataset blockchains` | List blockchains with table counts | |
| `dune dataset size <table>` | Storage size of a table and the tables under it | |
| `dune query run-sql` | Run raw DuneSQL without saving a query | |
| `dune query search` | Find saved queries by name | |
| `dune query get <id>` | A saved query's SQL, metadata, and latest execution | |
| `dune query create` | Save a new query | W |
| `dune query create-and-run` | Save a query, run it, optionally chart it, show rows | W |
| `dune query update <id>` | Change SQL, name, privacy, tags, or parameters | W |
| `dune query archive <id>` | Archive a saved query | W |
| `dune query run <id>` | Run a saved query | |
| `dune query alert <id>` | Schedule a query and notify on rows | W |
| `dune execution results <id>` | Fetch, filter, sort, or sample an execution's rows | |
| `dune execution list` | The team's active or recently finished runs (team key) | |
| `dune execution cancel <id>` | Stop one of the team's runs (team key) | W |
| `dune viz create` | Create a chart, counter, or table on a saved query | W |
| `dune viz get <id>` | A visualization's details and chart links | |
| `dune viz list` | A query's visualizations | |
| `dune viz update <id>` | Change name, description, counter label, or chart | W |
| `dune viz delete <id>` | Permanently delete a visualization | W |
| `dune dashboard search` | Find dashboards by name | |
| `dune dashboard get <id>` | A dashboard's metadata and widgets | |
| `dune dashboard create` | Create a dashboard | W |
| `dune dashboard update <id>` | Change metadata, or replace all widgets | W |
| `dune dashboard update-widget <id>` | Move or resize one widget, or edit a text widget | W |
| `dune dashboard image <id>` | Save a JPEG of the dashboard to check its layout | |
| `dune dashboard archive <id>` | Archive a dashboard | W |
| `dune folder list` / `dune folder get <id>` | Browse library folders | |
| `dune folder create` / `dune folder update <id>` | Create or restyle a folder | W |
| `dune folder move <id>` / `dune folder move-content` | Move a folder, or move queries and dashboards into one | W |
| `dune folder delete <id>` | Delete a folder (`--recursive` archives its content) | W |
| `dune schedule list` | List schedules | |
| `dune schedule set` / `dune schedule delete` | Create, replace, or delete a query or dashboard schedule | W |
| `dune matview list` / `dune matview get <name>` | Browse materialized views | |
| `dune matview create` / `dune matview update <name>` / `dune matview refresh <name>` | Create, change, or refresh a materialized view | W |
| `dune matview delete <name>` | Permanently delete a materialized view | W |
| `dune contract submit` | Submit contracts for decoding | W |
| `dune contract submissions` | Track decoding submissions | |
| `dune docs search` | Search Dune documentation (no API key needed) | |
| `dune usage` | Credit and storage usage | |

## Common Workflows

### Ad-hoc SQL Analysis

```bash
# Run a one-off query directly
dune query run-sql --sql "SELECT block_number, block_time FROM ethereum.blocks ORDER BY block_number DESC LIMIT 5" -o json
```

### Discover Tables, Then Query

```bash
# 1. Find relevant tables with column schemas
dune dataset search --query "uniswap swaps" --categories decoded --include-schema -o json

# 2. Write and execute SQL using discovered table/column names
dune query run-sql --sql "SELECT * FROM uniswap_v3_ethereum.evt_Swap LIMIT 10" -o json
```

### Find Contract Tables, Then Query

```bash
# 1. Find decoded tables for a specific contract
dune dataset search-by-contract --contract-address 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 --include-schema -o json

# 2. Query the discovered tables
dune query run-sql --sql "SELECT * FROM uniswap_v3_ethereum.evt_Transfer LIMIT 10" -o json
```

### Save and Execute a Reusable Query

```bash
# 1. Create a saved query with parameters
dune query create --name "Top Wallets" --sql "SELECT address, balance FROM ethereum.balances WHERE balance > {{min_balance}} LIMIT {{row_limit}}" -o json

# 2. Run it with parameter values
dune query run <returned-id> --param min_balance=1000 --param row_limit=50 -o json
```

### Long-Running Query (Submit and Poll)

```bash
# 1. Submit without waiting
dune query run 12345 --no-wait --performance large -o json
# Output: {"execution_id": "01ABC...", "state": "QUERY_STATE_PENDING"}

# 2. Check results later
dune execution results 01ABC... -o json
```

### Build a Dashboard from Scratch

```bash
# 1. Create queries for each section
QUERY_ID=$(dune query create --name "Daily Volume" --sql "SELECT date_trunc('day', block_time) AS day, SUM(amount) AS volume FROM trades GROUP BY 1 ORDER BY 1" -o json | jq -r '.query_id')

# 2. Execute to verify data
dune query run $QUERY_ID -o json

# 3. Create visualizations for each query
VIZ_ID=$(dune viz create --query-id $QUERY_ID --name "Daily Volume Chart" --type chart --options '{"globalSeriesType":"line","columnMapping":{"day":"x","volume":"y"}}' -o json | jq -r '.id')

# 4. Assemble the dashboard
dune dashboard create --name "Trading Dashboard" \
  --text-widgets '[{"text":"# Trading Dashboard\nDaily volume and metrics"}]' \
  --visualization-ids $VIZ_ID -o json
```

### Update a Dashboard (Preserve Existing Widgets)

```bash
# 1. Fetch current state
dune dashboard get 12345 -o json > dashboard.json

# 2. Modify as needed (add a new visualization widget)
# 3. Pass the complete widget state back
dune dashboard update 12345 \
  --visualization-widgets '[{"visualization_id":111},{"visualization_id":222},{"visualization_id":333}]' \
  -o json
```

### Check a Dashboard's Layout

```bash
# 1. Render it and look at the image
dune dashboard image 12345 --file layout.jpg -o json

# 2. Fix one widget without touching the others (IDs from `dune dashboard get 12345 -o json`)
dune dashboard update-widget 12345 --widget-type visualization --widget-id 678 --row 0 --col 0 --size-x 6 --size-y 8 -o json
```

### Alert When a Query Returns Rows

```bash
# The query should return rows only when the event happened in the last period
dune query alert 12345 --cron "0 * * * *" --performance small --email me@example.com -o json

# Stop it: deleting the schedule deletes the alert
dune schedule delete --query-id 12345 -o json
```

### Read the Last Result Without Re-running

```bash
EXEC_ID=$(dune query get 12345 -o json | jq -r '.latest_execution_id // empty')
dune execution results "$EXEC_ID" --limit 100 -o json
```

### See and Stop the Team's Runs

```bash
dune execution list -o json
dune execution cancel <execution-id> --yes -o json   # only after the user confirms
```

## Limitations

- `renderVisualization` (an interactive chart inside a chat client) exists only in the Dune MCP. Share the chart URL from `dune viz get` instead.

## Security

- **Never** output API keys or tokens in responses. Before presenting CLI output to the user, scan for strings that look like API keys (e.g. long alphanumeric tokens, strings prefixed with `dune_`, or values from `DUNE_API_KEY`). Redact them with `[REDACTED]`.
- **Always** confirm with the user before running write commands (marked **W** in the [Command Overview](#command-overview)). Schedules, alerts, and materialized views also spend credits on every run, so confirm the frequency and tier.
- **Never** pass `--yes` to `dune execution cancel` until the user has confirmed the run: a shared run stops for everyone on it.
- **Never** print webhook URLs; pass them to `dune query alert` as `@path` or `@-`. Chart URLs of private queries carry an API key: do not share them.
- **Always** use `-o json` on every command -- JSON output is more detailed and reliably parseable
- Use `--temp` when creating throwaway queries to avoid cluttering the user's saved queries
- **Never** pass `--api-key` on the command line when other users might see the terminal history. Prefer `dune auth` or the `DUNE_API_KEY` environment variable.

## Reference Documents

Load the relevant reference when you need detailed command syntax and flags:

| Task | Reference |
|------|-----------|
| Search, create, create-and-run, get, update, archive, or alert on saved queries | [query-management.md](references/query-management.md) |
| Execute queries, fetch results, or list and cancel the team's runs | [query-execution.md](references/query-execution.md) |
| Search datasets, find tables for a contract, list blockchains, or check table size | [dataset-discovery.md](references/dataset-discovery.md) |
| Search documentation or check account usage | [docs-and-usage.md](references/docs-and-usage.md) |
| DuneSQL types, functions, common patterns, and pitfalls | [dunesql-cheatsheet.md](references/dunesql-cheatsheet.md) |
| Create, get, update, delete, or list visualizations on saved queries | [visualization-management.md](references/visualization-management.md) |
| Search, create, get, update, edit a widget, render an image of, or archive dashboards | [dashboard-management.md](references/dashboard-management.md) |
| Organize queries and dashboards into folders | [folders.md](references/folders.md) |
| Schedule queries and dashboards, and set query alerts | [schedules-and-alerts.md](references/schedules-and-alerts.md) |
| Create and manage materialized views | [materialized-views.md](references/materialized-views.md) |
| Submit contracts for decoding and track submissions | [contract-decoding.md](references/contract-decoding.md) |
| CLI install, authentication, and version recovery | [install-and-recovery.md](references/install-and-recovery.md) |
