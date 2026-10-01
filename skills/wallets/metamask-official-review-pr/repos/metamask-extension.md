---
repo: metamask-extension
parent: review-pr
---

# MetaMask Extension review routing

Use this overlay with the shared workflow. Review stays read-only.

## Repository files

Read these files at the frozen head SHA when the diff touches the matching surface:

- `.github/pull-request-template.md` for `pr-guidelines`: **Description**, **Changelog**, **Related issues**, **Manual testing steps**, **Screenshots/Recordings**, **Pre-merge author checklist**, and **Pre-merge reviewer checklist**.
- `.github/guidelines/CODING_GUIDELINES.md` for `coding-guidelines`.
- `docs/testing.md` when the diff changes unit tests. It says to favor Jest. Layer selection for a broader test change comes from the installed `extension-testing` skill.

## Commands named by the repository

Treat these command names as evidence labels from check output or the pull request body. Record their result as `unknown` until that evidence supplies a conclusion. Terminal execution remains limited to [references/operations.md](references/operations.md).

- `yarn lint:changed`
- `yarn test:unit <test-file>`

## Module routing

| Changed files | Class | Module | Semantic signal |
| --- | --- | --- | --- |
| Application `*.test.ts`, `*.test.tsx`, `test/e2e/`, `test/integration/` | preference | `extension-testing` | Application behavior or test coverage changed |
| UI rendering | capability | `perf-rendering` when installed | Render frequency, lists, loading cost, or interaction cost changed |
| Hooks and effects | capability | `perf-hooks-effects` when installed | Effect lifecycle, dependencies, cancellation, or cascading updates changed |
| React compiler-sensitive code | capability | `perf-react-compiler` when installed | Compiler compatibility or memoization behavior changed |
| Redux state or selectors | capability | `perf-state-management` when installed | State identity, reducer behavior, selector output, or batching changed |
| Controller files | preference | `controller-guidelines` when installed | Controller implementation or state contract changed |
| User-facing copy | preference | `content-guidelines` when installed | Visible strings changed |

Skip `pr-readiness-check` on Extension. That skill has a Mobile overlay and no Extension overlay.

When the diff changes `.github/`, `scripts/`, `development/`, build tooling, or documentation and does not change application code, apply matching repository preferences and tooling-domain capabilities. Review the `*.test.ts` files next to that tooling. `docs/testing.md` still applies to those unit tests: favor Jest. Record `yarn test:unit <script-test-file>` as unknown unless check output shows that file.

## Author evidence

Compare the available pull request body and checks with:

- the named sections in `.github/pull-request-template.md`;
- manual testing evidence;
- screenshots or recordings;
- changelog evidence;
- linked issue context;
- check rollup.

Use `provided`, `needs author evidence`, or `unread`. Keep these statuses outside guided claim findings and severity.

## Require

- Compare the pull request body with the sections in `.github/pull-request-template.md` when that body is `available`.
- Put template, manual testing, screenshots, changelog, linked issue, and checks under **Author evidence**.
- Route application unit-test changes through `extension-testing` and cite the Jest guidance in `docs/testing.md`.
- Route a capability only when both the changed surface and semantic signal match.
- For a tooling-only diff, review the tooling's own tests and matching domain skills.

## Reject

- Treating `yarn lint:changed` or `yarn test:unit` as passed without command or check output.
- Applying the Mobile `pr-readiness-check` overlay to an Extension diff.
- Applying application-specific skills to a tooling, CI, build, or documentation diff that does not change application code.
- Giving author-evidence gaps finding severity.
- Selecting a performance capability from a UI path without its semantic signal.
