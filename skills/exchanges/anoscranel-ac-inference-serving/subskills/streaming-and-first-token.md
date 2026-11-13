---
name: streaming-and-first-token
domain: software-engineering/streaming-and-first-token
trigger: "Designing the response channel around time-to-first-token."
anti_trigger: "Not for prompt structure, and not for general UX copy."
scope: "Streaming and TTFT: the latency the user actually feels."
status: seedling
---

# Streaming and first token

## Standard

In a streamed response the user's felt latency is time-to-first-token, not total time. A response that completes in six seconds but starts streaming in half a second feels faster than a three-second response delivered as a block. TTFT is dominated by prefill — the compute-bound pass over the prompt — while the stream pace after the first token is decode speed under the current batch load.

The design consequences follow: prompt length drives TTFT more than model size does at the same hardware; a long shared prefix cached as blocks converts directly into lower TTFT for everyone after the first request; and any queueing in front of prefill adds to the felt delay even when the decode fleet is idle below. TTFT and inter-token pace are two different user experiences and get measured and budgeted separately.

Primary sources: <https://docs.anthropic.com/en/api/streaming> and <https://docs.vllm.ai/en/latest/>.

## Decision rules

- Budget TTFT and inter-token pace separately — they respond to different levers.
- Attribute TTFT to queue wait, prefill, or first-decode step by measurement, not guesswork.
- Treat prompt length as the TTFT lever at fixed hardware; document the measured slope.
- Exploit prefix caching for lowering prefill on repeated long prefixes.
- Record token pacing at load, not at idle; consumers experience the loaded value.
- Write the UX contract: what the user sees while TTFT is still elapsing (holding states, partial UI).

## Procedure

1. Instrument TTFT at the gateway and inter-token time along the stream.
2. Decompose TTFT into queue, prefill, and first-step components.
3. Measure the prompt-length-to-prefill slope for the fleet.
4. If prefixes repeat, wire prefix-block sharing and re-measure TTFT.
5. Record both metrics at representative load and at idle; publish the loaded numbers.
6. Define the UX contract for the waiting period and verify it against the measured TTFT tail.

## Anti-patterns

- Reporting only total completion time; the user never feels the mean, only the start.
- Blaming decode speed when the prefill stage dominates TTFT.
- Sampling TTFT on an idle fleet.
- Building holding-state UI for the average TTFT rather than the tail.
- No pacing measurement, so a decode-fleet stall is invisible until users complain.

## Done checklist

- [ ] TTFT decomposed by stage.
- [ ] Prompt-length slope measured.
- [ ] Prefix sharing evaluated where prefixes repeat.
- [ ] Pacing measured at representative load.
- [ ] UX contract matched to the TTFT tail.
- [ ] Both metrics written into the serving record.

## Sources

- Anthropic streaming API: <https://docs.anthropic.com/en/api/streaming>
- vLLM streaming behaviour: <https://docs.vllm.ai/en/latest/>
- Serving-engine context: <https://github.com/triton-inference-server/server>
