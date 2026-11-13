---
name: landscape-and-registries
domain: skill-authoring/landscape-and-registries
trigger: "Searching for third-party agent skills across registries; asking where agent skills live; deciding whether a registry index or open repository is reliable"
anti_trigger: "Judging the security or maintenance of a single skill (subskills/trust-signals.md); vetting skill code for injection (subskills/security-vetting.md)"
scope: "Mapping where third-party skills live, distinguishing curated registries from open source listings, searching by concrete task rather than name, and evaluating registry size or install count as popularity signals rather than quality verdicts"
status: "seedling"
---

# Landscape and Registries

## Standard

- **Agentskills.io**: standardisation of agent skill structure, metadata, and routing boundaries across tools and frameworks. <https://agentskills.io>
- **Vercel AI / skills.sh ecosystem**: open registries providing search, installation counts, and security scanner audits for community-contributed agent skills. <https://skills.sh>

## Decision rules

- **Search by concrete capability, not by package name**: query registries using specific verbs and task boundaries (e.g., "audit license", "parse PDF", "lint markdown") rather than vague descriptive categories.
- **Treat install counts as popularity signals, not quality verdicts**: high download numbers or prominent listing placement indicate community attention or packaging convenience, but never guarantee correctness, safety, or fitness for purpose.
- **Prefer curated audit registries over raw unvetted repositories**: when discovering skills, use platforms that attach automated security scans and license checks to every index entry before falling back to unmanaged source code forges.
- **Verify index metadata against source code**: never assume a registry description, author attribution, or summary matches the actual instructions inside the skill directory until the repository files are inspected directly.

## Procedure

1. Identify the concrete operational task or workflow gap that requires a third-party agent skill.
2. Query the primary community skill registries using precise capability keywords matching the task domain.
3. Filter search results by checking whether independent automated security scans are available for the listed packages.
4. Record candidate skill repositories along with their published install counts, last update timestamps, and author identities.
5. Cross-reference registry metadata against the source repository files to confirm that the documented instructions reflect actual file contents.
6. Select the top candidate that meets task requirements and proceeds to security and provenance vetting stages.

## Anti-patterns

- Relying on registry placement or high install counts as proof that a skill is secure or well-engineered.
- Searching registries with broad single-word terms that return irrelevant workflows and bloat the evaluation queue.
- Trusting registry description summaries without inspecting the underlying SKILL.md and subskill files.
- Treating open community listings and curated security-audited directories as interchangeable trust tiers.

## Done checklist

- [ ] Task requirements defined using concrete operational verbs.
- [ ] Primary community registries searched with precise keywords.
- [ ] Candidate repositories identified with install counts and update dates recorded.
- [ ] Registry metadata verified against repository file listings.
- [ ] Top candidate selected for subsequent security and provenance review.

## Sources

- Agentskills.io. _Agent Skills Specification and Interoperability Standard_. <https://agentskills.io>
- Skills.sh Registry. _Curated Discovery and Automated Audit Platform for Agent Skills_. <https://skills.sh>
