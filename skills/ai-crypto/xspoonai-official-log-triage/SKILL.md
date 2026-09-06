---
name: log-triage
description: CI/build/runtime error log analysis with root-cause detection, prioritized fix plans, and verification checklists
version: 1.0.0
author: ETHPanda
tags:
  - debugging
  - ci
  - error-analysis
  - troubleshooting
  - logs
  - devops
  - testing
triggers:
  - type: keyword
    keywords:
      - error
      - failed
      - debug
      - ci failure
      - build failed
      - log analysis
      - troubleshoot
      - crash
      - exception
    priority: 85
  - type: pattern
    patterns:
      - "(?i)(analyze|check|debug|fix) .*(error|failure|log|crash)"
      - "(?i)(ci|build|test) .*(failed|error|broken)"
      - "(?i)(what|why) .*(failed|error|broke)"
    priority: 80
  - type: intent
    intent_category: debugging_logs
    priority: 90
parameters:
  - name: log_file
    type: string
    required: false
    description: Path to log file or raw log text
  - name: command
    type: string
    required: false
    description: Command that was running when error occurred
  - name: environment
    type: string
    required: false
    description: Environment details (OS, versions, CI provider)
prerequisites:
  env_vars: []
  skills: []
composable: true
persist_state: false

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: log_triage
      description: Analyze error logs and generate fix plan
      type: python
      file: log_triage.py
      timeout: 30
---

# Skill: Log Triage & Fix Plan (Enterprise Debugging)

**Source:** ETHPanda  
**Track:** Enterprise & Team Skills → Debugging  
**Goal:** Turn raw error logs into (1) root-cause hypotheses, (2) reproducible steps, (3) prioritized fix plan, (4) verification checklist.

## When to use

Use this skill when you have:
- CI failure logs (GitHub Actions, GitLab CI, Jenkins, etc.)
- Runtime crashes, stack traces, uncaught exceptions
- Build failures (TypeScript, Python, Rust, Go, Java, Solidity/Hardhat)
- Dependency / environment / permission / network issues

## Required inputs (ask user to provide)

1. The error log (full text preferred)
2. What command was running (e.g. `pnpm test`, `hardhat test`, `pytest`, `cargo test`)
3. Environment (OS, Node/Python/Rust versions, CI provider if any)
4. Recent changes (commit, dependency bumps, config edits) if known

## Output format (must follow)

1. **1-paragraph summary** of what failed and where
2. **Error signature(s)** (key lines you matched)
3. **Root-cause candidates** (ranked, with confidence and reasoning)
4. **Fix plan** (ranked, each step includes exact commands or code areas to check)
5. **Verification checklist** (how to confirm the fix)
6. **If blocked:** minimal questions to unblock (max 3)

## Triage procedure

1. Extract the *first* fatal error (often earlier than the last line)
2. Classify into categories:
   - Syntax/type errors
   - Missing dependency / wrong version
   - Build toolchain mismatch
   - Env var / secret missing
   - Permission / path / file system
   - Network / rate limit / RPC issues
   - Test flakiness / timing
3. Match known patterns (e.g. "Cannot find module", "TypeError", "revert", "out of gas", "403/429", etc.)
4. Propose minimal reproduction locally
5. Provide safest fix first (pin version / clean install / config correction) before invasive refactors

## Constraints

- Don't hallucinate files that don't exist; when unsure, say "check whether X exists".
- Prefer reversible changes (lockfile pin, config tweak) over broad refactors.
- Always include a verification step (rerun exact command / CI workflow).

## Available Scripts

### log_triage.py

Analyzes error logs using pattern matching and generates a structured Markdown report.

**Usage:**
```bash
python scripts/log_triage.py --file <log_file> --format md
```

**Input:**
- `--file`: Path to log file
- `--format`: Output format (md or txt)

**Output:**
- Matched error signatures
- Prioritized fix plan
- Verification checklist

## Supported Error Patterns

| Category | Pattern | Fix Strategy |
|----------|---------|--------------|
| Node Missing Module | `Cannot find module 'X'` | Clean install, check lockfile |
| TypeScript Errors | `TS\d+:` | Fix types, check TS version |
| Python Module Not Found | `ModuleNotFoundError: No module named 'X'` | Check requirements, reinstall venv |
| Hardhat Errors | `HardhatError\|HH\d+:` | Check compiler version, clear cache |
| Revert Reasons | `reverted with reason string 'X'` | Trace contract logic, check inputs |
| Rate Limits | `429\|rate limit` | Add retries, reduce concurrency |

## Example Usage

### Scenario 1: CI Build Failed

**User Query:**
```
"My GitHub Actions workflow failed with this log: [paste log]"
```

**Agent Response:**
```markdown
## Log Triage Report

### Summary
Node.js build failed due to missing module 'viem'. The dependency exists in 
package.json but wasn't installed in CI environment.

### Matched Error Signatures
1. **node_missing_module**: `Cannot find module 'viem'`

### Fix Plan (Prioritized)
1. Run clean install: `rm -rf node_modules && pnpm install`
2. Check lockfile changes and Node version consistency (CI vs local)
3. If monorepo, ensure package is listed in the right package.json

### Verification Checklist
- [ ] Re-run the exact failing command locally
- [ ] Re-run CI workflow and confirm green
- [ ] Add a regression test if applicable
```

### Scenario 2: Hardhat Test Failure

**User Query:**
```
"My hardhat test is failing with HH600 error"
```

**Agent Response:**
```markdown
## Log Triage Report

### Summary
Hardhat compilation failed due to compiler version mismatch between 
hardhat.config and contract pragma.

### Matched Error Signatures
1. **hardhat_compile**: `HH600: Compilation failed`

### Fix Plan (Prioritized)
1. Run `pnpm hardhat compile --show-stack-traces` locally
2. Check Solidity compiler version in hardhat config matches pragma
3. If error about artifacts/cache: remove `artifacts/ cache/` and recompile

### Verification Checklist
- [ ] Contracts compile successfully
- [ ] Tests pass locally
- [ ] CI passes
```

## Best Practices

1. **Extract First Error**: Often the first error causes cascading failures
2. **Minimal Reproduction**: Simplify to smallest failing case
3. **Reversible Fixes**: Try safe fixes (clean install, version pin) before refactoring
4. **Verify Thoroughly**: Re-run exact command + CI workflow
5. **Document Root Cause**: Add regression test or config comment

## Integration with SpoonReactSkill

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="debug_assistant",
    skill_paths=["./enterprise-skills/debugging/log-triage"],
    scripts_enabled=True
)

await agent.activate_skill("log-triage")

result = await agent.run(
    "My CI failed with this error: [paste log]. What's wrong and how do I fix it?"
)
print(result)
```

## Context Variables

- `{{log_file}}`: Path to log file
- `{{command}}`: Command that failed
- `{{environment}}`: Environment details
- `{{recent_changes}}`: Recent commits or dependency changes
