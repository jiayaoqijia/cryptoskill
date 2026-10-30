#!/usr/bin/env bash
set -euo pipefail

# `! cmd` is exempt from errexit, so negative assertions go through refute.
refute() { if "$@"; then echo "unexpected match: $*" >&2; exit 1; fi; }

root="$(mktemp -d)"
trap 'rm -rf "$root"' EXIT
bin="$root/bin"
validator="$root/node_modules/@farmslot/recipe-cli"
mkdir -p "$bin" "$validator/bin" "$validator/dist"
printf '%s\n' '{"name":"@deeeed/metamask-harness","version":"7.4.2","bin":{"mm-harness":"bin/mm-harness"}}' > "$root/package.json"
printf '%s\n' '{"name":"@farmslot/recipe-cli","version":"0.0.0","main":"dist/index.js"}' > "$validator/package.json"
printf '%s\n' 'export {};' > "$validator/dist/index.js"

cat >"$bin/mm-harness" <<'FAKE'
#!/usr/bin/env bash
set -euo pipefail
if [ "${1:-}" = update ]; then
  package_root="$(cd "$(dirname "$0")/.." && pwd -P)"
  current="$(node -p 'require(process.argv[1]).version' "$package_root/package.json")"
  printf '{"schemaVersion":1,"command":"update","current":"%s","latest":"%s","updateAvailable":false}\n' "$current" "$current"
  exit 0
fi
[ -z "${FAKE_LOG:-}" ] || printf '%s\n' "$*" >>"$FAKE_LOG"
case "${1:-}" in
  doctor)
    [ "${FAKE_DOCTOR_DELAY:-0}" != 1 ] || sleep 1
    printf '{"status":"pass","adapter":"%s"}\n' "$FAKE_ADAPTER"
    ;;
  status)
    case "${FAKE_DEVICES:-}" in
      ios) printf '{"status":"pass","adapter":"mobile","devices":[{"platform":"ios","selected":true}]}\n' ;;
      android) printf '{"status":"pass","adapter":"mobile","devices":[{"platform":"android","selected":true}]}\n' ;;
      *) printf '{"status":"pass","adapter":"%s","devices":[]}\n' "$FAKE_ADAPTER" ;;
    esac
    ;;
  launch)
    if [ "${FAKE_LAUNCH_DELAY:-0}" = 1 ]; then
      printf 'launch started\n'
      sleep 1
    fi
    printf 'launch pass\n'
    ;;
  fixtures)
    printf 'fixture application\n'
    [ "${FAKE_SET_FAIL:-0}" != 1 ] || exit 9
    ;;
  execution-template)
    shift
    node - "$@" <<'NODE'
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const [command, ...args] = process.argv.slice(2);
const values = new Map();
const repeated = new Map();
let output;
for (let index = 0; index < args.length; index += 1) {
  const arg = args[index];
  if (!arg.startsWith('-')) {
    if (command === 'materialize' && output === undefined) output = arg;
    continue;
  }
  if (arg === '--json') continue;
  const value = args[++index];
  if (arg === '--dir' || arg === '--domain-dir') {
    const rows = repeated.get(arg) ?? [];
    rows.push(value);
    repeated.set(arg, rows);
  } else {
    values.set(arg, value);
  }
}
const sources = [
  ...(repeated.get('--dir') ?? []).map((root, index) => ({
    root,
    sourceId: `dir-${index + 1}`,
    sourceKind: 'custom',
    labels: [],
  })),
  ...(repeated.get('--domain-dir') ?? []).map((value, index) => {
    const separator = value.indexOf('=');
    return {
      root: value.slice(separator + 1),
      sourceId: `team:${value.slice(0, separator)}`,
      sourceKind: 'workspace',
      labels: [`domain:${value.slice(0, separator)}`],
    };
  }),
  ...(values.has('--package-templates')
    ? [{
        root: values.get('--package-templates'),
        sourceId: `package:${values.get('--package-id') ?? 'shared'}`,
        sourceKind: 'package',
        labels: [],
      }]
    : []),
];
const requestedDomain = values.get('--domain');
const platformAliases = {
  core: ['core', 'cli'],
  extension: ['extension', 'chrome-extension'],
  mobile: ['mobile', 'ios', 'android'],
};
const entries = [];
for (const source of sources) {
  if (!fs.existsSync(source.root)) continue;
  for (const flow of fs.readdirSync(source.root)) {
    const flowDir = path.join(source.root, flow);
    if (!fs.statSync(flowDir).isDirectory()) continue;
    for (const file of fs.readdirSync(flowDir).filter((name) => name.endsWith('.md'))) {
      const stem = file.slice(0, -3);
      const platform = Object.keys(platformAliases).find((item) => stem.endsWith(`.${item}`));
      const text = fs.readFileSync(path.join(flowDir, file), 'utf8');
      entries.push({
        id: `${flow}/${stem}`,
        title: text.match(/^#\s+(.+)$/m)?.[1] ?? stem,
        description: text.match(/^description:\s*(.+)$/m)?.[1]?.trim(),
        flow,
        platforms: platform ? platformAliases[platform] : ['*'],
        labels: source.labels,
        relativePath: `${flow}/${file}`,
        sourceId: source.sourceId,
        sourceKind: source.sourceKind,
        sha256: crypto.createHash('sha256').update(text).digest('hex'),
        sourcePath: path.join(flowDir, file),
      });
    }
  }
}
const compatible = entries.filter((entry) =>
  (!values.has('--flow') || entry.flow === values.get('--flow')) &&
  (!values.has('--platform') || entry.platforms.includes('*') || entry.platforms.includes(values.get('--platform'))) &&
  (entry.labels.length === 0 || entry.labels.includes(`domain:${requestedDomain}`))
);
if (command === 'list') {
  // Mark shadowed entries: for each id, the first-source entry wins.
  const seen = new Map();
  for (const entry of compatible) {
    if (!seen.has(entry.id)) {
      seen.set(entry.id, entry.sourceId);
    } else {
      entry.shadowedBy = seen.get(entry.id);
    }
  }
  process.stdout.write(`${JSON.stringify({ templates: compatible.map(({ sourcePath, ...entry }) => entry) })}\n`);
  process.exit(0);
}
if (command === 'lint') {
  process.stdout.write(`${JSON.stringify({ ok: true, filesChecked: entries.length, issues: [] })}\n`);
  process.exit(0);
}
if (command !== 'materialize' || !output) process.exit(2);
const id = values.get('--id');
const selected = compatible.find((entry) => entry.id === id);
if (!selected) {
  process.stderr.write(`Execution template "${id}" is missing or incompatible. Compatible ids: ${compatible.map((entry) => entry.id).sort().join(', ')}.\n`);
  process.exit(1);
}
if (fs.existsSync(output)) {
  process.stderr.write(`destination already exists: ${output}\n`);
  process.exit(1);
}
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.copyFileSync(selected.sourcePath, output, fs.constants.COPYFILE_EXCL);
const renderedSha256 = crypto.createHash('sha256').update(fs.readFileSync(output)).digest('hex');
const reference = {
  id: selected.id,
  sourceId: selected.sourceId,
  flow: selected.flow,
  platforms: selected.platforms,
  labels: selected.labels,
  relativePath: selected.relativePath,
  sha256: selected.sha256,
  renderedSha256,
};
const provenance = {
  schemaVersion: 1,
  selectionReason: 'explicit',
  executionTemplate: reference,
};
const provenancePath = values.get('--provenance');
if (provenancePath) {
  fs.mkdirSync(path.dirname(provenancePath), { recursive: true });
  fs.writeFileSync(provenancePath, `${JSON.stringify(provenance, null, 2)}\n`, { flag: 'wx' });
}
process.stdout.write(`${JSON.stringify({ path: path.resolve(output), reference, provenance })}\n`);
NODE
    ;;
  task)
    shift
    [ "${1:-}" = init ] || exit 2
    shift
    fake_task_dir="${1:?}"
    shift
    fake_flow=""; fake_platform=""; fake_template=""; fake_title=""
    fake_domain=""; fake_ticket=""; fake_source_ref=""; fake_text=""; fake_text_file=""; fake_label=""
    fake_acceptance=()
    # Default mirrors the real producer: mark straight through this executable.
    fake_mark_cmd="$0 checklist mark"
    fake_sources=()
    while [ "$#" -gt 0 ]; do
      case "$1" in
        --flow) fake_flow="$2"; shift 2 ;;
        --platform) fake_platform="$2"; shift 2 ;;
        --template) fake_template="$2"; shift 2 ;;
        --title) fake_title="$2"; shift 2 ;;
        --domain) fake_domain="$2"; shift 2 ;;
        --ticket) fake_ticket="$2"; shift 2 ;;
        --source-ref) fake_source_ref="$2"; shift 2 ;;
        --task-text) fake_text="$2"; shift 2 ;;
        --acceptance) fake_acceptance+=("$2"); shift 2 ;;
        --task-file) fake_text_file="$2"; shift 2 ;;
        --task-dir-label) fake_label="$2"; shift 2 ;;
        --mark-command) fake_mark_cmd="$2"; shift 2 ;;
        --package-templates|--package-id|--dir|--domain-dir) fake_sources+=("$1" "$2"); shift 2 ;;
        --json) shift ;;
        *) echo "fake task init: unknown argument: $1" >&2; exit 2 ;;
      esac
    done
    materialize_args=(
      execution-template materialize "$fake_task_dir/CHECKLIST.md"
      --flow "$fake_flow" --platform "$fake_platform"
      --id "$fake_template" --json
    )
    [ -z "$fake_domain" ] || materialize_args+=(--domain "$fake_domain")
    # The nested call is an implementation detail of this producer, not a step the
    # skill asked for, so it stays out of the command log.
    selection="$(FAKE_LOG= "$0" "${materialize_args[@]}" ${fake_sources[@]+"${fake_sources[@]}"})" || exit $?
    {
      printf '# %s: %s\n\n' "$fake_flow" "$fake_title"
      printf '## Task\n\n```text\n'
      printf 'TICKET: %s\n' "$fake_ticket"
      case "$fake_source_ref" in
        http://*|https://*) printf 'TICKET_URL: %s\n' "$fake_source_ref" ;;
        *) printf 'SOURCE_REF: %s\n' "$fake_source_ref" ;;
      esac
      printf 'TITLE: %s\nFLOW: %s\nPLATFORM: %s\n' \
        "$fake_title" "$fake_flow" "$fake_platform"
      [ -z "$fake_domain" ] || printf 'DOMAIN: %s\n' "$fake_domain"
      printf 'TEMPLATE: %s\nTASK_DIR: %s\nSTATUS: pending\n```\n\n' "$fake_template" "$fake_label"
      printf '## Description\n\n'
      if [ -n "$fake_text_file" ]; then
        cat "$fake_text_file"
      elif [ -n "$fake_text" ]; then
        printf '%s\n' "$fake_text"
      else
        printf '_Provided in the conversation._\n'
      fi
      printf '\n## Acceptance Criteria\n\n'
      if [ "${#fake_acceptance[@]}" -gt 0 ]; then
        printf '%s\n' "${fake_acceptance[@]}"
      else
        printf '_Freeze the observable criteria here._\n'
      fi
      printf '\n'
      printf '## Checklist\n\nFollow `%s/CHECKLIST.md` top to bottom.\n' "$fake_label"
    } >"$fake_task_dir/TASK.md"
    {
      printf '#!/usr/bin/env bash\nset -euo pipefail\n'
      printf 'DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
      printf 'exec ${FARMSLOT_MARK_CMD:-%s} "$DIR" "$@"\n' "$fake_mark_cmd"
    } >"$fake_task_dir/mark"
    chmod +x "$fake_task_dir/mark"
    node - "$fake_task_dir" "$fake_flow" "$fake_domain" "$selection" "${fake_acceptance[@]}" <<'NODE'
const fs = require('node:fs');
const path = require('node:path');
const { randomUUID } = require('node:crypto');
const [dir, flow, domain, selectionJson, ...acceptanceCriteria] = process.argv.slice(2);
const { reference } = JSON.parse(selectionJson);
const report = flow === 'review-pr' ? 'artifacts/report.md' : 'artifacts/pr-description.md';
fs.mkdirSync(path.join(dir, 'inputs'), { recursive: true });
fs.writeFileSync(
  path.join(dir, 'inputs/handoff.json'),
  `${JSON.stringify({
    schemaVersion: 1,
    attemptId: randomUUID(),
    surface: 'skill',
    domain,
    flow,
    ...(acceptanceCriteria.length > 0 ? { task: { acceptanceCriteria } } : {}),
    taskDocument: 'TASK.md',
    report,
    learnings: 'artifacts/learnings.md',
    executionTemplate: { id: reference.id, sourceId: reference.sourceId },
  }, null, 2)}\n`,
);
fs.writeFileSync(
  path.join(dir, 'inputs/worker-terminal-contract.json'),
  `${JSON.stringify({ schemaVersion: 1, flowType: flow, requireSignal: true }, null, 2)}\n`,
);
NODE
    printf 'Task document: %s\n' "$fake_task_dir/TASK.md"
    printf 'Checklist: %s\n' "$fake_task_dir/CHECKLIST.md"
    ;;
  prepare)
    shift
    fake_platform=""; fake_mobile=""; fake_artifacts=""
    while [ "$#" -gt 0 ]; do
      case "$1" in
        --platform) fake_platform="$2"; shift 2 ;;
        --mobile-platform) fake_mobile="$2"; shift 2 ;;
        --artifacts-dir) fake_artifacts="$2"; shift 2 ;;
        --target) shift 2 ;;
        --json) shift ;;
        *) echo "fake prepare: unknown argument: $1" >&2; exit 2 ;;
      esac
    done
    mkdir -p "$fake_artifacts/prepare"
    fake_steps=""
    fake_fail=""
    emit_error() {
      node -e 'process.stdout.write(`${JSON.stringify({ schemaVersion: 1, ready: false, error: { userAction: process.argv[1] } })}\n`)' "$1"
      exit 1
    }
    run_step() {
      local id="$1"
      local label="$2"
      shift 2
      printf 'prepare: %s...\n' "$label" >&2
      if "$0" "$@" 2>&1 | tee "$fake_artifacts/prepare/$id.txt" >&2; then
        fake_steps="$fake_steps{\"id\":\"$id\",\"command\":\"$*\",\"status\":\"pass\",\"exitCode\":0,\"reportPath\":\"prepare/$id.txt\"},"
        return 0
      fi
      fake_fail="prepare: $label failed.
Resolve the reported problem, then rerun preparation."
      return 1
    }
    run_step doctor "doctor --fix" doctor --fix --json || emit_error "$fake_fail"
    run_step status "status" status --json || emit_error "$fake_fail"
    case "$fake_platform" in
      extension)
        run_step launch "launch --verify" launch --verify || emit_error "$fake_fail"
        run_step fixtures "fixtures set" fixtures set || emit_error "${FAKE_USER_ACTION:-$fake_fail}"
        ;;
      mobile)
        if [ -z "$fake_mobile" ]; then
          fake_mobile="$(node -e '
            const fs = require("node:fs");
            const value = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
            const selected = (value.devices || []).filter((device) => device && device.selected === true);
            const candidates = selected.length ? selected : (value.devices || []);
            const platforms = [...new Set(candidates.map((device) => device && device.platform).filter((item) => item === "ios" || item === "android"))];
            if (platforms.length === 1) process.stdout.write(platforms[0]);
          ' "$fake_artifacts/prepare/status.txt")"
        fi
        if [ -z "$fake_mobile" ]; then
          emit_error "prepare: choose the mobile target, then rerun preparation with it:
1. iOS     --mobile-platform ios
2. Android --mobile-platform android"
        fi
        run_step launch "launch $fake_mobile --verify" launch "$fake_mobile" --verify || emit_error "$fake_fail"
        run_step fixtures "fixtures set" fixtures set --platform "$fake_mobile" || emit_error "$fake_fail"
        ;;
      core)
        # Headless Core reads its fixture file directly; no launch, no live fixtures.
        ;;
    esac
    run_step verify "verify" verify --json || emit_error "$fake_fail"
    # A harness that exits 0 without a valid readiness record (older/faulty build).
    case "${FAKE_PREPARE_RECORD:-}" in
      missing) exit 0 ;;
      symlink) ln -s /dev/null "$fake_artifacts/sandbox.json"; exit 0 ;;
      not-ready) printf '{"schemaVersion":1,"ready":false,"steps":[]}\n' > "$fake_artifacts/sandbox.json"; exit 0 ;;
    esac
    node -e '
      const fs = require("node:fs");
      const [file, platform, mobilePlatform, executable, steps] = process.argv.slice(1);
      fs.writeFileSync(file, `${JSON.stringify({
        schemaVersion: 1,
        harness: { name: "fake-mm-harness", version: "0.0.0", source: "test", executable },
        platform,
        ...(mobilePlatform ? { mobilePlatform } : {}),
        steps: JSON.parse(`[${steps}]`),
        ready: true,
        recordedAt: new Date().toISOString(),
      }, null, 2)}\n`);
    ' "$fake_artifacts/sandbox.json" "$fake_platform" "$fake_mobile" "$0" "${fake_steps%,}"
    ;;
  checklist) ;;
  verify) printf '{"status":"pass","adapter":"%s"}\n' "$FAKE_ADAPTER" ;;
  *) exit 2 ;;
esac
FAKE
chmod +x "$bin/mm-harness"
export MM_HARNESS_BIN="$bin/mm-harness"

skill="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
init="$skill/scripts/init-template"

run_case() {
  local adapter="$1"
  local devices="$2"
  local task="$root/$adapter"
  local log="$root/$adapter.log"
  mkdir -p "$task"
  (
    cd "$root"
    PATH="$bin:$PATH" FAKE_LOG="$log" FAKE_ADAPTER="$adapter" FAKE_DEVICES="$devices" \
      "$init" --task-kind dev --platform "$adapter" --slug contract --task-dir "$task" --prepare >/dev/null
  )
  # sandbox.json is the single readiness record; the removed per-step files and
  # the checklist-target manifest must not come back.
  test -s "$task/artifacts/sandbox.json"
  test ! -e "$task/artifacts/sandbox.md"
  test ! -e "$task/checklist-target.json"
  test -s "$task/artifacts/harness-provenance.json"
  test ! -e "$task/closeout"
  test -s "$task/inputs/handoff.json"
  test -s "$task/inputs/worker-terminal-contract.json"
  test -x "$task/mark"
  # TASK.md is the task document; CHECKLIST.md is the only file with step boxes.
  test -s "$task/TASK.md"
  grep -q '^# dev: contract$' "$task/TASK.md"
  grep -q '^## Acceptance Criteria$' "$task/TASK.md"
  grep -q '/CHECKLIST.md` top to bottom' "$task/TASK.md"
  refute grep -q '^- \[ \]' "$task/TASK.md"
  # The readiness record names exactly the steps this platform runs.
  node - "$task" "$adapter" <<'NODE'
const fs = require('node:fs');
const path = require('node:path');
const [task, adapter] = process.argv.slice(2);
const sandbox = JSON.parse(fs.readFileSync(path.join(task, 'artifacts/sandbox.json'), 'utf8'));
if (sandbox.ready !== true || sandbox.platform !== adapter) process.exit(1);
const ids = sandbox.steps.map((step) => step.id).join(',');
const expected = adapter === 'core' ? 'doctor,status,verify' : 'doctor,status,launch,fixtures,verify';
if (ids !== expected) process.exit(1);
NODE
}

# The harness runs the same bring-up steps, in the same order, as before.
step_order() {
  grep -E '^(doctor --fix --json|status --json|launch( (ios|android))? --verify|fixtures set( --platform (ios|android))?|verify --json)$' "$1" | paste -sd '|' -
}

run_case extension ""
test "$(grep -c '^fixtures set$' "$root/extension.log")" -eq 1
test "$(step_order "$root/extension.log")" = "doctor --fix --json|status --json|launch --verify|fixtures set|verify --json"

run_case mobile ios
test "$(grep -c '^fixtures set --platform ios$' "$root/mobile.log")" -eq 1
test "$(step_order "$root/mobile.log")" = "doctor --fix --json|status --json|launch ios --verify|fixtures set --platform ios|verify --json"

run_case core ""
refute grep -q '^fixtures set' "$root/core.log"
refute grep -q '^launch' "$root/core.log"

# Long harness steps stream progress before completion while retaining the same artifact.
progress="$root/progress"
mkdir -p "$progress"
PATH="$bin:$PATH" "$init" --task-kind dev --platform extension --slug progress --task-dir "$progress" >/dev/null
PATH="$bin:$PATH" FAKE_LOG="$root/progress.log" FAKE_ADAPTER=extension FAKE_DOCTOR_DELAY=1 FAKE_LAUNCH_DELAY=1 \
  "$skill/scripts/prepare-sandbox" "$progress" --platform extension >"$root/progress.out" 2>"$root/progress.err" &
progress_pid=$!
for _ in $(seq 1 60); do
  grep -q '^prepare: doctor --fix\.\.\.$' "$root/progress.err" && break
  sleep 0.05
done
grep -q '^prepare: doctor --fix\.\.\.$' "$root/progress.err"
kill -0 "$progress_pid"
for _ in $(seq 1 60); do
  grep -q '^launch started$' "$root/progress.err" && break
  sleep 0.05
done
grep -q '^launch started$' "$root/progress.err"
kill -0 "$progress_pid"
wait "$progress_pid"
grep -q '^launch started$' "$progress/artifacts/prepare/launch.txt"

failed="$root/set-failure"
mkdir -p "$failed"
set +e
set_failure_output="$(
  cd "$root"
  PATH="$bin:$PATH" FAKE_LOG="$root/set-failure.log" FAKE_ADAPTER=extension FAKE_SET_FAIL=1 \
    "$init" --task-kind dev --platform extension --slug set-failure --task-dir "$failed" --prepare 2>&1
)"
status=$?
set -e
test "$status" -eq 1
test "$(grep -c '^fixtures set$' "$root/set-failure.log")" -eq 1
refute grep -q '^verify' "$root/set-failure.log"
test ! -e "$failed/artifacts/sandbox.json"
grep -q 'fixture application' "$failed/artifacts/prepare/fixtures.txt"
failure_line="$(grep -n '^prepare: fixtures set failed\.$' <<<"$set_failure_output" | cut -d: -f1)"
stop_line="$(grep -n '^STOP: no choice to make. Run the recovery above once, then rerun exactly this prepare-sandbox command synchronously:$' <<<"$set_failure_output" | cut -d: -f1)"
rerun_line="$(grep -n "^$skill/scripts/prepare-sandbox $failed --platform extension$" <<<"$set_failure_output" | cut -d: -f1)"
repeat_line="$(grep -n '^If the same failure repeats, stop and report it\.$' <<<"$set_failure_output" | cut -d: -f1)"
test "$failure_line" -lt "$stop_line"
test "$stop_line" -lt "$rerun_line"
test "$rerun_line" -lt "$repeat_line"

# When the harness userAction has numbered options, the original choice STOP lines appear.
numbered_failed="$root/numbered-failure"
mkdir -p "$numbered_failed"
set +e
numbered_output="$(
  cd "$root"
  PATH="$bin:$PATH" FAKE_LOG="$root/numbered-failure.log" FAKE_ADAPTER=extension FAKE_SET_FAIL=1 \
    FAKE_USER_ACTION="1. Use fixture A
2. Stop" \
    "$init" --task-kind dev --platform extension --slug numbered-failure --task-dir "$numbered_failed" --prepare 2>&1
)"
numbered_status=$?
set -e
test "$numbered_status" -eq 1
grep -qx 'STOP: show the exact numbered options from the output above; wait for a NEW human reply; do not rerun yet.' <<<"$numbered_output"
grep -qx 'After the human reply, run the selected recovery, then rerun exactly this prepare-sandbox command synchronously:' <<<"$numbered_output"
refute grep -q 'no choice to make' <<<"$numbered_output"

# A zero harness exit is not readiness: sandbox.json must be a regular file the
# harness wrote with ready: true, or prepare-sandbox stops with the rerun hint.
for record_mode in missing symlink not-ready; do
  bad="$root/record-$record_mode"
  mkdir -p "$bad/artifacts"
  set +e
  bad_output="$(
    cd "$root"
    PATH="$bin:$PATH" FAKE_ADAPTER=extension FAKE_PREPARE_RECORD="$record_mode" \
      "$skill/scripts/prepare-sandbox" "$bad" --platform extension 2>&1
  )"
  status=$?
  set -e
  test "$status" -eq 1
  refute grep -qx "$bad/artifacts/sandbox.json" <<<"$bad_output"
  case "$record_mode" in
    not-ready) grep -q 'does not report ready: true' <<<"$bad_output" ;;
    *) grep -q 'missing or not a regular file' <<<"$bad_output" ;;
  esac
  grep -Fq "$skill/scripts/prepare-sandbox $bad --platform extension" <<<"$bad_output"
done

# Harness-resolution recovery preserves an explicit platform because current
# execution templates intentionally do not embed the old Platform: line.
resolution_recovery="$root/resolution-recovery"
mkdir -p "$resolution_recovery"
node_dir="$(dirname "$(command -v node)")"
set +e
resolution_recovery_output="$(
  env -u MM_HARNESS_BIN PATH="$node_dir:/usr/bin:/bin" \
    "$skill/scripts/prepare-sandbox" "$resolution_recovery" --platform extension 2>&1
)"
resolution_recovery_status=$?
set -e
test "$resolution_recovery_status" -eq 1
grep -Fq "$skill/scripts/prepare-sandbox $resolution_recovery --platform extension --harness-choice 1" \
  <<<"$resolution_recovery_output"

choice="$root/mobile-choice"
mkdir -p "$choice"
set +e
choice_output="$(cd "$root" && PATH="$bin:$PATH" FAKE_LOG="$root/mobile-choice.log" FAKE_ADAPTER=mobile FAKE_DEVICES='' \
  "$init" --task-kind dev --platform mobile --slug choice --task-dir "$choice" --prepare 2>&1)"
choice_status=$?
set -e
test "$choice_status" -eq 1
grep -q '^1\. iOS' <<<"$choice_output"
grep -q '^2\. Android' <<<"$choice_output"
PATH="$bin:$PATH" FAKE_LOG="$root/mobile-choice.log" FAKE_ADAPTER=mobile FAKE_DEVICES='' \
  "$skill/scripts/prepare-sandbox" "$choice" --platform mobile --mobile-platform android >/dev/null
test "$(grep -c '^fixtures set --platform android$' "$root/mobile-choice.log")" -eq 1

# TASK.md description: --task-text alone, --task-file alone, and file precedence when both are given.
desc_root="$root/description"
mkdir -p "$desc_root"
printf 'From the file\nsecond line\n' >"$desc_root/task.md"
PATH="$bin:$PATH" "$init" --task-kind dev --platform extension --slug text-only --task-dir "$desc_root/text" --task-text 'Only the text' >/dev/null
grep -q '^Only the text$' "$desc_root/text/TASK.md"
PATH="$bin:$PATH" FAKE_LOG="$desc_root/acceptance.log" "$init" --task-kind qa --platform extension --slug criteria --task-dir "$desc_root/criteria" --task-text 'Check both' --acceptance 'First criterion' --acceptance 'Second criterion' >/dev/null
grep -Fq -- '--acceptance First criterion --acceptance Second criterion' "$desc_root/acceptance.log"
node -e 'const assert=require("node:assert/strict");const fs=require("node:fs");assert.deepEqual(JSON.parse(fs.readFileSync(process.argv[1],"utf8")).task.acceptanceCriteria,["First criterion","Second criterion"])' "$desc_root/criteria/inputs/handoff.json"
grep -q '^First criterion$' "$desc_root/criteria/TASK.md"
grep -q '^Second criterion$' "$desc_root/criteria/TASK.md"
PATH="$bin:$PATH" "$init" --task-kind dev --platform extension --slug file-only --task-dir "$desc_root/file" --task-file "$desc_root/task.md" >/dev/null
grep -q '^From the file$' "$desc_root/file/TASK.md"
grep -q '^SOURCE_REF: task.md$' "$desc_root/file/TASK.md"
test ! -e "$desc_root/file/PROMPT.md"
PATH="$bin:$PATH" "$init" --task-kind dev --platform extension --slug both --task-dir "$desc_root/both" --task-file "$desc_root/task.md" --task-text 'Only the text' >/dev/null
grep -q '^From the file$' "$desc_root/both/TASK.md"
refute grep -q '^Only the text$' "$desc_root/both/TASK.md"

# Autonomous handoff is script-owned and fixed; no mode flag exists.
handoff_root="$root/handoff"
autonomous_out="$(PATH="$bin:$PATH" "$init" --task-kind dev --platform mobile --slug coffee --task-dir "$handoff_root/autonomous")"
test "$(printf '%s\n' "$autonomous_out" | tail -1)" = "$handoff_root/autonomous/CHECKLIST.md"
# Steerability: a custom template with a HUMAN GATE row is selectable and keeps the row.
steer_templates="$root/steer-templates"
mkdir -p "$steer_templates/dev"
cat > "$steer_templates/dev/guided.mobile.md" <<'TEMPLATE'
---
platforms: [mobile, ios, android]
description: Custom guided template for steerability test.
---
# Custom guided checklist

- [ ] 1. Reproduce the issue.
- [ ] 2. HUMAN GATE — confirm reproduction before proceeding.
- [ ] 3. Fix and validate.
TEMPLATE
steer_list="$(RECIPE_COOK_TEMPLATES_DIRS="$steer_templates" PATH="$bin:$PATH" \
  "$skill/scripts/list-templates" --task-kind dev --platform mobile 2>&1)"
grep -q 'dev/guided.mobile' <<<"$steer_list"
RECIPE_COOK_TEMPLATES_DIRS="$steer_templates" PATH="$bin:$PATH" \
  "$init" --task-kind dev --platform mobile \
  --template dev/guided.mobile --slug guided --task-dir "$handoff_root/guided" >/dev/null
grep -q 'HUMAN GATE' "$handoff_root/guided/CHECKLIST.md"

# The task-local marker delegates terminal closeout to mm-harness through the
# task-local front door, so every mark re-verifies the locked harness receipt
# instead of trusting a bare executable path.
grep -Fq '"$DIR/mm-harness" checklist mark' "$handoff_root/autonomous/mark"
FAKE_LOG="$root/handoff-mark-harness.log" \
  "$handoff_root/autonomous/mark" complete --mark-last
grep -qx "checklist mark $handoff_root/autonomous complete --mark-last" "$root/handoff-mark-harness.log"

set +e
invalid_domain_output="$(PATH="$bin:$PATH" "$init" --task-kind dev \
  --platform core --domain 'perps team' --task-dir "$root/invalid-domain" 2>&1)"
invalid_domain_status=$?
set -e
test "$invalid_domain_status" -eq 2
grep -q '^--domain must match ' <<<"$invalid_domain_output"

# Domains name subtasks (`<domain>-review`), whose ids allow only [a-z0-9-].
set +e
underscore_domain_output="$(PATH="$bin:$PATH" "$init" --task-kind dev --platform core \
  --domain money_movement --task-dir "$root/underscore-domain" 2>&1)"
underscore_domain_status=$?
set -e
test "$underscore_domain_status" -eq 2
grep -q '^--domain must match ' <<<"$underscore_domain_output"

explicit_domain="$root/explicit-domain"
PATH="$bin:$PATH" "$init" --task-kind dev --platform core \
  --domain perps --task-dir "$explicit_domain" >/dev/null
node -e 'if (require(process.argv[1]).domain !== "perps") process.exit(1)' \
  "$explicit_domain/inputs/handoff.json"

# Exact template IDs resolve directly, including custom overlays.
custom_templates="$root/custom-templates"
mkdir -p "$custom_templates/dev"
cat > "$custom_templates/dev/performance-autonomous.extension.md" <<'TEMPLATE'
## Custom performance checklist
TEMPLATE
custom_task="$root/custom-choice"
RECIPE_COOK_TEMPLATES_DIRS="$custom_templates" PATH="$bin:$PATH" \
  "$init" --task-kind dev --platform extension \
  --template dev/performance-autonomous.extension --task-dir "$custom_task" >/dev/null
grep -q '^## Custom performance checklist$' "$custom_task/CHECKLIST.md"
test ! -e "$custom_task/inputs/execution-template.json"
node -e '
  const value = require(process.argv[1]);
  if (value.executionTemplate.id !== "dev/performance-autonomous.extension") process.exit(1);
  if (value.executionTemplate.sourceId !== "dir-1") process.exit(1);
' "$custom_task/inputs/handoff.json"

# Named runtime libraries remain domain-scoped and use stable team source ids.
team_perps="$root/team-perps"
team_money="$root/team-money"
mkdir -p "$team_perps/checklists/dev" "$team_money/checklists/dev"
cp "$custom_templates/dev/performance-autonomous.extension.md" \
  "$team_perps/checklists/dev/performance-autonomous.extension.md"
cp "$custom_templates/dev/performance-autonomous.extension.md" \
  "$team_money/checklists/dev/performance-autonomous.extension.md"
team_task="$root/team-choice"
RECIPE_LIBRARY_PATH="perps=$team_perps:money-movement=$team_money" PATH="$bin:$PATH" \
  "$init" --task-kind dev --platform extension --domain perps \
  --template dev/performance-autonomous.extension --task-dir "$team_task" >/dev/null
node -e '
  const value = require(process.argv[1]);
  if (value.executionTemplate.sourceId !== "team:perps") process.exit(1);
' "$team_task/inputs/handoff.json"

# Domain selection requires a named team root instead of guessing ownership
# from the caller's selected domain.
set +e
unnamed_domain_output="$(
  RECIPE_LIBRARY_PATH="$team_perps" PATH="$bin:$PATH" \
    "$init" --task-kind dev --platform extension --domain perps \
      --task-dir "$root/unnamed-domain" 2>&1
)"
unnamed_domain_status=$?
set -e
test "$unnamed_domain_status" -eq 2
grep -q 'name team libraries as <domain>=<path>' <<<"$unnamed_domain_output"

# A team library without checklists contributes recipes/actions only. Its other
# directories must never be scanned as execution templates.
team_without_checklists="$root/team-without-checklists"
mkdir -p "$team_without_checklists/dev"
cp "$custom_templates/dev/performance-autonomous.extension.md" \
  "$team_without_checklists/dev/unrelated.extension.md"
fallback_json="$(
  RECIPE_LIBRARY_PATH="money-movement=$team_without_checklists" PATH="$bin:$PATH" \
    "$skill/scripts/list-templates" --task-kind dev \
      --platform extension --domain money-movement --json
)"
node -e '
  const rows = JSON.parse(process.argv[1]).templates;
  if (!rows.some((row) => row.sourceId === "package:consensys-recipe-cook")) process.exit(1);
  if (rows.some((row) => row.sourceId === "team:money-movement")) process.exit(1);
' "$fallback_json"

# An unnamed recipe-only library is also irrelevant to template discovery and
# must not block a domain-scoped canonical fallback.
unnamed_fallback_json="$(
  RECIPE_LIBRARY_PATH="$team_without_checklists" PATH="$bin:$PATH" \
    "$skill/scripts/list-templates" --task-kind dev \
      --platform extension --domain money-movement --json
)"
node -e '
  const rows = JSON.parse(process.argv[1]).templates;
  if (!rows.some((row) => row.sourceId === "package:consensys-recipe-cook")) process.exit(1);
' "$unnamed_fallback_json"

set +e
unknown_template_output="$(RECIPE_COOK_TEMPLATES_DIRS="$custom_templates" PATH="$bin:$PATH" \
  "$init" --task-kind dev --platform extension \
  --template dev/missing-autonomous.extension --task-dir "$root/missing-choice" 2>&1)"
unknown_template_status=$?
set -e
test "$unknown_template_status" -eq 1
grep -q 'Execution template "dev/missing-autonomous.extension" is missing or incompatible' <<<"$unknown_template_output"
grep -q 'dev/performance-autonomous.extension' <<<"$unknown_template_output"
grep -q 'dev/extension' <<<"$unknown_template_output"

# The list surface returns portable catalog rows without local paths.
catalog_json="$(PATH="$bin:$PATH" "$skill/scripts/list-templates" --task-kind dev --platform extension --json)"
node -e '
  const rows = JSON.parse(process.argv[1]).templates;
  if (!rows.length || rows.some((row) => row.flow !== "dev")) process.exit(1);
  if (rows.some((row) => "path" in row || "sourcePath" in row)) process.exit(1);
' "$catalog_json"
catalog_text="$(PATH="$bin:$PATH" "$skill/scripts/list-templates" --task-kind dev --platform extension)"
grep -q 'Extension dev checklist with runtime proof.' <<<"$catalog_text"

# Fresh installations can discover the bundled catalog before choosing the
# task-local harness installation offered by init-template.
no_harness_bin="$root/no-harness-bin"
mkdir -p "$no_harness_bin"
ln -s "$(command -v node)" "$no_harness_bin/node"
bundled_catalog="$(
  env -u MM_HARNESS_BIN PATH="$no_harness_bin:/usr/bin:/bin" \
    "$skill/scripts/list-templates" --task-kind dev \
      --platform extension --json
)"
node -e '
  const rows = JSON.parse(process.argv[1]).templates;
  if (rows.length !== 1 || rows[0].id !== "dev/extension") process.exit(1);
  if (rows[0].sourceId !== "package:consensys-recipe-cook") process.exit(1);
' "$bundled_catalog"

# The six bundled interactive ids are gone; SELECT still names the default id.
for _flow in dev fix-bug; do
  for _platform in mobile extension core; do
    _deleted_json="$(env -u MM_HARNESS_BIN PATH="$no_harness_bin:/usr/bin:/bin" \
      "$skill/scripts/list-templates" --task-kind "$_flow" --platform "$_platform" --json)"
    node -e '
      const rows = JSON.parse(process.argv[1]).templates;
      if (rows.some((row) => row.id.includes("interactive"))) process.exit(1);
    ' "$_deleted_json"
    _select_out="$(env -u MM_HARNESS_BIN PATH="$no_harness_bin:/usr/bin:/bin" \
      "$skill/scripts/list-templates" --task-kind "$_flow" --platform "$_platform")"
    grep -q "SELECT: $_flow/$_platform" <<<"$_select_out"
  done
done

set +e
external_without_harness="$(
  env -u MM_HARNESS_BIN PATH="$no_harness_bin:/usr/bin:/bin" \
    "$skill/scripts/list-templates" --templates-dir "$custom_templates" \
      --task-kind dev --platform extension --json 2>&1
)"
external_without_harness_status=$?
set -e
test "$external_without_harness_status" -eq 1
grep -q 'mm-harness is required to discover external template sources' <<<"$external_without_harness"

set +e
legacy_output="$(PATH="$bin:$PATH" "$skill/scripts/list-templates" --flow dev --platform extension 2>&1)"
legacy_status=$?
set -e
test "$legacy_status" -eq 2
grep -q '^Unknown arg: --flow$' <<<"$legacy_output"

# --mode is removed; both scripts reject it as unknown.
set +e
mode_list_output="$(PATH="$bin:$PATH" "$skill/scripts/list-templates" --task-kind dev --platform extension --mode autonomous 2>&1)"
mode_list_status=$?
set -e
test "$mode_list_status" -eq 2
grep -q '^Unknown arg: --mode$' <<<"$mode_list_output"

set +e
mode_init_output="$(PATH="$bin:$PATH" "$init" --task-kind dev --platform extension --mode autonomous --task-dir "$root/mode-check" 2>&1)"
mode_init_status=$?
set -e
test "$mode_init_status" -eq 2
grep -q '^Unknown arg: --mode$' <<<"$mode_init_output"

# Resume mode reuses the exact materialized task and never creates another checklist.
resume_count_before="$(find "$custom_task" -name CHECKLIST.md -type f | wc -l | tr -d ' ')"
resume_output="$("$init" --resume-task-dir "$custom_task")"
test "$resume_output" = "$custom_task/CHECKLIST.md"
resume_count_after="$(find "$custom_task" -name CHECKLIST.md -type f | wc -l | tr -d ' ')"
test "$resume_count_before" = 1
test "$resume_count_after" = 1

# Resume requires a real CHECKLIST.md file: a missing one is not resumable.
invalid_resume="$root/invalid-resume"
mkdir -p "$invalid_resume"
set +e
"$init" --resume-task-dir "$invalid_resume" >/dev/null 2>&1
invalid_resume_status=$?
set -e
test "$invalid_resume_status" -eq 1

# A symlinked checklist escapes the task directory and is rejected too.
outside_checklist="$root/outside-checklist.md"
printf '# Outside\n' >"$outside_checklist"
ln -s "$outside_checklist" "$invalid_resume/CHECKLIST.md"
set +e
"$init" --resume-task-dir "$invalid_resume" >/dev/null 2>&1
invalid_resume_status=$?
set -e
test "$invalid_resume_status" -eq 1

# Fixture/setup recovery instructions follow printed recovery lines.
grep -q 'If preparation fails, follow the printed recovery lines' "$skill/skill.md"
grep -q 'A one-character reply selects that item; also accept its exact ID' "$skill/skill.md"
grep -q 'require that exact ID in `.templates\[\]`' "$skill/skill.md"
grep -q 'Never fuzzy-match or substitute' "$skill/skill.md"
grep -q 'Never create a second task/checklist' "$skill/skill.md"
grep -q 'references/team-libraries.md' "$skill/skill.md"
grep -q 'On the first deterministic-state mutation failure, stop: do not tune parameters, retry, or switch mutation actions' "$skill/skill.md"
grep -q 'never run `yarn skills` or another skill install/update/sync command' "$skill/skill.md"
grep -q 'mm-harness help --json' "$skill/skill.md"
grep -q 'Never put secrets in reports or learnings' "$skill/skill.md"
grep -q 'mm-harness checklist closeout <task> --share' "$skill/skill.md"
shared_rules="$skill/references/dev-fix-bug.md"
grep -q 'check diff \[--fix\] --artifacts-dir <task>/artifacts' "$shared_rules"
grep -q 'The default fast profile skips typecheck' "$shared_rules"
grep -q 'Do not substitute repo build/typecheck for the fast-profile skip' "$shared_rules"
grep -q 'Require PASS before marking the gate; UI flows retain `validation-summary.json`' "$shared_rules"
for template in "$skill"/references/templates/{dev,fix-bug}/{core,extension,mobile}.md; do
  grep -q 'Read and apply .*references/dev-fix-bug.md' "$template"
done
grep -q "follow Cook's Finish before marking no-change" "$shared_rules"
for template in "$skill"/references/templates/fix-bug/*.md; do
  refute grep -q 'closeout\|--share' "$template"
done

# list-templates SELECT vs STOP: uses fake harness (MM_HARNESS_BIN is set).
# (a) no library: SELECT names dev/mobile from package:consensys-recipe-cook, no STOP.
lt_a="$(PATH="$bin:$PATH" "$skill/scripts/list-templates" --task-kind dev --platform mobile 2>&1)"
grep -q 'SELECT: dev/mobile from package:consensys-recipe-cook' <<<"$lt_a"
refute grep -q '^STOP:' <<<"$lt_a"

# (b) team library shadows generic one AND has extra variant: SELECT shows team sourceId, no STOP.
team_lib_b="$root/team-lib-b"
mkdir -p "$team_lib_b/checklists/dev"
printf '# Mobile dev checklist\n' >"$team_lib_b/checklists/dev/mobile.md"
printf '# Rendering network autonomous\n' >"$team_lib_b/checklists/dev/rendering-network-autonomous.mobile.md"
lt_b="$(PATH="$bin:$PATH" RECIPE_LIBRARY_PATH="myteam=$team_lib_b" \
  "$skill/scripts/list-templates" --task-kind dev --platform mobile --domain myteam 2>&1)"
grep -q 'SELECT: dev/mobile from team:myteam' <<<"$lt_b"
grep -q 'dev/rendering-network-autonomous.mobile' <<<"$lt_b"
refute grep -q '^STOP:' <<<"$lt_b"

# (c) qa defaults to qa/default like any other flow: SELECT, never STOP.
lt_c="$(PATH="$bin:$PATH" "$skill/scripts/list-templates" --task-kind qa --platform extension 2>&1)"
grep -q '^SELECT: qa/default from ' <<<"$lt_c"
refute grep -q '^STOP:' <<<"$lt_c"

# (d) an unscoped request names no flow: SELECT dev/<platform> so a headless run proceeds.
lt_d="$(PATH="$bin:$PATH" "$skill/scripts/list-templates" --platform extension 2>&1)"
grep -q '^SELECT: dev/extension from ' <<<"$lt_d"
refute grep -q '^STOP:' <<<"$lt_d"

echo 'recipe-cook task init + prepare: step order, sandbox.json readiness, failure/core N/A, and mark delegation passed'
