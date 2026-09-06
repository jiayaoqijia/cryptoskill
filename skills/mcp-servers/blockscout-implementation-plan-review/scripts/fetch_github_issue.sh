#!/usr/bin/env bash
#
# Fetches a GitHub issue (title + body + labels/state/url) into a local markdown file.
#
# Usage:
#   fetch_github_issue.sh <issue-number> [--out <path>]
#
# Output on success (when --out is used):
#   OK <path>
#
# Output on failure:
#   ERROR <classification>
#   ACTION <what the caller should do next>
#   DETAIL <first line from gh, when useful>
#
# Exit codes:
#   0 - Success
#   1 - Missing/invalid arguments
#   3 - GitHub credentials unavailable to this process
#   4 - GitHub fetch failed for a non-network reason
#   5 - Failed to write output file
#   6 - GitHub API network access unavailable

set -euo pipefail

if [[ $# -lt 1 || -z "${1:-}" ]]; then
    echo "ERROR Missing GitHub issue number argument"
    exit 1
fi

ISSUE_NUMBER="$1"
shift

OUT=""
if [[ $# -gt 0 ]]; then
    if [[ "${1:-}" == "--out" ]]; then
        if [[ $# -lt 2 || -z "${2:-}" ]]; then
            echo "ERROR --out requires a non-empty path"
            exit 1
        fi
        OUT="$2"
        shift 2
    else
        echo "ERROR Unknown argument: ${1:-}"
        exit 1
    fi
fi

if [[ $# -gt 0 ]]; then
    echo "ERROR Too many arguments"
    exit 1
fi

if [[ ! "$ISSUE_NUMBER" =~ ^[0-9]+$ ]]; then
    echo "ERROR Issue number must be digits (example: 326)"
    exit 1
fi

CMD=(gh issue view "$ISSUE_NUMBER")

set +e
MD="$("${CMD[@]}" --json title,body,url,state,labels --template \
    '{{printf "# %s\n\n" .title -}}
{{printf "Source: %s\n" .url -}}
{{printf "State: %s\n" .state -}}
{{- printf "Labels: " -}}
{{- if .labels -}}
{{- range $i, $l := .labels -}}
{{- if $i -}}, {{- end -}}
{{- $l.name -}}
{{- end -}}
{{- else -}}None{{- end -}}
{{printf "\n\n## Body\n\n%s\n" .body -}}' 2>&1)"
STATUS=$?
set -e

if [[ $STATUS -ne 0 ]]; then
    FIRST_LINE="$(printf "%s" "$MD" | head -n 1)"
    LOWER_ERROR="$(printf "%s" "$MD" | tr '[:upper:]' '[:lower:]')"

    case "$LOWER_ERROR" in
        *"error connecting to"*|\
        *"check your internet connection"*|\
        *"could not resolve host"*|\
        *"temporary failure in name resolution"*|\
        *"network is unreachable"*|\
        *"connection refused"*|\
        *"connection timed out"*|\
        *"failed to connect"*|\
        *"tls handshake timeout"*|\
        *"i/o timeout"*|\
        *"context deadline exceeded"*)
            echo "ERROR GitHub API network access is unavailable to this process."
            echo "ACTION Agent: rerun this exact fetch command outside the network sandbox (require_escalated). Do not ask the user to re-authenticate for this error."
            echo "DETAIL ${FIRST_LINE}"
            exit 6
            ;;
    esac

    case "$LOWER_ERROR" in
        *"gh auth login"*|\
        *"bad credentials"*|\
        *"http 401"*|\
        *"authentication required"*|\
        *"not logged into any github hosts"*)
            echo "ERROR GitHub credentials are unavailable to this process."
            echo "ACTION Run 'gh auth status'. If it is not logged in, run 'gh auth login'. If an interactive terminal is already logged in, rerun this fetch outside the sandbox so it can access the keyring."
            echo "DETAIL ${FIRST_LINE}"
            exit 3
            ;;
    esac

    if ! gh auth token -h github.com &>/dev/null; then
        echo "ERROR GitHub credentials are unavailable to this process."
        echo "ACTION Run 'gh auth status'. If it is not logged in, run 'gh auth login'. If an interactive terminal is already logged in, rerun this fetch outside the sandbox so it can access the keyring."
        echo "DETAIL ${FIRST_LINE}"
        exit 3
    fi

    echo "ERROR GitHub CLI could not fetch issue ${ISSUE_NUMBER} although credentials are available."
    echo "ACTION Check the issue number and repository access, then inspect the gh error below."
    echo "DETAIL ${FIRST_LINE}"
    exit 4
fi

if [[ -n "$OUT" ]]; then
    OUT_DIR="$(dirname -- "$OUT")"
    if [[ ! -d "$OUT_DIR" ]]; then
        echo "ERROR Output directory does not exist: ${OUT_DIR}"
        exit 5
    fi
    if [[ ! -w "$OUT_DIR" ]]; then
        echo "ERROR Output directory is not writable: ${OUT_DIR}"
        exit 5
    fi
    if ! printf "%s" "$MD" >"$OUT"; then
        echo "ERROR Failed to write output file: ${OUT}"
        exit 5
    fi
    echo "OK $OUT"
else
    printf "%s" "$MD"
fi
