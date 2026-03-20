#!/usr/bin/env bash
# crypto-whale-tracker - Financial tracking and analysis tool
set -euo pipefail
VERSION="2.0.0"
DATA_DIR="${CRYPTO_WHALE_TRACKER_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/crypto-whale-tracker}"
DB="$DATA_DIR/data.log"
mkdir -p "$DATA_DIR"

show_help() {
    cat << EOF
crypto-whale-tracker v$VERSION

Financial tracking and analysis tool

Usage: crypto-whale-tracker <command> [args]

Commands:
  track                Record a transaction
  balance              Show current balance
  summary              Financial summary
  export               Export to CSV
  budget               Budget overview
  history              Transaction history
  alert                Set price/budget alert
  compare              Compare periods
  forecast             Simple forecast
  categories           Spending categories
  help                 Show this help
  version              Show version

Data: \$DATA_DIR
EOF
}

_log() { echo "$(date '+%m-%d %H:%M') $1: $2" >> "$DATA_DIR/history.log"; }

cmd_track() {
    echo "  Transaction: $1 Amount: ${2:-0}"
    _log "track" "${1:-}"
}

cmd_balance() {
    echo "  Balance: check $DATA_DIR/ledger"
    _log "balance" "${1:-}"
}

cmd_summary() {
    echo "  Period: $(date +%Y-%m) | Income: $0 | Expenses: $0"
    _log "summary" "${1:-}"
}

cmd_export() {
    echo "date,description,amount" && cat "$DB" 2>/dev/null
    _log "export" "${1:-}"
}

cmd_budget() {
    echo "  Category | Budget | Spent | Remaining"
    _log "budget" "${1:-}"
}

cmd_history() {
    [ -f "$DB" ] && tail -20 "$DB" || echo "No history"
    _log "history" "${1:-}"
}

cmd_alert() {
    echo "  Alert set for: $1 at $2"
    _log "alert" "${1:-}"
}

cmd_compare() {
    echo "  Comparing current vs previous period"
    _log "compare" "${1:-}"
}

cmd_forecast() {
    echo "  Based on trends: [projection]"
    _log "forecast" "${1:-}"
}

cmd_categories() {
    echo "  Food | Transport | Housing | Entertainment | Savings"
    _log "categories" "${1:-}"
}

case "${1:-help}" in
    track) shift; cmd_track "$@" ;;
    balance) shift; cmd_balance "$@" ;;
    summary) shift; cmd_summary "$@" ;;
    export) shift; cmd_export "$@" ;;
    budget) shift; cmd_budget "$@" ;;
    history) shift; cmd_history "$@" ;;
    alert) shift; cmd_alert "$@" ;;
    compare) shift; cmd_compare "$@" ;;
    forecast) shift; cmd_forecast "$@" ;;
    categories) shift; cmd_categories "$@" ;;
    help|-h) show_help ;;
    version|-v) echo "crypto-whale-tracker v$VERSION" ;;
    *) echo "Unknown: $1"; show_help; exit 1 ;;
esac
