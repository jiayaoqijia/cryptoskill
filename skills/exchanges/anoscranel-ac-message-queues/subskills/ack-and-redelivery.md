---
name: ack-and-redelivery
domain: software-engineering/ack-and-redelivery
trigger: "Reading what happens when a consumer dies holding a message."
anti_trigger: "Not for broker selection, and not for the poison path specifically."
scope: "Acknowledgement windows, the death-during-processing case, and redelivery."
status: seedling
---

# Ack and redelivery

## Standard

The acknowledgement is a promise with a timing question: ack before processing and a crash loses the work silently; ack after processing and a crash between the work and the ack redelivers it. At-least-once systems choose the second, which makes the redelivery the normal case rather than the exception, and makes the consumer's tolerance of it the actual correctness mechanism.

The mechanics worth reading are the ack's scope and the redelivery's address. Some brokers ack per-message, some per-batch — and a batch ack that covers messages a worker has not touched yet turns a crash into silent loss, the exact failure the ack was meant to prevent. The redelivery's address decides whether a message returns to the front of its queue, lands on another consumer in the group, or waits out a visibility timeout; each behaviour changes what a wedged worker does to the tail behind it.

Primary sources: <https://www.rabbitmq.com/tutorials/tutorial-one-python> and <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html>.

## Decision rules

- Record the ack's timing: before work, after work, or after persistence.
- Record the ack's scope: per message or per batch, and what a batch ack covers.
- Record the redelivery address and the delay before it returns.
- Record the redelivery count a consumer can observe, if the broker exposes one.
- Record the timeout that assumes death — and what a slow-but-alive worker does to it.
- Record the duplicate-handling obligation placed on the consumer by these choices.

## Procedure

1. State the ack timing and what dies unacked.
2. State the ack scope and whether it can cover untouched work.
3. Trace a consumer killed mid-message from the broker's view.
4. Trace a consumer killed after work but before ack.
5. Check the visibility or lease timeout against the slowest legitimate processing time.
6. Write the redelivery behaviour with the consumer's obligations named.

## Anti-patterns

- Batch-acking to save round trips without checking what a crash loses.
- A visibility timeout shorter than legitimate work, redelivering live messages.
- Treating redelivery as an error path when it is the design.
- Assuming the redelivered message goes to the same consumer.
- Acknowledging on receipt, converting at-least-once to at-most-once by accident.

## Done checklist

- [ ] Ack timing stated.
- [ ] Ack scope stated.
- [ ] Mid-message crash traced.
- [ ] Pre-ack crash traced.
- [ ] Timeout checked against slow work.
- [ ] Consumer obligations named.

## Sources

- Acknowledgement tutorial: <https://www.rabbitmq.com/tutorials/tutorial-one-python>
- Visibility timeout semantics: <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html>
- Messaging background: <https://www.enterpriseintegrationpatterns.com/>
