#!/bin/bash
# CryptoSkill auto-update bot - runs every 6 hours
# Logs to scripts/bot.log

cd "$(dirname "$0")/.." || exit 1
LOG="scripts/bot.log"

echo "=== Bot run: $(date -u) ===" >> "$LOG"

python3 scripts/auto-update.py \
  --skip-openclaw \
  --no-ai-security \
  --update-watchlist \
  >> "$LOG" 2>&1

# Regenerate catalog from disk to avoid duplicates
python3 scripts/update-catalog.py >> "$LOG" 2>&1

# Score all skills (Phase 1: static + security + depth heuristic)
python3 scripts/score-skills.py >> "$LOG" 2>&1

# Track score regressions (Phase 4: snapshot + diff)
python3 scripts/score-history.py >> "$LOG" 2>&1

# Update website HTML stats to match current counts
TOTAL=$(find skills -mindepth 2 -maxdepth 2 -type d | wc -l)
MCP=$(find skills/mcp-servers -mindepth 1 -maxdepth 1 -type d | wc -l)
CATS=$(ls -d skills/*/ | wc -l)
sed -i "s/statSkills\">[0-9]*/statSkills\">$TOTAL/" docs/index.html
sed -i "s/statMCP\">[0-9]*/statMCP\">$MCP/" docs/index.html
sed -i "s/[0-9]\+\+ crypto skills/$TOTAL+ crypto skills/" docs/index.html
sed -i "s/[0-9]\+ MCP servers/$MCP MCP servers/" docs/index.html
OFFICIAL=$(grep -rl 'Classification.*OFFICIAL' skills/*/*/SOURCE.md 2>/dev/null | wc -l)

# Update README badges
sed -i "s/skills-[0-9]*/skills-$TOTAL/" README.md
sed -i "s/MCP%20servers-[0-9]*/MCP%20servers-$MCP/" README.md
sed -i "s/official-[0-9]*/official-$OFFICIAL/" README.md

echo "Updated website + README: $TOTAL skills, $MCP MCPs, $OFFICIAL official" >> "$LOG"

# Commit all changes if any
git add docs/ README.md scripts/watchlist.json >> "$LOG" 2>&1
if ! git diff --cached --quiet 2>/dev/null; then
  git commit -m "Bot: update $TOTAL skills, $MCP MCPs, $OFFICIAL official" >> "$LOG" 2>&1
  git push >> "$LOG" 2>&1
fi

echo "=== Done: $(date -u) ===" >> "$LOG"
echo "" >> "$LOG"

# Keep log under 10k lines
tail -10000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
