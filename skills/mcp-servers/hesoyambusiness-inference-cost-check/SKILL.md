---
name: inference-cost-check
description: Estimate the cost and check crypto funding conditions for a proposed 1NFER task without sending a paid model request.
---
Connect to public read-only MCP https://hesoyam.business/agent-tools/mcp . Call list_models, estimate_cost with exact model and estimated input/output tokens, and payment_terms. These operations do not generate inference or spend money.
The estimate uses public reference rates. Do not assume an earned account discount, official model provenance or that one model will achieve the same quality as another. If price fields are unavailable, report that an estimate is unavailable; never invent a rate. Check the authenticated account separately through the local client to determine actual account rates.
Return a brief cost/compatibility comparison and suggest one small authorized task only if it meets the operator's requirements. Registration, invoice creation and transfer require the applicable authority; they are not implied by reading this skill. No free generation, fake benchmarks or automatic funding. No keys in prompts, URLs or public files.
