---
name: measure-time-to-first-contribution
description: Use when you need to know whether onboarding actually works. Tracks time-to-first-merged-contribution from a start timestamp to a merge, with a target and a per-blocker log, instead of asking how it went.
---

# Measure Time to First Contribution

"Onboarding felt fine" is not evidence. Time from a new joiner's start to their first merged change, with the blockers logged, shows where the friction is and whether a change helped.

## Procedure

1. Record the start timestamp when access is granted, not when the offer was signed: `date -u +%Y-%m-%dT%H:%M:%SZ > onboarding/start.txt`.
2. Define the finish event precisely: the first commit by the newcomer that reaches `main`.
3. Compute the gap from git, not from memory: `git log --author="<email>" --merges -1 --format=%cI`.
4. Set a target: first merged change within 2 working days; flag any joiner over 5 days.
5. Log each blocker with the minutes it cost (waiting on access, broken bootstrap, unclear task).
6. Compare across joiners; a rising median points at the environment, not the people.
7. Re-measure after each onboarding change to see whether the fix actually moved the number.
8. Report the median and the worst case, not just the average, so outliers stay visible.
9. Exclude pre-arranged mechanical commits (a reverted typo) so the first real change is the one counted.
10. Keep the raw start/finish rows in `onboarding/metrics.csv` so the trend is auditable.
11. Bucket the metric by team so a bad environment is localised.
12. Track blocker categories with counts, not prose.
13. Set the target with the team, so the number is owned rather than imposed.
14. Store each joiner as one row with start, merge, and blocker columns.
15. Chart the trend quarterly so a regression is visible.
16. Share the number with the team, since hidden metrics do not change behaviour.

## Pitfalls

- Counting a merged doc typo from a pre-arranged task as the first contribution, which flatters the metric.
- Measuring from the offer date instead of from access, blaming the joiner for provisioning delays.
- Tracking only the number, never the blockers, so nothing can be fixed.
- Changing many things at once, so you cannot attribute the improvement.
- Hiding a 14-day outlier inside a healthy-looking median.
- Defining "contribution" differently per joiner, so the numbers are not comparable.
- Optimising the metric by pre-merging a fake first commit.
- Comparing across roles that have genuinely different ramp times.
- Reporting a single average that hides the worst onboarding.
- Free-text blocker notes that cannot be counted.
- A single snapshot with no trend.
- Keeping the metric private so nobody acts on it.

## Verification

    python3 - <<'EOF'
    import subprocess
    s=open('onboarding/start.txt').read().strip()
    print('start',s)
    print(subprocess.run(['git','log','--author=<email>','--merges','-1','--format=%cI'],capture_output=True,text=True).stdout)
    EOF
    # passes when the delta is computed in days and each blocker has a cost in minutes

Report to the user: the start and merge timestamps, the day delta, and the ranked blockers.
