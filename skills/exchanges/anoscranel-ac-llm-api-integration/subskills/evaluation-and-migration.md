---
name: evaluation-and-migration
domain: software-engineering/llm-api-integration
trigger: "Running integration regression test suites, pinning model versions, tracking deprecations, and migrating between models"
anti_trigger: "Designing prompt test datasets or writing prompt evaluation criteria (prompt design craft); configuring basic request shapes (subskills/request-shape.md)"
scope: "Regression test execution, model version pinning versus floating aliases, deprecation lifecycle tracking, and migration safety"
status: "seedling"
---

# Evaluation and Migration

## Standard

- **Anthropic Model Versioning and Deprecation Policy**: tracking version identifiers, deprecation lifecycles, and upgrade pathways. <https://docs.anthropic.com/en/docs/about-claude/models#model-versioning>
- **OpenAI Model Lifecycle Guide**: managing floating aliases versus pinned date-stamped model identifiers in production applications. <https://platform.openai.com/docs/models>

## Decision rules

- Pin production applications to explicit date-stamped model identifiers (such as versioned snapshots) to prevent breaking changes caused by automatic updates to floating model aliases.
- Establish an automated integration regression test suite containing representative test cases that execute whenever model versions, base instructions, or upstream SDKs are updated.
- Monitor provider deprecation notices and sunset schedules well in advance of end-of-life dates to ensure smooth migration paths without production downtime.
- Run comparative evaluations on staging environments before cutting production traffic over to newly released model tiers.

## Procedure

1. Define a core regression test suite consisting of representative input payloads and expected output assertions for critical integration paths.
2. Execute the test suite against the existing production model configuration to establish a baseline success rate.
3. Update model version strings or swap provider endpoints in staging configuration files.
4. Re-run the regression test suite, analyzing output quality, structural JSON compliance, latency differentials, and token cost impacts.
5. Promote the new model configuration to production only after regression tests pass successfully and performance baselines are confirmed.

## Anti-patterns

- Relying exclusively on floating model aliases in production without version pinning or regression testing.
- Upgrading production model versions without running an automated regression test suite.
- Ignoring provider deprecation warnings until models reach hard end-of-life sunset dates.
- Changing multiple variables simultaneously (such as swapping models while rewriting base instructions) during migration testing.

## Done checklist

- [ ] Production applications utilize pinned or version-controlled model identifiers.
- [ ] Automated regression tests execute successfully against model configurations.
- [ ] Deprecation schedules and sunset dates are tracked systematically.
- [ ] Staging evaluations precede production model migrations.

## Sources

- Anthropic, "Model Versioning and Lifecycle Policy", <https://docs.anthropic.com/en/docs/about-claude/models#model-versioning>
- OpenAI, "Model Lifecycle and Versioning", <https://platform.openai.com/docs/models>

⚠️ Provider versioning schemes, alias behavior, and deprecation notice periods change across vendors; review current platform lifecycle policies regularly.


⚠️ Provider API pricing models and parameter default behaviors vary across releases; always verify operational metrics against current production traffic.

⚠️ Production deployment guidelines require thorough monitoring of token latency distributions and error retry frequency to maintain reliable client-side integrations.