# Folders

> **Prerequisite:** Read the [main skill](../SKILL.md) for authentication, global flags, and key concepts.

Organize saved queries and dashboards into library folders. Folder IDs are strings such as `dp180Cu3jW3L`.

```bash
dune folder <subcommand> [flags]
```

---

## folder list

List the folders directly under a path, with how many queries and dashboards each holds.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--parent-path` | `string` | No | `/` | Path whose subfolders to list, e.g. `/Research` |
| `--name-contains` | `string` | No | -- | Case-insensitive filter on the folder name |
| `--limit` | `int` | No | `50` | Maximum folders (1-100) |
| `--offset` | `int` | No | `0` | Folders to skip |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune folder list --name-contains research -o json
```

---

## folder get

Show one folder, its direct subfolders, and the queries and dashboards in it.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--limit` | `int` | No | `50` | Maximum items (1-100) |
| `--offset` | `int` | No | `0` | Items to skip |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune folder get dp180Cu3jW3L -o json
```

---

## folder create

Create a folder at the top level, or inside `--parent-id`. If one already exists at that path, the error names its ID; use that folder instead.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | Yes | -- | Folder name; no `/` |
| `--parent-id` | `string` | No | -- | Create inside this folder |
| `--description` | `string` | No | -- | What the folder holds |
| `--color` | `string` | No | `gray` | Preset (green, yellow, red, blue-light, gray, orange, blue, pink, mauve, amber) or hex |
| `--icon` | `string` | No | `folder` | Icon name; `dune folder create --help` lists them |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune folder create --name Research -o json
```

Save new queries into it with `dune query create --folder-id <id>`.

---

## folder update

Rename a folder or change its description, icon, or color. Omitted flags keep their value; an empty `--description` clears it.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--name` | `string` | No | -- | New name; no `/` |
| `--description` | `string` | No | -- | New description |
| `--color` | `string` | No | -- | New color |
| `--icon` | `string` | No | -- | New icon |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

---

## folder move

Move a folder, with everything in it, under another folder or to the top level.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--to` | `string` | One of | -- | Destination folder ID |
| `--to-root` | `bool` | One of | `false` | Move to the top level |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

---

## folder move-content

Move up to 100 queries and 100 dashboards into a folder, or out of all folders. All or nothing. Everything must belong to the API key's library.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--query-ids` | `[]int` | No | -- | Query IDs (comma-separated) |
| `--dashboard-ids` | `[]int` | No | -- | Dashboard IDs (comma-separated) |
| `--to` | `string` | One of | -- | Destination folder ID |
| `--to-root` | `bool` | One of | `false` | Move out of folders |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune folder move-content --query-ids 4512345,4512346 --dashboard-ids 98765 --to dp180Cu3jW3L -o json
```

---

## folder delete

Delete an empty folder. A folder with content is refused, and the error says what it holds.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--recursive` | `bool` | No | `false` | Delete a non-empty folder: deletes subfolders and **archives** every query and dashboard in it |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

> [!CAUTION]
> `create`, `update`, `move`, and `move-content` are **write** commands. `delete --recursive` archives content; confirm with the user first, and move content out with `folder move-content` if it should be kept.

---

## See Also

- [query-management.md](query-management.md) -- `query create --folder-id` saves a query into a folder
- [dashboard-management.md](dashboard-management.md) -- Find dashboards to move
