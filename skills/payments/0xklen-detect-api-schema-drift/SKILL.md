---
name: detect-api-schema-drift
description: Use when you depend on a third-party API's shape over time. Snapshot the schema, diff it on a schedule, and alert on removed or retyped fields before they break parsing.
---

# Detect API schema drift

A provider can remove or retype a field in a patch release. Without a snapshot to diff against,
your parser discovers it in production at the worst moment.

## Procedure

1. Snapshot the contract daily and keep it in version control:
   ```bash
   curl -s "$BASE/openapi.json" > "schemas/openapi.$(date -u +%F).json"
   ```
2. Diff the schema objects between yesterday and today:
   ```bash
   jq -S '.components.schemas' "schemas/openapi.$(date -u +%F).json" > /tmp/new
   jq -S '.components.schemas' "schemas/openapi.$(date -u -v-1d +%F).json" > /tmp/old
   diff /tmp/old /tmp/new
   ```
3. Classify the diff: additive (new optional field) is safe; removal, type change, or new required field is breaking.
4. Also diff a live sample, since specs lag reality:
   ```bash
   curl -s "$API/v1/item/1" | jq -S . > "schemas/sample.$(date -u +%F).json"
   ```
5. Alert on breaking diffs to the owning channel and pin the parser to the last-known-good shape until fixed.
6. Run the check in CI weekly so drift is caught off the critical path.
7. Keep snapshots so you can bisect when a field actually disappeared.

## Pitfalls

- Specs lie: fields exist live but undocumented, and documented fields are absent for some accounts.
- Cursor/request-id fields are random and always differ; exclude volatile keys before comparing.
- Key-ordering noise creates false diffs; always `jq -S` (sorted) before diffing.
- A provider swapping `/v1` to `/v2` in place is a schema change even if the spec URL is unchanged.
- Paging on every additive field trains people to ignore the alert; only breakings should page.

## Verification

    bash tools/schema-drift.sh; echo "exit=$?"    # 0 = no breaking change

Report the removed or retyped fields, or "no breaking drift since <date>". Name the field and the date it changed, never "the API changed".
