# Log Triage & Fix Plan (Debugging)

> **Source:** ETHPanda  
> **Track 4:** Enterprise & Team Skills → Debugging

This skill helps an agent analyze error logs (CI/build/runtime) and generate:
- Root-cause candidates (ranked by confidence)
- A prioritized fix plan with concrete commands
- Verification checklist to confirm fixes

## Quick Demo

### Using conda environment (recommended)

```powershell
# 1. Create and activate conda environment
conda create -n skilltest python=3.12 -y
conda activate skilltest

# 2. Run the triage script on sample logs
python scripts/log_triage.py --file scripts/sample_log_node.txt --format md
python scripts/log_triage.py --file scripts/sample_log_python.txt --format md
python scripts/log_triage.py --file scripts/sample_log_hardhat.txt --format md
```

### Using system Python

```bash
# If you have Python 3.10+ installed globally
python scripts/log_triage.py --file scripts/sample_log_node.txt --format md
```

## What to Submit in PR

This folder includes:
- `SKILL.md` - Skill definition for agent triggering
- `README.md` - Human-readable documentation (this file)
- `scripts/log_triage.py` - Pattern matching and fix generation
- `scripts/sample_log_*.txt` - Example error logs for demo

**Required for PR approval:**
- Screenshot of running the demo commands
- Screenshot of generated output reports

## Supported Log Types

| Ecosystem | Error Patterns | Fix Strategies |
|-----------|----------------|----------------|
| **Node/TypeScript** | Missing modules, TS type errors | Clean install, lockfile sync, TS version pinning |
| **Python** | ModuleNotFoundError, import issues | Reinstall venv, check requirements.txt/pyproject.toml |
| **Rust** | Cargo compile errors, dependency conflicts | Update Cargo.lock, check rustc version |
| **Solidity/Hardhat** | Compilation failures, gas issues | Compiler version match, clear cache/artifacts |
| **HTTP/Network** | 429 rate limits, timeouts | Retries with backoff, API key checks |

## Output Format

The script generates a Markdown report with:

1. **Summary**: One-paragraph explanation of the failure
2. **Error Signatures**: Specific patterns matched in the log
3. **Fix Plan**: Ranked steps with exact commands to run
4. **Verification Checklist**: How to confirm the issue is resolved

### Example Output

```markdown
# Log Triage Report

## Source
scripts/sample_log_node.txt

## Matched error signatures
1. **node_missing_module**: `Cannot find module 'viem'`

## Fix plan (prioritized)
1. Run a clean install: `rm -rf node_modules && pnpm install` (or npm/yarn).
2. Check lockfile changes and Node version consistency (CI vs local).
3. If it's a workspace/monorepo, ensure package is listed in the right package.json.

## Verification checklist
- Re-run the exact failing command locally
- Re-run CI workflow and confirm green
- Add a regression test if applicable
```

## Installation & Dependencies

This skill uses **only Python standard library** - no external dependencies required!

The script uses:
- `argparse` - Command-line argument parsing
- `re` - Regular expression pattern matching
- `pathlib` - File path operations

## Usage in SpoonReactSkill

```python
from spoon_ai.agents import SpoonReactSkill
from spoon_ai.chat import ChatBot

# Configure agent with log-triage skill
agent = SpoonReactSkill(
    name="debug_assistant",
    description="AI agent for debugging and error analysis",
    skill_paths=["./enterprise-skills/debugging/log-triage"],
    scripts_enabled=True,
    auto_trigger_skills=True,
    llm=ChatBot(llm_provider="openai", model_name="gpt-4o")
)

await agent.initialize()
await agent.activate_skill("log-triage")

# Example usage
result = await agent.run(
    """
    My GitHub Actions workflow failed with this error:
    
    Error: Cannot find module 'viem'
    at Function.Module._resolveFilename (node:internal/modules/cjs/loader:xxx)
    
    What's wrong and how can I fix it?
    """
)
print(result)
```

## Usage in Claude Code

```bash
# Copy skill to your workspace
cp -r enterprise-skills/debugging/log-triage/ .claude/skills/

# Or for agent workspace
cp -r enterprise-skills/debugging/log-triage/ .agent/skills/

# Then ask Claude to help debug errors
# Claude will automatically use the skill when you paste error logs
```

## Extending the Skill

To add more error patterns, edit `scripts/log_triage.py`:

```python
PATTERNS = [
    # Add your pattern here
    ("your_pattern_name", re.compile(r"your regex pattern"), [
        "Fix step 1",
        "Fix step 2",
        "Fix step 3",
    ]),
    # ... existing patterns ...
]
```

### Pattern Structure

Each pattern is a tuple with:
1. **Name** (string): Identifier for the error type
2. **Regex** (compiled regex): Pattern to match in logs
3. **Fix steps** (list of strings): Prioritized commands/actions

### Example: Adding a New Pattern

```python
("go_module_not_found", re.compile(r"cannot find module ([^\s]+)"), [
    "Run `go mod tidy` to sync dependencies",
    "Check if module exists in go.mod",
    "Try `go get <module>` if it's missing",
])
```

## Common Use Cases

### 1. CI/CD Pipeline Failures

**Input:** GitHub Actions / GitLab CI / Jenkins logs

**Agent generates:**
- Root cause analysis
- Environment-specific fixes
- Cache/dependency cleanup steps

### 2. Local Build Errors

**Input:** Terminal output from `npm run build`, `cargo build`, `hardhat compile`

**Agent generates:**
- Compiler/toolchain version checks
- Configuration file corrections
- Dependency resolution steps

### 3. Runtime Crashes

**Input:** Stack traces from production or staging

**Agent generates:**
- Exception analysis
- Code path investigation
- Monitoring/logging improvements

### 4. Test Suite Failures

**Input:** Jest/Pytest/Hardhat test output

**Agent generates:**
- Test isolation issues
- Mock/fixture problems
- Async timing fixes

## Best Practices for Log Analysis

1. **Provide Full Context**
   - Include 20-50 lines around the error
   - Mention the command that was running
   - Share environment details (OS, versions)

2. **Start with First Error**
   - Often the first error causes cascading failures
   - Later errors might be symptoms, not root causes

3. **Try Safe Fixes First**
   - Clean install (delete node_modules/venv)
   - Clear build caches
   - Pin/lock dependency versions

4. **Verify Thoroughly**
   - Re-run locally with exact command
   - Re-run full CI workflow
   - Add regression test if possible

## Troubleshooting the Skill Itself

### Issue: Script not executable

```powershell
# On Windows with conda
conda activate skilltest
python scripts/log_triage.py --help

# On Linux/Mac
chmod +x scripts/log_triage.py
./scripts/log_triage.py --help
```

### Issue: File encoding errors

The script reads logs with `encoding="utf-8", errors="ignore"` to handle non-UTF8 characters. If you see garbled output, the pattern matching may still work on ASCII portions.

### Issue: No patterns matched

If the script reports "No known patterns matched", you can:
1. Add a new pattern for your specific error type
2. Share the log with the maintainers to expand coverage
3. Use the generic guidance to manually analyze

## Contributing New Patterns

We welcome contributions! To add support for new error types:

1. Identify the error signature (unique string or regex)
2. Research common fixes from Stack Overflow, docs, GitHub issues
3. Test your regex on real logs
4. Submit a PR with:
   - Updated `PATTERNS` list in `log_triage.py`
   - Sample log file demonstrating the pattern
   - Screenshot of the generated fix plan

## License

MIT License - see repository root for details

## Credits

Created for **ETHPanda** skill challenge submission.

Built on patterns collected from:
- Stack Overflow troubleshooting guides
- CI/CD platform documentation
- Real-world debugging sessions
- Open source issue trackers

---

**Questions or Issues?**  
Open an issue in the [spoon-awesome-skill](https://github.com/XSpoonAi/spoon-awesome-skill) repository.
