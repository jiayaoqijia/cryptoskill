---
name: async-processing-jobs
domain: software-engineering/async-processing-jobs
trigger: "Running expensive media work asynchronously without losing track of it."
anti_trigger: "Not for workflow orchestration in general, and not for capacity profiling."
scope: "The worker pattern for expensive media work: queueing, progress tracking, partial results, cancellation, and SLA."
status: seedling
---

# Async processing jobs

## Standard

Media work is too slow to run inside a web request. A transcode of a long video takes minutes; an image derivative set can take seconds; but even seconds is beyond the request/response contract of most web applications. The pipeline therefore runs **asynchronously**: the upload handler enqueues a job, returns a handle immediately, and the user's interface polls or subscribes for progress. The upload URL and the "your media is ready" URL are different endpoints with different lifecycles.

The job's state machine is the design's backbone: **queued → processing → done/failed/cancelled**. Each state comes with its own contract — queued work is resumable, processing work reports progress, done work exposes its derivatives, failed work exposes a reason (and, for media, often a partially-completed derivative set), and cancelled work cleans up after itself. Designing the intermediate "processing" state is the craft: progress is not "52%" but a set of mechanical facts — which derivative is being generated, how many remain, whether the current one can be retried independently.

A thought-through pipeline answers three questions the moment a job fails. Can the source be reprocessed? Can the failed derivative alone be retried? Is anything downstream gated on this job's completion? Those answers exist because the pipeline treats jobs as first-class objects, not as opaque background work whose disappearance is discovered when a thumbnail URL 404s in production.

## Decision rules

- Media work runs in an asynchronous queue; the request handler enqueues and returns a handle, never blocks.
- Job state machine: queued → processing → done/failed/cancelled, each with its own contract.
- Progress is reported in mechanical facts (current derivative, remaining count), not vague percentages.
- Partial results are first-class: completed derivatives from a failed job must be usable or cleanly discarded.
- Cancellation must actually cancel: in-flight encoder processes are terminated, not orphaned.
- An SLA on queue depth and processing time is monitored; "no one noticed the backlog" is itself a failure.


## Procedure

1. Enqueue the job with (source-id, recipe-version) and return a job handle to the client.
2. Drive the pipeline in a worker process; emit progress facts to a store the client can poll.
3. On partial failure, mark the specific derivative as failed and let completed derivatives survive.
4. On cancellation, kill the encoder process, clean in-flight temporary files, and mark the job state.
5. Monitor queue depth and processing duration against a stated SLA; alert on breach.
6. Cleanup jobs for cancelled/failed work run on their own schedule, not in the failure handler.

## Anti-patterns

- Polling "is it done yet" without exposing mechanical progress facts.
- Losing partial results: a failed 9/10-rendition job discarding the 9 finished renditions.
- Cancellation that marks the state but leaves the encoder process running.
- No queue-depth alerting; the pipeline dies by silent saturation.

## Done checklist

- [ ] Job state machine implemented with all five states.
- [ ] Progress facts (not percentages) emitted and consumable.
- [ ] Partial results usable or cleanly discarded, stated per derivative.
- [ ] Cancellation terminates actual work, verified by process check.
- [ ] Queue-depth and duration SLA monitored.
- [ ] Cleanup job exists for cancelled/failed work.

## Sources

- Asynchronous processing and background jobs: <https://12factor.net/backing-services>
- MDN web video codec guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs>
