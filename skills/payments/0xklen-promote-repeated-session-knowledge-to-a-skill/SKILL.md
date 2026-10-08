---
name: promote-repeated-session-knowledge-to-a-skill
description: Use when the same procedure is re-derived from scratch every session. Turns the repeatable steps into a skill with real commands and pitfalls.
---

# Promote Repeated Session Knowledge to a Skill

If you have worked out the same steps three times, the fourth time should be a lookup. Promotion turns a re-derived procedure into a stored one — but only when it is stable.

## Procedure

1. Confirm the repetition: find three separate sessions where the same steps were derived.
2. Write the procedure down as the exact commands that worked, not a paraphrase.
3. Include the environment: paths, versions, credential source, so it runs without re-discovery.
4. Add the pitfalls you actually hit — a skill without its failure modes re-derives them.
5. Give it a slug that states the action: `promote-repeated-session-knowledge-to-a-skill`, not `session-tips`.
6. Add a verification block: the command that proves the procedure worked.
7. Test the skill on a clean context: run it as if you had never done it before.
8. If a step needs judgement that varies by case, keep that as a branch, not a fixed command.
9. Only promote procedures that have succeeded three times; a twice-used trick may still be wrong.
10. Link it from the session notes so the next occurrence finds the skill instead of re-deriving.

## Pitfalls

- Promoting a procedure that worked once, freezing a lucky result into policy.
- Writing the steps in prose so the next reader cannot run them verbatim.
- Omitting the pitfalls, so the skill re-derives the same failure every time.
- Encoding case-specific judgement as a fixed command, breaking it on the next input.
- Promoting before the third occurrence, when the procedure is still changing each run.

- Promoting the steps but not the environment, so the next run fails on a missing path.
- Copying an example from another skill and leaving its commands, which do not apply.
- Making the skill so general that it no longer states a runnable step.

## Verification

    ls skills/<slug>/SKILL.md && grep -c "^[0-9]\." skills/<slug>/SKILL.md
    # passes when the skill exists and every step is a runnable command or an explicit branch

Report to the user: the slug created, the three sessions that showed the repetition, and the verification command.
