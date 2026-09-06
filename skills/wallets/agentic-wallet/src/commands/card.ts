import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { execSync, spawn } from 'child_process';
import { isJsonMode, jsonOut, jsonError, ExitCode } from '../utils/output.js';

interface CardOptions {
  json?: boolean;
}

interface CardCreateOptions extends CardOptions {}

interface CardOnboardingOptions extends CardOptions {
  firstName?: string;
  lastName?: string;
  countryOfResidence?: string;
  countryOfNationality?: string;
  phoneCountryCode?: string;
  phoneNumber?: string;
  dateOfBirth?: string;
}

interface CardOnboardingFinishOptions extends CardOptions {
  addressLine1?: string;
  city?: string;
  zip?: string;
  acceptTerms?: boolean;
}

interface CardLinkOptions extends CardOptions {
  wallet?: string;
  currency?: string;
  amount?: string;
}

interface CardUnlinkOptions extends CardOptions {
  wallet?: string;
}

interface CardTransactionsOptions extends CardOptions {
  limit?: string;
}

const SUPPORTED_REGIONS = ['UK', 'LATAM'];
const PLANNED_REGIONS = ['US', 'EU'];

function findMpCli(): string {
  try {
    execSync('which mp', { stdio: 'pipe' });
    return 'mp';
  } catch {
    try {
      execSync('npx @moonpay/cli --version', { stdio: 'pipe', timeout: 15000 });
      return 'npx @moonpay/cli';
    } catch {
      return '';
    }
  }
}

function requireMpCli(useJson: boolean): string {
  const mpCmd = findMpCli();
  if (!mpCmd) {
    if (useJson) {
      jsonError(ExitCode.PROVIDER_NOT_INSTALLED, 'MoonPay CLI (@moonpay/cli) is not installed', {
        installCommand: 'npm install -g @moonpay/cli',
        docsUrl: 'https://www.moonpay.com/agents/card'
      });
    }
    console.error(chalk.red('MoonPay CLI (@moonpay/cli) is not installed.'));
    console.log();
    console.log(chalk.yellow('Install it with:'));
    console.log(chalk.white('  npm install -g @moonpay/cli'));
    console.log();
    console.log(chalk.gray('Then authenticate:'));
    console.log(chalk.white('  mp login'));
    console.log();
    console.log(chalk.gray('Docs: https://www.moonpay.com/agents/card'));
    process.exit(ExitCode.PROVIDER_NOT_INSTALLED);
  }
  return mpCmd;
}

function checkMpAuth(mpCmd: string): boolean {
  try {
    const result = execSync(`${mpCmd} user retrieve 2>/dev/null`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 10000
    });
    return !result.includes('Token refresh failed') && !result.includes('not logged in');
  } catch {
    return false;
  }
}

function requireMpAuth(mpCmd: string, useJson: boolean): void {
  if (!checkMpAuth(mpCmd)) {
    if (useJson) {
      jsonError(ExitCode.NOT_AUTHENTICATED, 'Not authenticated with MoonPay CLI. Run: mp login');
    }
    console.error(chalk.red('Not authenticated with MoonPay CLI.'));
    console.log();
    console.log(chalk.yellow('Run the following to authenticate:'));
    console.log(chalk.white('  mp login'));
    console.log();
    process.exit(ExitCode.NOT_AUTHENTICATED);
  }
}

function runMpCommand(mpCmd: string, args: string, useJson: boolean): string {
  try {
    return execSync(`${mpCmd} ${args}`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 30000
    }).trim();
  } catch (error: any) {
    const stderr = error.stderr?.toString().trim() || '';
    const stdout = error.stdout?.toString().trim() || '';
    const msg = stderr || stdout || error.message || 'Command failed';
    if (useJson) {
      jsonError(ExitCode.GENERAL_ERROR, msg, { command: `${mpCmd} ${args}` });
    }
    console.error(chalk.red(`Command failed: mp ${args}`));
    console.error(chalk.gray(msg));
    process.exit(ExitCode.GENERAL_ERROR);
  }
}

export async function cardStatus(options: CardOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  const spinner = useJson ? null : ora('Checking MoonAgents Card status...').start();

  try {
    const output = runMpCommand(mpCmd, 'card retrieve', useJson);

    spinner?.succeed('MoonAgents Card status retrieved');

    if (useJson) {
      try {
        const parsed = JSON.parse(output);
        jsonOut({ ok: true, provider: 'moonpay-card', cards: parsed });
      } catch {
        jsonOut({ ok: true, provider: 'moonpay-card', raw: output });
      }
    } else {
      console.log();
      console.log(chalk.bold('MoonAgents Card Status'));
      console.log(chalk.gray('─'.repeat(50)));
      console.log();
      if (output) {
        console.log(output);
      } else {
        console.log(chalk.yellow('No cards found. Create one with:'));
        console.log(chalk.white('  npx agentic-wallet card create'));
      }
      console.log();
    }
  } catch (error: any) {
    spinner?.fail('Failed to check card status');
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, error.message || 'Failed to check card status');
    console.error(chalk.red(error.message || 'Failed to check card status'));
    process.exit(ExitCode.GENERAL_ERROR);
  }
}

export async function cardOnboardingStart(options: CardOnboardingOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  if (!useJson) {
    console.log();
    console.log(chalk.bold('MoonAgents Card — Identity Verification (KYC)'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log(chalk.white('Card issuance requires identity verification through Monavate.'));
    console.log(chalk.gray(`Currently available in: ${SUPPORTED_REGIONS.join(', ')}`));
    console.log(chalk.gray(`Planned: ${PLANNED_REGIONS.join(', ')}`));
    console.log();
  }

  let { firstName, lastName, countryOfResidence, countryOfNationality,
        phoneCountryCode, phoneNumber, dateOfBirth } = options;

  if (!firstName || !lastName || !countryOfResidence || !phoneNumber || !dateOfBirth) {
    if (useJson) {
      jsonError(ExitCode.INVALID_INPUT, 'All onboarding fields are required in JSON mode', {
        required: ['firstName', 'lastName', 'countryOfResidence', 'countryOfNationality', 'phoneCountryCode', 'phoneNumber', 'dateOfBirth']
      });
    }

    const answers = await inquirer.prompt([
      ...(!firstName ? [{
        type: 'input' as const,
        name: 'firstName',
        message: 'First name:',
        validate: (v: string) => v.length > 0 || 'Required'
      }] : []),
      ...(!lastName ? [{
        type: 'input' as const,
        name: 'lastName',
        message: 'Last name:',
        validate: (v: string) => v.length > 0 || 'Required'
      }] : []),
      ...(!countryOfResidence ? [{
        type: 'input' as const,
        name: 'countryOfResidence',
        message: 'Country of residence (ISO 3166-1 alpha-3, e.g. GBR):',
        validate: (v: string) => /^[A-Z]{3}$/.test(v) || 'Use 3-letter country code (e.g. GBR, BRA)'
      }] : []),
      ...(!countryOfNationality ? [{
        type: 'input' as const,
        name: 'countryOfNationality',
        message: 'Country of nationality (ISO 3166-1 alpha-3, e.g. GBR):',
        validate: (v: string) => /^[A-Z]{3}$/.test(v) || 'Use 3-letter country code (e.g. GBR, BRA)'
      }] : []),
      ...(!phoneCountryCode ? [{
        type: 'input' as const,
        name: 'phoneCountryCode',
        message: 'Phone country code (e.g. +44):',
        validate: (v: string) => /^\+\d{1,4}$/.test(v) || 'Use format: +44, +1, +55'
      }] : []),
      ...(!phoneNumber ? [{
        type: 'input' as const,
        name: 'phoneNumber',
        message: 'Phone number (digits only):',
        validate: (v: string) => /^\d{6,15}$/.test(v) || 'Enter digits only (6-15 digits)'
      }] : []),
      ...(!dateOfBirth ? [{
        type: 'input' as const,
        name: 'dateOfBirth',
        message: 'Date of birth (YYYY-MM-DD):',
        validate: (v: string) => /^\d{4}-\d{2}-\d{2}$/.test(v) || 'Use format: YYYY-MM-DD'
      }] : [])
    ]);

    firstName = firstName || answers.firstName;
    lastName = lastName || answers.lastName;
    countryOfResidence = countryOfResidence || answers.countryOfResidence;
    countryOfNationality = countryOfNationality || answers.countryOfNationality;
    phoneCountryCode = phoneCountryCode || answers.phoneCountryCode;
    phoneNumber = phoneNumber || answers.phoneNumber;
    dateOfBirth = dateOfBirth || answers.dateOfBirth;
  }

  countryOfNationality = countryOfNationality || countryOfResidence;
  phoneCountryCode = phoneCountryCode || '+44';

  const spinner = useJson ? null : ora('Starting KYC onboarding...').start();

  const args = [
    'card onboarding start',
    `--firstName "${firstName}"`,
    `--lastName "${lastName}"`,
    `--countryOfResidence ${countryOfResidence}`,
    `--countryOfNationality ${countryOfNationality}`,
    `--phoneCountryCode ${phoneCountryCode}`,
    `--phoneNumber ${phoneNumber}`,
    `--dateOfBirth ${dateOfBirth}`
  ].join(' ');

  const output = runMpCommand(mpCmd, args, useJson);

  spinner?.succeed('KYC onboarding initiated');

  if (useJson) {
    jsonOut({ ok: true, provider: 'moonpay-card', action: 'onboarding-start', raw: output });
  } else {
    console.log();
    console.log(chalk.green('KYC onboarding started.'));
    if (output) console.log(chalk.gray(output));
    console.log();
    console.log(chalk.bold('Next steps:'));
    console.log('  1. Complete identity verification in the browser link provided');
    console.log('  2. Check status: npx agentic-wallet card onboarding-check');
    console.log('  3. Finish: npx agentic-wallet card onboarding-finish');
    console.log();
  }
}

export async function cardOnboardingCheck(options: CardOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  const spinner = useJson ? null : ora('Checking KYC onboarding status...').start();

  const output = runMpCommand(mpCmd, 'card onboarding check', useJson);

  spinner?.succeed('KYC status retrieved');

  if (useJson) {
    try {
      const parsed = JSON.parse(output);
      jsonOut({ ok: true, provider: 'moonpay-card', action: 'onboarding-check', status: parsed });
    } catch {
      jsonOut({ ok: true, provider: 'moonpay-card', action: 'onboarding-check', raw: output });
    }
  } else {
    console.log();
    console.log(chalk.bold('KYC Onboarding Status'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log(output);
    console.log();
  }
}

export async function cardOnboardingFinish(options: CardOnboardingFinishOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  let { addressLine1, city, zip, acceptTerms } = options;

  if (!addressLine1 || !city || !zip) {
    if (useJson) {
      jsonError(ExitCode.INVALID_INPUT, 'Address fields are required in JSON mode', {
        required: ['addressLine1', 'city', 'zip']
      });
    }

    const answers = await inquirer.prompt([
      ...(!addressLine1 ? [{
        type: 'input' as const,
        name: 'addressLine1',
        message: 'Street address:',
        validate: (v: string) => v.length > 0 || 'Required'
      }] : []),
      ...(!city ? [{
        type: 'input' as const,
        name: 'city',
        message: 'City:',
        validate: (v: string) => v.length > 0 || 'Required'
      }] : []),
      ...(!zip ? [{
        type: 'input' as const,
        name: 'zip',
        message: 'ZIP / Postal code:',
        validate: (v: string) => v.length > 0 || 'Required'
      }] : [])
    ]);

    addressLine1 = addressLine1 || answers.addressLine1;
    city = city || answers.city;
    zip = zip || answers.zip;
  }

  if (!acceptTerms) {
    if (useJson) {
      jsonError(ExitCode.INVALID_INPUT, '--accept-terms is required');
    }
    const { confirm } = await inquirer.prompt([{
      type: 'confirm',
      name: 'confirm',
      message: 'Do you accept the MoonAgents Card terms and conditions?\n  (https://www.exodus.com/legal/exodus-card-row-terms-202509.pdf)',
      default: false
    }]);
    if (!confirm) {
      console.log(chalk.gray('Onboarding cancelled — terms not accepted.'));
      return;
    }
  }

  const spinner = useJson ? null : ora('Completing KYC onboarding...').start();

  const args = [
    'card onboarding finish',
    `--addressLine1 "${addressLine1}"`,
    `--city ${city}`,
    `--zip "${zip}"`,
    '--acceptTerms true'
  ].join(' ');

  const output = runMpCommand(mpCmd, args, useJson);

  spinner?.succeed('KYC onboarding complete');

  if (useJson) {
    jsonOut({ ok: true, provider: 'moonpay-card', action: 'onboarding-finish', raw: output });
  } else {
    console.log();
    console.log(chalk.green('KYC onboarding complete!'));
    if (output) console.log(chalk.gray(output));
    console.log();
    console.log(chalk.bold('Next step:'));
    console.log('  Create your card: npx agentic-wallet card create');
    console.log();
  }
}

export async function cardCreate(options: CardCreateOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  if (!useJson) {
    console.log();
    console.log(chalk.bold('MoonAgents Card — Create Virtual Mastercard'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log(chalk.white('This issues a virtual Mastercard debit card through Monavate.'));
    console.log(chalk.white('Your stablecoins stay in your wallet until a purchase is made.'));
    console.log();
    console.log(chalk.gray(`Available in: ${SUPPORTED_REGIONS.join(', ')}`));
    console.log(chalk.gray(`Planned: ${PLANNED_REGIONS.join(', ')}`));
    console.log();
    console.log(chalk.yellow('Prerequisites:'));
    console.log(chalk.white('  - MoonPay account (mp login)'));
    console.log(chalk.white('  - KYC verification complete (npx agentic-wallet card onboarding-start)'));
    console.log();
  }

  const spinner = useJson ? null : ora('Issuing MoonAgents Card...').start();

  const output = runMpCommand(mpCmd, 'card create', useJson);

  spinner?.succeed('MoonAgents Card issued');

  if (useJson) {
    try {
      const parsed = JSON.parse(output);
      jsonOut({ ok: true, provider: 'moonpay-card', action: 'create', card: parsed });
    } catch {
      jsonOut({ ok: true, provider: 'moonpay-card', action: 'create', raw: output });
    }
  } else {
    console.log();
    console.log(chalk.green('MoonAgents Card issued successfully!'));
    console.log();
    if (output) console.log(output);
    console.log();
    console.log(chalk.bold('Next step:'));
    console.log('  Link a wallet: npx agentic-wallet card link-wallet --wallet <name> --amount 5000');
    console.log();
    console.log(chalk.bold('Security:'));
    console.log(chalk.white('  - Funds stay in your wallet until purchase'));
    console.log(chalk.white('  - Spending cap set when linking wallet'));
    console.log(chalk.white('  - Freeze anytime: npx agentic-wallet card freeze'));
    console.log(chalk.white('  - Revoke access: npx agentic-wallet card unlink-wallet'));
    console.log();
  }
}

export async function cardLinkWallet(options: CardLinkOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  let { wallet, currency, amount } = options;
  currency = currency || 'usdc';

  if (!wallet || !amount) {
    if (useJson) {
      jsonError(ExitCode.INVALID_INPUT, '--wallet and --amount are required', {
        example: 'npx agentic-wallet card link-wallet --wallet my-wallet --amount 5000'
      });
    }

    const answers = await inquirer.prompt([
      ...(!wallet ? [{
        type: 'input' as const,
        name: 'wallet',
        message: 'Wallet name to link:',
        validate: (v: string) => v.length > 0 || 'Required'
      }] : []),
      ...(!amount ? [{
        type: 'input' as const,
        name: 'amount',
        message: 'Spending cap (in USDC):',
        validate: (v: string) => {
          const num = parseFloat(v);
          return (!isNaN(num) && num > 0) || 'Enter a positive number';
        }
      }] : [])
    ]);

    wallet = wallet || answers.wallet;
    amount = amount || answers.amount;
  }

  const spinner = useJson ? null : ora(`Linking wallet "${wallet}" with ${amount} ${currency.toUpperCase()} spending cap...`).start();

  const args = `card wallet link --wallet ${wallet} --currency ${currency} --amount ${amount}`;
  const output = runMpCommand(mpCmd, args, useJson);

  spinner?.succeed(`Wallet "${wallet}" linked with ${amount} ${currency.toUpperCase()} spending cap`);

  if (useJson) {
    jsonOut({
      ok: true,
      provider: 'moonpay-card',
      action: 'link-wallet',
      wallet,
      currency: currency.toUpperCase(),
      spendingCap: amount,
      raw: output
    });
  } else {
    console.log();
    console.log(chalk.green(`Wallet "${wallet}" linked to your MoonAgents Card.`));
    console.log();
    console.log(`  Spending cap: ${chalk.cyan(amount + ' ' + currency.toUpperCase())}`);
    console.log();
    if (output) console.log(chalk.gray(output));
    console.log();
    console.log(chalk.gray('Update cap anytime: npx agentic-wallet card link-wallet --wallet <name> --amount <new-cap>'));
    console.log(chalk.gray('Revoke access:      npx agentic-wallet card unlink-wallet --wallet <name>'));
    console.log();
  }
}

export async function cardUnlinkWallet(options: CardUnlinkOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  let { wallet } = options;

  if (!wallet) {
    if (useJson) {
      jsonError(ExitCode.INVALID_INPUT, '--wallet is required');
    }

    const answers = await inquirer.prompt([{
      type: 'input',
      name: 'wallet',
      message: 'Wallet name to unlink:',
      validate: (v: string) => v.length > 0 || 'Required'
    }]);
    wallet = answers.wallet;
  }

  if (!useJson) {
    const { confirm } = await inquirer.prompt([{
      type: 'confirm',
      name: 'confirm',
      message: `Revoke card access to wallet "${wallet}"? This stops all spending immediately.`,
      default: false
    }]);
    if (!confirm) {
      console.log(chalk.gray('Cancelled.'));
      return;
    }
  }

  const spinner = useJson ? null : ora(`Unlinking wallet "${wallet}"...`).start();

  const output = runMpCommand(mpCmd, `card wallet unlink --wallet ${wallet} --currency usdc`, useJson);

  spinner?.succeed(`Wallet "${wallet}" unlinked — card can no longer spend from it`);

  if (useJson) {
    jsonOut({ ok: true, provider: 'moonpay-card', action: 'unlink-wallet', wallet, raw: output });
  } else {
    console.log();
    console.log(chalk.green(`Wallet "${wallet}" unlinked from your MoonAgents Card.`));
    console.log(chalk.white('Your agent can no longer spend from this wallet.'));
    console.log();
  }
}

export async function cardFreeze(options: CardOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  const spinner = useJson ? null : ora('Freezing MoonAgents Card...').start();

  const output = runMpCommand(mpCmd, 'card freeze', useJson);

  spinner?.succeed('MoonAgents Card frozen — all transactions paused');

  if (useJson) {
    jsonOut({ ok: true, provider: 'moonpay-card', action: 'freeze', raw: output });
  } else {
    console.log();
    console.log(chalk.green('MoonAgents Card frozen.'));
    console.log(chalk.white('All transactions are paused. Your wallet funds are untouched.'));
    console.log();
    console.log(chalk.gray('Unfreeze: npx agentic-wallet card unfreeze'));
    console.log();
  }
}

export async function cardUnfreeze(options: CardOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  const spinner = useJson ? null : ora('Unfreezing MoonAgents Card...').start();

  const output = runMpCommand(mpCmd, 'card unfreeze', useJson);

  spinner?.succeed('MoonAgents Card unfrozen — transactions re-enabled');

  if (useJson) {
    jsonOut({ ok: true, provider: 'moonpay-card', action: 'unfreeze', raw: output });
  } else {
    console.log();
    console.log(chalk.green('MoonAgents Card unfrozen.'));
    console.log(chalk.white('Transactions are re-enabled.'));
    console.log();
  }
}

export async function cardTransactions(options: CardTransactionsOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const mpCmd = requireMpCli(useJson);
  requireMpAuth(mpCmd, useJson);

  const spinner = useJson ? null : ora('Fetching card transactions...').start();

  const output = runMpCommand(mpCmd, 'card transaction list', useJson);

  spinner?.succeed('Card transactions retrieved');

  if (useJson) {
    try {
      const parsed = JSON.parse(output);
      jsonOut({ ok: true, provider: 'moonpay-card', action: 'transactions', transactions: parsed });
    } catch {
      jsonOut({ ok: true, provider: 'moonpay-card', action: 'transactions', raw: output });
    }
  } else {
    console.log();
    console.log(chalk.bold('MoonAgents Card Transactions'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    if (output) {
      console.log(output);
    } else {
      console.log(chalk.gray('No transactions yet.'));
    }
    console.log();
  }
}
