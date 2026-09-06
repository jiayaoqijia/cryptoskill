---
name: code-refactoring-advisor
description: Enterprise code refactoring advisor that detects code smells, anti-patterns, and complexity issues with specific refactoring recommendations, test generation, and maintainability metrics
version: 1.0.0
author: Sambit Sargam
tags:
  - refactoring
  - code-quality
  - code-smells
  - complexity-analysis
  - python
  - solidity
  - enterprise
  - static-analysis
  - testing
triggers:
  - type: keyword
    keywords:
      - refactor
      - code quality
      - code smell
      - complexity
      - maintainability
      - pattern
      - technical debt
      - clean code
      - best practices
      - code review
    priority: 95
  - type: pattern
    patterns:
      - "(?i)(refactor|improve|optimize) .*code"
      - "(?i)(analyze|detect|find) .*code .*smell"
      - "(?i)(reduce|lower) .*(complexity|cyclomatic)"
      - "(?i)(what|generate) .*test.*case"
      - "(?i)(code quality|maintainability) .*score"
    priority: 90
  - type: intent
    intent_category: code_refactoring
    priority: 98
parameters:
  - name: code_input
    type: string
    required: true
    description: Source code to analyze (Python or Solidity)
  - name: language
    type: string
    required: false
    default: python
    description: Programming language (python, solidity, typescript)
  - name: analysis_type
    type: string
    required: false
    default: comprehensive
    description: Type of analysis (smells, complexity, refactoring, testing)
  - name: severity_threshold
    type: string
    required: false
    default: MEDIUM
    description: Minimum severity to report (CRITICAL, HIGH, MEDIUM, LOW)
  - name: include_test_generation
    type: boolean
    required: false
    default: true
    description: Generate test cases for refactored code
  - name: focus_areas
    type: array
    required: false
    description: Specific areas to focus on (patterns, complexity, security, maintainability)
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
    - name: pattern_detector
      description: Detect code smells and anti-patterns
      type: python
      file: pattern_detector.py
      timeout: 30
      requires_auth: false
      confidence: 92%

    - name: refactoring_suggester
      description: Generate specific refactoring recommendations
      type: python
      file: refactoring_suggester.py
      timeout: 30
      requires_auth: false
      confidence: 88%

    - name: complexity_analyzer
      description: Calculate cyclomatic complexity and maintainability metrics
      type: python
      file: complexity_analyzer.py
      timeout: 30
      requires_auth: false
      confidence: 90%

    - name: test_generator
      description: Generate unit and integration test cases
      type: python
      file: test_generator.py
      timeout: 30
      requires_auth: false
      confidence: 85%
---
capabilities:
  - python code smell detection (god functions, long parameters, deep nesting, etc.)
  - solidity smart contract anti-patterns (reentrancy, unchecked arithmetic, etc.)
  - cyclomatic complexity calculation per function
  - maintainability index scoring (0-100)
  - specific refactoring recommendations with code examples
  - automatic unit test generation
  - security pattern detection
  - test strategy planning
  - code quality metrics and reporting

security_considerations:
  - Read-only code analysis (no code execution)
  - No external file access
  - Pattern-based detection only
  - Safe AST parsing with error handling
  - No sensitive data exposure
  - No code modification without user confirmation
  - Sandbox analysis environment

## Overview

The **Code Refactoring Advisor** is an enterprise-grade code quality tool that analyzes Python and Solidity code to detect smells, anti-patterns, and complexity issues with actionable refactoring recommendations. It combines pattern detection, complexity metrics, and test generation to improve code quality systematically.

Key capabilities:
- **Code Smell Detection**: 12+ patterns (god functions, long parameters, deep nesting, etc.)
- **Complexity Analysis**: Cyclomatic complexity and maintainability index calculation
- **Refactoring Recommendations**: Specific solutions with code examples and effort estimates
- **Test Generation**: Automatic unit and integration test case generation
- **Security Patterns**: Solidity vulnerability detection (reentrancy, arithmetic, etc.)

## Module Details

### Module 1: Pattern Detector (92% Confidence)
Detects code smells and anti-patterns in Python and Solidity:
- **Python**: God functions, long parameter lists, deep nesting, bare excepts, global variables, magic numbers
- **Solidity**: Reentrancy vulnerabilities, unbounded loops, unchecked arithmetic, unclear visibility
- Outputs: Severity levels (CRITICAL/HIGH/MEDIUM/LOW), confidence scores, line numbers

### Module 2: Refactoring Suggester (88% Confidence)
Generates specific refactoring solutions:
- Pattern-based recommendations (extract method, parameter object, strategy pattern, etc.)
- Effort estimates (TRIVIAL to LARGE)
- Benefits per refactoring (testability, maintainability, security, etc.)
- Code examples showing before/after

### Module 3: Complexity Analyzer (90% Confidence)
Calculates code metrics:
- Cyclomatic complexity per function
- Maintainability Index (0-100)
- Code statistics (lines, comments, ratio)
- Health scoring and improvement recommendations

### Module 4: Test Generator (85% Confidence)
Creates test cases for refactored code:
- Unit tests (extracted methods, parameters, guards)
- Integration tests (combined functionality)
- Security tests (reentrancy, edge cases)
- Test templates and strategies

## Usage Examples

### Detect Code Smells
```python
from scripts.pattern_detector import PatternDetector

detector = PatternDetector()
result = detector.analyze_code(source_code, language="python")
print(f"Smells found: {result['smells_detected']}")
print(f"Code quality: {result['code_quality']}%")
```

### Get Refactoring Recommendations
```python
from scripts.refactoring_suggester import RefactoringSuggester

suggester = RefactoringSuggester()
suggestions = suggester.suggest_refactoring(smell_data)
for suggestion in suggestions['suggestions']:
    print(f"{suggestion['smell_type']}: {suggestion['solutions']}")
```

### Analyze Complexity
```python
from scripts.complexity_analyzer import ComplexityAnalyzer

analyzer = ComplexityAnalyzer()
metrics = analyzer.analyze_module(source_code)
print(f"Maintainability: {metrics['maintainability_index']['rating']}")
```

### Generate Tests
```python
from scripts.test_generator import TestGenerator

generator = TestGenerator()
tests = generator.generate_tests(refactoring_suggestions)
for test in tests['test_cases']:
    print(f"Test: {test['name']}")
```

## Output Format

All modules return structured JSON:

```json
{
  "analysis_type": "string",
  "smells_detected": number,
  "code_quality_score": 0-100,
  "severity_breakdown": { "CRITICAL": n, "HIGH": n, ... },
  "refactoring_opportunities": number,
  "estimated_effort": "string",
  "estimated_quality_improvement": number,
  "test_cases_generated": number,
  "recommendations": ["array of actionable items"],
  "metrics": { "complexity": number, "maintainability": number, ... }
}
```

## Severity Levels

| Level | Meaning | Impact | Action |
|-------|---------|--------|--------|
| CRITICAL | Major security/correctness issue | High risk | Fix immediately |
| HIGH | Significant code quality issue | Moderate risk | Fix in this sprint |
| MEDIUM | Maintainability concern | Low-moderate risk | Plan refactoring |
| LOW | Minor improvement opportunity | Low risk | Consider for future |

## Version & Support

- **Version**: 1.0.0
- **Released**: February 8, 2026
- **Status**: Production Ready
- **Confidence**: 90%

## Future Enhancements (v1.1.0)

- TypeScript and JavaScript support
- Machine learning-based pattern detection
- Historical complexity tracking
- Custom rule engine
- IDE plugin integration
- Automated refactoring execution
- Performance profiling integration
