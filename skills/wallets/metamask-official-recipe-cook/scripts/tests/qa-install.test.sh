#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "$0")/../.." && pwd)"
repo_root="$(cd "$skill_dir/../../../.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

for product in mobile extension core; do
  repo="metamask-$product"
  [ "$product" != core ] || repo=core
  target="$work/$product"
  mkdir -p "$target"
  bash "$repo_root/tools/install" --source "$repo_root" --repo "$repo" --target "$target" \
    --domain perps --include recipe-cook,recipe-qa > "$work/$product.log"
  installed="$target/.agents/skills/mms-recipe-cook/references/templates"
  cmp "$skill_dir/references/dev-fix-bug.md" "$target/.agents/skills/mms-recipe-cook/references/dev-fix-bug.md"
  cmp "$skill_dir/references/templates/qa/default.md" "$installed/qa/default.md"
  cmp "$skill_dir/references/templates/fix-bug/$product.md" "$installed/fix-bug/$product.md"
  test -f "$target/.agents/skills/mms-recipe-qa/scripts/resolve-scope.mjs"
  cmp "$repo_root/domains/perps/skills/recipe-qa/references/report-example.md" \
    "$target/.agents/skills/mms-recipe-qa/references/report-example.md"
  test ! -e "$installed/qa/release.md"
  for other in mobile extension core; do
    cmp "$skill_dir/references/templates/fix-bug/$other.md" "$installed/fix-bug/$other.md"
    cmp "$skill_dir/references/templates/dev/$other.md" "$installed/dev/$other.md"
  done
  # Installation keeps the bundle intact; template discovery owns compatibility.
  bash "$target/.agents/skills/mms-recipe-cook/scripts/list-templates" \
    --platform "$product" --json > "$work/$product-templates.json"
  node - "$work/$product-templates.json" "$product" <<'NODE'
const assert = require('node:assert/strict');
const fs = require('node:fs');
const [file, platform] = process.argv.slice(2);
const { templates } = JSON.parse(fs.readFileSync(file, 'utf8'));
for (const id of ['qa/default', `dev/${platform}`, `fix-bug/${platform}`]) {
  assert(templates.some(t => t.id === id), `missing compatible template ${id}`);
}
for (const t of templates) {
  assert(t.platforms.includes(platform) || t.platforms.includes('*'), `incompatible template ${t.id}`);
}
NODE
done

echo 'Shared QA template installation: PASS'
