#!/usr/bin/env python3
"""
GitHub Issue Script - Create, list, and get GitHub issues.
"""

import json
import sys
import os
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

GITHUB_API = "https://api.github.com"


def _request(method: str, url: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make authenticated request to GitHub API."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is required")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "SpoonOS-GitHub-Skill/1.0",
    }

    req_data = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else "{}"
        try:
            err_data = json.loads(body)
            msg = err_data.get("message", str(e))
        except json.JSONDecodeError:
            msg = body or str(e)
        raise RuntimeError(f"GitHub API error ({e.code}): {msg}")


def create_issue(repo: str, title: str, body: str = "") -> Dict:
    """Create a new issue."""
    url = f"{GITHUB_API}/repos/{repo}/issues"
    data = {"title": title, "body": body}
    result = _request("POST", url, data)
    return {
        "success": True,
        "issue": {
            "number": result["number"],
            "title": result["title"],
            "state": result["state"],
            "url": result["html_url"],
            "created_at": result["created_at"],
        },
    }


def list_issues(repo: str, state: str = "open", limit: int = 10) -> Dict:
    """List issues in a repository."""
    url = f"{GITHUB_API}/repos/{repo}/issues?state={state}&per_page={min(limit, 100)}"
    result = _request("GET", url)
    # Filter out PRs (issues endpoint returns both)
    issues = [i for i in result if "pull_request" not in i]
    return {
        "success": True,
        "issues": [
            {
                "number": i["number"],
                "title": i["title"],
                "state": i["state"],
                "url": i["html_url"],
                "created_at": i["created_at"],
            }
            for i in issues[:limit]
        ],
        "count": len(issues[:limit]),
    }


def get_issue(repo: str, issue_number: int) -> Dict:
    """Get a single issue by number."""
    url = f"{GITHUB_API}/repos/{repo}/issues/{issue_number}"
    result = _request("GET", url)
    if "pull_request" in result:
        return {"success": False, "error": "This is a pull request, use get_pr instead"}
    return {
        "success": True,
        "issue": {
            "number": result["number"],
            "title": result["title"],
            "body": result.get("body") or "",
            "state": result["state"],
            "url": result["html_url"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
            "user": result["user"]["login"],
        },
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        action = input_data.get("action")
        repo = input_data.get("repo")

        if not action:
            print(json.dumps({"success": False, "error": "Missing required: action"}))
            sys.exit(1)
        if not repo:
            print(json.dumps({"success": False, "error": "Missing required: repo"}))
            sys.exit(1)

        if action == "create_issue":
            title = input_data.get("title")
            if not title:
                print(json.dumps({"success": False, "error": "Missing required: title"}))
                sys.exit(1)
            body = input_data.get("body", "")
            result = create_issue(repo, title, body)

        elif action == "list_issues":
            state = input_data.get("state", "open")
            limit = int(input_data.get("limit", 10))
            result = list_issues(repo, state, limit)

        elif action == "get_issue":
            issue_number = input_data.get("issue_number")
            if issue_number is None:
                print(json.dumps({"success": False, "error": "Missing required: issue_number"}))
                sys.exit(1)
            result = get_issue(repo, int(issue_number))

        else:
            print(json.dumps({"success": False, "error": f"Unknown action: {action}"}))
            sys.exit(1)

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except json.JSONDecodeError:
        print(json.dumps({"success": False, "error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
