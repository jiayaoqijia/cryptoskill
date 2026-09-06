---
name: read-temp-file
description: Reads the content of a file located in the temporary directory (temp/) which is otherwise ignored by git.
---

# Read Temp File Skill

This skill allows you to safely read files from the project's temporary directory `temp/`, bypassing standard git-ignore restrictions.

## Instructions

When you need to read a file from the `temp/` directory (e.g., to verify the content of a generated issue description):

1.  **Do NOT use the `read_file` tool.** It will fail for ignored files.
2.  Instead, use the `run_shell_command` tool to execute the helper script.
3.  Command format: `python3 .gemini/skills/read-temp-file/scripts/read_temp_file.py <file_path>`

### Example

To read `temp/gh_issues/issue_description.md`:

```bash
python3 .gemini/skills/read-temp-file/scripts/read_temp_file.py temp/gh_issues/issue_description.md
```

### Constraints
*   The file **must** be inside the `temp/` directory.
*   The file **must not** be binary.
*   The file **must not** exceed 2000 lines.