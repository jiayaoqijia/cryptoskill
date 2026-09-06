#!/usr/bin/env python3

import json
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime


# README linting rules
LINTING_RULES = {
    "required_sections": ["Overview", "Features", "Usage", "Use Cases", "Parameters", "Example Output"],
    "min_word_count": 200,
    "max_line_length": 120,
    "min_code_blocks": 1,
    "required_markdown_elements": ["#", "##", "```"]
}


def format_success(data):
    """Format successful JSON response."""
    return json.dumps({"ok": True, "data": data})


def format_error(error):
    """Format error JSON response."""
    return json.dumps({"ok": False, "error": error})




def check_sections(content):
    """Verify all required sections are present."""
    sections_found = {}
    
    for section in LINTING_RULES["required_sections"]:
        pattern = rf"^## {section}"
        found = bool(re.search(pattern, content, re.IGNORECASE | re.MULTILINE))
        sections_found[section] = found
    
    missing = [s for s, found in sections_found.items() if not found]
    
    return {
        "all_present": len(missing) == 0,
        "found": {s: found for s, found in sections_found.items() if found},
        "missing": missing,
        "count": sum(1 for f in sections_found.values() if f)
    }


def check_word_count(content):
    """Verify README has sufficient content."""
    word_count = len(content.split())
    min_words = LINTING_RULES["min_word_count"]
    
    return {
        "word_count": word_count,
        "min_required": min_words,
        "sufficient": word_count >= min_words,
        "status": "✓" if word_count >= min_words else "✗"
    }


def check_code_blocks(content):
    """Verify code examples are present."""
    blocks = len(re.findall(r"```", content)) // 2
    min_blocks = LINTING_RULES["min_code_blocks"]
    
    return {
        "count": blocks,
        "min_required": min_blocks,
        "sufficient": blocks >= min_blocks,
        "status": "✓" if blocks >= min_blocks else "✗"
    }


def check_formatting(content):
    """Validate markdown formatting quality."""
    issues = []
    
    # Check line lengths
    lines = content.split("\n")
    long_lines = []
    for i, line in enumerate(lines, 1):
        if len(line) > LINTING_RULES["max_line_length"] and not line.strip().startswith("http"):
            long_lines.append(i)
    
    if long_lines:
        issues.append(f"Lines exceed {LINTING_RULES['max_line_length']} chars: {long_lines[:3]}")
    
    # Check for broken markdown links
    broken_links = re.findall(r"\[([^\]]+)\]\(\s*\)", content)
    if broken_links:
        issues.append(f"Found {len(broken_links)} broken markdown links")
    
    # Check heading hierarchy
    headings = re.findall(r"^(#+) (.+)$", content, re.MULTILINE)
    if headings:
        first_level = len(headings[0][0])
        if first_level != 1:
            issues.append(f"Document should start with # (H1), found {'#' * first_level}")
    
    # Check for proper spacing after headers
    header_spacing = re.findall(r"^#{1,6}[^ ]", content, re.MULTILINE)
    if header_spacing:
        issues.append("Headers should have space after #")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "long_lines": len(long_lines),
        "broken_links": len(broken_links)
    }


def check_headers(content):
    """Analyze header structure and naming."""
    headers = re.findall(r"^(#{1,6}) (.+)$", content, re.MULTILINE)
    
    levels = [len(h[0]) for h in headers]
    unique_levels = set(levels)
    
    return {
        "total_headers": len(headers),
        "header_levels": sorted(list(unique_levels)),
        "proper_hierarchy": min(levels) == 1 if levels else False,
        "headers": headers
    }


def check_tables(content):
    """Verify parameter tables if present."""
    # Look for markdown tables
    table_pattern = r"\|\s*\w+.*?\|\n\|.*?\|"
    tables = re.findall(table_pattern, content, re.MULTILINE)
    
    tables_valid = all("|" in t and "---" in content for t in tables) if tables else True
    
    return {
        "has_tables": len(tables) > 0,
        "table_count": len(tables),
        "valid": tables_valid
    }


def lint_readme(readme_path):
    """Run comprehensive README linting."""
    readme_path = Path(readme_path)
    
    if not readme_path.exists():
        return format_error(f"README not found: {readme_path}")
    
    try:
        content = readme_path.read_text(encoding='utf-8')
    except Exception as e:
        return format_error(f"Cannot read README: {e}")
    
    # Run all checks
    sections = check_sections(content)
    word_count = check_word_count(content)
    code_blocks = check_code_blocks(content)
    formatting = check_formatting(content)
    headers = check_headers(content)
    tables = check_tables(content)
    
    # Calculate score (0-100)
    checks_passed = [
        sections["all_present"],
        word_count["sufficient"],
        code_blocks["sufficient"],
        formatting["valid"],
        headers["proper_hierarchy"]
    ]
    
    score = (sum(checks_passed) / len(checks_passed)) * 100
    
    result = {
        "readme_path": str(readme_path),
        "linting_score": score,
        "status": "valid" if score == 100 else "needs_fixes",
        "file_size_bytes": len(content),
        "checks": {
            "sections": sections,
            "word_count": word_count,
            "code_blocks": code_blocks,
            "formatting": formatting,
            "headers": headers,
            "tables": tables
        },
        "summary": {
            "checks_passed": sum(checks_passed),
            "checks_total": len(checks_passed),
            "issues": []
        }
    }
    
    # Collect issues
    if not sections["all_present"]:
        for section in sections["missing"]:
            result["summary"]["issues"].append(f"Missing section: ## {section}")
    
    if not word_count["sufficient"]:
        result["summary"]["issues"].append(f"Insufficient content ({word_count['word_count']} words, need {word_count['min_required']})")
    
    if not code_blocks["sufficient"]:
        result["summary"]["issues"].append(f"Not enough code examples ({code_blocks['count']} found, need {code_blocks['min_required']})")
    
    if not formatting["valid"]:
        result["summary"]["issues"].extend(formatting["issues"])
    
    if not headers["proper_hierarchy"]:
        result["summary"]["issues"].append("Header hierarchy not starting with H1")
    
    return format_success(result)


def demo_linting():
    """Run demo linting on sample README."""
    demo_data = {
        "demo": True,
        "timestamp": datetime.now().isoformat(),
        "files_linted": [
            {
                "readme_path": "/Users/sambitsargam/Desktop/spoon-skills-pack/ai-productivity/api-webhook-signer/README.md",
                "linting_score": 100.0,
                "status": "valid",
                "file_size_bytes": 2847,
                "summary": {
                    "checks_passed": 5,
                    "checks_total": 5,
                    "issues": []
                }
            },
            {
                "readme_path": "/Users/sambitsargam/Desktop/spoon-skills-pack/enterprise-skills/security-deps-audit/README.md",
                "linting_score": 100.0,
                "status": "valid",
                "file_size_bytes": 2654,
                "summary": {
                    "checks_passed": 5,
                    "checks_total": 5,
                    "issues": []
                }
            },
            {
                "readme_path": "/Users/sambitsargam/Desktop/spoon-skills-pack/platform-challenge/skill-ci-checklist/README.md",
                "linting_score": 100.0,
                "status": "valid",
                "file_size_bytes": 2712,
                "summary": {
                    "checks_passed": 5,
                    "checks_total": 5,
                    "issues": []
                }
            }
        ],
        "aggregate": {
            "total_files_checked": 3,
            "all_valid": 3,
            "average_score": 100.0,
            "recommendation": "All READMEs meet quality standards"
        }
    }
    
    return format_success(demo_data)


def main():
    parser = argparse.ArgumentParser(description="Lint and validate README files")
    parser.add_argument("--demo", action="store_true", help="Run demo linting")
    parser.add_argument("--params", type=str, help="JSON parameters with readme_path")
    parser.add_argument("--readme", type=str, help="Path to README file")
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            print(demo_linting())
        elif args.params:
            params = json.loads(args.params)
            readme_path = params.get("readme_path", "README.md")
            print(lint_readme(readme_path))
        elif args.readme:
            print(lint_readme(args.readme))
        else:
            print(demo_linting())
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
