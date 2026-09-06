# Secret Guard Skill

**Secret Guard** is a lightweight security automation skill designed to prevent accidental leakage of sensitive credentials. It scans the `git` staged area for potential secrets (API keys, private keys, tokens) before they are committed to the codebase.

## Features

- **🛡️ Pre-commit Safety**: Scans only staged files (`git diff --cached`), ensuring speed and relevance.
- **🔒 Zero Dependencies**: Written in pure Python (Standard Library only), no `pip install` required.
- **👁️ Privacy Focused**: Detected secrets are masked (e.g., `sk-123***`) in the output to prevent secondary leakage in logs.
- **📦 Multi-Pattern Support**: Detects AWS Keys, OpenAI Keys, GitHub Tokens, and Generic Private Keys.

## Quick Start

### Installation
Copy the `secret-guard` folder into your agent's skill directory (e.g., `.claude/skills/`).

### Usage
This skill is triggered naturally when you ask the agent to check code or prepare for a commit.

**Example Prompts:**
- "Check my staged files for security issues."
- "I'm ready to commit, can you scan for secrets?"
- "Run secret-guard."

## Configuration

No environment variables are required. The script relies on the system having `git` installed and initialized in the current directory.

| Variable | Required | Description |
|----------|----------|-------------|
| N/A | No | This skill works out-of-the-box. |

## Error Handling

- **Exit Code 0**: No secrets found. The agent will proceed.
- **Exit Code 1**: Potential secrets found. The agent will alert the user and block the recommendation to commit until resolved.
- **Git Missing**: If `git` is not installed, the tool will return a friendly error message.

## Supported Patterns

Currently detects the following patterns via Regex:
- AWS Access Key ID
- AWS Secret Key
- OpenAI API Key
- GitHub Personal Access Token
- Standard Private Key Headers (RSA/DSA/EC)
- Generic "api_key" / "secret_token" assignments

## Directory Structure

```text
secret-guard/
├── SKILL.md              # Skill definition and metadata
├── README.md             # Documentation
└── scripts/
    └── scan.py           # Core scanning logic (Pure Python)