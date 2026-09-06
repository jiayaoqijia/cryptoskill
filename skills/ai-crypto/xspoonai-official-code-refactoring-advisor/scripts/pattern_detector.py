#!/usr/bin/env python3
"""
Code Smell Pattern Detector
Detects common anti-patterns in Python and Solidity code
"""

import re
from typing import Dict, List, Any
import ast

class PatternDetector:
    """Detect code smells and anti-patterns."""

    def __init__(self):
        self.patterns = {
            "god_function": {
                "threshold": 50,  # lines
                "weight": 8,
                "description": "Function too large (>50 lines)"
            },
            "deep_nesting": {
                "threshold": 4,
                "weight": 7,
                "description": "Too many nested levels (>4)"
            },
            "long_parameter_list": {
                "threshold": 5,
                "weight": 6,
                "description": "Function has too many parameters (>5)"
            },
            "duplicate_code": {
                "threshold": 0.15,  # 15% similarity
                "weight": 9,
                "description": "Code duplication detected"
            },
            "magic_numbers": {
                "weight": 5,
                "description": "Unexplained literal numbers"
            },
            "insufficient_comments": {
                "threshold": 0.1,  # 10% comment ratio
                "weight": 3,
                "description": "Low code documentation"
            },
            "global_variables": {
                "weight": 8,
                "description": "Unsafe global state"
            },
            "catch_all_exception": {
                "weight": 9,
                "description": "Bare except clause"
            }
        }

    def detect_python_smells(self, code: str) -> Dict[str, Any]:
        """Detect code smells in Python code."""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"error": f"Syntax error: {e}", "smells": []}

        smells = []
        lines = code.split("\n")

        # Check all function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # God function detection
                func_lines = node.end_lineno - node.lineno
                if func_lines > 50:
                    smells.append({
                        "type": "god_function",
                        "line": node.lineno,
                        "name": node.name,
                        "lines": func_lines,
                        "severity": "HIGH",
                        "confidence": 95,
                        "recommendation": f"Split {node.name}() into smaller functions"
                    })

                # Parameter list check
                param_count = len(node.args.args) + len(node.args.kwonlyargs)
                if param_count > 5:
                    smells.append({
                        "type": "long_parameter_list",
                        "line": node.lineno,
                        "name": node.name,
                        "param_count": param_count,
                        "severity": "MEDIUM",
                        "confidence": 90,
                        "recommendation": f"Use dataclass or config object for {node.name}() parameters"
                    })

                # Nesting depth
                max_depth = self._calculate_nesting_depth(node)
                if max_depth > 4:
                    smells.append({
                        "type": "deep_nesting",
                        "line": node.lineno,
                        "name": node.name,
                        "depth": max_depth,
                        "severity": "MEDIUM",
                        "confidence": 85,
                        "recommendation": "Extract nested logic into separate functions"
                    })

            # Global variables
            elif isinstance(node, ast.Global):
                smells.append({
                    "type": "global_variables",
                    "line": node.lineno,
                    "severity": "HIGH",
                    "confidence": 100,
                    "recommendation": "Use class attributes or dependency injection instead"
                })

        # Bare except detection
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                smells.append({
                    "type": "catch_all_exception",
                    "line": node.lineno,
                    "severity": "CRITICAL",
                    "confidence": 100,
                    "recommendation": "Catch specific exception types instead of bare except"
                })

        # Magic numbers detection
        for node in ast.walk(tree):
            if isinstance(node, (ast.Constant)):
                if isinstance(node.value, (int, float)) and node.value > 0:
                    if node.lineno and node.lineno > 0:
                        smells.append({
                            "type": "magic_numbers",
                            "line": node.lineno,
                            "value": node.value,
                            "severity": "LOW",
                            "confidence": 60,
                            "recommendation": f"Define constant for magic number {node.value}"
                        })

        # Comment ratio
        comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
        comment_ratio = comment_lines / (code_lines + 1) if code_lines > 0 else 0

        if comment_ratio < 0.1 and code_lines > 20:
            smells.append({
                "type": "insufficient_comments",
                "comment_ratio": round(comment_ratio, 3),
                "severity": "LOW",
                "confidence": 75,
                "recommendation": f"Increase code documentation (current: {comment_ratio*100:.1f}%)"
            })

        # Calculate smell score
        total_severity = sum({
            "CRITICAL": 10,
            "HIGH": 8,
            "MEDIUM": 5,
            "LOW": 2
        }.get(s.get("severity", "LOW"), 0) for s in smells)

        return {
            "smells_detected": len(smells),
            "smell_score": min(100, total_severity),
            "code_quality": max(0, 100 - min(100, total_severity)),
            "critical_issues": sum(1 for s in smells if s.get("severity") == "CRITICAL"),
            "high_priority": sum(1 for s in smells if s.get("severity") == "HIGH"),
            "smells": sorted(smells, key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(x.get("severity", "LOW"), 4))
        }

    def detect_solidity_smells(self, code: str) -> Dict[str, Any]:
        """Detect code smells in Solidity code."""
        smells = []
        lines = code.split("\n")

        # Reentrancy pattern detection
        if "call" in code and "lock" not in code.lower():
            smells.append({
                "type": "reentrancy_risk",
                "severity": "CRITICAL",
                "confidence": 70,
                "recommendation": "Add reentrancy guard (OpenZeppelin ReentrancyGuard)"
            })

        # Unbounded loop
        for i, line in enumerate(lines, 1):
            if "for" in line and "length" not in line:
                smells.append({
                    "type": "unbounded_loop",
                    "line": i,
                    "severity": "MEDIUM",
                    "confidence": 60,
                    "recommendation": "Ensure loop has bounded iterations"
                })

        # Unchecked arithmetic
        if "+" in code and "SafeMath" not in code and "pragma solidity >=0.8" not in code:
            smells.append({
                "type": "unchecked_arithmetic",
                "severity": "HIGH",
                "confidence": 65,
                "recommendation": "Use SafeMath library for arithmetic operations"
            })

        # Visibility not explicit
        pattern = r"function\s+\w+\s*\("
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line) and "public" not in line and "private" not in line:
                smells.append({
                    "type": "unclear_visibility",
                    "line": i,
                    "severity": "MEDIUM",
                    "confidence": 80,
                    "recommendation": "Explicitly declare function visibility"
                })

        # Calculate score
        total_severity = sum({
            "CRITICAL": 10,
            "HIGH": 8,
            "MEDIUM": 5,
            "LOW": 2
        }.get(s.get("severity", "LOW"), 0) for s in smells)

        return {
            "smells_detected": len(smells),
            "smell_score": min(100, total_severity),
            "code_quality": max(0, 100 - min(100, total_severity)),
            "critical_issues": sum(1 for s in smells if s.get("severity") == "CRITICAL"),
            "smells": sorted(smells, key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(x.get("severity", "LOW"), 4))
        }

    def _calculate_nesting_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth."""
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                depth = self._calculate_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)
        return max_depth

    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Main entry point."""
        if language.lower() == "python":
            return self.detect_python_smells(code)
        elif language.lower() == "solidity":
            return self.detect_solidity_smells(code)
        else:
            return {"error": f"Language {language} not supported"}


if __name__ == "__main__":
    # Test code with smells
    test_code = """
def process_data(a, b, c, d, e, f):  # Many params
    for i in range(100):
        if condition1:
            if condition2:
                if condition3:
                    if condition4:
                        if condition5:  # Deep nesting
                            do_something()
    
    try:
        risky_operation()
    except:  # Bare except
        pass
    
    return 42  # Magic number
"""

    detector = PatternDetector()
    result = detector.analyze_code(test_code, "python")
    
    import json
    print(json.dumps(result, indent=2))
