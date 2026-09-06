# skill-example-runner (Track: platform-challenge)

Execute and validate skill examples with comprehensive reporting

## Overview

This skill discovers, extracts, executes, and validates examples from skill implementations. It runs sample commands from skill documentation, captures output, validates JSON format compliance, measures execution time, and generates comprehensive reports.

## Features

- **Example Discovery**: Find and extract executable examples from skill documentation
- **Example Execution**: Run skill examples with subprocess and capture output
- **Format Validation**: Validate that output complies with expected JSON format and has required fields
- **Performance Metrics**: Capture execution time for each example in milliseconds
- **Error Reporting**: Track execution errors, exit codes, and provide detailed error messages
- **Success Tracking**: Calculate execution success rates per skill and overall
- **Output Limits**: Safely truncate large outputs to prevent memory issues
- **Comprehensive Reporting**: Generate detailed reports with metrics for all executed examples

## Usage

Execute skill examples and validate their outputs:

```bash
# Demo mode - execute examples from 3 sample skills
python3 scripts/main.py --demo

# Analyze specific skill examples
python3 scripts/main.py --skill security-deps-audit

# Custom execution with parameters
python3 scripts/main.py --params '{"action": "analyze", "skills": ["skill-name"]}'
```

## Use Cases

- Verify skill functionality by executing examples
- Validate skill output compliance with JSON standards
- Generate execution reports for quality assurance
- Performance testing of skill examples
- Documentation validation (examples must execute successfully)

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action | string | No | Action to perform: "analyze" (default) |
| skill | string | No | Specific skill to analyze examples for |
| skills | array | No | List of specific skills to analyze |

## Example Output

Running demo mode executes examples from 3 skills (api-webhook-signer, security-deps-audit, skill-ci-checklist) with:
- Total examples: 6
- Successfully executed: 4
- Failed: 2
- Success rate: 66.7%

Key metrics per example:
- **execution_time_ms**: Time taken to execute the example
- **exit_code**: Exit code returned by the skill process
- **output_validation**: JSON format validation results
- **output**: First 500 chars of skill output
- **error**: Error message if execution failed
