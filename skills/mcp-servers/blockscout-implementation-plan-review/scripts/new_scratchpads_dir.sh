#!/usr/bin/env bash
# SPDX-License-Identifier: LicenseRef-Blockscout
#
# Create a fresh timestamped scratchpad directory for implementation-plan-review.
#
# For a plan file at <dir>/<stem>.<ext>, creates and prints:
#   <dir>/<stem>/scratchpads/<timestamp>/   (timestamp = `date +%y%m%d-%H%M`)
# e.g. for .ai/impl_plans/issue-428.md this is
#   .ai/impl_plans/issue-428/scratchpads/260714-1022/
#
# Nothing is ever deleted: every run gets its own new timestamped directory.
# The plan file does NOT need to live under .ai/impl_plans -- any local path
# works, since the target is derived from the plan file's own location and
# basename. This script does not require a git repository.
#
# Usage: new_scratchpads_dir.sh <plan-file>
# Output on success: absolute path of the new directory on stdout, nothing else.
# Output on failure: "error: <message>" on stderr.
# Exit codes: 2 = bad usage / unsafe or empty plan-file basename or stem
#             3 = plan file (or its parent directory) does not exist
#             4 = target directory path exists but is not a directory, or
#                 could not be created
#             (5 is reserved for the git-anchored sibling scripts; unused here)

set -euo pipefail

lib_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../_lib" && pwd)"
source "$lib_dir/report_dir.sh"

if [[ $# -ne 1 || -z "${1:-}" ]]; then
  report_dir::die 2 "usage: $(basename "$0") <plan-file>"
fi

plan_file="$1"
plan_dir="$(dirname -- "$plan_file")"
plan_base="$(basename -- "$plan_file")"

if [[ "$plan_base" == "" || "$plan_base" == "." || "$plan_base" == ".." ]]; then
  report_dir::die 2 "unsafe plan filename: $plan_file"
fi

if [[ ! -d "$plan_dir" ]]; then
  report_dir::die 3 "plan parent directory does not exist or is not a directory: $plan_dir"
fi

if [[ ! -f "$plan_file" ]]; then
  report_dir::die 3 "plan file does not exist or is not a file: $plan_file"
fi

plan_stem="$plan_base"
if [[ "$plan_stem" == *.* && "$plan_stem" != .* ]]; then
  plan_stem="${plan_stem%.*}"
fi

if [[ -z "$plan_stem" || "$plan_stem" == "." || "$plan_stem" == ".." ]]; then
  report_dir::die 2 "unsafe scratchpad base name derived from: $plan_base"
fi

report_dir::new "$plan_dir/$plan_stem" "scratchpads"
