#!/usr/bin/env bash
# upgrade-icp-cli.sh — keep the `icp` CLI and `ic-wasm` current.
#
# Checks the installed version of each tool against the latest release and
# either reports what is available (notify mode, the default) or upgrades it
# through the channel it was actually installed from (auto mode).
#
# Modes:
#   notify  print what is out of date and the exact upgrade command  (default)
#   auto    run that upgrade command
#
#   ICP_UPGRADE_MODE=auto|notify        or  --mode auto|notify
#
# The version probes cost about a second, which is a lot to pay at every single
# session start, so a successful check is stamped and not repeated for
# ICP_UPGRADE_CHECK_INTERVAL seconds (default 6h; 0 disables the throttle).
# --force, and any run from a terminal, check anyway.
#
# Design notes:
#   - Needs only curl and POSIX tools. No jq: the version probes are a GitHub
#     redirect and one small Homebrew JSON field, both readable with grep/awk.
#   - Never installs a tool that is not already present, and never upgrades a
#     tool it cannot identify the install channel for — guessing there would
#     leave two copies of the CLI on PATH shadowing each other.
#   - Exits 0 on every failure path. This runs at session start; a network
#     blip or a locked package manager must not block the session.
set -euo pipefail

MODE="${ICP_UPGRADE_MODE:-notify}"
INTERVAL="${ICP_UPGRADE_CHECK_INTERVAL:-21600}"
FORCE=0
# A human ran this by hand: answer them rather than the stamp.
if [ -t 1 ]; then FORCE=1; fi

while [ $# -gt 0 ]; do
  case "$1" in
    --mode) MODE="${2:-notify}"; shift 2 ;;
    --mode=*) MODE="${1#--mode=}"; shift ;;
    --force) FORCE=1; shift ;;
    *) shift ;;
  esac
done
case "$MODE" in
  auto|notify) ;;
  *) echo "[autoupgrade-icp-cli] unknown mode '$MODE' — using notify" >&2; MODE=notify ;;
esac

if ! command -v curl >/dev/null 2>&1; then
  echo "[autoupgrade-icp-cli] 'curl' not found — cannot check for updates" >&2
  exit 0
fi

# --- Throttle. The stamp holds the epoch second of the last check that actually
#     reached a release feed, so an offline run retries next session instead of
#     going quiet for the whole interval. ---
STAMP="${CLAUDE_PROJECT_DIR:-.}/.claude/.icp-upgrade-check"
CHECKED_OK=0
case "$INTERVAL" in ''|*[!0-9]*) INTERVAL=21600 ;; esac
if [ "$FORCE" -eq 0 ] && [ "$INTERVAL" -gt 0 ] && [ -f "$STAMP" ]; then
  last="$(cat "$STAMP" 2>/dev/null || echo 0)"
  case "$last" in ''|*[!0-9]*) last=0 ;; esac
  now="$(date +%s 2>/dev/null || echo 0)"
  if [ "$now" -gt 0 ] && [ $((now - last)) -lt "$INTERVAL" ]; then
    exit 0
  fi
fi

NOTES=""   # lines to surface to the user, joined with \n at the end
# Notes end up inside a JSON string, so drop the two characters that would
# break it. Nothing this script reports legitimately contains either.
note() {
  line="$(printf '%s' "$1" | tr -d '"\\' | tr '\n' ' ')"
  NOTES="${NOTES:+$NOTES\\n}$line"
}

# --- Resolve a symlink chain without readlink -f (absent on older macOS). ---
resolve_path() {
  p="$1"; n=0
  while [ -L "$p" ] && [ "$n" -lt 20 ]; do
    t="$(readlink "$p")"
    case "$t" in
      /*) p="$t" ;;
      *)  p="$(dirname "$p")/$t" ;;
    esac
    n=$((n + 1))
  done
  printf '%s\n' "$p"
}

# --- True when $1 is an older version than $2. Compares dot-separated numeric
#     components; a pre-release suffix (1.6.0-beta.1) compares as its release
#     (1.6.0), so running a beta never nags you back down to the release. ---
version_lt() {
  awk -v a="$1" -v b="$2" '
    function norm(v) { sub(/^v/, "", v); sub(/[-+].*$/, "", v); return v }
    BEGIN {
      na = split(norm(a), A, "."); nb = split(norm(b), B, ".")
      n = (na > nb ? na : nb)
      for (i = 1; i <= n; i++) {
        x = (i <= na ? A[i] + 0 : 0); y = (i <= nb ? B[i] + 0 : 0)
        if (x < y) exit 0
        if (x > y) exit 1
      }
      exit 1
    }'
}

# --- Installed version. Both tools print "<name> <version>" to stdout. ---
installed_version() {
  command -v "$1" >/dev/null 2>&1 || return 1
  "$1" --version 2>/dev/null | awk 'NR==1 {print $2}'
}

# --- Which channel a tool came from, inferred from where its binary really
#     lives. This decides the upgrade command, so an unrecognised location
#     stays "unknown" rather than being guessed at. ---
detect_channel() {   # $1 = binary name, $2 = cargo-dist app name
  bin="$(command -v "$1" 2>/dev/null)" || return 1
  real="$(resolve_path "$bin")"
  case "$real" in
    */node_modules/@icp-sdk/*) printf 'npm\n'; return 0 ;;
    */Cellar/*)                printf 'brew\n'; return 0 ;;
  esac
  # The shell installer (cargo-dist) leaves a receipt naming the install it owns.
  if [ -f "${XDG_CONFIG_HOME:-$HOME/.config}/$2/$2-receipt.json" ]; then
    printf 'shell\n'; return 0
  fi
  printf 'unknown\n'
}

# --- Latest version per channel. npm and the shell installer both track the
#     GitHub release, and its /releases/latest URL redirects to the tag — one
#     HEAD request, no API token and no rate limit. Homebrew is asked
#     separately because its formula can trail the release by a day or two,
#     and nagging about a version `brew upgrade` cannot yet install is noise. ---
latest_from_github() {   # $1 = repo (dfinity/icp-cli)
  url="$(curl -fsSLI -o /dev/null -w '%{url_effective}' --max-time 10 \
    "https://github.com/$1/releases/latest" 2>/dev/null)" || return 1
  case "$url" in
    */releases/tag/*) v="${url##*/tag/}"; printf '%s\n' "${v#v}" ;;
    *) return 1 ;;
  esac
}

latest_from_brew() {     # $1 = formula name
  curl -fsSL --max-time 10 "https://formulae.brew.sh/api/formula/$1.json" 2>/dev/null |
    grep -o '"stable":"[^"]*"' | head -1 | cut -d'"' -f4
}

# --- Run an upgrade, keeping its chatter off stdout: stdout carries the hook's
#     JSON and nothing else. ---
run_upgrade() {
  if "$@" >&2 2>&1; then return 0; fi
  return 1
}

# --- One tool, end to end. ---
check_tool() {           # $1 = binary  $2 = cargo-dist app / brew formula  $3 = npm package  $4 = repo
  bin="$1"; app="$2"; pkg="$3"; repo="$4"

  if ! current="$(installed_version "$bin")" || [ -z "$current" ]; then
    # Absent, or present but not answering --version. Installing something the
    # user never had is not an upgrade, so say so instead of acting.
    if command -v "$bin" >/dev/null 2>&1; then
      echo "[autoupgrade-icp-cli] '$bin' did not report a version — skipping" >&2
    else
      note "$bin is not installed. Install it with: npm install -g $pkg"
    fi
    return 0
  fi

  channel="$(detect_channel "$bin" "$app")"

  if [ "$channel" = "brew" ]; then
    latest="$(latest_from_brew "$app" || true)"
  else
    latest="$(latest_from_github "$repo" || true)"
  fi
  if [ -z "$latest" ]; then
    echo "[autoupgrade-icp-cli] could not determine the latest $bin version — skipping" >&2
    return 0
  fi
  CHECKED_OK=1

  version_lt "$current" "$latest" || return 0

  case "$channel" in
    npm)
      cmd_desc="npm install -g $pkg@latest"
      set -- npm install -g "$pkg@latest"
      # A global prefix owned by root turns the upgrade into a sudo password
      # prompt with nothing to type into it, which would hang session start.
      root="$(npm root -g 2>/dev/null || true)"
      if [ -n "$root" ] && [ ! -w "$root" ]; then
        note "$bin $current -> $latest available. Run: sudo $cmd_desc (the global npm prefix is not writable, so this is not upgraded automatically)"
        return 0
      fi
      ;;
    brew)
      cmd_desc="brew upgrade $app"
      set -- brew upgrade "$app"
      ;;
    shell)
      if command -v "$app-update" >/dev/null 2>&1; then
        cmd_desc="$app-update"
        set -- "$app-update"
      else
        note "$bin $current -> $latest available. Re-run the installer: curl --proto '=https' --tlsv1.2 -LsSf https://github.com/$repo/releases/latest/download/$app-installer.sh | sh"
        return 0
      fi
      ;;
    *)
      note "$bin $current -> $latest available, but its install channel is unrecognised ($(command -v "$bin")). Upgrade it the way you installed it: https://github.com/$repo/releases/latest"
      return 0
      ;;
  esac

  if [ "$MODE" != "auto" ]; then
    note "$bin $current -> $latest available. Run: $cmd_desc"
    return 0
  fi

  if run_upgrade "$@"; then
    new="$(installed_version "$bin" || true)"
    if [ -n "$new" ] && ! version_lt "$new" "$latest"; then
      note "$bin upgraded $current -> $new"
    else
      # The command succeeded but the binary on PATH did not move. Usually a
      # second copy from another channel is shadowing the one just upgraded.
      note "$bin: ran '$cmd_desc' but PATH still resolves to ${new:-$current}. Check for a second copy of $bin on PATH."
    fi
  else
    note "$bin $current -> $latest available. '$cmd_desc' failed — run it manually to see why."
  fi
}

check_tool icp     icp-cli @icp-sdk/icp-cli dfinity/icp-cli
check_tool ic-wasm ic-wasm @icp-sdk/ic-wasm dfinity/ic-wasm

# Only stamp a check that actually saw a release feed.
if [ "$CHECKED_OK" -eq 1 ] && [ "$INTERVAL" -gt 0 ]; then
  mkdir -p "$(dirname "$STAMP")" 2>/dev/null &&
    date +%s > "$STAMP" 2>/dev/null || true
fi

[ -n "$NOTES" ] || exit 0

# --- Report. On a terminal a human is reading, so print plain text. Under a
#     SessionStart hook, plain stdout only reaches Claude and is never shown to
#     the user, so emit one JSON object instead:
#       systemMessage      -> shown to the USER as a system notice
#       additionalContext  -> given to Claude, so it knows the CLI version it
#                             is about to generate commands for
if [ -t 1 ]; then
  printf '[autoupgrade-icp-cli]\n%b\n' "$NOTES"
else
  printf '{"systemMessage":"[autoupgrade-icp-cli]\\n%s","hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"icp toolchain status: %s"}}\n' \
    "$NOTES" "$NOTES"
fi
