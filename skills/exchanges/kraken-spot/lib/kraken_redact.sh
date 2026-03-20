#!/usr/bin/env bash

kraken_redact() {
  local input="${1:-}"
  input="${input//${KRAKEN_API_KEY:-}/[REDACTED_API_KEY]}"
  input="${input//${KRAKEN_API_SECRET:-}/[REDACTED_API_SECRET]}"
  input="${input//API-Sign: */API-Sign: [REDACTED]}"
  input="${input//API-Key: */API-Key: [REDACTED]}"
  printf '%s' "$input"
}

kraken_log() {
  local level="$1"
  shift
  local message="$*"
  printf '[%s] %s\n' "$level" "$(kraken_redact "$message")" >&2
}

kraken_fail() {
  kraken_log error "$*"
  exit 1
}
