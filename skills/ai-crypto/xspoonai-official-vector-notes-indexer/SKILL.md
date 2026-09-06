---
name: vector-notes-indexer
track: ai-productivity
version: 0.1.0
summary: Create local embedding index for notes
---

## Description

Create a simple local embedding index for notes using vector embeddings. Enables semantic search and similarity matching for note collections.

## Inputs

```json
{
  "notes": ["Note texts to index"],
  "model": "embedding model name",
  "index_path": "Path to save index"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "indexed": 10,
    "index_size": "5.2MB"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Create Index
```bash
echo '{"notes":["Note 1","Note 2"],"model":"sentence-transformers"}' | python3 scripts/main.py
```

## Examples

### Example 1: Index Notes
```bash
$ echo '{"notes":["Meeting notes about Q1 planning","Project status update"],"model":"sentence-transformers","index_path":"./notes_index"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "indexed": 2,
    "index_size": "1.2MB"
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": {
    "notes": "Notes list is required"
  }
}
```
