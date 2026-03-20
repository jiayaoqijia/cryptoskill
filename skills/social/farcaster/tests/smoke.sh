#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[smoke] deps"
command -v jq >/dev/null
command -v python3 >/dev/null

echo "[smoke] --help works (offline)"
./scripts/fc_user.sh --help >/dev/null
./scripts/fc_feed.sh --help >/dev/null
./scripts/fc_cast.sh --help >/dev/null
./scripts/fc_search.sh --help >/dev/null
./scripts/fc_channels.sh --help >/dev/null
./scripts/fc_react.sh --help >/dev/null
./scripts/fc_delete.sh --help >/dev/null

echo "[smoke] required env var errors"
set +e
OUT=$(NEYNAR_API_KEY="" ./scripts/fc_user.sh --username dwr 2>&1)
CODE=$?
set -e
[[ $CODE -ne 0 ]]
echo "$OUT" | grep -q "NEYNAR_API_KEY"

echo "[smoke] stubbed API calls"
export NEYNAR_API_KEY="test-key"
export NEYNAR_SIGNER_UUID="test-signer"
export PATH="$ROOT/tests/stubs:$PATH"

# user lookup
U=$(./scripts/fc_user.sh --username dwr)
echo "$U" | jq -e '.username=="dwr" and .fid==3' >/dev/null

# feed
F=$(./scripts/fc_feed.sh --fid 3 --limit 1)
echo "$F" | jq -e '.casts[0].hash=="0xaaa" and .next_cursor=="CUR"' >/dev/null

# post cast
C=$(./scripts/fc_cast.sh --text "Hello")
echo "$C" | jq -e '.success==true and .hash=="0xbbb"' >/dev/null

# search
S=$(./scripts/fc_search.sh --query "base" --limit 1)
echo "$S" | jq -e '.casts[0].hash=="0xccc" and .next_cursor=="CUR2"' >/dev/null

# channel
CH=$(./scripts/fc_channels.sh --id base)
echo "$CH" | jq -e '.id=="base" and .lead=="lead"' >/dev/null

echo "[smoke] OK"
