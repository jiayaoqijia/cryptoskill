#!/usr/bin/env python3
import json
import argparse
import sys
import os
from typing import Dict, Any, Optional

# Try importing boto3 for AWS S3
try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def upload_file_to_s3(file_path: str, bucket: str, key: str, 
                      public: bool = False, metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Upload file to AWS S3."""
    
    if not HAS_BOTO3:
        return {
            "success": False,
            "error": "boto3_not_installed",
            "message": "Run: pip install boto3"
        }
    
    if not os.path.exists(file_path):
        return {"success": False, "error": "file_not_found", "message": f"File not found: {file_path}"}
    
    try:
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create S3 client
        s3_client = boto3.client('s3')
        
        # Prepare extra args
        extra_args = {}
        if metadata:
            extra_args['Metadata'] = metadata
        if public:
            extra_args['ACL'] = 'public-read'
        
        # Upload file
        s3_client.upload_file(file_path, bucket, key, ExtraArgs=extra_args if extra_args else None)
        
        # Generate URLs
        s3_url = f"s3://{bucket}/{key}"
        public_url = f"https://{bucket}.s3.amazonaws.com/{key}"
        
        return {
            "success": True,
            "file_path": os.path.abspath(file_path),
            "bucket": bucket,
            "key": key,
            "file_size": file_size,
            "s3_url": s3_url,
            "public_url": public_url,
            "public_access": public,
            "metadata": metadata or {},
            "status": "uploaded"
        }
    
    except Exception as e:
        return {"success": False, "error": "upload_error", "message": str(e)}


def list_s3_files(bucket: str, prefix: str = "", max_keys: int = 100) -> Dict[str, Any]:
    """List files in S3 bucket."""
    
    if not HAS_BOTO3:
        return {
            "success": False,
            "error": "boto3_not_installed",
            "message": "Run: pip install boto3"
        }
    
    try:
        s3_client = boto3.client('s3')
        
        response = s3_client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=max_keys
        )
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    "key": obj['Key'],
                    "size": obj['Size'],
                    "last_modified": obj['LastModified'].isoformat()
                })
        
        return {
            "success": True,
            "bucket": bucket,
            "prefix": prefix,
            "files": files,
            "file_count": len(files),
            "is_truncated": response.get('IsTruncated', False)
        }
    
    except Exception as e:
        return {"success": False, "error": "list_error", "message": str(e)}


def get_s3_file_info(bucket: str, key: str) -> Dict[str, Any]:
    """Get metadata for S3 file."""
    
    if not HAS_BOTO3:
        return {
            "success": False,
            "error": "boto3_not_installed",
            "message": "Run: pip install boto3"
        }
    
    try:
        s3_client = boto3.client('s3')
        
        response = s3_client.head_object(Bucket=bucket, Key=key)
        
        return {
            "success": True,
            "bucket": bucket,
            "key": key,
            "file_size": response.get('ContentLength', 0),
            "last_modified": response.get('LastModified', '').isoformat() if response.get('LastModified') else None,
            "content_type": response.get('ContentType', ''),
            "metadata": response.get('Metadata', {}),
            "etag": response.get('ETag', ''),
            "storage_class": response.get('StorageClass', '')
        }
    
    except Exception as e:
        return {"success": False, "error": "info_error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Upload files to S3 with metadata')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            result = {
                "demo": True,
                "boto3_available": HAS_BOTO3,
                "capabilities": {
                    "upload": "Available" if HAS_BOTO3 else "Requires: pip install boto3",
                    "list_files": "Available" if HAS_BOTO3 else "Requires: pip install boto3",
                    "get_metadata": "Available" if HAS_BOTO3 else "Requires: pip install boto3",
                    "public_access": "Available" if HAS_BOTO3 else "Requires: pip install boto3"
                },
                "example_upload": {
                    "file_path": "document.pdf",
                    "bucket": "my-bucket",
                    "key": "uploads/document.pdf",
                    "s3_url": "s3://my-bucket/uploads/document.pdf",
                    "public_url": "https://my-bucket.s3.amazonaws.com/uploads/document.pdf",
                    "status": "would be uploaded"
                }
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            action = params.get("action", "upload")
            
            if action == "upload":
                file_path = params.get("file_path", "")
                bucket = params.get("bucket", "")
                key = params.get("key", "")
                
                if not all([file_path, bucket, key]):
                    raise ValueError("file_path, bucket, and key are required")
                
                public = params.get("public", False)
                metadata = params.get("metadata", {})
                
                result = upload_file_to_s3(file_path, bucket, key, public, metadata)
            
            elif action == "list":
                bucket = params.get("bucket", "")
                prefix = params.get("prefix", "")
                max_keys = params.get("max_keys", 100)
                
                if not bucket:
                    raise ValueError("bucket is required")
                
                result = list_s3_files(bucket, prefix, max_keys)
            
            elif action == "info":
                bucket = params.get("bucket", "")
                key = params.get("key", "")
                
                if not all([bucket, key]):
                    raise ValueError("bucket and key are required")
                
                result = get_s3_file_info(bucket, key)
            
            else:
                raise ValueError(f"Unknown action: {action}")
            
            if result.get("success") == False:
                print(format_error(result.get("error", "unknown_error"), {"message": result.get("message")}))
            else:
                print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
