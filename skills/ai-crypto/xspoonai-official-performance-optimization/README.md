# Performance Optimization Guide

## Complete Performance Analysis Framework

This guide demonstrates the Performance Optimization skill for identifying and resolving performance bottlenecks in Python applications.

---

## 1. Performance Profiler

### Overview

The PerformanceProfiler measures execution time, memory usage, and CPU consumption for functions and code blocks.

### Example: Profiling a Data Processing Function

```python
from scripts.profiler import PerformanceProfiler
import time

profiler = PerformanceProfiler()

def fibonacci(n):
    """Example function for profiling."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Profile a single function
result = profiler.profile_function(fibonacci, 30)
print(f"Execution Time: {result['execution_time_ms']}ms")
print(f"Memory Used: {result['memory_used_mb']}MB")
print(f"CPU Percent: {result['cpu_percent']}%")
```

### Example: Batch Profiling

```python
functions = [
    (fibonacci, 25),
    (fibonacci, 28),
    (fibonacci, 30)
]

batch_results = profiler.batch_profile(functions)
for func_name, metrics in batch_results.items():
    print(f"{func_name}: {metrics['avg_time_ms']}ms avg")
```

### Example: Code Block Profiling

```python
code_block = """
result = []
for i in range(1000):
    for j in range(1000):
        result.append(i * j)
"""

result = profiler.profile_code_block(code_block, {})
print(f"Code Block Execution: {result['execution_time_ms']}ms")
```

### Example: Real-time Resource Monitoring

```python
# Monitor system resources for 30 seconds
samples = profiler.monitor_resource_usage(duration_seconds=30, interval=1)
for sample in samples:
    print(f"Memory: {sample['memory_mb']}MB, CPU: {sample['cpu_percent']}%")
```

### Example: Performance Comparison

```python
# Baseline (slow implementation)
def slow_sum(n):
    total = 0
    for i in range(n):
        total = total + i
    return total

# Optimized (fast implementation)
def fast_sum(n):
    return n * (n - 1) // 2

baseline = profiler.profile_function(slow_sum, 1000000)
optimized = profiler.profile_function(fast_sum, 1000000)

comparison = profiler.compare_performance(baseline, optimized)
print(f"Speedup: {comparison['speedup']}x faster")
```

### Example: Hotspot Identification

```python
# Profile multiple iterations to find hotspots
def complex_operation():
    data = [i for i in range(1000)]
    for _ in range(100):
        data.sort()
        result = [x * 2 for x in data]
    return result

profiles = [profiler.profile_function(complex_operation) for _ in range(10)]
hotspots = profiler.identify_hotspots(profiles)
print(f"Top Bottleneck: {hotspots[0]}")
```

---

## 2. Bottleneck Detector

### Overview

The BottleneckDetector identifies common performance anti-patterns and issues in code.

### Example: Detecting Code Bottlenecks

```python
from scripts.bottleneck_detector import BottleneckDetector

detector = BottleneckDetector()

# Code with nested loops (O(n²))
code = """
for i in range(1000):
    for j in range(1000):
        print(i * j)
"""

bottlenecks = detector.detect_code_bottlenecks(code)
for issue in bottlenecks:
    print(f"Issue: {issue['type']}")
    print(f"Severity: {issue['severity']}")
    print(f"Recommendation: {issue['recommendation']}")
```

### Example: Database Query Analysis

```python
queries = [
    "SELECT * FROM users WHERE id = 1; SELECT * FROM orders WHERE user_id = 1;",
    "SELECT * FROM products WHERE category = 'electronics' ORDER BY price;",
    "SELECT u.id FROM users u WHERE u.status = 'active';"
]

db_issues = detector.analyze_database_queries(queries)
for issue in db_issues:
    print(f"Query Issue: {issue['type']} - {issue['severity']}")
```

### Example: Memory Leak Detection

```python
# Simulate memory growth
memory_samples = [
    50.0, 51.2, 52.5, 54.1, 56.3, 58.7,  # Growing
    60.2, 62.1, 65.3, 68.5, 71.2, 74.8    # Significant growth
]

leak_analysis = detector.detect_memory_leaks(memory_samples)
print(f"Memory Leak Risk: {leak_analysis['risk_level']}")
print(f"Growth Rate: {leak_analysis['growth_rate_percent']}%/hour")
```

### Example: Concurrency Issue Detection

```python
concurrent_code = """
shared_variable = 0

def increment():
    global shared_variable
    shared_variable += 1

def thread_func():
    for i in range(1000000):
        increment()
"""

concurrency_issues = detector.detect_concurrency_issues(concurrent_code)
for issue in concurrency_issues:
    print(f"Concurrency Issue: {issue['type']} - {issue['severity']}")
```

### Example: I/O Pattern Analysis

```python
io_code = """
with open('file.txt', 'r') as f:
    for line in f:
        data = requests.get('http://api.example.com/data')
        process(data)
"""

io_issues = detector.analyze_io_operations(io_code)
for issue in io_issues:
    print(f"I/O Issue: {issue['type']}")
```

---

## 3. Cache Advisor

### Overview

The CacheAdvisor recommends optimal caching strategies based on access patterns.

### Example: Analyzing Cache Opportunity

```python
from scripts.cache_advisor import CacheAdvisor

advisor = CacheAdvisor()

# Access pattern: [1, 2, 3, 1, 2, 3, 1, 4, 5, 1]
# Shows high reuse of elements 1, 2, 3
access_pattern = [1, 2, 3, 1, 2, 3, 1, 4, 5, 1]

opportunity = advisor.analyze_caching_opportunity(access_pattern)
print(f"Caching Beneficial: {opportunity['is_beneficial']}")
print(f"Reuse Ratio: {opportunity['reuse_ratio']}")
```

### Example: Cache Size Recommendation

```python
memory_budget_mb = 512
access_pattern = list(range(10000)) * 2  # Each item accessed twice

sizing = advisor.recommend_cache_size(access_pattern, memory_budget_mb)
print(f"Recommended Cache Size: {sizing['cache_size_mb']}MB")
print(f"Estimated Hit Rate: {sizing['estimated_hit_rate']:.1%}")
print(f"Working Set Size: {sizing['working_set_size']} items")
```

### Example: Strategy Comparison

```python
# Access metrics
metrics = {
    "total_accesses": 100000,
    "unique_items": 5000,
    "access_frequency": "mixed",  # Some hot items
    "memory_budget_mb": 256
}

strategies = advisor.compare_strategies(metrics)
for strategy in strategies:
    print(f"Strategy: {strategy['name']} - Score: {strategy['score']}/100")
    print(f"  Pros: {', '.join(strategy['pros'])}")
    print(f"  Cons: {', '.join(strategy['cons'])}")
```

### Example: Cache Implementation Generation

```python
# Generate Python LRU cache implementation
lru_implementation = advisor.generate_cache_implementation("LRU", "python")
print(lru_implementation['code'])

# Generate JavaScript TTL cache implementation
ttl_implementation = advisor.generate_cache_implementation("TTL", "javascript")
print(ttl_implementation['code'])
```

### Example: Invalidation Strategy Analysis

```python
# Analyze cache invalidation approaches
invalidation = advisor.analyze_cache_invalidation(access_pattern)
print(f"Recommended Strategy: {invalidation['recommended_strategy']}")
print(f"TTL Duration: {invalidation['ttl_seconds']}s")
print(f"Event-Based Invalidation: {invalidation['event_based_triggers']}")
```

---

## 4. Load Tester

### Overview

The LoadTester simulates various load patterns to test system capacity and stability.

### Example: Constant Load Test

```python
from scripts.load_tester import LoadTester

tester = LoadTester()

def sample_endpoint():
    import time
    import random
    time.sleep(random.uniform(0.01, 0.05))

config = {
    "duration_seconds": 30,
    "initial_load_rps": 100,
    "pattern": "constant"
}

result = tester.run_load_test(sample_endpoint, config)
print(f"Throughput: {result['throughput_rps']} RPS")
print(f"Avg Response: {result['avg_response_time_ms']}ms")
print(f"Error Rate: {result['error_rate']:.2%}")
```

### Example: Ramp-Up Load Test

```python
config = {
    "duration_seconds": 60,
    "initial_load_rps": 10,
    "pattern": "ramp",
    "max_load_rps": 1000
}

result = tester.run_load_test(sample_endpoint, config)
print(f"Max Sustainable Load: {result['max_load_rps']} RPS")
print(f"P95 Latency: {result['p95_response_time_ms']}ms")
print(f"P99 Latency: {result['p99_response_time_ms']}ms")
```

### Example: Stress Testing

```python
config = {
    "initial_load_rps": 50,
    "max_load_rps": 5000,
    "step_rps": 100,
    "duration_per_step": 30
}

stress_result = tester.stress_test(sample_endpoint, config)
print(f"Breaking Point: {stress_result['breakpoint_rps']} RPS")
print(f"Max Sustainable: {stress_result['max_sustainable_load']} RPS")
```

### Example: Soak Testing

```python
config_soak = {
    "load_rps": 100,
    "duration_hours": 2
}

soak_result = tester.soak_test(sample_endpoint, 100, 2)
print(f"Stability: {soak_result['stability']}")
print(f"Performance Trend: {soak_result['performance_trend']}")
print(f"Total Errors: {soak_result['total_errors']}")
```

### Example: Chaos Testing

```python
chaos_config = {
    "duration_seconds": 60,
    "failure_rate": 0.05,  # 5% of requests fail
    "latency_range_ms": [100, 500]  # 100-500ms latency injection
}

chaos_result = tester.chaos_test(sample_endpoint, chaos_config)
print(f"Resilience Score: {chaos_result['resilience_score']:.1f}%")
for recommendation in chaos_result['recommendations']:
    print(f"  - {recommendation}")
```

### Example: Load Test Report

```python
results = [
    {"load_rps": 100, "requests": 3000, "errors": 5, "avg_time_ms": 12.5},
    {"load_rps": 200, "requests": 6000, "errors": 15, "avg_time_ms": 18.2},
    {"load_rps": 500, "requests": 15000, "errors": 150, "avg_time_ms": 45.7}
]

report = tester.generate_load_test_report(results)
print(report)
```

---

## Integration Examples

### Complete Performance Analysis Workflow

```python
from scripts.profiler import PerformanceProfiler
from scripts.bottleneck_detector import BottleneckDetector
from scripts.cache_advisor import CacheAdvisor
from scripts.load_tester import LoadTester

# 1. Profile the current implementation
profiler = PerformanceProfiler()
baseline = profiler.profile_function(my_function, large_dataset)

# 2. Detect bottlenecks in the code
detector = BottleneckDetector()
issues = detector.detect_code_bottlenecks(code_string)

# 3. Recommend caching if beneficial
advisor = CacheAdvisor()
cache_rec = advisor.analyze_caching_opportunity(access_pattern)

# 4. Test under load
tester = LoadTester()
load_result = tester.run_load_test(my_endpoint, load_config)

# 5. Report findings
print(f"Baseline Performance: {baseline['execution_time_ms']}ms")
print(f"Bottlenecks Found: {len(issues)}")
print(f"Caching Recommended: {cache_rec['is_beneficial']}")
print(f"Load Test Result: {load_result['status']}")
```

---

## Performance Best Practices

### 1. Profiling
- **Always profile before optimizing** - measure, don't guess
- **Use realistic data** - small samples can hide performance issues
- **Profile multiple runs** - account for system variance

### 2. Bottleneck Detection
- **Regular code reviews** - catch patterns early
- **Focus on hot paths** - optimize where it matters most
- **Test after changes** - ensure optimization worked

### 3. Caching Strategy
- **Measure hit rates** - determine if cache is effective
- **Choose appropriate TTL** - balance freshness vs. performance
- **Monitor cache size** - avoid memory exhaustion

### 4. Load Testing
- **Test realistic scenarios** - spike, ramp, and sustained loads
- **Use chaos testing** - find weak points
- **Monitor over time** - detect performance degradation

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| High memory usage in profiler | Reduce batch size or monitoring duration |
| Missed bottlenecks in static analysis | Combine with runtime profiling |
| Cache hit rate too low | Increase cache size or adjust TTL |
| System crashes under load | Implement backpressure and rate limiting |

---

## Summary

The Performance Optimization skill provides complete visibility into application performance:

- **Profiler**: Measure what matters (time, memory, CPU)
- **Bottleneck Detector**: Find performance anti-patterns
- **Cache Advisor**: Recommend optimal caching strategies
- **Load Tester**: Test capacity and resilience

Use these tools to systematically improve application performance.
