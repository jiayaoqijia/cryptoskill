import { SkillError } from './src/core/errors.js';

export function parseJsonInput(input?: string): any {
  if (!input) return {};
  try {
    return JSON.parse(input);
  } catch (err) {
    throw new SkillError('INVALID_JSON', `invalid json input: ${String(err)}`);
  }
}

export function printResult(result: unknown): void {
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}
