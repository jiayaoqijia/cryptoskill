# Trust Manifest v3 — final design

This is the implementation spec, synthesizing:
- v1 (`docs/TRUST.md`) — the original design
- v2 (`docs/TRUST-v2.md`) — incorporating CC engineering review
- Prior-art research (TCRs, ERC-8004, L2BEAT, SLSA, CycloneDX, Sigstore, GoPlus AgentGuard, Snyk, Oathe, EigenLayer, Optimism fault proofs)

v3 supersedes v1 and v2.

---

## Executive summary

A skill ships with three artifacts:

```
skills/{category}/{name}/
├── SKILL.md            # the skill itself (existing)
├── SOURCE.md           # provenance (existing)
├── TRUST.auto.yaml     # bot-owned, regenerated from analysis
└── TRUST.md            # human-curated overlay (frontmatter YAML + free-form notes)
```

The **trust manifest** is the merged view of `.auto.yaml` and the YAML frontmatter of `TRUST.md`. It contains:

1. **Trust ladder** — a single Stage 0 / 1 / 2 classification (borrowed from L2BEAT)
2. **Risk rosette** — 6 independent dimensions, each scored 0-3 (borrowed from L2BEAT + DeFiSafety)
3. **Ingredient list** — every external dependency the skill calls (CycloneDX-style SBOM)
4. **Attestations** — signed claims about specific dimensions (SLSA + in-toto + Sigstore)
5. **On-chain anchor** — ERC-8004 Identity ID for the skill, optional Reputation feedback, optional Validation requests

No registry token. Stake is in ETH or USDC. Slashing is gated by a Kleros-style arbitration committee, not pure token-weighted voting. We are not building a TCR; we are building a layered attestation system that uses the same primitives selectively.

---

## 1. Trust ladder (single tier per skill)

Borrowed verbatim from L2BEAT, adapted to skills:

| Stage | Criteria | Example |
|---|---|---|
| **Stage 0** — Disclose | Source visible, ingredient list complete, classification of each ingredient. User must trust the publisher and every operator in the ingredient list. | Most skills today |
| **Stage 1** — Signed + committee | Stage 0 + signed manifest (Sigstore keyless or PGP) + automated scan suite passes (Snyk, GoPlus, our scanner) + named security council (≥3 members, ≥50% outsiders) can pause/delist. 7-day exit window for sensitive upgrades (e.g., changing the default RPC endpoint). | A skill maintained by a known org with visible signing identity |
| **Stage 2** — Reproducible + slashable | Stage 1 + reproducible build (SLSA L3) + deterministic execution sandbox + ERC-8004 attestation backed by ≥1 ETH stake + 30-day exit window. | Aspirational; very few skills will reach this initially |

The single tier is the headline metric on each skill page. It's defined precisely so disagreement is rare.

---

## 2. Risk rosette (6 independent dimensions)

Each dimension is scored 0-3, independent of the others. Never collapsed into a single number. Inspired by L2BEAT's risk rosette and DeFiSafety's PQR.

| Dimension | What it measures | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| **Source provenance** | How traceable is the code? | unverified | repo public, git log preserved | + signed commits | + Sigstore attestation tying CI build to source SHA |
| **Documentation** | Can a reader determine intent and surface area? | none | SKILL.md exists | + traceability between docs and code | + per-call docs for every external endpoint |
| **Test coverage** | How well exercised is the skill? | none | smoke test | + integration tests against real APIs | + deterministic golden outputs + adversarial test suite |
| **Audit history** | Has someone independent reviewed this? | self only | community review with PR receipts | named third-party report covering scripts | + ongoing bounty + multiple firms |
| **Permission scope** | What can the skill do at runtime? | all tools, no caps | scoped tools listed | + per-tool justification | + capability tokens (e.g. read-only RPC) enforced at runtime |
| **Network egress** | Where does data leak? | unknown | declared egress list, all hardcoded | declared list, all `user_specified` or `decentralized` | declared list + signed network log proves runtime matches manifest |

**Why 6 axes and not 3 or 10**: 3 was too lossy (CC P0-2). 10 is over-engineered for what authors will actually fill in. 6 maps cleanly to L2BEAT's rosette + the supply-chain literature.

The 0-3 scale lets us replace the binary `audited / local-first / trustless` from v1/v2, which collapsed too much. Each axis carries its own meaning.

The single Stage (0/1/2) is computed from the rosette: Stage 1 requires every axis ≥ 1 plus signed manifest. Stage 2 requires every axis ≥ 2 plus reproducible build plus on-chain stake.

---

## 3. Ingredient list — CycloneDX-flavored SBOM

We adopt CycloneDX 1.7 as the schema baseline (it has native attestation support and is OWASP-maintained). Each `ingredient` is a CycloneDX `component` with extended fields:

```yaml
ingredients:
  - bom_ref: api.binance.com  # CycloneDX bom-ref
    type: service               # CycloneDX component type
    purpose_auto: "Spot trading, order placement, market data"
    trust_label: trusted_operator
    operator: Binance
    label_source: hand_curated
    label_fetched_at: 2026-04-01T00:00:00Z
    failure_mode_auto: "If api.binance.com is unreachable..."
    _machine_only:
      hardcoded: true
      user_overridable: false
```

### Ingredient kinds (CycloneDX-aligned)

| Kind | CycloneDX `type` | Notes |
|---|---|---|
| api_endpoint | service | HTTP API |
| smart_contract | application | On-chain contract; bom_ref = `eip155:{chainId}:{address}` |
| rpc_provider | service | JSON-RPC node |
| bridge | service | Cross-chain bridge with stage classification |
| oracle | service | Chainlink, Pyth, etc. |
| relayer | service | Off-chain message routers (Axelar, LayerZero) |
| signer | application | External signers (custodial wallet, MPC) |
| data_source | service | Indexers, analytics APIs (Dune, The Graph) |
| webhook_consumer | service | User-defined webhook (privacy implication) |
| llm_endpoint | service | OpenAI / Anthropic / Together — operator sees prompts |
| key_storage | application | env var / OS keychain / hardware wallet / MPC service |
| library | library | npm/pip — but **scoped out of TRUST.md** (see CC P1-6); covered separately by an SBOM in `bom.cdx.json` if/when we generate one |

### Trust labels

| Label | Meaning |
|---|---|
| `decentralized` | No single party can censor or steal (Ethereum L1, IPFS multi-pin) |
| `immutable_contract` | Contract code cannot change; behavior is fully fixed |
| `user_specified` | User must provide their own endpoint |
| `decentralized_with_council` | Mostly decentralized, emergency council exists (most stage-1 L2s) |
| `social_consensus` | Bridges relying on watcher quorum (Wormhole-class) |
| `multisig_controlled` | Small group can change behavior |
| `trusted_operator` | Single party can change/halt |
| `unknown` | Could not classify; pending review |

### Authoritative label sources (CC P0-4)

The bot pulls labels at build time from:
- **L2BEAT API** — bridge stages, council sizes, exit windows
- **DefiLlama** — protocol admin keys, multisig thresholds
- **Etherscan / Sourcify** — contract verification, admin slot reads
- **Hand-curated overlay** — ~50 entries for things outside those feeds (CEX APIs, project-run SaaS)

Per-label provenance: `label_source: l2beat`, `label_fetched_at: ...`. Anything older than 30d auto-downgrades to `unknown`.

---

## 4. Attestations (SLSA + Sigstore + in-toto)

### Attestation kinds

| Kind | Identity binding | Trust level |
|---|---|---|
| `cryptoskill_team` | GitHub OIDC bound to the cryptoskill org | medium |
| `third_party` | Sigstore keyless signature with verifiable OIDC identity | high |
| `community` | **Disabled until Phase 5** (sock-puppet attack — CC P1-3) |
| `onchain_attestation` | ERC-8004 Identity + ETH/USDC stake | high (slashable) |

`kind: self` is removed entirely. Author claims live in `reason:` fields, not in the `attestors:` list.

### Attestation envelope (in-toto Statement)

For the high-trust kinds, attestations are signed in-toto Statements with predicates:

- `slsa-provenance/v1` for "this skill was built from this source"
- `cyclonedx/bom/1.7` for the ingredient list
- `cryptoskill/skill-trust/v1` for our custom dimension scores

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{"name": "skills/exchanges/binance-spot-api", "digest": {"sha256": "..."}}],
  "predicateType": "https://cryptoskill.org/skill-trust/v1",
  "predicate": {
    "rosette": {"source_provenance": 3, "documentation": 2, ...},
    "stage": 1,
    "ingredients_bom_ref": "...",
    "auditor": {"name": "Trail of Bits", "report_url": "..."}
  }
}
```

Signed via `cosign` with keyless OIDC. Verification uses `--certificate-identity` + `--certificate-oidc-issuer`.

### What gets stored where

| Layer | Storage | Why |
|---|---|---|
| Bot-extracted manifest | `TRUST.auto.yaml` in repo | Free, fast, queryable |
| Human overlay | `TRUST.md` frontmatter in repo | Free, PR-reviewable |
| Third-party attestation | Sigstore + Rekor transparency log | Public auditability, no gatekeeper |
| Ingredient SBOM | `bom.cdx.json` in repo (Phase 2) | Standard format, tool ecosystem |
| On-chain attestation (Phase 5) | ERC-8004 Reputation + Validation | Slashable, censorship-resistant |

---

## 5. On-chain layer — ERC-8004 mapping

When Phase 5 lands:

| ERC-8004 component | Our use |
|---|---|
| **Identity Registry** | Each skill registers as an Agent. Skill metadata includes `cryptoskill:trust-manifest:sha256:...` pointing at the signed manifest |
| **Reputation Registry** | Per-dimension feedback. Tag1 = dimension name (e.g. `audit_history`), Tag2 = attestor kind. Value = rosette score 0-3 |
| **Validation Registry** | Used for slashable claims. A challenge becomes a `validationRequest` against the skill's Identity. Response 0-100 = "claim is correct" |

Slashing economics borrowed from EigenLayer:
- Stake denominated in **ETH or USDC** (not a CryptoSkill token — CC P2-1, prior-art lesson #1)
- ≥1 ETH minimum stake per attestation
- Per-dimension stake (compromised on `audit_history` doesn't slash all reputation — EigenLayer attributability lesson)
- **Veto committee can reverse unjust slashes** (EigenLayer + Kleros pattern). Committee = 5-of-9 multisig of CryptoSkill maintainers + outside observers, named publicly.

Disputes use **bisection-style narrowing** (Optimism Cannon pattern):
1. Challenger identifies the specific ingredient, dimension, or claim in dispute
2. Both parties agree the dispute is reproducible from the SKILL.md + ingredient list
3. A deterministic check is run (re-extract URLs, re-verify Sigstore signature, re-fetch L2BEAT label)
4. If deterministic, ground truth is automatic. If not, escalates to Kleros-style jury.

This avoids the "all token holders vote on every claim" failure mode (Goldin TCR 1.0 → AdChain).

---

## 6. UI

Per-skill page (CC P1-4 — file viewer first):

```
┌───────────────────────────────────────────────┐
│ Binance Spot API                              │
│ Stage 0 — Disclosed                           │
│                                               │
│ ROSETTE                                       │
│   Source provenance ████░    2/3              │
│   Documentation     ██████   3/3              │
│   Test coverage     ░░░░░    0/3              │
│   Audit history     ░░░░░    0/3              │
│   Permission scope  ████░    2/3              │
│   Network egress    ██░░░    1/3              │
│                                               │
│ INGREDIENTS (5)                               │
│   ▸ api.binance.com   trusted_operator        │
│   ▸ ...                                       │
│                                               │
│ ATTESTATIONS                                   │
│   none yet                                    │
│                                               │
│ FILES                                         │
│   [SKILL.md] [tree] [GitHub raw]              │
└───────────────────────────────────────────────┘
```

Quality grade and Risk Gate (existing scoring) remain on a separate row, clearly labeled as orthogonal (CC P2-4).

### File viewer

Inline `marked` rendering of SKILL.md. File tree from existing repo structure. Raw-source link to GitHub. No iframe, fast paint.

### Trust filter

On the main registry: filter pills for `Stage ≥ 1`, `Audit ≥ 1`, `Network egress ≥ 2`. Combinable with category.

### Skill API

`/api/trust/{skill_id}` returns the merged manifest as JSON. Documented for AI agent operators who want to refuse-install on threshold (CC P3-5 promoted to Phase 2).

---

## 7. Implementation phases (final order)

| Phase | Deliverable | Why this order |
|---|---|---|
| **1** | Schema + AST extractor + file viewer in UI + L2BEAT/DefiLlama label fetcher + 6h bot generates `TRUST.auto.yaml` for all 1256 skills | File viewer first builds trust narrative; rest of phases hang off the manifest |
| **2** | Rosette + Stage badges + ingredient table + `/api/trust/{id}` | Surface the manifest |
| **3** | Manual attribution flow (PR-based for `cryptoskill_team` and `third_party` attestations); Sigstore signing pipeline for our own attestations | Get the medium/high-trust attestations actually flowing |
| **4** | Trust filter + per-dimension challenge windows + label-change protocol | Make trust queryable |
| **5** | ERC-8004 Identity registration for top 50 skills + staked attestations + Kleros-style arbitration committee + bisection dispute resolution | Skin in the game; only ships when manual flow has produced ≥50 attestations |

Note: phases 1-4 ship without any on-chain dependency. Phase 5 only happens once we have organic demand — measured by ≥50 manual attestations and ≥1 third-party paid audit.

---

## 8. Defenses against past failure modes

| Failure mode | Source | Our defense |
|---|---|---|
| Free-rider / tragedy of commons | TCR 1.0, AdChain | We pay attestors from a registry fee (Phase 5+); pre-Phase 5, attestation has reputational value only |
| Bribery attacks on token holders | TCR literature | No token. Stake is ETH/USDC. Bribery requires direct private key compromise of a named auditor |
| Whale dominance, 1-token-1-vote | TCR 1.0 | Per-dimension stake (no aggregate weight). Kleros jury for subjective disputes |
| Bootstrapping (no traffic until curation, no curation until traffic) | TCR 1.0 | Phases 1-4 ship without staking; manifest exists for all skills day one regardless of demand |
| Sybil attack on `community` attestor kind | CC P1-3 | Community kind disabled until Phase 5 (then sock puppets cost ETH) |
| Self-attestation laundering | CC P1-2 | `kind: self` removed from schema entirely |
| Hand-curated label rot | CC P0-4 | L2BEAT/DefiLlama as source of truth; 30-day staleness auto-downgrades |
| Regex misclassification | CC P0-3 | AST-based extractor; regex fallback only |
| Bot vs human edit conflict | CC P1-1 | Split files: `.auto.yaml` (bot) + `.md` overlay (human); merge view |
| Single-score collapse | CC P0-2, L2BEAT lesson | 6-axis rosette never collapsed; single Stage is computed but transparent |
| TCR death spiral | All TCR post-mortems | Not a TCR. No new token. Stake only on Phase 5, only for top 50 skills |
| Audit scope ambiguity | CC top-of-doc | `audit_target: skill_text \| skill_scripts \| target_protocol \| infrastructure` |
| Library/transitive supply chain hidden | CC P1-6 | Out of scope for TRUST.md; will be a separate `bom.cdx.json` if/when we ship that |

---

## 9. Open questions for v3

1. **What's in the SBOM `bom.cdx.json`** — do we generate it pre-publish, or is it the publisher's responsibility? Phase 2 question.
2. **Reproducible build for skill scripts** — most skills are SKILL.md + a few scripts. SLSA L3 is overkill; L2 (signed by hosted CI) is achievable. Decision needed.
3. **Who runs the Kleros-style arbitration jury** in Phase 5? Reuse Kleros mainnet? Custom implementation? Decide before Phase 5 design.
4. **Stake size for Phase 5** — 1 ETH minimum is arbitrary. Empirical decision after watching Phase 1-4 traffic.
5. **Missing-manifest UI policy** — show as "not analyzed" badge or hide entirely? Recommend show with badge so unscanned skills are visible.

---

## 10. What this is not

- Not a TCR. We use stake + slashing primitives for high-stakes attestations only.
- Not a replacement for the existing scoring (Quality + Risk Gate). Trust manifest is orthogonal.
- Not a proof of correctness. A Stage 2 skill can still be buggy. We surface what's verifiable.
- Not a single number. Six axes + one stage. Users see all of them.

---

## References

Prior art consulted (full list in research output):

- **TCRs** — Mike Goldin (2017), AdChain post-mortems, Kleros T2CR, Tabarrok critique
- **ERC-8004** — EIP, ChaosChain reference impl, Phala TEE extension
- **L2BEAT** — Stage classifications, Risk Rosette framework
- **SBOM** — CycloneDX 1.7, SPDX 3.0, in-toto attestation framework
- **SLSA** — Build levels v1.0
- **Sigstore** — Cosign keyless signing, Fulcio, Rekor
- **Local-first** — Ink & Switch 2019 essay
- **Skill scanners** — GoPlus AgentGuard, Snyk Agent Scan / ToxicSkills, Oathe ClawMutiny, STSS
- **DeFi trust** — DeFiSafety PQR, Code4rena severity rubric
- **Slashing** — EigenLayer AVS, Optimism Cannon FPVM
- **Monitoring** — Forta detection bots, OpenZeppelin Defender Monitor
