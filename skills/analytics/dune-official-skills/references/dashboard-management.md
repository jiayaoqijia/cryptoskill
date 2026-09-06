# Dashboard Management

> **Prerequisite:** Read the [main skill](../SKILL.md) for authentication, global flags, and key concepts.

Manage Dune dashboards -- create, retrieve, update, and archive.

```bash
dune dashboard <subcommand> [flags]
```

Alias: `dune dash`

---

## dashboard create

Create a new dashboard with optional visualization and text widgets.

```bash
dune dashboard create --name <NAME> [flags]
```

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | Yes | -- | Dashboard display name |
| `--private` | `bool` | No | `false` | Make the dashboard private |
| `--visualization-ids` | `[]int64` | No | -- | Comma-separated visualization IDs to add |
| `--text-widgets` | `string` | No | -- | JSON array of text widgets: `[{"text":"# Title"}]` |
| `--columns-per-row` | `int` | No | `2` | Visualizations per row: 1, 2, or 3 |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Output

- **text**: `Created dashboard <id>\n<url>`
- **json**: Full `DashboardResponse` object with all widget details

### Examples

```bash
# Empty dashboard
dune dashboard create --name "My Dashboard" -o json

# Dashboard with visualizations (2 per row)
dune dashboard create --name "DEX Overview" --visualization-ids 111,222,333 -o json

# Dashboard with text header and full-width visualizations
dune dashboard create --name "ETH Analysis" \
  --text-widgets '[{"text":"# Ethereum Analysis\nDaily metrics and trends"}]' \
  --visualization-ids 111,222 --columns-per-row 1 -o json

# Private dashboard
dune dashboard create --name "Internal Metrics" --private -o json
```

### Tips

- Create visualizations first with `dune viz create`, then reference their IDs here.
- Use `--columns-per-row 1` for detailed full-width charts, `3` for compact counter grids.
- Text widgets always span the full width and appear above visualizations.

> [!CAUTION]
> This is a **write** command -- it creates a resource in the user's Dune account.

---

## dashboard get

Fetch a dashboard's metadata, widgets, and URL.

```bash
dune dashboard get <dashboard_id>
dune dashboard get --owner <handle> --slug <slug>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `dashboard_id` | `integer` | The numeric ID of the dashboard (positional) |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--owner` | `string` | No | -- | Owner username or team handle (use with --slug) |
| `--slug` | `string` | No | -- | Dashboard URL slug (use with --owner) |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

Provide either a positional `dashboard_id` OR both `--owner` and `--slug`.

### Output

**text** format displays a summary table with ID, name, slug, privacy, tags, URL, and widget counts.

**json** format returns the full `DashboardResponse` object including all visualization and text widgets with their positions.

### Examples

```bash
# Get by ID
dune dashboard get 12345 -o json

# Get by owner and slug (from URL: dune.com/alice/my-dashboard)
dune dashboard get --owner alice --slug my-dashboard -o json
```

### Tips

- **Always call this before updating.** The update command uses all-or-nothing widget replacement -- you need the current state to preserve existing widgets.
- Use `-o json` to extract widget IDs and positions for the update command.

---

## dashboard update

Update an existing dashboard. At least one flag must be provided.

```bash
dune dashboard update <dashboard_id> [flags]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `dashboard_id` | `integer` | The numeric ID of the dashboard to update |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | No | -- | New dashboard name |
| `--slug` | `string` | No | -- | New URL slug (auto-generated from name if omitted) |
| `--private` | `bool` | No | -- | Set dashboard privacy |
| `--tags` | `[]string` | No | -- | Replace all tags (comma-separated) |
| `--visualization-widgets` | `string` | No | -- | Visualization widgets JSON (replaces all) |
| `--text-widgets` | `string` | No | -- | Text widgets JSON (replaces all) |
| `--param-widgets` | `string` | No | -- | Param widgets JSON (replaces all, pass through from get) |
| `--columns-per-row` | `int` | No | `2` | Visualizations per row (for auto-layout) |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

Only the provided flags are updated; omitted fields remain unchanged.

### Widget Replacement

**IMPORTANT:** Widget updates are all-or-nothing. When you provide `--visualization-widgets`, `--text-widgets`, or `--param-widgets`, ALL existing widgets of ALL types are replaced. To preserve widgets:

1. Fetch current state: `dune dashboard get <id> -o json`
2. Modify the widget arrays as needed
3. Pass the complete desired state back via the flags — include `param_widgets` from the get output to preserve dashboard parameters

**Param widget preservation:** When you change visualization or text widgets but omit `--param-widgets`, existing param widgets are preserved automatically. Only provide `--param-widgets` when you need to explicitly change them.

### Widget JSON Format

```bash
# Visualization widgets (auto-layout)
--visualization-widgets '[{"visualization_id":111},{"visualization_id":222}]'

# Visualization widgets (preserve positions from get output)
--visualization-widgets '[{"visualization_id":111,"position":{"row":0,"col":0,"size_x":3,"size_y":8}}]'

# Text widgets
--text-widgets '[{"text":"# Section Header"},{"text":"Description text"}]'

# Param widgets (pass through from get output to preserve)
--param-widgets '[{"id":"uuid","key":"param_name","query_id":123,"visualization_widget_id":456,"options":"{}","unique_param_key":"key"}]'
```

### Output

- **text**: `Updated dashboard <id>`
- **json**: Full `DashboardResponse` object

### Examples

```bash
# Update name only
dune dashboard update 12345 --name "New Name" -o json

# Update tags
dune dashboard update 12345 --tags blockchain,defi,ethereum -o json

# Make private
dune dashboard update 12345 --private -o json

# Replace all widgets
dune dashboard update 12345 \
  --text-widgets '[{"text":"# Updated Header"}]' \
  --visualization-widgets '[{"visualization_id":111},{"visualization_id":222}]' \
  --columns-per-row 1 -o json
```

> [!CAUTION]
> This is a **write** command -- it modifies an existing resource. Widget updates replace ALL existing widgets.

---

## dashboard archive

Archive a dashboard. Archived dashboards are hidden from public view but can be restored.

```bash
dune dashboard archive <dashboard_id>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `dashboard_id` | `integer` | The numeric ID of the dashboard to archive |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Output

- **text**: `Archived dashboard <id>`
- **json**: `{"ok": true, "dashboard_id": <id>}`

### Examples

```bash
dune dashboard archive 12345 -o json
```

> [!CAUTION]
> This is a **destructive** command -- it archives the dashboard and deletes associated scheduled refresh jobs.

---

## See Also

- [query-management.md](query-management.md) -- Create queries to power dashboard visualizations
- [query-execution.md](query-execution.md) -- Execute queries and verify data before adding to dashboards
