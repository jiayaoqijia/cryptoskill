import chalk from 'chalk';
import { isJsonMode, jsonOut } from '../utils/output.js';

interface ProvidersOptions {
  json?: boolean;
}

const PROVIDERS_DATA = [
  {
    id: 'coinbase',
    name: 'Coinbase Agentic Wallet',
    company: 'Coinbase',
    type: 'managed',
    storage: 'Coinbase infrastructure (keys never leave Coinbase)',
    features: [
      'Enterprise-grade compliance (KYT, OFAC screening)',
      'Spending guardrails and limits',
      'Native x402 payment support',
      'Email-based authentication'
    ],
    caveats: ['Requires email verification'],
    setupCommand: 'npx agentic-wallet setup --provider coinbase',
    docsUrl: 'https://docs.cdp.coinbase.com/agentic-wallet/welcome'
  },
  {
    id: 'tempo',
    name: 'Tempo Wallet',
    company: 'Stripe',
    type: 'passkey',
    storage: 'Local device + Tempo network',
    features: [
      '~500ms finality, sub-cent fees',
      'Built-in service discovery',
      'Machine Payments Protocol (MPP) support',
      'Passkey authentication (no passwords)'
    ],
    caveats: ['Requires browser for initial setup'],
    setupCommand: 'npx agentic-wallet setup --provider tempo',
    docsUrl: 'https://docs.tempo.xyz/guide/using-tempo-with-ai'
  },
  {
    id: 'openwallet',
    name: 'OpenWallet Standard',
    company: 'Moonpay',
    type: 'self-custody',
    storage: 'Encrypted on your local filesystem',
    features: [
      'Full control over keys',
      'No external accounts required',
      'Works offline',
      'AES-256-GCM encryption'
    ],
    caveats: ['You manage backups and security'],
    setupCommand: 'npx agentic-wallet setup --provider openwallet',
    docsUrl: 'https://docs.openwallet.sh/'
  },
  {
    id: 'crossmint',
    name: 'Crossmint Wallet',
    company: 'Crossmint',
    type: 'managed/api',
    storage: 'Crossmint infrastructure (custodial or non-custodial)',
    features: [
      '50+ chains supported (EVM + Solana + Stellar)',
      'REST API + TypeScript SDK for programmatic access',
      'Custodial and non-custodial wallet options',
      'Built-in transaction and signature management'
    ],
    caveats: ['Requires Crossmint account and API key'],
    setupCommand: 'npx agentic-wallet setup --provider crossmint',
    docsUrl: 'https://docs.crossmint.com/introduction/platform-overview'
  },
  {
    id: 'moonpay-card',
    name: 'MoonAgents Card',
    company: 'MoonPay + Monavate',
    type: 'spending/debit-card',
    storage: 'Self-custodial wallet — funds stay onchain until purchase',
    features: [
      'Virtual Mastercard debit card for AI agents',
      'Spend stablecoins at any online Mastercard merchant globally',
      'Funds stay in wallet until moment of purchase (no pre-loading)',
      'Programmable spending caps and instant freeze/revoke',
      'Full transaction logging for agent audit trails'
    ],
    caveats: [
      'Requires KYC identity verification (via Monavate)',
      'Currently available in UK and LATAM (US/EU planned)',
      'Requires MoonPay CLI (@moonpay/cli)'
    ],
    setupCommand: 'npx agentic-wallet card create',
    docsUrl: 'https://www.moonpay.com/agents/card'
  }
];

export async function providers(options: ProvidersOptions = {}): Promise<void> {
  if (isJsonMode(options)) {
    jsonOut(PROVIDERS_DATA);
    return;
  }

  console.log();
  console.log(chalk.bold('Available Wallet Providers'));
  console.log(chalk.gray('═'.repeat(70)));
  console.log();

  // Coinbase
  console.log(chalk.cyan.bold('1. COINBASE AGENTIC WALLET (by Coinbase)'));
  console.log(chalk.gray('   Type: Managed/Custodial'));
  console.log(chalk.gray('   Storage: Coinbase infrastructure (keys never leave Coinbase)'));
  console.log();
  console.log('   ' + chalk.green('✓') + ' Enterprise-grade compliance (KYT, OFAC screening)');
  console.log('   ' + chalk.green('✓') + ' Spending guardrails and limits');
  console.log('   ' + chalk.green('✓') + ' Native x402 payment support');
  console.log('   ' + chalk.green('✓') + ' Email-based authentication');
  console.log('   ' + chalk.yellow('⚠') + ' Requires email verification');
  console.log();
  console.log(chalk.gray('   Setup: npx agentic-wallet setup --provider coinbase'));
  console.log(chalk.gray('   Docs:  https://docs.cdp.coinbase.com/agentic-wallet/welcome'));
  console.log();

  // Tempo (Stripe)
  console.log(chalk.cyan.bold('2. TEMPO WALLET (by Stripe)'));
  console.log(chalk.gray('   Type: Passkey-based'));
  console.log(chalk.gray('   Storage: Local device + Tempo network'));
  console.log();
  console.log('   ' + chalk.green('✓') + ' ~500ms finality, sub-cent fees');
  console.log('   ' + chalk.green('✓') + ' Built-in service discovery');
  console.log('   ' + chalk.green('✓') + ' Machine Payments Protocol (MPP) support');
  console.log('   ' + chalk.green('✓') + ' Passkey authentication (no passwords)');
  console.log('   ' + chalk.yellow('⚠') + ' Requires browser for initial setup');
  console.log();
  console.log(chalk.gray('   Setup: npx agentic-wallet setup --provider tempo'));
  console.log(chalk.gray('   Docs:  https://docs.tempo.xyz/guide/using-tempo-with-ai'));
  console.log();

  // OpenWallet (Moonpay)
  console.log(chalk.cyan.bold('3. OPENWALLET STANDARD (by Moonpay)'));
  console.log(chalk.gray('   Type: Self-custody'));
  console.log(chalk.gray('   Storage: Encrypted on your local filesystem'));
  console.log();
  console.log('   ' + chalk.green('✓') + ' Full control over keys');
  console.log('   ' + chalk.green('✓') + ' No external accounts required');
  console.log('   ' + chalk.green('✓') + ' Works offline');
  console.log('   ' + chalk.green('✓') + ' AES-256-GCM encryption');
  console.log('   ' + chalk.yellow('⚠') + ' You manage backups and security');
  console.log();
  console.log(chalk.gray('   Setup: npx agentic-wallet setup --provider openwallet'));
  console.log(chalk.gray('   Docs:  https://docs.openwallet.sh/'));
  console.log();

  // Crossmint
  console.log(chalk.cyan.bold('4. CROSSMINT WALLET (by Crossmint)'));
  console.log(chalk.gray('   Type: Managed / API-first'));
  console.log(chalk.gray('   Storage: Crossmint infrastructure (custodial or non-custodial)'));
  console.log();
  console.log('   ' + chalk.green('✓') + ' 50+ chains supported (EVM + Solana + Stellar)');
  console.log('   ' + chalk.green('✓') + ' REST API + TypeScript SDK for programmatic access');
  console.log('   ' + chalk.green('✓') + ' Custodial and non-custodial wallet options');
  console.log('   ' + chalk.green('✓') + ' Built-in transaction and signature management');
  console.log('   ' + chalk.yellow('⚠') + ' Requires Crossmint account and API key');
  console.log();
  console.log(chalk.gray('   Setup: npx agentic-wallet setup --provider crossmint'));
  console.log(chalk.gray('   Docs:  https://docs.crossmint.com/introduction/platform-overview'));
  console.log();

  // MoonAgents Card (MoonPay)
  console.log(chalk.cyan.bold('5. MOONAGENTS CARD (by MoonPay + Monavate)'));
  console.log(chalk.gray('   Type: Spending / Debit Card'));
  console.log(chalk.gray('   Storage: Self-custodial — funds stay onchain until purchase'));
  console.log();
  console.log('   ' + chalk.green('✓') + ' Virtual Mastercard debit card for AI agents');
  console.log('   ' + chalk.green('✓') + ' Spend stablecoins at any online Mastercard merchant globally');
  console.log('   ' + chalk.green('✓') + ' Funds stay in wallet until moment of purchase (no pre-loading)');
  console.log('   ' + chalk.green('✓') + ' Programmable spending caps and instant freeze/revoke');
  console.log('   ' + chalk.green('✓') + ' Full transaction logging for agent audit trails');
  console.log('   ' + chalk.yellow('⚠') + ' Requires KYC identity verification (via Monavate)');
  console.log('   ' + chalk.yellow('⚠') + ' Currently available in UK and LATAM (US/EU planned)');
  console.log('   ' + chalk.yellow('⚠') + ' Requires MoonPay CLI: npm install -g @moonpay/cli');
  console.log();
  console.log(chalk.gray('   Setup: npx agentic-wallet card create'));
  console.log(chalk.gray('   Docs:  https://www.moonpay.com/agents/card'));
  console.log();

  console.log(chalk.gray('═'.repeat(70)));
  console.log();
  console.log(chalk.bold('Security Notice:'));
  console.log(chalk.white('  Agent Arena NEVER stores your private keys or credentials.'));
  console.log(chalk.white('  This CLI delegates to provider tools that store data locally.'));
  console.log(chalk.white('  All wallet data remains on YOUR machine or with YOUR chosen provider.'));
  console.log();
}
