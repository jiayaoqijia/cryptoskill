# Trust Manifest v4 — final design after codex challenge

This is the design we will ship. It supersedes v1, v2, and v3.

The codex review (`/tmp/codex-review.md`) found 15 issues with v1, several of which v3 didn't fully address. This v4 incorporates the most important corrections:

- **The frame was wrong.** A skill's blast radius comes from its capabilities (can it execute shell? move funds? install packages?), not from its endpoint list. Trust starts with capabilities; ingredients are secondary. (codex #1)
- **`trustless` is marketing language**, not a classifier. Hardcoded Alchemy is not in the same risk class as a CEX. Cut it. (codex #2)
- **`local-first` is misappropriated** from Ink & Switch. Renamed to what it actually means. (codex #3)
- **Hash-and-lock is fake immutability** when most skills `npx` remote code or call hosted backends whose behavior changes without local diff. (codex #7)
- **Inline markdown rendering of third-party content is an XSS footgun.** (codex #9)
- **Composition matters.** Router/orchestrator skills dispatch to other skills at runtime; a static manifest cannot tell you what will run. (codex #6)
- **Don't reinvent SBOM/SLSA badly.** Use CycloneDX + in-toto + Sigstore directly. (codex #14)
- **Phases were backwards.** Shipping badges before the evidence is trustworthy creates false precision more harmful than showing nothing. (codex #13, #15)

What survived from v1-v3:
- Three-layer artifacts (`SKILL.md` + `SOURCE.md` + trust manifest)
- Auto-extraction by bot, human overlay
- L2BEAT/DefiLlama as authoritative label sources
- ERC-8004 as identity anchor (later)
- Risk rosette concept (but with corrected dimensions)
- Defer staking to phase 5+ pending demand

---

## Frame: capabilities first, ingredients second

Every skill answers ten capability questions before anything else. These are the **blast radius** axes. They're machine-extractable from the SKILL.md frontmatter (`allowed-tools`, `user-invocable`, `disable-model-invocation`, `metadata.openclaw.requires`) plus a static analysis pass over scripts.

| Capability | What it asks | Source |
|---|---|---|
| `auto_invocable` | Will the agent run this without user prompt? | `user-invocable` frontmatter inverted |
| `can_execute_shell` | Does it run arbitrary Bash? | `allowed-tools` includes Bash |
| `can_install_code` | Does it `npx`, `pip install`, `curl \| sh`, or download CLIs? | shell snippet scan |
| `can_write_files` | Does it edit user files? | `allowed-tools` includes Edit/Write |
| `can_browse_web` | Does it fetch arbitrary URLs? | `allowed-tools` includes WebFetch / WebSearch |
| `can_spawn_subagents` | Does it call sub-skills or other agents? | `allowed-tools` includes Agent / SubAgent |
| `can_move_funds` | Does it sign or broadcast transactions? | scripts call `sendTransaction`, signers, CEX endpoints |
| `requires_private_key` | Does it ask the user for a key, mnemonic, or wallet config? | regex on docs + scripts |
| `requires_hosted_operator` | Does correct behavior depend on a specific company's running infra? | computed from ingredient list |
| `uses_remote_install_script` | Does setup involve running a script downloaded from the internet? | shell snippet scan for `curl \| sh`, `wget \| sh` |

These are **negative-leaning facts**. The UI surfaces them as red flags, not green checks. "This skill can execute shell and install code" is a useful sentence even when nothing else is known.

The capability manifest is the foundation. Everything else (ingredients, audits, attestations) layers on top.

---

## Skill execution model (a single enum on every skill)

From codex #5, we add `execution_model`:

| Value | Meaning |
|---|---|
| `read_only` | Pure read; no writes, no signing, no installs |
| `analysis_only` | Read + transforms; produces text/data only |
| `unsigned_tx_builder` | Constructs unsigned calldata; user signs elsewhere |
| `local_executor` | Runs locally with user-provided keys/RPC |
| `installer_bootstrap` | Sets up a CLI, plugin, or local service first run |
| `hosted_executor` | Real execution happens on operator-controlled backend |
| `custodial_executor` | Operator holds funds during the operation (CEX) |
| `opaque_tool_wrapper` | Wraps a third-party tool whose internals are not inspectable |
| `router_orchestrator` | Dispatches to other skills/adapters at runtime |

This frames everything else. Audit questions, ingredient questions, and trust questions are different per execution model. A `read_only` skill scoring poorly on `audit_history` is fine. A `custodial_executor` scoring poorly on `audit_history` is a red flag.

---

## Custody model — replaces `trustless`

From codex #2. `trustless` is killed. We replace with five orthogonal fields:

| Field | Values |
|---|---|
| `custody_model` | `read_only` / `unsigned_calldata` / `local_signing` / `delegated_signing` / `custodial` |
| `approval_blast_radius` | scope of any token approvals issued (specific token + amount / specific token + unlimited / multiple tokens / not applicable) |
| `execution_authority` | who decides what the skill executes — `user_only` / `agent_with_confirmation` / `agent_autonomous` |
| `upgrade_escape_hatch` | for skills using upgradeable contracts: `none` / `time_locked` / `optional_exit` / `n_a` |
| `quote_data_trust` | for skills consuming external quotes/prices/data: `none` / `single_oracle` / `multiple_oracles` / `signed_attested` |

Together these capture what `trustless` was trying to gesture at, without flattening distinct risks.

---

## Operator dependence — replaces `local-first`

From codex #3. The dimension `local_first` becomes `operator_dependence` — a more honest name.

| Value | Meaning |
|---|---|
| `none` | No operator infrastructure required; works offline once installed |
| `interchangeable` | Any matching provider works (e.g. any Ethereum RPC) |
| `multiple_with_failover` | Skill knows about >1 operator and can fall back |
| `single_replaceable` | One operator default but user can override |
| `single_required` | One operator is required and not user-overridable |

A user-specified Infura URL is `interchangeable`, not `local-first`. A truly local-first skill — one that holds state on disk and survives vendor disappearance — is rare and we should not pretend most skills qualify.

---

## Risk rosette (6 axes, 0-3 each, never collapsed)

Same dimensions as v3, kept because they're orthogonal to capability/custody:

| Axis | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Source provenance** | unverified | repo public | + signed commits | + Sigstore attestation tying CI build to source SHA |
| **Documentation** | none | SKILL.md exists | + traceability docs↔code | + per-call docs for every external endpoint |
| **Test coverage** | none | smoke test | + integration tests | + golden outputs + adversarial suite |
| **Permission scope** | all tools, no caps | scoped tools listed | + per-tool justification | + capability tokens enforced at runtime |
| **Network egress declaration** | unknown | declared list | declared list, all `interchangeable` or better | + signed runtime network log proves manifest matches reality |
| **Remote artifact pinning** | unpinned (`npx pkg`, `curl \| sh`) | versions pinned | + integrity hashes | + content-addressed (OCI digests, git SHAs, signed releases) |

The 6th axis (remote artifact pinning) is new in v4, prompted by codex #7. It directly addresses "fake immutability" — a skill that runs `npx polymarket-cli@latest` without integrity hash gets 0 here regardless of how clean its scripts look.

The single Stage (0/1/2) is **derived** from the rosette + capabilities, not asserted. We compute it server-side. Authors don't claim a Stage; they document the underlying facts and the system tells them what Stage they're at.

---

## Audits — scoped records, not global badges

From codex #8. Each audit is a record, not a yes/no:

```yaml
audits:
  - subject: skill_text          # skill_text | skill_scripts | target_protocol | infrastructure | runtime_behavior
    artifact_digest: sha256:...  # hash of the exact thing audited
    scope: |
      Reviewed SKILL.md and scripts/main.py. Did NOT review the Polymarket
      backend API or the polymarket-cli binary downloaded by the install
      script.
    reviewer:
      name: Trail of Bits
      identity: github:trailofbits  # OIDC identity for keyless verification
    date: 2026-03-15
    expires_at: 2027-03-15
    exclusions:
      - "Behavior of remote polymarket-cli once installed"
      - "Backend API correctness"
    report_url: https://github.com/...
    signature: sigstore_keyless_url://...
```

The UI renders "audited components" — never a single global ✓.

---

## Ingredients — CycloneDX, no reinvention

From codex #14. We adopt CycloneDX 1.7 directly. The ingredient list lives in a standard `bom.cdx.json` file alongside `TRUST.md`, with our skill-specific extensions in a `cryptoskill:` namespace:

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.7",
  "metadata": {
    "component": {"type": "application", "name": "binance-spot-api"}
  },
  "components": [
    {
      "type": "service",
      "name": "Binance Spot API",
      "endpoints": ["https://api.binance.com"],
      "properties": [
        {"name": "cryptoskill:trust_label", "value": "trusted_operator"},
        {"name": "cryptoskill:operator", "value": "Binance"},
        {"name": "cryptoskill:label_source", "value": "hand_curated"},
        {"name": "cryptoskill:label_fetched_at", "value": "2026-04-01T00:00:00Z"}
      ]
    }
  ]
}
```

Components support all CycloneDX types (`service`, `application`, `library`, `cryptographic-asset`). We don't need to invent ingredient kinds; CycloneDX has them.

`bom.cdx.json` is bot-generated. Human overlay still goes in `TRUST.md` frontmatter.

For runtime locators (codex #4), we add a `runtime_locators` extension:

```json
{
  "type": "library",
  "purl": "pkg:npm/polymarket-cli@1.2.0",
  "hashes": [{"alg": "SHA-256", "content": "..."}],
  "properties": [
    {"name": "cryptoskill:install_method", "value": "remote_install_script"},
    {"name": "cryptoskill:install_url", "value": "https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh"},
    {"name": "cryptoskill:integrity", "value": "unverified"}
  ]
}
```

This is what proper provenance looks like. A skill bootstrapping a remote CLI without integrity hash is now visible as a flag.

---

## Composition / runtime expansion (router skills)

From codex #6. Some skills (e.g. `openclaw-trading-suite`) dispatch to adapters at runtime. Their static manifest cannot answer "which dependency graph runs?" because it depends on user choice.

We add an `expansion` field on the manifest:

```yaml
expansion:
  type: router  # static | router | dynamic
  routes:
    - condition: "input_token in ['ETH', 'USDC'] and chain == 'ethereum'"
      delegates_to: skills/defi/uniswap-official-swap-integration
    - condition: "chain == 'solana'"
      delegates_to: skills/defi/jupiter-official-swap
  unbounded: false  # true if can route to skills not enumerated
```

Router skills get a "depends on selected route" warning in the UI with links to each route's manifest. The bot computes the **union** of capabilities across all enumerated routes — a router that delegates to one custodial executor is itself custodial-capable.

`unbounded: true` is a strong red flag (skill can route to anything).

---

## Attestations — Sigstore + in-toto, anchored later in ERC-8004

From codex #14. We use the standard formats directly:

- **Build provenance** — SLSA L2+ provenance signed via Sigstore keyless OIDC
- **Audit attestation** — in-toto Statement with a custom `cryptoskill/audit/v1` predicate type (CycloneDX 1.7 has a similar field, we use whichever is more adopted by audit firms)
- **Verification** — `cosign verify-attestation --certificate-identity ... --certificate-oidc-issuer ...`

ERC-8004 anchoring is **deferred to Phase 4+**. When we do anchor, the skill's Identity Registry entry contains:

```
metadata:
  - key: "cryptoskill:trust-manifest"
    value: "ipfs://Qm..."  # Content-addressed manifest
  - key: "cryptoskill:bom-cdx"
    value: "ipfs://Qm..."
```

Reputation Registry is used for per-dimension feedback. Validation Registry is used only for **objective machine-checkable claims** (codex #11, #12), e.g.:

- "Does the bot's re-extracted ingredient list match the published `bom.cdx.json`?"
- "Does the Sigstore signature verify against the claimed identity?"

Subjective claims (was the audit good? does this skill behave well in practice?) stay **off-chain, signed, scoped, and non-slashable**. We do not put juries on those questions.

---

## No TCR. No new token.

From codex #11. We are not building a TCR.

Pre-Phase 5: attestations are **signed reviewer endorsements**. Reviewer reputation matters; stake doesn't.

Post-Phase 5 (only if we see organic demand): bounty-style rewards for **demonstrated falsehoods of objective claims**, not slashing of subjective opinions. The bounty is paid by the registry from a small fee on premium features (if we ever ship them) or from a sponsor pool. Stake is per-claim, not on a token.

This is what the prior art actually supports. AdChain failed because it pretended subjective trust could be priced. We don't repeat that.

---

## File viewer — sanitized or external

From codex #9. We do not inline-render arbitrary third-party markdown.

Phase 1 ships **external links to GitHub** for SKILL.md viewing. No registry-side rendering of skill content.

Phase 2 (later) adds an inline viewer **only after** we have a hardened pipeline:
- Server-side render through `markdown-it` with strict HTML sanitization (no raw HTML, no `javascript:` links, no embedded `<script>`)
- All links open in new tabs with `rel="noopener noreferrer"`
- Embedded images proxied through our domain to break tracking and prevent unverified external image fetches
- Pre-rendered to static HTML during the bot cycle and served from our origin

Until that pipeline exists, the skill page just says "View source on GitHub" with a link.

---

## UI: red flags first, green checks last

From codex #13.

Default state for any skill on the page:

```
Binance Spot API
Stage: not classified yet (Stage 0 minimum)

⚠ Capabilities
  · Can execute shell
  · Can move funds
  · Custodial execution model
  · Requires hosted operator: Binance

📋 Coverage
  · Source: visible
  · Audits: 0
  · Egress declarations: 5 / unknown total

🔍 Source: View on GitHub →
```

We never show "Trustless: ✓" because that field doesn't exist. We never show "Audited" as a single check; we show the audit count and a link.

Filters in v4 are negative-only:
- `Cannot execute shell`
- `Cannot move funds`
- `No hosted operator required`
- `No remote install scripts`

These are unambiguous. Positive filters (`Trustless`, `Local-first`) are absent.

---

## Phases (revised)

| Phase | Deliverable | Why this order |
|---|---|---|
| **1** | Capability manifest extractor (the 10 negative-leaning facts) + execution_model classifier + GitHub link viewer | Establish the foundation — what can each skill do? Honest, conservative, immediately useful. |
| **2** | CycloneDX `bom.cdx.json` ingredient extractor + AST scan + L2BEAT/DefiLlama label fetcher with provenance | Layer the dependency graph on the capability foundation |
| **3** | Risk rosette + scoped audit records + custody/operator dependence fields + UI surfacing red flags | Add the secondary trust signals |
| **4** | Sigstore signing pipeline for `cryptoskill_team` attestations + in-toto Statements + manual third-party audit submission flow | Get cryptographically verifiable attestations flowing |
| **5** | ERC-8004 Identity registration for skills with manifests; on-chain anchor for SHA-pinned manifests; objective-only Validation Registry checks | Censorship-resistant anchor, no subjective slashing |
| **6** | Hardened inline viewer + composition expansion view (router skills) + bounty pool for objective falsehoods | Polish + demand-driven extras |

Phases 1-3 are the table stakes. Phase 4 is the cryptographic skeleton. Phase 5 is the on-chain anchor. Phase 6 is polish.

We **do not** ship Phase 1's badges to users until Phase 3's evidence is in place. UI sees the manifest as data; the badges/filter live in Phase 3 onward.

---

## What we cut

From codex #15:

- ❌ `trustless` badge (replaced by 5 specific fields)
- ❌ `local_first` (replaced by `operator_dependence`)
- ❌ Hand-curated 500-host table (kept ~50 for things outside L2BEAT/DefiLlama)
- ❌ Inline markdown render of third-party content in Phase 1 (deferred to Phase 6 with hardening)
- ❌ TCR / slashing on subjective claims
- ❌ Custom ingredient schema (using CycloneDX directly)
- ❌ "Hash and lock" as a substitute for proper artifact pinning
- ❌ Self-attestations (`kind: self`)
- ❌ Pre-Phase-5 community attestations (sock puppet risk)

## What we kept

- ✅ Three-artifact split (`SKILL.md` + `SOURCE.md` + manifest)
- ✅ Bot-owned `.auto.yaml`, human overlay
- ✅ Risk rosette (with corrected axes)
- ✅ L2BEAT/DefiLlama as authoritative label sources
- ✅ ERC-8004 as identity anchor (deferred to Phase 5)
- ✅ Per-dimension scoring, never collapsed
- ✅ `unknown` as honest default
- ✅ Migration: bot generates manifests for all 1256 skills in one batch

---

## Next steps

1. Land this v4 doc.
2. Build Phase 1 — capability manifest extractor for all 1256 skills.
3. Verify the "what can this skill do?" answers against a sample of 20 hand-reviewed skills.
4. Phase 2 once Phase 1 is honest.

The lesson from both reviews: **honest "unknown" beats false green checks**. Ship the conservative version and let the manifest fill in over time.

---

## References

- v1 — `docs/TRUST.md` (original sketch)
- v2 — `docs/TRUST-v2.md` (CC engineering review punch list)
- v3 — `docs/TRUST-v3.md` (synthesized prior art + L2BEAT rosette)
- CC review — `/tmp/claude-1001/.../a399ac4fcc6081c48.output`
- Codex review — `/tmp/codex-review.md`
- Research — TCRs, ERC-8004, L2BEAT, SLSA, CycloneDX, Sigstore, GoPlus AgentGuard, Snyk Agent Scan, Oathe, EigenLayer, Optimism Cannon, Ink & Switch local-first
