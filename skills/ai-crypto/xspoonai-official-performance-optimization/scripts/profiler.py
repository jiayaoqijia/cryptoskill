#!/usr/bin/env python3
"""
Performance Profiler
Profiles application performance and resource usage
"""

import time
import psutil
import os
from typing import Dict, List, Any, Callable
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProfileResult:
    """Performance profile result."""
    function_name: str
    execution_time_ms: float
    memory_used_mb: float
    cpu_percent: float
    call_count: int
    average_time_ms: float

class PerformanceProfiler:
    """Profiles application performance metrics."""

    def __init__(self):
        self.profiles = defaultdict(list)
        self.process = psutil.Process(os.getpid())

    def profile_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Profile a single function call."""
        
        start_memory = self.process.memory_info().rss / 1024 / 1024
        start_cpu = self.process.cpu_percent()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            exception = None
        except Exception as e:
            exception = str(e)
            result = None
        
        end_time = time.time()
        end_memory = self.process.memory_info().rss / 1024 / 1024
        end_cpu = self.process.cpu_percent()
        
        execution_time = (end_time - start_time) * 1000
        memory_used = end_memory - start_memory
        
        return {
            "function": func.__name__,
            "execution_time_ms": round(execution_time, 2),
            "memory_used_mb": round(memory_used, 2),
            "cpu_percent": round((start_cpu + end_cpu) / 2, 1),
            "success": exception is None,
            "exception": exception,
            "result": result
        }

    def batch_profile(self, functions: List[Dict]) -> Dict[str, Any]:
        """Profile multiple functions."""
        
        results = []
        total_time = 0
        total_memory = 0
        
        for func_info in functions:
            func = func_info.get("function")
            args = func_info.get("args", ())
            kwargs = func_info.get("kwargs", {})
            iterations = func_info.get("iterations", 1)
            
            times = []
            memories = []
            
            for _ in range(iterations):
                result = self.profile_function(func, *args, **kwargs)
                times.append(result["execution_time_ms"])
                memories.append(result["memory_used_mb"])
                results.append(result)
            
            avg_time = sum(times) / len(times)
            avg_memory = sum(memories) / len(memories)
            total_time += avg_time
            total_memory += avg_memory
        
        return {
            "total_functions": len(functions),
            "total_iterations": sum(f.get("iterations", 1) for f in functions),
            "results": results,
            "summary": {
                "total_execution_time_ms": round(total_time, 2),
                "total_memory_mb": round(total_memory, 2),
                "average_per_function_ms": round(total_time / len(functions), 2)
            }
        }

    def profile_code_block(self, code: str, globals_dict: Dict = None) -> Dict[str, Any]:
        """Profile a block of code."""
        
        if globals_dict is None:
            globals_dict = {}
        
        start_memory = self.process.memory_info().rss / 1024 / 1024
        start_time = time.time()
        
        try:
            exec(code, globals_dict)
            exception = None
        except Exception as e:
            exception = str(e)
        
        end_time = time.time()
        end_memory = self.process.memory_info().rss / 1024 / 1024
        
        return {
            "code_block": code[:100] + "..." if len(code) > 100 else code,
            "execution_time_ms": round((end_time - start_time) * 1000, 2),
            "memory_used_mb": round(end_memory - start_memory, 2),
            "success": exception is None,
            "exception": exception
        }

    def monitor_resource_usage(self, duration_seconds: int, interval: float = 0.1) -> Dict[str, Any]:
        """Monitor resource usage over time."""
        
        samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            samples.append({
                "timestamp": datetime.now().isoformat(),
                "memory_mb": round(self.process.memory_info().rss / 1024 / 1024, 2),
                "cpu_percent": round(self.process.cpu_percent(), 1),
                "threads": self.process.num_threads()
            })
            time.sleep(interval)
        
        memory_values = [s["memory_mb"] for s in samples]
        cpu_values = [s["cpu_percent"] for s in samples]
        
        return {
            "duration_seconds": duration_seconds,
            "sample_count": len(samples),
            "samples": samples,
            "statistics": {
                "memory": {
                    "min_mb": min(memory_values),
                    "max_mb": max(memory_values),
                    "avg_mb": round(sum(memory_values) / len(memory_values), 2),
                    "peak_mb": max(memory_values)
                },
                "cpu": {
                    "min_percent": min(cpu_values),
                    "max_percent": max(cpu_values),
                    "avg_percent": round(sum(cpu_values) / len(cpu_values), 1)
                }
            }
        }

    def compare_performance(self, baseline: Dict, current: Dict) -> Dict[str, Any]:
        """Compare performance between two runs."""
        
        baseline_time = baseline.get("execution_time_ms", 0)
        current_time = current.get("execution_time_ms", 0)
        
        baseline_memory = baseline.get("memory_used_mb", 0)
        current_memory = current.get("memory_used_mb", 0)
        
        time_diff = current_time - baseline_time
        time_percent = (time_diff / baseline_time * 100) if baseline_time > 0 else 0
        
        memory_diff = current_memory - baseline_memory
        memory_percent = (memory_diff / baseline_memory * 100) if baseline_memory > 0 else 0
        
        return {
            "execution_time": {
                "baseline_ms": baseline_time,
                "current_ms": current_time,
                "difference_ms": round(time_diff, 2),
                "percent_change": round(time_percent, 1),
                "improvement": "FASTER" if time_diff < 0 else "SLOWER"
            },
            "memory": {
                "baseline_mb": baseline_memory,
                "current_mb": current_memory,
                "difference_mb": round(memory_diff, 2),
                "percent_change": round(memory_percent, 1),
                "improvement": "REDUCED" if memory_diff < 0 else "INCREASED"
            },
            "overall_assessment": "IMPROVED" if time_diff < 0 and memory_diff < 0 else "DEGRADED"
        }

    def identify_hotspots(self, profiles: List[Dict]) -> Dict[str, Any]:
        """Identify performance hotspots."""
        
        sorted_by_time = sorted(profiles, key=lambda p: p.get("execution_time_ms", 0), reverse=True)
        sorted_by_memory = sorted(profiles, key=lambda p: p.get("memory_used_mb", 0), reverse=True)
        
        hotspots = []
        
        for i, profile in enumerate(sorted_by_time[:5]):
            if profile.get("execution_time_ms", 0) > 100:
                hotspots.append({
                    "rank": i + 1,
                    "type": "TIME",
                    "function": profile.get("function", "unknown"),
                    "metric": f"{profile.get('execution_time_ms', 0)}ms",
                    "severity": "CRITICAL" if profile.get("execution_time_ms", 0) > 1000 else "HIGH"
                })
        
        for i, profile in enumerate(sorted_by_memory[:5]):
            if profile.get("memory_used_mb", 0) > 10:
                hotspots.append({
                    "rank": i + 1,
                    "type": "MEMORY",
                    "function": profile.get("function", "unknown"),
                    "metric": f"{profile.get('memory_used_mb', 0)}MB",
                    "severity": "CRITICAL" if profile.get("memory_used_mb", 0) > 100 else "HIGH"
                })
        
        return {
            "hotspot_count": len(hotspots),
            "hotspots": hotspots,
            "recommendations": [
                "Optimize high-CPU functions with caching",
                "Reduce memory allocations in loop-heavy code",
                "Profile with production-like data volumes",
                "Consider async/parallel processing"
            ]
        }


if __name__ == "__main__":
    profiler = PerformanceProfiler()
    
    # Test function
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    result = profiler.profile_function(fibonacci, 10)
    
    import json
    print(json.dumps(result, indent=2))
