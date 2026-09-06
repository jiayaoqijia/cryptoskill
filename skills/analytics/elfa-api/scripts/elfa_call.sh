#!/usr/bin/env bash
# elfa_call.sh — Make authenticated Elfa API calls from the command line.
#
# Supports two auth modes:
#   API key:  Set ELFA_API_KEY in the environment (default).
#   x402:     Pass --x402 with a pre-signed payment header via --payment.
#
# Supports Auto endpoints:
#   --agent-secret Agent identity secret for x402 Auto requests.
#
# Usage:
#   ./elfa_call.sh <endpoint> [options]
#
# Examples:
#   ./elfa_call.sh /v2/ping   # no auth required
#   ./elfa_call.sh /v2/aggregations/trending-tokens -q 'timeWindow=24h&pageSize=10'
#   ./elfa_call.sh /v2/data/top-mentions -q 'ticker=$SOL&timeWindow=24h'
#   ./elfa_call.sh /v2/chat -d '{"message":"What is trending?","analysisType":"chat"}'
#   ./elfa_call.sh /v2/aggregations/trending-tokens --x402 --payment '<base64-payload>'

set -euo pipefail

BASE_URL="https://api.elfa.ai"

usage() {
  cat <<'EOF'
elfa_call.sh — Make authenticated Elfa API calls from the command line.

Supports two auth modes:
  API key:  Set ELFA_API_KEY in the environment (default).
  x402:     Pass --x402 with a pre-signed payment header via --payment.

Usage:
  ./elfa_call.sh <endpoint> [options]

Options:
  -q, --query <params>        Query string (e.g. 'timeWindow=24h&pageSize=10')
  -X, --method <METHOD>       HTTP method (default: GET, auto-set to POST with -d)
  -d, --data <json>           Request body (JSON). Implies -X POST.
  --x402                      Use x402 keyless mode (rewrites /v2/ to /x402/v2/).
  --payment <payload>         Pre-signed x402 payment header (base64). Requires --x402.
  --agent-secret <secret>     Agent identity secret added as x-elfa-agent-secret header
                              when using --x402 with Auto endpoints. Can also be set via
                              ELFA_AGENT_SECRET env var.
  -h, --help                  Show this help

Auto endpoints:
  All /v2/auto/* routes authenticate with x-elfa-api-key alone.

  Cancel and delete are distinct operations:
    - POST /cancel: only on active queries (returns 409 if terminal)
    - DELETE: only on terminal queries — triggered/expired/cancelled/failed
      (returns 409 if active; you must cancel first)

Examples:
  # API key mode (reads ELFA_API_KEY from env)
  ./elfa_call.sh /v2/ping
  ./elfa_call.sh /v2/aggregations/trending-tokens -q 'timeWindow=24h&pageSize=10'
  ./elfa_call.sh /v2/chat -d '{"message":"What is trending?","analysisType":"chat"}'

  # x402 mode (pay-per-request with USDC on Base)
  ./elfa_call.sh /v2/aggregations/trending-tokens --x402 --payment '<base64-payload>'

  # Auto: validate a query
  ./elfa_call.sh /v2/auto/queries/validate -d '{"query":{...}}'

  # Auto: validate a stored draft
  ./elfa_call.sh /v2/auto/queries/drafts/d_123/validate -X POST

  # Auto: Builder Chat (produces drafts only)
  ./elfa_call.sh /v2/auto/chat -d '{"message":"Alert me when BTC breaks 100k"}'

  # Auto: create a query with notification action
  ./elfa_call.sh /v2/auto/queries -d '{"query":{"actions":[{"type":"notify",...}],...}}'

  # Auto: cancel an active query
  ./elfa_call.sh /v2/auto/queries/q_123/cancel -X POST

  # Auto: delete a terminal query
  ./elfa_call.sh /v2/auto/queries/q_123 -X DELETE  # only after status is terminal

  # Auto: upsert a draft
  ./elfa_call.sh /v2/auto/queries/drafts -d '{"query":{...}}'

  # Auto: convert a draft to active query
  ./elfa_call.sh /v2/auto/queries/drafts/d_123/convert -X POST

  # Auto: list executions
  ./elfa_call.sh /v2/auto/executions

  # Auto x402: create query with agent secret
  ./elfa_call.sh /v2/auto/queries --x402 --payment '<payload>' --agent-secret "$ELFA_AGENT_SECRET"
EOF
  exit 0
}

die() { echo "error: $1" >&2; exit 1; }

# Format JSON — prefer jq, fall back to python3
fmt_json() {
  if command -v jq &>/dev/null; then
    jq .
  elif command -v python3 &>/dev/null; then
    python3 -m json.tool
  else
    cat
  fi
}

# Parse arguments
METHOD="GET"
QUERY=""
BODY=""
X402=false
PAYMENT=""
AGENT_SECRET="${ELFA_AGENT_SECRET:-}"

[[ $# -eq 0 ]] && usage
[[ "$1" == "-h" || "$1" == "--help" ]] && usage

ENDPOINT="$1"; shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    -X|--method)        [[ $# -lt 2 ]] && die "-X requires a value"; METHOD="$2"; shift 2 ;;
    -q|--query)         [[ $# -lt 2 ]] && die "-q requires a value"; QUERY="$2"; shift 2 ;;
    -d|--data)          [[ $# -lt 2 ]] && die "-d requires a value"; BODY="$2"; METHOD="POST"; shift 2 ;;
    --x402)             X402=true; shift ;;
    --payment)          [[ $# -lt 2 ]] && die "--payment requires a value"; PAYMENT="$2"; shift 2 ;;
    --agent-secret)     [[ $# -lt 2 ]] && die "--agent-secret requires a value"; AGENT_SECRET="$2"; shift 2 ;;
    -h|--help)          usage ;;
    *)                  die "unknown option: $1" ;;
  esac
done

# Normalize method to uppercase (use tr for bash 3.x / macOS compat)
METHOD=$(printf '%s' "$METHOD" | tr '[:lower:]' '[:upper:]')

# Validate
[[ "$ENDPOINT" == /* ]] || die "endpoint must start with / (e.g. /v2/ping)"

if [[ "$X402" == true ]]; then
  # Rewrite /v2/ → /x402/v2/ if not already prefixed
  [[ "$ENDPOINT" == /v2/* ]] && ENDPOINT="/x402${ENDPOINT}"
  [[ -n "$PAYMENT" ]] || die "--x402 requires --payment <payload>. See https://docs.elfa.ai/x402-payments"
else
  [[ -z "${ELFA_API_KEY:-}" ]] && die "ELFA_API_KEY is not set. Get a free key at https://go.elfa.ai/claude-skills"
fi

# Detect Auto endpoints. We check the *original* endpoint (before x402 rewrite).
IS_AUTO_ENDPOINT=false
ORIGINAL_ENDPOINT="${ENDPOINT#/x402}"
[[ "$ORIGINAL_ENDPOINT" == /v2/auto/* ]] && IS_AUTO_ENDPOINT=true

# Build URL
URL="${BASE_URL}${ENDPOINT}"
[[ -n "$QUERY" ]] && URL="${URL}?${QUERY}"

# Build curl args
CURL_ARGS=(-s --fail-with-body --max-time 30 -X "$METHOD")

if [[ "$X402" == true ]]; then
  CURL_ARGS+=(-H "PAYMENT-SIGNATURE: ${PAYMENT}")
  # Add agent-secret header only for x402 Auto requests when provided
  if [[ -n "$AGENT_SECRET" ]] && [[ "$IS_AUTO_ENDPOINT" == true ]]; then
    CURL_ARGS+=(-H "x-elfa-agent-secret: ${AGENT_SECRET}")
  fi
else
  CURL_ARGS+=(-H "x-elfa-api-key: ${ELFA_API_KEY}")
fi

if [[ -n "$BODY" ]]; then
  CURL_ARGS+=(-H "Content-Type: application/json" -d "$BODY")
fi

# Execute
HTTP_BODY=$(curl "${CURL_ARGS[@]}" -w '\n%{http_code}' "$URL") || true

HTTP_CODE=$(echo "$HTTP_BODY" | tail -n1)
RESPONSE=$(echo "$HTTP_BODY" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]] 2>/dev/null; then
  echo "$RESPONSE" | fmt_json
else
  echo "HTTP $HTTP_CODE" >&2
  echo "$RESPONSE" | fmt_json >&2
  exit 1
fi
