// ============================================================================
// Custom Error Classes
// ============================================================================

export class ElsaToolError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly details?: unknown
  ) {
    super(message);
    this.name = 'ElsaToolError';
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      details: this.details,
    };
  }
}

export class BudgetExceededError extends ElsaToolError {
  constructor(
    message: string,
    details?: { limit: number; requested: number; spent: number }
  ) {
    super('BUDGET_EXCEEDED', message, details);
    this.name = 'BudgetExceededError';
  }
}

export class RateLimitError extends ElsaToolError {
  constructor(
    message: string,
    details?: { limit: number; current: number; reset_in_seconds: number }
  ) {
    super('RATE_LIMIT_EXCEEDED', message, details);
    this.name = 'RateLimitError';
  }
}

export class ExecutionDisabledError extends ElsaToolError {
  constructor(message: string = 'Execution tools are disabled. Set ELSA_ENABLE_EXECUTION_TOOLS=true to enable.') {
    super('EXECUTION_DISABLED', message);
    this.name = 'ExecutionDisabledError';
  }
}

export class ConfirmationRequiredError extends ElsaToolError {
  constructor(message: string = 'Confirmation token required. Run elsa_execute_swap_dry_run first.') {
    super('CONFIRMATION_REQUIRED', message);
    this.name = 'ConfirmationRequiredError';
  }
}

export class ConfirmationInvalidError extends ElsaToolError {
  constructor(
    message: string,
    details?: { reason: 'expired' | 'not_found' | 'params_mismatch' | 'already_used' }
  ) {
    super('CONFIRMATION_INVALID', message, details);
    this.name = 'ConfirmationInvalidError';
  }
}

export class UpstreamHttpError extends ElsaToolError {
  constructor(
    message: string,
    details?: { status: number; statusText: string; url?: string }
  ) {
    super('UPSTREAM_HTTP_ERROR', message, details);
    this.name = 'UpstreamHttpError';
  }
}

export class PipelineTimeoutError extends ElsaToolError {
  constructor(
    message: string,
    details?: { pipeline_id: string; timeout_seconds: number; last_status: string }
  ) {
    super('PIPELINE_TIMEOUT', message, details);
    this.name = 'PipelineTimeoutError';
  }
}

export class PipelineTaskError extends ElsaToolError {
  constructor(
    message: string,
    details?: { task_id: string; status: string; description?: string }
  ) {
    super('PIPELINE_TASK_ERROR', message, details);
    this.name = 'PipelineTaskError';
  }
}

export class ValidationError extends ElsaToolError {
  constructor(message: string, details?: unknown) {
    super('VALIDATION_ERROR', message, details);
    this.name = 'ValidationError';
  }
}

// ============================================================================
// Error Result Builder
// ============================================================================

export function buildErrorResult(error: unknown): {
  ok: false;
  error: { code: string; message: string; details?: unknown };
} {
  if (error instanceof ElsaToolError) {
    return {
      ok: false,
      error: error.toJSON(),
    };
  }

  if (error instanceof Error) {
    return {
      ok: false,
      error: {
        code: 'INTERNAL_ERROR',
        message: error.message,
      },
    };
  }

  return {
    ok: false,
    error: {
      code: 'UNKNOWN_ERROR',
      message: String(error),
    },
  };
}
