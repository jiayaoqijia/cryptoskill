# GitHub Manager Skill

The **GitHub Manager** skill empowers SpoonOS agents to automate GitHub workflows. It uses the `PyGithub` library to interact with the GitHub API.

## Features

- **List Issues**: Fetch open issues with optional filtering.
- **Create Issues**: Open new issues with titles and bodies.
- **Comment**: Add comments to existing issues or PRs.

## Usage

### Parameters

- `action` (string, required): One of `list_issues`, `create_issue`, `comment_issue`, `get_issue`.
- `repo` (string, required): Repository name in `owner/name` format.
- `title` (string, optional): Title for new issues.
- `body` (string, optional): Body text for issues or comments.
- `issue_number` (integer, optional): ID of the issue to comment on or retrieve.

### Example Agent Prompts

> "List the top 5 open bugs in the 'XSpoonAi/spoon-core' repo."
> "Create a feature request in 'my-org/my-repo' titled 'Add Dark Mode' with body 'Please add dark mode support.'"

### Output

Returns JSON-formatted data containing issue details or confirmation messages.

## Setup

Ensure your environment has the `GITHUB_TOKEN` set.
```bash
export GITHUB_TOKEN=your_pat_here
```
