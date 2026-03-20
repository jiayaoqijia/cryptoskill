# Contributing to QELT RWA Oracle Skill

This skill wraps the QXMP Oracle REST API. Determine where the problem lies before reporting issues.

## Issue Reporting Guide

### Open an issue in this repository if

- The skill documentation is unclear or missing
- Examples in SKILL.md do not work as described
- The asset code format or response shape has changed
- The skill is missing an endpoint or use-case

### Open an issue at the QXMP team if

- The Oracle API is down or returning unexpected errors
- Proof freshness values appear incorrect
- Asset valuations seem inconsistent with published data

## Before Opening an Issue

1. Test the API call directly in your terminal:
   ```bash
   curl -fsSL "https://api.qxmp.ai/api/v1/rwa/health"
   ```

2. Check if the oracle proof is within its 24-hour update window.

## Issue Report Template

```markdown
### Description
[Provide a clear and concise description of the problem]

### Reproduction Steps
1. [First Step]
2. [Second Step]
3. [Observe error]

### Expected Behavior
[Describe what you expected to happen]

### Environment Details
- **Skill Version:** [from _meta.json]
- **Asset Code:** [e.g. QXMP:RHENO-JORC-ZA]
- **curl Version:** [output of curl --version]
- **Operating System:** [e.g. macOS, Ubuntu 22.04]

### Additional Context
- [Full API response or error output]
- [Proof timestamp if relevant]
```

## Adding New Assets or Endpoints

Update SKILL.md when new assets or API endpoints are added to the QXMP Oracle.
- Keep the asset types and jurisdictions table accurate
- Add new endpoints in the correct category with working curl examples
