#!/usr/bin/env python3
"""
Generate Conventional Commit Message - Analyzes git diff and generates commit messages.

Author: Contributed via Claude Code
Version: 1.0.0
"""

import json
import subprocess
import sys
from typing import Dict, List, Optional


class CommitMessageGenerator:
    """Generate conventional commit messages based on git changes."""

    COMMIT_TYPES = {
        "feat": "A new feature",
        "fix": "A bug fix",
        "docs": "Documentation only changes",
        "style": "Changes that do not affect the meaning of the code",
        "refactor": "A code change that neither fixes a bug nor adds a feature",
        "perf": "A code change that improves performance",
        "test": "Adding missing tests or correcting existing tests",
        "chore": "Changes to the build process or auxiliary tools",
    }

    def __init__(self):
        self.staged_files = []
        self.diff_stats = {}

    def run_git_command(self, args: List[str]) -> str:
        """Run a git command and return output."""
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return ""

    def get_staged_changes(self) -> Dict:
        """Get information about staged changes."""
        # Get list of staged files
        staged_output = self.run_git_command(["diff", "--cached", "--name-status"])

        files_changed = []
        for line in staged_output.split("\n"):
            if line:
                parts = line.split("\t")
                if len(parts) >= 2:
                    status, filename = parts[0], parts[1]
                    files_changed.append({"status": status, "file": filename})

        # Get diff stats
        stats_output = self.run_git_command(["diff", "--cached", "--numstat"])

        total_added = 0
        total_deleted = 0

        for line in stats_output.split("\n"):
            if line:
                parts = line.split("\t")
                if len(parts) >= 3:
                    added, deleted = parts[0], parts[1]
                    if added != "-":
                        total_added += int(added)
                    if deleted != "-":
                        total_deleted += int(deleted)

        return {
            "files_changed": files_changed,
            "total_files": len(files_changed),
            "lines_added": total_added,
            "lines_deleted": total_deleted
        }

    def analyze_changes(self, files_changed: List[Dict]) -> Dict:
        """Analyze changes to determine commit type and scope."""
        if not files_changed:
            return {"type": "chore", "scope": None}

        # Analyze file patterns
        file_paths = [f["file"] for f in files_changed]

        # Determine scope based on common directory
        scopes = set()
        for path in file_paths:
            parts = path.split("/")
            if len(parts) > 1:
                scopes.add(parts[0])

        scope = list(scopes)[0] if len(scopes) == 1 else None

        # Determine type based on file patterns
        commit_type = "chore"

        for file_info in files_changed:
            path = file_info["file"]
            status = file_info["status"]

            if status == "A":  # Added file
                if "test" in path:
                    commit_type = "test"
                elif any(doc in path for doc in ["README", "docs/", ".md"]):
                    commit_type = "docs"
                else:
                    commit_type = "feat"
            elif status == "M":  # Modified file
                if "test" in path:
                    commit_type = "test"
                elif any(doc in path for doc in ["README", "docs/", ".md"]):
                    commit_type = "docs"
                elif any(perf in path for perf in ["performance", "optimize"]):
                    commit_type = "perf"

        return {"type": commit_type, "scope": scope}

    def generate_message(
        self,
        commit_type: str,
        scope: Optional[str] = None,
        subject: Optional[str] = None,
        include_body: bool = False,
        include_breaking: bool = False
    ) -> str:
        """Generate a conventional commit message."""
        # Build the commit message header
        scope_str = f"({scope})" if scope else ""

        if not subject:
            subject = f"update {scope if scope else 'code'}"

        header = f"{commit_type}{scope_str}: {subject}"

        if not include_body:
            return header

        # Add body if requested
        body_lines = []
        body_lines.append("")
        body_lines.append("Changes include:")
        body_lines.append("- Updated implementation")
        body_lines.append("- Added necessary tests")

        # Add breaking change footer if requested
        if include_breaking:
            body_lines.append("")
            body_lines.append("BREAKING CHANGE: This change requires migration")

        return "\n".join([header] + body_lines)

    def execute(self, params: Dict) -> Dict:
        """Execute commit message generation."""
        # Get staged changes
        changes = self.get_staged_changes()

        if changes["total_files"] == 0:
            return {
                "success": False,
                "error": "No staged changes found. Use 'git add' to stage files first."
            }

        # Analyze changes to determine type and scope
        analysis = self.analyze_changes(changes["files_changed"])

        # Use provided parameters or defaults from analysis
        commit_type = params.get("type", analysis["type"])
        scope = params.get("scope", analysis["scope"])
        subject = params.get("subject")
        include_body = params.get("include_body", False)
        include_breaking = params.get("include_breaking", False)

        # Generate the commit message
        message = self.generate_message(
            commit_type=commit_type,
            scope=scope,
            subject=subject,
            include_body=include_body,
            include_breaking=include_breaking
        )

        return {
            "success": True,
            "message": message,
            "type": commit_type,
            "scope": scope,
            "files_changed": changes["total_files"],
            "lines_added": changes["lines_added"],
            "lines_deleted": changes["lines_deleted"],
            "changed_files": [f["file"] for f in changes["files_changed"]]
        }


def main():
    """Main entry point for the script."""
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        params = json.loads(input_data) if input_data.strip() else {}

        # Create generator and execute
        generator = CommitMessageGenerator()
        result = generator.execute(params)

        # Output result as JSON
        print(json.dumps(result, indent=2))

        sys.exit(0 if result.get("success", False) else 1)

    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
