#!/usr/bin/env bash
# SPDX-License-Identifier: LicenseRef-Blockscout
#
# Create a fresh timestamped new-findings directory for an implementation-plan
# feedback review: <repo>/.ai/impl_plans/<plan-id>/findings/<timestamp>/.
# Every run gets its own timestamped subdirectory; nothing from a previous
# run is deleted or touched.
#
# Directory-agnostic: resolves the project root via `git rev-parse
# --show-toplevel`, so it behaves the same in the principal checkout and in
# a linked git worktree.
#
# Usage: new_findings_dir.sh <plan-id> [impl-plans-dir]
# Output on success: absolute path of the new directory on stdout, nothing else.
# Output on failure: "error: <message>" on stderr.
# Exit codes: 2 = missing/invalid plan-id
#             3 = plan file <impl-plans-dir>/<plan-id>.md not found
#             4 = target directory path exists but is not a directory, or
#                 could not be created
#             5 = not inside a git repository

set -euo pipefail

lib_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../_lib" && pwd)"
source "$lib_dir/report_dir.sh"

plan_id="${1:-}"

if [[ -z "$plan_id" ]]; then
  report_dir::die 2 "usage: $(basename "$0") <plan-id> [impl-plans-dir]"
fi

if [[ ! "$plan_id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]; then
  report_dir::die 2 "invalid plan id '$plan_id' (expected a single segment like 'issue-418')"
fi

if ! repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  report_dir::die 5 "not inside a git repository (run within the project checkout or a git worktree)"
fi

impl_plans_dir="${2:-$repo_root/.ai/impl_plans}"

plan_file="$impl_plans_dir/$plan_id.md"
if [[ ! -f "$plan_file" ]]; then
  report_dir::die 3 "plan file $plan_file not found -- is the plan id '$plan_id' correct?"
fi

report_dir::new "$impl_plans_dir/$plan_id" "findings"
