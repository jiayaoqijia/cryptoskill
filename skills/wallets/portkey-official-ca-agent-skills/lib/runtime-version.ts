import * as fs from 'node:fs';

const PACKAGE_JSON_URL = new URL('../package.json', import.meta.url);

function readRuntimeSkillVersion(): string {
  try {
    const raw = fs.readFileSync(PACKAGE_JSON_URL, 'utf8');
    const parsed = JSON.parse(raw) as { version?: string };
    return parsed.version || '0.0.0';
  } catch {
    return '0.0.0';
  }
}

export const RUNTIME_SKILL_VERSION = readRuntimeSkillVersion();
