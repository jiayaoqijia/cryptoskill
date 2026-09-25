# 11 Conclusion

Two to three sentences, no new information, at most half a page.

## Template

> We presented <framework/construction> in which <structural statement>, so that
> <prior works> become special cases of <one cost formula / one family>.
> More importantly, <structure> yields <new construction> for <coverage>, and
> <algorithm> accelerates <stage> by <range> over <strongest baseline>.
> [Optional] <One or two open problems / invitation for third-party analysis.>

## Rules

- Same numbers, scope and wording as the abstract. No claim that the abstract lacks.
- Symmetric-design papers: include generalisability and invite third-party
  cryptanalysis; publish the analysis scripts.
- Theory papers: one or two precise open problems are welcome.
- If pages are tight, the optional third sentence is the first thing to go; the
  conclusion must still end on the last allowed body page.
- Do not "summarise the sections" ("In Section 3 we ...").

## Toy (T2, illustrative)

> We showed that a SAT model with a truncated-difference layer finds 6-round
> distinguishers for ToySPN-64 that exhaustive-trail search misses, and that its cost
> grows linearly in the number of rounds. The resulting distinguisher has probability
> 2^{-58} [illustrative], two rounds more than the best previous one. Extending the
> model to related-key trails is left open.
