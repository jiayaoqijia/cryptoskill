# Agent cron that writes an artifact for another process to consume

Some jobs should not "report" at all — they should **produce a file that a dashboard/script reads**.
Pattern proven with the per-token reasoning layer: a daily 07:45 agent job researches each holding and
writes `~/.hermes/data/token_thesis_ai.json`; `porto_risk.py` then merges it into the dashboard payload.

## Prompt shape that works

1. **Name the input file and the exact fields to read** (`~/.hermes/data/porto_risk.json` → `assets[]`;
   list the fields by name). The job must ground on data the fleet already computed, not re-derive it.
2. **Bound the research**: "web_search 1–2 kueri per entity, open 2–4 articles with web_extract, keep
   only catalysts — regulation, partnership, product, listing, unlock, buyback, upgrade, ETF, hack";
   explicitly list what to discard (price predictions, target prices, shill/SEO filler).
3. **Forbid invention in words the model obeys**: *"kalau gak nemu katalis material, tulis apa adanya
   'gak ada katalis material pekan ini' — JANGAN mengarang berita, angka, atau tanggal"*. Same for
   links: `"src": only links you actually opened`, empty array allowed. Ungrounded links are the
   fastest way an artifact cron turns into a fabrication machine.
4. **Spec the JSON contract verbatim** (keys, nesting, and a **document-level `ts`** taken from
   `date +%s%3N`) — the consumer uses that `ts` for freshness expiry. Per-entry timestamps are optional;
   the consumer must fall back to the document `ts` (`entry.get("ts") or doc.get("ts")`), because an
   author will forget them.
5. **Make the job rebuild the consumer**: last step `python3 <consumer>.py --save`, plus a self-check
   one-liner that prints the entry count (`python3 -c "import json;print(len(json.load(open(...))['by_token']))"`).
6. **Cap the reply**: *"BALAS KE USER: MAKSIMAL 2 BARIS"* — 1 line confirming the refresh, 1 line with
   the single most important finding. Artifact jobs are daily; an essay every morning is spam (see
   `cron-output-style` / the delta-only rule).
7. `enabled_toolsets: [web, file, terminal]` is enough — no messaging tools, no delegation.

## Hygiene

- Write to a **fixed path** and overwrite; the consumer expires stale content by `ts` (48 h is a good
  default for daily jobs), so a dead job degrades to the deterministic layer instead of showing stale
  claims as if fresh.
- Label the artifact on the surface that shows it (`dianalisis AI · <waktu> · sumber: …`) — the user
  must be able to tell machine-written narrative from computed facts.
- Test-run once immediately after creating the job (`cronjob action=run`) to prove the whole chain
  (file written → consumer rebuild → page updated). Deliver the real artifact, not a promise.
