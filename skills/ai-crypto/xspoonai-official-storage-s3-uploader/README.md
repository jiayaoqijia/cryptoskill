# storage-s3-uploader (Track: ai-productivity)

Upload files to AWS S3 or S3-compatible storage with lifecycle policies, multipart upload, and metadata management

## Overview

This skill provides efficient file uploads to S3 with support for large files, metadata tagging, access control, and lifecycle policy configuration. It handles multipart uploads for optimal performance, sets storage class hints, and manages object metadata for better data governance.

## Features

- **S3 Upload**: Upload files to AWS S3 buckets
- **S3-Compatible**: Work with MinIO, DigitalOcean Spaces, Wasabi, etc.
- **Multipart Upload**: Efficient large file uploads with parallel parts
- **Metadata Management**: Set object tags, custom metadata, and headers
- **Access Control**: Configure ACL and bucket policies
- **Lifecycle Hints**: Set storage class (Standard, Glacier, etc.)
- **Progress Tracking**: Monitor upload progress for large files
- **Batch Upload**: Upload multiple files efficiently

## Use Cases

- Upload application logs and archives to long-term storage
- Store generated reports and exports in S3
- Backup database dumps and configurations
- Archive AI model artifacts and training data
- Upload build artifacts and deployment packages
- Store user-generated content with lifecycle rules

## Quickstart
```bash
python3 scripts/main.py --help
```

## Example
```bash
python3 scripts/main.py --demo
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| bucket_name | string | Yes | S3 bucket name |
| file_path | string | Yes | Local file path to upload |
| object_key | string | No | S3 object key (defaults to filename) |
| storage_class | string | No | Storage class (STANDARD, GLACIER, DEEP_ARCHIVE) |
| acl | string | No | Access control (private, public-read, public-read-write) |
| metadata | object | No | Custom metadata key-value pairs |
| tags | object | No | Object tags for lifecycle and filtering |
| content_type | string | No | MIME type (auto-detected if not provided) |
| multipart | boolean | No | Use multipart upload for large files - default: true |
| lifecycle_days | integer | No | Days before transitioning to cheaper storage |

## Example Output

```json
{
  "ok": true,
  "data": {
    "file": "backup_2026-02-07.tar.gz",
    "bucket": "my-backups",
    "object_key": "backups/2026/02/backup_2026-02-07.tar.gz",
    "size_bytes": 5368709120,
    "upload_status": "completed",
    "upload_time_seconds": 245,
    "throughput_mbps": 21.2,
    "storage_class": "GLACIER",
    "metadata": {
      "source_server": "db-prod-01",
      "backup_type": "full",
      "compressed": true
    },
    "s3_url": "s3://my-backups/backups/2026/02/backup_2026-02-07.tar.gz"
  }
}
