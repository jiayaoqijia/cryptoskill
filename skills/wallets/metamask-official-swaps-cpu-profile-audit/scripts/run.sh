#!/usr/bin/env bash
#
# run.sh — one-shot runner for the swaps-cpu-profile-audit skill
# (domains/swaps/skills/swaps-cpu-profile-audit) against metamask-mobile.
#
# This script itself lives in the skill's own scripts/ directory (alongside
# analyze-cpuprofile.cjs). Everything it EXTRACTS, CONVERTS, or WRITES —
# staged input, extracted archives, the *-converted.json, the final Markdown
# report — ends up under a throwaway run folder created *inside the
# target repo* (not the OS tmp directory). That run folder, and everything
# under it, is removed automatically when the script exits, whether it
# succeeds, fails, or is interrupted — nothing is left on disk afterwards.
# (The profiler CLI has no output-path flag: it always writes its converted
# JSON into the process cwd, i.e. the repo root, so this script moves that
# file into the run folder immediately after conversion.)
#
# Why not the OS tmp directory: routing the working folder through
# $TMPDIR/os.tmpdir() and then calling `yarn --cwd <repo> ...` from inside it
# made Corepack resolve the wrong Yarn version — Corepack picks the pinned
# version from the `packageManager` field by walking up from the shell's
# *actual* cwd at invocation time, not from `--cwd`, so running from a tmp
# folder with no package.json in its ancestry made it fall back to whatever
# Corepack/Yarn happened to be active globally instead of the repo's pinned
# version. Anchoring the run folder inside the repo (and always invoking
# `yarn` with the repo itself as cwd) avoids that entirely.
#
# Usage:
#   run.sh --repo <path-to-metamask-mobile> --profile <path> [--sourcemaps <path>]
#          [--scope <substring>] [--top <n>] [--context-min-pct <n>]
#          [--trigger-min-pct <n>] [--swaps-only]
#
# --scope, --context-min-pct, --trigger-min-pct and --swaps-only are forwarded to
# analyze-cpuprofile.cjs untouched, and omitted entirely when not given so the
# analyzer applies its own defaults (notably its full list of swaps-owned
# paths, which is wider than the Bridge screen tree alone).
#
# <path> for --profile can be:
#   - a raw .cpuprofile
#   - an already-converted *-converted.json
#   - a .zip/.tar/.tar.gz archive containing one of the above (it will be
#     extracted into the run folder first)
#   - any of the above renamed to a non-standard extension (e.g.
#     `sampling-profiler-trace123.cpuprofile.txt`, from a chat tool that only
#     allows attaching `.txt`) — if no file matches the expected extensions,
#     the script sniffs each staged file's JSON *content* to tell a
#     converted trace (JSON array) from a raw Hermes capture (JSON object
#     with `samples` + `stackFrames`), regardless of its name
#
# <path> for --sourcemaps (optional) can be:
#   - the source map file itself (index.js.map / index.android.bundle.map)
#   - a directory containing one of those
#   - a .zip archive of a sourcemaps CI artifact (it will be extracted into
#     the run folder first)
# In every case this script resolves it down to a single .map FILE before
# calling the profiler CLI, which JSON-parses whatever it is handed and so
# cannot take a directory.
#
# All intermediate and output files are written under a per-run subdirectory
# created inside the repo, e.g.:
#   <repo>/.mms-swaps-cpu-audit-run.XXXXXX/
# and deleted automatically (via an EXIT trap) before this script returns.
#
set -euo pipefail

REPO=""
PROFILE=""
SOURCEMAPS=""
TOP="40"
# Collected as an array so unset options are simply not forwarded, leaving the
# analyzer's own defaults in charge.
ANALYZER_OPTS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --profile) PROFILE="$2"; shift 2 ;;
    --sourcemaps) SOURCEMAPS="$2"; shift 2 ;;
    --scope) ANALYZER_OPTS+=(--scope "$2"); shift 2 ;;
    --context-min-pct) ANALYZER_OPTS+=(--context-min-pct "$2"); shift 2 ;;
    --trigger-min-pct) ANALYZER_OPTS+=(--trigger-min-pct "$2"); shift 2 ;;
    --swaps-only) ANALYZER_OPTS+=(--swaps-only); shift ;;
    --top) TOP="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,60p' "$0"
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [ -z "$REPO" ] || [ -z "$PROFILE" ]; then
  echo "Usage: run.sh --repo <path-to-metamask-mobile> --profile <path> [--sourcemaps <path>] [--scope <substring>] [--top <n>] [--context-min-pct <n>] [--trigger-min-pct <n>] [--swaps-only]" >&2
  exit 1
fi

if [ ! -d "$REPO" ]; then
  echo "No such repo directory: $REPO" >&2
  exit 1
fi
if [ ! -e "$PROFILE" ]; then
  echo "No such profile/archive: $PROFILE" >&2
  exit 1
fi
REPO="$(cd "$REPO" && pwd)"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

RUNDIR="$(mktemp -d "$REPO/.mms-swaps-cpu-audit-run.XXXXXX")"
cleanup() {
  rm -rf "$RUNDIR"
}
trap cleanup EXIT
mkdir -p "$RUNDIR/input" "$RUNDIR/sourcemaps"
echo "Working directory (removed automatically when this script exits): $RUNDIR" >&2

# --- Stage the profile into the run folder ----------------------------------
case "$PROFILE" in
  *.zip)
    unzip -q "$PROFILE" -d "$RUNDIR/input"
    ;;
  *.tar.gz|*.tgz)
    tar -xzf "$PROFILE" -C "$RUNDIR/input"
    ;;
  *.tar)
    tar -xf "$PROFILE" -C "$RUNDIR/input"
    ;;
  *)
    cp "$PROFILE" "$RUNDIR/input/"
    ;;
esac

# --- Stage sourcemaps (optional) into the run folder ------------------------
if [ -n "$SOURCEMAPS" ]; then
  if [ -d "$SOURCEMAPS" ]; then
    cp -R "$SOURCEMAPS"/. "$RUNDIR/sourcemaps/"
  else
    case "$SOURCEMAPS" in
      *.zip) unzip -q "$SOURCEMAPS" -d "$RUNDIR/sourcemaps" ;;
      *.tar.gz|*.tgz) tar -xzf "$SOURCEMAPS" -C "$RUNDIR/sourcemaps" ;;
      *.tar) tar -xf "$SOURCEMAPS" -C "$RUNDIR/sourcemaps" ;;
      *) cp "$SOURCEMAPS" "$RUNDIR/sourcemaps/" ;;
    esac
  fi
fi

# --- Locate (or produce) the converted JSON ---------------------------------
CONVERTED="$(find "$RUNDIR/input" -iname '*-converted.json' -print -quit)"
RAW_CPUPROFILE="$(find "$RUNDIR/input" -iname '*.cpuprofile' -print -quit)"
RAW_JSON="$(find "$RUNDIR/input" -iname '*.json' ! -iname '*-converted.json' -print -quit)"

# Extension-based detection above misses files whose real extension was
# stripped or replaced (commonly `.cpuprofile.txt` / `.json.txt`, e.g. from a
# chat tool that only allows attaching `.txt`). Fall back to sniffing file
# *content*: a converted trace is a JSON array of B/E duration events; a raw
# Hermes capture is a JSON object with `samples` + `stackFrames`. This is the
# same shape check analyze-cpuprofile.cjs's loadProfile() already does, just
# performed here first so we know which staged file to hand it when the
# filename itself gives no hint.
if [ -z "$CONVERTED" ] && [ -z "$RAW_CPUPROFILE" ] && [ -z "$RAW_JSON" ]; then
  SNIFFED="$(node -e '
    const fs = require("fs");
    const path = require("path");
    const dir = process.argv[1];
    for (const entry of fs.readdirSync(dir)) {
      const p = path.join(dir, entry);
      if (!fs.statSync(p).isFile()) continue;
      let data;
      try {
        data = JSON.parse(fs.readFileSync(p, "utf8"));
      } catch {
        continue;
      }
      if (Array.isArray(data)) {
        process.stdout.write(p + "\tconverted\n");
        break;
      }
      if (data && Array.isArray(data.samples) && data.stackFrames) {
        process.stdout.write(p + "\traw\n");
        break;
      }
    }
  ' "$RUNDIR/input")"
  if [ -n "$SNIFFED" ]; then
    SNIFFED_PATH="${SNIFFED%%$'\t'*}"
    SNIFFED_KIND="${SNIFFED##*$'\t'}"
    echo "No file matched by extension; sniffed content of $SNIFFED_PATH as a $SNIFFED_KIND profile." >&2
    if [ "$SNIFFED_KIND" = "converted" ]; then
      CONVERTED="$SNIFFED_PATH"
    else
      RAW_CPUPROFILE="$SNIFFED_PATH"
    fi
  fi
fi

if [ -z "$CONVERTED" ] && [ -n "$RAW_CPUPROFILE" ]; then
  # --sourcemap-path must point at the source map FILE, not at a directory:
  # the transformer behind the CLI does readFile() + JSON.parse() on it, so a
  # directory (such as the one we just unzipped a CI artifact into) fails with
  # EISDIR. Pick the map out of whatever was staged.
  SOURCEMAP_FILE=""
  if [ -n "$SOURCEMAPS" ]; then
    for NAME in index.js.map index.android.bundle.map; do
      SOURCEMAP_FILE="$(find "$RUNDIR/sourcemaps" -type f -name "$NAME" -print -quit)"
      if [ -n "$SOURCEMAP_FILE" ]; then break; fi
    done
    if [ -z "$SOURCEMAP_FILE" ]; then
      SOURCEMAP_FILE="$(find "$RUNDIR/sourcemaps" -type f -name '*.map' -print -quit)"
    fi
    if [ -n "$SOURCEMAP_FILE" ]; then
      echo "Using source map: $SOURCEMAP_FILE" >&2
    else
      echo "WARNING: --sourcemaps was given but contains no .map file (expected index.js.map or index.android.bundle.map)." >&2
    fi
  fi

  # The CLI has no --output/--dstPath flag — it always writes
  # <profile-basename>-converted.json into the *process cwd*, and that cwd has
  # to be the repo so Corepack resolves the pinned Yarn version (see the
  # header comment). So predict the name and move the result into the run
  # folder afterwards, keeping the repo clean.
  CONVERTED_NAME="$(basename "$RAW_CPUPROFILE")"
  CONVERTED_NAME="${CONVERTED_NAME%.cpuprofile}-converted.json"
  echo "Converting raw .cpuprofile via yarn react-native-release-profiler..." >&2
  if [ -n "$SOURCEMAP_FILE" ]; then
    ( cd "$REPO" && yarn --cwd "$REPO" react-native-release-profiler --local "$RAW_CPUPROFILE" --sourcemap-path "$SOURCEMAP_FILE" )
  else
    echo "WARNING: converting without source maps — frames stay at the minified-bundle level, so nothing resolves to a real file path and the ownership/area columns collapse to \"unknown\"." >&2
    # With no --sourcemap-path, the CLI tries to *invent* one: it looks for an
    # Android debug build map and otherwise downloads `/index.map` from a
    # running Metro server on --port (default 8081). A Metro dev-bundle map
    # cannot symbolicate a release Hermes capture — it either crashes the
    # transformer or produces confidently wrong attributions — so point --port
    # at a port nothing listens on. The fetch then fails, and the CLI
    # continues mapless, which is the honest outcome here.
    ( cd "$REPO" && yarn --cwd "$REPO" react-native-release-profiler --local "$RAW_CPUPROFILE" --port 0 )
  fi
  if [ -f "$REPO/$CONVERTED_NAME" ]; then
    mv "$REPO/$CONVERTED_NAME" "$RUNDIR/input/"
  fi
  CONVERTED="$(find "$RUNDIR/input" -iname '*-converted.json' -print -quit)"
fi

if [ -z "$CONVERTED" ] && [ -n "$RAW_JSON" ]; then
  # Already-converted JSON that just doesn't match the *-converted.json naming.
  CONVERTED="$RAW_JSON"
fi

if [ -z "$CONVERTED" ]; then
  echo "Could not find a converted JSON, raw .cpuprofile, or usable JSON under $RUNDIR/input" >&2
  exit 1
fi

echo "Using profile: $CONVERTED" >&2

# --- Locate the analyzer script (read-only; never copied/written) -----------
# Prefer the copy co-located with this script (the skill's own source of
# truth); fall back to whichever harness directory `yarn skills` synced into
# the target repo, in case this runner is ever invoked standalone/copied
# without its sibling analyze-cpuprofile.cjs.
ANALYZER=""
if [ -f "$SCRIPT_DIR/analyze-cpuprofile.cjs" ]; then
  ANALYZER="$SCRIPT_DIR/analyze-cpuprofile.cjs"
else
  for AC in \
    "$REPO/.claude/skills/mms-swaps-cpu-profile-audit/scripts/analyze-cpuprofile.cjs" \
    "$REPO/.cursor/rules/mms-swaps-cpu-profile-audit/scripts/analyze-cpuprofile.cjs" \
    "$REPO/.agents/skills/mms-swaps-cpu-profile-audit/scripts/analyze-cpuprofile.cjs"
  do
    if [ -f "$AC" ]; then ANALYZER="$AC"; break; fi
  done
fi

if [ -z "$ANALYZER" ]; then
  echo "analyze-cpuprofile.cjs not found next to run.sh, nor under .claude, .cursor, or .agents in $REPO." >&2
  echo "Run 'yarn skills' in $REPO to (re)sync it, then retry." >&2
  exit 1
fi

REPORT="$RUNDIR/report.md"
node "$ANALYZER" --profile "$CONVERTED" --top "$TOP" --out "$REPORT" "${ANALYZER_OPTS[@]+"${ANALYZER_OPTS[@]}"}"

# Capture the report content now — the run folder (including this file) is
# removed by the EXIT trap as soon as the script returns.
REPORT_CONTENT="$(cat "$REPORT")"

echo "" >&2
echo "Run folder will be removed automatically now that the report is generated (nothing is left on disk)." >&2
echo "" >&2
printf '%s\n' "$REPORT_CONTENT"
