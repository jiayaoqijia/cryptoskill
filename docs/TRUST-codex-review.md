# Adversarial Review of `docs/TRUST.md`

1. **Severity: Critical**
   **Why it's wrong:** The doc treats trust as an inventory of endpoints and contracts, but AI-agent skills are primarily an authority-transfer problem. A skill with no hardcoded URL can still be dangerous if it can execute shell, install packages, browse the web, spawn subagents, write files, or auto-invoke. `docs/TRUST.md:16-20`, `docs/TRUST.md:123-133`, and `docs/TRUST.md:177-189` focus on dependencies, while real skill blast radius lives in capabilities like `allowed-tools`, `user-invocable`, and `disable-model-invocation`. Concrete examples: `skills/wallets/coinbase-official-send-usdc/SKILL.md:4-6` can move money through `npx awal`; `skills/defi/uniswap-official-swap-integration/SKILL.md:4` can edit files, execute package managers, fetch the web, and spawn a subagent.
   **What I would do instead:** Make a capability manifest first, not a trust manifest first. Record `side_effect_class`, `tool_permissions`, `can_move_funds`, `can_install_code`, `can_write_files`, `can_browse_web`, `can_spawn_subagents`, `auto_invocable`, and `requires_explicit_confirmation`. Dependency trust is secondary.
   **Refs:** `docs/TRUST.md:16-20`, `docs/TRUST.md:123-133`, `docs/TRUST.md:177-189`, `skills/wallets/coinbase-official-send-usdc/SKILL.md:4-6`, `skills/defi/uniswap-official-swap-integration/SKILL.md:4`

2. **Severity: Critical**
   **Why it's wrong:** `trustless` is defined in a way that is actively misleading for AI-agent skills. `docs/TRUST.md:161-169` says a skill is trustless if funds remain recoverable when operators disappear. That misses the main failure mode: the skill can still drain the user by generating toxic approvals, wrong recipients, bad calldata, malicious slippage, or social-engineering the user into exporting/importing keys, all without taking custody. It also confuses censorship with custody by saying a hardcoded Alchemy RPC makes a skill `trustless: no`. That is not the same risk as “Binance can seize funds.”
   **What I would do instead:** Kill the `trustless` badge. Replace it with separate fields: `custody_model` (`read_only`, `unsigned_calldata`, `local_signing`, `delegated_signing`, `custodial`), `approval_blast_radius`, `execution_authority`, `upgrade_escape_hatch`, and `quote/data_trust`. Those are real axes. “Trustless” is marketing language, not a reliable classifier here.
   **Refs:** `docs/TRUST.md:159-169`, `skills/trading/universal-trading/agents/openai.yaml:4`, `skills/defi/pendle-official-pendle-swap/SKILL.md:14-27`

3. **Severity: High**
   **Why it's wrong:** The doc abuses `local-first`. `docs/TRUST.md:149-157` and `docs/TRUST.md:305` redefine “local-first” to mean “every endpoint is user-overridable or decentralized.” That is not what local-first means. Ink & Switch local-first is about local ownership of data, offline survivability, and sync semantics. A user-specified Infura URL is not local-first. A public Ethereum RPC is not local-first. A hosted API with an override knob is not local-first.
   **What I would do instead:** Rename this dimension to something honest like `operator_dependence` or `endpoint_portability`. If you want to talk about local-first, only do it for skills that actually keep state locally and still work when the vendor disappears.
   **Refs:** `docs/TRUST.md:149-157`, `docs/TRUST.md:305`

4. **Severity: Critical**
   **Why it's wrong:** Static URL-regex extraction is nowhere near sufficient as the evidence base. `docs/TRUST.md:177-187` assumes regex scanning `SKILL.md`, `references/`, and `scripts/` will enumerate runtime dependencies. At scale this will explode with false positives and false negatives. False positives: docs links, marketing links, install guides, examples, explorer URLs, social links. False negatives: dynamic URLs built from env vars, package manager fetches, `npx`, `curl | sh`, downloaded CLIs, MCP servers, opaque built-in tools, browser extensions, WebSockets, OAuth callbacks, and whatever the installed package does after launch. `skills/prediction-markets/polymarket/SKILL.md:28-40` literally installs remote code and tells the user to put a private key in a config file. `skills/defi/uniswap-official-swap-integration/SKILL.md:18` installs a plugin. `skills/defi/pendle-official-pendle-swap/SKILL.md:4` depends on opaque semantic tools that never show up as URLs.
   **What I would do instead:** Separate `documentation_links` from `runtime_locators`. Extract from frontmatter, install metadata, shell snippets, package manifests, Dockerfiles, MCP configs, and tool declarations. Then add runtime tracing in a sandbox for representative executions. Static regex should be a weak hint, not the classifier of record.
   **Refs:** `docs/TRUST.md:177-187`, `docs/TRUST.md:286`, `skills/prediction-markets/polymarket/SKILL.md:28-40`, `skills/defi/uniswap-official-swap-integration/SKILL.md:18`, `skills/defi/pendle-official-pendle-swap/SKILL.md:4`

5. **Severity: High**
   **Why it's wrong:** The schema cannot express important classes of skills. It collapses everything into the same three badges plus an ingredient table, but the registry contains fundamentally different execution models: read-only data skills, unsigned-transaction builders, local shell wrappers, package/bootstrap installers, hosted executors, opaque tool wrappers, payment-gated skills, and orchestration/router skills. `skills/defi/pendle-official-pendle-swap/SKILL.md:14` only produces unsigned calldata. `skills/prediction-markets/polymarket/SKILL.md:28-40` bootstraps a CLI and local wallet config. `skills/trading/crypto-strategy-suite/SKILL.md:13-31` charges users through a billing API before execution.
   **What I would do instead:** Add a first-pass `skill_execution_model` enum: `read_only`, `analysis_only`, `unsigned_tx_builder`, `local_executor`, `installer/bootstrap`, `hosted_executor`, `custodial_executor`, `opaque_tool_wrapper`, `router/orchestrator`. Then ask different trust questions per class instead of pretending one schema fits all.
   **Refs:** `docs/TRUST.md:17-18`, `docs/TRUST.md:123-133`, `skills/defi/pendle-official-pendle-swap/SKILL.md:14-27`, `skills/prediction-markets/polymarket/SKILL.md:28-40`, `skills/trading/crypto-strategy-suite/SKILL.md:13-31`

6. **Severity: High**
   **Why it's wrong:** The design has no model for transitive or compositional trust. `docs/TRUST.md:16` says every external dependency a skill calls is enumerated, but some skills dispatch to other skills or to interchangeable adapters at runtime. `skills/trading/openclaw-trading-suite/references/adapter_plugin_contract.md:17-24` explicitly supports skill-backed routing, direct adapter routing, mutable provider preferences, and periodic rediscovery. A sibling `TRUST.md` cannot tell the user which dependency graph will actually execute.
   **What I would do instead:** Support transitive manifests and composition-time trust evaluation. For router/orchestrator skills, the only honest answer is “depends on selected route,” followed by route-specific manifests or runtime-expanded call graphs.
   **Refs:** `docs/TRUST.md:16`, `skills/trading/openclaw-trading-suite/references/adapter_plugin_contract.md:17-24`

7. **Severity: Critical**
   **Why it's wrong:** `Hash and lock` is fake immutability. `docs/TRUST.md:193` hashes `SKILL.md + scripts`, but many skills execute remote code or remote backends whose behavior can change without any local diff. `npx`, `npm`, `curl | sh`, hosted MCP servers, web apps, plugins, CLIs, semantic tools, model providers, DNS, and API backends all sit outside that hash. The manifest will look “fresh” while the real execution surface has changed under it.
   **What I would do instead:** Record remote artifacts with content-addressed locators where possible: package versions plus integrity hashes, OCI image digests, git SHAs, release checksums, pinned MCP server versions. For everything else, explicitly label it `mutable_remote_runtime` and refuse to imply immutability.
   **Refs:** `docs/TRUST.md:193`, `skills/wallets/coinbase-official-send-usdc/SKILL.md:6`, `skills/prediction-markets/polymarket/SKILL.md:28-31`

8. **Severity: High**
   **Why it's wrong:** `audited: yes` is defined far too loosely. `docs/TRUST.md:141-147` says a public report URL that reviewed the `SKILL.md` and scripts is enough. That is absurdly weak for agent skills. Auditing the prompt and local scripts tells you almost nothing about the remote CLI, backend API, hosted semantic tools, private SaaS, plugin install, or package manager behavior the skill actually relies on. It also ignores freshness, version binding, exclusions, and whether the report covered the exact artifact hash the registry is serving.
   **What I would do instead:** Replace the badge with scoped audit records. Each audit should bind to `subject`, `artifact_digest/version`, `scope`, `method`, `reviewer_identity`, `date`, `expires_at`, and `exclusions`. Then render “audited components” instead of a global green check.
   **Refs:** `docs/TRUST.md:141-147`, `docs/TRUST.md:197-217`, `skills/wallets/coinbase-official-send-usdc/SKILL.md:6`, `skills/defi/pendle-official-pendle-swap/SKILL.md:4`

9. **Severity: Critical**
   **Why it's wrong:** The file viewer design is an XSS footgun. `docs/TRUST.md:257-259` says to use GitHub raw API plus `marked` and render markdown directly into the page, with no iframe. These files come from public third-party repos and are exactly the sort of content an attacker will stuff with raw HTML, script gadgets, `javascript:` links, or phishing markup. You are proposing to turn the registry itself into a malware delivery surface.
   **What I would do instead:** Do not inline-render untrusted markdown without hard sanitization. Disable raw HTML, sanitize links, sanitize embedded images, or pre-render server-side through a trusted pipeline. If you cannot guarantee sanitization, link out to GitHub and skip inline rendering.
   **Refs:** `docs/TRUST.md:20`, `docs/TRUST.md:257-259`

10. **Severity: High**
   **Why it's wrong:** The known-host table is an operational fantasy at this scale. `docs/TRUST.md:187` proposes ~500 known hosts and contract labels with 6h updates. With 1200+ skills, long-tail domains, per-project subdomains, regional endpoints, custom RPCs, dynamic hosts, proxies, bridge contracts, and rapidly changing infra, this will rot immediately. Either you classify almost everything as `unknown`, or you overfit and silently mislabel things.
   **What I would do instead:** Keep the automated classifier tiny and high-signal. Detect a short list of obvious patterns: hardcoded CEX endpoints, hosted RPCs, package-manager execution, remote install scripts, custom writable shell, and opaque hosted tools. Everything else stays `unknown` until manually reviewed. Do not promise comprehensive trust classification from a 500-row lookup table.
   **Refs:** `docs/TRUST.md:178-187`, `docs/TRUST.md:271`, `docs/TRUST.md:284`

11. **Severity: Critical**
   **Why it's wrong:** The real TCR failure mode is not “wrong token choice.” It is challenge-cost asymmetry plus externalized harm. `docs/TRUST.md:221-230` assumes slashing creates honesty. It does not. Bad actors can spray many low-stake attestations, sybil across identities, and treat slashing as CAC. Honest challengers must do expensive technical work to disprove ambiguous claims, while user harm from a bad skill can be massively larger than the stake at risk. The attacker only has to make challenge economics unattractive; they do not need the claim to be true.
   **What I would do instead:** Do not use slashing for subjective trust claims. Start with signed, scoped endorsements and reviewer reputation. If you want financial incentives, reserve them for objective, machine-checkable claims only, and pay bounties for demonstrated falsehoods rather than pretending the stake covers user harm.
   **Refs:** `docs/TRUST.md:221-230`, `docs/TRUST.md:288`

12. **Severity: High**
   **Why it's wrong:** The proposed resolution model is epistemically broken. `docs/TRUST.md:227` offers “Kleros-style jury OR deterministic on-chain check.” Deterministic checks can only settle trivial facts. Juries are terrible at nuanced, dynamic, agent-specific claims that require environment reconstruction, tool understanding, prompt interpretation, backend behavior, and adversarial reasoning. The result will be one of two bad outcomes: only trivial claims get challenged, or subjective disputes get decided arbitrarily.
   **What I would do instead:** Split claims into two buckets. Bucket 1: objective facts the bot can re-measure offchain. Bucket 2: subjective reviews that stay offchain, signed, scoped, and non-slashable. Do not force a court game onto claims that are not crisply decidable.
   **Refs:** `docs/TRUST.md:221-230`

13. **Severity: High**
   **Why it's wrong:** The badge/filter UI creates false precision and dangerous authority. `docs/TRUST.md:240-245` and `docs/TRUST.md:261-263` make `Audited`, `Local-first`, and `Trustless` look like clean truth values that users and agents can filter on. They are not. With weak evidence and partial coverage, a false positive `trustless: yes` badge will be more harmful than showing nothing. This is especially bad if you later expose `/api/trust/{skill_id}` and let agents gate installs on it.
   **What I would do instead:** Default to “unreviewed,” “partial evidence,” and “unknown coverage.” Show raw facts and red flags before you show green badges. If you ship filters, ship only hard negatives first, such as “contains remote install script,” “can execute arbitrary Bash,” “requires hosted operator,” or “requires local private key config.”
   **Refs:** `docs/TRUST.md:240-245`, `docs/TRUST.md:261-263`, `docs/TRUST.md:316`

14. **Severity: High**
   **Why it's wrong:** The design is reinventing a worse version of several existing standards. The “ingredient list” is a weak SBOM. “Hash and lock” is a weak provenance attestation. “Attestors” are a weak signed-claim format. ERC-8004 is identity anchoring, not provenance, evidence, or truth resolution. Right now you are taking the hard parts from SPDX/CycloneDX, in-toto/SLSA/Sigstore/DSSE, and standard attestation systems, then reimplementing them with less precision and less interoperability.
   **What I would do instead:** Use a standard component inventory format first, preferably CycloneDX or SPDX with extensions for services and trust annotations. Use in-toto/SLSA-style attestations or Sigstore/DSSE envelopes for signed provenance and review claims. If you want on-chain identity, map those signed claims into ERC-8004 or EAS later. Do not let the chain-identity layer dictate the evidence model.
   **Refs:** `docs/TRUST.md:193`, `docs/TRUST.md:197-230`, `docs/TRUST.md:296-305`

15. **Severity: High**
   **Why it's wrong:** The phase plan is backwards and too ambitious. `docs/TRUST.md:267-278` ships badges, ingredient tables, filters, and a file viewer before the evidence model is trustworthy. That is exactly how you create a high-confidence-looking system that is wrong in the most dangerous cases. The TCR phase then adds complexity before you have crisp claim semantics.
   **What I would do instead:** The simplest useful version is much smaller:
   - Ship a `capabilities + external operators` manifest, not `trustless/local-first`.
   - Extract only explicit high-signal facts: `allowed-tools`, `auto_invocable`, `can_install_packages`, `can_execute_shell`, `can_move_funds`, `requires_private_key`, `requires_hosted_operator`, `uses_remote_install_script`.
   - Keep `audits[]` as scoped records, not a global yes/no.
   - Default unknowns aggressively.
   - Cut `trustless`.
   - Cut `local-first`.
   - Cut ERC-8004/TCR entirely.
   - Cut inline file rendering until you have hardened sanitization.
   - Cut the “500 known hosts” ambition.
   That version would actually ship and be useful.
   **Refs:** `docs/TRUST.md:149-169`, `docs/TRUST.md:177-193`, `docs/TRUST.md:221-230`, `docs/TRUST.md:257-259`, `docs/TRUST.md:267-278`
