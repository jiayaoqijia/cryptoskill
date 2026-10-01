---
repo: metamask-mobile
parent: review-pr
---

# MetaMask Mobile review routing

Use this overlay with the shared workflow. Review stays read-only.

## Repository files

Read these files at the frozen head SHA when the diff touches the matching surface:

- `.github/pull-request-template.md` for `pr-guidelines`: **Description**, **Changelog**, **Related issues**, **Manual testing steps**, **Screenshots/Recordings**, **Pre-merge author checklist**, and **Pre-merge reviewer checklist**.
- `.github/guidelines/CODING_GUIDELINES.md` for `coding-guidelines`.
- `docs/testing/component-view-tests.md` when the diff changes a screen or view test. Layer selection still comes from the installed `mobile-testing` skill and its `knowledge/testing-layers.md` policy: component-view, then integration, then unit.

## Commands named by the repository

Treat these command names as evidence labels from check output or the pull request body. Record their result as `unknown` until that evidence supplies a conclusion. Terminal execution remains limited to [references/operations.md](references/operations.md).

- `yarn lint`
- `yarn lint:tsc`
- `yarn jest <test-file>`

## Module routing

| Changed files | Class | Module | Semantic signal |
| --- | --- | --- | --- |
| Application `*.test.ts`, `*.test.tsx`, `*.view.test.tsx`, `*.integration.test.ts`, `tests/smoke-appium/` | preference | `mobile-testing` | Application behavior or test-layer coverage changed |
| React Native components and screens | capability | `performance` when installed | Rendering, effects, data flow, lists, interaction cost, startup, memory, or responsiveness changed |
| React Native component JSX | capability | `check-nesting` when installed | Component nesting changed |
| User-facing copy | preference | `content-guidelines` when installed | Visible strings changed |
| Analytics, feature flags, or navigation | capability | The installed `analytics`, `feature-flags`, or `navigation` skill | Matching domain behavior changed |
| Flaky-test detector scripts and workflows | capability | `flaky-test-detection` when installed | Flaky-test detection, history, analysis, or sticky-comment behavior changed |

`pr-readiness-check` is a preference skill with a Mobile overlay. Invoke it when installed, the frozen diff is available, and application code changed. Put its result under **Author evidence**.

When the diff changes `.github/`, `scripts/`, build tooling, or documentation and does not change application code, apply matching repository preferences and script-domain capabilities. Review the `*.test.ts` files next to those scripts. Record `yarn jest <script-test-file>` as unknown unless check output shows that file.

## Author evidence

Compare the available pull request body and checks with:

- the named sections in `.github/pull-request-template.md`;
- manual testing evidence;
- screenshots or recordings;
- changelog evidence;
- linked issue context;
- check rollup;
- `pr-readiness-check` output when selected.

Use `provided`, `needs author evidence`, or `unread`. Keep these statuses outside guided claim findings and severity.

## Require

- Compare the pull request body with the sections in `.github/pull-request-template.md` when that body is `available`.
- Put template, manual testing, screenshots, changelog, linked issue, checks, and `pr-readiness-check` results under **Author evidence**.
- Route application test changes to `mobile-testing` and cite `docs/testing/component-view-tests.md` only for a screen or view test in the diff.
- Route a capability only when both the changed surface and semantic signal match.
- Route flaky-test detector scripts and workflows to `flaky-test-detection` when that installed skill is readable.
- For a tooling-only diff, review the tooling's own tests and matching domain skills.

## Reject

- Treating `yarn lint`, `yarn lint:tsc`, or `yarn jest` as passed without command or check output.
- Choosing Appium while the installed `mobile-testing` layer policy still accepts component-view or integration.
- Applying application-specific skills to a tooling, CI, build, or documentation diff that does not change application code.
- Giving author-evidence gaps finding severity.
- Selecting `performance` from a component path without a performance semantic signal.
