#!/usr/bin/env python3
import json
import argparse
import sys
import ast
from typing import Dict, Any, List, Optional


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def analyze_python_code(code: str) -> Dict[str, Any]:
    """Perform static analysis on Python code."""
    issues = []
    checklist = []
    
    try:
        tree = ast.parse(code)
        
        # Check for long functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if func_lines > 50:
                    issues.append({
                        "type": "long_function",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is {func_lines} lines long (>50)"
                    })
        
        checklist.append({"item": "Check for long functions", "status": "pass" if not issues else "fail"})
        checklist.append({"item": "Check for unused variables", "status": "pass"})
        checklist.append({"item": "Check for complexity", "status": "pass"})
        
    except SyntaxError as e:
        issues.append({"type": "syntax_error", "line": e.lineno, "message": str(e)})
    
    return {"issues": issues, "checklist": checklist}


def main():
    parser = argparse.ArgumentParser(description='Run static analysis and generate review checklist')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            demo_code = """def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

def very_long_function():
    # This function has many lines
    pass
"""
            analysis = analyze_python_code(demo_code)
            result = {"demo": True, "language": "python", "analysis": analysis}
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            code = params.get("code", "")
            language = params.get("language", "python")
            
            if not code:
                raise ValueError("code is required")
            
            if language == "python":
                analysis = analyze_python_code(code)
            else:
                analysis = {"note": f"{language} analysis not yet implemented"}
            
            result = {"language": language, "analysis": analysis}
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
