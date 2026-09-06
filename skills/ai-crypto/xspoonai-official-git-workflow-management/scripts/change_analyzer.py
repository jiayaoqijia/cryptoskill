#!/usr/bin/env python3
"""
Change Analyzer - Analyze git history and generate insights.

Author: Contributed via Claude Code
Version: 1.0.0
"""

import json
import subprocess
import sys
from typing import Dict, List
from collections import defaultdict


class ChangeAnalyzer:
    """Analyze git history and generate insights."""

    def run_git_command(self, args: List[str]) -> tuple:
        """Run a git command and return (success, output)."""
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=True
            )
            return (True, result.stdout.strip())
        except subprocess.CalledProcessError as e:
            return (False, e.stderr.strip())

    def get_commits(self, from_ref: str = None, to_ref: str = "HEAD", limit: int = 100) -> List[Dict]:
        """Get commit history."""
        args = ["log", "--pretty=format:%H|%an|%ae|%ad|%s", f"--max-count={limit}"]

        if from_ref:
            args.append(f"{from_ref}..{to_ref}")
        else:
            args.append(to_ref)

        success, output = self.run_git_command(args)

        if not success:
            return []

        commits = []
        for line in output.split("\n"):
            if line:
                parts = line.split("|")
                if len(parts) >= 5:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    })

        return commits

    def generate_changelog(self, from_ref: str, to_ref: str, group_by: str = "type") -> Dict:
        """Generate a changelog from commits."""
        commits = self.get_commits(from_ref, to_ref)

        if group_by == "type":
            grouped = defaultdict(list)

            for commit in commits:
                message = commit["message"]

                # Parse conventional commit format
                if ":" in message:
                    commit_type = message.split(":")[0].split("(")[0].strip()
                    grouped[commit_type].append(message)
                else:
                    grouped["other"].append(message)

            return {
                "success": True,
                "changelog": dict(grouped),
                "total_commits": len(commits)
            }

        elif group_by == "author":
            grouped = defaultdict(list)

            for commit in commits:
                author = commit["author"]
                grouped[author].append(commit["message"])

            return {
                "success": True,
                "changelog": dict(grouped),
                "total_commits": len(commits)
            }

        return {"success": False, "error": f"Unknown group_by: {group_by}"}

    def analyze_contributors(self, limit: int = 100) -> Dict:
        """Analyze contributor statistics."""
        commits = self.get_commits(limit=limit)

        contributors = defaultdict(int)
        for commit in commits:
            contributors[commit["author"]] += 1

        sorted_contributors = sorted(
            contributors.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "success": True,
            "contributors": [
                {"name": name, "commits": count}
                for name, count in sorted_contributors
            ],
            "total_contributors": len(contributors)
        }

    def analyze_file_changes(self, limit: int = 100) -> Dict:
        """Analyze which files change most frequently."""
        args = ["log", f"--max-count={limit}", "--name-only", "--pretty=format:"]
        success, output = self.run_git_command(args)

        if not success:
            return {"success": False, "error": "Failed to get file changes"}

        file_counts = defaultdict(int)
        for line in output.split("\n"):
            if line.strip():
                file_counts[line.strip()] += 1

        sorted_files = sorted(
            file_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]

        return {
            "success": True,
            "hotspots": [
                {"file": file, "changes": count}
                for file, count in sorted_files
            ]
        }

    def get_commit_stats(self, from_ref: str = None, to_ref: str = "HEAD") -> Dict:
        """Get commit statistics."""
        commits = self.get_commits(from_ref, to_ref)

        # Count by type
        type_counts = defaultdict(int)
        for commit in commits:
            message = commit["message"]
            if ":" in message:
                commit_type = message.split(":")[0].split("(")[0].strip()
                type_counts[commit_type] += 1
            else:
                type_counts["other"] += 1

        return {
            "success": True,
            "total_commits": len(commits),
            "by_type": dict(type_counts),
            "contributors": len(set(c["author"] for c in commits))
        }

    def execute(self, params: Dict) -> Dict:
        """Execute change analysis."""
        analysis_type = params.get("analysis_type", "stats")

        if analysis_type == "changelog":
            from_ref = params.get("from_tag") or params.get("from_ref")
            to_ref = params.get("to_tag") or params.get("to_ref", "HEAD")
            group_by = params.get("group_by", "type")

            return self.generate_changelog(from_ref, to_ref, group_by)

        elif analysis_type == "contributors":
            limit = params.get("limit", 100)
            return self.analyze_contributors(limit)

        elif analysis_type == "hotspots":
            limit = params.get("limit", 100)
            return self.analyze_file_changes(limit)

        elif analysis_type == "stats":
            from_ref = params.get("from_ref")
            to_ref = params.get("to_ref", "HEAD")
            return self.get_commit_stats(from_ref, to_ref)

        else:
            return {
                "success": False,
                "error": f"Unknown analysis type: {analysis_type}"
            }


def main():
    """Main entry point for the script."""
    try:
        input_data = sys.stdin.read()
        params = json.loads(input_data) if input_data.strip() else {}

        analyzer = ChangeAnalyzer()
        result = analyzer.execute(params)

        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("success", False) else 1)

    except Exception as e:
        error_result = {"success": False, "error": str(e)}
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
