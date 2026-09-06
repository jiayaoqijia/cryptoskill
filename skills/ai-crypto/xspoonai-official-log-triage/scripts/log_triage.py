#!/usr/bin/env python3
"""
Log Triage & Fix Plan Generator

Analyzes error logs from CI/build/runtime and generates:
- Root-cause hypotheses
- Prioritized fix plans
- Verification checklists

Author: ETHPanda
Version: 1.0.0
License: MIT
"""

import argparse
import re
from pathlib import Path
from typing import List, Tuple, Pattern

# Error patterns and their corresponding fix strategies
# Format: (name, regex, [fix_steps])
PATTERNS: List[Tuple[str, Pattern[str], List[str]]] = [
    (
        "node_missing_module",
        re.compile(r"Cannot find module '([^']+)'"),
        [
            "Run a clean install: `rm -rf node_modules && pnpm install` (or npm/yarn).",
            "Check lockfile changes and Node version consistency (CI vs local).",
            "If it's a workspace/monorepo, ensure package is listed in the right package.json.",
        ],
    ),
    (
        "ts_type_error",
        re.compile(r"TS\d+:"),
        [
            "Locate the first TS error; fix types/interfaces before chasing follow-up errors.",
            "Run `pnpm -w typecheck` (or `tsc -p ...`) locally to reproduce.",
            "If recently upgraded TS, consider pinning TypeScript version.",
        ],
    ),
    (
        "python_module_not_found",
        re.compile(r"ModuleNotFoundError: No module named '([^']+)'"),
        [
            "Ensure dependency exists in requirements/pyproject; reinstall deps in a fresh venv.",
            "Check PYTHONPATH / working directory in CI.",
            "If using conda: `conda install <package>` or `pip install <package>`",
        ],
    ),
    (
        "hardhat_compile",
        re.compile(r"HardhatError|HH\d+:"),
        [
            "Run `pnpm hardhat compile --show-stack-traces` locally.",
            "Check Solidity compiler version in hardhat config matches contracts' pragma.",
            "If error is about artifacts/cache: remove `artifacts/ cache/` and recompile.",
        ],
    ),
    (
        "revert_reason",
        re.compile(r"reverted with reason string '([^']+)'"),
        [
            "The contract reverted with an explicit reason; trace the require() that emits it.",
            "Confirm test setup inputs (msg.sender, allowances, balances, chain fork) match expectations.",
        ],
    ),
    (
        "http_429",
        re.compile(r"\b429\b|rate limit", re.IGNORECASE),
        [
            "Add retries with exponential backoff; reduce concurrency.",
            "Use a higher-rate endpoint / set API key in CI secrets.",
            "Check if you're hitting daily/monthly quotas.",
        ],
    ),
    (
        "rust_compile_error",
        re.compile(r"error\[E\d+\]:", re.IGNORECASE),
        [
            "Read the first error carefully - Rust errors are usually very descriptive.",
            "Run `cargo clean && cargo build` to clear cached artifacts.",
            "Check Rust toolchain version: `rustc --version` and update if needed.",
        ],
    ),
    (
        "permission_denied",
        re.compile(r"permission denied|EACCES", re.IGNORECASE),
        [
            "Check file/directory permissions: `ls -la <path>`",
            "If in CI, ensure the runner has write access to the target directory.",
            "On Windows, check if file is locked by another process.",
        ],
    ),
    (
        "out_of_memory",
        re.compile(r"out of memory|OOM|heap out of memory", re.IGNORECASE),
        [
            "Increase memory limit in CI config or local environment.",
            "Check for memory leaks in loops or recursive functions.",
            "Use streaming/chunking for large data processing.",
        ],
    ),
    (
        "network_timeout",
        re.compile(r"timeout|ETIMEDOUT|ECONNREFUSED", re.IGNORECASE),
        [
            "Increase timeout values in config or test setup.",
            "Check network connectivity and firewall rules.",
            "Verify service/endpoint is actually running and accessible.",
        ],
    ),
]


def triage(text: str) -> List[Tuple[str, str, List[str]]]:
    """
    Scan log text for known error patterns.
    
    Args:
        text: Raw log content
        
    Returns:
        List of (pattern_name, matched_text, fix_steps) tuples
    """
    hits = []
    for name, regex, fixes in PATTERNS:
        match = regex.search(text)
        if match:
            matched_text = match.group(0)
            hits.append((name, matched_text, fixes))
    return hits


def to_markdown(hits: List[Tuple[str, str, List[str]]], raw_path: str) -> str:
    """
    Generate a Markdown-formatted triage report.
    
    Args:
        hits: List of pattern matches from triage()
        raw_path: Path to the original log file
        
    Returns:
        Formatted Markdown report string
    """
    if not hits:
        return f"""# Log Triage Report

## Summary
No known patterns matched. Please review the **first fatal error** line and share:
1. The command you ran
2. Environment versions (Node/Python/Rust/etc.)
3. ~30 lines around the first error

## Source
{raw_path}

## Next Steps
- Check for typos or config issues
- Search error message on Stack Overflow
- Enable verbose logging: add `--verbose` or `--show-stack-traces`
- Share more context in issue tracker for manual analysis
"""

    blocks = ["# Log Triage Report\n"]
    
    # Summary section
    blocks.append("## Summary\n")
    error_types = [name.replace("_", " ").title() for name, _, _ in hits]
    blocks.append(
        f"Detected {len(hits)} error pattern(s): {', '.join(error_types)}. "
        f"See prioritized fix plan below.\n\n"
    )
    
    # Source
    blocks.append(f"## Source\n`{raw_path}`\n\n")
    
    # Matched signatures
    blocks.append("## Matched error signatures\n")
    for i, (name, sig, _) in enumerate(hits, 1):
        blocks.append(f"{i}. **{name}**: `{sig}`\n")
    blocks.append("\n")
    
    # Fix plan (prioritized)
    blocks.append("## Fix plan (prioritized)\n")
    step_num = 1
    for _, _, fixes in hits:
        for fix in fixes:
            blocks.append(f"{step_num}. {fix}\n")
            step_num += 1
    blocks.append("\n")
    
    # Verification checklist
    blocks.append("## Verification checklist\n")
    blocks.append("- [ ] Re-run the exact failing command locally\n")
    blocks.append("- [ ] Re-run CI workflow and confirm green\n")
    blocks.append("- [ ] Add a regression test if applicable\n")
    blocks.append("- [ ] Document the fix in commit message or issue\n\n")
    
    # Additional context
    blocks.append("## Additional context questions\n")
    blocks.append("If the above fixes don't work, please provide:\n")
    blocks.append("1. What was the exact command that failed?\n")
    blocks.append("2. What environment are you running in? (OS, versions, CI platform)\n")
    blocks.append("3. What changed recently? (dependencies, config, code)\n")
    
    return "".join(blocks)


def to_text(hits: List[Tuple[str, str, List[str]]], raw_path: str) -> str:
    """
    Generate a plain-text triage report.
    
    Args:
        hits: List of pattern matches from triage()
        raw_path: Path to the original log file
        
    Returns:
        Formatted plain text report
    """
    if not hits:
        return f"""LOG TRIAGE REPORT
{'=' * 60}

SUMMARY: No known patterns matched.

Please review the first fatal error line and share:
1. The command you ran
2. Environment versions
3. ~30 lines around the first error

SOURCE: {raw_path}
"""

    lines = ["LOG TRIAGE REPORT", "=" * 60, ""]
    
    # Summary
    error_types = [name.replace("_", " ").title() for name, _, _ in hits]
    lines.append(f"SUMMARY: Detected {len(hits)} error pattern(s)")
    lines.append(f"         {', '.join(error_types)}")
    lines.append("")
    
    # Source
    lines.append(f"SOURCE: {raw_path}")
    lines.append("")
    
    # Matched signatures
    lines.append("MATCHED ERROR SIGNATURES:")
    for i, (name, sig, _) in enumerate(hits, 1):
        lines.append(f"  {i}. {name}: {sig}")
    lines.append("")
    
    # Fix plan
    lines.append("FIX PLAN (PRIORITIZED):")
    step_num = 1
    for _, _, fixes in hits:
        for fix in fixes:
            lines.append(f"  {step_num}. {fix}")
            step_num += 1
    lines.append("")
    
    # Verification
    lines.append("VERIFICATION CHECKLIST:")
    lines.append("  [ ] Re-run the exact failing command locally")
    lines.append("  [ ] Re-run CI workflow and confirm green")
    lines.append("  [ ] Add a regression test if applicable")
    
    return "\n".join(lines)


def main() -> None:
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Analyze error logs and generate fix plans",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a log file and output Markdown
  python log_triage.py --file ci_error.log --format md
  
  # Analyze a log file and output plain text
  python log_triage.py --file build_error.log --format txt
  
  # Use sample logs included with this skill
  python log_triage.py --file sample_log_node.txt --format md
        """,
    )
    
    parser.add_argument(
        "--file",
        required=True,
        help="Path to log file",
        type=Path,
    )
    parser.add_argument(
        "--format",
        default="md",
        choices=["md", "txt"],
        help="Output format: md (Markdown) or txt (plain text)",
    )
    
    args = parser.parse_args()
    
    # Read log file
    log_path: Path = args.file
    if not log_path.exists():
        print(f"Error: File not found: {log_path}")
        return
    
    try:
        text = log_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Analyze
    hits = triage(text)
    
    # Generate report
    if args.format == "md":
        output = to_markdown(hits, str(log_path))
    else:
        output = to_text(hits, str(log_path))
    
    print(output)


if __name__ == "__main__":
    main()
