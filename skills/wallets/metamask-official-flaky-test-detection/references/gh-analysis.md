# Flaky Test Audit — GitHub Actions

## Prerequisites

```bash
gh auth status
git remote get-url origin  # must contain MetaMask/metamask-mobile
```

## Step 1 — Find the exact unit-test workflow name

```bash
# List recent runs across all workflows — note the name column
gh run list --repo MetaMask/metamask-mobile --limit 50

# Confirm the correct name by filtering (adjust if different from "Unit Tests")
gh run list --repo MetaMask/metamask-mobile --workflow "Unit Tests" --limit 5
```

Use the **exact** workflow name returned by `gh run list` (e.g. `"Unit Tests"`, `"Jest"`, `"CI"`). Substitute it in every `--workflow` flag in the steps below. If the filter returns 0 results, the name is wrong — re-check Step 1.

## Step 2 — Collect IDs of failed runs

Replace `"Unit Tests"` with the name found in Step 1.

```bash
FAILED_RUN_IDS=$(gh run list \
  --repo MetaMask/metamask-mobile \
  --workflow "Unit Tests" \
  --limit 200 \
  --json databaseId,conclusion \
  --jq '.[] | select(.conclusion == "failure") | .databaseId')
```

## Step 3 — Extract failing test file names

```bash
gh run view <run-id> --repo MetaMask/metamask-mobile --log-failed \
  | grep -oE 'FAIL .+\.test\.(ts|tsx|js|jsx)' \
  | sed 's/^FAIL //'
```

## Step 4 — Compute per-file failure count and rate

`TOTAL_RUNS` is all runs in the sampled window (not just failures) — the denominator for rate calculation. It is fetched separately at the end of the script.

> Requires Bash 4+ (for `declare -A`). macOS ships Bash 3.2 by default — run this with `brew install bash` or via `gh`'s bundled environment, or invoke as `bash script.sh` with a Bash 4+ binary on `PATH`.

```bash
declare -A fail_count

for run_id in $FAILED_RUN_IDS; do
  files=$(gh run view "$run_id" --repo MetaMask/metamask-mobile --log-failed 2>/dev/null \
    | grep -oE 'FAIL .+\.test\.(ts|tsx|js|jsx)' \
    | sed 's/^FAIL //')
  for f in $files; do
    fail_count[$f]=$(( ${fail_count[$f]:-0} + 1 ))
  done
done

# Count total runs sampled (all runs in the window, not just failures)
TOTAL_RUNS=$(gh run list \
  --repo MetaMask/metamask-mobile \
  --workflow "Unit Tests" \
  --limit 200 \
  --json databaseId \
  --jq 'length')

# Print: failures total rate% file
for f in "${!fail_count[@]}"; do
  count=${fail_count[$f]}
  rate=$(echo "scale=2; $count * 100 / $TOTAL_RUNS" | bc)
  echo "$count $TOTAL_RUNS ${rate}% $f"
done | sort -rn
```

> Rate limit: ~5,000 gh API requests/hour. Add `sleep 1` between loop iterations for large histories (>100 runs).

## Step 5 — Ranked output format

Columns: rank, test file path, failure count, total runs sampled, failure rate, pattern category (from symptom mapping below).

```
Rank | Test file                                             | Failures | Runs | Rate  | Category
-----|-------------------------------------------------------|---------:|-----:|------:|---------
  1  | app/components/Views/BankDetails/BankDetails.test.tsx |      12  |  50  | 24 %  | J1
  2  | app/util/transactions/transactions.test.ts            |       9  |  50  | 18 %  | J3
```

Assign the category by matching the failure log symptoms in the table below, then open the pattern section in the skill for the fix.

## Symptom → category mapping

| Symptom in failed log | Category |
|---|---|
| `TypeError: terminated` / `SocketError: other side closed` | J1 |
| Timer / timeout mismatch | J2 |
| `toHaveBeenCalledTimes` wrong count | J3 |
| `waitFor` never resolved | J4 or J8 |
| `Cannot read property of undefined` from store selector | J5 |
| Test timed out (5 s default) | J6 |
| Assertion on `Date` or random value fails | J7 |
| Test hangs indefinitely under fake timers | J8 |
| Test passes in isolation but fails in suite | J9 |
| Unexpected function called / wrong return value | J10 |

## Thresholds

| Rate | Action |
|------|--------|
| ≥ 10 % | Actively flaky — fix before merging new tests in that file |
| 5–10 % | At-risk — review for patterns in its category |
| < 5 % | Monitor |
