import path from 'node:path';
import { buildCatalog, writeCatalogArtifacts } from './lib/catalog.ts';
import { maybePrintUpdateReminder } from './lib/update-check.ts';

interface CliOptions {
  workspacePath?: string;
  includeLocalPaths: boolean;
  outputPath?: string;
  syncReadme: boolean;
}

function parseArgValue(flag: string): string | undefined {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function hasFlag(flag: string): boolean {
  return process.argv.includes(flag);
}

function parseArgs(): CliOptions {
  return {
    workspacePath: parseArgValue('--workspace'),
    includeLocalPaths: hasFlag('--include-local-paths'),
    outputPath: parseArgValue('--output'),
    syncReadme: !hasFlag('--no-readme-sync'),
  };
}

async function main(): Promise<void> {
  try {
    await maybePrintUpdateReminder();

    const options = parseArgs();
    const rootDir = process.cwd();

    const catalog = buildCatalog({
      workspacePath: options.workspacePath,
      includeLocalPaths: options.includeLocalPaths,
    });

    writeCatalogArtifacts(catalog, {
      rootDir,
      outputPath: options.outputPath,
      syncReadme: options.syncReadme,
    });

    const finalOutputPath = options.outputPath
      ? path.resolve(rootDir, options.outputPath)
      : path.join(rootDir, 'skills-catalog.json');

    console.log(`[DONE] Generated catalog: ${finalOutputPath}`);
    console.log(`[INFO] Schema: ${catalog.schemaVersion}`);
    console.log(`[INFO] Skills: ${catalog.skills.length}`);
    console.log(`[INFO] Includes local paths: ${options.includeLocalPaths ? 'YES' : 'NO'}`);
    console.log(`[INFO] Readme sync: ${options.syncReadme ? 'YES' : 'NO'}`);

    if (catalog.warnings.length > 0) {
      console.log('[WARN] Non-blocking issues:');
      for (const warning of catalog.warnings) {
        console.log(`  - ${warning}`);
      }
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(message.startsWith('[FAIL]') ? message : `[FAIL] ${message}`);
    process.exitCode = 1;
  }
}

void main();
