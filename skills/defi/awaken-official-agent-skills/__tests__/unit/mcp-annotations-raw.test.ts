import { afterEach, describe, expect, test } from 'bun:test';
import { spawn, type ChildProcessWithoutNullStreams } from 'node:child_process';

type RawTool = {
  name: string;
  annotations?: Record<string, unknown>;
};

async function waitForResponse(
  proc: ChildProcessWithoutNullStreams,
  messages: any[],
  stderrState: { value: string },
): Promise<any> {
  const deadline = Date.now() + 3000;

  while (Date.now() < deadline) {
    const response = messages.find(message => message?.id === 2);
    if (response) return response;
    if (proc.exitCode !== null) {
      throw new Error(`MCP server exited before tools/list response. stderr: ${stderrState.value}`);
    }
    await Bun.sleep(20);
  }

  throw new Error(`Timed out waiting for tools/list response. stderr: ${stderrState.value}`);
}

function killProcess(proc: ChildProcessWithoutNullStreams): void {
  if (proc.exitCode === null) {
    proc.kill();
  }
}

describe('MCP raw annotation contract', () => {
  let procToKill: ChildProcessWithoutNullStreams | null = null;

  afterEach(() => {
    if (procToKill) {
      killProcess(procToKill);
      procToKill = null;
    }
  });

  test('raw tools/list includes both camelCase and snake_case approval hints', async () => {
    const proc = spawn('bun', ['run', 'src/mcp/server.ts'], {
      cwd: process.cwd(),
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    procToKill = proc;

    const messages: any[] = [];
    let stdoutBuffer = '';
    const stderrState = { value: '' };

    proc.stdout.on('data', chunk => {
      stdoutBuffer += chunk.toString();
      while (true) {
        const newlineIndex = stdoutBuffer.indexOf('\n');
        if (newlineIndex < 0) break;
        const line = stdoutBuffer.slice(0, newlineIndex).trim();
        stdoutBuffer = stdoutBuffer.slice(newlineIndex + 1);
        if (!line) continue;
        messages.push(JSON.parse(line));
      }
    });

    proc.stderr.on('data', chunk => {
      stderrState.value += chunk.toString();
    });

    const send = (payload: unknown) => {
      proc.stdin.write(`${JSON.stringify(payload)}\n`);
    };

    send({
      jsonrpc: '2.0',
      id: 1,
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        capabilities: {
          roots: { listChanged: false },
          sampling: {},
        },
        clientInfo: {
          name: 'raw-annotations-test',
          version: '1.0.0',
        },
      },
    });
    send({ jsonrpc: '2.0', method: 'notifications/initialized' });
    send({ jsonrpc: '2.0', id: 2, method: 'tools/list' });

    const response = await waitForResponse(proc, messages, stderrState);
    const tools = response.result.tools as RawTool[];

    const readOnly = tools.find(tool => tool.name === 'awaken_quote');
    const networkWrite = tools.find(tool => tool.name === 'awaken_swap');

    expect(readOnly?.annotations?.readOnlyHint).toBe(true);
    expect(readOnly?.annotations?.read_only_hint).toBe(true);

    expect(networkWrite?.annotations?.destructiveHint).toBe(true);
    expect(networkWrite?.annotations?.destructive_hint).toBe(true);
    expect(networkWrite?.annotations?.openWorldHint).toBe(true);
    expect(networkWrite?.annotations?.side_effects_hint).toBe(true);
  });
});
