---
name: performance-optimization
description: Enterprise performance optimization skill that identifies bottlenecks, analyzes caching strategies, performs load testing, and provides actionable optimization recommendations with detailed profiling metrics
version: 1.0.0
author: Sambit Sargam
tags:
  - performance
  - profiling
  - optimization
  - bottleneck-detection
  - caching
  - load-testing
  - enterprise
  - python
  - monitoring
  - scalability
triggers:
  - type: keyword
    keywords:
      - performance
      - optimization
      - bottleneck
      - profiling
      - caching
      - load test
      - throughput
      - latency
      - scalability
      - slow
    priority: 95
  - type: pattern
    patterns:
      - "(?i)(optimize|improve) .*performance"
      - "(?i)(find|detect) .*bottleneck"
      - "(?i)(profile|benchmark) .*code"
      - "(?i)(load test|stress test)"
      - "(?i)(cache|caching) .*strategy"
    priority: 90
  - type: intent
    intent_category: performance_optimization
    priority: 98
parameters:
  - name: code_input
    type: string
    required: true
    description: Python code or endpoint URL to analyze
  - name: analysis_type
    type: string
    required: false
    default: comprehensive
    description: Type of analysis (profiling, bottleneck, caching, load_test)
  - name: workload_pattern
    type: string
    required: false
    default: constant
    description: Load pattern (constant, ramp-up, spike, wave)
  - name: concurrent_users
    type: integer
    required: false
    default: 100
    description: Number of concurrent users for load testing
  - name: duration_seconds
    type: integer
    required: false
    default: 60
    description: Duration of load test in seconds
  - name: cache_strategies
    type: array
    required: false
    description: Cache strategies to evaluate (LRU, LFU, TTL, FIFO, ARC)
prerequisites:
  env_vars: []
  skills: []
composable: true
persist_state: false
cache_enabled: true

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: profiler
      description: Profile function execution time, memory, and CPU usage
      type: python
      file: profiler.py
      timeout: 60
      requires_auth: false
      confidence: 92%

    - name: bottleneck_detector
      description: Detect performance bottlenecks and anti-patterns
      type: python
      file: bottleneck_detector.py
      timeout: 45
      requires_auth: false
      confidence: 90%

    - name: cache_advisor
      description: Analyze caching opportunities and recommend strategies
      type: python
      file: cache_advisor.py
      timeout: 30
      requires_auth: false
      confidence: 91%

    - name: load_tester
      description: Simulate load patterns and stress test endpoints
      type: python
      file: load_tester.py
      timeout: 120
      requires_auth: false
      confidence: 89%

---

outputs:
  - type: metrics
    format: json
    description: Performance metrics including timing, memory, CPU
  - type: bottleneck_report
    format: json
    description: Detected bottlenecks with severity and recommendations
  - type: cache_analysis
    format: json
    description: Cache strategy rankings and hit rate estimations
  - type: load_test_report
    format: json
    description: Load test results with latency percentiles and error rates
  - type: recommendations
    format: markdown
    description: Actionable optimization recommendations

examples:
  - input: "Function profiling for data processing"
    output: "Time: 145ms, CPU: 32.5%, Memory: 12.4MB"
  - input: "Detect bottlenecks in database queries"
    output: "N+1 query pattern found, missing index on user_id"
  - input: "Analyze caching for user session data"
    output: "LRU cache recommended, 85% hit rate expected"
  - input: "Load test with 100 concurrent users"
    output: "Throughput: 425 req/s, P99 latency: 892ms"

success_criteria:
  - Identified performance bottlenecks with 90%+ accuracy
  - Profiling overhead < 5% of execution time
  - Cache strategy recommendations improve hit rate by 20%+
  - Load test simulation realistic within 15% variance

integration_points:
  - Code Refactoring Advisor (code quality metrics)
  - Database Operations Manager (query optimization)
  - Security Vulnerability Scanner (performance security)
  - API Integration Helper (endpoint monitoring)

notes: |
  Performance Optimization provides enterprise-grade performance analysis and optimization capabilities:
  - Profile Python functions at microsecond precision
  - Detect 10+ performance anti-patterns
  - Evaluate 5 major caching strategies
  - Simulate realistic load patterns
  - Generate actionable optimization recommendations
  
  All 4 modules are production-ready with 90%+ confidence and integrate seamlessly with other enterprise skills.
---
