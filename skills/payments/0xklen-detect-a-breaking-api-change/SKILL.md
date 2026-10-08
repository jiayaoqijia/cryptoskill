---
name: detect-a-breaking-api-change
description: Use when an API spec or protobuf may change between releases — diff the previous published contract against the new one in CI and fail on any change a deployed client could observe.
---

# Detect a breaking API change

Backward compatibility is enforced by tooling, not by reviewers noticing. Diff the last published contract against the new one and fail the build on the exact rules that break clients.

## Procedure

1. Pin the previous contract — the last released OpenAPI/proto/GraphQL schema — from the last git tag, not the working tree:
```
git show v1.4.0:api/openapi.yaml > /tmp/openapi.old.yaml
```
2. Diff OpenAPI with `oasdiff`:
```
oasdiff breaking /tmp/openapi.old.yaml api/openapi.yaml --fail-on ERR
```
It lists each break: removed path, removed response field, new required request field, type change, tightened enum.
3. Diff protobuf with `buf`:
```
buf breaking --against '.git#branch=main'
```
The breaking set includes field renumbering, type change, and reserved-tag reuse.
4. Diff GraphQL with `graphql-inspector diff old.graphql new.graphql --rule breaking`.
5. Treat these as non-negotiable regardless of tool: removing an endpoint or field, adding a required request field, narrowing an enum, changing a type, renaming anything in the wire contract.
6. Prove the gate catches a break: delete one required field and confirm exit 1. An allow-listed gate that never fails is decoration.
7. Wire the check into CI ahead of build/publish so it blocks, and keep an explicit, reviewed, dated allow-list file for the rare intentional break.

## Pitfalls

- Running the diff against the working tree instead of the released tag hides uncommitted spec edits.
- `--fail-on WARN` over-fails on doc-only changes and gets disabled; keep WARN informational and ERR as the gate.
- A deprecation notice is not a break yet — deprecate, ship, wait a release, then remove, so the diff passes at each step.
- GraphQL `@deprecated` fields still count as present; their later removal is the break to gate.

## Verification

```
oasdiff breaking /tmp/openapi.old.yaml api/openapi.yaml --fail-on ERR; echo "exit=$?"
```
Passes = `exit=0` on a compatible change and `exit=1` after planting a removed endpoint. Report: "oasdiff gate green on PR; planted a removed field, got exit 1 naming the field."
