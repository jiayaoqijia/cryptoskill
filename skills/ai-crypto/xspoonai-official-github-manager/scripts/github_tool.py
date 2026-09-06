#!/usr/bin/env python3
"""
GitHub Manager Tool - Manage GitHub issues and PRs.

Author: SpoonOS Contributor
Version: 1.0.0
"""

import os
import json
import sys
import subprocess
from typing import Dict, Any, Optional, List

# Ensure PyGithub is installed
try:
    from github import Github, Auth
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyGithub"])
        from github import Github, Auth
    except Exception as e:
        print(f"Error installing PyGithub: {e}")
        sys.exit(1)

# Attempt to import BaseTool, handle running standalone for testing
try:
    from spoon_ai.tools.base import BaseTool
except ImportError:
    from pydantic import BaseModel, Field
    class BaseTool(BaseModel):
        name: str
        description: str
        parameters: dict
        async def execute(self, **kwargs): pass

from pydantic import Field

class GitHubTool(BaseTool):
    name: str = "github_tool"
    description: str = "Interact with GitHub issues and PRs (list, create, comment)."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["list_issues", "create_issue", "comment_issue", "get_issue"],
                "description": "Action to perform"
            },
            "repo": {
                "type": "string",
                "description": "Repository in 'owner/name' format"
            },
            "title": {
                "type": "string",
                "description": "Title for new issue"
            },
            "body": {
                "type": "string",
                "description": "Body/Content for issue or comment"
            },
            "issue_number": {
                "type": "integer",
                "description": "Issue number for comments or retrieval"
            },
            "state": {
                "type": "string", 
                "enum": ["open", "closed", "all"],
                "default": "open",
                "description": "Filter by issue state (default: open)"
            }
        },
        "required": ["action", "repo"]
    })

    async def execute(self, action: str, repo: str, title: str = None, body: str = None, issue_number: int = None, state: str = "open") -> str:
        """
        Executes the GitHub action.
        """
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return "Error: GITHUB_TOKEN environment variable not set."

        try:
            auth = Auth.Token(token)
            g = Github(auth=auth)
            repository = g.get_repo(repo)

            if action == "list_issues":
                issues = repository.get_issues(state=state)
                # Limit to 10 for brevity
                result = []
                for issue in issues[:10]:
                    result.append({
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "url": issue.html_url
                    })
                return json.dumps(result, indent=2)

            elif action == "create_issue":
                if not title:
                    return "Error: 'title' is required for creating an issue."
                issue = repository.create_issue(title=title, body=body or "")
                return json.dumps({
                    "message": "Issue created successfully",
                    "number": issue.number,
                    "url": issue.html_url
                }, indent=2)

            elif action == "comment_issue":
                if not issue_number or not body:
                    return "Error: 'issue_number' and 'body' are required for commenting."
                issue = repository.get_issue(issue_number)
                comment = issue.create_comment(body)
                return json.dumps({
                    "message": "Comment added successfully",
                    "url": comment.html_url
                }, indent=2)

            elif action == "get_issue":
                if not issue_number:
                    return "Error: 'issue_number' is required."
                issue = repository.get_issue(issue_number)
                return json.dumps({
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body,
                    "state": issue.state,
                    "comments": issue.comments,
                    "url": issue.html_url
                }, indent=2)

            else:
                return f"Error: Unknown action '{action}'"

        except Exception as e:
            return f"Error interacting with GitHub: {str(e)}"

if __name__ == "__main__":
    import asyncio
    
    async def main():
        tool = GitHubTool()
        # Simple test with mock args if run interactively, or check env
        print("GitHub Manager Tool Standalone Mode")
        print("Set GITHUB_TOKEN and modify main() for manual testing.")

    asyncio.run(main())
