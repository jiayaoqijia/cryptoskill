---
name: architecture
domain: software-engineering/architecture
trigger: "\"How should we structure this system\", \"monolith or microservices\", \"draw the architecture\", \"which architecture style\", \"will this scale\", \"C4 diagram\"."
anti_trigger: "Writing down a decision already made (subskills/adr.md); boundaries inside one codebase (subskills/module-design.md); the external API contract."
scope: "System structure, styles and quality-attribute trade-offs, C4 views"
status: "seedling"
---

# Architecture

## Standard

⚠️ The primary standard is paywalled; these points come from secondary sources and the public summary.

- **SWEBOK v4** makes Software Architecture its own knowledge area (https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics).
- **ISO/IEC/IEEE 42010:2022**: architecture descriptions use viewpoints and views for stakeholder concerns.
- **C4 model** (Simon Brown, https://c4model.com): Context → Container → Component → Code. **arc42** (https://arc42.org): 12-section template.
- **Styles**: layered/clean/hexagonal/onion all keep a stable domain core with inward dependencies. Modular monolith first; extract services at proven seams (Fowler, MonolithFirst, https://martinfowler.com/bliki/MonolithFirst.html).
- **Trade-off analysis**: ATAM (SEI) finds sensitivity and trade-off points by scenario.
- **Fitness functions** check architecture rules in CI (Ford et al., *Building Evolutionary Architectures*; ArchUnit, dependency-cruiser).

## Decision rules

1. Name the top three quality attributes first (from ISO/IEC 25010:2023: e.g. performance efficiency, reliability, maintainability). Structure follows them.
2. Default to a modular monolith. Split a service out only when it needs independent deploy, independent scale, a separate team, or a separate compliance fence.
3. Never share one database between services. Each service owns its data.
4. Cross-service consistency uses sagas or a transactional outbox, not distributed transactions.
5. "Exactly-once delivery" claims mean effectively-once inside one system. Consumers stay idempotent.
6. Conway's law: structure follows team communication. Check team shape before drawing boxes.
7. Use DDD bounded contexts for complex domains. Skip tactical DDD for CRUD.
8. Every rule that matters gets a fitness function in CI.

## Procedure

1. Write the drivers: functional scope, top three quality attributes with scenarios, constraints (team, budget, compliance).
2. Draw C4 Level 1 (context): the system, its users, external systems.
3. Draw C4 Level 2 (containers): apps, data stores, queues, with protocols. Use Mermaid or Structurizr text kept in the repo.
4. Choose a style with rules 2–7. Write at least two candidate structures.
5. For each quality scenario, walk it through each candidate. Note where it breaks. That is a sensitivity point.
6. Pick one. Record it as an ADR with the rejected options.
7. Add fitness functions, e.g. dependency-cruiser rule "domain must not import infrastructure", or a latency test for the top scenario.
8. Draw C4 Level 3 only for containers that are complex. Skip Level 4.
9. Review the diagrams each quarter or on any new container.

## Anti-patterns

- Microservices before the domain is understood (distributed monolith).
- Shared database across services.
- Diagrams with unlabelled arrows.
- Architecture chosen for a résumé.
- Rules that live only in a wiki, not in CI.
- Big-bang rewrite instead of strangler fig (Fowler 2004).

## Done checklist

- [ ] Top three quality attributes have measurable scenarios.
- [ ] C4 L1 and L2 in the repo.
- [ ] Two or more candidates compared against the scenarios.
- [ ] ADR written for the choice.
- [ ] Fitness functions in CI for key rules.

## Sources

- <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- <https://rivergroup.ai/insights/the-case-for-boring-technology>
- https://c4model.com · https://arc42.org · https://martinfowler.com/bliki/MonolithFirst.html
