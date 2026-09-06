import { describe, expect, test } from 'bun:test';
import { SkillError, fail, ok, toToolError } from '../../src/core/errors.js';

describe('errors', () => {
  test('maps SkillError', () => {
    const err = new SkillError('X', 'oops', { a: 1 });
    const e = toToolError(err);
    expect(e.code).toBe('X');
    expect(e.message).toBe('oops');
  });

  test('ok/fail wrappers', () => {
    const success = ok({ a: 1 });
    expect(success.success).toBeTrue();

    const failed = fail(new Error('bad'));
    expect(failed.success).toBeFalse();
    expect(failed.error?.message).toBe('bad');
  });
});
