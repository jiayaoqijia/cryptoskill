#!/usr/bin/env bash

kraken_endpoint_lookup() {
  local alias="$1"
  local line

  while IFS='|' read -r endpoint_alias endpoint_method endpoint_path endpoint_signed endpoint_confirm endpoint_description; do
    [ -n "$endpoint_alias" ] || continue
    case "$endpoint_alias" in
      \#*)
        continue
        ;;
    esac

    if [ "$endpoint_alias" = "$alias" ]; then
      KRAKEN_ENDPOINT_ALIAS="$endpoint_alias"
      KRAKEN_ENDPOINT_METHOD="$endpoint_method"
      KRAKEN_ENDPOINT_PATH="$endpoint_path"
      KRAKEN_ENDPOINT_SIGNED="$endpoint_signed"
      KRAKEN_ENDPOINT_CONFIRM="$endpoint_confirm"
      KRAKEN_ENDPOINT_DESCRIPTION="$endpoint_description"
      return 0
    fi
  done <"$KRAKEN_ENDPOINTS_FILE"

  kraken_fail "unknown endpoint alias: $alias"
}

kraken_list_endpoints() {
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
  done <"$KRAKEN_ENDPOINTS_FILE"
}

kraken_describe_endpoint() {
  local alias="$1"
  kraken_endpoint_lookup "$alias"
  cat <<EOF
alias: $KRAKEN_ENDPOINT_ALIAS
method: $KRAKEN_ENDPOINT_METHOD
path: $KRAKEN_ENDPOINT_PATH
signed: $KRAKEN_ENDPOINT_SIGNED
confirm_required: $KRAKEN_ENDPOINT_CONFIRM
description: $KRAKEN_ENDPOINT_DESCRIPTION
EOF
}

kraken_normalize_raw_path() {
  local scope="$1"
  local endpoint="$2"

  case "$endpoint" in
    /public/*|/private/*)
      printf '%s' "$endpoint"
      ;;
    /*)
      if [ "$scope" = "public" ]; then
        printf '/public%s' "$endpoint"
      else
        printf '/private%s' "$endpoint"
      fi
      ;;
    *)
      if [ "$scope" = "public" ]; then
        printf '/public/%s' "$endpoint"
      else
        printf '/private/%s' "$endpoint"
      fi
      ;;
  esac
}
