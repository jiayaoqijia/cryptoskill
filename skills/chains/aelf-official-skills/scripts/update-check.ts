import { checkForUpdates, renderHumanSummary } from './lib/update-check.ts';

interface CliOptions {
  force: boolean;
  quiet: boolean;
  json: boolean;
}

function parseArgs(): CliOptions {
  const args = process.argv.slice(2);
  return {
    force: args.includes('--force'),
    quiet: args.includes('--quiet'),
    json: args.includes('--json'),
  };
}

async function main(): Promise<void> {
  try {
    const options = parseArgs();
    const result = await checkForUpdates({
      force: options.force,
      allowWhenDisabled: true,
    });

    if (!result) {
      if (!options.quiet) {
        console.log('[INFO] Update check disabled by environment configuration.');
      }
      return;
    }

    if (options.json) {
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    if (options.quiet && !result.hasUpdates) {
      return;
    }

    console.log(renderHumanSummary(result));
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(message.startsWith('[FAIL]') ? message : `[FAIL] ${message}`);
    process.exitCode = 1;
  }
}

void main();
