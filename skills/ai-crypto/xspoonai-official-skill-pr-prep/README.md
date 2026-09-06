# skill-pr-prep (Track: platform-challenge)

Validate skills before pull request submission

## Overview

This skill validates that skills meet all requirements for PR submission. It checks file structure, YAML frontmatter, code quality, and functionality before allowing merge.

## Features

- **File Structure Validation**: Verify all required files exist (SKILL.md, README.md, pull.md, scripts/main.py)
- **YAML Frontmatter Check**: Validate SKILL.md contains required metadata fields
- **Python Script Validation**: Check for required flags (--demo, --params) and JSON output
- **Code Quality**: Verify shebang, proper imports, and error handling
- **Pre-Merge Checks**: Comprehensive validation before repository acceptance
- **Detailed Reports**: Itemized feedback on what needs to be fixed
- **Automated Linting**: Consistent quality standard enforcement

## Usage

Validate skill readiness for PR submission:

```bash
# Run validation checks
python3 scripts/main.py --demo

# Validate specific skill
python3 scripts/main.py --params '{"skill_path": "../skill-name"}'
```

## Use Cases

- Pre-submission validation for skill authors
- Automated CI/CD quality gates for pull requests
- Consistent quality standards across repository
- Catch common issues before review
- Streamline skill acceptance process

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skill_path | string | No | Path to skill directory to validate |

## Example Output

Validation of sample skill showing all checks passed: file structure complete, SKILL.md valid with all required fields, main.py has --demo, --params, JSON output, ok field, and proper shebang. Ready for PR submission.
