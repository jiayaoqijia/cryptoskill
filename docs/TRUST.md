# Trust Manifest

The implementation spec for skill trust at cryptoskill.org. Supersedes earlier drafts in `docs/archive/`.

This doc has been through two rounds of independent review (Claude Code engineering review + codex adversarial review), with all critical and high issues addressed. Earlier drafts are archived for historical reference.

The codex round-1 review found 15 issues, several of which earlier drafts didn't fully address. The current spec incorporates the most important corrections:

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

Every skill answers eleven capability questions before anything else. These are the **blast radius** axes.

### Tri-state values

Every capability field is `true | false | unknown`. **`unknown` means the extractor declined to assert.** A `false` is only emitted when the extractor has positive evidence the skill cannot do the thing (e.g., `allowed-tools` is declared and does not include Bash). When in doubt, the answer is `unknown`. The UI must surface `unknown` as a red flag, not as `false`.

Each value carries a `confidence` tag: `high` (deterministic source like frontmatter), `medium` (specific AST/pattern match), `low` (generic regex hint). Low-confidence claims are badged "tentative — not human-verified" in the UI.

### Phase 1 fidelity contract

Phase 1 extractors are **frontmatter parse + AST/regex over scripts only**. Anything that requires sandboxed execution, type-resolution across SDK calls, or runtime tracing resolves to `unknown` with explanatory evidence. AST/sandbox extraction is deferred to Phase 2.

### Corpus reality (current)

Codex round-2 corpus scan (April 2026): of 1265 SKILL.md files, only 44 declare `allowed-tools`, 32 declare `user-invocable`, 9 declare `disable-model-invocation`. The remaining 1204 declare none of these. This means most skills' capabilities **cannot be extracted from frontmatter alone today** — they require:

1. **Inference from prose** in SKILL.md (low confidence, marked as such)
2. **AST/regex over scripts** (medium confidence at best)
3. **`unknown` everywhere else** — the honest default

We will not pretend coverage exists where it doesn't. Phase 1 ships with measured corpus coverage on the website. If `auto_invocable` is `unknown` for 96% of skills initially, the UI shows "auto_invocable: unknown (96% of corpus)" and the public dashboard tracks the % over time as we improve extractors and as authors add structured frontmatter.

### Provenance per field

Every capability value carries its origin:

```yaml
capabilities:
  can_execute_shell:
    value: true
    confidence: high
    source: declared              # declared | extracted | inferred | unknown
    evidence: "frontmatter allowed-tools: ['Bash']"
```

| Source | Meaning |
|---|---|
| `declared` | Read directly from SKILL.md frontmatter (highest confidence) |
| `extracted` | Found via deterministic AST/regex pattern match in scripts |
| `inferred` | Heuristic match on prose (lowest confidence; UI shows "tentative") |
| `unknown` | Extractor declined to assert |

### The eleven capability questions

| Capability | What it asks | Phase 1 source | Phase 1 default when unclear |
|---|---|---|---|
| `auto_invocable` | Will the agent run this without user prompt? | `user-invocable` / `disable-model-invocation` frontmatter | `unknown` |
| `can_execute_shell` | Does it run arbitrary Bash? | `allowed-tools` listing (high), shell snippet count >0 (medium) | `unknown` |
| `can_install_code` | Does it `npx`, `pip install`, `curl \| sh`, or download CLIs? | shell snippet scan for known managers (high) | `false` (only after full snippet scan, otherwise `unknown`) |
| `can_write_files` | Does it edit user files? | `allowed-tools` includes Edit/Write (high) | `unknown` |
| `can_browse_web` | Does it fetch arbitrary URLs? | `allowed-tools` includes WebFetch / WebSearch (high) | `unknown` |
| `can_spawn_subagents` | Does it call sub-skills or other agents? | `allowed-tools` includes Agent/SubAgent (high) | `unknown` |
| `can_move_funds` | Does it sign or broadcast transactions? | regex hits on `sendTransaction`, signer methods, CEX trade calls (low) | `unknown` |
| `requires_private_key` | Does it ask the user for a key, mnemonic, or wallet config? | regex on docs + scripts (low) | `unknown` |
| `requires_hosted_operator` | Does correct behavior depend on a specific company's running infra? | Phase 1 mini-extractor: regex over text + URL extraction against the curated, **versioned** host list at `scripts/hosted-operator-hosts.yaml` (host → operator name). Each positive carries `source: extracted, confidence: medium` and evidence pointing to the matched host. The host list is a **heuristic**, not a stable fact: it requires periodic maintenance, so `hostlist_version` (date-stamped) is recorded in every attestation. Phase 2 expands using full ingredient list. | `unknown` if no hits |
| `uses_remote_install_script` | Does setup involve running a script downloaded from the internet? | regex for `curl \| sh`, `wget \| sh` (high) | `false` once script scan completes |
| `mutable_remote_runtime` | Does the skill execute remote code (`npx`, hosted CLI, downloaded binary) whose behavior can change without a local diff? | true whenever `can_install_code: true` AND no `runtime_locator` records integrity hash; or whenever a runtime_locator's `integrity == unverified` | `unknown` if `can_install_code` is unknown |

These are **negative-leaning facts**. The UI surfaces them as red flags, not green checks. "This skill can execute shell and install code; mutable_remote_runtime: true" is a useful sentence even when nothing else is known.

The capability manifest is the foundation. Everything else (ingredients, audits, attestations) layers on top.

---

## Skill execution modes (per-mode, not a single enum)

A single `execution_model` enum is **lossy** for real skills. From codex round-2 critical-2: `polymarket` is `read_only` for browsing, `installer_bootstrap` for CLI setup, and `local_executor` once a wallet is configured. Forcing one label per skill either flattens to the scariest mode (lying about safer subpaths) or hides the dangerous mode (lying about the worst case).

We model this as `execution_modes[]` — a list. Each mode carries its own per-mode capability subset.

```yaml
execution_modes:
  - id: browse
    label: read_only
    description: "Default; queries public Polymarket data."
    capabilities_override:
      can_move_funds: false
      requires_private_key: false
  - id: install
    label: installer_bootstrap
    description: "First-run wallet-setup downloads polymarket-cli."
    capabilities_override:
      uses_remote_install_script: true
      mutable_remote_runtime: true
      can_install_code: true
  - id: trade
    label: local_executor
    description: "After wallet setup; signs and broadcasts orders locally."
    capabilities_override:
      can_move_funds: true
      requires_private_key: true
```

The skill-level capability manifest is the **worst-case union** across all modes. The UI surfaces both the union and the per-mode breakdown so a user choosing "read-only" can see the safer subpath.

Mode `label` values:

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

A skill with a single mode (most skills) just has a one-element `execution_modes[]`. The schema scales naturally.

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

If insufficient evidence exists to compute a Stage, `stage` is `null` and the UI renders "Stage: not yet evaluated" with a link explaining what evidence is needed. **`null` is not "Stage 0".** A skill that's missing test coverage data hasn't been measured; we don't pretend it has been.

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
      tier: tier_1               # see Reviewer Trust Tiers below
    date: 2026-03-15
    expires_at: 2027-03-15
    exclusions:
      - "Behavior of remote polymarket-cli once installed"
      - "Backend API correctness"
    report:
      url: https://github.com/.../audit-2026-03-15.pdf
      digest: sha256:abc123...   # report content-addressed; URL drift is detected
    signature: sigstore_keyless_url://...
```

The UI renders "audited components" — never a single global ✓. The report is bound by digest; if the URL serves different bytes later, the bot flags `report_drift: true`.

### Reviewer Trust Tiers

To prevent low-value signed endorsements from diluting the system, every reviewer has a tier. Tier is a function of identity, not stake.

| Tier | Who qualifies | Weight in UI |
|---|---|---|
| `tier_1` | Named professional audit firms listed in `docs/reviewer-tiers.yaml` (Trail of Bits, OpenZeppelin, Spearbit, Code4rena, Sigma Prime, Cyfrin, etc.). Each entry pins a Sigstore OIDC identity. | Shown prominently |
| `tier_2` | CryptoSkill maintainers reviewing as `cryptoskill_team` | Shown as second-class endorsement |
| `tier_3` | Independent researchers added by maintainer PR after manual identity verification, with a pinned Sigstore OIDC identity. **No automatic eligibility.** | Shown with disclaimer |
| `unverified` | Any other signed claim | **Not displayed by default**; visible only via "show all attestations" toggle |

Sock puppet attestations land in `unverified` and don't surface. All tier promotions are manual maintainer decisions via PR against `docs/reviewer-tiers.yaml`. See "Reviewer tier governance" below for issuance / revocation / expiry rules.

### Attestation predicate — pinned

We pin a single attestation predicate now: **`https://cryptoskill.org/attestations/skill-audit/v1`**. This is the in-toto Statement `predicateType` for all audit attestations. The schema is versioned; v1 is the spec above. Verifiers check this predicate type only.

CycloneDX-native attestation fields (CycloneDX 1.7's audit metadata) are emitted as a parallel record for tooling compatibility, but the **canonical** attestation is the in-toto Statement signed via Sigstore keyless.

**Predicate v1 required fields.** Pinning the URL only proves a signer endorsed *some* blob. To bind the attestation to the exact thing audited and the exact extractor that produced it, the predicate body MUST include:

```yaml
predicateType: https://cryptoskill.org/attestations/skill-audit/v1
predicate:
  manifest_digest: sha256:...        # TRUST.auto.yaml + TRUST.md overlay, canonicalized
  bom_digest: sha256:...             # bom.cdx.json at audit time
  report_digest: sha256:...          # the human-readable audit report PDF/MD
  extractor_version: 0.2.0           # version string of extract-capabilities.py
  taxonomy_version: 1                # capability registry / TRUST.md schema version
  hostlist_version: 2026-04-26       # date-stamped curated host list version
  reviewed_at: 2026-03-15T00:00:00Z
  expires_at:  2027-03-15T00:00:00Z  # attestation freshness window; UI badges expired
  reviewer:                          # mirrored from `audits[].reviewer` for self-containment
    name: Trail of Bits
    identity: github:trailofbits
    tier: tier_1
```

Verifiers reject attestations missing any of these fields. Stale attestations (`now > expires_at`) render with a "stale" badge and are excluded from Stage computation. Attestations with `taxonomy_version` lower than the current spec render as "applies to older taxonomy" and require re-signing before they count toward Stage upgrades.

### Reviewer tier governance

Tier assignments live in a public, versioned policy file (`docs/reviewer-tiers.yaml`) signed by the `cryptoskill_team` identity. The policy enumerates:

- **Issuance** — tier_1 firms are added by maintainer PR with public discussion. tier_2 is the maintainer team itself. tier_3 is added by maintainer PR after manual identity verification (see below). `unverified` is the default for any signed claim from an identity not in the policy.
- **Revocation** — any tier can be downgraded by maintainer PR. Revocation invalidates future signatures from that identity at the previous tier; **prior signed attestations remain visible** but render with a "reviewer tier was downgraded after signing" badge.
- **Identity binding** — every tier_1/tier_2/tier_3 entry pins a Sigstore OIDC identity (`certificate-identity` + `certificate-oidc-issuer`). Signatures from any other identity, even with the same display name, fall to `unverified`.
- **Expiry** — tier assignments themselves expire after 24 months and require re-confirmation by maintainer PR. This catches firms that have wound down or been acquired.
- **Tier_3 promotion is manual-only.** There is no automatic OR clause. A reviewer becomes tier_3 only via a maintainer PR after off-line identity verification.

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
  discovery:
    source: static                  # static | runtime_registry | env_var
    ttl_seconds: null               # null = enumerated forever; integer = re-fetch interval if source is dynamic
  routes:
    - target_type: skill            # skill | adapter | service
      target: skills/defi/uniswap-official-swap-integration
      condition:
        kind: equals                # equals | in | always | regex
        field: chain                # chain | input_token | output_token | category
        value: ethereum
    - target_type: skill
      target: skills/defi/jupiter-official-swap
      condition:
        kind: equals
        field: chain
        value: solana
    - target_type: adapter          # an adapter is an in-process plugin, not a sibling skill
      target: openclaw://adapters/uniswap-v3
      condition:
        kind: in
        field: input_token
        value: ["ETH", "USDC", "USDT"]
  unbounded: false  # true if can route to targets not enumerated
```

**`condition` is a structured object, not a DSL.** Allowed `kind` values are `equals`, `in`, `always`, `regex`. Allowed `field` values are `chain`, `input_token`, `output_token`, `category`. Anything more expressive must be expressed as multiple route entries. This makes the evaluator a few lines of code, not a parser.

**`condition.value` type per `kind`** (parsers MUST reject mismatches):

| `kind` | `value` type | Notes |
|---|---|---|
| `equals` | string | Exact match against `field` |
| `in` | array of strings | OR over array; empty array is invalid |
| `always` | (omitted) | The route always matches; `value` MUST be absent |
| `regex` | string | ECMA-262 regex source, no flags. Implementations apply against the string form of `field` with case-sensitive matching, no anchoring (caller must include `^`/`$` if needed) |

**`expansion.discovery.source` enum** — Phase 1 supports only `static`. Phase 2+ values are reserved but parsers SHOULD reject them today:

| `source` | Phase | Semantics |
|---|---|---|
| `static` | 1+ | All routes are enumerated in `expansion.routes`. `ttl_seconds` MUST be `null`. |
| `runtime_registry` | 2+ (reserved) | Routes are fetched from a registry endpoint at evaluation time. Endpoint URL and shape are not yet specified; this enum value is a placeholder. |
| `env_var` | 2+ (reserved) | An environment variable selects among enumerated routes. Variable name and resolution rules are not yet specified. |

Phase 1 parsers MUST treat `runtime_registry` and `env_var` as `unbounded: true` for capability-union purposes, since their semantics are not yet defined.

**`capabilities_override` semantics** (governs the multi-mode example above):

- A `capabilities_override` is a **partial map** of capability fields → tri-state values. Omitted fields inherit from the skill-level capability manifest.
- The skill-level manifest is the **worst-case union** across all modes, computed as: for each capability, if any mode (after override) has `true`, the union is `true`; else if any mode has `false` AND no mode has `unknown`, the union is `false`; else `unknown`. (`unknown` propagates upward; one explicit `false` does not mask another mode's `unknown` or `true`.)
- A mode's `false` override does NOT reduce the skill-level union — it only affects display in that mode's per-mode breakdown.
- Modes MUST NOT override `mutable_remote_runtime` to `false` if any mode has `can_install_code: true`; the parser rejects manifests that violate this (mutable runtime is a property of the skill's worst case, not a per-mode opinion).

### Two-pass extraction

Phase 1 runs in two passes per cycle:
1. **Pass 1** — extract capabilities for all leaf skills (no `expansion.routes`).
2. **Pass 2** — for router skills, compute **union of capabilities** across all enumerated routes. A router that delegates to one custodial executor inherits `can_move_funds: true`, etc.

### `unbounded: true` semantics

If a router can route to skills not enumerated:
- All capability fields → `unknown` (we don't know what it might call)
- `execution_model` → `router_orchestrator`
- UI shows: "⚠ This skill routes to runtime-determined targets. Worst-case capability set assumed; install only if you trust the publisher's full set of possible delegates."

---

## Attestations — Sigstore + in-toto, anchored later in ERC-8004

From codex #14. We use the standard formats directly:

- **Build provenance** — SLSA L2+ provenance signed via Sigstore keyless OIDC
- **Audit attestation** — in-toto Statement with the canonical predicate type `https://cryptoskill.org/attestations/skill-audit/v1` (defined in §"Attestation predicate — pinned" above; this is the only string verifiers should match against). CycloneDX 1.7 audit metadata is emitted as a parallel record for tooling compatibility but is **not** the canonical signed object.
- **Verification** — `cosign verify-attestation --type https://cryptoskill.org/attestations/skill-audit/v1 --certificate-identity ... --certificate-oidc-issuer ...`

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
Stage: not yet evaluated  (insufficient evidence — see what's missing)

⚠ Capabilities
  · Can execute shell
  · Can move funds
  · Custodial execution model
  · Requires hosted operator: Binance

📋 Coverage
  · Source: visible
  · Audits attempted: 0 (no audit yet — distinct from "audited and clean")
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

### Audits — evidence-of-absence vs absence-of-evidence

The UI distinguishes:
- `audits_attempted: 0` — no audit has ever been requested or performed (default state)
- `audits_attempted: N, audits_passed: 0` — audit was performed, found nothing meeting the threshold; render as "audit attempted; no clean record"

These are different signals and the UI must not collapse them.

---

## BOM reconciliation

`bom.cdx.json` is bot-generated, but humans can override component metadata via the `TRUST.md` overlay. On every bot run:

1. Re-extract ingredients from the current source tree.
2. Diff against the published `bom.cdx.json`.
3. If diff non-empty:
   - Set `manifest_stale: true` on the skill's TRUST manifest.
   - Add the diff to a `pending_reconciliation` list in `TRUST.auto.yaml`.
   - **Do not silently overwrite** the published BOM.
   - Mark any audit whose `artifact_digest` no longer matches as `audit_artifact_drift: true` — the audit is preserved but its applicability is in question.
4. A maintainer reviews the diff via PR. Acceptance updates the BOM and clears the stale flag.

This prevents two failure modes:
- The bot silently changing what users think they trust.
- Audits remaining marked "valid" against a moved target.

---

## Phases (revised)

| Phase | Deliverable | Why this order |
|---|---|---|
| **1** | Capability manifest extractor (the 11 negative-leaning facts) + execution_modes classifier + GitHub link viewer + per-capability precision/recall sheet | Establish the foundation — what can each skill do? Honest, conservative, immediately useful. |
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

## Phase 1 verification protocol

Phase 1 is "done" when the extractor's output agrees with hand-review on a stratified sample of 20 skills.

**Sample composition** (stratified by category and execution model):
- 4 from `exchanges` (likely `custodial_executor`)
- 4 from `defi` (likely `local_executor` or `unsigned_tx_builder`)
- 4 from `analytics` (likely `analysis_only` or `read_only`)
- 4 from `mcp-servers` (likely `installer_bootstrap` or `hosted_executor`)
- 4 from `trading` / `wallets` / `payments` / `chains` (mixed)

**Per-skill review form** (filled by human reviewer, blind to extractor output):
- 11 capability fields, each `true | false | unknown`
- `execution_modes[]` and per-mode label from the 9-value enum (graded separately from the capability cells)
- Free-form note for any field where extractor and human disagreed

**Pass/fail criteria for the stratified sample (capability cells):**
- 11 capability fields × 20 skills = **220 capability cells**. `execution_modes[]` and `label` are graded separately and are NOT part of the 220.
- Per-cell agreement rate ≥ 90% (≥ 198 of 220).
- Zero `true` claims by the extractor that the human marks `false`. A single false positive sends Phase 1 back to design.
- False negatives (extractor `unknown`/`false` where human says `true`) acceptable up to 15%. These become Phase 2 fixes.

**Pass/fail for execution mode classification (separate axis):**
- ≥ 90% agreement on the per-mode `label` enum across 20 skills × N modes.
- ≥10% disagreement triggers re-spec of the classifier rules before shipping.

**Capability-aware adjudication (covers the long tail).** The 20-skill stratified sample cannot validate rare-positive capabilities like `auto_invocable` (1/1250 in the latest run), `can_write_files` (4), `can_spawn_subagents` (5), `can_browse_web` (7). These tails are where the model is weakest, so we run a separate pass before declaring Phase 1 done:

1. **Exhaust positives.** For every capability with extractor-positive count ≤ 30 across the corpus, hand-review **all** positive cases. Any false positive → defect logged → extractor patched and re-run.
2. **Sample negatives per capability.** For each of the 11 capabilities, draw a stratified sample of 20 extractor-negative skills (mix `unknown` and `false`) and hand-label them. Compute per-capability **precision** (TP / (TP+FP)) and **recall** (TP / (TP+FN)).
3. **Publish.** Per-capability precision and recall numbers ship with the launch as `docs/phase1-verification/precision-recall.md`, regenerated each time the extractor changes.
4. **Pass bar.** Precision ≥ 0.95 on every capability (a positive claim is almost never wrong); recall is reported but is not gated — `unknown` is the honest fallback.

**Sample stays public.** The 20 reviewed skills' hand-labeled forms and the per-capability precision/recall sheets are checked into `docs/phase1-verification/`. Reviewers sign their forms with Sigstore keyless. This makes the verification protocol auditable.

---

## Next steps

1. Land this v4 doc.
2. Build Phase 1 — capability manifest extractor for all 1256 skills.
3. Run the 20-skill verification protocol above.
4. Phase 2 once verification passes.

The lesson from both reviews: **honest "unknown" beats false green checks**. Ship the conservative version and let the manifest fill in over time.

---

## References

### Internal drafts (archived)
- v1 — `docs/archive/archive-trust-v1.md` (original sketch)
- v2 — `docs/archive/archive-trust-v2.md` (CC engineering review punch list)
- v3 — `docs/archive/archive-trust-v3.md` (synthesized prior art + L2BEAT rosette)
- Codex round-1 review — `docs/TRUST-codex-review.md`

### External standards
- **L2BEAT** — Stage 0/1/2 classification, Risk Rosette framework
- **SLSA** — Supply chain Levels for Software Artifacts (build provenance)
- **CycloneDX 1.7** — SBOM with native attestation support
- **in-toto** — Attestation framework (Statement + predicate types)
- **Sigstore** — Cosign keyless signing, Fulcio CA, Rekor transparency log
- **EIP / ERC-8004** — Trustless agent identity registries
- **OWASP** — Agentic Skills Top 10
- **Ink & Switch** — Local-first software (concept origin)

### Skill scanners surveyed
- GoPlus AgentGuard, Snyk Agent Scan / ToxicSkills, Oathe ClawMutiny, STSS, Cisco AI Defense skill-scanner, DeFiSafety PQR

### Failure modes studied
- Mike Goldin TCR 1.0 (and AdChain post-mortem, Tabarrok critique)
- Optimism Cannon FPVM (bisection-based dispute resolution)
- EigenLayer slashing + veto committee pattern
- Forta detection-bot marketplace
