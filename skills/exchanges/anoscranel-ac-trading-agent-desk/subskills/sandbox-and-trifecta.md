---
name: sandbox-and-trifecta
domain: crypto-trading/sandbox-and-trifecta
trigger: how to sandbox trading agents, trifecta invariant for agent security, untrusted content credentials egress separation
anti_trigger: trusting prompt boundaries, putting API keys in agent context, allowing network access to untrusted parsers
scope: Disjoint sandboxes, the trifecta invariant, and tool absence over prompt wording for agent security
status: seedling
---

## Standard
The sandbox and trifecta standard enforces absolute structural isolation between three hazardous capabilities in any agentic trading infrastructure: processing untrusted external content (such as scraped news, forum posts, or API payloads), holding private credentials (such as exchange API keys, private keys, or database passwords), and possessing outbound network egress capability. The trifecta invariant dictates that no single execution context or agent session may hold more than one of these three capabilities simultaneously. 

Security engineering principles for autonomous systems (https://doi.org/10.1109/SP.2019.00028) demonstrate that prompt wording and instruction-based guardrails are insufficient to prevent indirect prompt injection. Attackers embedding malicious instructions in public RSS feeds or order books can easily bypass soft constraints. Therefore, security is enforced strictly through disjoint physical or virtual sandboxes with hardware- or OS-level capability restrictions, ensuring that an agent parsing untrusted web data physically lacks access to credentials and network egress (https://arxiv.org/abs/2302.12173).

## Decision rules
- Rule 1: Ingestion agents processing untrusted external text must execute in an isolated sandbox with zero network egress and zero access to credential stores.
- Rule 2: Credential-holding execution modules (signing transactions, submitting orders) must operate in air-gapped or strictly firewalled environments that never parse external raw text.
- Rule 3: Egress-enabled communication tools must never interface directly with prompt-driven language models handling untrusted content.
- Rule 4: Security boundaries must be enforced via container network namespaces, file system permissions, and explicit IAM policies, never via prompt instructions.
- Rule 5: Any configuration change or code update touching sandbox boundaries requires an independent peer review and automated vulnerability scan.

## Procedure
1. Map all data flows in the trading desk architecture, identifying points where external data enters, where credentials are stored, and where network requests leave.
2. Partition the infrastructure into three disjoint security zones: Zone A (Untrusted Ingestion), Zone B (Computation & Storage), Zone C (Execution & Signatures).
3. Deploy Zone A agents inside restricted containers with read-only storage, disabled outbound internet access, and no environment variables containing keys.
4. Implement strict IPC (Inter-Process Communication) queues or message brokers between zones, ensuring data payloads are sanitized and validated against rigid schemas before crossing boundaries.
5. Conduct automated architecture audits that verify capability isolation and flag any violations of the trifecta invariant prior to deployment.

## Anti-patterns
- Anti-pattern 1: Storing exchange API keys in the environment variables of a container that also runs an LLM news scraping client.
- Anti-pattern 2: Relying on written instructions inside the model's context ("do not follow external instructions") to protect against indirect injection.
- Anti-pattern 3: Granting general-purpose network access tools to text summarization agents.
- Anti-pattern 4: Sharing temporary scratch volumes between ingestion sandboxes and execution modules.

## Done checklist
- [ ] Ingestion agents operate in sandboxes with verified zero egress and zero credentials.
- [ ] Credential stores are isolated from all prompt-processing execution paths.
- [ ] Inter-zone communication enforces strict schema validation and payload sanitization.
- [ ] Security posture relies on OS/container isolation rather than prompt wording.
- [ ] Architecture documentation and verification scripts are up to date (https://doi.org/10.1109/SP.2019.00028).

## Sources
- Security Boundaries and Principle of Least Privilege in Autonomous Systems: https://doi.org/10.1109/SP.2019.00028
- Mitigating Indirect Prompt Injection in Multi-Component Agent Architectures: https://arxiv.org/abs/2302.12173
