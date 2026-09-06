import { afterEach, describe, expect, spyOn, test } from 'bun:test';
import { log, newTraceId, setLogLevel } from '../../src/core/logger.js';

describe('logger', () => {
  let stderrSpy: any;

  afterEach(() => {
    if (stderrSpy) {
      stderrSpy.mockRestore();
      stderrSpy = undefined;
    }
    setLogLevel('error');
  });

  test('filters logs by active level', () => {
    const lines: string[] = [];
    stderrSpy = spyOn(process.stderr, 'write').mockImplementation((chunk: any) => {
      lines.push(String(chunk));
      return true;
    });

    setLogLevel('error');
    log('info', 'should_not_print', { value: 1 });
    log('error', 'should_print', { value: 2 });

    expect(lines.length).toBe(1);
    const parsed = JSON.parse(lines[0].trim()) as Record<string, unknown>;
    expect(parsed.event).toBe('should_print');
    expect(parsed.level).toBe('error');
  });

  test('redacts sensitive fields in payload', () => {
    const lines: string[] = [];
    stderrSpy = spyOn(process.stderr, 'write').mockImplementation((chunk: any) => {
      lines.push(String(chunk));
      return true;
    });

    setLogLevel('debug');
    log('debug', 'redaction_test', {
      privateKey: 'secret-1',
      accessToken: 'secret-2',
      authorization: 'Bearer secret-3',
      tokenValue: 'secret-4',
      keep: 'ok',
    });

    expect(lines.length).toBe(1);
    const parsed = JSON.parse(lines[0].trim()) as Record<string, unknown>;
    expect(parsed.privateKey).toBe('[REDACTED]');
    expect(parsed.accessToken).toBe('[REDACTED]');
    expect(parsed.authorization).toBe('[REDACTED]');
    expect(parsed.tokenValue).toBe('[REDACTED]');
    expect(parsed.keep).toBe('ok');
  });

  test('newTraceId returns uuid v4 string', () => {
    const traceId = newTraceId();
    expect(traceId).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i);
  });
});
