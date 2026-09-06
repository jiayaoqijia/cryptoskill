import path from 'node:path';
import { existsSync, readFileSync } from 'node:fs';
import type { SkillsCatalog } from './lib/types.ts';
import { readJsonFile } from './lib/utils.ts';

const EN_PATH = path.join(process.cwd(), 'README.md');
const ZH_PATH = path.join(process.cwd(), 'README.zh-CN.md');
const CATALOG_PATH = path.join(process.cwd(), 'skills-catalog.json');

function ensureContains(readmePath: string, catalog: SkillsCatalog): string[] {
  if (!existsSync(readmePath)) return [`${readmePath} not found`];
  const content = readFileSync(readmePath, 'utf8');
  const missing: string[] = [];

  for (const skill of catalog.skills) {
    if (!content.includes(`| ${skill.id} |`)) {
      missing.push(`${readmePath}: missing table row for ${skill.id}`);
    }
  }

  return missing;
}

function main(): void {
  if (!existsSync(CATALOG_PATH)) {
    console.error('[ERROR] skills-catalog.json not found. Run `bun run catalog:generate` first.');
    process.exit(1);
  }

  const catalog = readJsonFile<SkillsCatalog>(CATALOG_PATH);
  const issues = [...ensureContains(EN_PATH, catalog), ...ensureContains(ZH_PATH, catalog)];

  if (issues.length > 0) {
    console.error('[ERROR] README/catalog consistency check failed:');
    for (const issue of issues) {
      console.error(`  - ${issue}`);
    }
    process.exit(1);
  }

  console.log('[OK] README files are in sync with skills-catalog.json');
}

main();
