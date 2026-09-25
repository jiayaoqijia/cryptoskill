# 06 Related Work

Full procedure: [related-work-writing](../../related-work-writing/SKILL.md).

## Organise by axis, not by time

Place all prior work on one or two **axes** (e.g. "reduce the degree" vs "reduce the
evaluation cost"; "reduce rounds" vs "reduce bandwidth"). A comparison table places
each work at a coordinate; the "Ours" row occupies the region no one else does. The
section itself then argues "prior work sits on the boundary, we are in the interior".

## Structure (≈ 2 LNCS pages)

```
[lead-in, 3 sentences]  We overview prior optimisations for <task>, focusing on
                        <bottleneck>. Accelerating (1) follows two paths: <axis 1> and
                        <axis 2>. Table 1 summarises the asymptotic comparison.
[Table 1]               columns: Technique | Method | <cost measure 1> | <cost 2> | <coordinate>
                        rows grouped by technique; last row \textbf{Ours}; caption defines
                        every symbol; † ‡ footnotes mark scope restrictions.
[¶ axis 1, classic]     one sentence per work: authors + what + cost; last sentence states
                        what all of them still share ("... at a cost that still grows
                        with <parameter>").
[¶ recent, both axes]   "Recently, two independent lines of work exploit <structure>
                        rather than <old measure>:" then two bullets, each built on a pair
                        of contrasting verbs (e.g. "restricts *where* ..." vs "restricts
                        *how* ...").
[¶ bridge]              \textbf{Insight from <structure>.} Why the two lines are compatible
                        (one algebraic/structural reason), where each prior work sits in
                        our framework, back-reference to Table 1.
[¶ Our work]            five sentences: framework + three technical points joined by
                        colons/commas + one results sentence. This is the elevator pitch.
[¶ orthogonal]          "Complementary approaches" (alternative pipelines, other schemes)
                        in 2–3 sentences, labelled as complementary.
```

## Rules

- Judge prior work only by **factual limitations**: "they instantiate a single
  case, leaving open ...", "the required correction is assumed rather than shown to
  exist". Never "unfortunately", "fail to", "naive".
- Give each prior work's cost in its concrete form (e.g. O(√(pe))) and verify it
  against the original paper, not a secondary description.
- The "Ours" row equals, character for character, the formula in the abstract,
  contribution 3 and the body proposition.
- Your own earlier papers appear in the third person and receive the same factual
  critique as anyone else's.
- When you restate a prior work's bottleneck, reread **that paper's own experiments
  section**; the bottleneck it states about itself is often different from how later
  papers paraphrase it, and misattribution is easy to catch.
- Concurrent work gets its own short labelled paragraph ("Concurrent work.").

## Checklist

- [ ] Organised by axis; Table 1 with an "Ours" row.
- [ ] Contrasting verb pair used for parallel routes.
- [ ] Bridge paragraph + "Our work" paragraph present.
- [ ] Each cost formula verified against the source paper.
- [ ] No evaluative adjectives about others.
