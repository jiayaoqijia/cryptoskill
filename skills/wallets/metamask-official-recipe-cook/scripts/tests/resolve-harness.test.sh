#!/usr/bin/env bash
set -euo pipefail

root="$(mktemp -d)"
root="$(cd "$root" && pwd -P)"
trap 'rm -rf "$root"' EXIT
skill="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
resolver="$skill/scripts/resolve-harness"
init="$skill/scripts/init-template"
# shellcheck source=../scripts/harness-package-policy
source "$skill/scripts/harness-package-policy"
real_node="$(command -v node)"
mkdir -p "$root/clean-bin"
ln -s "$real_node" "$root/clean-bin/node"
clean_path="$root/clean-bin:/usr/bin:/bin:/usr/sbin:/sbin"

current_version="7.4.2"
older_version="7.4.1"
newer_version="7.4.3"

make_harness() {
  local dir="$1"
  local version="${2:-$current_version}"
  local validator="$dir/node_modules/@farmslot/recipe-cli"
  mkdir -p "$dir/bin" "$dir/dist" "$dir/adapters" "$dir/library" "$validator/dist"
  node - "$dir/package.json" "$HARNESS_PACKAGE_NAME" "$version" <<'NODE'
const fs = require('node:fs');
const [file, name, version] = process.argv.slice(2);
fs.writeFileSync(file, `${JSON.stringify({
  name,
  version,
  repository: { type: 'git', url: 'https://github.com/MetaMask/experimental-metamask-harness.git' },
})}\n`);
NODE
  cat > "$dir/bin/mm-harness" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
package_root="$(cd "$(dirname "$0")/.." && pwd -P)"
current="$(node -p 'require(process.argv[1]).version' "$package_root/package.json")"
if [ "${1:-}" = "update" ]; then
  case "${FAKE_UPDATE_MODE:-ok}" in
    offline)
      printf '%s\n' "{\"schemaVersion\":1,\"command\":\"update\",\"status\":\"fail\",\"current\":\"$current\",\"error\":{\"code\":\"REGISTRY_UNREACHABLE\"}}"
      exit 3
      ;;
    invalid)
      printf '%s\n' 'not-json'
      exit 0
      ;;
  esac
  latest="${FAKE_LATEST_VERSION:-$current}"
  if [ "$latest" = "$current" ]; then
    printf '%s\n' "{\"schemaVersion\":1,\"command\":\"update\",\"current\":\"$current\",\"latest\":\"$latest\",\"updateAvailable\":false}"
    exit 0
  fi
  printf '%s\n' "{\"schemaVersion\":1,\"command\":\"update\",\"current\":\"$current\",\"latest\":\"$latest\",\"updateAvailable\":true}"
  exit 1
fi
if [ -n "${FAKE_HARNESS_LOG:-}" ]; then
  printf '%s\n' "$*" >> "$FAKE_HARNESS_LOG"
fi
if [ "${1:-}" = task ] && [ "${2:-}" = init ]; then
  init_dir="${3:?}"
  shift 3
  templates=""
  template_id=""
  mark_cmd="$0 checklist mark"
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --package-templates) templates="$2"; shift 2 ;;
      --template) template_id="$2"; shift 2 ;;
      --mark-command) mark_cmd="$2"; shift 2 ;;
      --json) shift ;;
      --*) shift 2 ;;
      *) shift ;;
    esac
  done
  source_template="$templates/$template_id.md"
  [ -f "$source_template" ] || exit 1
  mkdir -p "$init_dir/inputs"
  cp "$source_template" "$init_dir/CHECKLIST.md"
  printf '# task\n' > "$init_dir/TASK.md"
  printf '{"schemaVersion":1,"surface":"skill"}\n' > "$init_dir/inputs/handoff.json"
  # The caller's --mark-command decides how the marker reaches the harness.
  {
    printf '#!/usr/bin/env bash\nset -euo pipefail\n'
    printf 'DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
    printf 'exec ${FARMSLOT_MARK_CMD:-%s} "$DIR" "$@"\n' "$mark_cmd"
  } > "$init_dir/mark"
  chmod +x "$init_dir/mark"
  exit 0
fi
if [ "${1:-}" = execution-template ] && [ "${2:-}" = materialize ]; then
  output="${3:?}"
  shift 3
  templates=""
  template_id=""
  provenance=""
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --package-templates) templates="$2"; shift 2 ;;
      --id) template_id="$2"; shift 2 ;;
      --provenance) provenance="$2"; shift 2 ;;
      --flow|--platform|--domain|--package-id) shift 2 ;;
      --json) shift ;;
      *) shift ;;
    esac
  done
  source="$templates/$template_id.md"
  [ -f "$source" ] || exit 1
  mkdir -p "$(dirname "$output")" "$(dirname "$provenance")"
  cp "$source" "$output"
  node - "$source" "$template_id" "$provenance" <<'NODE'
const crypto = require('node:crypto');
const fs = require('node:fs');
const [source, id, destination] = process.argv.slice(2);
const text = fs.readFileSync(source);
const sha256 = crypto.createHash('sha256').update(text).digest('hex');
fs.writeFileSync(destination, `${JSON.stringify({
  schemaVersion: 1,
  selectionReason: 'explicit',
  executionTemplate: {
    id,
    sourceId: 'package:consensys-recipe-cook',
    flow: id.split('/')[0],
    platforms: ['*'],
    labels: [],
    relativePath: `${id}.md`,
    sha256,
    renderedSha256: sha256,
  },
}, null, 2)}\n`);
NODE
fi
SH
  chmod +x "$dir/bin/mm-harness"
  printf '%s\n' 'implementation-v1' > "$dir/library/implementation.js"
  printf '%s\n' '{"name":"@farmslot/recipe-cli","version":"0.0.0","main":"dist/index.js"}' > "$validator/package.json"
  printf '%s\n' 'export {};' > "$validator/dist/index.js"
}

override="$root/override"
path_harness="$root/path-harness"
make_harness "$override" "$older_version"
make_harness "$path_harness" "$current_version"

# An explicit source override wins without a registry check. It records the
# exact package/tree and, for a checkout, revision plus working-tree identity.
override_task="$root/override-task"
mkdir -p "$override_task"
FAKE_UPDATE_MODE=offline FAKE_HARNESS_LOG="$root/unused.log" PATH="$path_harness/bin:$clean_path" MM_HARNESS_BIN="$override/bin/mm-harness" \
  "$resolver" "$override_task" > "$root/override.path"
test "$(cat "$root/override.path")" = "$(cd "$override/bin" && pwd)/mm-harness"
node -e '
  const j=require(process.argv[1]);
  if (j.package.name!==process.argv[2] || j.package.version!==process.argv[3]) process.exit(1);
  if (j.source.kind!=="MM_HARNESS_BIN" || !/^[a-f0-9]{64}$/.test(j.entrySha256) || !/^[a-f0-9]{64}$/.test(j.packageTreeSha256)) process.exit(1);
' "$override_task/artifacts/harness-provenance.json" "$HARNESS_PACKAGE_NAME" "$older_version"

# A recorded version recommends; the current configured runtime wins on resume.
old_pool="$root/old-pool"
new_pool="$root/new-pool"
make_harness "$old_pool" "0.94.1"
make_harness "$new_pool" "0.94.6"
pool_task="$root/pool-task"
mkdir -p "$pool_task"
PATH="$clean_path" MM_HARNESS_BIN="$old_pool/bin/mm-harness" "$resolver" "$pool_task" >/dev/null
pool_receipt_before="$(shasum -a 256 "$pool_task/artifacts/harness-provenance.json" | awk '{print $1}')"
pool_resolved="$(PATH="$clean_path" MM_HARNESS_BIN="$new_pool/bin/mm-harness" "$resolver" "$pool_task" --verify-only 2>"$root/pool-warning")"
test "$pool_resolved" = "$new_pool/bin/mm-harness"
grep -q 'recommended harness 0.94.1; using 0.94.6' "$root/pool-warning"
test "$pool_receipt_before" = "$(shasum -a 256 "$pool_task/artifacts/harness-provenance.json" | awk '{print $1}')"
# Normal resolution records the selected runtime; verification never rewrites the receipt.
PATH="$clean_path" MM_HARNESS_BIN="$new_pool/bin/mm-harness" "$resolver" "$pool_task" >/dev/null
node -e 'if(require(process.argv[1]).package.version!=="0.94.6")process.exit(1)' "$pool_task/artifacts/harness-provenance.json"

# Runtime verification returns the selected executable without rewriting provenance.
refreshed_task="$root/refreshed-return-task"
mkdir -p "$refreshed_task"
PATH="$clean_path" MM_HARNESS_BIN="$old_pool/bin/mm-harness" "$resolver" "$refreshed_task" >/dev/null
cp "$refreshed_task/artifacts/harness-provenance.json" "$root/standalone-receipt.json"
refreshed="$(PATH="$clean_path" MM_HARNESS_BIN="$new_pool/bin/mm-harness" node "$skill/scripts/verify-harness.mjs" "$refreshed_task" --runtime)"
test "$refreshed" = "$new_pool/bin/mm-harness"
cmp "$root/standalone-receipt.json" "$refreshed_task/artifacts/harness-provenance.json"
# A path-only change has the same read-only contract.
same_version="$root/same-version"
make_harness "$same_version" "0.94.1"
same_resolved="$(PATH="$clean_path" MM_HARNESS_BIN="$same_version/bin/mm-harness" "$resolver" "$refreshed_task" --verify-only)"
test "$same_resolved" = "$same_version/bin/mm-harness"
cmp "$root/standalone-receipt.json" "$refreshed_task/artifacts/harness-provenance.json"

# A valid receipt is the task lock: it is reused before PATH/registry resolution,
# even when latest changes. Implementation drift invalidates and refreshes it.
receipt_before="$(shasum -a 256 "$override_task/artifacts/harness-provenance.json" | awk '{print $1}')"
FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$override_task" >/dev/null
receipt_after="$(shasum -a 256 "$override_task/artifacts/harness-provenance.json" | awk '{print $1}')"
test "$receipt_before" = "$receipt_after"
verified="$(FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$override_task" --verify-only)"
test "$verified" = "$(cd "$override/bin" && pwd)/mm-harness"
tree_before="$(node -p 'require(process.argv[1]).packageTreeSha256' "$override_task/artifacts/harness-provenance.json")"
entry_before="$(node -p 'require(process.argv[1]).entrySha256' "$override_task/artifacts/harness-provenance.json")"
# Runner session bookkeeping must not invalidate a frozen executable tree.
# The same exclusion applies to transitive validator packages.
mkdir -p "$override/dist/.omc/state/sessions/test" "$override/node_modules/@farmslot/recipe-cli/dist/.omx/state"
printf '%s\n' '{"lastTool":"build"}' > "$override/dist/.omc/state/sessions/test/tool.json"
printf '%s\n' '{"tick":1}' > "$override/node_modules/@farmslot/recipe-cli/dist/.omx/state/run.json"
FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$override_task" --verify-only >/dev/null
printf '%s\n' '{"lastTool":"verify"}' > "$override/dist/.omc/state/sessions/test/tool.json"
FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$override_task" --verify-only >/dev/null
test "$receipt_before" = "$(shasum -a 256 "$override_task/artifacts/harness-provenance.json" | awk '{print $1}')"
# Unrelated added implementation remains part of the lock.
printf '%s\n' 'new implementation' > "$override/dist/new-code.js"
if FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$override_task" --verify-only > /dev/null 2>&1; then
  echo 'new implementation unexpectedly passed provenance verification' >&2
  exit 1
fi
rm "$override/dist/new-code.js"
printf '%s\n' '// validator drift' >> "$override/node_modules/@farmslot/recipe-cli/dist/index.js"
set +e
validator_output="$(FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$override_task" --verify-only 2>&1)"
validator_status=$?
set -e
test "$validator_status" -eq 1
grep -q 'harness provenance is missing, stale, or invalid' <<< "$validator_output"
printf '%s\n' 'export {};' > "$override/node_modules/@farmslot/recipe-cli/dist/index.js"
node - "$override_task/artifacts/harness-provenance.json" "$path_harness" "$override" <<'NODE'
const fs = require('node:fs');
const [receiptPath, wrongRoot, correctRoot] = process.argv.slice(2);
const receipt = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
receipt.source.packageRoot = wrongRoot;
fs.writeFileSync(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`);
NODE
set +e
root_output="$(FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$override_task" --verify-only 2>&1)"
root_status=$?
set -e
test "$root_status" -eq 1
grep -q 'harness provenance is missing, stale, or invalid' <<< "$root_output"
node - "$override_task/artifacts/harness-provenance.json" "$override" <<'NODE'
const fs = require('node:fs');
const [receiptPath, correctRoot] = process.argv.slice(2);
const receipt = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
receipt.source.packageRoot = correctRoot;
fs.writeFileSync(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`);
NODE
printf '%s\n' 'implementation-v2' > "$override/library/implementation.js"
set +e
verify_output="$(FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$override_task" --verify-only 2>&1)"
verify_status=$?
set -e
test "$verify_status" -eq 1
grep -q 'harness provenance is missing, stale, or invalid' <<< "$verify_output"
tree_output="$(FAKE_HARNESS_LOG="$root/unused.log" PATH="$clean_path" MM_HARNESS_BIN="$override/bin/mm-harness" \
  "$resolver" "$override_task" 2>&1)"
grep -q 'existing harness provenance is stale or invalid' <<< "$tree_output"
tree_after="$(node -p 'require(process.argv[1]).packageTreeSha256' "$override_task/artifacts/harness-provenance.json")"
entry_after="$(node -p 'require(process.argv[1]).entrySha256' "$override_task/artifacts/harness-provenance.json")"
test "$tree_before" != "$tree_after"
test "$entry_before" = "$entry_after"

checkout="$root/checkout"
make_harness "$checkout" "$older_version"
git -C "$checkout" init -q
git -C "$checkout" add .
git -C "$checkout" -c user.name=contract -c user.email=contract@example.invalid commit -qm initial
checkout_task="$checkout/temp/task"
mkdir -p "$checkout_task"
FAKE_HARNESS_LOG="$root/unused.log" PATH="$clean_path" MM_HARNESS_BIN="$checkout/bin/mm-harness" \
  "$resolver" "$checkout_task" >/dev/null
node -e '
  const j=require(process.argv[1]);
  if(!/^[a-f0-9]{40,64}$/.test(j.source.revision) || j.source.dirty!==false || !/^[a-f0-9]{64}$/.test(j.source.workingTreeSha256))process.exit(1);
' "$checkout_task/artifacts/harness-provenance.json"
checkout_work_before="$(node -p 'require(process.argv[1]).source.workingTreeSha256' "$checkout_task/artifacts/harness-provenance.json")"
checkout_reuse="$(FAKE_HARNESS_LOG="$root/unused.log" PATH="$clean_path" MM_HARNESS_BIN="$checkout/bin/mm-harness" \
  "$resolver" "$checkout_task" 2>&1)"
case "$checkout_reuse" in *'stale or invalid'*) exit 1 ;; esac
# Source-checkout provenance applies the same runner-state boundary as package hashing.
mkdir -p "$checkout/dist/.omc/state" "$checkout/.omx/state"
printf '%s\n' '{"tick":1}' > "$checkout/dist/.omc/state/run.json"
printf '%s\n' '{"tick":2}' > "$checkout/.omx/state/run.json"
FAKE_UPDATE_MODE=offline PATH="$clean_path" "$resolver" "$checkout_task" --verify-only >/dev/null
test "$checkout_work_before" = "$(node -p 'require(process.argv[1]).source.workingTreeSha256' "$checkout_task/artifacts/harness-provenance.json")"
printf '%s\n' 'dirty-checkout' >> "$checkout/library/implementation.js"
checkout_output="$(FAKE_HARNESS_LOG="$root/unused.log" PATH="$clean_path" MM_HARNESS_BIN="$checkout/bin/mm-harness" \
  "$resolver" "$checkout_task" 2>&1)"
grep -q 'existing harness provenance is stale or invalid' <<< "$checkout_output"
node -e 'if(require(process.argv[1]).source.dirty!==true)process.exit(1)' "$checkout_task/artifacts/harness-provenance.json"
checkout_work_after="$(node -p 'require(process.argv[1]).source.workingTreeSha256' "$checkout_task/artifacts/harness-provenance.json")"
test "$checkout_work_before" != "$checkout_work_after"


# PATH harness is accepted and recorded directly, regardless of what update --check
# would return. The update command must never be invoked.
for scenario in stale offline invalid; do
  scenario_task="$root/$scenario-task"
  mkdir -p "$scenario_task"
  scenario_log="$root/$scenario-invoke.log"
  case "$scenario" in
    stale)
      scenario_resolved="$(FAKE_HARNESS_LOG="$scenario_log" FAKE_LATEST_VERSION="$newer_version" \
        PATH="$path_harness/bin:$clean_path" "$resolver" "$scenario_task")"
      ;;
    offline)
      scenario_resolved="$(FAKE_HARNESS_LOG="$scenario_log" FAKE_UPDATE_MODE=offline \
        PATH="$path_harness/bin:$clean_path" "$resolver" "$scenario_task")"
      ;;
    invalid)
      scenario_resolved="$(FAKE_HARNESS_LOG="$scenario_log" FAKE_UPDATE_MODE=invalid \
        PATH="$path_harness/bin:$clean_path" "$resolver" "$scenario_task")"
      ;;
  esac
  test "$scenario_resolved" = "$(cd "$path_harness/bin" && pwd)/mm-harness"
  node -e '
    const j=require(process.argv[1]);
    if (j.source.kind!=="PATH") process.exit(1);
  ' "$scenario_task/artifacts/harness-provenance.json"
  test ! -e "$scenario_task/.mm-harness"
  if [ -f "$scenario_log" ]; then
    grep -q '^update' "$scenario_log" && { echo "resolve-harness: $scenario: update was unexpectedly invoked" >&2; exit 1; } || true
  fi
  # A second run reuses the receipt without calling update.
  second_log="$root/$scenario-second.log"
  FAKE_HARNESS_LOG="$second_log" PATH="$path_harness/bin:$clean_path" \
    "$resolver" "$scenario_task" >/dev/null
  if [ -f "$second_log" ]; then
    grep -q '^update' "$second_log" && { echo "resolve-harness: $scenario second-run: update was unexpectedly invoked" >&2; exit 1; } || true
  fi
  FAKE_HARNESS_LOG="$root/$scenario-verify.log" PATH="$path_harness/bin:$clean_path" \
    "$resolver" "$scenario_task" --verify-only >/dev/null
done

# A genuinely clean PATH never installs silently and accepts one-character input.
missing_task="$root/missing-task"
mkdir -p "$missing_task"
set +e
missing_output="$(PATH="$clean_path" "$resolver" "$missing_task" 2>&1)"
missing_status=$?
set -e
test "$missing_status" -eq 1
grep -Fq "1. Install $HARNESS_PACKAGE_SPEC inside this task only, lock its exact resolution, and continue." <<< "$missing_output"
grep -q '^2\. Stop without installing\.$' <<< "$missing_output"
grep -q '^Reply with 1 or 2\.$' <<< "$missing_output"
test ! -e "$missing_task/artifacts/harness-provenance.json"

missing_init_task="$root/missing-init-task"
set +e
missing_init_output="$(PATH="$clean_path" "$init" --task-kind dev --platform core --slug missing --task-dir "$missing_init_task" --task-text 'Fix the "quoted" $thing; keep it' 2>&1)"
missing_init_status=$?
set -e
test "$missing_init_status" -eq 1
test ! -e "$missing_init_task/CHECKLIST.md"
test ! -e "$missing_init_task/artifacts/harness-provenance.json"
grep -q '^Reply with 1 or 2\.$' <<< "$missing_init_output"
grep -q 'scripts/init-template .*--harness-choice 1$' <<< "$missing_init_output"
# The printed recovery command re-creates the same TASK.md: task text survives with
# its quotes and shell metacharacters escaped.
recovery_cmd="$(grep 'scripts/init-template .*--harness-choice 1$' <<< "$missing_init_output")"
grep -q -- '--task-text' <<< "$recovery_cmd"
eval "recovery_args=(${recovery_cmd#*init-template })"
recovered_text=""
for ((i = 0; i < ${#recovery_args[@]}; i++)); do
  [ "${recovery_args[i]}" = "--task-text" ] && recovered_text="${recovery_args[i+1]}"
done
test "$recovered_text" = 'Fix the "quoted" $thing; keep it'

# Choice 1 requests the pinned package version and records npm's exact dependency
# and lockfile metadata. The receipt remains reusable after registry latest advances.
install_bin="$root/install-bin"
mkdir -p "$install_bin"
ln -s "$real_node" "$install_bin/node"
cat > "$install_bin/npm" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" > "${FAKE_NPM_LOG:?}"
prefix=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --prefix) prefix="$2"; shift 2 ;;
    *) shift ;;
  esac
done
[ -n "$prefix" ]
pkg="$prefix/node_modules/@deeeed/metamask-harness"
validator="$prefix/node_modules/@farmslot/recipe-cli"
mkdir -p "$pkg/bin" "$pkg/dist" "$pkg/adapters" "$pkg/library" "$prefix/node_modules/.bin" "$validator/dist"
node - "$pkg/package.json" "$FAKE_INSTALL_VERSION" <<'NODE'
const fs = require('node:fs');
const [file, version] = process.argv.slice(2);
fs.writeFileSync(file, `${JSON.stringify({name:'@deeeed/metamask-harness', version, repository:'https://github.com/MetaMask/experimental-metamask-harness.git'})}\n`);
NODE
cat > "$pkg/bin/mm-harness" <<'BIN'
#!/usr/bin/env bash
exit 0
BIN
chmod +x "$pkg/bin/mm-harness"
ln -s ../@deeeed/metamask-harness/bin/mm-harness "$prefix/node_modules/.bin/mm-harness"
printf '%s\n' '{"name":"@farmslot/recipe-cli","version":"0.0.0","main":"dist/index.js"}' > "$validator/package.json"
printf '%s\n' 'export {};' > "$validator/dist/index.js"
node - "$prefix/package.json" "$prefix/package-lock.json" "$FAKE_INSTALL_VERSION" <<'NODE'
const fs = require('node:fs');
const [manifest, lockfile, version] = process.argv.slice(2);
fs.writeFileSync(manifest, `${JSON.stringify({private:true, dependencies:{'@deeeed/metamask-harness':version}})}\n`);
const entry = {
  version,
  resolved:`https://registry.npmjs.org/@deeeed/metamask-harness/-/metamask-harness-${version}.tgz`,
  integrity:'sha512-Y29udHJhY3QtaW50ZWdyaXR5',
};
let lock;
switch (process.env.FAKE_LOCK_MODE) {
  case 'v1':
    lock = {lockfileVersion:1, dependencies:{'@deeeed/metamask-harness':entry}};
    break;
  case 'mismatch':
    lock = {lockfileVersion:1, dependencies:{'@deeeed/metamask-harness':{...entry, version:'1.0.0'}}};
    break;
  case 'malformed':
    lock = {lockfileVersion:1, dependencies:{'@deeeed/metamask-harness':{version, resolved:entry.resolved}}};
    break;
  case 'bad-url':
    lock = {lockfileVersion:1, dependencies:{'@deeeed/metamask-harness':{...entry, resolved:'not-a-url'}}};
    break;
  default:
    lock = {packages:{
      '': {dependencies:{'@deeeed/metamask-harness':version}},
      '../../../../private/tmp/task/.mm-harness/node_modules/@deeeed/metamask-harness':entry,
    }};
}
fs.writeFileSync(lockfile, `${JSON.stringify(lock)}\n`);
NODE
SH
chmod +x "$install_bin/npm"

# A PATH candidate is accepted and recorded directly; no npm install is performed.
path_task="$root/path-task"
mkdir -p "$path_task"
path_log="$root/path-invoke.log"
path_resolved="$(FAKE_HARNESS_LOG="$path_log" PATH="$path_harness/bin:$install_bin:$clean_path" \
  "$resolver" "$path_task")"
test "$path_resolved" = "$(cd "$path_harness/bin" && pwd)/mm-harness"
node -e '
  const j=require(process.argv[1]);
  if(j.source.kind!=="PATH" || j.package.version!==process.argv[2])process.exit(1);
' "$path_task/artifacts/harness-provenance.json" "$current_version"
test ! -e "$path_task/.mm-harness"
if [ -f "$path_log" ]; then
  grep -q '^update' "$path_log" && { echo "resolve-harness: path-task: update was unexpectedly invoked" >&2; exit 1; } || true
fi

# An unusable override does not skip a PATH candidate; PATH is recorded directly.
wrong_override="$root/wrong-override"
make_harness "$wrong_override" "$older_version"
node -e 'const fs=require("fs"); const p=require(process.argv[1]); p.name="wrong-package"; fs.writeFileSync(process.argv[1], JSON.stringify(p))' "$wrong_override/package.json"
fallback_task="$root/fallback-task"
mkdir -p "$fallback_task"
PATH="$path_harness/bin:$install_bin:$clean_path" MM_HARNESS_BIN="$wrong_override/bin/mm-harness" \
  "$resolver" "$fallback_task" >/dev/null
node -e 'if(require(process.argv[1]).source.kind!=="PATH")process.exit(1)' \
  "$fallback_task/artifacts/harness-provenance.json"

# A second run reuses the locked receipt; --verify-only passes on the PATH receipt.
path_receipt_before="$(shasum -a 256 "$path_task/artifacts/harness-provenance.json" | awk '{print $1}')"
PATH="$path_harness/bin:$clean_path" "$resolver" "$path_task" >/dev/null
test "$path_receipt_before" = "$(shasum -a 256 "$path_task/artifacts/harness-provenance.json" | awk '{print $1}')"
verified_path="$(PATH="$path_harness/bin:$clean_path" "$resolver" "$path_task" --verify-only)"
test "$verified_path" = "$path_resolved"

# An explicit --choice 1 still pins a task-local install when PATH already has a harness.
pinned_task="$root/pinned-over-path-task"
mkdir -p "$pinned_task"
FAKE_INSTALL_VERSION="$newer_version" FAKE_NPM_LOG="$root/pinned-npm.log" FAKE_HARNESS_LOG="$root/unused.log" \
  PATH="$path_harness/bin:$install_bin:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$resolver" "$pinned_task" --choice 1 > "$root/pinned.path"
case "$(cat "$root/pinned.path")" in "$pinned_task/.mm-harness/"*) ;; *) exit 1 ;; esac
node -e 'if(require(process.argv[1]).source.kind!=="task-local-npm")process.exit(1)' \
  "$pinned_task/artifacts/harness-provenance.json"

install_task="$root/install-task"
mkdir -p "$install_task"
FAKE_INSTALL_VERSION="$newer_version" FAKE_NPM_LOG="$root/npm.log" PATH="$install_bin:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$resolver" "$install_task" --choice 1 > "$root/installed.path"
case "$(cat "$root/installed.path")" in "$install_task/.mm-harness/"*) ;; *) exit 1 ;; esac
grep -Fq -- '--save-exact' "$root/npm.log"
grep -Fq -- '--package-lock=true' "$root/npm.log"
grep -Fq -- "$HARNESS_PACKAGE_SPEC" "$root/npm.log"
node -e '
  const j=require(process.argv[1]);
  if(j.package.version!==process.argv[2] || j.source.kind!=="task-local-npm")process.exit(1);
  if(j.source.requested!==process.argv[3] || j.source.integrity!=="sha512-Y29udHJhY3QtaW50ZWdyaXR5")process.exit(1);
  if(!j.source.registry.endsWith(`metamask-harness-${process.argv[2]}.tgz`))process.exit(1);
' "$install_task/artifacts/harness-provenance.json" "$newer_version" "$HARNESS_PACKAGE_SPEC"
node -e '
  const manifest=require(process.argv[1]); const lock=require(process.argv[2]);
  if(manifest.dependencies[process.argv[3]]!==process.argv[4])process.exit(1);
  const entry=Object.entries(lock.packages).find(([key])=>key.endsWith("node_modules/"+process.argv[3]));
  if(entry?.[1].version!==process.argv[4])process.exit(1);
' "$install_task/.mm-harness/package.json" "$install_task/.mm-harness/package-lock.json" "$HARNESS_PACKAGE_NAME" "$newer_version"
installed_receipt_before="$(shasum -a 256 "$install_task/artifacts/harness-provenance.json" | awk '{print $1}')"
PATH="$clean_path" "$resolver" "$install_task" >/dev/null
installed_receipt_after="$(shasum -a 256 "$install_task/artifacts/harness-provenance.json" | awk '{print $1}')"
test "$installed_receipt_before" = "$installed_receipt_after"

# npm v6 package-lock v1 carries the same exact provenance under dependencies.
v1_task="$root/v1-install-task"
mkdir -p "$v1_task"
FAKE_INSTALL_VERSION="$newer_version" FAKE_LOCK_MODE=v1 FAKE_NPM_LOG="$root/npm-v1.log" PATH="$install_bin:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$resolver" "$v1_task" --choice 1 >/dev/null
node -e '
  const j=require(process.argv[1]);
  if(j.package.version!==process.argv[2] || j.source.kind!=="task-local-npm")process.exit(1);
  if(j.source.integrity!=="sha512-Y29udHJhY3QtaW50ZWdyaXR5" || !j.source.registry.endsWith(`metamask-harness-${process.argv[2]}.tgz`))process.exit(1);
' "$v1_task/artifacts/harness-provenance.json" "$newer_version"

# Legacy metadata never weakens provenance: version mismatch or missing
# integrity fails after install and does not create a receipt.
for lock_mode in mismatch malformed bad-url; do
  rejected_task="$root/$lock_mode-install-task"
  mkdir -p "$rejected_task"
  set +e
  rejected_output="$(FAKE_INSTALL_VERSION="$newer_version" FAKE_LOCK_MODE="$lock_mode" FAKE_NPM_LOG="$root/npm-$lock_mode.log" PATH="$install_bin:/usr/bin:/bin:/usr/sbin:/sbin" \
    "$resolver" "$rejected_task" --choice 1 2>&1)"
  rejected_status=$?
  set -e
  test "$rejected_status" -eq 1
  grep -q 'lacks exact version, resolved URL, or integrity' <<< "$rejected_output"
  test ! -e "$rejected_task/artifacts/harness-provenance.json"
done

# init-template and its marker use the same exact recorded executable after
# PATH/override disappear.
marker_task="$root/marker-task"
FAKE_HARNESS_LOG="$root/marker.log" PATH="$clean_path" MM_HARNESS_BIN="$override/bin/mm-harness" \
  "$init" --task-kind dev --platform core --slug marker --task-dir "$marker_task" >/dev/null
FAKE_HARNESS_LOG="$root/marker.log" PATH="$clean_path" "$marker_task/mark" start
grep -qx "checklist mark $marker_task start" "$root/marker.log"
grep -Fq '"$DIR/mm-harness" checklist mark' "$marker_task/mark"

# The marker routes through the task-local front door, so every mark re-verifies
# the recorded receipt: a tampered harness is refused instead of being run.
printf '%s\n' 'implementation-v3' > "$override/library/implementation.js"
set +e
tampered_mark_output="$(FAKE_HARNESS_LOG="$root/tampered-mark.log" PATH="$clean_path" "$marker_task/mark" 1 2>&1)"
tampered_mark_status=$?
set -e
test "$tampered_mark_status" -ne 0
grep -q 'harness provenance is missing, stale, or invalid' <<< "$tampered_mark_output"
test ! -e "$root/tampered-mark.log"

echo 'resolve-harness: exact receipt reuse, explicit override, PATH recording, and task-local lock passed'
