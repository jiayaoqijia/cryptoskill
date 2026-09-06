import { describe, expect, test } from 'bun:test';
import { runTool, withTraceId } from '../../src/mcp/runtime.js';

describe('mcp runtime', () => {
  test('withTraceId injects traceId when result is a tool payload', () => {
    const result = withTraceId({ success: true, data: { ok: 1 } }, 'trace-1') as any;
    expect(result.traceId).toBe('trace-1');
  });

  test('withTraceId keeps existing traceId', () => {
    const result = withTraceId(
      { success: true, traceId: 'trace-existing', data: {} },
      'trace-new',
    ) as any;
    expect(result.traceId).toBe('trace-existing');
  });

  test('runTool logs failed tool response and returns formatted payload', async () => {
    const logs: Array<{ event: string; payload?: Record<string, unknown> }> = [];
    const output = await runTool(
      'tool-a',
      { a: 1 },
      async () => ({ success: false, error: { code: 'X', message: 'oops' } }),
      {
        newTraceId: () => 'trace-failed',
        toToolError: err => ({ code: 'E', message: String(err) }),
        logError: (event, payload = {}) => {
          logs.push({ event, payload });
        },
      },
    );

    const parsed = JSON.parse(output.content[0]?.text || '{}');
    expect(parsed.success).toBeFalse();
    expect(parsed.traceId).toBe('trace-failed');
    expect(logs[0]?.event).toBe('mcp_tool_failed');
  });

  test('runTool maps thrown error through toToolError and logs exception', async () => {
    const logs: Array<{ event: string; payload?: Record<string, unknown> }> = [];
    const output = await runTool(
      'tool-b',
      {},
      async () => {
        throw new Error('boom');
      },
      {
        newTraceId: () => 'trace-exception',
        toToolError: () => ({
          code: 'MAPPED_ERROR',
          message: 'mapped message',
          details: { where: 'test' },
        }),
        logError: (event, payload = {}) => {
          logs.push({ event, payload });
        },
      },
    );

    const parsed = JSON.parse(output.content[0]?.text || '{}');
    expect(parsed.success).toBeFalse();
    expect(parsed.traceId).toBe('trace-exception');
    expect(parsed.error.code).toBe('MAPPED_ERROR');
    expect(logs[0]?.event).toBe('mcp_tool_exception');
  });
});
