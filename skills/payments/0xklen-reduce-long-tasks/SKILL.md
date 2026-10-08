---
name: reduce-long-tasks
description: Use when Total Blocking Time is high and taps feel unresponsive. Finds main-thread tasks over 50 ms and breaks or yields them.
---

# Reduce Long Tasks

A task over 50 ms blocks the main thread, so input queues behind it. TBT is the sum of that excess, and it is the clearest signal that the page is not ready to be touched.

## Procedure

1. Instrument long tasks to see them in the field, not just in a lab:

       new PerformanceObserver(list => {
         for (const e of list.getEntries())
           navigator.sendBeacon('/rum', JSON.stringify({n:'longtask',d:e.duration,at:e.startTime}));
       }).observe({type: 'longtask', buffered: true});

2. In DevTools Performance, record a load with 4x CPU throttling and open the Long Tasks lane; sort the bottom-up view by "Self time".
3. Break a long loop into chunks that yield between frames, giving the browser a chance to handle input:

       for (const chunk of chunks(items, 200)) {
         process(chunk);
         await scheduler.yield();   // or: await new Promise(r => setTimeout(r, 0));
       }

4. Move parsing and computation off the main thread into a Worker, posting plain data and receiving results.
5. Trim synchronous startup: defer non-critical analytics init until after `requestIdleCallback`, and lazy-init widgets on first interaction.
6. Watch the hydration/parse cost of large dependencies; a 200 kB parser package executed at boot is a guaranteed long task.

## Pitfalls

- Yielding with `setTimeout(..., 0)` in a loop that makes millions of micro-tasks, which schedules more work than it spreads.
- Moving work to a Worker but serializing a huge object across `postMessage`, whose structured clone becomes the new bottleneck.
- Splitting a task into 49 ms slices that still add up inside one frame; the browser coalesces them and the task is still blocking.
- Measuring TBT without throttling and concluding the main thread is free.
- Fixing the loudest task while dozens of 60-80 ms tasks below it sum to more total blocking time.

## Verification

    npx lighthouse https://shop.example.com --preset=perf --form-factor=mobile --only-audits=total-blocking-time --output=json | jq '.audits."total-blocking-time".numericValue'

TBT under 200 ms on the mobile preset. Report the number and the longest task's self-time before and after.
