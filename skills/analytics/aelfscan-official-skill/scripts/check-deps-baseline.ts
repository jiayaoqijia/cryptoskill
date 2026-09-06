#!/usr/bin/env bun
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { resolve } from 'node:path';
import Ajv from 'ajv';

type Baseline = {
  dependencies: Record<string, string>;
};

function readJson<T>(filePath: string): T {
  return JSON.parse(readFileSync(filePath, 'utf8')) as T;
}

function main() {
  const cwd = process.cwd();
  const baselinePath = resolve(cwd, 'deps-baseline.json');
  const packagePath = resolve(cwd, 'package.json');
  const contextSchemaPath = resolve(cwd, 'schemas', 'wallet-context.v1.schema.json');

  if (!existsSync(baselinePath)) {
    console.error(`[deps:check] missing deps-baseline.json at ${baselinePath}`);
    process.exit(1);
  }

  if (!existsSync(packagePath)) {
    console.error(`[deps:check] missing package.json at ${packagePath}`);
    process.exit(1);
  }

  const baseline = readJson<Baseline>(baselinePath);
  const pkg = readJson<any>(packagePath);
  const declaredDeps = {
    ...(pkg.dependencies || {}),
    ...(pkg.devDependencies || {}),
  } as Record<string, string>;

  const failures: string[] = [];
  for (const [name, expected] of Object.entries(baseline.dependencies || {})) {
    const actual = declaredDeps[name];
    if (!actual) {
      failures.push(`${name}: missing (expected ${expected})`);
      continue;
    }
    if (actual !== expected) {
      failures.push(`${name}: expected ${expected}, got ${actual}`);
    }
  }

  const contextPath =
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH ||
    resolve(homedir(), '.portkey', 'skill-wallet', 'context.v1.json');
  if (!existsSync(contextSchemaPath)) {
    failures.push(`missing wallet-context schema: ${contextSchemaPath}`);
  } else if (existsSync(contextPath)) {
    try {
      const schema = readJson<Record<string, unknown>>(contextSchemaPath);
      const contextRaw = readJson<Record<string, unknown>>(contextPath);
      const ajv = new Ajv({ allErrors: true, strict: false });
      const validate = ajv.compile(schema);
      if (!validate(contextRaw)) {
        const details = (validate.errors || [])
          .map((err) => `${err.instancePath || '/'} ${err.message || 'invalid'}`)
          .join('; ');
        failures.push(`wallet-context schema validation failed (${contextPath}): ${details}`);
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      failures.push(`wallet-context parse/validation failed: ${message}`);
    }
  }

  if (failures.length > 0) {
    console.error('[deps:check] check failed:');
    for (const failure of failures) {
      console.error(`- ${failure}`);
    }
    process.exit(1);
  }

  console.log('[deps:check] passed');
}

main();
