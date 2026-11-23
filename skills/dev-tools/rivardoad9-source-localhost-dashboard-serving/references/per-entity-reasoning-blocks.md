# Per-entity "cara mikir" blocks (reasoning, not just numbers)

The ask, verbatim: *"nah gw pengen thought process kayak gini masuk ke zemizrisk tiap token"* — i.e. the
dashboard's per-entity card must show the **chain of reasoning** the agent just used in chat
(driver → evidence for → evidence against → what to watch → verdict), not only metrics and bullets.

## Two-layer architecture (do this, not one prompt-in-a-template)

| Layer | Producer | Content | Cost / risk |
|---|---|---|---|
| **Facts** | `token_thesis.py` (`compose(a, macro)`) — pure Python, no LLM | driver (theme perf + top verified catalyst), support, against, watch triggers, stance, confidence — every sentence assembled from fields already in the data file | free, deterministic, cannot hallucinate |
| **Narrative** | agent **cron job** (07:45 daily) → `token_thesis_ai.json` | 3–5 sentences of real "why it's moving": researched catalysts, honest "no catalyst this week", 1–3 source links actually opened | tokens; must be freshness-bounded |

Merge rule that makes it safe: the enrichment file is keyed by entity symbol and carries a
document-level `ts`; the deterministic layer copies `ai` onto the entity **only while fresh**
(48 h), so a dead/forgotten cron degrades gracefully to rule-based text instead of showing stale
claims. Render the AI text above the rule-based block, labelled (`dianalisis AI · <waktu> · sumber: …`)
so the reader always knows which layer wrote what.

### Shape of the deterministic composer

```python
def compose(a, macro=None):   # a = one entity dict already built by the report script
    driver  = [theme + narr r7/alpha/breadth/volratio, "katalis terakhir: …", regime tailwind/headwind]
    support = potensi[] (minus lines you re-write nicer) + sentiment + on-chain flow
    against = negatif[] + alpha<0 + range_pos high + euphoric sentiment + flags + unlock
    watch   = MA50 level, alpha must turn >0, sentiment floor, DEX buy-ratio floor,
              whale long% floor, "trim before <unlock date>", "no new catalyst = fuel out"
    stance  = existing action field;  conf = count of present data sources → tinggi/sedang/rendah
```

Design rules that made it read like an analyst instead of a template:
- **Confidence is computed, not asserted**: count how many independent sources are present
  (narrative perf, verified news, sentiment, on-chain flow, whale, unlock) → tinggi ≥7, sedang ≥4.
- **Every watch line is checkable**: a price level (MA50), a percentage threshold, or a date.
  "Pantau perkembangan" is not a watch line.
- **Reuse the risk engine's own numbers** (alpha vs BTC, allocation %, unlock days) so the reasoning
  block and the metrics block can never contradict each other.
- **Dedupe deliberately**: the `potensi[]`/`negatif[]` lists already carry some sentences you rewrite
  more precisely (sentiment, DEX flow) — filter them out with a regex when picking, or the same fact
  appears twice in one card.
- Feed the block into the **push card** too (`🧠 <driver>` + `👁 <watch>`), so an alert carries the
  reasoning, not just the delta.

## Pitfalls hit while wiring this up

- **Unit scale silently multiplies**: a `range_pos` field that is already *percent* (80.1) rendered as
  `8010% rentang 30 hari` after `*100`. Before formatting `x*100`, print the real field from the data
  file once and confirm the scale (fraction 0–1 vs percent 0–100).
- **Merge returned 0 and looked like a render bug**: the per-entity enrichment entries carried
  `text`/`src`/`watch` but the timestamp only existed at the document root. Fix: read
  `ts = entry.get("ts") or doc.get("ts")` (same for `asof`). When a merge silently does nothing,
  test the merge function *directly* in a REPL against a hand-written fixture before touching the page.
- **Do not let a failed composer blank the section** — wrap the attach in `try/except` and fall back to
  a minimal dict so the card still renders (a visible "modul gagal" beats a missing block).
- Markdown-ish `**bold**` inside the strings must be converted at render time
  (`const BD = s => esc(MS(s)).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>')` — order matters: mask money
  *and* escape HTML, then inject the tags), otherwise the card is litered with asterisks.

## Verify

1. `node --check` on the extracted inline `<script>` (cheap gate, always first).
2. Re-run the data producer, then assert in the JSON that every entity has `thesis` (and `thesis.ai`
   when the enrichment file is fresh).
3. Playwright: count the new card selector (`.th` == number of entities), assert the three group
   headings exist, assert `.nfull` `is_visible()` is **False** before the click and **True** after,
   assert the verdict line text, and collect `pageerror` (expect zero).
4. `vision_analyze` the collapsed + expanded screenshots and read them; ship both to the user.
5. Bump the service-worker `CACHE` string (`zemizrisk-v3` → `-v4`) on **every** page change, or the
   installed PWA keeps serving the old HTML and the user reports "gak ada yang berubah".
