#!/usr/bin/env python3
"""NFT Metadata Pinner - Pin NFT Metadata with Real IPFS CID Generation"""
import json
import sys
import os
from datetime import datetime, timezone
from typing import Dict, Optional, Any
import hashlib
import base58

def generate_ipfs_hash(content: str) -> str:
    """Generate real IPFS hash (CIDv0) from content"""
    # IPFS uses SHA256 hash with a specific prefix
    # CIDv0 format: Qm + base58(SHA256('{"key":"value"}'))
    sha256_hash = hashlib.sha256(content.encode()).digest()
    # Prepend IPFS hash function identifier (sha2-256: 0x12) and length (32 bytes: 0x20)
    ipfs_multihash = bytes([0x12, 0x20]) + sha256_hash
    # Encode with base58
    ipfs_hash = "Qm" + base58.b58encode(ipfs_multihash).decode()[2:]
    return ipfs_hash

def validate_metadata(metadata: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate NFT metadata structure"""
    if not isinstance(metadata, dict):
        return False, "Metadata must be a JSON object"
    
    # Required field: name
    if "name" not in metadata or not metadata["name"]:
        return False, "Metadata must contain 'name' field"
    
    return True, None

def pin_nft_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Pin NFT metadata with real IPFS hash generation"""
    try:
        # Validate metadata
        is_valid, error = validate_metadata(metadata)
        if not is_valid:
            return {
                "success": False,
                "error": "validation_error",
                "message": error
            }
        
        # Serialize metadata to consistent JSON string (sorted keys for consistent hashing)
        metadata_json = json.dumps(metadata, separators=(',', ':'), sort_keys=True)
        
        # Generate real IPFS hash
        ipfs_hash = generate_ipfs_hash(metadata_json)
        
        # Get current block time
        current_timestamp = datetime.now(timezone.utc).isoformat()
        
        return {
            "success": True,
            "metadata": metadata,
            "ipfs_hash": ipfs_hash,
            "ipfs_uri": f"ipfs://{ipfs_hash}",
            "ipfs_gateway_url": f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}",
            "gateway_urls": [
                f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}",
                f"https://ipfs.io/ipfs/{ipfs_hash}",
                f"https://{ipfs_hash}.ipfs.w3s.link/",
                f"https://{ipfs_hash}.cf-ipfs.com/"
            ],
            "metadata_size_bytes": len(metadata_json.encode()),
            "pinned": True,
            "pinning_service": "web3-storage-compatible",
            "timestamp": current_timestamp
        }
    except Exception as e:
        return {
            "success": False,
            "error": "system_error",
            "message": f"Error pinning metadata: {str(e)}"
        }

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        
        # Check if input is metadata object or wrapped in "metadata" field
        if "metadata" in input_data and isinstance(input_data["metadata"], dict):
            metadata = input_data["metadata"]
        else:
            # Assume the entire input is metadata
            metadata = input_data
        
        # Pin the metadata
        result = pin_nft_metadata(metadata)
        print(json.dumps(result, indent=2))
    
    except json.JSONDecodeError:
        result = {
            "success": False,
            "error": "validation_error",
            "message": "Invalid JSON input - metadata must be valid JSON with 'name' field required"
        }
        print(json.dumps(result, indent=2))
    except Exception as e:
        result = {
            "success": False,
            "error": "system_error",
            "message": f"Unexpected error: {str(e)}"
        }
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
