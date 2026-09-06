import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

type WorkspaceConfig = {
  projects: Array<{ path: string }>;
};

type SmokeStatus = 'pass' | 'fail' | 'skip';
type SmokeResult = {
  status: SmokeStatus;
  reason?: string;
  details?: Record<string, unknown>;
};

function readWorkspaceConfig(filePath: string): WorkspaceConfig {
  return JSON.parse(readFileSync(filePath, 'utf8')) as WorkspaceConfig;
}

function resolveWorkspacePath(raw: string, skillsBase: string): string {
  return resolve(raw.replace('${SKILLS_BASE}', skillsBase));
}

function findRepoPath(config: WorkspaceConfig, skillsBase: string, name: string): string | null {
  for (const entry of config.projects) {
    const candidate = resolveWorkspacePath(entry.path, skillsBase);
    if (candidate.endsWith(`/${name}`) || candidate.endsWith(`\\${name}`)) {
      return candidate;
    }
  }
  return null;
}

function printResult(result: SmokeResult): void {
  console.log(JSON.stringify(result, null, 2));
  if (result.status === 'fail') {
    process.exitCode = 1;
  }
}

async function importFromFile<T = unknown>(filePath: string): Promise<T> {
  return import(pathToFileURL(filePath).href) as Promise<T>;
}

async function main(): Promise<void> {
  const cwd = process.cwd();
  const workspacePath = join(cwd, 'workspace.json');
  if (!existsSync(workspacePath)) {
    printResult({
      status: 'skip',
      reason: `workspace.json not found at ${workspacePath}`,
    });
    return;
  }

  const skillsBase = process.env.SKILLS_BASE || resolve(cwd, '..', '..');
  const workspace = readWorkspaceConfig(workspacePath);
  const caRepo = findRepoPath(workspace, skillsBase, 'portkey-agent-skills');
  const awakenRepo = findRepoPath(workspace, skillsBase, 'awaken-agent-skills');

  if (!caRepo || !awakenRepo) {
    printResult({
      status: 'skip',
      reason: 'required repos not found in workspace.json (portkey-agent-skills / awaken-agent-skills)',
    });
    return;
  }

  const tempHome = mkdtempSync(join(tmpdir(), 'aelf-signer-chain-'));
  const originalEnv = {
    HOME: process.env.HOME,
    PORTKEY_SKILL_WALLET_CONTEXT_PATH: process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH,
    PORTKEY_CA_KEYSTORE_PASSWORD: process.env.PORTKEY_CA_KEYSTORE_PASSWORD,
  };

  try {
    process.env.HOME = tempHome;
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = join(
      tempHome,
      '.portkey',
      'skill-wallet',
      'context.v1.json',
    );

    const caAelfClientPath = join(caRepo, 'lib', 'aelf-client.ts');
    const caKeystorePath = join(caRepo, 'src', 'core', 'keystore.ts');
    const awakenSignerContextPath = join(awakenRepo, 'lib', 'signer-context.ts');

    if (!existsSync(caAelfClientPath) || !existsSync(caKeystorePath) || !existsSync(awakenSignerContextPath)) {
      printResult({
        status: 'skip',
        reason: 'required source files not found for cross-skill smoke test',
        details: {
          caAelfClientPath,
          caKeystorePath,
          awakenSignerContextPath,
        },
      });
      return;
    }

    const caAelfClient = await importFromFile<{
      createWallet: () => { privateKey: string; mnemonic: string; address: string };
    }>(caAelfClientPath);
    const caKeystore = await importFromFile<{
      saveKeystore: (input: {
        password: string;
        privateKey: string;
        mnemonic: string;
        caHash: string;
        caAddress: string;
        originChainId: 'AELF' | 'tDVV' | 'tDVW';
        network: 'mainnet' | 'testnet';
      }) => unknown;
      lockWallet: () => unknown;
    }>(caKeystorePath);
    const awakenSignerContext = await importFromFile<{
      resolveSignerContext: (input?: { signerMode?: 'auto' | 'context' }) => {
        provider: string;
        identity?: { walletType?: string; caAddress?: string };
        signer?: { address?: string };
      };
    }>(awakenSignerContextPath);

    const manager = caAelfClient.createWallet();
    const caAddress = 'ELF_smoke_ca_AELF';
    const caHash = 'smoke_ca_hash';
    const password = 'smoke-test-password';

    caKeystore.saveKeystore({
      password,
      privateKey: manager.privateKey,
      mnemonic: manager.mnemonic,
      caHash,
      caAddress,
      originChainId: 'AELF',
      network: 'mainnet',
    });
    caKeystore.lockWallet();

    process.env.PORTKEY_CA_KEYSTORE_PASSWORD = password;
    const resolved = awakenSignerContext.resolveSignerContext({ signerMode: 'context' });

    printResult({
      status: 'pass',
      details: {
        provider: resolved.provider,
        walletType: resolved.identity?.walletType || null,
        caAddress: resolved.identity?.caAddress || null,
        signerAddress: resolved.signer?.address || null,
        contextPath: process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH,
      },
    });
  } catch (error) {
    printResult({
      status: 'fail',
      reason: error instanceof Error ? error.message : String(error),
    });
  } finally {
    if (originalEnv.HOME !== undefined) process.env.HOME = originalEnv.HOME;
    else delete process.env.HOME;
    if (originalEnv.PORTKEY_SKILL_WALLET_CONTEXT_PATH !== undefined) {
      process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH =
        originalEnv.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
    } else {
      delete process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
    }
    if (originalEnv.PORTKEY_CA_KEYSTORE_PASSWORD !== undefined) {
      process.env.PORTKEY_CA_KEYSTORE_PASSWORD =
        originalEnv.PORTKEY_CA_KEYSTORE_PASSWORD;
    } else {
      delete process.env.PORTKEY_CA_KEYSTORE_PASSWORD;
    }
    rmSync(tempHome, { recursive: true, force: true });
  }
}

main();
