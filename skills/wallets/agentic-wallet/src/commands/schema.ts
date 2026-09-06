/**
 * Schema introspection command.
 * Returns machine-readable JSON describing what commands accept and return.
 * Allows agents to discover CLI capabilities at runtime.
 */

const SCHEMAS: Record<string, object> = {
  setup: {
    command: 'setup',
    description: 'Set up a new wallet with your chosen provider',
    options: {
      provider: { type: 'string', required: true, enum: ['coinbase', 'tempo', 'openwallet', 'crossmint'], description: 'Wallet provider' },
      chain: { type: 'string', required: false, default: 'base', enum: ['base', 'ethereum', 'arbitrum', 'optimism', 'polygon'], description: 'Target chain' },
      name: { type: 'string', required: false, default: 'default', description: 'Wallet name (openwallet only)' },
      'password-file': { type: 'string', required: false, description: 'Path to password file (non-interactive openwallet)' },
      'api-key-file': { type: 'string', required: false, description: 'Path to Crossmint API key file (non-interactive crossmint)' },
      'chain-type': { type: 'string', required: false, default: 'evm', enum: ['evm', 'solana', 'aptos', 'sui', 'stellar'], description: 'Crossmint chain type' },
      'wallet-type': { type: 'string', required: false, default: 'smart', enum: ['smart', 'mpc'], description: 'Crossmint wallet type' },
      'non-interactive': { type: 'boolean', required: false, description: 'Run without prompts' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: {
      type: 'object',
      fields: {
        ok: { type: 'boolean' },
        provider: { type: 'string' },
        name: { type: 'string' },
        address: { type: 'string' },
        chain: { type: 'string' },
        chainId: { type: 'number' }
      }
    },
    exitCodes: { 0: 'success', 1: 'general error', 4: 'provider not installed', 5: 'invalid input', 8: 'wallet already exists' },
    idempotent: false
  },
  balance: {
    command: 'balance',
    description: 'Check wallet balances across all providers',
    options: {
      all: { type: 'boolean', required: false, description: 'Check all providers at once' },
      provider: { type: 'string', required: false, enum: ['coinbase', 'tempo', 'openwallet', 'crossmint'], description: 'Check specific provider' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' },
      fields: { type: 'string', required: false, description: 'Comma-separated fields to include (e.g. address,balanceUSDC)' }
    },
    output: {
      type: 'array',
      items: {
        provider: { type: 'string' },
        name: { type: 'string' },
        address: { type: 'string' },
        chain: { type: 'string' },
        chainId: { type: 'number' },
        balanceUSDC: { type: 'string' },
        balanceETH: { type: 'string' },
        status: { type: 'string', enum: ['ok', 'error'] },
        error: { type: 'string', optional: true }
      }
    },
    exitCodes: { 0: 'success', 1: 'general error', 7: 'network error' },
    idempotent: true
  },
  status: {
    command: 'status',
    description: 'Check wallet authentication status',
    options: {
      provider: { type: 'string', required: false, enum: ['coinbase', 'tempo', 'openwallet', 'crossmint', 'all'], description: 'Provider to check (default: all)' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: {
      type: 'object',
      fields: {
        providers: {
          type: 'array', items: {
            provider: { type: 'string' },
            status: { type: 'string', enum: ['authenticated', 'not_authenticated', 'not_installed'] },
            address: { type: 'string', optional: true },
            wallets: { type: 'array', optional: true }
          }
        }
      }
    },
    exitCodes: { 0: 'success', 1: 'general error' },
    idempotent: true
  },
  fund: {
    command: 'fund',
    description: 'Get instructions to fund your wallet',
    options: {
      provider: { type: 'string', required: true, enum: ['coinbase', 'tempo', 'openwallet', 'crossmint'], description: 'Wallet provider' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: {
      type: 'object',
      fields: {
        provider: { type: 'string' },
        address: { type: 'string' },
        chain: { type: 'string' },
        fundingMethods: { type: 'array' }
      }
    },
    exitCodes: { 0: 'success', 2: 'not authenticated', 4: 'provider not installed' },
    idempotent: true
  },
  backup: {
    command: 'backup',
    description: 'Backup an OpenWallet to encrypted file',
    options: {
      name: { type: 'string', required: false, default: 'default', description: 'Wallet name to backup' },
      output: { type: 'string', required: false, description: 'Output directory for backup file' },
      'password-file': { type: 'string', required: false, description: 'Path to password file' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: {
      type: 'object',
      fields: {
        ok: { type: 'boolean' },
        file: { type: 'string' },
        wallet: { type: 'string' },
        address: { type: 'string' },
        createdAt: { type: 'string' }
      }
    },
    exitCodes: { 0: 'success', 3: 'wallet not found', 6: 'encryption error' },
    idempotent: true
  },
  recover: {
    command: 'recover',
    description: 'Recover an OpenWallet from backup or seed phrase',
    options: {
      from: { type: 'string', required: false, description: 'Path to backup file' },
      'seed-phrase': { type: 'boolean', required: false, description: 'Recover from 12-word seed phrase' },
      name: { type: 'string', required: false, default: 'recovered', description: 'Name for recovered wallet' },
      'password-file': { type: 'string', required: false, description: 'Path to password file' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: {
      type: 'object',
      fields: {
        ok: { type: 'boolean' },
        name: { type: 'string' },
        address: { type: 'string' },
        chain: { type: 'string' },
        chainId: { type: 'number' }
      }
    },
    exitCodes: { 0: 'success', 3: 'wallet/backup not found', 6: 'encryption error', 8: 'wallet already exists' },
    idempotent: false
  },
  providers: {
    command: 'providers',
    description: 'List available wallet providers and their features',
    options: {
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: {
      type: 'array',
      items: {
        id: { type: 'string' },
        name: { type: 'string' },
        company: { type: 'string' },
        type: { type: 'string' },
        features: { type: 'array' },
        setupCommand: { type: 'string' },
        docsUrl: { type: 'string' }
      }
    },
    exitCodes: { 0: 'success' },
    idempotent: true
  },
  'card status': {
    command: 'card status',
    description: 'Check MoonAgents Card status',
    options: { json: { type: 'boolean', required: false, description: 'Output as JSON' } },
    output: { type: 'object', fields: { ok: { type: 'boolean' }, provider: { type: 'string' }, cards: { type: 'array' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated', 4: 'MoonPay CLI not installed' },
    idempotent: true,
    prerequisite: 'npm install -g @moonpay/cli && mp login'
  },
  'card create': {
    command: 'card create',
    description: 'Issue a new MoonAgents virtual Mastercard (requires KYC)',
    options: { json: { type: 'boolean', required: false, description: 'Output as JSON' } },
    output: { type: 'object', fields: { ok: { type: 'boolean' }, provider: { type: 'string' }, card: { type: 'object' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated', 4: 'MoonPay CLI not installed' },
    idempotent: false,
    prerequisite: 'KYC verification must be completed first (card onboarding-start → card onboarding-finish)'
  },
  'card link-wallet': {
    command: 'card link-wallet',
    description: 'Link an onchain wallet to your card with a spending cap',
    options: {
      wallet: { type: 'string', required: true, description: 'Wallet name to link' },
      currency: { type: 'string', required: false, default: 'usdc', description: 'Stablecoin currency' },
      amount: { type: 'string', required: true, description: 'Spending cap in chosen currency' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: { type: 'object', fields: { ok: { type: 'boolean' }, wallet: { type: 'string' }, spendingCap: { type: 'string' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated', 5: 'invalid input' },
    idempotent: true
  },
  'card unlink-wallet': {
    command: 'card unlink-wallet',
    description: 'Revoke card access to a wallet (stops spending immediately)',
    options: {
      wallet: { type: 'string', required: true, description: 'Wallet name to unlink' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: { type: 'object', fields: { ok: { type: 'boolean' }, wallet: { type: 'string' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated' },
    idempotent: true
  },
  'card freeze': {
    command: 'card freeze',
    description: 'Freeze card — pause all transactions instantly',
    options: { json: { type: 'boolean', required: false, description: 'Output as JSON' } },
    output: { type: 'object', fields: { ok: { type: 'boolean' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated' },
    idempotent: true
  },
  'card unfreeze': {
    command: 'card unfreeze',
    description: 'Unfreeze card — re-enable transactions',
    options: { json: { type: 'boolean', required: false, description: 'Output as JSON' } },
    output: { type: 'object', fields: { ok: { type: 'boolean' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated' },
    idempotent: true
  },
  'card transactions': {
    command: 'card transactions',
    description: 'List card transactions',
    options: { json: { type: 'boolean', required: false, description: 'Output as JSON' } },
    output: { type: 'object', fields: { ok: { type: 'boolean' }, transactions: { type: 'array' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated' },
    idempotent: true
  },
  'card onboarding-start': {
    command: 'card onboarding-start',
    description: 'Start KYC identity verification (required before card issuance)',
    options: {
      'first-name': { type: 'string', required: true, description: 'First name' },
      'last-name': { type: 'string', required: true, description: 'Last name' },
      'country-of-residence': { type: 'string', required: true, description: 'ISO 3166-1 alpha-3 country code' },
      'country-of-nationality': { type: 'string', required: false, description: 'ISO 3166-1 alpha-3 country code' },
      'phone-country-code': { type: 'string', required: false, default: '+44', description: 'Phone country code' },
      'phone-number': { type: 'string', required: true, description: 'Phone number (digits only)' },
      'date-of-birth': { type: 'string', required: true, description: 'YYYY-MM-DD' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: { type: 'object', fields: { ok: { type: 'boolean' }, action: { type: 'string' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated', 5: 'invalid input' },
    idempotent: false
  },
  'card onboarding-check': {
    command: 'card onboarding-check',
    description: 'Check KYC verification status',
    options: { json: { type: 'boolean', required: false, description: 'Output as JSON' } },
    output: { type: 'object', fields: { ok: { type: 'boolean' }, status: { type: 'object' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated' },
    idempotent: true
  },
  'card onboarding-finish': {
    command: 'card onboarding-finish',
    description: 'Complete KYC by submitting address and accepting terms',
    options: {
      'address-line1': { type: 'string', required: true, description: 'Street address' },
      city: { type: 'string', required: true, description: 'City' },
      zip: { type: 'string', required: true, description: 'ZIP or postal code' },
      'accept-terms': { type: 'boolean', required: true, description: 'Accept terms and conditions' },
      json: { type: 'boolean', required: false, description: 'Output as JSON' }
    },
    output: { type: 'object', fields: { ok: { type: 'boolean' }, action: { type: 'string' } } },
    exitCodes: { 0: 'success', 1: 'general error', 2: 'not authenticated', 5: 'invalid input' },
    idempotent: false
  }
};

export async function schemaCommand(command?: string): Promise<void> {
  if (command) {
    const schema = SCHEMAS[command];
    if (!schema) {
      const error = { ok: false, error: { code: 5, message: `Unknown command: ${command}`, validCommands: Object.keys(SCHEMAS) } };
      process.stdout.write(JSON.stringify(error, null, 2) + '\n');
      process.exit(5);
    }
    process.stdout.write(JSON.stringify(schema, null, 2) + '\n');
  } else {
    const all = {
      cli: 'agent-wallet',
      version: '1.1.0',
      commands: SCHEMAS
    };
    process.stdout.write(JSON.stringify(all, null, 2) + '\n');
  }
}
