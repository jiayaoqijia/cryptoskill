# Visualization Management

> **Prerequisite:** Read the [main skill](../SKILL.md) for authentication, global flags, and key concepts.

Create and manage visualizations on saved Dune queries.

```bash
dune visualization <subcommand> [flags]
dune viz <subcommand> [flags]         # alias
```

---

## viz create

Create a new visualization attached to an existing saved query.

```bash
dune viz create --query-id <ID> --name <NAME> --type <TYPE> --options '<JSON>' [flags]
```

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--query-id` | `integer` | Yes | -- | ID of the query to attach the visualization to |
| `--name` | `string` | Yes | -- | Visualization name, max 300 characters |
| `--type` | `string` | No | `table` | Visualization type (see below) |
| `--description` | `string` | No | `""` | Visualization description, max 1000 characters |
| `--options` | `string` | Yes | -- | JSON string of visualization options (see format below) |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Visualization Types

| Type | Description | Options documented below? |
|------|-------------|--------------------------|
| `chart` | Line, column, area, scatter, or pie (set via `globalSeriesType` in options) | Yes |
| `table` | Tabular data display | Yes |
| `counter` | Single-value counter display | Yes |
| `pivot` | Pivot table | No — option format undocumented |
| `cohort` | Cohort analysis | No — option format undocumented |
| `funnel` | Funnel visualization | No — option format undocumented |
| `choropleth` | Geographic heat map | No — option format undocumented |
| `sankey` | Flow diagram | No — option format undocumented |
| `sunburst_sequence` | Hierarchical sunburst | No — option format undocumented |
| `word_cloud` | Word cloud | No — option format undocumented |

> **Note:** Types marked "undocumented" are accepted by the API but their `--options` format is not yet documented. Stick to `chart`, `table`, and `counter` for reliable results.

> [!CAUTION]
> This is a **write** command -- it creates a resource in the user's Dune account.

---

## viz get

Retrieve detailed information about a visualization by its ID.

```bash
dune viz get <visualization_id> [flags]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `visualization_id` | `integer` | The numeric ID of the visualization to fetch |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Examples

```bash
# View a visualization's details
dune viz get 12345 -o json

# Inspect current options before updating
dune viz get 12345 -o json | jq '.options'
```

---

## viz list

List all visualizations attached to a query.

```bash
dune viz list --query-id <ID> [flags]
```

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--query-id` | `integer` | Yes | -- | ID of the query to list visualizations for |
| `--limit` | `integer` | No | `25` | Maximum number of results to return |
| `--offset` | `integer` | No | `0` | Number of results to skip |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Examples

```bash
# List all visualizations for a query
dune viz list --query-id 12345 -o json

# Paginate through results
dune viz list --query-id 12345 --limit 10 --offset 0 -o json
dune viz list --query-id 12345 --limit 10 --offset 10 -o json
```

---

## viz update

Update an existing visualization. Fetches the current state first, applies only the provided changes, and preserves unchanged fields.

```bash
dune viz update <visualization_id> [flags]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `visualization_id` | `integer` | The numeric ID of the visualization to update |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | No | -- | New visualization name (max 300 characters) |
| `--type` | `string` | No | -- | New visualization type (see [Visualization Types](#visualization-types)) |
| `--description` | `string` | No | -- | New description (max 1000 characters) |
| `--options` | `string` | No | -- | New visualization options JSON (see [Options Format](#options-format)) |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

At least one flag must be provided. Only the provided flags are updated; omitted fields remain unchanged.

> **Important:** The `--options` flag replaces the **entire** options object, not individual fields within it. To change a single option field, first fetch the current options with `dune viz get <id> -o json`, modify the JSON, then pass the full updated object to `--options`.

### Examples

```bash
# Rename a visualization
dune viz update 12345 --name "New Chart Name" -o json

# Change chart type and options
dune viz update 12345 --type counter \
  --options '{"counterColName":"count","rowNumber":1,"stringDecimal":0}' -o json

# Update description only
dune viz update 12345 --description "Updated weekly report chart" -o json
```

> [!CAUTION]
> This is a **write** command -- it modifies an existing resource in the user's Dune account.

---

## viz delete

Permanently delete a visualization. This action cannot be undone.

```bash
dune viz delete <visualization_id> [flags]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `visualization_id` | `integer` | The numeric ID of the visualization to delete |

### Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

### Examples

```bash
# Delete a visualization
dune viz delete 12345 -o json

# List first, then delete
dune viz list --query-id 12345 -o json
dune viz delete <id-from-list> -o json
```

> [!CAUTION]
> This is a **destructive** command -- it permanently deletes the visualization. There is no undelete. Use `dune viz get <id>` to inspect the visualization before deleting.

---

## Required Workflow (for creating visualizations)

> **You MUST follow this workflow every time.** Skipping step 1 is the #1 cause of broken visualizations.
>
> **Visualizations require saved (non-temporary) queries.** When creating a query that will have visualizations, do NOT use `--temp`. Temporary queries are auto-deleted and cannot have visualizations attached.

### Step 1: Run the query first (required for both column discovery AND rendering)

```bash
dune query run <query-id> -o json
```

This step is required for **two reasons**:
1. **Column discovery:** Look at `result.metadata.column_names` in the response — these are the **exact** column names you must use in `--options`. Column names are case-sensitive and may be auto-generated (e.g. `SELECT 1` produces `_col0`, not `1`).
2. **Rendering:** A visualization will show "No results available" until the query has been executed at least once. The embed page displays results from the latest execution — without one, there's nothing to render.

### Step 2: Build options using the discovered column names

Use the column names from step 1 to construct the `--options` JSON for your visualization type (see format below).

### Step 3: Create the visualization

```bash
dune viz create --query-id <id> --name "..." --type <type> --options '<json>' -o json
```

### Step 4: Verify the visualization renders

Open the returned URL to confirm it renders correctly.

---

## Options Format

> **Applies to:** `viz create --options` and `viz update --options`.

> **Critical:** The `--options` JSON must match the visualization type. Column names in options must match the actual query result column names exactly. Omitting required fields or using wrong column names produces broken visualizations.

### Minimum Required Templates

Copy the appropriate template, replace `<placeholders>` with actual column names from `result.metadata.column_names`:

**Counter** (minimum):
```json
{"counterColName":"<column>","rowNumber":1,"stringDecimal":0}
```

**Table** (minimum — one entry per column you want to show):
```json
{"columns":[{"name":"<column>","title":"<Display Name>","type":"normal","alignContent":"left","isHidden":false}]}
```

**Line/Column/Area/Scatter chart** (minimum):
```json
{"globalSeriesType":"line","sortX":true,"columnMapping":{"<x_column>":"x","<y_column>":"y"},"seriesOptions":{"<y_column>":{"type":"line","yAxis":0,"zIndex":0}},"xAxis":{"title":{"text":"<X Label>"}},"yAxis":[{"title":{"text":"<Y Label>"}}],"legend":{"enabled":true},"series":{"stacking":null}}
```
Change `"line"` to `"column"`, `"area"`, or `"scatter"` in both `globalSeriesType` and `seriesOptions[].type`.

**Pie chart** (minimum):
```json
{"globalSeriesType":"pie","sortX":true,"columnMapping":{"<category_column>":"x","<value_column>":"y"},"seriesOptions":{"<value_column>":{"type":"pie","yAxis":0,"zIndex":0}}}
```

---

### Counter Options

The simplest type — displays a single number from one row of the query results.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `counterColName` | `string` | Yes | Query result column to display |
| `rowNumber` | `integer` | Yes | 1-based row index (usually `1`) |
| `stringDecimal` | `integer` | No | Decimal places (default `0`) |
| `stringPrefix` | `string` | No | Prefix (e.g. `"$"`) |
| `stringSuffix` | `string` | No | Suffix (e.g. `"%"`, `" ETH"`) |
| `counterLabel` | `string` | No | Display label below the number |
| `coloredPositiveValues` | `boolean` | No | Color positive values green |
| `coloredNegativeValues` | `boolean` | No | Color negative values red |

```bash
dune viz create --query-id 12345 --name "Total Transfers" --type counter \
  --options '{"counterColName":"count","rowNumber":1,"stringDecimal":0,"counterLabel":"Total Transfers"}' -o json
```

### Table Options

Displays query results as a formatted table.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `itemsPerPage` | `integer` | No | Rows per page (default `25`) |
| `columns` | `array` | Yes | Column definitions (see below) |

Each column object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Query result column name (must match exactly) |
| `title` | `string` | Yes | Display header text |
| `type` | `string` | No | `"normal"` (default) or `"progressbar"` |
| `alignContent` | `string` | No | `"left"`, `"right"`, or `"center"` |
| `isHidden` | `boolean` | No | Hide this column |
| `numberFormat` | `string` | No | Numeral.js format for numbers (e.g. `"$0,0.00"`) |
| `coloredPositiveValues` | `boolean` | No | Color positive numbers green |
| `coloredNegativeValues` | `boolean` | No | Color negative numbers red |

```bash
dune viz create --query-id 12345 --name "Top Wallets" --type table \
  --options '{"itemsPerPage":25,"columns":[{"name":"address","title":"Wallet","type":"normal","alignContent":"left","isHidden":false},{"name":"balance","title":"Balance (ETH)","type":"normal","alignContent":"right","isHidden":false,"numberFormat":"0,0.0000"}]}' -o json
```

### Chart Options (line, column, area, scatter)

2D charts require mapping query columns to axes.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `globalSeriesType` | `string` | Yes | `"line"`, `"column"`, `"area"`, or `"scatter"` |
| `sortX` | `boolean` | Yes | Sort x-axis values (usually `true`) |
| `columnMapping` | `object` | Yes | Maps column names to `"x"` or `"y"` |
| `seriesOptions` | `object` | Yes | Per-series config (type, axis, display name) |
| `xAxis` | `object` | Yes | `{"title": {"text": "Label"}}` |
| `yAxis` | `array` | Yes | `[{"title": {"text": "Label"}}]` |
| `legend` | `object` | No | `{"enabled": true}` |
| `series` | `object` | No | `{"stacking": null}` or `{"stacking": "stack"}` |
| `numberFormat` | `string` | No | Numeral.js format for left y-axis labels |
| `numberFormatRightYAxisSeries` | `string` | No | Numeral.js format for right y-axis (line/area only, when using dual y-axis) |

`columnMapping` maps each query column to an axis role:
- Exactly **one** column mapped to `"x"` (the x-axis)
- One or more columns mapped to `"y"` (data series)

`seriesOptions` has one entry per y-column:
```json
{"<column_name>": {"type": "line", "yAxis": 0, "zIndex": 0, "name": "Display Name"}}
```

```bash
# Line chart with single series
dune viz create --query-id 12345 --name "Daily Volume" --type chart \
  --options '{"globalSeriesType":"line","sortX":true,"columnMapping":{"day":"x","volume":"y"},"seriesOptions":{"volume":{"type":"line","yAxis":0,"zIndex":0,"name":"Volume"}},"xAxis":{"title":{"text":"Day"}},"yAxis":[{"title":{"text":"Volume (USD)"}}],"legend":{"enabled":true},"series":{"stacking":null}}' -o json

# Stacked column chart with multiple series
dune viz create --query-id 12345 --name "Volume by Chain" --type chart \
  --options '{"globalSeriesType":"column","sortX":true,"columnMapping":{"day":"x","eth_vol":"y","arb_vol":"y"},"seriesOptions":{"eth_vol":{"type":"column","yAxis":0,"zIndex":0,"name":"Ethereum"},"arb_vol":{"type":"column","yAxis":0,"zIndex":0,"name":"Arbitrum"}},"xAxis":{"title":{"text":"Day"}},"yAxis":[{"title":{"text":"Volume"}}],"legend":{"enabled":true},"series":{"stacking":"stack"}}' -o json
```

### Chart Options (pie)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `globalSeriesType` | `string` | Yes | Must be `"pie"` |
| `sortX` | `boolean` | Yes | Usually `true` |
| `columnMapping` | `object` | Yes | One column → `"x"` (categories), one → `"y"` (values) |
| `seriesOptions` | `object` | Yes | Config for the value column |
| `showDataLabels` | `boolean` | No | Show percentage labels on slices |
| `numberFormat` | `string` | No | Numeral.js format for values |

```bash
dune viz create --query-id 12345 --name "Volume by Chain" --type chart \
  --options '{"globalSeriesType":"pie","sortX":true,"showDataLabels":true,"columnMapping":{"chain":"x","volume":"y"},"seriesOptions":{"volume":{"type":"pie","yAxis":0,"zIndex":0,"name":"Volume"}}}' -o json
```

---

## Numeral.js Format Reference

Use these in `numberFormat`, `stringPrefix`/`stringSuffix` fields:

| Format | Example | Use Case |
|--------|---------|----------|
| `"0,0"` | 1,234 | Integer with thousands separator |
| `"0,0.00"` | 1,234.56 | Two decimal places |
| `"0.0a"` | 1.2k | Abbreviated (k/m/b) |
| `"$0,0.00"` | $1,234.56 | USD currency |
| `"0%"` | 50% | Percentage |
| `"0.00%"` | 50.00% | Percentage with decimals |

---

## Common Mistakes

1. **Using a temporary query**: Visualizations only work on saved (non-temp) queries. If you created the query with `--temp`, recreate it without `--temp` before adding a visualization.
2. **Not running the query first**: You MUST run `dune query run <id> -o json` first to discover actual column names from `result.metadata.column_names`. Never guess column names — `SELECT 1` produces `_col0`, `SELECT count(*) FROM x` produces `_col0`, etc. Only `SELECT x AS my_name` gives predictable names.
3. **Empty options**: `--options '{}'` always produces a broken visualization that shows errors when opened
4. **Wrong column names**: Column names in options must match query result columns exactly (case-sensitive)
5. **Missing columnMapping**: Charts require `columnMapping` with at least one `"x"` and one `"y"` entry
6. **Counter row number**: `rowNumber` is 1-based, not 0-based
7. **Chart type vs globalSeriesType**: Use `--type chart` for all chart subtypes, then set `globalSeriesType` in options to `"line"`, `"column"`, `"area"`, `"scatter"`, or `"pie"`
8. **Deleting without checking first**: Always use `dune viz get <id>` or `dune viz list --query-id <id>` to verify the visualization before deleting. There is no undo.
9. **Updating options without fetching first**: When changing `--options`, use `dune viz get <id> -o json` to see the current options format, then provide a complete replacement. The `--options` flag replaces the entire options object, not individual fields within it.

---

## See Also

- [query-management.md](query-management.md) -- create and manage the queries that visualizations are attached to
- [query-execution.md](query-execution.md) -- execute queries to generate data for visualizations
