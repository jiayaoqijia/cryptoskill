# Security Linting Skill

The **Security Linting** skill brings automated security analysis to your SpoonOS agents. It leverages `bandit`, a tool designed to find common security issues in Python code.

## Features

- **Recursive Scanning**: Scans entire directories or single files.
- **Severity Filtering**: Categorizes issues by severity (Low, Medium, High).
- **JSON Output**: Returns structured data for easy parsing by AI agents.
- **Auto-Installation**: Automatically asserts `bandit` is installed.

## Usage

### Parameters

- `path` (string, required): The file or directory path to scan.
- `recursive` (boolean, optional): Whether to scan recursively (default: `True`).
- `format` (string, optional): Output format, e.g., 'json' or 'txt' (default: `json`).

### Example Agent Prompt

> "Scan the 'src' directory for security vulnerabilities and summarize the high-severity issues."

### Output Structure

```json
{
  "metrics": {
    "_totals": {
      "loc": 120,
      "nosec": 0,
      "skipped_tests": 0,
      "sev": 6,
      "conf": 6
    }
  },
  "results": [
    {
      "code": "exec(user_input)",
      "filename": "unsafe.py",
      "issue_severity": "HIGH",
      "issue_text": "Use of exec detected."
    }
  ]
}
```

## Troubleshooting

- **Bandit not found**: The script attempts to install `bandit` via pip. Ensure your environment allows pip execution.
- **Permission Denied**: Ensure the agent has read access to the target directory.
