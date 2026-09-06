---
name: storage-s3-uploader
track: ai-productivity
version: 0.1.0
summary: Upload files to S3-compatible storage
---

## Description

Upload files to S3-compatible storage with lifecycle hints. Supports batch uploads, permissions, and object metadata management.

## Inputs

```json
{
  "bucket": "S3 bucket name",
  "files": ["List of file paths"],
  "prefix": "S3 key prefix",
  "lifecycle": "temporary|permanent"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "uploaded": 3,
    "urls": ["Array of S3 URLs"]
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Upload Files
```bash
echo '{"bucket":"my-bucket","files":["file1.txt"],"prefix":"uploads/"}' | python3 scripts/main.py
```

## Examples

### Example 1: Upload to S3
```bash
$ echo '{"bucket":"my-bucket","files":["data.csv"],"prefix":"reports/","lifecycle":"permanent"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "uploaded": 1,
    "urls": ["https://my-bucket.s3.amazonaws.com/reports/data.csv"]
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
    "bucket": "Bucket not found"
  }
}
```
