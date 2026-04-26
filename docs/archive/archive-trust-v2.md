# Trust Manifest v2 — incorporating eng review

This is a revision of `TRUST.md` after a senior engineering review. Items marked **[FROM CC]** are direct fixes from that review. Items marked **[NEW]** are additions on reflection.

The original v1 design lives at `docs/TRUST.md` and remains the public statement of intent. v2 is the implementation spec.

---

## Changes from v1

### Decision rule changes

1. **`trustless` becomes a tier, not a binary** [FROM CC P0-2]. Three stages:
   - **Stage 0** — trusted operator holds custody, signing, or critical state
   - **Stage 1** — self-custody but with multisig/council backstops, or upgradeable contracts with exit windows
   - **Stage 2** — self-custody, immutable contracts, user-supplied or decentralized RPC, no operator dependency
   Rationale: v1 binary collapsed self-custody Uniswap-via-Alchemy into the same bucket as a CEX skill.

2. **Split `trustless` for non-fund-moving skills** [FROM CC P0-1]. Two parallel dimensions:
   - **`custody_trustless`** — applies when funds are at stake (`tier 0/1/2/n_a`)
   - **`data_trustless`** — applies to any skill that returns data the user/agent acts on (`tier 0/1/2`). A Dune query is `data_trustless: 0` (Dune can lie) even though it has no custody.
   Most skills will have one of the two; some (a CEX skill) have both.

3. **Drop `kind: self`** [FROM CC P1-2]. Self-claims are not attestations. The author's view goes in `reason:` fields. Attestor list only contains parties distinct from the skill author.

4. **Drop `kind: community` until Phase 6** [FROM CC P1-3]. Pre-staking, sock-puppet attestations are unstoppable. Community attestation only enables when ETH is on the line.

### Schema changes

5. **Split file: `TRUST.auto.yaml` + `TRUST.md` overlay** [FROM CC P1-1]. The bot owns `.auto.yaml` and rewrites it freely. Humans own the YAML frontmatter in `TRUST.md`. Final view = overlay merged on top. No more thrash.

6. **`hardcoded`, `user_overridable`, `default` are auto-only** [FROM CC P2-5]. Explicitly marked `_machine_only: true`. Cannot appear in human overlay.

7. **New ingredient kinds** [FROM CC P3-1]:
   - `webhook_consumer` — outbound POST to user-defined endpoint (privacy)
   - `llm_endpoint` — calls to OpenAI/Anthropic/Together (operator sees prompts; for crypto skills this leaks wallet activity)
   - `key_storage` — where private keys live (env var / OS keychain / hardware wallet / MPC)

8. **New trust labels** [FROM CC P3-2]:
   - `immutable_contract` — distinct from `decentralized` (immutable+broken is still broken)
   - `social_consensus` — bridges relying on watcher quorum (Wormhole-class)

### Implementation changes

9. **L2BEAT/DefiLlama as authoritative sources, not hand-curated JSON** [FROM CC P0-4]. Bot pulls from:
   - L2BEAT public API → bridge stages, council sizes, exit windows
   - DefiLlama → protocol admin keys, multisig thresholds, TVL
   - Etherscan / Sourcify → contract verification, admin slot reads
   - Hand-curated overlay only for things outside those feeds (CEX APIs, project-run SaaS) — target ~50 entries, not 500.
   Per-label provenance: `source: l2beat`, `fetched_at: ...`. Anything older than 30d auto-downgrades to `unknown`.

10. **AST-based extraction, not regex** [FROM CC P0-3]. For Python and JS, walk the AST and recognize known SDK constructors (`AlchemyProvider`, `InfuraProvider`, `ethers.getDefaultProvider`, `Web3.HTTPProvider`, `binance.Client`, etc.). Map them to their default endpoints. Plus parse `package.json`/`requirements.txt` and intersect with a known-default-endpoint table. Regex remains as fallback. Document `unknown` as the honest output for code that resists analysis.

11. **Phase reorder** [FROM CC P1-4]:
   - **Phase 1** — schema, AST extractor, **file viewer in UI** (was Phase 4)
   - **Phase 2** — ingredient table, badges, **`/api/trust/{skill_id}`** (was out-of-band)
   - **Phase 3** — manual attribution flow
   - **Phase 4** — trust filter on registry
   - **Phase 5** — TCR / staked attestation, scoped to top 50 skills only

12. **Migration plan: bot generates TRUST.auto.yaml for all 1256 skills in one batch** [FROM CC P1-5]. Stubs for skills the extractor cannot analyze. UI treats absent files as "not yet analyzed" but ships with full coverage.

13. **Failure-mode templates per ingredient kind** [FROM CC P2-6]. Auto-generated default text labeled `auto_generated: true`. Reviewers override.

14. **Per-dimension challenge windows** [FROM CC P2-2]:
   - `local_first`, `data_trustless`, `custody_trustless` — 48 hours (deterministic re-scan resolves)
   - `audited` — 60 days (challenge requires real review work)

15. **Label-change protocol** [FROM CC P2-3]: when `trust-labels` upstream change, regenerate affected dimensions but do *not* slash existing attestations (claim was correct at the time). Old attestations get `superseded_at`. UI shows current state with diff history.

### UI changes

16. **Group badges visually** [FROM CC P2-4]:
   - Row 1 — *Code metrics*: Quality grade, Risk Gate
   - Row 2 — *Trust manifest*: Audited, Local-first, Custody, Data
   Copy explicitly states they're orthogonal.

17. **File viewer is Phase 1** [FROM CC P1-4]. Render SKILL.md inline with `marked`, file tree from existing repo structure, raw-source link to GitHub. No iframe.

### Scoping changes

18. **TCR scoped to top 50 skills only** [FROM CC P2-1]. The economic mechanism only works where someone cares enough to challenge. Long-tail skills get author/reviewer signature attestations (no stake, no slashing).

19. **Library kind explicitly out of scope** [FROM CC P1-6]. Transitive deps belong to the existing security scanner, not TRUST.md. Remove `library` from ingredient kinds in v2; revisit with proper SBOM (CycloneDX) in a future doc.

---

## Open questions surfaced by review

1. **Audit scope ambiguity** [FROM CC top-of-doc]. "Trail of Bits audited the SKILL.md" vs "Trail of Bits audited the protocol the skill calls" are very different claims. v2 schema must distinguish: `audit_target` field with values `skill_text` | `skill_scripts` | `target_protocol` | `infrastructure`.

2. **Missing-manifest policy**. Unanswered: what happens when a skill author refuses to add TRUST.md? Default: bot generates a stub; UI shows "no manifest" badge but doesn't hide the skill. Decision needed before Phase 1 ships.

3. **Hard dependency on L2BEAT API**. Cleanest fix for staleness but introduces a runtime dependency. Mitigation: cache L2BEAT responses, fall back to last-known-good for 7d if API is down, then `unknown`.

4. **Quality vs Trust display**. Need design pass on the skill page header layout. Currently 5 badges; should be 2 grouped rows.

---

## Schema v2 (illustrative)

```yaml
# TRUST.auto.yaml — bot owns this
schema_version: 2
generated_at: 2026-04-26T00:00:00Z
generated_by: cryptoskill-bot/2.0
extractor_version: "ast-py-1.0,ast-js-1.0"

dimensions:
  audited:
    status: no  # auto-default; humans override in TRUST.md
    audit_target: null

  local_first:
    status: no
    reason_auto: "Uses default Binance API endpoint, no override path detected"

  custody_trustless:
    tier: 0
    n_a: false
    reason_auto: "Funds custodied on Binance CEX"

  data_trustless:
    tier: 0
    reason_auto: "Market data from api.binance.com — single operator can return arbitrary values"

ingredients:
  - kind: api_endpoint
    host: api.binance.com
    purpose_auto: "Spot trading, order placement, market data"
    trust_label: trusted_operator
    operator: Binance
    label_source: hand-curated
    label_fetched_at: 2026-04-01T00:00:00Z
    _machine_only:
      hardcoded: true
      user_overridable: false
    failure_mode_auto: "If api.binance.com is unreachable, all order operations fail. There is no automatic fallback."
```

```markdown
---
# TRUST.md — human overlay
schema_version: 2

dimensions:
  audited:
    status: yes
    audit_target: skill_scripts
    attestors:
      - kind: third_party
        name: Trail of Bits
        url: https://github.com/trailofbits/audits/binance-spot-api-2026.pdf
        date: 2026-03-15
        scope: full

ingredients:
  - host: api.binance.com
    failure_mode: |
      Custom override: in addition to the auto-generated text, our integration
      test suite verifies that signed orders are rejected if the response
      domain mismatches.
---

# Author notes follow.
```

---

## What did NOT change

- Three-dimension model itself remains (audited / local-first / trustless-tier). CC validated the directional design.
- Auto-extraction-first approach remains. Manual editing is overlay only.
- ERC-8004 anchor for Phase 5 stake remains.
- `unknown` as honest default remains.

---

## Next step

Once codex review and the trust-prior-art research land, merge their findings into v3. Until then, v2 is the spec we'd implement.
