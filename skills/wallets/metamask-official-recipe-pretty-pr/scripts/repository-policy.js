const path = require('node:path');
const { execFileSync } = require('node:child_process');

const REPOSITORY_POLICIES = Object.freeze([
  Object.freeze({ canonicalSlug: 'MetaMask/metamask-extension', adapter: 'extension', visualEvidence: true }),
  Object.freeze({ canonicalSlug: 'MetaMask/metamask-mobile', adapter: 'mobile', visualEvidence: true }),
  Object.freeze({ canonicalSlug: 'MetaMask/core', adapter: 'core', visualEvidence: false }),
]);

function parseGithubRemote(url) {
  const value = String(url || '').trim();
  let owner = '';
  let repo = '';
  const scp = /^git@github\.com:([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+?)(?:\.git)?$/iu.exec(value);
  if (scp) {
    [, owner, repo] = scp;
  } else {
    try {
      const parsed = new URL(value);
      if (!['https:', 'ssh:'].includes(parsed.protocol) || parsed.hostname.toLowerCase() !== 'github.com') return null;
      if (parsed.search || parsed.hash || (parsed.protocol === 'ssh:' && parsed.username && parsed.username !== 'git')) return null;
      const parts = parsed.pathname.replace(/^\//u, '').replace(/\.git$/u, '').split('/');
      if (parts.length !== 2 || !parts.every((part) => /^[A-Za-z0-9_.-]+$/u.test(part))) return null;
      [owner, repo] = parts;
    } catch {
      return null;
    }
  }
  return { host: 'github.com', owner, repo, slug: `${owner}/${repo}`, url: value };
}

function policyForCanonicalSlug(slug) {
  const normalized = String(slug || '').toLowerCase();
  return REPOSITORY_POLICIES.find((policy) => policy.canonicalSlug.toLowerCase() === normalized) || null;
}

function policyForAdapter(adapter) {
  return REPOSITORY_POLICIES.find((policy) => policy.adapter === adapter) || null;
}

function gitRemote(repoRoot, name) {
  try {
    const url = execFileSync('git', ['-C', repoRoot, 'remote', 'get-url', name], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    return { name, url, identity: parseGithubRemote(url) };
  } catch {
    return null;
  }
}

function resolveRepositoryPolicy(repoRoot, explicitAdapter = '') {
  const origin = gitRemote(repoRoot, 'origin');
  if (!origin) throw new Error(`Repository at ${repoRoot} has no origin remote.`);
  if (!origin.identity) {
    throw new Error(`Origin must be an approved github.com SSH/HTTPS remote; refusing local path or non-GitHub identity: ${origin.url}`);
  }

  const canonicalOrigin = policyForCanonicalSlug(origin.identity.slug);
  const upstream = gitRemote(repoRoot, 'upstream');
  const canonicalUpstream = upstream?.identity ? policyForCanonicalSlug(upstream.identity.slug) : null;
  if (upstream && !upstream.identity) {
    throw new Error(`Upstream must be an approved github.com SSH/HTTPS remote: ${upstream.url}`);
  }

  let policy = canonicalOrigin || canonicalUpstream;
  let familySource = canonicalOrigin ? 'canonical-origin' : canonicalUpstream ? 'canonical-upstream' : '';
  if (canonicalOrigin && canonicalUpstream && canonicalOrigin.adapter !== canonicalUpstream.adapter) {
    throw new Error(`Origin and upstream resolve to different MetaMask product families (${canonicalOrigin.adapter} vs ${canonicalUpstream.adapter}).`);
  }

  if (explicitAdapter) {
    const explicitPolicy = policyForAdapter(explicitAdapter);
    if (!explicitPolicy) throw new Error(`Unsupported adapter: ${explicitAdapter} (expected ${adapterHelp()}).`);
    if (policy && policy.adapter !== explicitPolicy.adapter) {
      throw new Error(`Adapter ${explicitAdapter} does not match canonical repository family ${policy.adapter}.`);
    }
    if (!policy) {
      const expectedRepo = explicitPolicy.canonicalSlug.split('/')[1].toLowerCase();
      if (origin.identity.repo.toLowerCase() !== expectedRepo) {
        throw new Error(`Adapter ${explicitAdapter} requires a github.com fork named ${expectedRepo}; got ${origin.identity.slug}.`);
      }
      policy = explicitPolicy;
      familySource = 'explicit-adapter';
    }
  }

  if (!policy) {
    throw new Error(`Could not derive a canonical MetaMask product family. Add an exact github.com/MetaMask upstream remote or pass a verified --adapter (${adapterHelp()}).`);
  }

  return {
    ...policy,
    canonicalSlug: policy.canonicalSlug,
    familySource,
    targetSlug: origin.identity.slug,
    targetRemote: origin.name,
    cwd: repoRoot,
  };
}

function candidateDirs(start) {
  const dirs = [];
  let dir = path.resolve(start);
  while (true) {
    dirs.push(dir);
    const parent = path.dirname(dir);
    if (parent === dir) return dirs;
    dir = parent;
  }
}

function detectRepositoryPolicy(starts, explicitAdapter = '') {
  for (let index = 0; index < starts.length; index += 1) {
    const start = starts[index];
    let root = '';
    for (const cwd of candidateDirs(start)) {
      try {
        root = execFileSync('git', ['-C', cwd, 'rev-parse', '--show-toplevel'], {
          encoding: 'utf8',
          stdio: ['ignore', 'pipe', 'ignore'],
        }).trim();
        break;
      } catch {
        // Keep walking only until this start path resolves to a Git root.
      }
    }
    if (root) return resolveRepositoryPolicy(root, explicitAdapter);
    // The first start is the task path. Only a non-repository task may fall
    // back to cwd; an unsupported task repository must fail closed above.
    if (index === 0) continue;
  }
  throw new Error('Could not detect a Git repository from the task path or current directory.');
}

function adapterHelp() {
  return REPOSITORY_POLICIES.map((policy) => policy.adapter).join('|');
}

module.exports = {
  REPOSITORY_POLICIES,
  adapterHelp,
  detectRepositoryPolicy,
  parseGithubRemote,
  policyForAdapter,
  policyForCanonicalSlug,
  resolveRepositoryPolicy,
};
