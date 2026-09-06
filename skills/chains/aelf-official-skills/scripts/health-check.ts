import path from 'node:path';
import { existsSync } from 'node:fs';
import type { SkillsCatalog } from './lib/types.ts';
import { readJsonFile, parseCsv, writeJsonFile } from './lib/utils.ts';
import { buildCatalog, writeCatalogArtifacts } from './lib/catalog.ts';
import { printHealthReport, runHealthCheck } from './lib/health.ts';
import { maybePrintUpdateReminder } from './lib/update-check.ts';

interface CliOptions {
  catalogPath: string;
  skillsRoot?: string;
  onlyIds: string[];
}

function parseArgs(): CliOptions {
  const args = process.argv.slice(2);
  let catalogPath = path.resolve(process.cwd(), 'skills-catalog.json');
  let skillsRoot: string | undefined;
  let only = '';

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--catalog' && args[i + 1]) {
      catalogPath = path.resolve(process.cwd(), args[i + 1]);
      i += 1;
      continue;
    }

    if (arg === '--skills-root' && args[i + 1]) {
      skillsRoot = path.resolve(process.cwd(), args[i + 1]);
      i += 1;
      continue;
    }

    if (arg === '--only' && args[i + 1]) {
      only = args[i + 1];
      i += 1;
      continue;
    }
  }

  return {
    catalogPath,
    skillsRoot,
    onlyIds: parseCsv(only),
  };
}

function ensureCatalog(catalogPath: string): void {
  if (existsSync(catalogPath)) return;
  console.log(`[INFO] ${catalogPath} not found. Generating from workspace.json ...`);
  const catalog = buildCatalog();
  const defaultCatalogPath = path.join(process.cwd(), 'skills-catalog.json');
  if (path.resolve(catalogPath) === path.resolve(defaultCatalogPath)) {
    writeCatalogArtifacts(catalog, { rootDir: process.cwd() });
    return;
  }

  writeJsonFile(catalogPath, catalog);
}

async function main(): Promise<void> {
  try {
    await maybePrintUpdateReminder();

    const options = parseArgs();
    ensureCatalog(options.catalogPath);

    const inputCatalog = readJsonFile<SkillsCatalog>(options.catalogPath);

    // When --skills-root is not provided, health-check uses local-path mode generated from workspace.json,
    // so public catalogs can safely omit sourcePath.
    let checkCatalog = inputCatalog;
    let onlyIds = options.onlyIds;

    if (!options.skillsRoot) {
      const hasSourcePath = inputCatalog.skills.every(skill => Boolean(skill.sourcePath));
      if (!hasSourcePath) {
        checkCatalog = buildCatalog({ includeLocalPaths: true });
        if (onlyIds.length === 0) {
          onlyIds = inputCatalog.skills.map(skill => skill.id);
        }
      }
    }

    const report = runHealthCheck(checkCatalog, {
      skillsRoot: options.skillsRoot,
      onlyIds,
    });

    printHealthReport(report);

    if (report.summary.fail > 0) {
      process.exitCode = 1;
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(message.startsWith('[FAIL]') ? message : `[FAIL] ${message}`);
    process.exitCode = 1;
  }
}

void main();
