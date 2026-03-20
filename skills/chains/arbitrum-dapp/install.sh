#!/bin/bash
set -e

SKILL_NAME="arbitrum-dapp-skill"
SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME"
REPO_URL="https://github.com/hummusonrails/arbitrum-dapp-skill.git"

echo "Installing $SKILL_NAME skill for Claude Code..."

# Create skills directory if it doesn't exist
mkdir -p "$HOME/.claude/skills"

# Clone or update
if [ -d "$SKILL_DIR" ]; then
  echo "Updating existing installation..."
  cd "$SKILL_DIR"
  git pull origin main
else
  echo "Cloning skill..."
  git clone "$REPO_URL" "$SKILL_DIR"
fi

# Pings GoatCounter to count installs. No cookies, no personal data.
# What is sent: a single pageview hit on "/install" — nothing else.
# The token below can ONLY record pageviews; it cannot read any data.
# See: https://www.goatcounter.com
# To opt out: set ARBITRUM_SKILL_NO_ANALYTICS=1 before running this script.
if [ -z "${ARBITRUM_SKILL_NO_ANALYTICS:-}" ]; then
  curl -s -X POST "https://arbitrum-dapp-skill.goatcounter.com/api/v0/count" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer s8p7jjjeclhc1gs76e5ry1zm4pgm5e1qlxz11uwr6zslbpr4h" \
    --data '{"no_sessions": true, "hits": [{"path": "/install"}]}' \
    > /dev/null 2>&1 || true
fi

echo ""
echo "Installed to: $SKILL_DIR"
echo ""
echo "The skill is now available in Claude Code. Start a new session and ask Claude to help you build an Arbitrum dApp."
