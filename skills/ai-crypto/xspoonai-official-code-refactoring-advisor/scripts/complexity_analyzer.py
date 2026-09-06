#!/usr/bin/env python3
"""
Code Complexity Analyzer
Calculates cyclomatic complexity and maintainability metrics
"""

import ast
from typing import Dict, List, Any

class ComplexityAnalyzer:
    """Analyze code complexity metrics."""

    def calculate_cyclomatic_complexity(self, code: str) -> Dict[str, Any]:
        """Calculate cyclomatic complexity."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"error": "Invalid syntax", "complexity": 0}

        metrics = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_function_complexity(node)
                metrics[node.name] = {
                    "complexity": complexity,
                    "rating": self._rate_complexity(complexity),
                    "line_count": node.end_lineno - node.lineno if node.end_lineno else 0
                }

        avg_complexity = sum(m["complexity"] for m in metrics.values()) / len(metrics) if metrics else 0
        
        return {
            "functions": metrics,
            "average_complexity": round(avg_complexity, 2),
            "max_complexity": max((m["complexity"] for m in metrics.values()), default=0),
            "functions_high_complexity": sum(1 for m in metrics.values() if m["complexity"] > 10),
            "maintainability_index": self._calculate_maintainability_index(code, avg_complexity)
        }

    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.BoolOp)):
                # Count and/or operators
                if isinstance(child.op, (ast.And, ast.Or)):
                    complexity += len(child.values) - 1
        
        return complexity

    def _rate_complexity(self, complexity: int) -> str:
        """Rate complexity level."""
        if complexity <= 1:
            return "SIMPLE"
        elif complexity <= 5:
            return "EASY"
        elif complexity <= 10:
            return "MODERATE"
        elif complexity <= 20:
            return "COMPLEX"
        else:
            return "VERY_COMPLEX"

    def _calculate_maintainability_index(self, code: str, avg_complexity: float) -> Dict[str, Any]:
        """Calculate maintainability index (0-100)."""
        lines = len(code.split("\n"))
        comment_lines = sum(1 for line in code.split("\n") if line.strip().startswith("#"))
        
        # Simplified Maintainability Index
        halstead_volume = self._estimate_halstead_volume(code)
        
        mi = 171 - 5.2 * (halstead_volume ** 0.4) - 0.23 * avg_complexity - 16.2 * ((comment_lines / max(lines, 1)) ** 0.5)
        mi = max(0, min(100, mi))
        
        return {
            "score": round(mi, 1),
            "rating": self._rate_maintainability(mi),
            "factors": {
                "complexity_impact": round(-0.23 * avg_complexity, 2),
                "documentation_impact": round(16.2 * ((comment_lines / max(lines, 1)) ** 0.5), 2),
                "volume_impact": round(-5.2 * (halstead_volume ** 0.4), 2)
            }
        }

    def _estimate_halstead_volume(self, code: str) -> float:
        """Rough estimate of Halstead volume."""
        words = len(code.split())
        unique_words = len(set(code.split()))
        
        if unique_words == 0:
            return 0
        
        # Simplified Halstead: Volume = N * log2(n)
        import math
        n = words
        n_unique = unique_words
        
        if n_unique > 0:
            volume = n * math.log2(n_unique)
        else:
            volume = 0
        
        return volume / 1000  # Normalize

    def _rate_maintainability(self, score: float) -> str:
        """Rate maintainability."""
        if score >= 85:
            return "EXCELLENT"
        elif score >= 70:
            return "GOOD"
        elif score >= 50:
            return "FAIR"
        elif score >= 25:
            return "POOR"
        else:
            return "CRITICALLY_LOW"

    def analyze_module(self, code: str) -> Dict[str, Any]:
        """Complete analysis of code module."""
        complexity_data = self.calculate_cyclomatic_complexity(code)
        
        lines = len([l for l in code.split("\n") if l.strip()])
        blank_lines = len([l for l in code.split("\n") if not l.strip()])
        comment_lines = len([l for l in code.split("\n") if l.strip().startswith("#")])
        
        return {
            "complexity_analysis": complexity_data,
            "code_metrics": {
                "total_lines": lines + blank_lines,
                "code_lines": lines,
                "blank_lines": blank_lines,
                "comment_lines": comment_lines,
                "comment_ratio": round(comment_lines / max(lines, 1), 3)
            },
            "overall_health": self._generate_health_report(complexity_data),
            "recommendations": self._generate_recommendations(complexity_data)
        }

    def _generate_health_report(self, complexity_data: Dict) -> Dict[str, Any]:
        """Generate overall code health report."""
        avg_complexity = complexity_data.get("average_complexity", 0)
        high_complexity_count = complexity_data.get("functions_high_complexity", 0)
        
        if avg_complexity > 15:
            status = "CRITICAL"
            score = 20
        elif avg_complexity > 10:
            status = "POOR"
            score = 40
        elif avg_complexity > 7:
            status = "FAIR"
            score = 60
        elif avg_complexity > 4:
            status = "GOOD"
            score = 80
        else:
            status = "EXCELLENT"
            score = 95
        
        return {
            "overall_status": status,
            "health_score": score,
            "primary_issues": [
                f"High complexity functions: {high_complexity_count}"
            ] if high_complexity_count > 0 else ["Code health is good"]
        }

    def _generate_recommendations(self, complexity_data: Dict) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        if complexity_data.get("max_complexity", 0) > 15:
            recommendations.append("High complexity detected - refactor large functions")
        
        high_count = complexity_data.get("functions_high_complexity", 0)
        if high_count > 3:
            recommendations.append(f"{high_count} functions exceed complexity threshold - prioritize refactoring")
        
        avg = complexity_data.get("average_complexity", 0)
        if avg > 10:
            recommendations.append("Consider breaking down module-level complexity with composition")
        
        return recommendations or ["Code complexity is acceptable"]


if __name__ == "__main__":
    analyzer = ComplexityAnalyzer()
    
    test_code = """
def complex_function(a, b, c):
    if a > 0:
        if b > 0:
            if c > 0:
                return a + b + c
            else:
                return a + b
        else:
            if c > 0:
                return a + c
            else:
                return a
    elif b > 0:
        if c > 0:
            return b + c
        else:
            return b
    else:
        return c
    """
    
    result = analyzer.analyze_module(test_code)
    
    import json
    print(json.dumps(result, indent=2))
