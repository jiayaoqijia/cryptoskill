#!/bin/bash
# CryptoSkill auto-update bot - runs every 6 hours
# Logs to scripts/bot.log

cd "$(dirname "$0")/.." || exit 1
LOG="scripts/bot.log"

echo "=== Bot run: $(date -u) ===" >> "$LOG"

python3 scripts/auto-update.py \
  --skip-openclaw \
  --skip-web \
  --no-ai-security \
  --update-watchlist \
  >> "$LOG" 2>&1

echo "=== Done: $(date -u) ===" >> "$LOG"
echo "" >> "$LOG"

# Keep log under 10k lines
tail -10000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
