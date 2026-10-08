---
name: add-backpressure-to-a-queue-worker
description: Use when a consumer falls behind and the queue grows without bound — bounds in-flight work, handles visibility timeouts and dead-letters poison messages instead of losing them.
---

# Add backpressure to a queue worker

A consumer that accepts work faster than it can process it is no consumer at all: the queue grows, memory grows, and the oldest messages expire unprocessed. Slow the intake to match the processing rate.

## Procedure

1. Measure the steady-state drain rate before tuning: processed-per-second and queue depth over an hour. Depth growing linearly at constant input means the worker is under-provisioned or blocked.

2. Bound the in-flight work: RabbitMQ `basic_qos(prefetch_count=2*concurrency)`, Kafka `max.poll.records=500`, SQS a fixed `MaxNumberOfMessages` with a fixed poller count. Unbounded prefetch pulls the whole queue into memory.

3. Make processing idempotent so a redelivery (visibility timeout, rebalance) cannot double-apply:
       if redis.set(f"done:{msg.id}", 1, nx=True, ex=86400) is None: ack(); return

4. Set the visibility timeout above the p99 processing time, not the mean, and dead-letter after a bound:
       maxReceiveCount = 5  →  DLQ
   A message that times out mid-processing is redelivered; with a slow handler it is redelivered forever unless it reaches the DLQ.

5. Apply backpressure to producers by exposing consumer lag and pausing intake when a downstream is slow: `basic_cancel` or `consumer.pause()`. The broker retains messages; dropping them is not backpressure.

6. For Kafka, watch lag per partition. One hot partition with lag while others idle indicates a bad partition key — re-key or add partitions.

7. Auto-scale on queue depth, not CPU: I/O-blocked workers show low CPU while lag grows. Scale when `queue_depth / drain_rate > 60s`.

## Pitfalls

- Unbounded `prefetch_count`, so one worker holds 100k messages in memory, crashes, and drops them all back onto the queue at once.
- A visibility timeout shorter than the slowest handler, so messages loop forever and never reach the DLQ because each attempt looks like it is still running.
- Non-idempotent side effects (charge, email) applied on every redelivery.
- Scaling on CPU for an I/O-bound worker, so the autoscaler never fires during the actual backlog.

## Verification

    aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages
    awk '/processed/{p++} END{print p}' worker.log    # drain rate vs input rate
    # steady state: depth flat, NotVisible == prefetch * workers

Report: prefetch/poll settings, the measured drain rate against the input rate, a steady-state depth that is flat rather than growing, and the DLQ redrive policy (maxReceiveCount=5).
