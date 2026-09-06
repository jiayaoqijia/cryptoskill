import type { ToolError, ToolResult } from './types.js';

export class SkillError extends Error {
  public readonly code: string;
  public readonly details?: unknown;

  constructor(code: string, message: string, details?: unknown) {
    super(message);
    this.code = code;
    this.details = details;
  }
}

export function toToolError(err: unknown): ToolError {
  if (err instanceof SkillError) {
    return {
      code: err.code,
      message: err.message,
      details: err.details,
    };
  }
  if (err instanceof Error) {
    return {
      code: 'UNKNOWN_ERROR',
      message: err.message,
    };
  }
  return {
    code: 'UNKNOWN_ERROR',
    message: String(err),
  };
}

export function ok<T>(data: T, extras?: Pick<ToolResult<T>, 'traceId' | 'tx'>): ToolResult<T> {
  return {
    success: true,
    data,
    ...extras,
  };
}

export function fail<T>(err: unknown, traceId?: string): ToolResult<T> {
  return {
    success: false,
    error: toToolError(err),
    traceId,
  };
}

export function requireField<T>(value: T | null | undefined, name: string): T {
  if (value === null || value === undefined || value === '') {
    throw new SkillError('INVALID_INPUT', `${name} is required`);
  }
  return value;
}
