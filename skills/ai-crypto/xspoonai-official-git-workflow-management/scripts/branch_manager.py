#!/usr/bin/env python3
"""
Branch Manager - Manage git branches with best practices.

Author: Contributed via Claude Code
Version: 1.0.0
"""

import json
import subprocess
import sys
from typing import Dict, List


class BranchManager:
    """Manage git branches following best practices."""

    BRANCH_TYPES = {
        "feature": "feature/",
        "bugfix": "bugfix/",
        "hotfix": "hotfix/",
        "release": "release/",
        "experiment": "experiment/"
    }

    def run_git_command(self, args: List[str], check: bool = True) -> tuple:
        """Run a git command and return (success, output)."""
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=check
            )
            return (True, result.stdout.strip())
        except subprocess.CalledProcessError as e:
            return (False, e.stderr.strip())

    def get_current_branch(self) -> str:
        """Get the current branch name."""
        success, output = self.run_git_command(["branch", "--show-current"])
        return output if success else ""

    def branch_exists(self, branch_name: str) -> bool:
        """Check if a branch exists."""
        success, output = self.run_git_command(["branch", "--list", branch_name])
        return bool(output)

    def create_branch(self, branch_type: str, name: str, base_branch: str = None) -> Dict:
        """Create a new branch with proper naming."""
        # Build full branch name
        prefix = self.BRANCH_TYPES.get(branch_type, "")
        full_branch_name = f"{prefix}{name}"

        # Check if branch already exists
        if self.branch_exists(full_branch_name):
            return {
                "success": False,
                "error": f"Branch '{full_branch_name}' already exists"
            }

        # Determine base branch
        if not base_branch:
            base_branch = "develop" if branch_type == "feature" else "main"

        # Ensure we're on the base branch
        success, _ = self.run_git_command(["checkout", base_branch])
        if not success:
            return {
                "success": False,
                "error": f"Failed to checkout base branch '{base_branch}'"
            }

        # Pull latest changes
        success, _ = self.run_git_command(["pull"])

        # Create and checkout new branch
        success, output = self.run_git_command(["checkout", "-b", full_branch_name])

        if not success:
            return {
                "success": False,
                "error": f"Failed to create branch: {output}"
            }

        return {
            "success": True,
            "branch_name": full_branch_name,
            "base_branch": base_branch,
            "message": f"Created and switched to branch '{full_branch_name}'"
        }

    def switch_branch(self, branch_name: str) -> Dict:
        """Switch to an existing branch."""
        success, output = self.run_git_command(["checkout", branch_name])

        if not success:
            return {
                "success": False,
                "error": f"Failed to switch to branch '{branch_name}': {output}"
            }

        return {
            "success": True,
            "branch_name": branch_name,
            "message": f"Switched to branch '{branch_name}'"
        }

    def delete_branch(self, branch_name: str, force: bool = False) -> Dict:
        """Delete a branch."""
        current_branch = self.get_current_branch()

        if current_branch == branch_name:
            return {
                "success": False,
                "error": "Cannot delete the current branch. Switch to another branch first."
            }

        flag = "-D" if force else "-d"
        success, output = self.run_git_command(["branch", flag, branch_name])

        if not success:
            return {
                "success": False,
                "error": f"Failed to delete branch: {output}"
            }

        return {
            "success": True,
            "message": f"Deleted branch '{branch_name}'"
        }

    def list_branches(self, filter_type: str = None) -> Dict:
        """List all branches, optionally filtered by type."""
        success, output = self.run_git_command(["branch", "-a"])

        if not success:
            return {
                "success": False,
                "error": "Failed to list branches"
            }

        branches = []
        current_branch = self.get_current_branch()

        for line in output.split("\n"):
            line = line.strip()
            if line:
                is_current = line.startswith("*")
                branch_name = line.replace("*", "").strip()

                if filter_type:
                    prefix = self.BRANCH_TYPES.get(filter_type, "")
                    if not branch_name.startswith(prefix):
                        continue

                branches.append({
                    "name": branch_name,
                    "current": is_current
                })

        return {
            "success": True,
            "branches": branches,
            "current_branch": current_branch
        }

    def merge_branch(self, branch_name: str, no_ff: bool = True) -> Dict:
        """Merge a branch into the current branch."""
        current_branch = self.get_current_branch()

        args = ["merge", branch_name]
        if no_ff:
            args.insert(1, "--no-ff")

        success, output = self.run_git_command(args, check=False)

        if not success:
            return {
                "success": False,
                "error": f"Merge failed: {output}"
            }

        return {
            "success": True,
            "message": f"Merged '{branch_name}' into '{current_branch}'",
            "current_branch": current_branch,
            "merged_branch": branch_name
        }

    def execute(self, params: Dict) -> Dict:
        """Execute branch management action."""
        action = params.get("action", "list")

        if action == "create":
            branch_type = params.get("branch_type", "feature")
            name = params.get("name")
            base_branch = params.get("base_branch")

            if not name:
                return {"success": False, "error": "Branch name is required"}

            return self.create_branch(branch_type, name, base_branch)

        elif action == "switch":
            branch_name = params.get("branch_name")
            if not branch_name:
                return {"success": False, "error": "Branch name is required"}

            return self.switch_branch(branch_name)

        elif action == "delete":
            branch_name = params.get("branch_name")
            force = params.get("force", False)

            if not branch_name:
                return {"success": False, "error": "Branch name is required"}

            return self.delete_branch(branch_name, force)

        elif action == "list":
            filter_type = params.get("filter_type")
            return self.list_branches(filter_type)

        elif action == "merge":
            branch_name = params.get("branch_name")
            no_ff = params.get("no_ff", True)

            if not branch_name:
                return {"success": False, "error": "Branch name is required"}

            return self.merge_branch(branch_name, no_ff)

        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }


def main():
    """Main entry point for the script."""
    try:
        input_data = sys.stdin.read()
        params = json.loads(input_data) if input_data.strip() else {}

        manager = BranchManager()
        result = manager.execute(params)

        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("success", False) else 1)

    except Exception as e:
        error_result = {"success": False, "error": str(e)}
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
