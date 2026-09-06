import type { ToolError, ToolResult } from './types.js';

export class SkillError extends Error {
  public readonly code: string;
  public readonly details?: unknown;
  public readonly httpStatus?: number;

  constructor(code: string, message: string, details?: unknown, httpStatus?: number) {
    super(message);
    this.name = 'SkillError';
    this.code = code;
    this.details = details;
    this.httpStatus = httpStatus;
  }
}

export class HttpStatusError extends SkillError {
  constructor(status: number, body: unknown) {
    super('HTTP_ERROR', `HTTP request failed with status ${status}`, body, status);
    this.name = 'HttpStatusError';
  }
}

export function toToolError(err: unknown, fallbackCode = 'UNKNOWN_ERROR'): ToolError {
  if (err instanceof SkillError) {
    return {
      code: err.code,
      message: err.message,
      details: err.details,
      httpStatus: err.httpStatus,
    };
  }

  if (err instanceof Error) {
    return {
      code: fallbackCode,
      message: err.message,
    };
  }

  return {
    code: fallbackCode,
    message: String(err),
  };
}

export function ok<T>(traceId: string, data: T, raw?: unknown): ToolResult<T> {
  return {
    success: true,
    data,
    traceId,
    raw,
  };
}

export function fail<T>(traceId: string, err: unknown, fallbackCode = 'UNKNOWN_ERROR', raw?: unknown): ToolResult<T> {
  return {
    success: false,
    error: toToolError(err, fallbackCode),
    traceId,
    raw,
  };
}

export function requireField<T>(value: T | null | undefined, name: string): T {
  if (value === undefined || value === null || value === '') {
    throw new SkillError('INVALID_INPUT', `${name} is required`);
  }

  return value;
}
