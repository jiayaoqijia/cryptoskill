#!/usr/bin/env python3
"""
Load Tester
Simulates load and performance testing
"""

import time
import random
from typing import Dict, List, Any, Callable
from dataclasses import dataclass
from enum import Enum

class LoadPattern(Enum):
    """Load test patterns."""
    CONSTANT = "constant"
    RAMP = "ramp"
    SPIKE = "spike"
    WAVE = "wave"

@dataclass
class LoadTestResult:
    """Load test result."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_response_time_ms: float
    min_response_time_ms: float
    max_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    throughput_rps: float
    error_rate: float

class LoadTester:
    """Simulates load testing scenarios."""

    def __init__(self):
        self.results = []

    def run_load_test(self, endpoint_func: Callable, config: Dict) -> Dict[str, Any]:
        """Run a load test."""
        
        duration = config.get("duration_seconds", 60)
        initial_load = config.get("initial_load_rps", 10)
        pattern = config.get("pattern", "constant")
        
        responses = []
        errors = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Calculate current load based on pattern
            current_load = self._calculate_load(pattern, elapsed, duration, initial_load, config)
            
            # Simulate requests for this second
            for _ in range(int(current_load)):
                try:
                    req_start = time.time()
                    endpoint_func()
                    req_time = (time.time() - req_start) * 1000
                    responses.append(req_time)
                except Exception as e:
                    errors.append(str(e))
            
            time.sleep(1)
        
        # Analyze results
        return self._analyze_results(responses, errors, start_time, duration)

    def stress_test(self, endpoint_func: Callable, config: Dict) -> Dict[str, Any]:
        """Run stress test - gradually increase load until failure."""
        
        initial_load = config.get("initial_load_rps", 10)
        max_load = config.get("max_load_rps", 1000)
        step = config.get("step_rps", 10)
        duration_per_step = config.get("duration_per_step", 30)
        
        current_load = initial_load
        results = []
        breakpoint = None
        
        while current_load <= max_load:
            print(f"Testing at {current_load} RPS...")
            
            responses = []
            errors = []
            start_time = time.time()
            
            while time.time() - start_time < duration_per_step:
                for _ in range(int(current_load)):
                    try:
                        req_start = time.time()
                        endpoint_func()
                        responses.append((time.time() - req_start) * 1000)
                    except Exception as e:
                        errors.append(str(e))
                
                time.sleep(0.1)
            
            # Check for failure
            error_rate = len(errors) / (len(responses) + len(errors)) if (responses or errors) else 0
            
            if error_rate > 0.05:  # 5% error rate threshold
                breakpoint = current_load
                break
            
            result = {
                "load_rps": current_load,
                "requests": len(responses),
                "errors": len(errors),
                "error_rate": error_rate,
                "avg_time_ms": sum(responses) / len(responses) if responses else 0
            }
            results.append(result)
            
            current_load += step
        
        return {
            "results": results,
            "breakpoint_rps": breakpoint,
            "max_sustainable_load": results[-1]["load_rps"] if results else initial_load,
            "recommendation": f"System can handle {results[-1]['load_rps'] if results else initial_load} RPS"
        }

    def soak_test(self, endpoint_func: Callable, load_rps: int, duration_hours: int) -> Dict[str, Any]:
        """Run soak test - sustained load over long period."""
        
        duration_seconds = duration_hours * 3600
        sample_interval = 300  # Sample every 5 minutes
        
        samples = []
        errors = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            sample_responses = []
            sample_start = time.time()
            
            # Run for sample interval
            while time.time() - sample_start < sample_interval:
                for _ in range(load_rps):
                    try:
                        req_start = time.time()
                        endpoint_func()
                        sample_responses.append((time.time() - req_start) * 1000)
                    except Exception as e:
                        errors.append(str(e))
                
                time.sleep(0.1)
            
            # Record sample
            avg_time = sum(sample_responses) / len(sample_responses) if sample_responses else 0
            samples.append({
                "elapsed_seconds": time.time() - start_time,
                "avg_response_ms": avg_time,
                "requests": len(sample_responses),
                "errors": len(errors)
            })
        
        # Detect memory leaks or degradation
        trend = self._analyze_trend(samples)
        
        return {
            "duration_hours": duration_hours,
            "load_rps": load_rps,
            "samples": samples,
            "total_errors": len(errors),
            "performance_trend": trend,
            "stability": "STABLE" if trend == "FLAT" else "DEGRADING"
        }

    def chaos_test(self, endpoint_func: Callable, config: Dict) -> Dict[str, Any]:
        """Run chaos test - random failures and latency injection."""
        
        duration = config.get("duration_seconds", 60)
        failure_rate = config.get("failure_rate", 0.05)  # 5%
        latency_range = config.get("latency_range_ms", [0, 100])
        
        responses = []
        errors = []
        injected_failures = 0
        injected_latencies = 0
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # Randomly inject failure
                if random.random() < failure_rate:
                    injected_failures += 1
                    raise Exception("Chaos - injected failure")
                
                # Randomly inject latency
                injected_latency = 0
                if random.random() < 0.1:
                    injected_latency = random.uniform(*latency_range)
                    injected_latencies += 1
                    time.sleep(injected_latency / 1000)
                
                req_start = time.time()
                endpoint_func()
                responses.append((time.time() - req_start) * 1000 + injected_latency)
            except Exception as e:
                errors.append(str(e))
            
            time.sleep(0.01)
        
        return {
            "duration_seconds": duration,
            "total_requests": len(responses) + len(errors),
            "successful": len(responses),
            "failed": len(errors),
            "resilience_score": (len(responses) / (len(responses) + len(errors))) * 100 if (responses or errors) else 0,
            "injected_failures": injected_failures,
            "injected_latencies": injected_latencies,
            "recommendations": self._get_chaos_recommendations(len(errors), len(responses))
        }

    def generate_load_test_report(self, results: List[Dict]) -> str:
        """Generate load test report."""
        
        report = "# Load Test Report\n\n"
        report += f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "## Summary\n"
        report += f"- Total Requests: {sum(r.get('requests', 0) for r in results)}\n"
        report += f"- Total Errors: {sum(r.get('errors', 0) for r in results)}\n"
        report += f"- Average Response Time: {sum(r.get('avg_time_ms', 0) for r in results) / len(results):.2f}ms\n\n"
        
        report += "## Results by Load Level\n"
        report += "| Load (RPS) | Requests | Errors | Avg Time (ms) | Error Rate |\n"
        report += "|-----------|----------|--------|---------------|------------|\n"
        
        for result in results:
            error_rate = (result.get('errors', 0) / (result.get('requests', 0) + result.get('errors', 0)) * 100) if (result.get('requests', 0) + result.get('errors', 0)) > 0 else 0
            report += f"| {result.get('load_rps', 0):<9} | {result.get('requests', 0):<8} | {result.get('errors', 0):<6} | {result.get('avg_time_ms', 0):<13.2f} | {error_rate:<10.1f}% |\n"
        
        return report

    # ===== Private Methods =====

    def _calculate_load(self, pattern: str, elapsed: float, duration: float, base_load: int, config: Dict) -> int:
        """Calculate current load based on pattern."""
        
        if pattern == "constant":
            return base_load
        
        elif pattern == "ramp":
            max_load = config.get("max_load_rps", base_load * 10)
            progress = elapsed / duration
            return int(base_load + (max_load - base_load) * progress)
        
        elif pattern == "spike":
            spike_time = config.get("spike_time_seconds", duration / 2)
            spike_load = config.get("spike_load_rps", base_load * 5)
            if abs(elapsed - spike_time) < 5:
                return spike_load
            return base_load
        
        elif pattern == "wave":
            wave_duration = config.get("wave_duration_seconds", 10)
            progress = (elapsed % wave_duration) / wave_duration
            max_load = config.get("max_load_rps", base_load * 5)
            return int(base_load + (max_load - base_load) * abs(0.5 - progress) * 2)
        
        return base_load

    def _analyze_results(self, responses: List[float], errors: List[str], start_time: float, duration: float) -> Dict[str, Any]:
        """Analyze test results."""
        
        total = len(responses) + len(errors)
        error_rate = len(errors) / total if total > 0 else 0
        
        if responses:
            responses.sort()
            avg = sum(responses) / len(responses)
            min_time = responses[0]
            max_time = responses[-1]
            p95 = responses[int(len(responses) * 0.95)]
            p99 = responses[int(len(responses) * 0.99)]
        else:
            avg = min_time = max_time = p95 = p99 = 0
        
        elapsed = time.time() - start_time
        throughput = total / elapsed if elapsed > 0 else 0
        
        return {
            "total_requests": total,
            "successful_requests": len(responses),
            "failed_requests": len(errors),
            "error_rate": round(error_rate, 4),
            "avg_response_time_ms": round(avg, 2),
            "min_response_time_ms": round(min_time, 2),
            "max_response_time_ms": round(max_time, 2),
            "p95_response_time_ms": round(p95, 2),
            "p99_response_time_ms": round(p99, 2),
            "throughput_rps": round(throughput, 2),
            "status": "PASS" if error_rate < 0.01 else "FAIL"
        }

    def _analyze_trend(self, samples: List[Dict]) -> str:
        """Analyze trend in samples."""
        
        if len(samples) < 2:
            return "UNKNOWN"
        
        avg_times = [s.get("avg_response_ms", 0) for s in samples]
        
        increases = sum(1 for i in range(len(avg_times) - 1) if avg_times[i+1] > avg_times[i])
        increase_ratio = increases / (len(avg_times) - 1)
        
        if increase_ratio > 0.7:
            return "DEGRADING"
        elif increase_ratio < 0.3:
            return "IMPROVING"
        else:
            return "FLAT"

    def _get_chaos_recommendations(self, errors: int, successes: int) -> List[str]:
        """Get recommendations based on chaos test results."""
        
        if errors == 0:
            return ["Excellent resilience - system handles all chaos scenarios"]
        
        resilience = successes / (successes + errors) if (successes + errors) > 0 else 0
        
        if resilience < 0.5:
            return [
                "Low resilience - implement circuit breakers",
                "Add retry logic with exponential backoff",
                "Implement timeout mechanisms"
            ]
        elif resilience < 0.95:
            return [
                "Good resilience - consider improving error handling",
                "Add monitoring and alerting",
                "Implement graceful degradation"
            ]
        else:
            return ["Excellent resilience - good error handling in place"]


if __name__ == "__main__":
    tester = LoadTester()
    
    def dummy_endpoint():
        time.sleep(random.uniform(0.01, 0.1))
    
    config = {
        "duration_seconds": 10,
        "initial_load_rps": 5,
        "pattern": "ramp",
        "max_load_rps": 50
    }
    
    result = tester.run_load_test(dummy_endpoint, config)
    
    import json
    print(json.dumps(result, indent=2))
