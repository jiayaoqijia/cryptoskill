const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(process.cwd(), 'config');
const API_KEY_FILE = path.join(CONFIG_DIR, 'api-key.json');

class ApiKeyError extends Error {
  constructor(message, code = 'API_KEY_ERROR') {
    super(message);
    this.name = 'ApiKeyError';
    this.code = code;
  }
}

class ApiKeyManager {
  static getApiKey() {
    if (process.env.JUPITER_API_KEY) {
      return process.env.JUPITER_API_KEY;
    }

    if (fs.existsSync(API_KEY_FILE)) {
      try {
        const config = JSON.parse(fs.readFileSync(API_KEY_FILE, 'utf8'));
        if (config.jupiterApiKey && config.jupiterApiKey !== 'TU_API_KEY_AQUI') {
          return config.jupiterApiKey;
        }
      } catch (error) {
        throw new ApiKeyError(`Error reading API key file: ${error.message}`, 'FILE_READ_ERROR');
      }
    }

    throw new ApiKeyError(
      'API_KEY_REQUIRED: Configure your Jupiter API key using one of these methods:\n' +
      '1. Set JUPITER_API_KEY environment variable\n' +
      '2. Create config/api-key.json with {"jupiterApiKey": "your-key"}\n' +
      '3. Use JupiterPredictionClient.setApiKey("your-key")',
      'API_KEY_MISSING'
    );
  }

  static async setApiKey(apiKey) {
    if (!apiKey || typeof apiKey !== 'string') {
      throw new ApiKeyError('Invalid API key provided', 'INVALID_API_KEY');
    }

    if (!fs.existsSync(CONFIG_DIR)) {
      fs.mkdirSync(CONFIG_DIR, { recursive: true });
    }

    const trimmedKey = apiKey.trim();
    fs.writeFileSync(API_KEY_FILE, JSON.stringify({ jupiterApiKey: trimmedKey }, null, 2));
    return trimmedKey;
  }

  static hasApiKey() {
    if (process.env.JUPITER_API_KEY) {
      return true;
    }

    if (fs.existsSync(API_KEY_FILE)) {
      try {
        const config = JSON.parse(fs.readFileSync(API_KEY_FILE, 'utf8'));
        return !!(config.jupiterApiKey && config.jupiterApiKey !== 'TU_API_KEY_AQUI');
      } catch {
        return false;
      }
    }

    return false;
  }

  static removeApiKey() {
    if (fs.existsSync(API_KEY_FILE)) {
      fs.unlinkSync(API_KEY_FILE);
    }
  }

  static getApiKeyFromInput() {
    throw new ApiKeyError(
      'INTERACTIVE_MODE: Please provide your API key',
      'INTERACTIVE_INPUT_REQUIRED'
    );
  }
}

module.exports = { ApiKeyManager, ApiKeyError };
