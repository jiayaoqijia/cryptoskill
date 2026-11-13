---
name: references-and-gc
domain: software-engineering/references-and-gc
trigger: "Working out what garbage collection may delete in a content store."
anti_trigger: "Not for memory management in a language runtime, and not for retention policy law."
scope: "Reachability, roots, mark-and-sweep at the blob tier, and the race between deletion and fetch."
status: seedling
---

# References and GC

## Standard

In a content-addressed store, data has no intrinsic owner; it has whatever references point to it. A manifest references layers, a commit references a tree, a build references inputs. Garbage collection is therefore a reachability computation: from a set of roots — manifests in current use, tags that exist, builds that matter — walk the reference graph, mark everything reachable, and sweep the rest. What has no path from a root is unreachable regardless of how recently it was written.

The two systems hardest to get right are the root set and the race. If a root is missing from the set, live data is deleted; if roots are managed by the same layer that lags behind reality, deletion lags too. And while collection runs, a fetch may arrive for content that was just deemed unreachable — so the collector must either quiesce the store or tolerate fetch-after-sweep, and which of those it does is a visible design choice.

Primary sources: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects> and <https://llvm.org/docs/>.

## Decision rules

- Record the root set precisely: what a user, tag, manifest, or build must be to count as live.
- Record whether a timestamp ever outranks a reference in deletion decisions.
- Record the collection algorithm and whether fetches are blocked, rejected, or tolerated mid-sweep.
- Record the grace period between unreachable and deleted, and who can override it.
- Record what the collector does with partially uploaded or interrupted content.
- Record how the store logs deletions so an operator can diagnose a wrongly deleted object.

## Procedure

1. Enumerate every category of root the store honours.
2. Test deletion of an object whose only reference was removed mid-cycle.
3. Observe the collector's behaviour against concurrent fetches.
4. Measure the grace period between unreferenced and removed.
5. Check how interrupted uploads are treated by the collector.
6. Write the liveness policy with the race behaviour stated.

## Anti-patterns

- Using age alone as the deletion criterion and deleting referenced content.
- Treating unreferenced as worthless; manifests often reference content not yet committed.
- Running collection without either quiescing or tolerating in-flight fetches.
- Missing roots, the classic cause of data loss in content stores.
- Skipping deletion logs; operators cannot diagnose loss from absence.

## Done checklist

- [ ] Root set enumerated.
- [ ] Reference-versus-time precedence recorded.
- [ ] Collection algorithm and race behaviour recorded.
- [ ] Grace period measured.
- [ ] Interrupted-upload treatment recorded.
- [ ] Deletion logging verified.

## Sources

- Git object reachability model: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>
- Content-addressed caching in tooling: <https://llvm.org/docs/>
- Mark-and-sweep reference: <https://en.wikipedia.org/wiki/Tracing_garbage_collection>
