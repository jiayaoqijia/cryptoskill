import path from 'node:path';
import { existsSync } from 'node:fs';
import type { SkillsCatalog } from './lib/types.ts';
import { readJsonFile } from './lib/utils.ts';

interface CliOptions {
  catalogPath: string;
}

interface SecurityIssue {
  skillId: string;
  field: string;
  command: string;
  rule: string;
}

const RISK_PATTERNS: Array<{ name: string; regex: RegExp }> = [
  { name: 'curl/wget piped to shell', regex: /\b(curl|wget)\b[^\n|]*\|\s*(bash|sh|zsh|pwsh|powershell)\b/i },
  { name: 'explicit shell -c execution', regex: /\b(bash|sh|zsh|pwsh|powershell)\s+-c\b/i },
  { name: 'command substitution using $(...)', regex: /\$\([^\n)]*\)/ },
  { name: 'command substitution using backticks', regex: /`[^`]+`/ },
  { name: 'multi-command chain with semicolon', regex: /;\s*\S+/ },
];

function parseArgs(): CliOptions {
  const args = process.argv.slice(2);
  let catalogPath = path.resolve(process.cwd(), 'skills-catalog.json');

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--catalog' && args[i + 1]) {
      catalogPath = path.resolve(process.cwd(), args[i + 1]);
      i += 1;
    }
  }

  return { catalogPath };
}

function collectIssues(catalog: SkillsCatalog): SecurityIssue[] {
  const issues: SecurityIssue[] = [];

  for (const skill of catalog.skills) {
    const commandEntries = Object.entries(skill.setupCommands || {});
    for (const [field, command] of commandEntries) {
      for (const pattern of RISK_PATTERNS) {
        if (pattern.regex.test(command)) {
          issues.push({
            skillId: skill.id,
            field,
            command,
            rule: pattern.name,
          });
          break;
        }
      }
    }

    const installEntries = Object.entries(skill.clientInstall || {})
      .map(([field, config]) => [field, config?.installCommand] as const)
      .filter(([, command]): command is string => typeof command === 'string' && command.length > 0);

    for (const [field, command] of installEntries) {
      for (const pattern of RISK_PATTERNS) {
        if (pattern.regex.test(command)) {
          issues.push({
            skillId: skill.id,
            field: `clientInstall.${field}.installCommand`,
            command,
            rule: pattern.name,
          });
          break;
        }
      }
    }
  }

  return issues;
}

function main(): void {
  try {
    const options = parseArgs();
    if (!existsSync(options.catalogPath)) {
      throw new Error(`[FAIL] Catalog file not found: ${options.catalogPath}`);
    }

    const catalog = readJsonFile<SkillsCatalog>(options.catalogPath);
    const issues = collectIssues(catalog);

    if (issues.length === 0) {
      console.log(`[OK] Security audit passed for ${catalog.skills.length} skill(s).`);
      return;
    }

    console.error(`[FAIL] Security audit found ${issues.length} risky setup command(s):`);
    for (const issue of issues) {
      console.error(`  - ${issue.skillId}.${issue.field}: ${issue.rule} -> ${issue.command}`);
    }
    process.exitCode = 1;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(message.startsWith('[FAIL]') ? message : `[FAIL] ${message}`);
    process.exitCode = 1;
  }
}

main();
