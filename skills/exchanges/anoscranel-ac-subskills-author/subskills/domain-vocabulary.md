---
name: domain-vocabulary
domain: skill-authoring/domain-vocabulary
trigger: "When minting a new top-level domain: segment for a skill, or checking a segment is legal."
anti_trigger: "The skill's domain chain reuses an existing top segment already in this enum."
scope: "The closed enum of legal top-level domain: segments; the only file allowed to define them."
status: "seedling"
---

# Domain Vocabulary (the closed enum)

This file owns the **closed enum** of legal top-level `domain:` segments. It is data, versioned, and the **only** file allowed to define legal top
segments. A leaf's `domain:` is `<top-segment>/<...>`; the linter rejects any top segment
not in this enum.

## Standard

An open vocabulary lets a leaf exit its parent's domain by naming a novel top segment —
defeating the in-domain constraint silently. A closed enum makes the
violation a linter error instead of a judgment call.

## The enum (top-level segments)

| top segment | governs | minted for |
|-------------|---------|-----------|
| `skill-authoring` | creating/decomposing/linting/vetting/install-gating/publishing skills-with-subskills, and discovering/evaluating/adopting third-party skills | ac-subskills-author, ac-release-publish, ac-skill-adoption (v0.8.0) |
| `security-hardening` | application security, OWASP, privacy, supply-chain, LLM-security, and running security as an operation | ac-security-engineer, ac-security-standards, ac-security-operations (v0.59.0) |
| `research-operations` | multi-source deep-research: planning, retrieval, verification, synthesis, reporting, statistical synthesis and pooling, and qualitative synthesis methods | ac-deep-researcher, ac-adversarial-corpus-challenge, ac-systematic-review-conduct, ac-meta-analysis-and-synthesis, ac-qualitative-synthesis (v0.61.0) |
| `prompt-engineering` | the craft of prompting models and agents: instruction design, patterns, evaluation, robustness, injection defense, and per-request value craft under API limits, and model evaluation suite design, and per-dollar token spend economics | ac-prompt-engineer, ac-single-request-value, ac-model-evaluation, ac-token-cost-optimization (v0.76.0) |
| `rsi` | RESERVED — self-improvement observe/propose leaves (`00-rsi`) + the shared `ac-rsi` core; never a task/action domain | SPEC-rsi-skills (github.com/anoscranel/rsi-skills) |
| `software-engineering` | software lifecycle practice: requirements, design, construction, testing, delivery, operations, maintenance, authoring agent-tool servers over open protocols, integrating model APIs into application code, read-only evidence-ranked architecture surveys of existing codebases, and modeling business domains: ubiquitous language, bounded contexts, aggregates, domain events, plus mobile clients, internationalisation, privacy engineering, event-driven design, chaos and capacity testing, cost, build systems, CLI design, and money arithmetic, GraphQL and streaming interfaces, retrieval systems, multitenancy, resilience budgets, durable execution, platform engineering, data contracts, webhook delivery, and client library design, and concurrency, replication, streams, analytical modeling, lifecycle, and cutover, frontend bundling, network edge delivery, code generation, supply chain, static analysis, and test environments, production debugging, resource exhaustion, scheduled jobs, text encoding, and time and clocks, and the layer below the language runtime, and operating against third-party API limits, and online controlled experiments, and GPU parallel-compute reasoning, email deliverability, time-series storage, and notification routing, and geospatial and realtime media transport, and SaaS tax geography | ac-agent-coding-governance, ac-api-design, ac-architecture, ac-architecture-survey, ac-chaos-and-capacity-testing, ac-ci-and-release, ac-cli-and-tool-design, ac-code-construction, ac-code-review, ac-codebase-maintenance, ac-cost-aware-engineering, ac-data-contracts, ac-database-changes, ac-debugging, ac-design-taste, ac-domain-modeling, ac-durable-execution, ac-event-driven-architecture, ac-frontend-ui, ac-git-workflow, ac-graphql-and-streaming-apis, ac-i18n-and-localisation, ac-llm-api-integration, ac-mcp-authoring, ac-mobile-client-engineering, ac-money-arithmetic, ac-monorepo-and-build-systems, ac-multitenancy-and-isolation, ac-performance, ac-platform-engineering, ac-privacy-engineering, ac-quality-verification, ac-reliability, ac-resilience-budgets, ac-retrieval-and-vector-systems, ac-sdk-and-client-library-design, ac-software-engineering-standards, ac-spec-writing, ac-task-planning, ac-testing, ac-webhook-and-async-delivery, ac-distributed-state-and-replication, ac-analytical-data-modeling, ac-stream-processing, ac-service-lifecycle, ac-data-migration-cutover, ac-async-and-concurrency, ac-frontend-bundling, ac-network-edge-and-delivery, ac-code-generation-and-apis, ac-software-supply-chain, ac-static-analysis, ac-test-environments, ac-production-debugging, ac-resource-exhaustion-diagnosis, ac-scheduled-jobs, ac-time-and-clocks, ac-text-encoding, ac-binary-formats, ac-transaction-isolation, ac-audit-logging, ac-memory-layout-and-caches, ac-low-level-io-and-syscalls, ac-compilers-and-abis, ac-wasm-and-sandboxes, ac-content-addressed-storage, ac-sharding-and-placement, ac-consensus-protocols, ac-message-queues, ac-byzantine-consensus, ac-caching-and-invalidation, ac-query-and-index-design, ac-database-engine-internals, ac-api-limit-operations, ac-online-experiments, ac-client-state-and-interaction, ac-ml-systems-practice, ac-data-pipeline-orchestration, ac-gpu-and-parallel-compute, ac-payments-and-billing-engineering, ac-recommendation-systems, ac-lexical-search-engineering, ac-email-deliverability, ac-time-series-storage, ac-notification-systems, ac-geospatial-data, ac-realtime-media-transport, ac-media-pipelines, ac-content-moderation, ac-saas-tax-and-geography (v0.74.0) |
| `writing` | non-fiction and professional writing process and genres, above sentence level, plus codifying and auditing a brand's voice and style rules across a document corpus, and co-authoring structured documents through a staged authoring workflow | ac-academic-writing, ac-brand-guidelines, ac-business-writing, ac-dataviz, ac-doc-coauthoring, ac-drafting, ac-editing, ac-evidence-and-citation, ac-narrative-writing, ac-news-writing, ac-persuasive-writing, ac-plain-language, ac-proposal-writing, ac-slide-decks, ac-technical-writing, ac-voice-and-style, ac-writing-standards (v0.58.0) |
| `collaboration` | transferring work between people, sessions, and agents: handoff artifacts, context selection, resumption checks, incoming-queue triage and dispatch, and designing and supervising multi-agent work: role splits, delegation prompts, verification loops | ac-handoff, ac-inbound-triage, ac-multi-agent-orchestration (v0.11.0) |
| `crypto-trading` | discretionary crypto trading as a documented decision process: pre-trade memos, risk budgets, position sizing, invalidation and kill criteria, journals and periodic review, plus options and volatility craft, plus account security for exchange access, and crypto option conventions, and quantitative methods for systematic trading | ac-crypto-trading-discipline, ac-liquidation-hunt-analysis, ac-perp-venue-diligence, ac-cascade-forensics, ac-market-data-collection, ac-backtest-integrity, ac-funding-and-basis, ac-liquidation-risk-management, ac-order-execution, ac-stablecoin-collateral-risk, ac-trading-agent-desk, ac-derivatives-instrument-selection, ac-portfolio-construction, ac-token-diligence, ac-trading-operations-runbook, ac-onchain-flow-analysis, ac-options-and-volatility, ac-exchange-account-security, ac-crypto-options, ac-quantitative-methods-for-trading (v0.59.0) |
| `investing` | equity and multi-asset investing practice: fundamental research, valuation, portfolio policy, behavioural discipline, fixed income and rates, currency exposure, corporate actions, market structure, alternatives, macro reading, fund selection, insurance, bank credit, performance measurement, liquidity risk, factor construction, scenario stress testing, alternative data, earnings quality, special situations, tax-aware investing, credit curve, index methodology design, and institutional positioning, order flow and operations analysis, retirement drawdown, estate succession, structured products, portfolio leverage, and stock, FX and commodity trading venues, bond futures and equity index futures, credit derivatives, market-specific option conventions across FX, rates, commodities, equities, credit, performance measurement, liquidity risk, factor construction, scenario stress testing, alternative data, earnings quality, special situations, tax-aware investing, credit curve, index methodology design, and institutional positioning, order flow and operations, and broker and custody selection, hybrid capital, securitisation and tranches, fund reporting metrics, liability-driven investing, transaction cost analysis, rating mechanics, trade policy exposure, insurance-linked securities, investment oversight, direct real estate, and forensic accounting, distressed restructuring, primary equity issuance, municipal credit, fund wrappers, equity compensation, corporate treasury, pension risk transfer, project finance, and sovereign debt, M&A transaction execution, and venture financing mechanics | ac-equity-research, ac-valuation, ac-investment-policy-statement, ac-behavioral-investing, ac-fixed-income-and-rates, ac-currency-and-fx-risk, ac-corporate-actions, ac-equity-market-structure, ac-alternatives-and-real-assets, ac-macro-and-policy-reading, ac-trading-records-and-tax, ac-bank-and-credit-analysis, ac-retirement-and-drawdown, ac-fund-selection, ac-insurance-and-risk-transfer, ac-estate-and-succession, ac-structured-products, ac-broker-and-custody-selection, ac-portfolio-leverage, ac-stock-trading, ac-forex-trading, ac-commodities-trading, ac-rates-trading, ac-equity-index-futures, ac-credit-derivatives, ac-fx-options, ac-rates-options, ac-commodity-options, ac-equity-options, ac-credit-options, ac-institutional-positioning, ac-institutional-order-flow, ac-institutional-operations, ac-performance-measurement, ac-earnings-quality, ac-special-situations, ac-tax-aware-investing, ac-liquidity-risk, ac-factor-investing, ac-scenario-and-stress-testing, ac-alternative-data, ac-credit-curve, ac-index-methodology-design, ac-convertible-and-hybrid-capital, ac-capital-return-policy, ac-private-credit, ac-shareholder-activism, ac-climate-and-transition-risk, ac-manager-and-vehicle-diligence, ac-securities-litigation, ac-emerging-market-access, ac-portfolio-financing, ac-trade-finance, ac-securitisation-and-tranches, ac-fund-reporting-and-metrics, ac-liability-driven-investing, ac-transaction-cost-analysis, ac-credit-rating-mechanics, ac-trade-policy-and-restrictions, ac-insurance-linked-securities, ac-investment-oversight-and-ocio, ac-direct-real-estate, ac-forensic-accounting, ac-distressed-and-restructuring, ac-equity-capital-markets, ac-municipal-bonds, ac-fund-structures-and-wrappers, ac-share-based-compensation, ac-corporate-treasury, ac-pension-risk-transfer, ac-infrastructure-and-project-finance, ac-sovereign-debt, ac-ma-transaction-execution, ac-venture-financing (v0.75.0) |
| `critical-thinking` | interrogating ideas, plans, and claims before commitment, and generating options for them: assumption surfacing, failure mapping, evidence tests, alternatives, close-out, idea generation, divergence, convergence | ac-interrogation, ac-ideation (v0.7.0) |

The meta-skill's own chain is `skill-authoring`; the pilot's is `security-hardening`.

## Decision rules

- A skill whose domain fits an existing segment reuses that segment.
- No existing segment covers the domain → add exactly one row here, then lint.
- Keep segments coarse (a domain, not a topic); leaves add fine segments below the top
  via prefix-extension, which needs no enum entry.

## Procedure

1. Confirm no existing segment already covers the domain (dedup first).
2. Add one row: top segment | what it governs | the skill that minted it.
3. Re-run lint-tree on every authored tree that names a top segment.

## Anti-patterns

- Inventing a top segment inline in a leaf instead of editing THIS file.
- Adding a topic-level segment that a fine segment (prefix-extension) would cover.

## Done checklist

- New segment row committed; all authored trees lint PASS against the updated enum.

## Sources

- House standard for skills-with-subskills (unpublished).
- SPEC-rsi-skills (`rsi` reservation): https://github.com/anoscranel/rsi-skills; the skills directory the vocabulary indexes: <https://skills.sh>