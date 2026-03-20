class JupiterPredictionError extends Error {
  constructor(message, status = 0, code = 'UNKNOWN_ERROR', details = null) {
    super(message);
    this.name = 'JupiterPredictionError';
    this.status = status;
    this.code = code;
    this.details = details;
    Error.captureStackTrace(this, this.constructor);
  }

  isRetryable() {
    return this.status === 429 || 
           this.status === 500 || 
           this.status === 502 || 
           this.status === 503 ||
           this.status === 504;
  }

  isAuthError() {
    return this.status === 401 || this.status === 403;
  }

  isNotFound() {
    return this.status === 404;
  }

  isClientError() {
    return this.status >= 400 && this.status < 500;
  }

  isServerError() {
    return this.status >= 500;
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      status: this.status,
      code: this.code,
      details: this.details,
      stack: this.stack
    };
  }
}

class ValidationError extends JupiterPredictionError {
  constructor(message, details = null) {
    super(message, 400, 'VALIDATION_ERROR', details);
    this.name = 'ValidationError';
  }
}

class AuthenticationError extends JupiterPredictionError {
  constructor(message = 'Authentication failed') {
    super(message, 401, 'AUTHENTICATION_ERROR');
    this.name = 'AuthenticationError';
  }
}

class RateLimitError extends JupiterPredictionError {
  constructor(retryAfter = null) {
    const message = retryAfter 
      ? `Rate limit exceeded. Retry after ${retryAfter} seconds` 
      : 'Rate limit exceeded';
    super(message, 429, 'RATE_LIMIT_ERROR', { retryAfter });
    this.name = 'RateLimitError';
  }
}

class NotFoundError extends JupiterPredictionError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404, 'NOT_FOUND');
    this.name = 'NotFoundError';
  }
}

function handleError(error, context = {}) {
  const { operation, params } = context;

  if (error instanceof JupiterPredictionError) {
    return {
      success: false,
      error: error.message,
      code: error.code,
      status: error.status,
      retryable: error.isRetryable(),
      operation,
      params
    };
  }

  if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
    return {
      success: false,
      error: 'Network error: Unable to connect to Jupiter API',
      code: 'NETWORK_ERROR',
      status: 0,
      retryable: true,
      operation,
      params
    };
  }

  return {
    success: false,
    error: error.message || 'Unknown error',
    code: 'UNKNOWN_ERROR',
    status: 0,
    retryable: false,
    operation,
    params
  };
}

async function withRetry(operation, options = {}) {
  const { 
    maxRetries = 3, 
    baseDelay = 1000, 
    maxDelay = 10000,
    retryableStatuses = [429, 500, 502, 503, 504]
  } = options;

  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;

      const shouldRetry = 
        attempt < maxRetries && 
        (retryableStatuses.includes(error.status) || error.isRetryable());

      if (!shouldRetry) {
        throw error;
      }

      const delay = Math.min(
        baseDelay * Math.pow(2, attempt),
        maxDelay
      );

      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError;
}

module.exports = {
  JupiterPredictionError,
  ValidationError,
  AuthenticationError,
  RateLimitError,
  NotFoundError,
  handleError,
  withRetry
};
