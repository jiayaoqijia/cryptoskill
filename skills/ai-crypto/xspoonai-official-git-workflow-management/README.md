# Git Workflow Management Skill

A comprehensive Git workflow automation skill for SpoonOS agents and Claude Code, providing intelligent commit message generation, branch management, pre-commit checks, and change history analysis.

## Features

- **Smart Commit Message Generation**: Automatically generate conventional commit messages based on staged changes
- **Pre-Commit Checks**: Run comprehensive validation before committing (linting, formatting, conflicts, secrets)
- **Branch Management**: Create, switch, merge, and delete branches following Git flow best practices
- **Change Analysis**: Analyze git history, generate changelogs, and identify code hotspots

## Installation

### For SpoonOS Agents

```bash
# Copy to your agent's skills directory
cp -r git-workflow/ /path/to/your/agent/.agent/skills/
```

### For Claude Code

```bash
# Copy to your workspace skills directory
cp -r git-workflow/ /path/to/your/project/.claude/skills/
```

## Quick Start

### Generate Commit Message

```bash
# Stage your changes
git add .

# Generate commit message
echo '{"type": "feat", "scope": "auth", "include_body": true}' | python scripts/generate_commit_message.py
```

### Run Pre-Commit Checks

```bash
echo '{"checks": ["conflicts", "secrets", "lint"], "auto_fix": true}' | python scripts/pre_commit_check.py
```

### Create Feature Branch

```bash
echo '{"action": "create", "branch_type": "feature", "name": "user-authentication"}' | python scripts/branch_manager.py
```

### Generate Changelog

```bash
echo '{"analysis_type": "changelog", "from_tag": "v1.0.0", "to_tag": "HEAD", "group_by": "type"}' | python scripts/change_analyzer.py
```

## Scripts Documentation

### 1. generate_commit_message.py

Analyzes staged changes and generates conventional commit messages.

**Input Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `type` | string | No | Auto-detected | Commit type (feat, fix, docs, style, refactor, perf, test, chore) |
| `scope` | string | No | Auto-detected | Scope of changes (e.g., auth, api, ui) |
| `subject` | string | No | Auto-generated | Commit subject line |
| `include_body` | boolean | No | false | Include detailed body in commit message |
| `include_breaking` | boolean | No | false | Include BREAKING CHANGE footer |

**Output:**

```json
{
  "success": true,
  "message": "feat(auth): add OAuth2 authentication flow\n\nImplement OAuth2 with Google and GitHub providers.",
  "type": "feat",
  "scope": "auth",
  "files_changed": 5,
  "lines_added": 234,
  "lines_deleted": 12,
  "changed_files": ["src/auth/oauth.py", "tests/test_auth.py"]
}
```

**Example Usage:**

```bash
# Auto-detect type and scope
echo '{}' | python scripts/generate_commit_message.py

# Specify type and scope
echo '{"type": "fix", "scope": "api"}' | python scripts/generate_commit_message.py

# Include detailed body
echo '{"type": "feat", "scope": "auth", "include_body": true}' | python scripts/generate_commit_message.py
```

### 2. pre_commit_check.py

Runs comprehensive pre-commit validation checks.

**Input Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `checks` | array | No | ["conflicts", "secrets", "large_files"] | List of checks to run |
| `auto_fix` | boolean | No | false | Automatically fix issues when possible |

**Available Checks:**

- `conflicts`: Check for merge conflict markers
- `secrets`: Detect potential secrets (API keys, passwords)
- `large_files`: Identify files larger than 10MB
- `lint`: Run linting (pylint, flake8, eslint)
- `format`: Check code formatting (black, prettier)

**Output:**

```json
{
  "success": true,
  "passed": true,
  "checks": {
    "conflicts": {"status": "passed", "message": "No conflicts detected"},
    "secrets": {"status": "passed", "message": "No obvious secrets detected"},
    "lint": {"status": "passed", "message": "Linting passed (pylint)"}
  },
  "summary": "3 passed, 0 failed, 0 warnings"
}
```

### 3. branch_manager.py

Manage git branches with best practices.

**Input Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | string | Yes | - | Action to perform (create, switch, delete, list, merge) |
| `branch_type` | string | No | "feature" | Branch type (feature, bugfix, hotfix, release) |
| `name` | string | Conditional | - | Branch name (required for create) |
| `branch_name` | string | Conditional | - | Full branch name (required for switch, delete, merge) |
| `base_branch` | string | No | Auto-detected | Base branch for new branches |
| `force` | boolean | No | false | Force delete unmerged branches |
| `no_ff` | boolean | No | true | Use --no-ff for merges |

**Actions:**

1. **create**: Create a new branch
2. **switch**: Switch to an existing branch
3. **delete**: Delete a branch
4. **list**: List all branches
5. **merge**: Merge a branch into current branch

**Output Examples:**

```json
// Create branch
{
  "success": true,
  "branch_name": "feature/user-authentication",
  "base_branch": "develop",
  "message": "Created and switched to branch 'feature/user-authentication'"
}

// List branches
{
  "success": true,
  "branches": [
    {"name": "main", "current": false},
    {"name": "develop", "current": true},
    {"name": "feature/user-auth", "current": false}
  ],
  "current_branch": "develop"
}
```

### 4. change_analyzer.py

Analyze git history and generate insights.

**Input Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `analysis_type` | string | No | "stats" | Type of analysis (changelog, contributors, hotspots, stats) |
| `from_ref` | string | No | - | Starting reference (tag or commit) |
| `to_ref` | string | No | "HEAD" | Ending reference |
| `group_by` | string | No | "type" | Grouping method for changelog (type, author) |
| `limit` | number | No | 100 | Maximum number of commits to analyze |

**Analysis Types:**

1. **changelog**: Generate changelog grouped by type or author
2. **contributors**: Analyze contributor statistics
3. **hotspots**: Identify frequently changed files
4. **stats**: Get commit statistics

**Output Examples:**

```json
// Changelog
{
  "success": true,
  "changelog": {
    "feat": [
      "feat(auth): add OAuth2 authentication",
      "feat(api): implement rate limiting"
    ],
    "fix": [
      "fix(db): resolve connection pool leak"
    ]
  },
  "total_commits": 45
}

// Contributors
{
  "success": true,
  "contributors": [
    {"name": "Alice", "commits": 120},
    {"name": "Bob", "commits": 85}
  ],
  "total_contributors": 2
}

// Hotspots
{
  "success": true,
  "hotspots": [
    {"file": "src/main.py", "changes": 45},
    {"file": "tests/test_api.py", "changes": 32}
  ]
}
```

## Best Practices

### Commit Messages

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance
- `test`: Tests
- `chore`: Maintenance

### Branch Naming

Use consistent naming conventions:

```
feature/user-authentication
bugfix/login-error-handling
hotfix/critical-security-patch
release/v1.2.0
```

### Pre-Commit Workflow

1. Stage changes: `git add <files>`
2. Run pre-commit checks
3. Fix any issues
4. Generate commit message
5. Review and commit
6. Push to remote

## Integration with SpoonOS

### Using with SpoonReactSkill

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="git_workflow_agent",
    skill_paths=[".agent/skills"],
    scripts_enabled=True
)

await agent.activate_skill("git-workflow-management")

# Agent can now use git workflow tools
result = await agent.run("Generate a commit message for my staged changes")
```

### Using with Claude Code

Simply copy the skill to your workspace:

```bash
cp -r git-workflow/ .claude/skills/
```

Then use natural language:
- "Generate a commit message for my changes"
- "Run pre-commit checks"
- "Create a feature branch for user authentication"

## Environment Variables

No environment variables required. The skill uses standard git commands.

## Requirements

- Git 2.0+
- Python 3.7+
- Optional: pylint, flake8, black, prettier (for linting/formatting checks)

## Troubleshooting

### "No staged changes found"

**Solution**: Stage your changes first with `git add <files>`

### "Linting failed"

**Solution**: Fix linting issues or use `auto_fix: true` to automatically fix formatting

### "Branch already exists"

**Solution**: Use a different branch name or delete the existing branch first

### "Merge conflicts detected"

**Solution**: Resolve conflicts manually before committing

## Contributing

This skill was contributed via Claude Code. To improve it:

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request with demo screenshots

## License

MIT License

## Author

Contributed via Claude Code

## Version

1.0.0
