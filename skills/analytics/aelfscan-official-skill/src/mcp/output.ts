import { getConfig } from '../../lib/config.js';
import type { ToolOutputPolicy } from '../tooling/tool-descriptors.js';
import {
  applyOutputGovernance,
  applySummaryPolicy as applySummaryPolicyFields,
} from '../tooling/mcp-output-governance.js';

function applySummaryPolicy(
  value: unknown,
  policy: ToolOutputPolicy,
  maxItems: number,
): { value: unknown; truncated: boolean } {
  if (policy !== 'summary') {
    return { value, truncated: false };
  }

  return applySummaryPolicyFields(value, maxItems);
}

export function asMcpResult(data: unknown, outputPolicy: ToolOutputPolicy = 'normal') {
  const config = getConfig();
  const maxItems = Math.max(1, config.mcpMaxItems);
  const maxChars = Math.max(1, config.mcpMaxChars);

  const summaryApplied = applySummaryPolicy(data, outputPolicy, maxItems);
  const governed = applyOutputGovernance(summaryApplied.value, {
    maxItems,
    maxChars,
    includeRaw: config.mcpIncludeRaw,
  });
  let payload = governed.payload as Record<string, unknown>;
  if (summaryApplied.truncated && payload?.meta && typeof payload.meta === 'object') {
    payload = {
      ...payload,
      meta: {
        ...(payload.meta as Record<string, unknown>),
        truncated: true,
      },
    };
  }
  const serialized = JSON.stringify(payload, null, 2);

  return {
    content: [
      {
        type: 'text' as const,
        text: serialized,
      },
    ],
  };
}
