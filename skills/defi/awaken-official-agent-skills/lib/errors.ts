export class SkillError extends Error {
  code: string;
  details?: unknown;
  traceId?: string;

  constructor(code: string, message: string, details?: unknown, traceId?: string) {
    super(message);
    this.name = 'SkillError';
    this.code = code;
    this.details = details;
    this.traceId = traceId;
  }
}

