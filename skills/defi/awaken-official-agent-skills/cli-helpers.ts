// ============================================================
// CLI Output Helpers - Used ONLY by CLI adapter layer
// ============================================================
// Core layer throws errors; CLI layer catches and formats output.

export function outputSuccess(data: any): void {
  console.log(JSON.stringify({ status: 'success', data }, null, 2));
}

export function outputError(message: string): never {
  console.error(`[ERROR] ${message}`);
  process.exit(1);
}
