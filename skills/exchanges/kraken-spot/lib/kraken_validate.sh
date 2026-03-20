#!/usr/bin/env bash

kraken_validate_runtime() {
  case "$KRAKEN_API_BASE_URL" in
    https://*)
      ;;
    http://*)
      [ "$KRAKEN_ALLOW_INSECURE_BASE_URL" = "true" ] || kraken_fail "refusing insecure base URL without KRAKEN_ALLOW_INSECURE_BASE_URL=true"
      ;;
    *)
      kraken_fail "invalid base URL: $KRAKEN_API_BASE_URL"
      ;;
  esac

  case "$KRAKEN_API_VERSION" in
    ''|*[!0-9]*)
      kraken_fail "KRAKEN_API_VERSION must be numeric"
      ;;
  esac

  case "$KRAKEN_OUTPUT_MODE" in
    raw|compact|pretty)
      ;;
    *)
      kraken_fail "unsupported KRAKEN_OUTPUT_MODE: $KRAKEN_OUTPUT_MODE"
      ;;
  esac

  command -v "$KRAKEN_HTTP_BIN" >/dev/null 2>&1 || kraken_fail "missing HTTP binary: $KRAKEN_HTTP_BIN"
  command -v "$KRAKEN_WS_NODE_BIN" >/dev/null 2>&1 || kraken_fail "missing websocket runtime: $KRAKEN_WS_NODE_BIN"
  command -v openssl >/dev/null 2>&1 || kraken_fail "missing required binary: openssl"
  command -v base64 >/dev/null 2>&1 || kraken_fail "missing required binary: base64"
  command -v od >/dev/null 2>&1 || kraken_fail "missing required binary: od"
  [ -r "$KRAKEN_ENDPOINTS_FILE" ] || kraken_fail "missing endpoints registry: $KRAKEN_ENDPOINTS_FILE"
  [ -r "$KRAKEN_FUTURES_ENDPOINTS_FILE" ] || kraken_fail "missing futures endpoints registry: $KRAKEN_FUTURES_ENDPOINTS_FILE"
}

kraken_validate_path() {
  local path="$1"
  case "$path" in
    /public/*|/private/*)
      ;;
    *)
      kraken_fail "unsupported API path: $path"
      ;;
  esac
}

kraken_require_private_env() {
  [ -n "${KRAKEN_API_KEY:-}" ] || kraken_fail "missing KRAKEN_API_KEY for private endpoint"
  [ -n "${KRAKEN_API_SECRET:-}" ] || kraken_fail "missing KRAKEN_API_SECRET for private endpoint"
}

kraken_require_confirmation() {
  local command="$1"
  if [ "${KRAKEN_REQUIRE_CONFIRM}" = "true" ] && [ "${KRAKEN_FLAG_confirm:-}" != "true" ]; then
    kraken_fail "refusing orders $command without --confirm"
  fi
}

kraken_require_jq() {
  command -v jq >/dev/null 2>&1 || kraken_fail "jq is required for this output mode"
}
