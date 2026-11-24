# Eligibility

A finding is eligible only if its "Done when" can be written entirely as commands that pass in a headless checkout: unit tests, type-check, lint, a scanner. If a reviewer would need to open the app to trust the change, it is not eligible.

## Allowed

- Test-quality refactors: wait hacks, manual teardown, hand-built mocks, type casts in tests, weak assertions, test titles.
- Lint, type-cast and suppression burn-down, where the suppression count proves progress.
- Dead-code removal, only when a tool or a repo-wide search proves it is unused.
- Behaviour-preserving migrations with a checker: React Compiler bail-outs (react-compiler-marker), codemods, deprecated API swaps.
- Renames and in-code docs that change no behaviour.
- Dependency hygiene that needs no runtime check (unused deps, duplicate pins).

## Rejected

- Features, UX, copy, analytics events, anything a user would notice.
- Anything verified only by a device, simulator, E2E, visual diff or manual QA.
- Native code and iOS or Android build config.
- Persisted state shape, storage, migrations.
- Security-sensitive code: keyring, signing, permissions, RPC request validation, secrets.
- Paths the team does not own in CODEOWNERS.
- Work that needs a design decision nobody has made. Decide it in phase 2 or drop it.

## Borderline

- **Source change with a unit test that proves behaviour is unchanged.** Allowed when the test runs headlessly and fails if the behaviour breaks. Say which test in "Done when".
- **Mobile component refactors.** Allowed only with component-view or unit tests that cover the change. If the only proof is how the screen looks, reject.
- **A smell that is also a real bug.** Not cleanup. File a normal bug ticket outside this epic.

Rejected findings go into `plan.md` under "Dropped", one line each with the reason. Findings that are worth doing but fail the headless test are filed with the `human-only` label, never in an agent wave.
