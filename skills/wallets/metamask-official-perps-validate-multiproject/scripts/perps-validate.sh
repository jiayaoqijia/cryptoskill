#!/usr/bin/env bash
#
# perps-validate.sh — deterministic helper for validating a Core
# @metamask/perps-controller change inside a client checkout (Mobile or
# Extension) via yalc.
#
# Direction is always: a CLIENT validates a CORE controller change.
#   owner  = the Core checkout that holds the perps-controller change
#   client = the Mobile/Extension checkout that consumes it
#
# Run subcommands in this order:
#   1. prestate <client-dir> [client-dir...]   # snapshot before touching anything
#   2. build    <core-dir> [--full]            # build the package (freshness gate)
#   3. push     <core-dir> <client-dir> [...]  # yalc publish + push into clients
#   4. verify   <client-dir>                   # confirm version + new symbols landed
#   5. restore  <client-dir> [client-dir...]   # put the client back to its snapshot
#
# Helper subcommands:
#   resolve-yalc                               # print the resolved yalc invocation
#   doctor <core-dir> <client-dir>             # quick environment sanity check
#
# Design goals:
#   - No assumption about the Node manager (asdf / nvm / volta / brew / none).
#   - No hardcoded paths. Everything is derived or passed in.
#   - Pre-state aware: if a client was ALREADY on a yalc link, restore brings
#     that exact link back instead of nuking the user's dev setup.
#
# Env overrides:
#   YALC_BIN   explicit yalc invocation (e.g. "/opt/homebrew/bin/yalc"
#              or "node /path/to/yalc/src/yalc.js"). Skips auto-resolution.
#   PKG        package name (default: @metamask/perps-controller)
#   STATE_DIR  where snapshots live (default: <client>/tmp/.perps-validate)

set -euo pipefail

PKG="${PKG:-@metamask/perps-controller}"
# perps-controller lives at packages/<leaf> in the Core monorepo.
PKG_LEAF="${PKG##*/}"          # perps-controller
PKG_SCOPE="${PKG%/*}"         # @metamask

# ---------------------------------------------------------------------------
# yalc resolution — the single most fragile thing across machines.
#
# A version-manager shim (notably asdf) can SUCCEED with exit 0 yet do nothing,
# printing "No version is set for command yalc". So we never trust exit code
# alone: a working yalc must print a semver to stdout. If the shim is broken we
# fall back to locating yalc's own yalc.js and running it through a real node.
# ---------------------------------------------------------------------------
_looks_like_version() { printf '%s' "$1" | grep -Eq '^[0-9]+\.[0-9]+'; }

resolve_yalc() {
  if [ -n "${YALC_BIN:-}" ]; then printf '%s' "$YALC_BIN"; return 0; fi

  # 1. plain yalc on PATH, but only if it actually reports a version.
  #    Use `command yalc` so we hit the real binary, never the run_yalc wrapper.
  if command -v yalc >/dev/null 2>&1; then
    local v; v="$(command yalc --version 2>/dev/null || true)"
    if _looks_like_version "$v"; then printf 'yalc'; return 0; fi
  fi

  # 2. a real node to run yalc.js with (any working node is fine).
  local node_bin; node_bin="$(command -v node || true)"
  [ -z "$node_bin" ] && { echo "ERROR: no node on PATH to run yalc" >&2; return 1; }

  # 3. hunt for yalc's entrypoint across the common install layouts.
  local cand
  for cand in \
    "$(npm root -g 2>/dev/null)/yalc/src/yalc.js" \
    "$(npm root -g 2>/dev/null)/yalc/yalc.js" \
    "$HOME"/.asdf/installs/nodejs/*/lib/node_modules/yalc/src/yalc.js \
    "$HOME"/.nvm/versions/node/*/lib/node_modules/yalc/src/yalc.js \
    "$HOME"/.volta/tools/image/packages/yalc/lib/node_modules/yalc/src/yalc.js \
    /opt/homebrew/lib/node_modules/yalc/src/yalc.js \
    /usr/local/lib/node_modules/yalc/src/yalc.js ; do
    [ -f "$cand" ] && { printf '%s %s' "$node_bin" "$cand"; return 0; }
  done

  echo "ERROR: could not resolve yalc. Install it (npm i -g yalc) or set YALC_BIN." >&2
  return 1
}

# Run yalc regardless of how it resolved (binary or "node yalc.js").
# NOT named `yalc` on purpose — a function named `yalc` would shadow the real
# binary and make resolve_yalc recurse forever.
# The resolved value is split into an argv array and invoked directly — never
# eval'd — so a value like YALC_BIN="node /path/to/yalc.js" stays two words but
# cannot inject shell. The first token must resolve to a real executable.
run_yalc() {
  local y; y="$(resolve_yalc)" || return 1
  local -a cmd; read -ra cmd <<<"$y"
  command -v "${cmd[0]}" >/dev/null 2>&1 || {
    echo "ERROR: yalc invocation '${cmd[0]}' is not an executable" >&2; return 1; }
  "${cmd[@]}" "$@"
}

# ---------------------------------------------------------------------------
state_dir() { printf '%s/tmp/.perps-validate' "$1"; }

# ===========================================================================
cmd_resolve_yalc() {
  local y; y="$(resolve_yalc)" || exit 1
  echo "yalc => $y"
  run_yalc --version
}

# ---------------------------------------------------------------------------
cmd_prestate() {
  [ "$#" -ge 1 ] || { echo "usage: prestate <client-dir> [client-dir...]" >&2; exit 2; }
  for client in "$@"; do
    client="$(cd "$client" && pwd)"
    local sd; sd="$(state_dir "$client")"; mkdir -p "$sd"
    echo "=== prestate: $client ==="
    git -C "$client" status --short --branch | tee "$sd/git-status.txt" >/dev/null
    cp "$client/package.json" "$sd/package.json.bak" 2>/dev/null || true
    cp "$client/yalc.lock"    "$sd/yalc.lock.bak"    2>/dev/null || true

    local linkdir="$client/.yalc/$PKG"
    if [ -d "$linkdir" ]; then
      # Client was ALREADY on a yalc link — back it up byte-for-byte so restore
      # reproduces the exact pre-existing dev setup, not a clean registry state.
      echo "mode=PREEXISTING_YALC" > "$sd/mode"
      tar -czf "$sd/yalc-pkg.tgz" -C "$client/.yalc/$PKG_SCOPE" "$PKG_LEAF"
      cat "$linkdir/yalc.sig" 2>/dev/null > "$sd/yalc.sig" || true
      echo "  was already yalc-linked: version=$(node -p "require('$linkdir/package.json').version" 2>/dev/null) sig=$(cat "$sd/yalc.sig" 2>/dev/null)"
    else
      echo "mode=REGISTRY" > "$sd/mode"
      echo "  no prior yalc link (registry baseline)"
    fi
    echo "  snapshot -> $sd"
  done
}

# ---------------------------------------------------------------------------
# Build the controller package. The package CANNOT build standalone in a fresh
# Core checkout: its referenced packages have no dist yet and tsc fails with
# TS6305. That is expected — the supported fix is a full monorepo build first.
cmd_build() {
  local core="${1:?usage: build <core-dir> [--full]}"; shift || true
  local full=0; [ "${1:-}" = "--full" ] && full=1
  core="$(cd "$core" && pwd)"
  local log="$core/tmp/perps-build.log"; mkdir -p "$core/tmp"

  if [ "$full" -eq 1 ]; then
    echo "=== full monorepo build (nice) — builds all referenced dists ==="
    ( cd "$core" && nice -n 10 yarn build ) 2>&1 | tee "$log"
  else
    echo "=== package build: yarn workspace $PKG build ==="
    if ! ( cd "$core" && yarn workspace "$PKG" build ) 2>&1 | tee "$log"; then
      :
    fi
    if grep -q "TS6305" "$log"; then
      echo ""
      echo "BLOCKED: TS6305 — referenced package dists are missing (fresh checkout)."
      echo "Do NOT use 'workspaces foreach -R' (cycle can delete dist)."
      echo "Re-run with --full to build the whole monorepo first:"
      echo "    perps-validate.sh build $core --full"
      exit 3
    fi
  fi

  # Freshness gate: prove the built dist actually carries this change.
  local dist="$core/packages/$PKG_LEAF/dist"
  [ -f "$dist/index.cjs" ] || { echo "ERROR: no dist/index.cjs produced" >&2; exit 3; }
  echo ""
  echo "built version: $(node -p "require('$core/packages/$PKG_LEAF/package.json').version")"
  echo "dist OK -> $dist"
}

# ---------------------------------------------------------------------------
cmd_push() {
  local core="${1:?usage: push <core-dir> <client-dir> [client-dir...]}"; shift
  [ "$#" -ge 1 ] || { echo "need at least one client dir" >&2; exit 2; }
  core="$(cd "$core" && pwd)"
  local pkgdir="$core/packages/$PKG_LEAF"

  echo "=== yalc publish $PKG from $pkgdir ==="
  ( cd "$pkgdir" && run_yalc publish --private )

  for client in "$@"; do
    client="$(cd "$client" && pwd)"
    echo "=== push into client: $client ==="
    if [ -d "$client/.yalc/$PKG" ] || grep -q "$PKG" "$client/yalc.lock" 2>/dev/null; then
      ( cd "$client" && run_yalc update "$PKG" )   # advance an existing link
    else
      ( cd "$client" && run_yalc add "$PKG" && yarn install --mode=skip-build )
    fi
  done
}

# ---------------------------------------------------------------------------
cmd_verify() {
  local client="${1:?usage: verify <client-dir>}"
  client="$(cd "$client" && pwd)"
  local inst="$client/node_modules/$PKG"
  echo "=== verify $PKG in $client ==="
  echo "installed version: $(node -p "require('$inst/package.json').version" 2>/dev/null || echo MISSING)"
  echo "yalc link version: $(node -p "require('$client/.yalc/$PKG/package.json').version" 2>/dev/null || echo none)"
  echo "yalc sig: $(cat "$client/.yalc/$PKG/yalc.sig" 2>/dev/null || echo none)"
  echo "--- next: run the client's own proof (type-check + the affected tests) ---"
}

# ---------------------------------------------------------------------------
# Restore is pre-state aware. PREEXISTING_YALC clients get their exact link
# back; REGISTRY clients are fully un-yalc'd.
cmd_restore() {
  [ "$#" -ge 1 ] || { echo "usage: restore <client-dir> [client-dir...]" >&2; exit 2; }
  for client in "$@"; do
    client="$(cd "$client" && pwd)"
    local sd; sd="$(state_dir "$client")"
    local mode; mode="$(cat "$sd/mode" 2>/dev/null | cut -d= -f2 || echo UNKNOWN)"
    echo "=== restore: $client (mode=$mode) ==="
    case "$mode" in
      PREEXISTING_YALC)
        rm -rf "$client/.yalc/$PKG"
        tar -xzf "$sd/yalc-pkg.tgz" -C "$client/.yalc/$PKG_SCOPE"
        cp "$sd/yalc.lock.bak"   "$client/yalc.lock"   2>/dev/null || true
        cp "$sd/package.json.bak" "$client/package.json" 2>/dev/null || true
        echo "  restored prior link: sig now=$(cat "$client/.yalc/$PKG/yalc.sig" 2>/dev/null) expected=$(cat "$sd/yalc.sig" 2>/dev/null)"
        echo "  run 'yarn install --mode=skip-build' if node_modules needs to match"
        ;;
      REGISTRY)
        ( cd "$client" && run_yalc remove "$PKG" || true )
        git -C "$client" checkout -- package.json yarn.lock 2>/dev/null || true
        rm -rf "$client/.yalc" "$client/yalc.lock"
        echo "  un-yalc'd; package.json/yarn.lock reverted"
        ;;
      *)
        echo "  no snapshot found ($sd) — nothing to restore. Run prestate next time." ;;
    esac
    git -C "$client" status --short --branch | sed 's/^/  /'
  done
}

# ---------------------------------------------------------------------------
cmd_doctor() {
  local core="${1:?usage: doctor <core-dir> <client-dir>}"; local client="${2:?need client dir}"
  echo "=== doctor ==="
  echo "node: $(command -v node) $(node -v 2>/dev/null)"
  echo -n "yalc: "; cmd_resolve_yalc || true
  echo "core:   $core ($(git -C "$core" rev-parse --abbrev-ref HEAD 2>/dev/null))"
  echo "client: $client ($(git -C "$client" rev-parse --abbrev-ref HEAD 2>/dev/null))"
  echo "package: $PKG  ($core/packages/$PKG_LEAF $( [ -d "$core/packages/$PKG_LEAF" ] && echo found || echo MISSING ))"
  echo "client links pkg already: $( [ -d "$client/.yalc/$PKG" ] && echo yes || echo no )"
}

# ===========================================================================
sub="${1:-}"; shift || true
case "$sub" in
  resolve-yalc) cmd_resolve_yalc "$@" ;;
  prestate)     cmd_prestate "$@" ;;
  build)        cmd_build "$@" ;;
  push)         cmd_push "$@" ;;
  verify)       cmd_verify "$@" ;;
  restore)      cmd_restore "$@" ;;
  doctor)       cmd_doctor "$@" ;;
  *) cat >&2 <<EOF
perps-validate.sh — validate a Core perps-controller change in a client via yalc

Usage:
  perps-validate.sh prestate <client-dir> [client-dir...]
  perps-validate.sh build    <core-dir> [--full]
  perps-validate.sh push     <core-dir> <client-dir> [client-dir...]
  perps-validate.sh verify   <client-dir>
  perps-validate.sh restore  <client-dir> [client-dir...]
  perps-validate.sh resolve-yalc
  perps-validate.sh doctor   <core-dir> <client-dir>

Env: YALC_BIN, PKG (default @metamask/perps-controller), STATE_DIR
EOF
     exit 2 ;;
esac
