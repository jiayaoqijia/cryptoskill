#!/usr/bin/env bash
# pyjail-lab.sh — replicate a python jail locally under podman, exact interpreter version.
#
# Usage:
#   pyjail-lab.sh [VERSION] JAIL_FILE [-- extra python args...]
#   pyjail-lab.sh 3.11 jail.py              # podman python:3.11-slim (default version: 3.11)
#   pyjail-lab.sh 3.8 jail.py               # match the challenge's python exactly
#   pyjail-lab.sh --system jail.py          # force local python3 (no container)
#
# Behavior:
#   - mounts $PWD at /x, runs the jail there, network disabled (offline replica).
#   - podman missing or --system: falls back to system python3 with a warning.
#   - first image pull needs network; afterwards runs offline.
#   - environment knobs: PYJAIL_LAB_IMAGE (default docker.io/library/python),
#                        PYJAIL_LAB_NET=1 to give the container network.
set -euo pipefail

DEFAULT_VERSION="3.11"
IMAGE="${PYJAIL_LAB_IMAGE:-docker.io/library/python}"
version="$DEFAULT_VERSION"
jail=""
system=0
passthrough=()

need_help() {
  cat <<'EOF'
Usage: pyjail-lab.sh [VERSION] JAIL_FILE [-- extra python args]
       pyjail-lab.sh --system JAIL_FILE
Replicate a python jail locally: podman run -it --rm -v $PWD:/x -w /x python:<VERSION>-slim python jail.py.
Falls back to system python3 (warning) when podman is unavailable.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) need_help; exit 0 ;;
    --system) system=1; shift ;;
    --) shift; passthrough+=("$@"); break ;;
    *)
      if [[ -z "$jail" && "$1" =~ ^[0-9]+\.[0-9]+([0-9]+)?$ ]]; then
        version="$1"
      elif [[ -z "$jail" ]]; then
        jail="$1"
      else
        passthrough+=("$1")
      fi
      shift
      ;;
  esac
done

if [[ -z "$jail" ]]; then
  need_help >&2
  exit 2
fi
if [[ ! -f "$jail" ]]; then
  echo "pyjail-lab.sh: jail file not found: $jail" >&2
  exit 2
fi

run_system() {
  echo "[!] running on system python3 ($(python3 --version 2>&1)) — version may not match the challenge" >&2
  exec python3 "$jail" "${passthrough[@]+"${passthrough[@]}"}"
}

if (( system )) || ! command -v podman >/dev/null 2>&1; then
  run_system
fi

net_args=(--network=none)
if [[ "${PYJAIL_LAB_NET:-0}" == "1" ]]; then
  net_args=()
fi

# shellcheck disable=SC2086
exec podman run -it --rm \
  -v "$PWD":/x:Z -w /x \
  "${net_args[@]}" \
  "$IMAGE:${version}-slim" \
  python "$jail" "${passthrough[@]+"${passthrough[@]}"}"
