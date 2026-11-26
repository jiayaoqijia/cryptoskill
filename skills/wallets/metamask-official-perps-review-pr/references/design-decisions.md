# Why the review checklist looks like this

Background for maintainers. Not part of a routine review.

## Problem

The Mobile checklist had 41 rows. Some did not say what to look for, some checks could never apply in a repository, and another team could not use the generator. We wanted clearer rows without losing a real finding.

## What we chose

- One row per check, with a plain title. Perps rows that have one say what they prevent.
- Only setup, verdict and the blocking policy were merged. No rule text was removed.
- Checks a repository cannot meet are left out of its checklist, such as Pro mode outside Mobile.
- No filter and no model decides what to skip.
- A review launched by hand gets its own folder, checklist and ledger, and later rounds build on earlier ones.
- Any team can generate a review from its own rules. Rules can be antipatterns or requirements.

| Repository | Rows before | Rows now |
| --- | --- | --- |
| Mobile | 41 | 37 |
| Extension | 44 | 39 |
| Core | 41 | 35 |
| Terminal | 37 | 31 |

## What we tried

Filters were replayed on 47 recorded reviews with 360 finding rows. These are what the reviewers reported, and not all were confirmed.

| Option | Result | Decision |
| --- | --- | --- |
| Merge real checks | 31 rows | Rejected: a merged row is easier to skim |
| Merge two rule checks into one row | 36 rows | Rejected: a check needs its own row to be marked or skipped |
| Keyword filter | Skipped 6 rows per review and hid no finding | Not used: tuned on the same reviews |
| Small model as filter | Hid 17 findings | Rejected |
| Small model that can only restore rows | Hid no finding, skipped 5 rows per review | Not used: no proven benefit |
| Decision model, 24 small diffs | Skipped nothing at the cut set beforehand. A cut chosen afterwards hid 0 of 31 findings, and 1 of 31 when each PR was held out | Rejected for now |
| One mark per section | Found the same known issues at 36% less cost | Not used: one run, thinner evidence |
| Ask in plain text to tick each row | The reviewer wrote the whole ledger, then ticked all 37 rows in one edit | Rejected: a script creates the ledger and refuses missing evidence |
| Cheaper reviewer | 2 of 6 unattended runs approved a PR with two known Majors | Rejected |

## Proof

One public PR, MetaMask/metamask-mobile#39018 at 267d34c7 (41 files). Two Majors were fixed before it merged. One run per version with the standard reviewer, marking one row at a time:

| | 41 rows | 36 rows |
| --- | --- | --- |
| Known Majors found | 2 of 2 | 2 of 2 |
| Cost | 100% | 69% |
| Tokens | 100% | 67% |

The list here differs from the tested one: the Mobile reference paths have their own row again, three checks moved to the client section, and two delegation rows keep their old titles.

## Limits

- One PR and one run per version. The cost gap may be chance: the runs also worked in different ways.
- Marking one row at a time does not force a reviewer to work row by row. In a hand-launched test the reviewer did four rows that way, then wrote the rest together. The ledger check still made every row answered with evidence.
- The warm round was tested on one PR with one reviewer. It resolved both Majors from the first round and missed a weak test an earlier review had reported.
- Only Mobile was tested. Extension, Core and Terminal use the same generator, and their own checks keep their old row text.
- No other team has used the generator yet.

## Repeat it

Use the same commit and prompt with each checklist. Score known Majors first, then cost. Keep a new list only if it finds every known Major.
