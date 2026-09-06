#!/usr/bin/env python3
import json
import argparse
import sys
from typing import Dict, Any, Optional


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def generate_github_actions(project_type: str, stages: list) -> str:
    """Generate GitHub Actions workflow."""
    config = f"""name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
"""
    
    if "build" in stages:
        if project_type == "python":
            config += """  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m build

"""
    
    if "test" in stages:
        config += """  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/

"""
    
    if "deploy" in stages:
        config += """  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]
    steps:
      - run: echo "Deploying application"

"""
    
    return config


def main():
    parser = argparse.ArgumentParser(description='Generate CI/CD pipeline configurations')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            config = generate_github_actions("python", ["build", "test", "deploy"])
            result = {
                "demo": True,
                "platform": "github",
                "project_type": "python",
                "config": config,
                "filename": ".github/workflows/ci.yml"
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            platform = params.get("platform", "github")
            project_type = params.get("project_type", "python")
            stages = params.get("stages", ["build", "test"])
            
            if platform == "github":
                config = generate_github_actions(project_type, stages)
                filename = ".github/workflows/ci.yml"
            else:
                config = f"# {platform} configuration not yet implemented"
                filename = f"{platform}.yml"
            
            result = {"platform": platform, "project_type": project_type, "config": config, "filename": filename}
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
