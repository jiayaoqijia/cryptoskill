---
repo: va-mmcx-terminal
parent: review-pr
---

# MetaMask Terminal review routing

Use this overlay with the shared workflow. Review stays read-only.

## Repository files

Read these files at the frozen head SHA when the diff touches the matching surface:

- `.github/pull_request_template.md` for `pr-guidelines`: **Description**, **Type of change**, **Tracking**, **Test plan**, **Secret key management (if applicable)**, and **Additional checks**. The filename uses underscores here, unlike Mobile and Extension.
- `docs/testing-guide.md` when the diff changes a test. It applies MetaMask's `mobile-testing` layer policy to this web repo and names the cheapest deterministic layer that exercises the responsible boundary; `*.view.test.tsx` is the component-view layer.
- `docs/e2e-testing.md` when the diff changes an E2E spec. An E2E spec needs a written reason why component view and unit cannot cover the behavior.
- `AGENTS.md`, which the PR template's **Additional checks** names: the author states deviations in the pull request body.

This repository has no `.github/guidelines/CODING_GUIDELINES.md`. Do not cite one.

## Commands named by the repository

Treat these command names as evidence labels from check output or the pull request body. Record their result as `unknown` until that evidence supplies a conclusion. Terminal execution remains limited to [references/operations.md](references/operations.md).

- `npm run lint` — Biome, the i18n string check and `typecheck` in one command, so a lint claim covers all three
- `npm run typecheck`
- `npm run test:unit`, or `vitest run <test-file>` for a single file
- `npm run test:view` for the component-view layer

## Module routing

| Changed files | Class | Module | Semantic signal |
| --- | --- | --- | --- |
| Perps feature code (`src/features/perpetuals/`) | preference | `perps-review-pr` | Perps behavior, provider use, formatting or network selection changed |
| Terminal product surfaces and conventions | preference | `metamask-terminal` when installed | Terminal-specific structure, routing or conventions changed |
| React components and routes | capability | `recipe-performance` when installed | Rendering, effects, data flow, lists, interaction cost or responsiveness changed |
| User-facing copy | preference | `content-guidelines` when installed | Visible strings changed |

Skip `pr-readiness-check` on Terminal. That skill has a Mobile overlay and no Terminal overlay.

When the diff changes `.github/`, `scripts/`, build tooling, or documentation and does not change application code, apply matching repository preferences and script-domain capabilities. Review the test files next to those scripts. Record `vitest run <script-test-file>` as unknown unless check output shows that file.

## Author evidence

Compare the available pull request body and checks with:

- the named sections in `.github/pull_request_template.md`;
- the **Test plan** section;
- linked tracking context;
- check rollup;
- the **Additional checks** boxes, including the AGENTS.md deviations line.

Use `provided`, `needs author evidence`, or `unread`. Keep these statuses outside guided claim findings and severity.

## Require

- Compare the pull request body with the sections in `.github/pull_request_template.md` when that body is `available`.
- Put template, test plan, tracking, checks and AGENTS.md deviation statements under **Author evidence**.
- Route Perps feature changes to `perps-review-pr` and cite `docs/testing-guide.md` only for a test in the diff.
- Route a capability only when both the changed surface and semantic signal match.
- For a tooling-only diff, review the tooling's own tests and matching domain skills.

## Reject

- Treating `npm run lint`, `npm run typecheck`, `npm run test:unit` or `npm run test:view` as passed without command or check output.
- Reading a passing `npm run lint` as covering only Biome: it also runs the i18n check and `typecheck`, so a failure in either is a lint failure.
- Choosing E2E while the layer policy in `docs/testing-guide.md` still accepts component-view or unit.
- Citing a coding-guidelines file this repository does not have.
- Applying application-specific skills to a tooling, CI, build, or documentation diff that does not change application code.
- Giving author-evidence gaps finding severity.
