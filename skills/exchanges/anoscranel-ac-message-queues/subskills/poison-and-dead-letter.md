---
name: poison-and-dead-letter
domain: software-engineering/poison-and-dead-letter
trigger: "Handling a message that cannot be processed no matter how many times it arrives."
anti_trigger: "Not for the ack mechanics, and not for retry policy in general systems."
scope: "The unreadable message, retry limits, and the dead-letter path with its reasons."
status: seedling
---

# Poison and dead letter

## Standard

A poison message fails for a reason no retry repairs: a schema the consumer cannot parse, a reference to a record that no longer exists, a payload that violates an invariant. Retrying it forever burns the worker; dropping it loses evidence. The dead-letter path is the third option: after a stated number of attempts, the message is diverted to another queue with the reason attached, the original keeps flowing, and the failure becomes inspectable instead of destructive.

The design obligation is explicit limits with explicit reasons. A message should land in the dead-letter queue carrying which attempt it was, what error each attempt produced, and from which queue and consumer it came — enough to diagnose it in place rather than replay it blind. And the dead-letter queue itself needs a reader and an alarm: an unmonitored dead-letter path is a data loss queue with a reassuring name.

Primary sources: <https://www.rabbitmq.com/tutorials/tutorial-one-python> and <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html>.

## Decision rules

- Record the retry limit and what counts as an attempt under redelivery.
- Record the dead-letter destination and the metadata attached on diversion.
- Record the errors that divert immediately versus those that merit retries.
- Record who reads the dead-letter queue and how often it is expected to be empty.
- Record the alarm on dead-letter arrival rate.
- Record the replay procedure from dead-letter back to the source, and its preconditions.

## Procedure

1. Define the retry limit and the attempt counter's scope.
2. Configure the diversion with its reason and attempt metadata.
3. Classify failure causes: transient, permanent, or unknown.
4. Name the dead-letter reader and the cadence.
5. Set the alarm and the threshold that triggers it.
6. Write the replay procedure with its precondition — fix first, replay second.

## Anti-patterns

- Infinite redelivery for a message no retry can fix.
- Dropping at the limit and calling the loss handled.
- A dead-letter queue no one reads or alarms on.
- Replaying poison without fixing the cause, returning it to poison.
- One dead-letter queue for every failure with no reason recorded.

## Done checklist

- [ ] Retry limit and attempt scope defined.
- [ ] Diversion metadata recorded.
- [ ] Failure causes classified.
- [ ] Reader and cadence named.
- [ ] Alarm with threshold set.
- [ ] Replay procedure written.

## Sources

- Dead-letter exchange behaviour: <https://www.rabbitmq.com/tutorials/tutorial-one-python>
- Managed dead-letter queue documentation: <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html>
- Message channel patterns: <https://www.enterpriseintegrationpatterns.com/>
