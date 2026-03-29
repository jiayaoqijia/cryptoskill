import { z } from 'zod';

// ============================================================================
// Environment Variable Schema
// ============================================================================

const EnvSchema = z.object({
  // API Configuration
  ELSA_API_URL: z
    .string()
    .url()
    .default('https://x402-api.heyelsa.ai'),
  BASE_RPC_URL: z
    .string()
    .url()
    .default('https://mainnet.base.org'),

  // Wallet Keys
  PAYMENT_PRIVATE_KEY: z
    .string()
    .regex(/^0x[a-fA-F0-9]{64}$/, 'PAYMENT_PRIVATE_KEY must be a valid hex private key with 0x prefix'),
  TRADE_PRIVATE_KEY: z
    .string()
    .regex(/^0x[a-fA-F0-9]{64}$/, 'TRADE_PRIVATE_KEY must be a valid hex private key with 0x prefix')
    .optional(),

  // Budget Configuration
  ELSA_MAX_USD_PER_CALL: z
    .string()
    .transform((v) => parseFloat(v))
    .pipe(z.number().positive())
    .default('0.05'),
  ELSA_MAX_USD_PER_DAY: z
    .string()
    .transform((v) => parseFloat(v))
    .pipe(z.number().positive())
    .default('2.00'),
  ELSA_MAX_CALLS_PER_MINUTE: z
    .string()
    .transform((v) => parseInt(v, 10))
    .pipe(z.number().int().positive())
    .default('30'),
  ELSA_TZ: z
    .string()
    .default('UTC'),

  // Execution Gate
  ELSA_ENABLE_EXECUTION_TOOLS: z
    .string()
    .transform((v) => v === 'true')
    .default('false'),
  ELSA_REQUIRE_CONFIRMATION_TOKEN: z
    .string()
    .transform((v) => v === 'true')
    .default('true'),
  ELSA_CONFIRMATION_TTL_SECONDS: z
    .string()
    .transform((v) => parseInt(v, 10))
    .pipe(z.number().int().positive())
    .default('600'),

  // Logging
  ELSA_AUDIT_LOG_PATH: z
    .string()
    .optional(),
  LOG_LEVEL: z
    .enum(['debug', 'info', 'warn', 'error'])
    .default('info'),
});

export type EnvConfig = z.infer<typeof EnvSchema>;

// ============================================================================
// Parse and Validate Environment
// ============================================================================

let cachedConfig: EnvConfig | null = null;

export function getConfig(): EnvConfig {
  if (cachedConfig) {
    return cachedConfig;
  }

  const result = EnvSchema.safeParse(process.env);

  if (!result.success) {
    const errors = result.error.errors.map(
      (e) => `  ${e.path.join('.')}: ${e.message}`
    );
    throw new Error(
      `Environment validation failed:\n${errors.join('\n')}\n\nRequired: PAYMENT_PRIVATE_KEY`
    );
  }

  cachedConfig = result.data;

  // Default TRADE_PRIVATE_KEY to PAYMENT_PRIVATE_KEY if not set
  if (!cachedConfig.TRADE_PRIVATE_KEY) {
    cachedConfig.TRADE_PRIVATE_KEY = cachedConfig.PAYMENT_PRIVATE_KEY;
  }

  return cachedConfig;
}

// ============================================================================
// Helper Functions
// ============================================================================

export function isExecutionEnabled(): boolean {
  return getConfig().ELSA_ENABLE_EXECUTION_TOOLS;
}

export function isConfirmationRequired(): boolean {
  return getConfig().ELSA_REQUIRE_CONFIRMATION_TOKEN;
}

export function getConfirmationTtlMs(): number {
  return getConfig().ELSA_CONFIRMATION_TTL_SECONDS * 1000;
}
