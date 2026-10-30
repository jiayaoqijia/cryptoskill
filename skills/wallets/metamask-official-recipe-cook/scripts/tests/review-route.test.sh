#!/usr/bin/env bash
set -euo pipefail
skill_dir="$(cd "$(dirname "$0")/../.." && pwd)"
runner="$skill_dir/scripts/create-harness-runner"
policy="$skill_dir/scripts/harness-package-policy"
init="$skill_dir/scripts/init-template"
# Removed runtime-review IDs cannot silently start a static review or launch an app.
for platform in mobile extension; do
  test -f "$skill_dir/references/templates/qa/pr.$platform.md"
  test ! -e "$skill_dir/references/templates/review-pr/autonomous.$platform.md"
done
if "$init" --platform mobile --task-kind review-pr --template review-pr/static-perps.mobile --prepare >/dev/null 2>&1; then
  echo 'static review accepted runtime preparation' >&2; exit 1
fi

# create-harness-runner must produce a runner that actually resolves and execs a
# harness, not merely contain the right text.
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

produced="$("$runner" "$work/task")"
[ "$produced" = "$work/task/mm-harness" ] || { echo "create-harness-runner returned an unexpected path: $produced" >&2; exit 1; }
test -x "$produced"

channel="$(sed -n 's/^HARNESS_PACKAGE_CHANNEL="\(.*\)"$/\1/p' "$policy")"
[ -n "$channel" ] || { echo "harness-package-policy has no resolvable channel" >&2; exit 1; }
# shellcheck source=../scripts/harness-package-policy
source "$policy"
setup_spec="$(sed -n 's/.*npm i -g \(@deeeed\/metamask-harness@[^`]*\)`.*/\1/p' "$skill_dir/../recipe-setup/skill.md")"
[ "$setup_spec" = "$HARNESS_PACKAGE_SPEC" ] || { echo 'Setup and Cook harness recommendations differ' >&2; exit 1; }

# Execution requires an existing receipt and cannot resolve a new PATH binary.
set +e
runner_output="$(env PATH="/usr/bin:/bin" MM_HARNESS_BIN="$work/absent-harness" "$produced" actions --json 2>&1)"
runner_status=$?
set -e
[ "$runner_status" -ne 0 ] || { echo "task-local runner succeeded without a resolvable harness" >&2; exit 1; }
grep -Fq 'harness provenance is missing, stale, or invalid' <<<"$runner_output"

echo "recipe-cook review route: PASS"
