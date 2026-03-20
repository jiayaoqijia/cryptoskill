#!/usr/bin/env python3
"""
Taostats API Client with Retry Logic
Taostats API client with rate limiting and retry logic
"""

import requests
import json
import time
from typing import Optional, Dict, Any

class TaostatsAPI:
    """
    Taostats API Client with automatic retry logic
    
    Attributes:
        base_url: API base URL
        api_key: Taostats API key
        max_retries: Max retries on 429
        retry_delay: Seconds between retries
    """
    
    def __init__(self, api_key: str, max_retries: int = 3, retry_delay: int = 12):
        self.base_url = "https://api.taostats.io/api"
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.headers = {
            "accept": "application/json",
            "Authorization": api_key
        }
    
    def get_json(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make API call with automatic retry on rate limit
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response dict
            
        Raises:
            RuntimeError: After max retries exceeded
        """
        url = f"{self.base_url}/{endpoint}"
        retries = 0
        
        while retries < self.max_retries:
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if response.status_code == 429:
                    retries += 1
                    if retries < self.max_retries:
                        print(f"  Rate limited. Waiting {self.retry_delay}s... (retry {retries}/{self.max_retries})")
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        raise RuntimeError(f"Rate limit exceeded after {self.max_retries} retries")
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.Timeout:
                retries += 1
                if retries < self.max_retries:
                    print(f"  Timeout. Retrying... ({retries}/{self.max_retries})")
                    time.sleep(2)
                    continue
                raise
            except Exception as e:
                raise RuntimeError(f"API call failed: {e}")
        
        raise RuntimeError("Max retries exceeded")
    
    def get_paginated(self, endpoint: str, params: Optional[Dict] = None, limit: int = 200) -> list:
        """
        Get all paginated results automatically
        
        Returns:
            List of all data items across pages
        """
        all_data = []
        page = 1
        count = limit
        
        while count > 0:
            page_params = {**(params or {}), "limit": limit, "page": page}
            result = self.get_json(endpoint, page_params)
            
            data = result.get('data', [])
            all_data.extend(data)
            
            total_items = result.get('pagination', {}).get('total_items', 0)
            
            if total_items < limit:
                # Last page
                break
            if len(data) < limit:
                # No more data
                break
                
            count = total_items
            page += 1
            
            # Small delay between pages
            time.sleep(0.5)
        
        return all_data
    
    def get_balance_history(self, coldkey: str, start_timestamp: int, end_timestamp: int) -> list:
        """
        Get daily balance history
        
        Args:
            coldkey: Wallet address
            start_timestamp: Unix timestamp
            end_timestamp: Unix timestamp
            
        Returns:
            List of daily balance records
        """
        endpoint = "account/history/v1"
        params = {
            "address": coldkey,
            "timestamp_start": start_timestamp,
            "timestamp_end": end_timestamp,
            "order": "timestamp_asc"
        }
        
        return self.get_paginated(endpoint, params)


# CLI usage
if __name__ == "__main__":
    import sys
    import os
    
    # Load API key
    try:
        api_key = os.environ.get("TAOSTATS_API_KEY")
        if not api_key:
            with open(os.path.expanduser("~/.openclaw/workspace/.taostats")) as f:
                            api_key = f.read().split("=")[1].strip()
    except Exception:
        print("Error: TAOSTATS_API_KEY not set. Export it or create ~/.openclaw/workspace/.taostats")
        sys.exit(1)
    
    api = TaostatsAPI(api_key)
    
    if len(sys.argv) < 2:
        print("Usage: python3 taostats_client.py <endpoint> [params]")
        print("Example: python3 taostats_client.py dtao/pool/latest/v1?netuid=33")
        sys.exit(1)
    
    endpoint = sys.argv[1]
    try:
        result = api.get_json(endpoint)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
