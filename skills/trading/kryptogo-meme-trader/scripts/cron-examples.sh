#!/usr/bin/env bash
# KryptoGO Meme Trader — OpenClaw Cron Configurations
#
# Usage:
#   bash scripts/cron-examples.sh setup-default      # Supervised: analysis + notifications (recommended)
#   bash scripts/cron-examples.sh setup-autonomous    # Autonomous: auto-buy + auto-sell (opt-in)
#   bash scripts/cron-examples.sh teardown            # Remove all trading cron jobs
#
# Or copy individual `openclaw cron add` commands from the strategies below.

set -euo pipefail

# ============================================================================
# COMMAND: setup-default (supervised, analysis-only)
# ============================================================================

if [[ "${1:-}" == "setup-default" ]]; then
  echo "Setting up default trading cron jobs (supervised mode)..."
  echo "  Trades will NOT be auto-executed. The agent will analyze and send recommendations."
  echo ""

  echo "→ Adding stop-loss-tp (every 5 min)..."
  openclaw cron add \
    --every 5m \
    --name "stop-loss-tp" \
    --message "Run the monitoring script: 'source ~/.openclaw/workspace/.env && python3 skills/kryptogo-meme-trader/scripts/monitor.py'. Check portfolio for stop-loss or take-profit conditions. Report triggered conditions to the user. Do NOT auto-execute sells."

  echo ""
  echo "→ Adding discovery-scan (every 1 hour)..."
  openclaw cron add \
    --every 1h \
    --name "discovery-scan" \
    --timeout-seconds 900 \
    --message "Load the kryptogo-meme-trader skill. Source .env. Execute the full discovery workflow:
1. Read memory/trading-preferences.json for current parameters.
2. Read memory/trading-lessons.md (if exists) to avoid known bad patterns.
3. Check open positions count — skip scanning if at max_open_positions.
4. Scan for candidates:
   - Pro/Alpha tier: call /signal-dashboard (sort_by=signal_count, page_size=10).
   - Free tier: call /agent/trending-tokens with min_market_cap filter.
5. Run top candidates through the 7-step analysis pipeline.
6. Send recommendations to the user. Do NOT auto-execute buys.
7. Update memory/trading-state.json with scan timestamp.
8. If any trades were closed since last scan: run post-trade reflection and update trading-lessons.md.
Report ALL findings to the user. If nothing happened, stay silent."

  echo ""
  echo "✓ Default setup complete (supervised mode). Two cron jobs active:"
  echo "  • stop-loss-tp    — every 5 min  (portfolio monitoring, notify only)"
  echo "  • discovery-scan  — every 1 hour (token discovery, recommend only)"
  echo ""
  echo "Run 'openclaw cron list' to verify."
  exit 0
fi

# ============================================================================
# COMMAND: setup-autonomous (opt-in, auto-execution enabled)
# ============================================================================

if [[ "${1:-}" == "setup-autonomous" ]]; then
  echo ""
  echo "WARNING: Autonomous mode enables automatic trade execution."
  echo "Only use with a dedicated low-value wallet."
  echo ""

  echo "Setting up autonomous trading cron jobs..."
  echo ""

  echo "→ Adding stop-loss-tp (every 5 min)..."
  openclaw cron add \
    --every 5m \
    --name "stop-loss-tp" \
    --message "Run the monitoring script: 'source ~/.openclaw/workspace/.env && python3 skills/kryptogo-meme-trader/scripts/monitor.py'. Report the output."

  echo ""
  echo "→ Adding discovery-scan (every 30 min)..."
  openclaw cron add \
    --every 30m \
    --name "discovery-scan" \
    --timeout-seconds 900 \
    --message "Load the kryptogo-meme-trader skill. Source .env. Execute the full discovery workflow:
1. Read memory/trading-preferences.json for current parameters.
2. Read memory/trading-lessons.md (if exists) to avoid known bad patterns.
3. Check open positions count — skip buying if at max_open_positions.
4. Scan for candidates:
   - Pro/Alpha tier: call /signal-dashboard (sort_by=signal_count, page_size=10).
   - Free tier: call /agent/trending-tokens with min_market_cap filter.
5. Run top candidates through the 7-step analysis pipeline.
6. For tokens passing ALL criteria in the Bullish Checklist: execute buy with max_position_size.
   For medium risk: ask user for confirmation (unless risk_tolerance=aggressive).
7. Log any new trades to memory/trading-journal.json.
8. Update memory/trading-state.json with scan timestamp.
9. If any trades were closed since last scan: run post-trade reflection and update trading-lessons.md.
10. If 20+ trades or 7+ days since last review: trigger Strategy Review.
Report ALL actions to the user. If nothing happened, stay silent."

  echo ""
  echo "✓ Autonomous setup complete. Two cron jobs active:"
  echo "  • stop-loss-tp    — every 5 min  (exit monitoring + auto-sell)"
  echo "  • discovery-scan  — every 30 min (new token discovery + auto-buy)"
  echo ""
  echo "Run 'openclaw cron list' to verify."
  exit 0
fi

# ============================================================================
# COMMAND: teardown
# ============================================================================

if [[ "${1:-}" == "teardown" ]]; then
  echo "Removing all trading cron jobs..."
  openclaw cron remove stop-loss-tp 2>/dev/null || true
  openclaw cron remove discovery-scan 2>/dev/null || true
  openclaw cron remove daily-portfolio-summary 2>/dev/null || true
  openclaw cron remove trading-scan-15m 2>/dev/null || true
  openclaw cron remove signal-monitor 2>/dev/null || true
  openclaw cron remove portfolio-monitor 2>/dev/null || true
  openclaw cron remove conservative-scan 2>/dev/null || true
  echo "✓ All trading cron jobs removed."
  exit 0
fi

# ============================================================================
# If no command given, print usage and strategy reference
# ============================================================================

cat <<'USAGE'
Usage:
  bash scripts/cron-examples.sh setup-default      # Supervised: analysis + notify (recommended)
  bash scripts/cron-examples.sh setup-autonomous    # Autonomous: auto-buy + auto-sell (opt-in)
  bash scripts/cron-examples.sh teardown            # Remove all trading cron jobs

Below are additional strategy examples you can copy and run individually.
USAGE

echo ""

# ============================================================================
# STRATEGY 1: Default — Supervised Dual Cron (RECOMMENDED)
# ============================================================================
# Two jobs: fast portfolio monitoring + slower discovery cycle
# Both in supervised mode: notify user, do NOT auto-execute
#
# Install with: bash scripts/cron-examples.sh setup-default

# ============================================================================
# STRATEGY 2: Daily Summary Only
# ============================================================================
# No trading, just a morning report

# openclaw cron add \
#   --cron "0 1 * * *" \
#   --name "daily-portfolio-summary" \
#   --message "Load the kryptogo-meme-trader skill. Call /agent/portfolio with the agent wallet address from .env. Send me a daily summary including: all open positions with current PnL (% and USD), total portfolio value, any positions that hit stop-loss or take-profit thresholds overnight. Format as a clean summary, not raw JSON."

# ============================================================================
# STRATEGY 3: Conservative (ask before trading)
# ============================================================================
# Scan and analyze, but NEVER auto-trade — always ask first

# openclaw cron add \
#   --every 1h \
#   --name "conservative-scan" \
#   --message "Load the kryptogo-meme-trader skill. Scan trending tokens and run analysis. Do NOT execute any trades. Instead, if you find tokens that pass the bullish checklist, send me a summary with your recommendation and ask for confirmation before trading."

# ============================================================================
# UTILITY COMMANDS
# ============================================================================

# openclaw cron list                          # List all active cron jobs
# openclaw cron remove <name>                 # Remove a specific job
# bash scripts/cron-examples.sh teardown      # Remove ALL trading jobs
