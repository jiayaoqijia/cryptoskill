---
name: role-and-scope
domain: collaboration/role-and-scope
trigger: "Defining boundaries and responsibilities for multiple agents on a shared project; setting up producer-validator separation"
anti_trigger: "Giving all agents identical prompts and full access to everything; naming roles by vague personas"
scope: "Designing the split: one outcome per agent; non-overlapping scopes; producer-is-not-validator invariant; least-privilege assignment"
status: seedling
---

# Role and Scope

## Standard

- **Saltzer and Schroeder, "The Protection of Information in Computer Systems" (1975)**: principle of least privilege — every agent must operate using the least set of privileges and resources necessary to complete its specific sub-task. <https://dl.acm.org/doi/10.1145/361011.361067>
- **ISO/IEC 25010 Quality Model**: functional suitability and security isolation require clear separation of concerns between operational modules. <https://iso.org/standard/35733.html>
- **Producer-validator separation invariant**: the agent that writes or generates an artifact cannot be the agent that verifies or signs off on it, preventing confirmation bias.
- **House convention**: roles are named by function (e.g., extractor, validator, aggregator) rather than personality or persona. ⚠️ House threshold.

## Decision rules

1. Each agent must have exactly one primary output deliverable and one clear success criterion.
2. Two agents must never be granted write access to the same file or directory path simultaneously.
3. If an agent processes untrusted external content, it must not hold write access to core system files or network egress credentials in the same session.
4. Name every role by its mechanical function (e.g., `researcher`, `formatter`, `auditor`), never by an emotional persona.
5. If an agent's scope cannot be summarized in a single sentence without conjunctions, the scope is too broad.
6. The validator role must be structurally isolated from the producer role, receiving only the finished artifact and the original requirements.

## Procedure

1. List all required deliverables for the multi-agent operation.
2. Assign each deliverable to a single responsible agent role.
3. Define strict file-system and tool boundaries for each role using least-privilege principles.
4. Establish the producer-validator pair: designate which independent agent reviews each generated artifact.
5. Review role descriptions to ensure they use functional nouns rather than persona adjectives.
6. Verify that no two roles have overlapping write permissions or conflicting output paths.
7. Document the scope and permissions in the agent dispatch manifest.

## Anti-patterns

- **God agent.** One agent with access to all tools, all files, and all steps while others watch. Fix: partition permissions.
- **Shared scratchpad.** Multiple agents writing to the same temp file without coordination. Fix: assign distinct output paths.
- **Self-grading student.** An agent checking its own work and declaring success. Fix: assign an independent validator.
- **Persona inflation.** Giving agents elaborate fictional backstories instead of precise functional instructions. Fix: name by function.

## Done checklist

- [ ] Every agent has exactly one primary outcome and deliverable.
- [ ] No two agents share write access to the same path.
- [ ] Least-privilege principle applied to tools and file access.
- [ ] Producer-validator separation enforced.
- [ ] Roles named by mechanical function rather than persona.

## Sources

- Saltzer and Schroeder, "The Protection of Information in Computer Systems": <https://dl.acm.org/doi/10.1145/361011.361067>
- ISO/IEC 25010 Quality Model: <https://iso.org/standard/35733.html>
- Internal architectural notes on role separation and least-privilege enforcement.
