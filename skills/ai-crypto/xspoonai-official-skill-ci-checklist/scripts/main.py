#!/usr/bin/env python3
import json
import argparse
import sys
import os
import re
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime


# CI/CD Quality Gate Thresholds
QUALITY_GATES = {
    "documentation_coverage": 80,
    "test_coverage": 50,
    "code_quality_score": 70,
    "required_sections": ["Usage", "Parameters", "Example"],
    "required_files": ["SKILL.md", "README.md", "scripts/main.py", "pull.md"]
}


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def validate_skill_structure(skill_path: str) -> Tuple[List[Dict], int]:
    """Validate skill directory structure and required files."""
    issues = []
    passed = 0
    
    for required_file in QUALITY_GATES["required_files"]:
        file_path = os.path.join(skill_path, required_file)
        if os.path.exists(file_path):
            passed += 1
            issues.append({
                "check": f"File exists: {required_file}",
                "status": "pass",
                "severity": "critical"
            })
        else:
            issues.append({
                "check": f"File exists: {required_file}",
                "status": "fail",
                "severity": "critical",
                "message": f"Missing {required_file}"
            })
    
    return issues, passed


def validate_readme(readme_path: str) -> Tuple[List[Dict], int]:
    """Validate README.md contains required sections."""
    issues = []
    passed = 0
    
    if not os.path.exists(readme_path):
        return issues, 0
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Check for required sections
    required_sections = {
        "Usage": r"## Usage|### Usage",
        "Parameters": r"## Parameters|### Parameters",
        "Example": r"## Example|### Example|## Examples|### Examples",
        "Overview": r"## Overview|### Overview",
        "Features": r"## Features|### Features",
        "Use Cases": r"## Use Cases|### Use Cases"
    }
    
    for section, pattern in required_sections.items():
        if re.search(pattern, content, re.IGNORECASE):
            passed += 1
            issues.append({
                "check": f"Section exists: {section}",
                "status": "pass",
                "severity": "high"
            })
        else:
            issues.append({
                "check": f"Section exists: {section}",
                "status": "fail" if section in ["Usage", "Parameters", "Example"] else "warning",
                "severity": "high",
                "message": f"Missing section: {section}"
            })
    
    # Check minimum length
    word_count = len(content.split())
    if word_count >= 200:
        passed += 1
        issues.append({
            "check": f"Documentation length ({word_count} words)",
            "status": "pass",
            "severity": "medium"
        })
    else:
        issues.append({
            "check": f"Documentation length ({word_count} words, min 200)",
            "status": "warning",
            "severity": "medium"
        })
    
    return issues, passed


def validate_skill_yaml(skill_path: str) -> Tuple[List[Dict], int]:
    """Validate SKILL.md YAML frontmatter."""
    issues = []
    passed = 0
    skill_file = os.path.join(skill_path, "SKILL.md")
    
    if not os.path.exists(skill_file):
        return issues, 0
    
    with open(skill_file, 'r') as f:
        content = f.read()
    
    required_fields = ["name", "track", "version", "summary"]
    yaml_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    
    if yaml_match:
        yaml_content = yaml_match.group(1)
        
        for field in required_fields:
            if f"{field}:" in yaml_content:
                passed += 1
                issues.append({
                    "check": f"YAML field exists: {field}",
                    "status": "pass",
                    "severity": "critical"
                })
            else:
                issues.append({
                    "check": f"YAML field exists: {field}",
                    "status": "fail",
                    "severity": "critical",
                    "message": f"Missing YAML field: {field}"
                })
    
    return issues, passed


def validate_python_script(script_path: str) -> Tuple[List[Dict], int]:
    """Validate Python script for required functionality."""
    issues = []
    passed = 0
    
    if not os.path.exists(script_path):
        issues.append({
            "check": "Python script exists and is executable",
            "status": "fail",
            "severity": "critical"
        })
        return issues, 0
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Check for required patterns
    checks = {
        "argparse imported": r"import argparse",
        "Demo mode handler": r"args\.demo|--demo",
        "Params mode handler": r"args\.params|--params",
        "JSON output handler": r"format_success|json\.dumps",
        "Error handler": r"format_error",
        "Main function": r"def main\(",
        "If __name__ == '__main__'": r"if __name__"
    }
    
    for check_name, pattern in checks.items():
        if re.search(pattern, content):
            passed += 1
            issues.append({
                "check": check_name,
                "status": "pass",
                "severity": "high"
            })
        else:
            issues.append({
                "check": check_name,
                "status": "fail",
                "severity": "high",
                "message": f"Missing implementation: {check_name}"
            })
    
    # Try to parse for syntax errors
    try:
        compile(content, script_path, 'exec')
        passed += 1
        issues.append({
            "check": "Python syntax valid",
            "status": "pass",
            "severity": "critical"
        })
    except SyntaxError as e:
        issues.append({
            "check": "Python syntax valid",
            "status": "fail",
            "severity": "critical",
            "message": f"Syntax error: {e}"
        })
    
    return issues, passed


def calculate_quality_metrics(all_issues: List[Dict]) -> Dict[str, Any]:
    """Calculate overall quality metrics."""
    total_checks = len(all_issues)
    passed = sum(1 for issue in all_issues if issue["status"] == "pass")
    failed = sum(1 for issue in all_issues if issue["status"] == "fail")
    warnings = sum(1 for issue in all_issues if issue["status"] == "warning")
    
    # Calculate quality score (0-100)
    quality_score = (passed / total_checks * 100) if total_checks > 0 else 0
    
    # Determine status
    if failed > 0:
        status = "failing"
    elif warnings > 0:
        status = "warning"
    elif quality_score >= 90:
        status = "excellent"
    elif quality_score >= 80:
        status = "good"
    elif quality_score >= 70:
        status = "acceptable"
    else:
        status = "needs_improvement"
    
    return {
        "total_checks": total_checks,
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "quality_score": round(quality_score, 1),
        "status": status
    }


def validate_skill(skill_path: str, skill_name: str) -> Dict[str, Any]:
    """Comprehensive skill validation."""
    all_issues = []
    
    # Run all validations
    structure_issues, _ = validate_skill_structure(skill_path)
    all_issues.extend(structure_issues)
    
    readme_issues, _ = validate_readme(os.path.join(skill_path, "README.md"))
    all_issues.extend(readme_issues)
    
    yaml_issues, _ = validate_skill_yaml(skill_path)
    all_issues.extend(yaml_issues)
    
    script_issues, _ = validate_python_script(os.path.join(skill_path, "scripts/main.py"))
    all_issues.extend(script_issues)
    
    # Calculate metrics
    metrics = calculate_quality_metrics(all_issues)
    
    # Group issues by category
    categories = {
        "critical": [i for i in all_issues if i.get("severity") == "critical"],
        "high": [i for i in all_issues if i.get("severity") == "high"],
        "medium": [i for i in all_issues if i.get("severity") == "medium"],
        "low": [i for i in all_issues if i.get("severity") == "low"]
    }
    
    return {
        "skill": skill_name,
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics,
        "checks_by_severity": {
            "critical": len(categories["critical"]),
            "high": len(categories["high"]),
            "medium": len(categories["medium"]),
            "low": len(categories["low"])
        },
        "issues": all_issues,
        "critical_issues": categories["critical"],
        "recommendations": generate_recommendations(all_issues, metrics)
    }


def generate_recommendations(issues: List[Dict], metrics: Dict) -> List[str]:
    """Generate actionable recommendations."""
    recommendations = []
    
    failed_issues = [i for i in issues if i["status"] == "fail"]
    
    if metrics["status"] == "failing":
        recommendations.append("CRITICAL: Address all failing checks before merging")
    
    for issue in failed_issues[:5]:
        if "message" in issue:
            recommendations.append(f"Fix: {issue['message']}")
    
    if metrics["quality_score"] < 80:
        recommendations.append("Improve documentation coverage and completeness")
    
    if not any("--demo" in str(i) for i in issues):
        recommendations.append("Ensure --demo mode is fully implemented and tested")
    
    if not any("Python syntax" in str(i) for i in issues):
        recommendations.append("Run syntax validation on Python scripts")
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(description='Validate skill quality and CI/CD readiness')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    parser.add_argument('--skill-path', type=str, help='Path to skill directory')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Validate the ci-checklist skill itself as demo
            demo_path = "/Users/sambitsargam/Desktop/spoon-skills-pack/platform-challenge/skill-ci-checklist"
            if os.path.exists(demo_path):
                result = validate_skill(demo_path, "skill-ci-checklist")
            else:
                # Fallback demo
                result = {
                    "demo": True,
                    "skill": "api-webhook-signer",
                    "timestamp": datetime.now().isoformat(),
                    "metrics": {
                        "total_checks": 24,
                        "passed": 22,
                        "failed": 0,
                        "warnings": 2,
                        "quality_score": 91.7,
                        "status": "excellent"
                    },
                    "checks_by_severity": {"critical": 4, "high": 8, "medium": 2, "low": 1},
                    "critical_issues": [],
                    "recommendations": ["All quality gates passed", "Consider adding type hints"]
                }
            
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            skill_path = params.get("skill_path") or args.skill_path
            skill_name = params.get("skill_name", "unknown")
            
            if not skill_path or not os.path.exists(skill_path):
                print(format_error("skill_path must be valid and accessible"))
                sys.exit(1)
            
            result = validate_skill(skill_path, skill_name)
            print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()

