# Routing

Select a module only when its skill is installed and every required input was classified `available`. Record each routing decision:

```text
skill: <name>
class: preference | capability
paths: <matching changed paths>
signal: <behavior or rule that selected it>
inputs: <available inputs>
result: applied | skipped — <reason>
```

## Repository preferences

Preference skills encode repository norms, conventions, and rules.

| Module | Select when | Required input | Report destination |
| --- | --- | --- | --- |
| `pr-guidelines` | Every peer pull request | Frozen diff and repository pull request template | Author evidence for template coverage; finding only for a code or process defect demonstrated by the diff |
| `pr-readiness-check` | The repository overlay supports it and application code changed | Frozen diff and installed repository overlay | Author evidence |
| `coding-guidelines` | Changed source or test files | Frozen diff and repository coding guidelines | Guided claim checks |
| Repository testing skill | Application tests changed | Frozen test diff and the testing references selected by the overlay | Guided claim checks |
| `controller-guidelines` | Controller implementation changed and the overlay selects it | Frozen controller diff | Guided claim checks |
| `content-guidelines` | User-facing copy changed and the skill is installed | Frozen copy diff | Guided claim checks |

Template sections, screenshots, manual testing, linked issues, changelog, and check conclusions are author evidence. Report their status without finding severity.

## Domain capabilities

Capability skills provide specialized review knowledge. Select one only when both its changed surface and semantic signal match.

| Capability | Changed surface | Semantic signal | Required input |
| --- | --- | --- | --- |
| Mobile `performance` | React Native components or screens | Rendering, effects, data flow, lists, interaction cost, startup, memory, or responsiveness | Frozen matching files and skill-required references |
| Extension performance skills | UI, hooks, or Redux | Rendering, effect lifecycle, compiler behavior, state identity, list or interaction cost | Frozen matching files and skill-required references |
| `analytics` | Event calls, schemas, properties, or tracking tests | Product measurement behavior changed | Frozen matching files and analytics references |
| `feature-flags` | Flag selectors, schemas, gates, or rollout code | Flag behavior or version gating changed | Frozen matching files and flag references |
| `navigation` | Routes, navigators, resets, or navigation callers | Navigation behavior changed | Frozen matching files and navigation references |
| Installed domain skill | Paths owned by that domain | Domain behavior described by the skill changed | Frozen matching files and every file the skill requires |
| `check-nesting` | React Native component | JSX nesting changed | Frozen component diff |
| `audit-observability` | Metrics, traces, or logs | Observability behavior changed | Frozen matching files |
| `check-high-cardinality` | Metric labels | Label values or dimensions changed | Frozen matching files |

A path match alone is insufficient for a capability. For example, copy-only changes in a React component select content guidance while rendering logic selects performance.

## Tooling, CI, and documentation

Treat `.github/`, `scripts/`, `development/`, build tooling, and documentation as non-application surfaces when the diff does not also change application code.

Apply repository preferences that match those files and any domain capability whose declared paths and semantics match. Review tests next to the changed tooling. Keep application performance, navigation, analytics, feature flags, controller, component-view, integration, Appium, and application end-to-end guidance outside this route.

## Skip reasons

Use one reason:

- skill not installed;
- required input `unavailable` or `failed`;
- changed paths do not match;
- semantic signal does not match;
- repository overlay routes the surface elsewhere.

The report preserves the skip reason. Specialist rules come from the installed skill.
