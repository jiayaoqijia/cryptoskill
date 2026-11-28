# Materialized Views

> **Prerequisite:** Read the [main skill](../SKILL.md) for authentication, global flags, and key concepts.

Store a saved query's results as a table that other queries can read, optionally refreshed on a schedule. Alias: `dune mv`.

`create` takes a bare name (`result_token_summary`). `get`, `update`, `refresh`, and `delete` take the fully qualified name (`dune.<team>.result_token_summary`); `get` also takes the ID from `matview list -o json`.

---

## matview create

Requirements: the source query is saved (not `--temp`), has no parameters, and has the same owner. The name starts with `result_`, is 8-128 lowercase letters, digits, or underscores, and cannot change later. The matview has its source query's privacy. It runs the query immediately.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | Yes | -- | e.g. `result_token_summary` |
| `--query-id` | `int` | Yes | -- | Source query |
| `--performance` | `string` | No | (account default) | `small`, `medium`, or `large` |
| `--cron` | `string` | No | -- | Refresh schedule, 5-field cron, at least 15 minutes apart |
| `--expires-at` | `string` | No | -- | RFC 3339 time when the refresh schedule ends (needs `--cron`) |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune matview create --name result_daily_blocks --query-id 12345 --cron "0 */6 * * *" -o json
```

---

## matview list

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--limit` | `int` | No | `100` | Per page (max 1000) |
| `--offset` | `int` | No | `0` | Pagination offset |
| `--all` | `bool` | No | `false` | Fetch every page |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

---

## matview get

Show a matview's source query, privacy, size, recent execution IDs, and refresh schedule.

```bash
dune matview get dune.my_team.result_token_summary -o json
```

---

## matview update

Change the tier or refresh schedule. Re-runs the source query. Omitted settings are kept: the schedule stays unless you pass `--cron` or `--no-schedule`.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--performance` | `string` | No | -- | New tier |
| `--cron` | `string` | No | -- | Set or replace the refresh schedule |
| `--no-schedule` | `bool` | No | `false` | Remove the refresh schedule |
| `--expires-at` | `string` | No | -- | RFC 3339 time when the schedule ends |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

---

## matview refresh

Run the source query now and replace the table's contents. Uses credits.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--performance` | `string` | No | (account default) | `small`, `medium`, or `large` |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

---

## matview delete

Permanently delete the matview, its table, and its schedule. Cannot be undone.

```bash
dune matview delete dune.my_team.result_token_summary -o json
```

> [!CAUTION]
> `create`, `update`, and `refresh` are **write** commands that run the query and use credits. `delete` is **destructive**; confirm with the user first.

---

## See Also

- [schedules-and-alerts.md](schedules-and-alerts.md) -- `dune schedule list` also lists matview refreshes
