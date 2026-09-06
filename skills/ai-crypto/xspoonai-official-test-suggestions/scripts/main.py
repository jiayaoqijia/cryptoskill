#!/usr/bin/env python3
import json
import argparse
import sys
import ast
import re
from typing import Dict, Any, List, Optional, Set
from datetime import datetime


# Edge case patterns and suggestions
EDGE_CASE_PATTERNS = {
    "empty_input": ["empty list", "empty string", "None", "empty dict"],
    "boundary_values": ["0", "-1", "very large number", "max_int", "min_int"],
    "type_errors": ["wrong type input", "mixed types", "unexpected None"],
    "state_mutations": ["verify immutability", "check side effects", "state after calls"],
    "error_conditions": ["raise exception", "return error code", "invalid state"],
    "concurrency": ["thread safety", "race conditions", "concurrent calls"]
}


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def extract_function_signature(func_node: ast.FunctionDef) -> Dict[str, Any]:
    """Extract detailed function signature information."""
    params = []
    for arg in func_node.args.args:
        params.append({"name": arg.arg, "type": "any"})
    
    # Check for type hints
    if func_node.returns:
        return_type = ast.unparse(func_node.returns) if hasattr(ast, 'unparse') else "unknown"
    else:
        return_type = "any"
    
    return {
        "name": func_node.name,
        "parameters": params,
        "return_type": return_type,
        "has_docstring": bool(ast.get_docstring(func_node)),
        "lineno": func_node.lineno
    }


def suggest_edge_cases(func_signature: Dict) -> List[Dict]:
    """Generate edge case test suggestions for a function."""
    suggestions = []
    param_count = len(func_signature["parameters"])
    
    # Empty input tests
    if param_count > 0:
        suggestions.append({
            "category": "empty_input",
            "test_name": f"test_{func_signature['name']}_with_empty_input",
            "description": "Test with empty/null inputs",
            "test_cases": [
                f"assert {func_signature['name']}(None) handles None gracefully",
                f"assert {func_signature['name']}([]) works with empty list",
                f"assert {func_signature['name']}('') handles empty string"
            ],
            "priority": "high"
        })
    
    # Boundary value tests
    suggestions.append({
        "category": "boundary_values",
        "test_name": f"test_{func_signature['name']}_boundary_values",
        "description": "Test boundary conditions and edge values",
        "test_cases": [
            f"assert {func_signature['name']}(0) is handled correctly",
            f"assert {func_signature['name']}(-1) is handled correctly",
            f"assert {func_signature['name']}(999999) doesn't overflow"
        ],
        "priority": "high"
    })
    
    # Type error tests
    suggestions.append({
        "category": "type_errors",
        "test_name": f"test_{func_signature['name']}_type_errors",
        "description": "Test type validation and error handling",
        "test_cases": [
            f"with pytest.raises(TypeError): {func_signature['name']}('string_when_int_expected')",
            f"with pytest.raises(TypeError): {func_signature['name']}(None)",
            f"assert isinstance({func_signature['name']}(...), {func_signature['return_type']})"
        ],
        "priority": "high"
    })
    
    # State mutation tests
    suggestions.append({
        "category": "state_mutations",
        "test_name": f"test_{func_signature['name']}_immutability",
        "description": "Test that function doesn't mutate input",
        "test_cases": [
            f"original = [1, 2, 3]; {func_signature['name']}(original); assert original == [1, 2, 3]",
            f"state_before = obj.state; {func_signature['name']}(obj); assert obj.state == state_before",
            "# Verify no global state was modified"
        ],
        "priority": "medium"
    })
    
    return suggestions


def suggest_assertions(func_signature: Dict) -> List[str]:
    """Generate assertion suggestions."""
    assertions = [
        "# Verify return type",
        f"assert isinstance(result, {func_signature['return_type']})",
        "",
        "# Verify return value correctness",
        "assert result is not None",
        "assert result != expected_wrong_value",
        "",
        "# Verify expected side effects (if any)",
        "# verify_called_once_with(...)"
    ]
    return assertions


def suggest_mocks(func_signature: Dict, code: str) -> List[Dict]:
    """Suggest mock objects needed for tests."""
    mocks = []
    
    # Check for external dependencies
    import_pattern = r'from\s+(\w+)|import\s+(\w+)'
    imports = set(re.findall(import_pattern, code))
    
    common_mocks = {
        "requests": {"suggestion": "@mock.patch('requests.get')", "reason": "Mock external API calls"},
        "time": {"suggestion": "@mock.patch('time.time')", "reason": "Mock time-dependent behavior"},
        "random": {"suggestion": "@mock.patch('random.random')", "reason": "Make random behavior deterministic"},
        "datetime": {"suggestion": "@mock.patch('datetime.datetime')", "reason": "Control datetime in tests"},
        "os": {"suggestion": "@mock.patch('os.path.exists')", "reason": "Mock file system operations"},
        "json": {"suggestion": "@mock.patch('json.loads')", "reason": "Mock JSON parsing"}
    }
    
    for module in imports:
        if module in common_mocks:
            mocks.append({
                "module": module,
                "suggestion": common_mocks[module]["suggestion"],
                "reason": common_mocks[module]["reason"]
            })
    
    return mocks


def suggest_test_fixtures(func_signature: Dict) -> List[Dict]:
    """Suggest pytest fixtures needed."""
    fixtures = []
    
    if len(func_signature["parameters"]) > 0:
        fixtures.append({
            "name": f"{func_signature['name']}_test_data",
            "scope": "function",
            "description": f"Valid test data for {func_signature['name']}",
            "fixture_code": f"""@pytest.fixture
def {func_signature['name']}_test_data():
    return {{"valid": True, "data": [1, 2, 3]}}"""
        })
    
    fixtures.append({
        "name": "mock_external_dependency",
        "scope": "module",
        "description": "Mock external service/database",
        "fixture_code": """@pytest.fixture
def mock_external_dependency():
    with mock.patch('module.external_call') as mock_ext:
        mock_ext.return_value = {"status": "success"}
        yield mock_ext"""
    })
    
    return fixtures


def generate_test_suite(func_signature: Dict, code: str) -> str:
    """Generate a complete test file template."""
    func_name = func_signature["name"]
    template = f'''import pytest
from unittest import mock
from module_under_test import {func_name}


class Test{func_name.title()}:
    """Test suite for {func_name} function."""
    
    def test_happy_path(self):
        """Test with valid inputs."""
        result = {func_name}(valid_input)
        assert result is not None
        assert isinstance(result, {func_signature['return_type']})
    
    def test_empty_input(self):
        """Test with empty/None inputs."""
        with pytest.raises(ValueError):
            {func_name}(None)
        
        with pytest.raises(ValueError):
            {func_name}([])
    
    def test_boundary_values(self):
        """Test boundary conditions."""
        assert {func_name}(0) == expected_value
        assert {func_name}(-1) == expected_value
        assert {func_name}(999999) == expected_value
    
    def test_type_validation(self):
        """Test type checking."""
        with pytest.raises(TypeError):
            {func_name}("invalid_type")
    
    @mock.patch('module.external_call')
    def test_with_mocks(self, mock_external):
        """Test with mocked dependencies."""
        mock_external.return_value = {{"status": "success"}}
        result = {func_name}(test_input)
        mock_external.assert_called_once()
        assert result is not None
    
    def test_no_side_effects(self):
        """Verify function doesn't mutate inputs."""
        original = [1, 2, 3]
        {func_name}(original)
        assert original == [1, 2, 3]
'''
    
    return template


def analyze_code(code: str) -> Dict[str, Any]:
    """Comprehensive code analysis for test generation."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"functions": []}
    
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            sig = extract_function_signature(node)
            edge_cases = suggest_edge_cases(sig)
            assertions = suggest_assertions(sig)
            mocks = suggest_mocks(sig, code)
            fixtures = suggest_test_fixtures(sig)
            
            functions.append({
                "signature": sig,
                "edge_cases": edge_cases,
                "assertion_templates": assertions,
                "required_mocks": mocks,
                "fixtures": fixtures,
                "test_template": generate_test_suite(sig, code)
            })
    
    return {"functions": functions}


def main():
    parser = argparse.ArgumentParser(description='Generate comprehensive test suggestions')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Real production code example
            demo_code = '''import requests
from datetime import datetime

def fetch_user_data(user_id, timeout=30):
    """
    Fetch user data from API.
    
    Args:
        user_id: Integer user ID
        timeout: Request timeout in seconds
    
    Returns:
        dict: User data or None if not found
    """
    if not user_id or user_id < 0:
        raise ValueError("user_id must be positive integer")
    
    try:
        response = requests.get(f"https://api.example.com/users/{user_id}", timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching user: {e}")
        return None

def calculate_total(items, tax_rate=0.1):
    """Calculate total with tax."""
    if not items:
        return 0
    
    return sum(items) * (1 + tax_rate)

def validate_email(email):
    """Simple email validation."""
    return "@" in email and "." in email
'''
            
            analysis = analyze_code(demo_code)
            result = {
                "demo": True,
                "timestamp": datetime.now().isoformat(),
                "language": "python",
                "file_analysis": analysis,
                "summary": {
                    "total_functions": len(analysis["functions"]),
                    "functions_needing_tests": len(analysis["functions"]),
                    "estimated_test_cases": len(analysis["functions"]) * 6
                }
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            code = params.get("code", "")
            language = params.get("language", "python")
            
            if not code:
                print(format_error("code parameter is required"))
                sys.exit(1)
            
            if language != "python":
                print(format_error(f"Language '{language}' not yet supported"))
                sys.exit(1)
            
            analysis = analyze_code(code)
            result = {
                "timestamp": datetime.now().isoformat(),
                "language": language,
                "file_analysis": analysis,
                "summary": {
                    "total_functions": len(analysis["functions"]),
                    "estimated_test_cases": len(analysis["functions"]) * 5
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

