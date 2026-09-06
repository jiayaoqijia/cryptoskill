# Unit ↔ CV overlap sub-pass (Approach A)

Reuse when shallow `ComponentName.test.tsx` and/or `ComponentName.view.test.tsx` exist for screen UI. Prefer loading personal Cursor skill `test-layer-overlap-audit` if present; otherwise follow this condensed Approach A.

**Goal:** Prefer **CV** for screen UI driven by Redux; keep **unit** for pure functions, selectors, utils, toast *copy builders*. Remove shallow screen units that only re-assert what CV covers.

## Reason → best layer

| If the test’s reason is… | Best layer | Action when wrong file |
| --- | --- | --- |
| Screen UI, button visibility, press → destination, disabled/empty/loading from Redux/streams | **CV** (`*.view.test.tsx`) | **MIGRATE** then delete unit `it` |
| Pure function / resolver / util / reducer / selector math | **Unit** | **KEEP** |
| Toast *copy/options* builders | **Unit** | **KEEP** |
| Same journey already asserted in CV | — | **DELETE** shallow unit |

**Hard rule:** UI / screen-behavior tests in unit files with mocked hooks/selectors/navigation are in the **wrong layer** — migrate to CV; do not improve mocks in place.

## Steps

1. Inventory siblings (see `inventory.md`).
2. Optional coverage snapshot (diagnostic only):

```bash
yarn jest ./path/Component.test.tsx -c jest.config.js \
  --coverage --coverageDirectory=test-reports/<ticket>/before/unit \
  --collectCoverageFrom='path/Component.{ts,tsx}' \
  --coverageReporters=json-summary --coverageReporters=text-summary --runInBand --silent

yarn jest -c jest.config.view.js ./path/Component.view.test.tsx \
  --coverage --coverageDirectory=test-reports/<ticket>/before/cv \
  --collectCoverageFrom='path/Component.{ts,tsx}' \
  --coverageReporters=json-summary --coverageReporters=text-summary --runInBand --silent
```

3. Classify each unit `it(...)`: reason → best layer → DELETE | MIGRATE | KEEP.
4. **Mandatory assert-parity gap check before DELETE** — Diff the deleted unit’s `expect` payloads against the CV replacement field-by-field (`tabId`, `filterId`, formatted dates, image URI, list membership, full analytics objects). If any field was dropped, restore it in CV **or** KEEP a focused unit with a reason — do **not** delete a specific assert and replace it with a weaker `objectContaining({ feedId })`. Partial parity is a regression.
5. Apply (IMPLEMENT mode only): add CV for MIGRATE → delete DELETE/migrated unit its → residual toast matrices via pure helper + unit (**EXTRACT+UNIT**) when user accepts → re-run unit + CV.
6. Record metrics: unit its removed, CV its added, ratio, app LOC + why, residual gaps.

## In-repo docs (keep minimal)

PR / main should only carry short guards in:

- `docs/testing/unit-testing.md`
- `docs/testing/component-view-tests.md`
- `tests/component-view/AGENTS.md`
- Optional playbook: `docs/testing/unit-vs-component-view-overlap.md`

Do **not** commit spike-only classification dumps into the mobile repo.
