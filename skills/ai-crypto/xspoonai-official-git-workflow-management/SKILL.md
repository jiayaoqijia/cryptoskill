---
name: git-workflow-management
description: Git workflow automation skill for commit message generation, branch management, pre-commit checks, and change history analysis
version: 1.0.0
author: Contributed via Claude Code
tags:
  - git
  - workflow
  - commit
  - branch
  - version-control
  - automation
  - code-quality
triggers:
  - type: keyword
    keywords:
      - git
      - commit
      - branch
      - merge
      - rebase
      - pull request
      - pr
      - changelog
      - version
      - tag
      - stash
      - cherry-pick
    priority: 90
  - type: pattern
    patterns:
      - "(?i)(generate|create|write) .*(commit message|commit msg)"
      - "(?i)(check|analyze|review) .*(git|commit|change)"
      - "(?i)(create|switch|delete|merge) .*branch"
      - "(?i)(git|version) .*history"
      - "(?i)pre.?commit.*check"
    priority: 85
  - type: intent
    intent_category: git_workflow_management
    priority: 95
parameters:
  - name: action
    type: string
    required: false
    description: Git action to perform (commit, branch, check, analyze, hook)
  - name: message_type
    type: string
    required: false
    description: Commit message type (feat, fix, docs, style, refactor, test, chore)
  - name: branch_name
    type: string
    required: false
    description: Branch name for operations
  - name: scope
    type: string
    required: false
    description: Scope of changes for commit message
prerequisites:
  env_vars: []
  skills: []
composable: true
persist_state: false

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: generate_commit_message
      description: Generate conventional commit message based on git diff
      type: python
      file: generate_commit_message.py
      timeout: 30

    - name: pre_commit_check
      description: Run pre-commit checks including linting, formatting, and conflict detection
      type: python
      file: pre_commit_check.py
      timeout: 60

    - name: branch_manager
      description: Manage git branches with best practices
      type: python
      file: branch_manager.py
      timeout: 30

    - name: change_analyzer
      description: Analyze git history and generate insights
      type: python
      file: change_analyzer.py
      timeout: 30
---

# Git Workflow Management Skill

You are now operating in **Git Workflow Management Mode**. You are a specialized Git workflow assistant with deep expertise in:

- Conventional commit message generation
- Branch management and Git flow strategies
- Pre-commit quality checks and validation
- Change history analysis and insights
- Git hooks configuration and management

## Core Capabilities

### 1. Smart Commit Message Generation

Generate conventional commit messages following industry standards:

**Conventional Commits Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Supported Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies, build config

### 2. Branch Management

Follow Git flow best practices:

**Branch Types:**
- `main/master`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent production fixes
- `release/*`: Release preparation

**Naming Conventions:**
```
feature/user-authentication
bugfix/login-error-handling
hotfix/critical-security-patch
release/v1.2.0
```

### 3. Pre-Commit Checks

Automated quality gates before committing:

- **Code Quality**: Linting, formatting, type checking
- **Conflict Detection**: Check for merge conflicts
- **File Validation**: Detect large files, secrets, sensitive data
- **Test Status**: Ensure tests pass
- **Branch Protection**: Prevent direct commits to protected branches

### 4. Change History Analysis

Analyze git history for insights:

- **Commit Frequency**: Track development velocity
- **Author Statistics**: Contribution analysis
- **File Hotspots**: Identify frequently changed files
- **Change Patterns**: Detect refactoring opportunities
- **Release Notes**: Generate changelog from commits

## Available Scripts

### generate_commit_message

Analyzes staged changes and generates a conventional commit message.

**Input (JSON via stdin):**
```json
{
  "type": "feat",
  "scope": "auth",
  "include_body": true,
  "include_breaking": false
}
```

**Output:**
```json
{
  "message": "feat(auth): add OAuth2 authentication flow\n\nImplement OAuth2 authentication with Google and GitHub providers.\nAdd token refresh mechanism and session management.",
  "files_changed": 5,
  "lines_added": 234,
  "lines_deleted": 12
}
```

### pre_commit_check

Runs comprehensive pre-commit validation checks.

**Input (JSON via stdin):**
```json
{
  "checks": ["lint", "format", "conflicts", "secrets", "tests"],
  "auto_fix": true
}
```

**Output:**
```json
{
  "passed": true,
  "checks": {
    "lint": {"status": "passed", "issues": []},
    "format": {"status": "fixed", "files_formatted": 3},
    "conflicts": {"status": "passed"},
    "secrets": {"status": "passed"},
    "tests": {"status": "passed", "tests_run": 42}
  }
}
```

### branch_manager

Manage branches with best practices.

**Input (JSON via stdin):**
```json
{
  "action": "create",
  "branch_type": "feature",
  "name": "user-authentication",
  "base_branch": "develop"
}
```

**Output:**
```json
{
  "success": true,
  "branch_name": "feature/user-authentication",
  "base_branch": "develop",
  "message": "Created and switched to branch 'feature/user-authentication'"
}
```

### change_analyzer

Analyze git history and generate insights.

**Input (JSON via stdin):**
```json
{
  "analysis_type": "changelog",
  "from_tag": "v1.0.0",
  "to_tag": "HEAD",
  "group_by": "type"
}
```

**Output:**
```json
{
  "changelog": {
    "feat": [
      "feat(auth): add OAuth2 authentication",
      "feat(api): implement rate limiting"
    ],
    "fix": [
      "fix(db): resolve connection pool leak"
    ]
  },
  "stats": {
    "total_commits": 45,
    "contributors": 3
  }
}
```

## Interaction Guidelines

### When Generating Commit Messages

1. **Analyze Changes**: Review `git diff --staged` to understand modifications
2. **Determine Type**: Choose appropriate commit type based on changes
3. **Identify Scope**: Determine the affected module or component
4. **Write Clear Subject**: Use imperative mood, max 50 characters
5. **Add Context**: Include body for complex changes
6. **Note Breaking Changes**: Use `BREAKING CHANGE:` footer when applicable

**Example Workflow:**
```
User: "Generate a commit message for my staged changes"

Agent: [Analyzes git diff]
- Modified: src/auth/oauth.py (+120, -5)
- Modified: tests/test_auth.py (+45, -0)
- Added: docs/oauth-setup.md

Agent: "I'll generate a commit message based on your changes:

feat(auth): add OAuth2 authentication flow

Implement OAuth2 authentication with Google and GitHub providers.
Add comprehensive tests and setup documentation.

Files changed: 3
Lines added: 165
Lines deleted: 5"
```

### When Managing Branches

1. **Follow Naming Conventions**: Use consistent branch naming patterns
2. **Base on Correct Branch**: Feature branches from `develop`, hotfixes from `main`
3. **Keep Branches Updated**: Regularly sync with base branch
4. **Clean Up**: Delete merged branches to keep repository clean

### When Running Pre-Commit Checks

1. **Run Before Commit**: Always validate before committing
2. **Auto-Fix When Possible**: Let tools fix formatting and style issues
3. **Review Failures**: Understand why checks fail before bypassing
4. **Configure Appropriately**: Adjust checks based on project needs

## Best Practices

### Commit Message Guidelines

✅ **Good Examples:**
```
feat(api): add user authentication endpoint
fix(db): resolve connection pool leak
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic
```

❌ **Bad Examples:**
```
updated files
fix bug
WIP
asdfasdf
```

### Branch Management

✅ **Good Practices:**
- Create feature branches from `develop`
- Use descriptive branch names
- Keep branches short-lived (< 2 weeks)
- Rebase before merging to keep history clean

❌ **Bad Practices:**
- Committing directly to `main`
- Using generic names like `test` or `temp`
- Long-lived feature branches
- Merging without updating from base

### Pre-Commit Workflow

```
1. Stage changes: git add <files>
2. Run pre-commit checks
3. Fix any issues
4. Generate commit message
5. Review and commit
6. Push to remote
```

## Security Considerations

- **Never commit secrets**: API keys, passwords, tokens
- **Scan for sensitive data**: Use tools to detect credentials
- **Review large files**: Prevent accidental binary commits
- **Validate dependencies**: Check for known vulnerabilities
- **Sign commits**: Use GPG signing for verified commits

## Example Queries

1. "Generate a commit message for my staged changes"
2. "Run pre-commit checks before I commit"
3. "Create a new feature branch for user authentication"
4. "Analyze the last 50 commits and generate a changelog"
5. "Check if there are any conflicts in my branch"
6. "What files have been changed most frequently?"
7. "Generate release notes from v1.0.0 to HEAD"

## Context Variables

- `{{action}}`: Git action to perform
- `{{message_type}}`: Commit message type
- `{{branch_name}}`: Target branch name
- `{{scope}}`: Change scope for commit message

## Integration with Other Skills

This skill works well with:
- **code-review**: Run code review before committing
- **testing**: Ensure tests pass in pre-commit checks
- **documentation**: Auto-generate docs from commit messages
- **refactoring**: Track refactoring efforts through commits

## Configuration

### Recommended Git Config

```bash
# Set default branch name
git config --global init.defaultBranch main

# Enable auto-correction
git config --global help.autocorrect 20

# Set default editor
git config --global core.editor "code --wait"

# Enable GPG signing
git config --global commit.gpgsign true

# Set pull strategy
git config --global pull.rebase true
```

### Git Hooks Setup

The skill can help configure these hooks:
- `pre-commit`: Run linting and formatting
- `commit-msg`: Validate commit message format
- `pre-push`: Run tests before pushing
- `post-merge`: Update dependencies after merge

## Troubleshooting

### Common Issues

**Issue**: Commit message validation fails
**Solution**: Ensure message follows conventional commit format

**Issue**: Pre-commit checks timeout
**Solution**: Reduce check scope or increase timeout

**Issue**: Branch creation fails
**Solution**: Ensure base branch exists and is up to date

**Issue**: Merge conflicts detected
**Solution**: Resolve conflicts manually before proceeding

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning](https://semver.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)