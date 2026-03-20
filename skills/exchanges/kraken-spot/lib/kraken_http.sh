#!/usr/bin/env bash

kraken_public_get() {
  local path="$1"
  local query="${2:-}"
  kraken_http_request "GET" "$path" "$query" "false"
}

kraken_private_post() {
  local path="$1"
  local body="${2:-}"
  kraken_http_request "POST" "$path" "$body" "true"
}

kraken_http_request() {
  local method="$1"
  local path="$2"
  local payload="${3:-}"
  local signed="$4"
  kraken_validate_path "$path"

  local nonce="" request_body="$payload" request_url="${KRAKEN_API_BASE_URL}/${KRAKEN_API_VERSION}${path}" signature=""
  local -a args
  args=(-sS --connect-timeout "$KRAKEN_TIMEOUT_SECS" --max-time "$KRAKEN_TIMEOUT_SECS" -A "$KRAKEN_USER_AGENT" -X "$method")

  if [ "$signed" = "true" ]; then
    nonce="$(kraken_generate_nonce)"
    request_body="$(kraken_join_query "$(kraken_query_kv nonce "$nonce")" "$payload" "$(kraken_query_kv otp "${KRAKEN_OTP:-}")")"
    signature="$(kraken_sign_payload "$path" "$request_body" "$nonce")"
    args+=(-H "API-Key: $KRAKEN_API_KEY" -H "API-Sign: $signature" -H "Content-Type: application/x-www-form-urlencoded" --data "$request_body")
  elif [ -n "$payload" ]; then
    request_url="${request_url}?${payload}"
  fi

  local response=""

  if [ "$KRAKEN_SIMULATE" = "true" ]; then
    response="$(kraken_simulate_response "$method" "$request_url" "$request_body" "$signed")"
    kraken_emit_output "$response"
    return
  fi

  kraken_log info "dispatching ${method} ${request_url}"
  set +x
  if [ "${KRAKEN_OUTPUT_MODE:-raw}" = "raw" ] && [ -z "${KRAKEN_JQ_FILTER:-}" ]; then
    "$KRAKEN_HTTP_BIN" "${args[@]}" "$request_url"
    return
  fi

  response="$("$KRAKEN_HTTP_BIN" "${args[@]}" "$request_url")"
  kraken_emit_output "$response"
}

kraken_simulate_response() {
  local method="$1"
  local url="$2"
  local body="$3"
  local signed="$4"
  printf '{"ok":true,"simulate":true,"method":"%s","url":"%s","signed":%s' "$method" "$url" "$signed"
  if [ -n "$body" ]; then
    printf ',"body":"%s"' "$(printf '%s' "$body" | sed 's/"/\\"/g')"
  fi
  printf '}\n'
}

kraken_emit_output() {
  local response="$1"

  if [ -n "${KRAKEN_JQ_FILTER:-}" ]; then
    kraken_require_jq
    printf '%s' "$response" | jq -r "$KRAKEN_JQ_FILTER"
    return
  fi

  case "${KRAKEN_OUTPUT_MODE:-raw}" in
    raw)
      printf '%s\n' "$response"
      ;;
    compact)
      kraken_require_jq
      printf '%s' "$response" | jq -c .
      ;;
    pretty)
      kraken_require_jq
      printf '%s' "$response" | jq .
      ;;
  esac
}
