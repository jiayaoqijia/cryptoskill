#!/usr/bin/env python3
import json
import argparse
import sys
import ast
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


# Code smell severity levels
CODE_SMELL_SEVERITY = {
    "long_method": {"level": "high", "points": 8},
    "long_class": {"level": "high", "points": 8},
    "large_parameters": {"level": "medium", "points": 5},
    "duplicate_code": {"level": "medium", "points": 5},
    "deep_nesting": {"level": "medium", "points": 5},
    "magic_numbers": {"level": "low", "points": 2},
    "unused_variables": {"level": "low", "points": 2},
    "missing_docstrings": {"level": "low", "points": 2}
}

# Technical debt estimation
EFFORT_HOURS = {
    "critical": 8,
    "high": 4,
    "medium": 2,
    "low": 0.5
}


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def analyze_code_smells(code: str) -> Tuple[List[Dict], int]:
    """Detect code smells and return issues with severity scoring."""
    issues = []
    smell_score = 0
    
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return [], 0
    
    lines = code.split('\n')
    
    # Check for long methods (>20 lines)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_length = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
            
            if func_length > 20:
                metric = CODE_SMELL_SEVERITY["long_method"]
                issues.append({
                    "type": "long_method",
                    "name": node.name,
                    "lines": func_length,
                    "severity": metric["level"],
                    "threshold": 20,
                    "description": f"Function '{node.name}' is {func_length} lines (threshold: 20)"
                })
                smell_score += metric["points"]
            
            # Check parameter count
            if len(node.args.args) > 4:
                metric = CODE_SMELL_SEVERITY["large_parameters"]
                issues.append({
                    "type": "large_parameters",
                    "name": node.name,
                    "param_count": len(node.args.args),
                    "severity": metric["level"],
                    "threshold": 4,
                    "description": f"Function '{node.name}' has {len(node.args.args)} parameters (threshold: 4)"
                })
                smell_score += metric["points"]
            
            # Check for missing docstring
            if not ast.get_docstring(node):
                metric = CODE_SMELL_SEVERITY["missing_docstrings"]
                issues.append({
                    "type": "missing_docstrings",
                    "name": node.name,
                    "severity": metric["level"],
                    "description": f"Function '{node.name}' has no docstring"
                })
                smell_score += metric["points"]
    
    # Check for classes (long class)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_length = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
            if class_length > 100:
                metric = CODE_SMELL_SEVERITY["long_class"]
                issues.append({
                    "type": "long_class",
                    "name": node.name,
                    "lines": class_length,
                    "severity": metric["level"],
                    "threshold": 100,
                    "description": f"Class '{node.name}' is {class_length} lines (threshold: 100)"
                })
                smell_score += metric["points"]
    
    # Check for magic numbers
    magic_number_pattern = re.compile(r'\b[0-9]{2,}\b')
    for i, line in enumerate(lines, 1):
        if magic_number_pattern.search(line):
            metric = CODE_SMELL_SEVERITY["magic_numbers"]
            issues.append({
                "type": "magic_numbers",
                "line": i,
                "code": line.strip(),
                "severity": metric["level"],
                "description": f"Line {i} contains magic number(s)"
            })
            smell_score += metric["points"]
            break  # Only report once
    
    return issues, smell_score


def calculate_technical_debt(code_smells: List[Dict], dependencies: List[Dict]) -> Dict:
    """Calculate technical debt metrics."""
    total_issues = len(code_smells)
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    total_hours = 0
    
    for smell in code_smells:
        severity = smell.get("severity")
        severity_counts[severity] += 1
        total_hours += EFFORT_HOURS.get(severity, 0)
    
    # Outdated dependencies factor
    outdated_deps = sum(1 for d in dependencies if d.get("outdated", False))
    debt_hours = total_hours + (outdated_deps * 2)
    
    # Calculate debt percentage (assuming 160 hours per sprint)
    debt_percentage = min((debt_hours / 160) * 100, 100)
    
    return {
        "total_issues": total_issues,
        "severity_breakdown": severity_counts,
        "estimated_hours": round(debt_hours, 1),
        "debt_percentage": round(debt_percentage, 1),
        "risk_level": "critical" if debt_percentage > 50 else "high" if debt_percentage > 25 else "medium"
    }


def generate_refactoring_roadmap(code_smells: List[Dict], dependencies: List[Dict]) -> List[Dict]:
    """Generate prioritized refactoring tasks."""
    tasks = []
    task_id = 1
    
    # Group by severity
    by_severity = {}
    for smell in code_smells:
        severity = smell.get("severity")
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(smell)
    
    # Add critical/high priority tasks
    for smell in by_severity.get("high", []):
        if smell["type"] == "long_method":
            tasks.append({
                "id": task_id,
                "priority": 1,
                "effort": "medium",
                "hours": EFFORT_HOURS["high"],
                "type": "refactor_function",
                "target": smell["name"],
                "description": f"Break down '{smell['name']}' into smaller functions",
                "acceptance_criteria": [
                    f"Function should be < 20 lines",
                    "All tests pass",
                    "Extract reusable modules"
                ]
            })
            task_id += 1
        elif smell["type"] == "large_parameters":
            tasks.append({
                "id": task_id,
                "priority": 1,
                "effort": "medium",
                "hours": EFFORT_HOURS["medium"],
                "type": "refactor_signature",
                "target": smell["name"],
                "description": f"Reduce parameters for '{smell['name']}' using parameter objects",
                "acceptance_criteria": [
                    f"Parameter count < 4",
                    "Create parameter object/class",
                    "Update all call sites"
                ]
            })
            task_id += 1
    
    # Add documentation tasks
    docstring_issues = [s for s in code_smells if s["type"] == "missing_docstrings"]
    if docstring_issues:
        tasks.append({
            "id": task_id,
            "priority": 2,
            "effort": "low",
            "hours": 1,
            "type": "documentation",
            "target": f"{len(docstring_issues)} functions",
            "description": "Add comprehensive docstrings to undocumented functions",
            "acceptance_criteria": [
                "All functions documented",
                "Include parameter/return descriptions",
                "Add usage examples where applicable"
            ]
        })
        task_id += 1
    
    # Add dependency update tasks
    if len(dependencies) > 3:
        tasks.append({
            "id": task_id,
            "priority": 2,
            "effort": "medium",
            "hours": 2,
            "type": "dependency_update",
            "target": f"{len(dependencies)} dependencies",
            "description": "Update outdated dependencies to latest versions",
            "acceptance_criteria": [
                "All dependencies updated",
                "Run full test suite",
                "Verify compatibility"
            ]
        })
    
    return tasks


def main():
    parser = argparse.ArgumentParser(description='Generate comprehensive refactoring plans')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Real legacy code example
            legacy_code = '''
def process_user_data(u_id, u_name, u_email, u_phone, u_addr, u_city, u_zip, extra1, extra2):
    # No docstring
    if u_id > 0:
        if u_name:
            if u_email:
                if len(u_email) > 5:
                    users = []
                    for i in range(100):
                        users.append({"id": u_id + i, "name": u_name})
                    for user in users:
                        print(user)
                    result = 99999
                    if result > 50000:
                        print("Large")
    return True

class DataProcessor:
    def __init__(self):
        self.data = []
    def proc1(self): pass
    def proc2(self): pass
    def proc3(self): pass
    def proc4(self): pass
'''
            
            demo_deps = [
                {"name": "requests", "version": "2.25.0", "latest": "2.31.0", "outdated": True},
                {"name": "flask", "version": "2.0.0", "latest": "2.3.0", "outdated": True},
                {"name": "numpy", "version": "1.21.0", "latest": "1.24.0", "outdated": True}
            ]
            
            code_smells, smell_score = analyze_code_smells(legacy_code)
            debt = calculate_technical_debt(code_smells, demo_deps)
            roadmap = generate_refactoring_roadmap(code_smells, demo_deps)
            
            result = {
                "demo": True,
                "timestamp": datetime.now().isoformat(),
                "project": "legacy-app",
                "analysis": {
                    "code_smells": code_smells,
                    "smell_score": smell_score,
                    "technical_debt": debt,
                    "refactoring_roadmap": roadmap,
                    "summary": {
                        "total_issues": len(code_smells),
                        "estimated_effort_days": round(debt["estimated_hours"] / 8, 1),
                        "recommended_priority": "immediate"
                    }
                }
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            code = params.get("code", "")
            dependencies = params.get("dependencies", [])
            
            if not code:
                print(format_error("code parameter is required"))
                sys.exit(1)
            
            code_smells, smell_score = analyze_code_smells(code)
            debt = calculate_technical_debt(code_smells, dependencies)
            roadmap = generate_refactoring_roadmap(code_smells, dependencies)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "analysis": {
                    "code_smells": code_smells,
                    "smell_score": smell_score,
                    "technical_debt": debt,
                    "refactoring_roadmap": roadmap
                }
            }
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

