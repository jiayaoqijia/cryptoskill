#!/usr/bin/env bash
# Template: idempotent keeper for a localhost dashboard + cloudflared quick tunnel.
# Register as a Hermes cron job: no_agent=true, deliver=origin, script=service_keeper.sh, */10 * * * *
# Empty stdout => no notification. It prints ONLY when the tunnel URL changed (delta-only).
#
# Why a script (not systemd): on hosts where the Hermes gateway is a SYSTEM service,
# `systemctl --user` fails with "Failed to connect to bus: No medium found". Start detached
# children from inside this file with setsid+nohup, and let cron be the supervisor.
set -uo pipefail

HH="$HOME/.hermes"
SCRIPTS="$HH/scripts"; DATA="$HH/data"; LOGS="$HH/logs"
PORT="${DASH_PORT:-8787}"
SRV="$SCRIPTS/dashboard_server.py"          # server file to keep alive
SRV_LOG="$LOGS/dash_server.log"
TUN_LOG="$LOGS/dash_tunnel.log"
URL_FILE="$DATA/dash_url.txt"
SEEN_FILE="$DATA/dash_url_seen.txt"
mkdir -p "$LOGS" "$DATA"

# ---------- 1. server ----------
if ! curl -sf -m 5 "http://127.0.0.1:$PORT/healthz" >/dev/null 2>&1; then
  # NOTE: match the process by a bracketed pattern so the pkill never matches this script's own
  # command line (a bare `pkill -f dashboard_server.py` run from an interactive shell kills it).
  pkill -f "[d]ashboard_server.py" >/dev/null 2>&1
  sleep 1
  setsid nohup env DASH_PORT="$PORT" python3 -u "$SRV" >>"$SRV_LOG" 2>&1 </dev/null &
  for _ in $(seq 1 20); do sleep 1; curl -sf -m 3 "http://127.0.0.1:$PORT/healthz" >/dev/null 2>&1 && break; done
fi

# ---------- 2. tunnel ----------
if ! pgrep -f "cloudflared tunnel --url http://localhost:$PORT" >/dev/null 2>&1; then
  : >"$TUN_LOG"                                     # truncate: only the newest URL should match
  setsid nohup cloudflared tunnel --url "http://localhost:$PORT" --no-autoupdate >>"$TUN_LOG" 2>&1 </dev/null &
  for _ in $(seq 1 20); do sleep 2; grep -qo 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUN_LOG" && break; done
fi

# ---------- 3. report a NEW url only ----------
URL="$(grep -ho 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUN_LOG" 2>/dev/null | tail -1)"
if [ -z "$URL" ]; then
  echo "⚠ dashboard: tunnel belum dapat URL — cek $TUN_LOG" >&2
  exit 0
fi
echo "$URL" >"$URL_FILE"
if [ ! -f "$SEEN_FILE" ] || [ "$(cat "$SEEN_FILE" 2>/dev/null)" != "$URL" ]; then
  echo "$URL" >"$SEEN_FILE"
  printf '🐋 DASHBOARD — live\n'
  printf '• %s\n' "$URL"
  printf '• auto-refresh tiap 60 detik · bisa dibuka dari HP (Add to Home Screen)\n'
  printf '• link quick-tunnel ganti kalau process restart — watchdog cek tiap 10 menit & kirim link baru\n'
fi
exit 0
