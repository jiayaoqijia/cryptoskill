#!/usr/bin/env bash

kraken_futures_lookup() {
  local alias="$1"
  local endpoint_alias endpoint_method endpoint_path endpoint_signed endpoint_confirm endpoint_description

  while IFS='|' read -r endpoint_alias endpoint_method endpoint_path endpoint_signed endpoint_confirm endpoint_description; do
    [ -n "$endpoint_alias" ] || continue
    case "$endpoint_alias" in
      \#*)
        continue
        ;;
    esac

    if [ "$endpoint_alias" = "$alias" ]; then
      KRAKEN_FUTURES_ALIAS="$endpoint_alias"
      KRAKEN_FUTURES_METHOD="$endpoint_method"
      KRAKEN_FUTURES_PATH="$endpoint_path"
      KRAKEN_FUTURES_SIGNED="$endpoint_signed"
      KRAKEN_FUTURES_CONFIRM="$endpoint_confirm"
      KRAKEN_FUTURES_DESCRIPTION="$endpoint_description"
      return 0
    fi
  done <"$KRAKEN_FUTURES_ENDPOINTS_FILE"

  kraken_fail "unknown futures endpoint alias: $alias"
}

kraken_futures_list() {
  local prefix="${1:-}"
  local endpoint_alias endpoint_method endpoint_path endpoint_signed endpoint_confirm endpoint_description

  while IFS='|' read -r endpoint_alias endpoint_method endpoint_path endpoint_signed endpoint_confirm endpoint_description; do
    [ -n "$endpoint_alias" ] || continue
    case "$endpoint_alias" in
      \#*)
        continue
        ;;
    esac

    if [ -n "$prefix" ]; then
      case "$endpoint_alias" in
        "$prefix"*|*"$prefix"*)
          ;;
        *)
          continue
          ;;
      esac
    fi

    printf '%s\t%s\t%s\tconfirm=%s\n' "$endpoint_alias" "$endpoint_method" "$endpoint_path" "$endpoint_confirm"
  done <"$KRAKEN_FUTURES_ENDPOINTS_FILE"
}

kraken_futures_describe() {
  local alias="$1"
  kraken_futures_lookup "$alias"
  cat <<EOF
alias: $KRAKEN_FUTURES_ALIAS
method: $KRAKEN_FUTURES_METHOD
path: $KRAKEN_FUTURES_PATH
signed: $KRAKEN_FUTURES_SIGNED
confirm_required: $KRAKEN_FUTURES_CONFIRM
description: $KRAKEN_FUTURES_DESCRIPTION
EOF
}

kraken_require_futures_private_env() {
  [ -n "${KRAKEN_FUTURES_API_KEY:-}" ] || kraken_fail "missing KRAKEN_FUTURES_API_KEY for futures private endpoint"
  [ -n "${KRAKEN_FUTURES_API_SECRET:-}" ] || kraken_fail "missing KRAKEN_FUTURES_API_SECRET for futures private endpoint"
}

kraken_futures_secret_hex() {
  printf '%s' "$KRAKEN_FUTURES_API_SECRET" | base64 -d | od -An -vtx1 | tr -d ' \n'
}

kraken_sign_futures_payload() {
  local path="$1"
  local payload="$2"
  local nonce="$3"
  local sha_input="${payload}${nonce}${path}"
  local digest
  digest="$(printf '%s' "$sha_input" | kraken_sha256_binary)"
  printf '%s' "$digest" | openssl dgst -sha512 -mac HMAC -macopt "hexkey:$(kraken_futures_secret_hex)" -binary | base64 | tr -d '\n'
}

kraken_sign_futures_challenge() {
  local challenge="$1"
  local digest
  digest="$(printf '%s' "$challenge" | kraken_sha256_binary)"
  printf '%s' "$digest" | openssl dgst -sha512 -mac HMAC -macopt "hexkey:$(kraken_futures_secret_hex)" -binary | base64 | tr -d '\n'
}

kraken_futures_http_request() {
  local method="$1"
  local path="$2"
  local payload="${3:-}"
  local signed="$4"
  local nonce=""
  local signature=""
  local url="${KRAKEN_FUTURES_API_BASE_URL}${path}"
  local -a args
  args=(-sS --connect-timeout "$KRAKEN_TIMEOUT_SECS" --max-time "$KRAKEN_TIMEOUT_SECS" -A "$KRAKEN_USER_AGENT" -X "$method")

  if [ "$signed" = "true" ]; then
    kraken_require_futures_private_env
    nonce="$(kraken_generate_nonce)"
    signature="$(kraken_sign_futures_payload "$path" "$payload" "$nonce")"
    args+=(-H "APIKey: $KRAKEN_FUTURES_API_KEY" -H "Authent: $signature" -H "Nonce: $nonce")
  fi

  case "$method" in
    GET)
      if [ -n "$payload" ]; then
        url="${url}?${payload}"
      fi
      ;;
    POST|PUT|DELETE)
      if [ -n "$payload" ]; then
        args+=(-H "Content-Type: application/x-www-form-urlencoded" --data "$payload")
      fi
      ;;
    *)
      kraken_fail "unsupported futures method: $method"
      ;;
  esac

  local response=""
  if [ "$KRAKEN_SIMULATE" = "true" ]; then
    response="$(kraken_simulate_response "$method" "$url" "$payload" "$signed")"
    kraken_emit_output "$response"
    return
  fi

  kraken_log info "dispatching ${method} ${url}"
  set +x
  if [ "${KRAKEN_OUTPUT_MODE:-raw}" = "raw" ] && [ -z "${KRAKEN_JQ_FILTER:-}" ]; then
    "$KRAKEN_HTTP_BIN" "${args[@]}" "$url"
    return
  fi

  response="$("$KRAKEN_HTTP_BIN" "${args[@]}" "$url")"
  kraken_emit_output "$response"
}
