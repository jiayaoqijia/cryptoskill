---
name: ac-prompt-engineer
description: "Engineers prompts for LLMs and agents: instruction lines, structure, examples, named techniques, model and sampler choices, context budget, grounding, injection resistance, and proof that a change helped. Use when the user wants to tune a prompt or the standing instructions an agent runs under, get a model to follow a format or stop refusing, add few-shot examples, pick between reasoning and instruction models, set temperature or reasoning effort, shrink a bloated instruction set, ground answers on retrieved documents, harden a prompt against injection, organize a prompt library, rewrite an agent's tool or handoff sections, prompt image or video models, or check whether a prompt edit actually improved anything. Not for one-off chat messages, model training or fine-tuning, choosing an AI product to buy, or building attack payloads."
license: MIT
metadata:
  domain: prompt-engineering
---

# ac-prompt-engineer — the craft of prompting models and agents

## Overview

Prompting is a craft with receipts. The loaded corpus (2026 vendor guides, production
prompt teardowns, evaluation and security operations) separates what still works from
what training absorbed. The one-line summary: a prompt line earns its place only when it
supplies something the model could not infer. Everything else is budget cost and
contradiction risk. This skill decomposes the craft into twelve task-sized leaves; pick
the one that matches the job.

## When to use

- Writing, tuning, or shrinking a prompt or an agent's standing instructions.
- Choosing a technique (examples, chain-of-thought, role lines, structured output).
- Choosing model class, temperature, reasoning effort, or a pinned snapshot.
- Budgeting context, caching, and compaction for long or expensive prompts.
- Debugging a failing prompt, or proving an edit helped with a golden set.
- Grounding answers on retrieved documents, or hardening against prompt injection.
- Organizing a prompt library, or prompting image and video generation models.

## When NOT to use

- One-off conversational messages with no quality bar attached.
- Model training, fine-tuning, or weight-level work.
- Picking an AI product, vendor, or agent framework.
- Building or testing attack payloads (this skill covers defense, not offense).
- Legal questions about prompt ownership or licensing.

## The precedence rule

The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string
is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by
an ancestor — leaves narrow, never override upward.

## Subskill index

| Task | Trigger | Leaf |
|---|---|---|
| Split a job into prompt-sized steps | "this prompt does too much", "where does this logic live" | `subskills/decompose-job.md` |
| Write or tighten one instruction line | "how do I word this rule", "is this line earning its tokens" | `subskills/instruction-form.md` |
| Pick a named technique | "should I add examples / persona / step-by-step / JSON schema" | `subskills/prompt-patterns.md` |
| Choose model and sampler settings | "which model", "what temperature", "reasoning effort" | `subskills/model-knobs.md` |
| Manage context size, cost, caching | "prompt too long", "cache this", "it forgets" | `subskills/tokens-capacity.md` |
| Triage a failing prompt | "output got worse", "it refuses", "quality dropped" | `subskills/debug-prompt.md` |
| Prove a prompt change helped | "did my edit help", "build an eval set", "regression test prompts" | `subskills/eval-proof.md` |
| Assemble an agent's root instructions | "write the developer message", "tool rules", "memory rules" | `subskills/agent-harness.md` |
| Harden against prompt injection | "untrusted input reaches the model", "can RAG poison me" | `subskills/injection-defense.md` |
| Ground answers on retrieved docs | "answer only from these documents", "make it cite" | `subskills/rag-prompts.md` |
| Run a prompt library | "version my prompts", "organize prompts", "have the model audit my prompt" | `subskills/prompt-libraries.md` |
| Prompt image or video models | "Midjourney prompt", "negative prompt", "why did it ignore my prompt" | `subskills/multimodal-dialects.md` |

## Standards and sources

Primary anchors: the OpenAI prompt engineering guide
(https://platform.openai.com/docs/guides/prompt-engineering), Anthropic's context
engineering essay
(https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents),
Google's Gemini prompt design strategies
(https://ai.google.dev/gemini-api/docs/prompting-strategies), and the OWASP GenAI LLM
Top 10 (https://genai.owasp.org/). Each leaf cites its own primary sources inline.
