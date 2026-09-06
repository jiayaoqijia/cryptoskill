import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';

export interface CommandResult {
  ok: boolean;
  code: number;
  stdout: string;
  stderr: string;
}

export function fileExists(target: string): boolean {
  return existsSync(target);
}

export function readJsonFile<T>(target: string): T {
  return JSON.parse(readFileSync(target, 'utf8')) as T;
}

export function writeJsonFile(target: string, value: unknown): void {
  const dir = path.dirname(target);
  mkdirSync(dir, { recursive: true });
  writeFileSync(target, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

export function runCommand(
  command: string,
  args: string[],
  cwd?: string,
  env?: Record<string, string>,
): CommandResult {
  const child = spawnSync(command, args, {
    cwd,
    env: env ? { ...process.env, ...env } : process.env,
    stdio: 'pipe',
    encoding: 'utf8',
  });

  return {
    ok: child.status === 0,
    code: child.status ?? 1,
    stdout: (child.stdout || '').toString().trim(),
    stderr: (child.stderr || '').toString().trim(),
  };
}

export function commandExists(command: string): boolean {
  const result = runCommand('which', [command]);
  return result.ok && result.stdout.length > 0;
}

export function normalizeRepoUrlToHttps(raw?: string): string | undefined {
  if (!raw) return undefined;
  const trimmed = raw.replace(/^git\+/, '').trim();

  if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
    return trimmed.replace(/^http:\/\//, 'https://');
  }

  const sshMatch = trimmed.match(/^git@([^:]+):(.+)$/);
  if (sshMatch) {
    return `https://${sshMatch[1]}/${sshMatch[2].replace(/^\//, '')}`;
  }

  if (trimmed.startsWith('ssh://git@')) {
    const withoutPrefix = trimmed.replace(/^ssh:\/\/git@/, '');
    const slashIndex = withoutPrefix.indexOf('/');
    if (slashIndex > 0) {
      const host = withoutPrefix.slice(0, slashIndex);
      const repoPath = withoutPrefix.slice(slashIndex + 1);
      return `https://${host}/${repoPath}`;
    }
  }

  return undefined;
}

export function parseFrontMatter(markdown: string): Record<string, string> {
  const match = markdown.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};

  const output: Record<string, string> = {};
  const lines = match[1].split(/\r?\n/);
  for (const line of lines) {
    const kv = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!kv) continue;
    output[kv[1]] = kv[2].replace(/^"|"$/g, '').trim();
  }
  return output;
}

export function extractFirstHeading(markdown: string): string {
  const heading = markdown.match(/^#\s+(.+)$/m);
  return heading ? heading[1].trim() : '';
}

export function extractSectionBullets(markdown: string, sectionTitle: string): string[] {
  const lines = markdown.split(/\r?\n/);
  const sectionPattern = new RegExp(`^##\\s+${escapeRegExp(sectionTitle)}\\s*$`, 'i');
  let inSection = false;
  const bullets: string[] = [];

  for (const line of lines) {
    if (!inSection && sectionPattern.test(line.trim())) {
      inSection = true;
      continue;
    }

    if (inSection && /^##\s+/.test(line.trim())) {
      break;
    }

    if (inSection) {
      const bullet = line.match(/^\s*[-*]\s+(.+)$/);
      if (bullet) {
        bullets.push(bullet[1].trim());
      }
    }
  }

  return bullets;
}

export function slugifyId(input: string): string {
  const noScope = input.replace(/^@/, '').replace('/', '-');
  return noScope
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, '-')
    .replace(/-{2,}/g, '-')
    .replace(/^-|-$/g, '');
}

export function parseCsv(input?: string): string[] {
  if (!input) return [];
  return input
    .split(',')
    .map(v => v.trim())
    .filter(Boolean);
}

export function requireCommand(command: string): void {
  if (!commandExists(command)) {
    throw new Error(`Required command not found: ${command}`);
  }
}

export function expandPathWithEnv(input: string): string {
  const missing = new Set<string>();
  const expanded = input.replace(/\$\{([A-Z0-9_]+)\}/g, (_match, envName: string) => {
    const value = process.env[envName];
    if (!value) {
      missing.add(envName);
      return '';
    }
    return value;
  });

  if (missing.size > 0) {
    throw new Error(
      `[FAIL] Unresolved environment variable(s) in path "${input}": ${Array.from(missing).join(', ')}`,
    );
  }

  return expanded;
}

export function replaceSection(
  source: string,
  startMarker: string,
  endMarker: string,
  content: string,
): string {
  const escapedStart = escapeRegExp(startMarker);
  const escapedEnd = escapeRegExp(endMarker);
  const pattern = new RegExp(`${escapedStart}[\\s\\S]*?${escapedEnd}`, 'm');
  const replacement = `${startMarker}\n${content}\n${endMarker}`;

  if (pattern.test(source)) {
    return source.replace(pattern, replacement);
  }

  return `${source.trimEnd()}\n\n${replacement}\n`;
}

function escapeRegExp(input: string): string {
  return input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
