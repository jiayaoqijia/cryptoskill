#!/bin/bash
# GitHub Integration Skill - Demo Script
# Usage: GITHUB_TOKEN=ghp_xxx ./run_demo.sh

set -e
cd "$(dirname "$0")"

if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: Set GITHUB_TOKEN first"
  echo "  export GITHUB_TOKEN=ghp_xxxxxxxxxxxx"
  exit 1
fi

echo "=== 1. List Issues (XSpoonAi/spoon-awesome-skill) ==="
echo '{"action":"list_issues","repo":"XSpoonAi/spoon-awesome-skill","state":"open","limit":3}' | python3 github_issue.py
echo ""

echo "=== 2. List PRs (XSpoonAi/spoon-awesome-skill) ==="
echo '{"action":"list_prs","repo":"XSpoonAi/spoon-awesome-skill","state":"open","limit":3}' | python3 github_pr.py
