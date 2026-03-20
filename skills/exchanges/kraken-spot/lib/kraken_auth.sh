#!/usr/bin/env bash

kraken_generate_nonce() {
  if [ -n "${KRAKEN_NONCE_CMD:-}" ]; then
    "$KRAKEN_NONCE_CMD"
    return
  fi

  printf '%s%03d\n' "$(date +%s)" "$((10#$(date +%N | cut -c1-3)))"
}

kraken_urlencode() {
  local value="${1:-}"
  local output=""
  local i char hex

  for ((i = 0; i < ${#value}; i++)); do
    char="${value:i:1}"
    case "$char" in
      [a-zA-Z0-9.~_-])
        output+="$char"
        ;;
      *)
        printf -v hex '%%%02X' "'$char"
        output+="$hex"
        ;;
    esac
  done

  printf '%s' "$output"
}

kraken_query_kv() {
  local key="$1"
  local value="${2:-}"
  if [ -z "$value" ]; then
    return 0
  fi

  printf '%s=%s' "$(kraken_urlencode "$key")" "$(kraken_urlencode "$value")"
}

kraken_join_query() {
  local result=""
  local item
  for item in "$@"; do
    [ -n "$item" ] || continue
    if [ -n "$result" ]; then
      result="${result}&${item}"
    else
      result="$item"
    fi
  done
  printf '%s' "$result"
}

kraken_sha256_binary() {
  openssl dgst -sha256 -binary
}

kraken_hmac_base64() {
  local secret="$1"
  openssl dgst -sha512 -mac HMAC -macopt "hexkey:$secret" -binary | base64 | tr -d '\n'
}

kraken_secret_hex() {
  printf '%s' "$KRAKEN_API_SECRET" | base64 -d | od -An -vtx1 | tr -d ' \n'
}

kraken_sign_payload() {
  local path="$1"
  local body="$2"
  local nonce="$3"
  local sha_input="${nonce}${body}"
  local digest
  digest="$(printf '%s' "$sha_input" | kraken_sha256_binary)"
  {
    printf '%s' "/${KRAKEN_API_VERSION}${path}"
    printf '%s' "$digest"
  } | kraken_hmac_base64 "$(kraken_secret_hex)"
}
