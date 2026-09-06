import { toToolError } from '../core/errors.js';
import { logError, newTraceId } from '../core/logger.js';

type RuntimeDeps = {
  toToolError: typeof toToolError;
  logError: typeof logError;
  newTraceId: typeof newTraceId;
};

const defaultDeps: RuntimeDeps = {
  toToolError,
  logError,
  newTraceId,
};

function format(result: unknown) {
  return {
    content: [
      {
        type: 'text' as const,
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

export function withTraceId(result: unknown, traceId: string): unknown {
  if (!result || typeof result !== 'object' || !('success' in result)) {
    return result;
  }
  const record = result as Record<string, unknown>;
  return {
    ...record,
    traceId: record.traceId || traceId,
  };
}

export async function runTool(
  name: string,
  input: unknown,
  handler: (payload: any) => Promise<unknown>,
  deps: RuntimeDeps = defaultDeps,
) {
  const traceId = deps.newTraceId();
  try {
    const raw = await handler(input);
    const result = withTraceId(raw, traceId);
    if ((result as any)?.success === false) {
      deps.logError('mcp_tool_failed', {
        tool: name,
        traceId,
        error: (result as any).error,
      });
    }
    return format(result);
  } catch (err) {
    const error = deps.toToolError(err);
    deps.logError('mcp_tool_exception', { tool: name, traceId, error });
    return format({
      success: false,
      traceId,
      error,
    });
  }
}
