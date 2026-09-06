# test-suggestions (Track: enterprise-skills)

Automatically suggest test cases and improve test coverage

## Overview

This skill analyzes source code and suggests comprehensive test cases for functions and modules. It identifies untested code paths and recommends test scenarios to improve coverage and reliability.

## Features

- **AST-Based Analysis**: Parse code structure to identify functions
- **Test Case Suggestions**: Generate relevant test scenarios
- **Edge Case Detection**: Suggest boundary and edge case tests
- **Coverage Improvement**: Identify gaps in test coverage
- **Multi-Language Support**: Python, JavaScript, and more

## Use Cases

- Improve test coverage systematically
- Generate test case ideas for developers
- Identify untested code paths
- Standardize test scenarios across project
- Train developers on testing best practices

## Quickstart
```bash
python3 scripts/main.py --help
```

## Example
```bash
python3 scripts/main.py --demo
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| code | string | Yes | Source code to analyze |
| language | string | No | Programming language (python, javascript) - default: python |

## Example Output

```json
{
  "ok": true,
  "data": {
    "demo": true,
    "timestamp": "2026-02-07T09:08:04",
    "language": "python",
    "file_analysis": {
      "functions": [
        {
          "signature": {
            "name": "fetch_user_data",
            "parameters": [{"name": "user_id"}, {"name": "timeout"}],
            "has_docstring": true
          },
          "edge_cases": [
            {
              "category": "empty_input",
              "test_name": "test_fetch_user_data_with_empty_input",
              "priority": "high",
              "test_cases": ["assert fetch_user_data(None) handles None", "assert fetch_user_data([]) works with empty list"]
            },
            {
              "category": "boundary_values",
              "test_name": "test_fetch_user_data_boundary_values",
              "priority": "high",
              "test_cases": ["assert fetch_user_data(0) is handled", "assert fetch_user_data(-1) is handled"]
            },
            {
              "category": "type_errors",
              "test_name": "test_fetch_user_data_type_errors",
              "priority": "high",
              "test_cases": ["with pytest.raises(TypeError): fetch_user_data('string_when_int_expected')"]
            }
          ],
          "fixtures": [
            {
              "name": "fetch_user_data_test_data",
              "scope": "function",
              "description": "Valid test data for fetch_user_data"
            }
          ]
        },
        {
          "signature": {
            "name": "calculate_total",
            "parameters": [{"name": "items"}, {"name": "tax_rate"}],
            "has_docstring": true
          }
        }
      ]
    },
    "summary": {
      "total_functions": 3,
      "functions_needing_tests": 3,
      "estimated_test_cases": 18
    }
  }
}
```
