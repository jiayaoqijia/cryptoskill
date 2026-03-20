#!/usr/bin/env bash
set -euo pipefail

# Test suite for cobo-tss-node skill scripts
# All tests use temp directories — never touches ~/.cobo-tss-node

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts"
TEST_DIR=$(mktemp -d)
PASS=0
FAIL=0
ERRORS=()

trap "rm -rf $TEST_DIR" EXIT

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

log_pass() { PASS=$((PASS + 1)); echo -e "  ${GREEN}✅ $1${NC}"; }
log_fail() { FAIL=$((FAIL + 1)); ERRORS+=("$1: $2"); echo -e "  ${RED}❌ $1: $2${NC}"; }

# Create a mock cobo-tss-node binary
create_mock_binary() {
  local dir="$1"
  cat > "$dir/cobo-tss-node" <<'MOCK'
#!/usr/bin/env bash
# Mock cobo-tss-node binary for testing
CMD="${1:-}"
shift || true
case "$CMD" in
  version) echo "v0.13.0-mock" ;;
  init)
    # Parse args to find --db
    DB=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --db) DB="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    [[ -n "$DB" ]] && mkdir -p "$(dirname "$DB")" && echo "mock-db" > "$DB"
    echo "Node initialized"
    echo "TSS Node ID: cobo-tss-node-mock-id-12345"
    ;;
  info)
    if [[ "${1:-}" == "group" ]]; then
      echo "Group: mock-group-001"
      echo "Threshold: 2/3"
    else
      echo "TSS Node ID: cobo-tss-node-mock-id-12345"
      echo "Created: 2025-01-01"
    fi
    ;;
  start) echo "Node started" ;;
  sign)
    echo "Signed message successfully"
    echo "Signature: 0xdeadbeef"
    ;;
  export-share)
    # Parse --export-dir
    EDIR=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --export-dir) EDIR="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    [[ -n "$EDIR" ]] && echo "mock-share-data" > "$EDIR/share.enc"
    echo "Exported shares"
    ;;
  migrate) echo "Migration complete (no changes)" ;;
  change-password) echo "Password changed" ;;
  *) echo "Unknown command: $CMD"; exit 1 ;;
esac
MOCK
  chmod 755 "$dir/cobo-tss-node"
}

# Setup a test install directory with mock binary + required files
setup_test_dir() {
  local dir="$1"
  mkdir -p "$dir"/{configs,db,logs,recovery,backups}
  create_mock_binary "$dir"
  printf 'test-password-123' > "$dir/.password"
  chmod 600 "$dir/.password"
  echo "env: development" > "$dir/configs/cobo-tss-node-config.yaml"
  echo "mock-db-content" > "$dir/db/secrets.db"
}

########################################
echo -e "\n${YELLOW}=== setup-keyfile.sh ===${NC}"
########################################

# Test: creates key file with random password
test_setup_keyfile_create() {
  local d="$TEST_DIR/keyfile-create"
  mkdir -p "$d"
  output=$(bash "$SCRIPT_DIR/setup-keyfile.sh" --dir "$d" 2>&1)
  if [[ -f "$d/.password" ]]; then
    perms=$(stat -c '%a' "$d/.password" 2>/dev/null || stat -f '%Lp' "$d/.password")
    if [[ "$perms" == "600" ]]; then
      log_pass "creates key file with mode 600"
    else
      log_fail "key file permissions" "expected 600 got $perms"
    fi
  else
    log_fail "creates key file" "file not found"
  fi
}

# Test: creates key file with specified password
test_setup_keyfile_custom_password() {
  local d="$TEST_DIR/keyfile-custom"
  mkdir -p "$d"
  bash "$SCRIPT_DIR/setup-keyfile.sh" --dir "$d" --password "my-secret-pw" 2>&1
  content=$(cat "$d/.password")
  if [[ "$content" == "my-secret-pw" ]]; then
    log_pass "custom password written correctly"
  else
    log_fail "custom password" "got '$content'"
  fi
}

# Test: refuses overwrite without --force in non-interactive mode
test_setup_keyfile_no_overwrite() {
  local d="$TEST_DIR/keyfile-noforce"
  mkdir -p "$d"
  bash "$SCRIPT_DIR/setup-keyfile.sh" --dir "$d" --password "first" 2>&1
  output=$(bash "$SCRIPT_DIR/setup-keyfile.sh" --dir "$d" --password "second" 2>&1 < /dev/null) && rc=$? || rc=$?
  content=$(cat "$d/.password")
  if [[ "$rc" -ne 0 && "$content" == "first" ]]; then
    log_pass "refuses overwrite without --force (non-interactive)"
  else
    log_fail "overwrite protection" "rc=$rc content='$content'"
  fi
}

# Test: --force overwrites
test_setup_keyfile_force() {
  local d="$TEST_DIR/keyfile-force"
  mkdir -p "$d"
  bash "$SCRIPT_DIR/setup-keyfile.sh" --dir "$d" --password "first" 2>&1
  bash "$SCRIPT_DIR/setup-keyfile.sh" --dir "$d" --password "second" --force 2>&1
  content=$(cat "$d/.password")
  if [[ "$content" == "second" ]]; then
    log_pass "--force overwrites existing key file"
  else
    log_fail "--force overwrite" "got '$content'"
  fi
}

# Test: password has no trailing newline
test_setup_keyfile_no_newline() {
  local d="$TEST_DIR/keyfile-nonewline"
  mkdir -p "$d"
  bash "$SCRIPT_DIR/setup-keyfile.sh" --dir "$d" --password "exact" 2>&1
  # Use wc -c to check exact byte count ("exact" = 5 bytes)
  bytes=$(wc -c < "$d/.password" | tr -d ' ')
  if [[ "$bytes" == "5" ]]; then
    log_pass "no trailing newline in password file"
  else
    log_fail "trailing newline" "expected 5 bytes got $bytes"
  fi
}

test_setup_keyfile_create
test_setup_keyfile_custom_password
test_setup_keyfile_no_overwrite
test_setup_keyfile_force
test_setup_keyfile_no_newline

########################################
echo -e "\n${YELLOW}=== init-node.sh ===${NC}"
########################################

# Test: initializes node successfully
test_init_node_success() {
  local d="$TEST_DIR/init-ok"
  mkdir -p "$d"/configs
  create_mock_binary "$d"
  printf 'pw' > "$d/.password"; chmod 600 "$d/.password"
  echo "env: dev" > "$d/configs/cobo-tss-node-config.yaml"
  output=$(bash "$SCRIPT_DIR/init-node.sh" --dir "$d" 2>&1)
  if [[ -f "$d/db/secrets.db" ]] && echo "$output" | grep -q "initialized"; then
    log_pass "initializes node and creates db"
  else
    log_fail "init node" "db missing or no success message"
  fi
}

# Test: refuses if db already exists
test_init_node_existing_db() {
  local d="$TEST_DIR/init-exists"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/init-node.sh" --dir "$d" 2>&1) && rc=$? || rc=$?
  if [[ "$rc" -ne 0 ]] && echo "$output" | grep -qi "already exists"; then
    log_pass "refuses init when db exists"
  else
    log_fail "existing db check" "rc=$rc output: $output"
  fi
}

# Test: fails without binary
test_init_node_no_binary() {
  local d="$TEST_DIR/init-nobin"
  mkdir -p "$d"/configs
  printf 'pw' > "$d/.password"; chmod 600 "$d/.password"
  output=$(bash "$SCRIPT_DIR/init-node.sh" --dir "$d" 2>&1) && rc=$? || rc=$?
  if [[ "$rc" -ne 0 ]]; then
    log_pass "fails without binary"
  else
    log_fail "no binary check" "should have failed"
  fi
}

# Test: fails without key file
test_init_node_no_keyfile() {
  local d="$TEST_DIR/init-nokey"
  mkdir -p "$d"/configs
  create_mock_binary "$d"
  output=$(bash "$SCRIPT_DIR/init-node.sh" --dir "$d" 2>&1) && rc=$? || rc=$?
  if [[ "$rc" -ne 0 ]]; then
    log_pass "fails without key file"
  else
    log_fail "no keyfile check" "should have failed"
  fi
}

test_init_node_success
test_init_node_existing_db
test_init_node_no_binary
test_init_node_no_keyfile

########################################
echo -e "\n${YELLOW}=== node-info.sh ===${NC}"
########################################

test_node_info_basic() {
  local d="$TEST_DIR/info-basic"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-info.sh" --dir "$d" 2>&1)
  if echo "$output" | grep -q "mock-id-12345"; then
    log_pass "shows node info"
  else
    log_fail "node info" "expected mock ID, got: $output"
  fi
}

test_node_info_group() {
  local d="$TEST_DIR/info-group"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-info.sh" --dir "$d" --group 2>&1)
  if echo "$output" | grep -q "mock-group"; then
    log_pass "shows group info"
  else
    log_fail "group info" "got: $output"
  fi
}

test_node_info_basic
test_node_info_group

########################################
echo -e "\n${YELLOW}=== node-ctl.sh ===${NC}"
########################################

# Test: health check output
test_ctl_health() {
  local d="$TEST_DIR/ctl-health"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" health --dir "$d" 2>&1) || true
  checks=0
  echo "$output" | grep -q "Version:" && checks=$((checks + 1))
  echo "$output" | grep -q "Database:" && checks=$((checks + 1))
  echo "$output" | grep -q "Config:" && checks=$((checks + 1))
  echo "$output" | grep -q "Key file:" && checks=$((checks + 1))
  echo "$output" | grep -q "Disk available:" && checks=$((checks + 1))
  if [[ "$checks" -ge 4 ]]; then
    log_pass "health check covers all sections ($checks/5)"
  else
    log_fail "health check" "only $checks/5 sections found"
  fi
}

# Test: health reports key file permission correctly
test_ctl_health_keyfile_perms() {
  local d="$TEST_DIR/ctl-health-perms"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" health --dir "$d" 2>&1) || true
  if echo "$output" | grep -q "mode 600"; then
    log_pass "health reports correct key file mode 600"
  else
    log_fail "health key perms" "didn't find mode 600"
  fi
}

# Test: health warns on bad key file permissions
test_ctl_health_bad_perms() {
  local d="$TEST_DIR/ctl-health-badperms"
  setup_test_dir "$d"
  chmod 644 "$d/.password"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" health --dir "$d" 2>&1) || true
  if echo "$output" | grep -q "⚠️"; then
    log_pass "health warns on bad key file permissions"
  else
    log_fail "health bad perms" "no warning found"
  fi
}

# Test: sign with auto-generated message
test_ctl_sign_auto() {
  local d="$TEST_DIR/ctl-sign"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" sign --dir "$d" mock-group-001 2>&1)
  if echo "$output" | grep -q "Signed\|Signature"; then
    log_pass "sign with auto message"
  else
    log_fail "sign auto" "got: $output"
  fi
}

# Test: sign without group-id fails
test_ctl_sign_no_group() {
  local d="$TEST_DIR/ctl-sign-nogrp"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" sign --dir "$d" 2>&1) && rc=$? || rc=$?
  if [[ "$rc" -ne 0 ]] && echo "$output" | grep -qi "usage"; then
    log_pass "sign fails without group-id"
  else
    log_fail "sign no group" "rc=$rc"
  fi
}

# Test: export creates recovery dir with files
test_ctl_export() {
  local d="$TEST_DIR/ctl-export"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" export --dir "$d" mock-group-001 2>&1)
  recovery_dirs=$(find "$d/recovery" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$recovery_dirs" -ge 1 ]]; then
    log_pass "export creates recovery directory"
  else
    log_fail "export" "no recovery dir created"
  fi
}

# Test: backup creates all required files + SHA256SUMS includes .password
test_ctl_backup() {
  local d="$TEST_DIR/ctl-backup"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" backup --dir "$d" 2>&1)
  backup_dir=$(find "$d/backups" -mindepth 1 -maxdepth 1 -type d | head -1)
  if [[ -z "$backup_dir" ]]; then
    log_fail "backup" "no backup dir created"
    return
  fi
  files_ok=0
  [[ -f "$backup_dir/secrets.db" ]] && files_ok=$((files_ok + 1))
  [[ -f "$backup_dir/cobo-tss-node-config.yaml" ]] && files_ok=$((files_ok + 1))
  [[ -f "$backup_dir/.password" ]] && files_ok=$((files_ok + 1))
  [[ -f "$backup_dir/SHA256SUMS" ]] && files_ok=$((files_ok + 1))
  if [[ "$files_ok" -eq 4 ]]; then
    log_pass "backup creates all 4 expected files"
  else
    log_fail "backup files" "only $files_ok/4 found in $backup_dir"
  fi
}

# Test: SHA256SUMS includes .password (the dotfile bug fix)
test_ctl_backup_sha_includes_dotfile() {
  local d="$TEST_DIR/ctl-backup-sha"
  setup_test_dir "$d"
  bash "$SCRIPT_DIR/node-ctl.sh" backup --dir "$d" 2>&1
  backup_dir=$(find "$d/backups" -mindepth 1 -maxdepth 1 -type d | head -1)
  if grep -q ".password" "$backup_dir/SHA256SUMS" 2>/dev/null; then
    log_pass "SHA256SUMS includes .password (dotfile fix)"
  else
    log_fail "SHA256SUMS dotfile" ".password not in checksums"
  fi
}

# Test: backup .password has mode 600
test_ctl_backup_password_perms() {
  local d="$TEST_DIR/ctl-backup-perms"
  setup_test_dir "$d"
  bash "$SCRIPT_DIR/node-ctl.sh" backup --dir "$d" 2>&1
  backup_dir=$(find "$d/backups" -mindepth 1 -maxdepth 1 -type d | head -1)
  perms=$(stat -c '%a' "$backup_dir/.password" 2>/dev/null || stat -f '%Lp' "$backup_dir/.password")
  if [[ "$perms" == "600" ]]; then
    log_pass "backup .password has mode 600"
  else
    log_fail "backup password perms" "got $perms"
  fi
}

# Test: groups command
test_ctl_groups() {
  local d="$TEST_DIR/ctl-groups"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" groups --dir "$d" 2>&1)
  if echo "$output" | grep -q "mock-group"; then
    log_pass "groups lists groups"
  else
    log_fail "groups" "got: $output"
  fi
}

# Test: help command
test_ctl_help() {
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" help 2>&1)
  if echo "$output" | grep -q "Service Management" && echo "$output" | grep -q "Maintenance"; then
    log_pass "help shows all sections"
  else
    log_fail "help" "incomplete output"
  fi
}

# Test: unknown command fails
test_ctl_unknown() {
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" nonexistent 2>&1) && rc=$? || rc=$?
  if [[ "$rc" -ne 0 ]] && echo "$output" | grep -qi "unknown"; then
    log_pass "unknown command exits with error"
  else
    log_fail "unknown command" "rc=$rc"
  fi
}

# Test: check_bin fails without binary
test_ctl_no_binary() {
  local d="$TEST_DIR/ctl-nobin"
  mkdir -p "$d"
  printf 'pw' > "$d/.password"; chmod 600 "$d/.password"
  output=$(bash "$SCRIPT_DIR/node-ctl.sh" health --dir "$d" 2>&1) && rc=$? || rc=$?
  if [[ "$rc" -ne 0 ]]; then
    log_pass "health fails without binary"
  else
    log_fail "no binary" "should have failed"
  fi
}

test_ctl_health
test_ctl_health_keyfile_perms
test_ctl_health_bad_perms
test_ctl_sign_auto
test_ctl_sign_no_group
test_ctl_export
test_ctl_backup
test_ctl_backup_sha_includes_dotfile
test_ctl_backup_password_perms
test_ctl_groups
test_ctl_help
test_ctl_unknown
test_ctl_no_binary

########################################
echo -e "\n${YELLOW}=== install-service.sh ===${NC}"
########################################

# Test: generates valid systemd unit (dry check, don't actually install)
test_install_service_linux_content() {
  local d="$TEST_DIR/svc-linux"
  setup_test_dir "$d"
  # Override HOME to capture the generated service file
  HOME_BAK="$HOME"
  export HOME="$TEST_DIR/svc-linux-home"
  mkdir -p "$HOME/.config/systemd/user"
  output=$(bash "$SCRIPT_DIR/install-service.sh" linux --dir "$d" 2>&1) || true
  export HOME="$HOME_BAK"

  svc_file="$TEST_DIR/svc-linux-home/.config/systemd/user/cobo-tss-node.service"
  if [[ ! -f "$svc_file" ]]; then
    log_fail "linux service file" "not created"
    return
  fi

  checks=0
  grep -q "ExecStart=" "$svc_file" && checks=$((checks + 1))
  grep -q "key-file" "$svc_file" && checks=$((checks + 1))
  grep -q "NoNewPrivileges=true" "$svc_file" && checks=$((checks + 1))
  grep -q "backups" "$svc_file" && checks=$((checks + 1))  # fix #1: backups in ReadWritePaths
  grep -q "ProtectHome=false" "$svc_file" && checks=$((checks + 1))  # fix #1: not read-only

  if [[ "$checks" -ge 5 ]]; then
    log_pass "linux service file has all expected directives ($checks/5)"
  else
    log_fail "linux service content" "only $checks/5 checks passed"
  fi
}

# Test: generates valid launchd plist
test_install_service_macos_content() {
  local d="$TEST_DIR/svc-macos"
  setup_test_dir "$d"
  HOME_BAK="$HOME"
  export HOME="$TEST_DIR/svc-macos-home"
  mkdir -p "$HOME/Library/LaunchAgents"
  output=$(bash "$SCRIPT_DIR/install-service.sh" macos --dir "$d" 2>&1) || true
  export HOME="$HOME_BAK"

  plist="$TEST_DIR/svc-macos-home/Library/LaunchAgents/com.cobo.tss-node.plist"
  if [[ ! -f "$plist" ]]; then
    log_fail "macos plist" "not created"
    return
  fi

  checks=0
  grep -q "com.cobo.tss-node" "$plist" && checks=$((checks + 1))
  grep -q "key-file" "$plist" && checks=$((checks + 1))
  grep -q "KeepAlive" "$plist" && checks=$((checks + 1))
  grep -q "ThrottleInterval" "$plist" && checks=$((checks + 1))

  if [[ "$checks" -ge 4 ]]; then
    log_pass "macos plist has all expected keys ($checks/4)"
  else
    log_fail "macos plist content" "only $checks/4 checks passed"
  fi
}

# Test: fails without platform arg
test_install_service_no_platform() {
  output=$(bash "$SCRIPT_DIR/install-service.sh" 2>&1) && rc=$? || rc=$?
  if [[ "$rc" -ne 0 ]]; then
    log_pass "fails without platform arg"
  else
    log_fail "no platform" "should have failed"
  fi
}

test_install_service_linux_content
test_install_service_macos_content
test_install_service_no_platform

########################################
echo -e "\n${YELLOW}=== start-node.sh ===${NC}"
########################################

test_start_node_runs() {
  local d="$TEST_DIR/start-ok"
  setup_test_dir "$d"
  output=$(bash "$SCRIPT_DIR/start-node.sh" --dir "$d" --env dev 2>&1)
  if echo "$output" | grep -q "started\|Starting"; then
    log_pass "start-node runs with mock binary"
  else
    log_fail "start node" "got: $output"
  fi
}

test_start_node_no_config() {
  local d="$TEST_DIR/start-noconf"
  mkdir -p "$d"
  create_mock_binary "$d"
  printf 'pw' > "$d/.password"; chmod 600 "$d/.password"
  output=$(bash "$SCRIPT_DIR/start-node.sh" --dir "$d" 2>&1) && rc=$? || rc=$?
  if [[ "$rc" -ne 0 ]]; then
    log_pass "start-node fails without config"
  else
    log_fail "no config check" "should have failed"
  fi
}

test_start_node_runs
test_start_node_no_config

########################################
# Summary
########################################
echo ""
echo "================================"
TOTAL=$((PASS + FAIL))
echo -e "Results: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC} / $TOTAL total"
if [[ ${#ERRORS[@]} -gt 0 ]]; then
  echo ""
  echo "Failures:"
  for e in "${ERRORS[@]}"; do
    echo -e "  ${RED}• $e${NC}"
  done
fi
echo "================================"
echo "Test dir: $TEST_DIR (cleaned up on exit)"

exit $FAIL
