#!/usr/bin/env python3
"""
Pre-Commit Check - Run comprehensive checks before committing code.

Author: Contributed via Claude Code
Version: 1.0.0
"""

import json
import subprocess
import sys
import os
from typing import Dict, List


class PreCommitChecker:
    """Run pre-commit validation checks."""

    def __init__(self):
        self.results = {}

    def run_command(self, args: List[str], check: bool = False) -> tuple:
        """Run a command and return (success, output)."""
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=check
            )
            return (result.returncode == 0, result.stdout + result.stderr)
        except subprocess.CalledProcessError as e:
            return (False, e.stderr)
        except FileNotFoundError:
            return (False, f"Command not found: {args[0]}")

    def check_conflicts(self) -> Dict:
        """Check for merge conflict markers."""
        success, output = self.run_command(["git", "diff", "--cached", "--name-only"])

        if not success:
            return {"status": "error", "message": "Failed to get staged files"}

        conflict_markers = ["<<<<<<<", "=======", ">>>>>>>"]
        files_with_conflicts = []

        for filename in output.split("\n"):
            if filename:
                try:
                    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if any(marker in content for marker in conflict_markers):
                            files_with_conflicts.append(filename)
                except Exception:
                    pass

        if files_with_conflicts:
            return {
                "status": "failed",
                "message": f"Conflict markers found in {len(files_with_conflicts)} file(s)",
                "files": files_with_conflicts
            }

        return {"status": "passed", "message": "No conflicts detected"}

    def check_secrets(self) -> Dict:
        """Check for potential secrets in staged files."""
        success, output = self.run_command(["git", "diff", "--cached"])

        if not success:
            return {"status": "error", "message": "Failed to get diff"}

        # Simple patterns for common secrets
        secret_patterns = [
            "api_key",
            "apikey",
            "secret",
            "password",
            "token",
            "private_key",
            "aws_access_key",
        ]

        potential_secrets = []
        for line in output.split("\n"):
            if line.startswith("+"):
                line_lower = line.lower()
                for pattern in secret_patterns:
                    if pattern in line_lower and "=" in line:
                        potential_secrets.append(line[:100])
                        break

        if potential_secrets:
            return {
                "status": "warning",
                "message": f"Found {len(potential_secrets)} potential secret(s)",
                "lines": potential_secrets[:5]
            }

        return {"status": "passed", "message": "No obvious secrets detected"}

    def check_large_files(self, max_size_mb: int = 10) -> Dict:
        """Check for large files in staged changes."""
        success, output = self.run_command(["git", "diff", "--cached", "--name-only"])

        if not success:
            return {"status": "error", "message": "Failed to get staged files"}

        large_files = []
        max_size_bytes = max_size_mb * 1024 * 1024

        for filename in output.split("\n"):
            if filename and os.path.exists(filename):
                try:
                    size = os.path.getsize(filename)
                    if size > max_size_bytes:
                        large_files.append({
                            "file": filename,
                            "size_mb": round(size / (1024 * 1024), 2)
                        })
                except Exception:
                    pass

        if large_files:
            return {
                "status": "warning",
                "message": f"Found {len(large_files)} large file(s) (>{max_size_mb}MB)",
                "files": large_files
            }

        return {"status": "passed", "message": "No large files detected"}

    def check_lint(self) -> Dict:
        """Run linting checks if available."""
        # Try common linters
        linters = [
            (["pylint", "--version"], ["pylint", "--errors-only"]),
            (["flake8", "--version"], ["flake8"]),
            (["eslint", "--version"], ["eslint", "."]),
        ]

        for version_cmd, lint_cmd in linters:
            success, _ = self.run_command(version_cmd)
            if success:
                lint_success, lint_output = self.run_command(lint_cmd)
                if lint_success:
                    return {"status": "passed", "message": f"Linting passed ({lint_cmd[0]})"}
                else:
                    return {
                        "status": "failed",
                        "message": f"Linting failed ({lint_cmd[0]})",
                        "output": lint_output[:500]
                    }

        return {"status": "skipped", "message": "No linter found"}

    def check_format(self, auto_fix: bool = False) -> Dict:
        """Check code formatting."""
        formatters = [
            (["black", "--version"], ["black", "--check", "."]),
            (["prettier", "--version"], ["prettier", "--check", "."]),
        ]

        for version_cmd, format_cmd in formatters:
            success, _ = self.run_command(version_cmd)
            if success:
                if auto_fix:
                    format_cmd = [cmd.replace("--check", "--write") if cmd == "--check" else cmd for cmd in format_cmd]

                format_success, format_output = self.run_command(format_cmd)

                if format_success:
                    return {"status": "passed", "message": f"Formatting passed ({format_cmd[0]})"}
                elif auto_fix:
                    return {"status": "fixed", "message": f"Formatting fixed ({format_cmd[0]})"}
                else:
                    return {
                        "status": "failed",
                        "message": f"Formatting issues found ({format_cmd[0]})",
                        "output": format_output[:500]
                    }

        return {"status": "skipped", "message": "No formatter found"}

    def execute(self, params: Dict) -> Dict:
        """Execute pre-commit checks."""
        checks_to_run = params.get("checks", ["conflicts", "secrets", "large_files"])
        auto_fix = params.get("auto_fix", False)

        results = {}
        all_passed = True

        if "conflicts" in checks_to_run:
            results["conflicts"] = self.check_conflicts()
            if results["conflicts"]["status"] == "failed":
                all_passed = False

        if "secrets" in checks_to_run:
            results["secrets"] = self.check_secrets()

        if "large_files" in checks_to_run:
            results["large_files"] = self.check_large_files()

        if "lint" in checks_to_run:
            results["lint"] = self.check_lint()
            if results["lint"]["status"] == "failed":
                all_passed = False

        if "format" in checks_to_run:
            results["format"] = self.check_format(auto_fix)
            if results["format"]["status"] == "failed":
                all_passed = False

        return {
            "success": True,
            "passed": all_passed,
            "checks": results,
            "summary": self._generate_summary(results)
        }

    def _generate_summary(self, results: Dict) -> str:
        """Generate a summary of check results."""
        passed = sum(1 for r in results.values() if r["status"] == "passed")
        failed = sum(1 for r in results.values() if r["status"] == "failed")
        warnings = sum(1 for r in results.values() if r["status"] == "warning")

        return f"{passed} passed, {failed} failed, {warnings} warnings"


def main():
    """Main entry point for the script."""
    try:
        input_data = sys.stdin.read()
        params = json.loads(input_data) if input_data.strip() else {}

        checker = PreCommitChecker()
        result = checker.execute(params)

        print(json.dumps(result, indent=2))
        sys.exit(0)

    except Exception as e:
        error_result = {"success": False, "error": str(e)}
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
