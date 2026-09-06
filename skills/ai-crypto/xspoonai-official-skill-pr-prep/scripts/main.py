#!/usr/bin/env python3

import json
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime


# PR validation checklist
PR_CHECKLIST = {
    "files": ["SKILL.md", "README.md", "pull.md", "scripts/main.py"],
    "skill_md_fields": ["name", "description", "track", "version", "summary"],
    "readme_sections": ["Overview", "Features", "Usage", "Parameters", "Example Output"],
    "main_py_required": ["--demo", "--params", "json.dumps", '"ok"'],
    "code_quality": ["error handling", "docstrings", "type hints"]
}


def format_success(data):
    """Format successful JSON response."""
    return json.dumps({"ok": True, "data": data})


def format_error(error):
    """Format error JSON response."""
    return json.dumps({"ok": False, "error": error})


def check_files_exist(skill_path):
    """Verify all required files exist."""
    skill_path = Path(skill_path)
    results = {}
    
    for file in PR_CHECKLIST["files"]:
        file_path = skill_path / file
        results[file] = {
            "exists": file_path.exists(),
            "status": "✓" if file_path.exists() else "✗"
        }
    
    return results, all(r["exists"] for r in results.values())


def check_skill_md(skill_path):
    """Validate SKILL.md metadata."""
    skill_path = Path(skill_path)
    skill_md_path = skill_path / "SKILL.md"
    
    if not skill_md_path.exists():
        return {"valid": False, "error": "SKILL.md not found"}, False
    
    content = skill_md_path.read_text()
    
    # Extract YAML frontmatter
    match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {"valid": False, "error": "Missing YAML frontmatter"}, False
    
    frontmatter = match.group(1)
    missing = []
    
    for field in PR_CHECKLIST["skill_md_fields"]:
        if f"{field}:" not in frontmatter:
            missing.append(field)
    
    valid = len(missing) == 0
    return {
        "valid": valid,
        "fields_present": [f for f in PR_CHECKLIST["skill_md_fields"] if f"{f}:" in frontmatter],
        "missing_fields": missing
    }, valid


def check_readme(skill_path):
    """Validate README.md structure."""
    skill_path = Path(skill_path)
    readme_path = skill_path / "README.md"
    
    if not readme_path.exists():
        return {"valid": False, "error": "README.md not found"}, False
    
    content = readme_path.read_text()
    word_count = len(content.split())
    
    # Check for required sections
    sections_found = {}
    for section in PR_CHECKLIST["readme_sections"]:
        found = bool(re.search(rf"^## {section}", content, re.IGNORECASE | re.MULTILINE))
        sections_found[section] = found
    
    all_sections = all(sections_found.values())
    min_words = 200
    enough_content = word_count >= min_words
    valid = all_sections and enough_content
    
    return {
        "valid": valid,
        "word_count": word_count,
        "min_required_words": min_words,
        "sections_found": sections_found,
        "missing_sections": [s for s, found in sections_found.items() if not found],
        "code_blocks": len(re.findall(r"```", content)) // 2
    }, valid


def check_main_py(skill_path):
    """Validate scripts/main.py structure."""
    skill_path = Path(skill_path)
    main_py_path = skill_path / "scripts" / "main.py"
    
    if not main_py_path.exists():
        return {"valid": False, "error": "scripts/main.py not found"}, False
    
    content = main_py_path.read_text()
    
    checks = {}
    for item in PR_CHECKLIST["main_py_required"]:
        checks[item] = item in content
    
    checks["executable"] = content.startswith("#!/usr/bin/env python3")
    
    valid = all(checks.values())
    
    return {
        "valid": valid,
        "checks": checks,
        "issues": [k for k, v in checks.items() if not v]
    }, valid


def check_pull_md(skill_path):
    """Validate pull.md exists with content."""
    skill_path = Path(skill_path)
    pull_md_path = skill_path / "pull.md"
    
    if not pull_md_path.exists():
        return {"valid": False, "error": "pull.md not found"}, False
    
    content = pull_md_path.read_text()
    has_demo_output = "demo" in content.lower() or "output" in content.lower()
    
    return {
        "valid": True,
        "file_size": len(content),
        "has_demo_output": has_demo_output
    }, True


def validate_pr_readiness(skill_path):
    """Comprehensive PR readiness validation."""
    skill_path = Path(skill_path)
    
    if not skill_path.exists():
        return format_error(f"Skill path not found: {skill_path}")
    
    # Run all checks
    files_check, files_ok = check_files_exist(skill_path)
    skill_md_check, skill_md_ok = check_skill_md(skill_path)
    readme_check, readme_ok = check_readme(skill_path)
    main_py_check, main_py_ok = check_main_py(skill_path)
    pull_md_check, pull_md_ok = check_pull_md(skill_path)
    
    all_checks = [files_ok, skill_md_ok, readme_ok, main_py_ok, pull_md_ok]
    passed = sum(all_checks)
    total = len(all_checks)
    
    result = {
        "skill_path": str(skill_path),
        "ready_for_pr": all(all_checks),
        "checks_passed": passed,
        "total_checks": total,
        "quality_score": (passed / total) * 100,
        "validation_details": {
            "files": files_check,
            "skill_md": skill_md_check,
            "readme": readme_check,
            "main_py": main_py_check,
            "pull_md": pull_md_check
        },
        "issues": []
    }
    
    # Collect issues
    if not files_ok:
        for file, status in files_check.items():
            if not status["exists"]:
                result["issues"].append(f"Missing file: {file}")
    
    if not skill_md_ok:
        if "missing_fields" in skill_md_check:
            for field in skill_md_check["missing_fields"]:
                result["issues"].append(f"SKILL.md missing: {field}")
    
    if not readme_ok:
        if "missing_sections" in readme_check:
            for section in readme_check["missing_sections"]:
                result["issues"].append(f"README.md missing section: {section}")
        if readme_check.get("word_count", 0) < readme_check.get("min_required_words", 200):
            result["issues"].append(f"README.md too short ({readme_check['word_count']} words)")
    
    if not main_py_ok:
        for issue in main_py_check.get("issues", []):
            result["issues"].append(f"main.py: {issue}")
    
    if not pull_md_ok:
        result["issues"].append(pull_md_check.get("error", "pull.md validation failed"))
    
    return format_success(result)


def demo_validation():
    """Run demo validation on sample skills."""
    demo_data = {
        "demo": True,
        "validation_timestamp": datetime.now().isoformat(),
        "skills_checked": [
            {
                "skill_path": "/Users/sambitsargam/Desktop/spoon-skills-pack/ai-productivity/api-webhook-signer",
                "ready_for_pr": True,
                "checks_passed": 5,
                "total_checks": 5,
                "quality_score": 100.0,
                "issues": []
            },
            {
                "skill_path": "/Users/sambitsargam/Desktop/spoon-skills-pack/enterprise-skills/security-deps-audit",
                "ready_for_pr": True,
                "checks_passed": 5,
                "total_checks": 5,
                "quality_score": 100.0,
                "issues": []
            },
            {
                "skill_path": "/Users/sambitsargam/Desktop/spoon-skills-pack/platform-challenge/skill-ci-checklist",
                "ready_for_pr": True,
                "checks_passed": 5,
                "total_checks": 5,
                "quality_score": 100.0,
                "issues": []
            },
            {
                "skill_path": "/Users/sambitsargam/Desktop/spoon-skills-pack/web3-core-operations/erc20-allowance-manager",
                "ready_for_pr": True,
                "checks_passed": 5,
                "total_checks": 5,
                "quality_score": 100.0,
                "issues": []
            },
            {
                "skill_path": "/Users/sambitsargam/Desktop/spoon-skills-pack/web3-data-intelligence/whale-tracker",
                "ready_for_pr": True,
                "checks_passed": 5,
                "total_checks": 5,
                "quality_score": 100.0,
                "issues": []
            }
        ],
        "summary": {
            "total_skills_checked": 5,
            "ready_for_pr": 5,
            "not_ready": 0,
            "average_quality_score": 100.0,
            "recommendation": "All skills are ready for PR submission - no blockers found"
        }
    }
    
    return format_success(demo_data)


def main():
    parser = argparse.ArgumentParser(description="Validate skills before PR submission")
    parser.add_argument("--demo", action="store_true", help="Run demo validation")
    parser.add_argument("--params", type=str, help="JSON parameters with skill_path")
    parser.add_argument("--skill", type=str, help="Path to skill directory")
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            print(demo_validation())
        elif args.params:
            params = json.loads(args.params)
            skill_path = params.get("skill_path", ".")
            print(validate_pr_readiness(skill_path))
        elif args.skill:
            print(validate_pr_readiness(args.skill))
        else:
            print(demo_validation())
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
