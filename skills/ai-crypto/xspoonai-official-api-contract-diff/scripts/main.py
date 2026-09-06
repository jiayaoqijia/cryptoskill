#!/usr/bin/env python3
import json
import argparse
import sys
from typing import Dict, Any, List, Optional


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def compare_openapi_schemas(schema1: Dict, schema2: Dict) -> Dict[str, List]:
    """Compare two OpenAPI schemas."""
    breaking = []
    non_breaking = []
    additions = []
    
    paths1 = set(schema1.get("paths", {}).keys())
    paths2 = set(schema2.get("paths", {}).keys())
    
    # Removed endpoints (breaking)
    for path in paths1 - paths2:
        breaking.append({"type": "removed_endpoint", "path": path})
    
    # Added endpoints (addition)
    for path in paths2 - paths1:
        additions.append({"type": "new_endpoint", "path": path})
    
    # Modified endpoints
    for path in paths1 & paths2:
        methods1 = set(schema1["paths"][path].keys())
        methods2 = set(schema2["paths"][path].keys())
        
        for method in methods1 - methods2:
            breaking.append({"type": "removed_method", "path": path, "method": method})
        
        for method in methods2 - methods1:
            additions.append({"type": "new_method", "path": path, "method": method})
    
    return {"breaking_changes": breaking, "non_breaking_changes": non_breaking, "additions": additions}


def main():
    parser = argparse.ArgumentParser(description='Compare API schemas for breaking changes')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            schema1 = {
                "paths": {
                    "/users": {"get": {}, "post": {}},
                    "/posts": {"get": {}}
                }
            }
            schema2 = {
                "paths": {
                    "/users": {"get": {}, "post": {}, "delete": {}},
                    "/comments": {"get": {}}
                }
            }
            
            diff = compare_openapi_schemas(schema1, schema2)
            result = {"demo": True, "schema_type": "openapi", "diff": diff}
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            schema_type = params.get("schema_type", "openapi")
            
            if schema_type == "openapi":
                schema1 = params.get("schema1", {})
                schema2 = params.get("schema2", {})
                diff = compare_openapi_schemas(schema1, schema2)
                result = {"schema_type": schema_type, "diff": diff}
            else:
                result = {"schema_type": schema_type, "note": "GraphQL comparison not yet implemented"}
            
            print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
