import { fail, ok, SkillError } from '../../lib/errors.js';
import { getConfig } from '../../lib/config.js';
import { normalizeAddress, normalizeChainId } from '../../lib/normalize.js';
import { createTraceId } from '../../lib/trace.js';
import type { PaginationInput, ToolResult } from '../../lib/types.js';

export type ActionResult<T> = {
  data: T;
  raw?: unknown;
};

export async function executeTool<T>(
  action: (traceId: string) => Promise<ActionResult<T>>,
  fallbackCode: string,
): Promise<ToolResult<T>> {
  const traceId = createTraceId();

  try {
    const result = await action(traceId);
    return ok(traceId, result.data, result.raw);
  } catch (error) {
    return fail(traceId, error, fallbackCode);
  }
}

export function resolveChainId(chainId?: string): string {
  const config = getConfig();
  return normalizeChainId(chainId ?? config.defaultChainId);
}

export function resolveAddress(address?: string): string {
  return normalizeAddress(address);
}

export function toPaginationQuery(input: PaginationInput): Record<string, unknown> {
  const config = getConfig();
  const query: Record<string, unknown> = {
    orderBy: input.orderBy,
    sort: input.sort,
    orderInfos: input.orderInfos,
    searchAfter: input.searchAfter,
  };

  if (input.skipCount !== undefined) {
    if (!Number.isInteger(input.skipCount) || input.skipCount < 0) {
      throw new SkillError('INVALID_INPUT', 'skipCount must be an integer greater than or equal to 0');
    }
    query.skipCount = input.skipCount;
  }

  if (input.maxResultCount !== undefined) {
    if (!Number.isInteger(input.maxResultCount) || input.maxResultCount <= 0) {
      throw new SkillError('INVALID_INPUT', 'maxResultCount must be a positive integer');
    }
    query.maxResultCount = Math.min(input.maxResultCount, config.maxResultCount);
  }

  return {
    ...query,
  };
}
