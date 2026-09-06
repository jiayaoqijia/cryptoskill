#!/usr/bin/env python3
"""
Bottleneck Detector
Identifies performance bottlenecks in code and systems
"""

import re
from typing import Dict, List, Any
from collections import defaultdict

class BottleneckDetector:
    """Detects performance bottlenecks."""

    def __init__(self):
        self.bottleneck_patterns = {
            "nested_loops": {
                "pattern": r"for\s+\w+\s+in.*:\s*.*for\s+\w+\s+in",
                "severity": "HIGH",
                "description": "Nested loops can cause O(n²) complexity"
            },
            "n_plus_one": {
                "pattern": r"for.*:\s*.*\.query\(|for.*:\s*.*\.get\(",
                "severity": "HIGH",
                "description": "N+1 query pattern - database call per loop"
            },
            "string_concatenation": {
                "pattern": r"\w+\s*\+=\s*['\"][^'\"]*['\"]",
                "severity": "MEDIUM",
                "description": "String concatenation in loops creates new strings"
            },
            "large_list_operations": {
                "pattern": r"\.sort\(|\.reverse\(|\.copy\(",
                "severity": "MEDIUM",
                "description": "Expensive list operations inside loops"
            },
            "blocking_io": {
                "pattern": r"open\(|\.read\(|requests\.get|socket\.send",
                "severity": "HIGH",
                "description": "Blocking I/O operations block execution"
            },
            "global_lookups": {
                "pattern": r"globals\(\)|getattr|setattr|hasattr",
                "severity": "LOW",
                "description": "Global lookups are slower than local"
            }
        }

    def detect_code_bottlenecks(self, code: str) -> Dict[str, Any]:
        """Detect bottlenecks in code."""
        
        bottlenecks = []
        
        for bottle_type, pattern_info in self.bottleneck_patterns.items():
            matches = list(re.finditer(pattern_info["pattern"], code))
            
            if matches:
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    bottlenecks.append({
                        "type": bottle_type,
                        "severity": pattern_info["severity"],
                        "description": pattern_info["description"],
                        "line": line_num,
                        "code_snippet": code[max(0, match.start()-20):match.end()+20]
                    })
        
        return {
            "bottleneck_count": len(bottlenecks),
            "bottlenecks": bottlenecks,
            "severity_breakdown": self._breakdown_by_severity(bottlenecks),
            "recommendations": self._get_bottleneck_recommendations(bottlenecks)
        }

    def analyze_database_queries(self, queries: List[Dict]) -> Dict[str, Any]:
        """Analyze database query patterns."""
        
        issues = []
        total_queries = len(queries)
        
        # Check for N+1 patterns
        query_patterns = defaultdict(int)
        for query in queries:
            pattern = query.get("pattern", "")
            query_patterns[pattern] += 1
        
        if any(count > 10 for count in query_patterns.values()):
            issues.append({
                "type": "REPETITIVE_QUERIES",
                "severity": "HIGH",
                "description": "Same query executed multiple times",
                "recommendation": "Cache results or batch queries"
            })
        
        # Check for missing indexes
        missing_indexes = []
        for query in queries:
            if "SELECT" in query.get("sql", "").upper() and "WHERE" in query.get("sql", "").upper():
                if not query.get("has_index"):
                    missing_indexes.append(query.get("sql"))
        
        if missing_indexes:
            issues.append({
                "type": "MISSING_INDEXES",
                "severity": "CRITICAL",
                "count": len(missing_indexes),
                "recommendation": "Create indexes on WHERE clause columns"
            })
        
        # Check for slow queries
        slow_queries = [q for q in queries if q.get("execution_time_ms", 0) > 100]
        if slow_queries:
            issues.append({
                "type": "SLOW_QUERIES",
                "severity": "HIGH",
                "count": len(slow_queries),
                "slowest_ms": max(q.get("execution_time_ms", 0) for q in slow_queries),
                "recommendation": "Optimize with indexes, joins, or query rewriting"
            })
        
        return {
            "total_queries": total_queries,
            "query_patterns": dict(query_patterns),
            "issues": issues,
            "query_efficiency": max(0, 100 - len(issues) * 20)
        }

    def detect_memory_leaks(self, memory_samples: List[Dict]) -> Dict[str, Any]:
        """Detect memory leak patterns."""
        
        if len(memory_samples) < 3:
            return {
                "status": "INSUFFICIENT_DATA",
                "samples": len(memory_samples),
                "recommendation": "Collect more memory samples"
            }
        
        memory_values = [s.get("memory_mb", 0) for s in memory_samples]
        
        # Check for monotonic increase
        increases = sum(1 for i in range(len(memory_values) - 1) if memory_values[i+1] > memory_values[i])
        increase_ratio = increases / (len(memory_values) - 1)
        
        # Detect trend
        trend = None
        if increase_ratio > 0.7:
            trend = "GROWING"
            severity = "CRITICAL"
        elif increase_ratio > 0.5:
            trend = "INCREASING"
            severity = "HIGH"
        else:
            trend = "STABLE"
            severity = "LOW"
        
        return {
            "memory_trend": trend,
            "severity": severity,
            "initial_mb": round(memory_values[0], 2),
            "final_mb": round(memory_values[-1], 2),
            "growth_mb": round(memory_values[-1] - memory_values[0], 2),
            "increase_ratio": round(increase_ratio, 2),
            "potential_leak": increase_ratio > 0.7,
            "recommendations": [
                "Check for circular references",
                "Verify cache cleanup",
                "Profile long-running processes",
                "Use memory profiler tools"
            ] if trend != "STABLE" else []
        }

    def detect_concurrency_issues(self, code: str) -> Dict[str, Any]:
        """Detect concurrency-related issues."""
        
        issues = []
        
        # Check for lack of synchronization
        thread_creation = re.findall(r"Thread\(|threading\.Thread|multiprocessing\.Process", code)
        shared_vars = re.findall(r"global\s+\w+|class\s+\w+:.*\n.*self\.\w+\s*=", code)
        locks = re.findall(r"Lock\(|RLock\(|Semaphore", code)
        
        if thread_creation and shared_vars and not locks:
            issues.append({
                "type": "UNPROTECTED_SHARED_STATE",
                "severity": "CRITICAL",
                "description": "Shared state accessed without synchronization",
                "recommendation": "Use locks, mutexes, or thread-safe data structures"
            })
        
        # Check for deadlock potential
        lock_acquisitions = re.findall(r"\.acquire\(|with\s+\w+:", code)
        if len(lock_acquisitions) >= 2:
            issues.append({
                "type": "POTENTIAL_DEADLOCK",
                "severity": "HIGH",
                "description": "Multiple locks acquired - check ordering",
                "recommendation": "Ensure consistent lock acquisition order"
            })
        
        return {
            "thread_count": len(thread_creation),
            "issues": issues,
            "concurrency_risk": "HIGH" if issues else "LOW"
        }

    def analyze_io_operations(self, code: str) -> Dict[str, Any]:
        """Analyze I/O operation patterns."""
        
        io_patterns = {
            "blocking_io": re.findall(r"open\(|\.read\(|\.write\(|\.readlines\(", code),
            "http_requests": re.findall(r"requests\.|urllib\.request|http\.client", code),
            "database_ops": re.findall(r"\.execute\(|\.query\(|cursor\.", code),
            "file_operations": re.findall(r"\.readfile|\.writefile|\.append", code)
        }
        
        io_count = sum(len(v) for v in io_patterns.values())
        
        issues = []
        
        if io_count > 10:
            issues.append({
                "type": "HIGH_IO_VOLUME",
                "severity": "MEDIUM",
                "io_operations": io_count,
                "recommendation": "Consider batching or async I/O"
            })
        
        if len(io_patterns["blocking_io"]) > 0:
            issues.append({
                "type": "BLOCKING_IO",
                "severity": "HIGH",
                "operations": len(io_patterns["blocking_io"]),
                "recommendation": "Use async I/O (aio, asyncio) for better concurrency"
            })
        
        return {
            "total_io_operations": io_count,
            "io_patterns": {k: len(v) for k, v in io_patterns.items()},
            "issues": issues,
            "io_efficiency": max(0, 100 - len(issues) * 15)
        }

    # ===== Private Methods =====

    def _breakdown_by_severity(self, bottlenecks: List[Dict]) -> Dict[str, int]:
        """Break down bottlenecks by severity."""
        breakdown = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for bottleneck in bottlenecks:
            severity = bottleneck.get("severity", "LOW")
            if severity in breakdown:
                breakdown[severity] += 1
        
        return breakdown

    def _get_bottleneck_recommendations(self, bottlenecks: List[Dict]) -> List[str]:
        """Get recommendations based on detected bottlenecks."""
        recommendations = []
        
        types = set(b.get("type") for b in bottlenecks)
        
        if "nested_loops" in types:
            recommendations.append("Reduce nested loop complexity - consider using sets/dicts")
        
        if "n_plus_one" in types:
            recommendations.append("Use batch queries or caching instead of N+1 queries")
        
        if "string_concatenation" in types:
            recommendations.append("Use list.join() instead of += for strings")
        
        if "blocking_io" in types:
            recommendations.append("Use async I/O for non-blocking operations")
        
        if not recommendations:
            recommendations.append("Code structure looks efficient")
        
        return recommendations


if __name__ == "__main__":
    detector = BottleneckDetector()
    
    # Test code
    code = """
for i in range(1000):
    for j in range(1000):
        data = db.query(f"SELECT * WHERE id = {i}")
        result = result + str(i)
"""
    
    result = detector.detect_code_bottlenecks(code)
    
    import json
    print(json.dumps(result, indent=2))
