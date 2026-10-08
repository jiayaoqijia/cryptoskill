---
name: find-the-critical-path-of-a-plan
description: Use when a plan has parallel and dependent tasks and you need to know which a delay would actually push the date. Computes the longest dependency path so attention lands on the tasks that matter.
---

# Find the critical path of a plan

The end date is set by one chain of dependencies, not by the sum of all work. Managing anything off that chain is overhead; missing a task on it moves the date. Compute the path before you schedule.

## Procedure

1. Write the tasks with durations and dependencies. Keep a plain text edge list in `notes/deps.txt`:

       notes/deps.txt
       design 3 -> api
       api 5 -> ui
       db 4 -> api
       ui 2 -> test
       test 2 ->

2. Compute earliest start/finish with a topological pass. A small script is more reliable than doing it by eye:

       python3 - <<'PY'
       dur={'design':3,'api':5,'db':4,'ui':2,'test':2}
       dep={'api':['design','db'],'ui':['api'],'test':['ui'],'design':[],'db':[]}
       order=[]; seen=set()
       def visit(n):
           if n in seen: return
           for d in dep[n]: visit(d)
           seen.add(n); order.append(n)
       for n in dur: visit(n)
       ef={}
       for n in order:
           ef[n]=max([ef[d] for d in dep[n]] or [0])+dur[n]
       print(ef); print('finish', max(ef.values()))
       PY
       {'design': 3, 'db': 4, 'api': 9, 'ui': 11, 'test': 13}
       finish 13

3. Backtrack from the finish: at each task, the predecessor whose earliest finish equals this task's earliest start is on the critical path. Here: db -> api -> ui -> test = 13 days.
4. Tasks with float (slack) — design, which finished at 3 while db finished at 4 — can slip by the slack without moving the date. Slack = late finish − early finish.
5. Recompute whenever a duration or dependency changes; the critical path is not stable, it jumps to whichever chain is now longest.
6. Watch for a nearly-critical chain (slack under ~1 day). It becomes critical on the smallest slip, so give it attention too.

## Pitfalls

- Assuming the longest individual task is on the critical path — duration and path length are different questions.
- Ignoring resource contention: two tasks "in parallel" that need the same person are serial in reality.
- Forgetting external waits (a review, a deploy window) that belong on the path as zero-work but real-duration nodes.
- Recomputing once and trusting it; the path moves as tasks finish.
- Speeding up off-path work to "save time," which saves nothing.

## Verification

    python3 -c "dur={'design':3,'api':5,'db':4,'ui':2,'test':2}; print('check finish',4+5+2+2)"
    # 13 — matches the script's finish; a mismatch means a dependency was mis-transcribed

Report the critical path as an ordered list, the total duration, and the tasks with zero slack.
