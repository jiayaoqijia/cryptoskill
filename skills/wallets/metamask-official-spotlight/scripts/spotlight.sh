#!/usr/bin/env bash
# Bring up Sentry Spotlight for a MetaMask Mobile dev build. Idempotent: safe to
# re-run. Run it from anywhere inside the metamask-mobile checkout.
#
#   spotlight.sh [on] [flags]       start the sidecar, fix .js.env, open the UI, and
#                                   reset Metro when .js.env changed
#       --no-open                   do not open the browser
#       --restart-metro             reset Metro even if .js.env did not change
#       --no-metro                  never touch Metro (print the manual steps instead)
#   spotlight.sh status             is the sidecar up, and are events arriving?
#   spotlight.sh mcp <tool> [json]  call a Spotlight MCP tool (no MCP setup needed)
#   spotlight.sh off                stop the sidecar (not Metro)
#
# Resetting Metro = stop the Metro already listening on its port (only this
# checkout's Metro), then `yarn watch:clean` from the repo root, detached. Babel
# inlines .js.env at bundle time, so a reload is not enough, and a second
# `yarn watch:clean` aborts on the busy port. The replacement Metro is detached, so
# its terminal keys (r, j) are gone; use --no-metro to keep your own terminal.
#
# Metro's port is WATCHER_PORT from .js.env (scripts/build.sh sources it and it
# wins over the shell), else $WATCHER_PORT, else 8081.
#
# Exit codes: 1 not running / bad env, 2 port conflict, 3 yarn missing or MCP query
# failed, 4 sidecar start timeout, 5 Metro stop refused, 6 Metro start timeout,
# 7 sidecar restarted by a supervisor, 64 usage.
#
# Env overrides: SPOTLIGHT_PORT (8969), SPOTLIGHT_VERSION (pinned below),
# SPOTLIGHT_LOG, SPOTLIGHT_STATUS_WINDOW (seconds, default 300), METRO_LOG.
# Written for bash 3.2 (macOS default) and Linux.
set -euo pipefail

PORT="${SPOTLIGHT_PORT:-8969}"
# Pinned on purpose: `yarn dlx` runs whatever it resolves, so do not float to latest.
VERSION="${SPOTLIGHT_VERSION:-4.12.1}"
LOG="${SPOTLIGHT_LOG:-${TMPDIR:-/tmp}/spotlight-sidecar.log}"
METRO_LOG="${METRO_LOG:-${TMPDIR:-/tmp}/spotlight-metro.log}"
STATUS_WINDOW="${SPOTLIGHT_STATUS_WINDOW:-300}"
UI_URL="http://localhost:${PORT}"
MCP_URL="http://127.0.0.1:${PORT}/mcp"
# Parses as a valid DSN but points at localhost, so nothing leaves the machine.
# Spotlight still receives every event: the SDK hands envelopes to Spotlight
# (`beforeEnvelope`) before it tries the transport.
THROWAWAY_DSN="https://spotlight@localhost/1"

repo_root() { git rev-parse --show-toplevel 2>/dev/null || pwd; }

healthy() { curl -fsS -m 3 -o /dev/null "http://127.0.0.1:${PORT}/health" 2>/dev/null; }

listener_pid() { lsof -nP -tiTCP:"${PORT}" -sTCP:LISTEN 2>/dev/null | head -n 1 || true; }

say() { printf '%s\n' "$*"; }

# Run a command in its own session so it outlives the caller. Agent shells kill
# the whole process group when a tool call ends, and a plain `&` or `nohup` child
# dies with it. macOS has no setsid(1), but perl ships with it.
detach() {
  if command -v setsid >/dev/null 2>&1; then
    setsid "$@"
  elif command -v perl >/dev/null 2>&1; then
    perl -MPOSIX -e 'POSIX::setsid(); exec { $ARGV[0] } @ARGV' -- "$@"
  else
    nohup "$@"
  fi
}

# ---- sidecar ---------------------------------------------------------------

start_sidecar() {
  if healthy; then
    say "sidecar: already running at ${UI_URL}"
    return 0
  fi

  local pid
  pid="$(listener_pid)"
  if [ -n "${pid}" ]; then
    say "ERROR: port ${PORT} is held by pid ${pid} ($(ps -o command= -p "${pid}" | cut -c1-80))" >&2
    say "       but /health does not answer. Stop it, or set SPOTLIGHT_PORT." >&2
    exit 2
  fi

  if ! command -v yarn >/dev/null 2>&1; then
    say "ERROR: yarn not found. This repo uses yarn only (never npx)." >&2
    exit 3
  fi

  say "sidecar: starting @spotlightjs/spotlight@${VERSION} on :${PORT} (log: ${LOG})"
  # Run from the repo root so yarn resolves the repo's pinned yarn version.
  # node-modules linker: Spotlight's dependency tree fails Yarn PnP's strict
  # resolution (missing @sentry/node peers), so do not rely on the repo default.
  # Redirect the whole subshell, not just the command inside it: the subshell
  # outlives this script, and one that inherits our stdout/stderr keeps a caller
  # that waits for pipe EOF (CI, `$(...)`, an agent harness) hanging.
  (cd "$(repo_root)" && YARN_NODE_LINKER=node-modules detach yarn dlx "@spotlightjs/spotlight@${VERSION}" --port "${PORT}") >"${LOG}" 2>&1 </dev/null &

  local i=0
  while [ "${i}" -lt 90 ]; do
    if healthy; then
      say "sidecar: up at ${UI_URL}"
      return 0
    fi
    i=$((i + 1))
    sleep 1
  done

  say "ERROR: sidecar did not become healthy within 90s. Last log lines:" >&2
  tail -n 15 "${LOG}" >&2 || true
  exit 4
}

# ---- Metro -----------------------------------------------------------------------

# The port `yarn watch:clean` will use: scripts/build.sh sources .js.env, whose
# WATCHER_PORT wins over the shell environment. There is deliberately no override:
# build.sh would ignore it and Expo would start on the .js.env port while this
# script waited on another.
resolve_metro_port() {
  local p
  p="$(get_env "$(repo_root)/.js.env" WATCHER_PORT)"
  printf '%s' "${p:-${WATCHER_PORT:-8081}}"
}

metro_pids() { lsof -nP -tiTCP:"${METRO_PORT}" -sTCP:LISTEN 2>/dev/null || true; }

metro_ready() {
  curl -fsS -m 3 "http://127.0.0.1:${METRO_PORT}/status" 2>/dev/null | grep -q 'packager-status:running'
}

# Stop the Metro listening on METRO_PORT. Refuses anything that is not this
# checkout's Metro: the command must contain the repo root (so another checkout's
# Expo server on the same port is left alone) and look like Metro. Same guardrail
# idea as `off`.
stop_metro() {
  local pids pid cmd root i
  pids="$(metro_pids)"
  [ -n "${pids}" ] || return 0
  root="$(repo_root)"

  for pid in ${pids}; do
    cmd="$(ps -o command= -p "${pid}" 2>/dev/null || true)"
    case "${cmd}" in
      *"${root}"*expo* | *"${root}"*metro* | *"${root}"*react-native*) ;;
      *)
        say "ERROR: pid ${pid} on :${METRO_PORT} is not this checkout's Metro ($(printf '%s' "${cmd}" | cut -c1-80)). Not killing it." >&2
        say "       Its command must contain ${root} and expo/metro/react-native. Free the port and re-run." >&2
        exit 5
        ;;
    esac
  done

  for pid in ${pids}; do
    say "metro: stopping pid ${pid} on :${METRO_PORT}"
    kill "${pid}" 2>/dev/null || true
  done

  i=0
  while [ -n "$(metro_pids)" ] && [ "${i}" -lt 15 ]; do
    i=$((i + 1))
    sleep 1
  done
  # Only force the pids verified above. Re-reading the listeners here could pick up
  # an unrelated process that took the port in the meantime.
  for pid in ${pids}; do
    if metro_pids | grep -qx "${pid}"; then
      kill -9 "${pid}" 2>/dev/null || true
    fi
  done
  sleep 1
  if [ -n "$(metro_pids)" ]; then
    say "ERROR: :${METRO_PORT} is still held after stopping Metro." >&2
    exit 5
  fi
}

# Stop this checkout's Metro on METRO_PORT, then `yarn watch:clean` from the repo
# root, in its own session so it survives the caller. The port must be free first: a second
# `yarn watch:clean` aborts on a busy port.
restart_metro() {
  if ! command -v yarn >/dev/null 2>&1; then
    say "ERROR: yarn not found. This repo uses yarn only (never npx)." >&2
    exit 3
  fi

  stop_metro

  say "metro: starting yarn watch:clean on :${METRO_PORT} (log: ${METRO_LOG})"
  # Same as the sidecar: redirect the subshell so it does not hold our pipes open.
  (cd "$(repo_root)" && detach yarn watch:clean) >"${METRO_LOG}" 2>&1 </dev/null &

  local i=0
  while [ "${i}" -lt 180 ]; do
    if metro_ready; then
      say "metro: up at http://localhost:${METRO_PORT} (clean cache)"
      return 0
    fi
    i=$((i + 1))
    sleep 1
  done

  say "ERROR: Metro did not report running within 180s. Last log lines:" >&2
  tail -n 15 "${METRO_LOG}" >&2 || true
  exit 6
}

# ---- app env (.js.env) -------------------------------------------------------

# NAME -> value without quotes or a trailing comment ("" when missing). Accepts
# `export NAME=v`, `NAME=v`, "v", 'v', and `v # comment`.
get_env() {
  local file="$1" name="$2" v
  [ -f "${file}" ] || return 0
  v="$(grep -E "^[[:space:]]*(export[[:space:]]+)?${name}=" "${file}" | tail -n 1 \
    | sed -E "s/^[[:space:]]*(export[[:space:]]+)?${name}=//" || true)"
  case "${v}" in
    \"*) v="${v#\"}"; v="${v%%\"*}" ;;
    \'*) v="${v#\'}"; v="${v%%\'*}" ;;
    *) v="${v%%[[:space:]]*}" ;;
  esac
  printf '%s' "${v}"
}

# NAME VALUE. Rewrites every `[export ]NAME=` line in place as `export NAME="VALUE"`
# (keeping a trailing `# comment`), or appends one. Keeps the file mode.
set_env() {
  local file="$1" name="$2" value="$3" tmp
  if grep -qE "^[[:space:]]*(export[[:space:]]+)?${name}=" "${file}"; then
    tmp="$(mktemp)"
    awk -v name="${name}" -v v="${value}" -v sq="'" '
      BEGIN { re = "^[ \t]*(export[ \t]+)?" name "=" }
      match($0, re) {
        rest = substr($0, RLENGTH + 1)
        q = substr(rest, 1, 1)
        if (q == "\"" || q == sq) {
          i = index(substr(rest, 2), q)
          after = (i > 0) ? substr(rest, i + 2) : ""
        } else {
          after = rest
          sub(/^[^ \t]*/, "", after)
        }
        tail = (after ~ /^[ \t]+#/) ? after : ""
        print "export " name "=\"" v "\"" tail
        next
      }
      { print }' "${file}" >"${tmp}"
    cat "${tmp}" >"${file}"
    rm -f "${tmp}"
  else
    printf '\nexport %s="%s"\n' "${name}" "${value}" >>"${file}"
  fi
}

ensure_app_env() {
  local root env_file changed=0
  root="$(repo_root)"
  env_file="${root}/.js.env"

  if [ ! -f "${env_file}" ]; then
    if [ -f "${root}/.js.env.example" ]; then
      cp "${root}/.js.env.example" "${env_file}"
      say "env: created .js.env from .js.env.example"
      changed=1
    else
      say "env: no .js.env and no .js.env.example here. Is this the metamask-mobile root?" >&2
      return 1
    fi
  fi

  if [ "$(get_env "${env_file}" SENTRY_SPOTLIGHT)" != "true" ]; then
    set_env "${env_file}" SENTRY_SPOTLIGHT true
    say "env: set SENTRY_SPOTLIGHT=true"
    changed=1
  else
    say "env: SENTRY_SPOTLIGHT=true already set"
  fi

  local dsn
  dsn="$(get_env "${env_file}" MM_SENTRY_DSN)"
  if [ -z "${dsn}" ]; then
    # setupSentry returns early without a DSN, so Spotlight would stay silent.
    set_env "${env_file}" MM_SENTRY_DSN "${THROWAWAY_DSN}"
    say "env: MM_SENTRY_DSN was empty; set a localhost-only throwaway DSN (events stay on this machine)"
    changed=1
  else
    say "env: MM_SENTRY_DSN set (host: $(printf '%s' "${dsn}" | sed -E 's#^[a-z]+://[^@]*@([^/]+)/.*#\1#')); events are ALSO sent to that Sentry project"
  fi

  ENV_CHANGED="${changed}"
}

# ---- Spotlight MCP over HTTP ---------------------------------------------------

# TOOL [JSON_ARGS] -> prints the tool's text output. Any failure prints a reason
# on stderr and returns non-zero, so callers can report it instead of dying silently.
mcp_call() {
  local tool="${1:-}" args="${2:-{\}}" resp code body raw
  case "${tool}" in
    "" | *[!a-z_]*) say "ERROR: invalid MCP tool name: '${tool}'" >&2; return 64 ;;
  esac
  if ! resp="$(curl -sS -m 30 -X POST "${MCP_URL}" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -w '\n%{http_code}' \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"${tool}\",\"arguments\":${args}}}" 2>&1)"; then
    say "ERROR: could not reach ${MCP_URL}: $(printf '%s' "${resp}" | head -n 1)" >&2
    return 1
  fi
  code="${resp##*$'\n'}"
  body="${resp%$'\n'*}"
  case "${code}" in
    2??) ;;
    *) say "ERROR: ${MCP_URL} answered HTTP ${code}: $(printf '%s' "${body}" | head -c 200)" >&2; return 1 ;;
  esac
  raw="$(printf '%s\n' "${body}" | sed -n 's/^data: //p')"
  [ -n "${raw}" ] || raw="${body}"
  if command -v python3 >/dev/null 2>&1; then
    printf '%s' "${raw}" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit("ERROR: could not parse the MCP response")
if "error" in d:
    sys.exit("ERROR: MCP error " + json.dumps(d["error"]))
print("\n".join(c.get("text", "") for c in d["result"].get("content", [])))'
  else
    printf '%s\n' "${raw}"
  fi
}

# ---- commands --------------------------------------------------------------------

open_ui() {
  # System browser on purpose: the Cursor in-app browser can render a blank gray
  # page for the Spotlight UI.
  case "$(uname -s)" in
    Darwin) open "${UI_URL}" || say "could not open a browser; open ${UI_URL} manually" ;;
    Linux) xdg-open "${UI_URL}" >/dev/null 2>&1 || say "open ${UI_URL} in a browser" ;;
    *) say "open ${UI_URL} in a browser" ;;
  esac
}

cmd_on() {
  local open_browser=1 force_metro=0 skip_metro=0 arg
  for arg in "$@"; do
    case "${arg}" in
      --no-open) open_browser=0 ;;
      --restart-metro) force_metro=1 ;;
      --no-metro) skip_metro=1 ;;
      *) say "unknown flag: ${arg} (try --help)" >&2; exit 64 ;;
    esac
  done
  if [ "${force_metro}" = 1 ] && [ "${skip_metro}" = 1 ]; then
    say "--restart-metro and --no-metro contradict each other" >&2
    exit 64
  fi

  ENV_CHANGED=0
  start_sidecar
  ensure_app_env || exit 1
  METRO_PORT="$(resolve_metro_port)"

  if [ "${open_browser}" = 1 ]; then open_ui; fi
  say "ui:   ${UI_URL}"
  say "mcp:  ${MCP_URL}  (tools: search_errors, search_logs, search_traces, get_traces)"

  # Env vars are inlined by Babel at bundle time, so a changed .js.env needs a
  # clean Metro restart. Only do it when something changed (or on request) so a
  # re-run never kills a healthy dev session.
  local metro_restarted=0
  if [ "${skip_metro}" = 0 ] && { [ "${force_metro}" = 1 ] || [ "${ENV_CHANGED}" = 1 ]; }; then
    restart_metro
    metro_restarted=1
  fi

  say ""
  say "Still needed for the app to connect (the sidecar cannot do these):"
  if [ "${metro_restarted}" = 1 ]; then
    say "  1. Fully relaunch the app so it loads the fresh bundle from the restarted Metro."
  elif [ "${ENV_CHANGED}" = 1 ]; then
    say "  1. Restart Metro with a clean cache (skipped by --no-metro). Env vars are inlined at bundle time."
    say "     Stop any Metro already on :${METRO_PORT}, then: yarn watch:clean"
    say "     Then fully relaunch the app."
  fi
  say "  - Metrics consent must be ON: Settings > Security and privacy > Participate in MetaMetrics."
  say "    Sentry reads consent at launch, so relaunch the app after turning it on."
  say "  - Use a __DEV__ build (Metro dev server). Release builds never forward to Spotlight."
  say "Verify with: $0 status"
}

cmd_status() {
  if ! healthy; then
    say "sidecar: NOT running on :${PORT}. Run: $0 on"
    exit 1
  fi

  local out traces errors earlier
  if ! out="$(mcp_call search_traces "{\"filters\":{\"timeWindow\":${STATUS_WINDOW},\"limit\":3}}" 2>&1)"; then
    say "sidecar: running at ${UI_URL}, but querying it failed. Cannot tell whether the app is connected." >&2
    say "  ${out}" >&2
    say "  Sidecar log: ${LOG}" >&2
    exit 3
  fi
  traces="$(printf '%s\n' "${out}" | head -n 1)"

  if ! out="$(mcp_call search_errors "{\"filters\":{\"timeWindow\":${STATUS_WINDOW},\"limit\":3}}" 2>&1)"; then
    say "sidecar: running at ${UI_URL}, but querying errors failed." >&2
    say "  ${out}" >&2
    say "  Sidecar log: ${LOG}" >&2
    exit 3
  fi
  errors="$(printf '%s\n' "${out}" | head -n 1)"

  say "sidecar: running at ${UI_URL}"
  say "traces (last ${STATUS_WINDOW}s): ${traces}"
  say "errors (last ${STATUS_WINDOW}s): ${errors}"
  case "${traces}" in
    "No traces found"*)
      earlier="$(mcp_call search_traces '{"filters":{"timeWindow":3600,"limit":1}}' 2>/dev/null | head -n 1 || true)"
      case "${earlier}" in
        "" | "No traces found"*)
          say "No traces yet. App not connected: consent off, app not relaunched on a Metro that has the current .js.env, or non-dev build."
          ;;
        *)
          say "No traces in the last ${STATUS_WINDOW}s, but earlier ones exist (last hour): the app connected before and has gone quiet. Use the app, or relaunch it."
          ;;
      esac
      ;;
    *) say "Connected: the app is sending events to Spotlight." ;;
  esac
}

# launchd jobs that could respawn the sidecar (macOS). Printed, never removed: this
# script did not create them.
supervisor_hint() {
  local labels
  command -v launchctl >/dev/null 2>&1 || return 0
  labels="$(launchctl list 2>/dev/null | awk '$3 ~ /spotlight/ && $3 !~ /^com\.apple\./ { print $3 }' || true)"
  if [ -n "${labels}" ]; then
    say "       launchd job(s) that may restart it: $(printf '%s' "${labels}" | tr '\n' ' ')" >&2
    say "       Remove one with: launchctl remove <label>" >&2
  fi
}

cmd_off() {
  local pid cmd i again
  pid="$(listener_pid)"
  if [ -z "${pid}" ]; then
    say "sidecar: not running"
    return 0
  fi
  cmd="$(ps -o command= -p "${pid}" || true)"
  # Match the package, not any path that happens to contain "spotlight": the dlx
  # install (`.../node_modules/@spotlightjs/...`) or an npx/global bin.
  case "${cmd}" in
    *@spotlightjs/* | */.bin/spotlight | */.bin/spotlight\ *) ;;
    *) say "ERROR: pid ${pid} on :${PORT} is not a Spotlight sidecar (${cmd}). Not killing it." >&2; exit 2 ;;
  esac

  kill "${pid}" 2>/dev/null || true
  # Wait for this pid to exit, not for the port to clear: a supervisor may already
  # have put a new listener on it.
  i=0
  while kill -0 "${pid}" 2>/dev/null && [ "${i}" -lt 10 ]; do
    i=$((i + 1))
    sleep 1
  done
  if kill -0 "${pid}" 2>/dev/null; then
    say "ERROR: pid ${pid} is still running 10s after SIGTERM." >&2
    exit 2
  fi

  # A supervisor (launchd KeepAlive, a process manager) respawns within a second or
  # two. Give it time, so "stopped" below is true rather than hopeful.
  sleep 3
  again="$(listener_pid)"
  if [ -n "${again}" ]; then
    say "ERROR: stopped pid ${pid}, but :${PORT} is listening again as pid ${again} (ppid $(ps -o ppid= -p "${again}" | tr -d ' ')). Something restarts it." >&2
    supervisor_hint
    exit 7
  fi
  say "sidecar: stopped (pid ${pid})"
}

main() {
  local cmd="${1:-on}"
  [ "$#" -gt 0 ] && shift
  case "${cmd}" in
    on) cmd_on "$@" ;;
    status) cmd_status ;;
    off) cmd_off ;;
    mcp)
      [ "$#" -ge 1 ] || { say "usage: $0 mcp <tool> [json-args]" >&2; exit 64; }
      mcp_call "$@"
      ;;
    -h | --help | help) awk 'NR > 1 && /^#/ { print; next } NR > 1 { exit }' "$0" ;;
    *) say "unknown command: ${cmd} (try --help)" >&2; exit 64 ;;
  esac
}

main "$@"
