# Schedules and Alerts

> **Prerequisite:** Read the [main skill](../SKILL.md) for authentication, global flags, and key concepts.

Run saved queries and refresh dashboards on a schedule, and get notified when a scheduled query returns rows. A query or dashboard has at most one schedule. Every scheduled run uses credits at its tier: prefer `small` and the lowest frequency that meets the need.

---

## Supported Cron Expressions

5-part, UTC. Only these forms are accepted:

| Expression | Meaning |
|------------|---------|
| `*/15 * * * *`, `*/20 * * * *`, `*/30 * * * *` | Every 15, 20, or 30 minutes |
| `0 * * * *` | Hourly |
| `0 */N * * *` with N in 2, 3, 4, 6, 8, 12 | Every N hours |
| `M H * * *` | Daily at H:M |
| `M H * * D` | Weekly on day D (0 = Sunday) at H:M |

M is 0 or 30, and H is 0-23.

---

## schedule list

List the schedules that the API key's user or team owns: query executions, dashboard refreshes, and materialized view refreshes.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--limit` | `int` | No | `20` | Schedules to return (1-100) |
| `--offset` | `int` | No | `0` | Schedules to skip |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

---

## schedule set

Create or replace the schedule of a saved query or a dashboard. It replaces **every** setting, so check `dune schedule list` first and pass what should stay.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--query-id` | `int` | One of | -- | Saved query to schedule |
| `--dashboard-id` | `int` | One of | -- | Dashboard to refresh |
| `--cron` | `string` | Yes | -- | Supported cron expression (above) |
| `--performance` | `string` | Yes | -- | `small`, `medium`, or `large` |
| `--expires-at` | `string` | No | -- | RFC 3339 time when the schedule stops |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune schedule set --query-id 12345 --cron "0 6 * * *" --performance small -o json
```

On the free plan a schedule expires after at most 3 months.

---

## schedule delete

Delete the schedule of a query or dashboard. **Alerts on the query are deleted with it.** Succeeds when there is no schedule. To stop a materialized view's refresh, use `dune matview update --no-schedule`.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--query-id` | `int` | One of | -- | Query whose schedule to delete |
| `--dashboard-id` | `int` | One of | -- | Dashboard whose schedule to delete |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

---

## Alerts

`dune query alert` schedules a query and notifies the user by email, Slack, Discord, or webhook each time a run returns rows. See [query-management.md](query-management.md#query-alert).

```bash
dune query alert 12345 --cron "0 * * * *" --performance small --email me@example.com -o json
```

> [!CAUTION]
> `schedule set`, `schedule delete`, and `query alert` are **write** commands, and schedules spend credits on every run. Confirm the frequency and tier with the user.

---

## See Also

- [materialized-views.md](materialized-views.md) -- Scheduled refreshes of materialized views
