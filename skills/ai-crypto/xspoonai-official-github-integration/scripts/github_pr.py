#!/usr/bin/env python3
"""
GitHub PR Script - List and get GitHub Pull Requests.
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


def list_prs(repo: str, state: str = "open", limit: int = 10) -> Dict:
    """List pull requests in a repository."""
    url = f"{GITHUB_API}/repos/{repo}/pulls?state={state}&per_page={min(limit, 100)}"
    result = _request("GET", url)
    prs = result[:limit] if isinstance(result, list) else []
    return {
        "success": True,
        "pull_requests": [
            {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "url": pr["html_url"],
                "created_at": pr["created_at"],
                "user": pr["user"]["login"],
                "head": pr["head"]["ref"],
                "base": pr["base"]["ref"],
            }
            for pr in prs
        ],
        "count": len(prs),
    }


def get_pr(repo: str, pr_number: int) -> Dict:
    """Get a single pull request by number."""
    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}"
    result = _request("GET", url)
    return {
        "success": True,
        "pull_request": {
            "number": result["number"],
            "title": result["title"],
            "body": result.get("body") or "",
            "state": result["state"],
            "url": result["html_url"],
            "diff_url": result["diff_url"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
            "user": result["user"]["login"],
            "head": result["head"]["ref"],
            "base": result["base"]["ref"],
            "mergeable": result.get("mergeable"),
            "merged": result.get("merged", False),
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

        if action == "list_prs":
            state = input_data.get("state", "open")
            limit = int(input_data.get("limit", 10))
            result = list_prs(repo, state, limit)

        elif action == "get_pr":
            pr_number = input_data.get("pr_number")
            if pr_number is None:
                print(json.dumps({"success": False, "error": "Missing required: pr_number"}))
                sys.exit(1)
            result = get_pr(repo, int(pr_number))

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
