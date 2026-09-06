// ============================================================
// Unit Test: CLI helpers — outputSuccess, outputError
// ============================================================

import { describe, test, expect, mock, beforeEach, afterEach } from 'bun:test';

describe('CLI helpers', () => {
  let originalLog: typeof console.log;
  let originalError: typeof console.error;
  let originalExit: typeof process.exit;

  let logOutput: string[];
  let errorOutput: string[];
  let exitCode: number | undefined;

  beforeEach(() => {
    logOutput = [];
    errorOutput = [];
    exitCode = undefined;

    originalLog = console.log;
    originalError = console.error;
    originalExit = process.exit;

    console.log = (...args: any[]) => {
      logOutput.push(args.map(String).join(' '));
    };
    console.error = (...args: any[]) => {
      errorOutput.push(args.map(String).join(' '));
    };
    // Mock process.exit to not actually exit
    process.exit = ((code?: number) => {
      exitCode = code;
      throw new Error(`process.exit(${code})`);
    }) as any;
  });

  afterEach(() => {
    console.log = originalLog;
    console.error = originalError;
    process.exit = originalExit;
  });

  test('outputSuccess outputs valid JSON to stdout', async () => {
    const { outputSuccess } = await import('../../cli-helpers');
    outputSuccess({ balance: '100.5', symbol: 'ELF' });

    expect(logOutput).toHaveLength(1);
    const parsed = JSON.parse(logOutput[0]);
    expect(parsed.status).toBe('success');
    expect(parsed.data.balance).toBe('100.5');
    expect(parsed.data.symbol).toBe('ELF');
  });

  test('outputSuccess handles arrays', async () => {
    const { outputSuccess } = await import('../../cli-helpers');
    outputSuccess([1, 2, 3]);

    const parsed = JSON.parse(logOutput[0]);
    expect(parsed.status).toBe('success');
    expect(parsed.data).toEqual([1, 2, 3]);
  });

  test('outputSuccess handles null', async () => {
    const { outputSuccess } = await import('../../cli-helpers');
    outputSuccess(null);

    const parsed = JSON.parse(logOutput[0]);
    expect(parsed.status).toBe('success');
    expect(parsed.data).toBeNull();
  });

  test('outputError writes to stderr with [ERROR] prefix', async () => {
    const { outputError } = await import('../../cli-helpers');

    try {
      outputError('Something went wrong');
    } catch {
      // expected: process.exit throws
    }

    expect(errorOutput).toHaveLength(1);
    expect(errorOutput[0]).toBe('[ERROR] Something went wrong');
  });

  test('outputError calls process.exit(1)', async () => {
    const { outputError } = await import('../../cli-helpers');

    try {
      outputError('fail');
    } catch {
      // expected
    }

    expect(exitCode).toBe(1);
  });

  test('outputSuccess produces pretty-printed JSON (indented)', async () => {
    const { outputSuccess } = await import('../../cli-helpers');
    outputSuccess({ a: 1 });

    // Should be pretty-printed with 2-space indent
    expect(logOutput[0]).toContain('\n');
    expect(logOutput[0]).toContain('  ');
  });
});
