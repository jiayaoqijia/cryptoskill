const fetch = require('cross-fetch');
const { ApiKeyManager, ApiKeyError } = require('./utils/api-key');

const BASE_URL = 'https://api.jup.ag/prediction/v1';

class JupiterPredictionError extends Error {
  constructor(message, status, code = 'API_ERROR') {
    super(message);
    this.name = 'JupiterPredictionError';
    this.status = status;
    this.code = code;
  }
}

class RateLimitError extends JupiterPredictionError {
  constructor(retryAfter = 1) {
    super('Rate limit exceeded', 429, 'RATE_LIMIT_ERROR');
    this.retryAfter = retryAfter;
  }
}

class JupiterPredictionClient {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || BASE_URL;
    this.apiKey = options.apiKey || null;
    this.timeout = options.timeout || 30000;
    this.maxRetries = options.maxRetries || 3;
    this.baseDelay = options.baseDelay || 1000;
    this.maxDelay = options.maxDelay || 30000;
    this.requestCount = 0;
    this.lastRequestTime = 0;
    this.minRequestInterval = 100;
  }

  static setApiKey(apiKey) {
    return ApiKeyManager.setApiKey(apiKey);
  }

  static getApiKey() {
    return ApiKeyManager.getApiKey();
  }

  static hasApiKey() {
    return ApiKeyManager.hasApiKey();
  }

  static RateLimitError = RateLimitError;

  _getHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    };

    let key = this.apiKey;
    if (!key) {
      try {
        key = ApiKeyManager.getApiKey();
      } catch (error) {
        if (error instanceof ApiKeyError) {
          throw error;
        }
      }
    }

    if (key) {
      headers['x-api-key'] = key;
    }

    return headers;
  }

  async _wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async _exponentialBackoff(attempt, retryAfter = null) {
    const baseDelay = retryAfter ? retryAfter * 1000 : this.baseDelay;
    const delay = Math.min(baseDelay * Math.pow(2, attempt), this.maxDelay);
    const jitter = Math.random() * 0.3 * delay;
    await this._wait(delay + jitter);
  }

  async _request(method, endpoint, body = null, params = null, retryCount = 0) {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    if (timeSinceLastRequest < this.minRequestInterval) {
      await this._wait(this.minRequestInterval - timeSinceLastRequest);
    }
    this.lastRequestTime = Date.now();

    const url = new URL(`${this.baseUrl}${endpoint}`);

    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== undefined && params[key] !== null) {
          url.searchParams.append(key, params[key]);
        }
      });
    }

    const options = {
      method,
      headers: this._getHeaders()
    };

    if (body && (method === 'POST' || method === 'DELETE' || method === 'PUT')) {
      options.body = JSON.stringify(body);
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);
    options.signal = controller.signal;

    try {
      const response = await fetch(url.toString(), options);
      clearTimeout(timeoutId);

      const contentType = response.headers.get('content-type');
      let data;
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      if (response.status === 429) {
        const retryAfter = response.headers.get('retry-after');
        const waitTime = retryAfter ? parseInt(retryAfter, 10) : null;
        
        if (retryCount < this.maxRetries) {
          console.log(`⚠️ Rate limit hit. Retry ${retryCount + 1}/${this.maxRetries} in ${waitTime || this.baseDelay}ms...`);
          await this._exponentialBackoff(retryCount, waitTime);
          return this._request(method, endpoint, body, params, retryCount + 1);
        }
        throw new RateLimitError(waitTime || 1);
      }

      if (!response.ok) {
        const errorMessage = data.message || data.error || `HTTP ${response.status}`;
        const errorCode = data.code || `HTTP_${response.status}`;
        throw new JupiterPredictionError(errorMessage, response.status, errorCode);
      }

      this.requestCount++;
      return data;
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === 'AbortError') {
        throw new JupiterPredictionError('Request timeout', 408, 'TIMEOUT');
      }

      if (error instanceof RateLimitError) {
        throw error;
      }

      if (error instanceof JupiterPredictionError || error instanceof ApiKeyError) {
        throw error;
      }

      if (retryCount < this.maxRetries && error.message.includes('network')) {
        console.log(`⚠️ Network error. Retry ${retryCount + 1}/${this.maxRetries}...`);
        await this._exponentialBackoff(retryCount);
        return this._request(method, endpoint, body, params, retryCount + 1);
      }

      throw new JupiterPredictionError(error.message, 0, 'NETWORK_ERROR');
    }
  }

  get(endpoint, params = null) {
    return this._request('GET', endpoint, null, params);
  }

  post(endpoint, body = null, params = null) {
    return this._request('POST', endpoint, body, params);
  }

  delete(endpoint, body = null, params = null) {
    return this._request('DELETE', endpoint, body, params);
  }

  getStats() {
    return {
      requestCount: this.requestCount,
      lastRequestTime: this.lastRequestTime
    };
  }

  resetStats() {
    this.requestCount = 0;
    this.lastRequestTime = 0;
  }
}

module.exports = { JupiterPredictionClient, JupiterPredictionError, RateLimitError, ApiKeyError };
