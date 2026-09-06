#!/usr/bin/env bun
import { Command } from 'commander';
import { ZodError } from 'zod';
import { CLI_TOOL_DESCRIPTOR_BY_KEY } from './src/tooling/tool-descriptors.js';

function parseInput(raw?: string): Record<string, unknown> {
  if (!raw) {
    return {};
  }

  try {
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      throw new Error('Input must be a JSON object.');
    }

    return parsed as Record<string, unknown>;
  } catch (error) {
    throw new Error(`Invalid --input JSON: ${(error as Error).message}`);
  }
}

async function runCommand(domain: string, action: string, inputRaw?: string): Promise<void> {
  const key = `${domain}.${action}`;
  const descriptor = CLI_TOOL_DESCRIPTOR_BY_KEY.get(key);

  if (!descriptor) {
    throw new Error(`Unsupported command: ${key}`);
  }

  const input = parseInput(inputRaw);
  const validatedInput = descriptor.parse(input);
  const result = await descriptor.handler(validatedInput);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);

  if (!result.success) {
    process.exitCode = 1;
  }
}

const program = new Command();
program
  .name('aelfscan-skill')
  .description('AelfScan skill CLI (search/blockchain/address/token/nft/statistics)')
  .argument('<domain>', 'search | blockchain | address | token | nft | statistics')
  .argument('<action>', 'action name under domain')
  .option('--input <json>', 'JSON input payload')
  .action(async (domain, action, options: { input?: string }) => {
    await runCommand(domain, action, options.input);
  });

program.parseAsync(process.argv).catch((error: unknown) => {
  if (error instanceof ZodError) {
    process.stderr.write(`[ERROR] Invalid input: ${error.message}\n`);
    process.exit(1);
    return;
  }

  process.stderr.write(`[ERROR] ${(error as Error).message}\n`);
  process.exit(1);
});
