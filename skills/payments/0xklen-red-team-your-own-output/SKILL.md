---
name: red-team-your-own-output
description: Use when about to deliver a claim, plan, or design you produced. Actively hunts the disconfirming case and the failure mode you are least able to see.
---

# Red-Team Your Own Output

You are the most likely source of the error and the least likely to catch it. Spend a pass trying to break your own conclusion before anyone else does.

## Procedure

1. State your main claim in one falsifiable sentence. If it has an "and", split it.
2. Write the strongest counter-argument as if paid to win. Not a strawman — the version a smart opponent would post.
3. Seek disconfirming evidence first, not confirming: `web_search("<claim> is false")`, `web_search("<claim> criticism")`, `grep -ri "contradict" notes/`. Confirmation search is where you already are.
4. Run a pre-mortem: assume the deliverable failed six months out and write the three most likely reasons. Fix the one that is cheap to fix.
5. Probe the assumptions that everything else rests on. List them; for each ask "what would I see if this were false?"
6. Test the load-bearing example. If your argument hinges on one case or number, verify that case independently (see the primary-source skill).
7. Check for the failure patterns that flatter: motivated reasoning toward a tidy answer, base-rate neglect, and overfitting the explanation to a single anecdote.
8. Record what would change your mind. If nothing would, you are defending an identity, not a claim.

```bash
# stress the numbers you were least sure about
grep -rn "approximately\|roughly\|~" draft.md    # each is an unverified claim
```

## Pitfalls

- Red-teaming after you have emotionally committed finds only cosmetic flaws; do it before the draft is polished.
- Seeking one counter-argument and declaring the claim robust is a token gesture; the goal is to find the fatal one.
- Confusing "I cannot disprove it" with "it is true" — absence of a counter is not support.
- Only attacking the easy sub-claim; the weak one is usually the premise you never questioned.
- Skipping the fix because the critique was theoretical; if it is real, patch the output.

## Verification

    grep -cE 'counter|falsif|pre-mortem|would change my mind' redteam.md

Report: "Red-team found 1 fatal flaw (base rate omitted) fixed, 2 minor hedged; main claim now holds under the strongest counter-argument I could build."
