# Query Management

> **Prerequisite:** Read the [main skill](../SKILL.md) for authentication, global flags, and key concepts.

Manage saved Dune queries -- create, retrieve, update, and archive.

```bash
dune query <subcommand> [flags]
```

---

## query create

Create a new saved query.

```bash
dune query create --name <NAME> --sql <SQL> [flags]
```

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | Yes | -- | Human-readable query title |
| `--sql` | `string` | Yes | -- | DuneSQL query text |
| `--description` | `string` | No | `""` | Short description of the query |
| `--private` | `bool` | No | `false` | Make the query private (not publicly visible); may be forced by team settings |
| `--temp` | `bool` | No | `false` | Create a temporary query (auto-deleted, not shown in saved queries) |
| `--folder-id` | `string` | No | -- | Save the query into this folder (see `dune folder list`) |
| `--folder-name` | `string` | No | -- | Save the query into the folder with this name |
| `--parameters` | `string` | No | -- | JSON array declaring `{{key}}` parameters: `[{"key":"days","type":"number","value":"30"}]`; type is text, number, date, or enum |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Output

- **text**: `Created query <id>`
- **json**: `{"query_id": <id>}`

### Examples

```bash
# Basic query
dune query create --name "Recent Blocks" --sql "SELECT block_number, block_time FROM ethereum.blocks ORDER BY block_number DESC LIMIT 10" -o json

# Private query with description
dune query create --name "Whale Tracker" \
  --sql "SELECT address, balance FROM ethereum.balances WHERE balance > 10000 ORDER BY balance DESC LIMIT 100" \
  --description "Track top ETH holders" \
  --private -o json

# Temporary query (for one-off analysis, not persisted to your saved queries)
dune query create --name "Quick Check" --sql "SELECT COUNT(*) FROM ethereum.transactions WHERE block_time > NOW() - INTERVAL '1' HOUR" --temp -o json

# Extract the query ID from JSON output
QUERY_ID=$(dune query create --name "My Query" --sql "SELECT 1" -o json | jq -r '.query_id')
```

### Tips

- Use `--temp` for throwaway queries to avoid cluttering your saved query list.
- Query IDs are integers. Save the returned ID to run the query later with `dune query run <id>`.
- All SQL must be valid DuneSQL syntax.

> [!CAUTION]
> This is a **write** command -- it creates a resource in the user's Dune account.

---

## query search

Find saved queries by name (not case-sensitive), in public queries and the private ones you or your team can access. Use it to get a query ID instead of asking the user for one.

```bash
dune query search --query <TEXT> [flags]
```

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--query` | `string` | Yes | -- | Text to find in the query name |
| `--owned-only` | `bool` | No | `false` | Only queries owned by the API key's user or team |
| `--limit` | `int` | No | `20` | Maximum results (1-50) |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune query search --query "dex volume" --owned-only -o json
```

---

## query create-and-run

Save a query, run it, optionally chart it, and show the first rows, in one call. Prefer it over `query create` + `query run` + `viz create` when the user wants a saved query and its results.

```bash
dune query create-and-run --name <NAME> --sql <SQL> [--chart-type <TYPE> --config <JSON>] [flags]
```

### Flags

Takes every `query create` flag, plus:

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | Yes | -- | Query title |
| `--sql` | `string` | Yes | -- | DuneSQL, `@path`, or `@-` |
| `--description` | `string` | No | -- | Query description |
| `--private` | `bool` | No | `false` | Make the query private |
| `--temp` | `bool` | No | `false` | Temporary query (cannot have a chart) |
| `--folder-id` | `string` | No | -- | Save into this folder |
| `--folder-name` | `string` | No | -- | Save into the folder with this name |
| `--parameters` | `string` | No | -- | Parameter declarations (JSON array) |
| `--performance` | `string` | No | (auto) | `small`, `medium`, or `large`; omit by default |
| `--limit` | `int` | No | `20` | Result rows to show (0-32000) |
| `--timeout` | `int` | No | `60` | Seconds to wait; on timeout it prints the IDs, so fetch rows later with `dune execution results` |
| `--chart-type` | `string` | No | -- | `column`, `line`, `area`, `scatter`, `pie`, `counter`, or `table` |
| `--config` | `string` | No | -- | Chart config JSON (see [visualization-management.md](visualization-management.md#chart-config)) |
| `--viz-name` | `string` | No | query name | Chart name |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune query create-and-run --name "Daily blocks" \
  --sql "SELECT date_trunc('day', time) AS day, count(*) AS blocks FROM ethereum.blocks WHERE time > now() - interval '7' day GROUP BY 1" \
  --chart-type line --config '{"chart_type":"line","x_axis":{"column":"day","title":"Day"},"y_axes":{"left":{"label_format":"0,0","series":[{"column":"blocks","title":"Blocks"}]},"right_enabled":false,"right_label_format":"","right_series":[]},"enable_legend":false,"stacked":false}' -o json
```

If the query, run, or chart fails, everything created so far is still printed and the command exits with an error.

> [!CAUTION]
> This is a **write** command, and the run uses credits.

---

## query alert

Put a saved query on a schedule and notify the user each time a run returns rows. Sets the query's schedule (creating it or replacing its frequency and tier) and creates or replaces the alert on the chosen channel.

```bash
dune query alert <query-id> --cron <EXPR> --performance <TIER> (--email <ADDR>... | --slack-webhook <URL> | --discord-webhook <URL> | --webhook <URL>)
```

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--cron` | `string` | Yes | -- | Supported 5-part UTC cron (see [schedules-and-alerts.md](schedules-and-alerts.md#supported-cron-expressions)) |
| `--performance` | `string` | Yes | -- | `small`, `medium`, or `large`; every run is charged at this tier |
| `--email` | `string` | One channel | -- | Address to notify; repeat for up to 5 |
| `--slack-webhook` | `string` | One channel | -- | Slack incoming webhook: inline, `@path`, or `@-` |
| `--discord-webhook` | `string` | One channel | -- | Discord webhook: inline, `@path`, or `@-` |
| `--webhook` | `string` | One channel | -- | HTTPS URL that receives a JSON POST per alert: inline, `@path`, or `@-` |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

- Write the query so it returns rows **only** when the event happened in the latest period (e.g. the last hour for an hourly schedule). Otherwise it alerts on every run.
- A query has one alert per channel; a new alert replaces that channel's alert.
- Webhook URLs are secrets: pass them as `@path` or `@-`, never inline in a command the user's history keeps.
- To stop the alert, delete the schedule: `dune schedule delete --query-id <id>`.

```bash
dune query alert 12345 --cron "0 * * * *" --performance small --email me@example.com -o json
```

> [!CAUTION]
> This is a **write** command. It changes the query's schedule, and every scheduled run uses credits.

---

## query get

Fetch a saved query's SQL, metadata, and execution state.

```bash
dune query get <query-id>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `query-id` | `integer` | The numeric ID of the query to fetch |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Output

**text** format displays (Description and Tags only shown when non-empty):

```
ID:          12345
Name:        My Query
Description: A useful query
Owner:       alice
Engine:      v2 DuneSQL
Version:     3
Private:     false
Archived:    false
Tags:        defi, ethereum

SQL:
  SELECT block_number, block_time
  FROM ethereum.blocks
  ORDER BY block_number DESC
  LIMIT 10
```

**json** format returns the full `GetQueryResponse` object with all fields.

### Examples

```bash
# View a query's details
dune query get 12345 -o json

# Extract SQL text from JSON output
dune query get 12345 -o json | jq -r '.query_sql'
```

---

## query update

Update an existing saved query. At least one flag must be provided.

```bash
dune query update <query-id> [flags]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `query-id` | `integer` | The numeric ID of the query to update |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | No | -- | New query name |
| `--sql` | `string` | No | -- | New DuneSQL query text |
| `--description` | `string` | No | -- | New description |
| `--private` | `bool` | No | -- | Set privacy flag |
| `--tags` | `[]string` | No | -- | Replace all tags (comma-separated) |
| `--parameters` | `string` | No | -- | Replace all parameters (JSON array, see `query create`) |
| `--archived` | `bool` | No | -- | `true` archives the query, `false` restores it |
| `--temp` | `bool` | No | -- | `true` makes the query temporary, `false` saves it to the library |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

Only the provided flags are updated; omitted fields remain unchanged.

### Output

- **text**: `Updated query <id>`
- **json**: `{"query_id": <id>}`

### Examples

```bash
# Update SQL only
dune query update 12345 --sql "SELECT * FROM ethereum.blocks LIMIT 20" -o json

# Update name and add tags
dune query update 12345 --name "Updated Query" --tags defi,ethereum,uniswap -o json

# Make a query private
dune query update 12345 --private -o json
```

> [!CAUTION]
> This is a **write** command -- it modifies an existing resource.

---

## query archive

Archive a saved query. Archived queries are hidden from the default query list but not deleted.

```bash
dune query archive <query-id>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `query-id` | `integer` | The numeric ID of the query to archive |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Output

- **text**: `Archived query <id>`
- **json**: `{"query_id": <id>}`

### Examples

```bash
dune query archive 12345 -o json
```

> [!CAUTION]
> This is a **destructive** command -- it archives the query. To unarchive, use the Dune web UI or API.

---

## See Also

- [query-execution.md](query-execution.md) -- Run queries and fetch execution results
- [dataset-discovery.md](dataset-discovery.md) -- Search for tables before writing SQL
- [visualization-management.md](visualization-management.md) -- Create and manage visualizations on saved queries
