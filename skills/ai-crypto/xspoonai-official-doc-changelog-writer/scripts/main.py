#!/usr/bin/env python3
import json
import argparse
import sys
from typing import Dict, Any, List
from datetime import datetime


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details=None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def parse_conventional_commit(message: str) -> Dict[str, str]:
    """Parse conventional commit message."""
    parts = message.split(":", 1)
    if len(parts) == 2:
        commit_type = parts[0].strip()
        description = parts[1].strip()
        return {"type": commit_type, "description": description}
    return {"type": "other", "description": message}


def generate_changelog(commits: List[Dict]) -> str:
    """Generate changelog from commits."""
    grouped = {"feat": [], "fix": [], "docs": [], "other": []}
    
    for commit in commits:
        parsed = parse_conventional_commit(commit.get("message", ""))
        commit_type = parsed["type"]
        if commit_type in grouped:
            grouped[commit_type].append(parsed["description"])
        else:
            grouped["other"].append(parsed["description"])
    
    changelog = "# Changelog\n\n"
    
    if grouped["feat"]:
        changelog += "## Features\n"
        for desc in grouped["feat"]:
            changelog += f"- {desc}\n"
        changelog += "\n"
    
    if grouped["fix"]:
        changelog += "## Fixes\n"
        for desc in grouped["fix"]:
            changelog += f"- {desc}\n"
        changelog += "\n"
    
    if grouped["docs"]:
        changelog += "## Documentation\n"
        for desc in grouped["docs"]:
            changelog += f"- {desc}\n"
        changelog += "\n"
    
    return changelog


def main():
    parser = argparse.ArgumentParser(description='Generate changelogs from git history')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            demo_commits = [
                {"message": "feat: Add user authentication", "author": "Alice", "date": "2026-02-01"},
                {"message": "fix: Resolve database connection issue", "author": "Bob", "date": "2026-02-02"},
                {"message": "docs: Update API documentation", "author": "Charlie", "date": "2026-02-03"},
                {"message": "feat: Implement password reset", "author": "Alice", "date": "2026-02-04"}
            ]
            
            changelog = generate_changelog(demo_commits)
            result = {"demo": True, "changelog": changelog, "commit_count": len(demo_commits)}
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            commits = params.get("commits", [])
            
            if not commits:
                raise ValueError("commits list is required")
            
            changelog = generate_changelog(commits)
            result = {"changelog": changelog, "commit_count": len(commits)}
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
