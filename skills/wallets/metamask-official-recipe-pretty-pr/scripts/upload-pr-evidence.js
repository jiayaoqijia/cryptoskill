#!/usr/bin/env node
// upload-pr-evidence.js — push packaged PR evidence images to the CURRENT GitHub
// user's public artifacts repo and create/edit the PR with hosted image URLs.
//
// The artifacts owner is ALWAYS the logged-in `gh` user (never hard-coded), and
// every outward action is explicit-flag gated so the calling skill can ask the
// human first:
//   --ensure-repo            create <owner>/mm-<adapter>-artifacts (public) if missing
//   --confirm-public-upload  REQUIRED to upload screenshots to the public repo (alias --upload)
//   --create-pr              create the PR if none exists for the branch (else edit it)
//   --target comment --comment <id>   update an existing PR comment (QA / review evidence)
//   --target new-comment --pr <n>     post a new comment on PR <n>
// Comment targets use the QA HTML report and renderer data, or legacy report.md.
// --body <file> overrides the comment text. QA posts a short summary plus a link
// to the full HTML; reruns refresh one comment instead of stacking new ones.
// Use --dry-run to print the plan (owner/repo/branch/URLs) without any writes.
//
// The owner is ALWAYS the logged-in gh user — there is no owner override, so
// uploads/public-repo creation cannot be retargeted at another account/org.
//
// Usage:
//   upload-pr-evidence.js --task <task-dir> [--adapter extension|mobile|core]
//     [--ensure-repo] [--confirm-public-upload] [--create-pr] [--pr <number>] [--title <pr title>] [--dry-run]
//     [--target pr-body|comment|new-comment] [--comment <id>] [--body <markdown file>]
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { adapterHelp, detectRepositoryPolicy } = require('./repository-policy.js');
const { readQaReport } = require('./qa-report.js');

function usage() {
  console.error(
    `Usage: upload-pr-evidence.js --task <task-dir> [--adapter ${adapterHelp()}] [--ensure-repo] [--confirm-public-upload] [--create-pr] [--pr <n>] [--title <t>] [--dry-run] [--target pr-body|comment|new-comment] [--comment <id>] [--body <file>]`,
  );
}

function parseArgs(argv) {
  const a = { task: '', adapter: '', ensureRepo: false, createPr: false, upload: false, pr: '', title: '', dryRun: false, target: 'pr-body', comment: '', body: '' };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--task') a.task = argv[++i] || '';
    else if (arg === '--adapter') a.adapter = argv[++i] || '';
    else if (arg === '--pr') a.pr = argv[++i] || '';
    else if (arg === '--title') a.title = argv[++i] || '';
    else if (arg === '--target') a.target = argv[++i] || '';
    else if (arg === '--comment') a.comment = argv[++i] || '';
    else if (arg === '--body') a.body = argv[++i] || '';
    else if (arg === '--ensure-repo') a.ensureRepo = true;
    else if (arg === '--create-pr') a.createPr = true;
    else if (arg === '--confirm-public-upload' || arg === '--upload') a.upload = true;
    else if (arg === '--dry-run') a.dryRun = true;
    else if (arg === '-h' || arg === '--help') { usage(); process.exit(0); }
    else throw new Error(`Unknown arg: ${arg}`);
  }
  if (!a.task) { usage(); throw new Error('--task is required'); }
  if (!['pr-body', 'comment', 'new-comment'].includes(a.target)) { usage(); throw new Error('--target must be pr-body, comment or new-comment'); }
  if (a.target === 'comment' && !/^\d+$/u.test(a.comment)) { usage(); throw new Error('--target comment requires --comment <id>'); }
  if (a.target === 'new-comment' && !/^\d+$/u.test(a.pr)) { usage(); throw new Error('--target new-comment requires --pr <n>'); }
  if (a.createPr && a.target !== 'pr-body') { usage(); throw new Error('--create-pr applies to --target pr-body only'); }
  return a;
}

// gh with GH_TOKEN stripped: the fine-grained PAT in GH_TOKEN lacks write scope,
// so writes must fall back to the keyring token. Reads work either way.
function gh(args, { input, cwd } = {}) {
  const env = { ...process.env };
  delete env.GH_TOKEN;
  return execFileSync('gh', args, { encoding: 'utf8', env, input, cwd, maxBuffer: 64 * 1024 * 1024 }).trim();
}

function git(args, cwd) {
  return execFileSync('git', args, { encoding: 'utf8', cwd }).trim();
}

// Percent-encode each path segment so branch names with `/` (kept as separators)
// or spaces/special chars don't break the GitHub contents URL or the raw URL.
function encodePathSegments(p) {
  return String(p)
    .split('/')
    .map((segment) => encodeURIComponent(segment))
    .join('/');
}

function readJson(file) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (error) { if (error && error.code === 'ENOENT') return null; throw error; }
}

function imageCaptions(prPackage) {
  const manifest = readJson(path.join(prPackage, 'package-manifest.json')) || {};
  const files = manifest.files || {};
  const images = Array.isArray(files.images) ? files.images : [];
  const captions = new Map();
  for (const item of images) captions.set(path.basename(item.path || ''), item.caption || 'Recipe evidence');
  return captions;
}

function listImages(prPackage) {
  const dir = path.join(prPackage, 'images');
  if (!fs.existsSync(dir)) return [];
  const captions = imageCaptions(prPackage);
  return fs
    .readdirSync(dir)
    .filter((n) => /\.(png|jpe?g|gif|webp)$/iu.test(n))
    .sort()
    .map((n) => ({ name: n, abs: path.join(dir, n), caption: captions.get(n) || n.replace(/\.[a-z0-9]+$/iu, '').replace(/[-_]+/gu, ' ') }));
}

function ghRepoExists(ownerRepo) {
  try { gh(['repo', 'view', ownerRepo, '--json', 'name']); return true; } catch { return false; }
}

function defaultBranch(ownerRepo) {
  try { return gh(['repo', 'view', ownerRepo, '--json', 'defaultBranchRef', '--jq', '.defaultBranchRef.name']) || 'main'; }
  catch { return 'main'; }
}

function existingSha(ownerRepo, repoPath) {
  try { return gh(['api', `repos/${ownerRepo}/contents/${repoPath}`, '--jq', '.sha']); }
  catch { return ''; }
}

function uploadFile(ownerRepo, repoPath, abs, branch, dryRun) {
  if (dryRun) return;
  const content = fs.readFileSync(abs).toString('base64');
  const sha = existingSha(ownerRepo, repoPath);
  const body = JSON.stringify({
    message: `evidence: ${repoPath}`,
    content,
    branch,
    ...(sha ? { sha } : {}),
  });
  gh(['api', '-X', 'PUT', `repos/${ownerRepo}/contents/${repoPath}`, '--input', '-'], { input: body });
}

// Replace (or append) the Screenshots/Recordings section of a PR body.
function escapeHtml(s) {
  return String(s || '')
    .replace(/&/gu, '&amp;')
    .replace(/</gu, '&lt;')
    .replace(/>/gu, '&gt;')
    .replace(/"/gu, '&quot;');
}

function buildScreenshotBlock(urls) {
  if (!urls.length) return '_No hosted screenshots; attach any local recordings by drag-and-drop._';
  const rows = [];
  for (let i = 0; i < urls.length; i += 2) {
    const left = urls[i];
    const right = urls[i + 1];
    const col = (item) => item
      ? `<td align="center" width="50%"><strong>${escapeHtml(item.caption)}</strong><br/><img src="${item.url}" alt="${escapeHtml(item.caption)}" width="400" /></td>`
      : '<td width="50%"></td>';
    rows.push('<tr>', col(left), col(right), '</tr>');
  }
  return [
    '<table>',
    '<tr><td colspan="2"><strong>Recipe visual evidence</strong><br/>Screenshots are grouped for quick reviewer comparison.</td></tr>',
    ...rows,
    '</table>',
  ].join('\n');
}

function injectScreenshots(body, block) {
  const heading = /^#{1,3}\s*\*{0,2}Screenshots(?:\/Recordings)?\*{0,2}\s*$/imu;
  if (heading.test(body)) {
    const lines = body.split('\n');
    const out = [];
    let i = 0;
    while (i < lines.length) {
      out.push(lines[i]);
      if (heading.test(lines[i])) {
        out.push('', block, '');
        i += 1;
        while (i < lines.length && !/^#{1,3}\s/u.test(lines[i])) i += 1; // drop old section body
        continue;
      }
      i += 1;
    }
    return out.join('\n');
  }
  return `${body.trim()}\n\n## Screenshots/Recordings\n\n${block}\n`;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const taskDir = path.resolve(args.task);
  const prPackage = fs.existsSync(path.join(taskDir, 'pr-package')) ? path.join(taskDir, 'pr-package') : taskDir;

  const repository = detectRepositoryPolicy([taskDir, process.cwd()], args.adapter);
  const prDescPath = path.join(prPackage, 'pr-desc.md');
  const hasPrDesc = fs.existsSync(prDescPath);
  if (args.createPr && !hasPrDesc) {
    throw new Error(`PR creation requires ${prDescPath}. Run package-pr-evidence.js for this task first so the repository PR template is preserved.`);
  }
  // A comment carries the task's own report (QA, review-pr), not the PR template.
  const commentTarget = args.target !== 'pr-body';
  const qaReport = commentTarget && !args.body ? readQaReport(taskDir) : null;
  const commentBodyPath = commentTarget
    ? qaReport?.htmlPath || path.resolve(args.body || path.join(taskDir, 'artifacts', 'report.md'))
    : null;
  if (commentTarget && !(fs.existsSync(commentBodyPath) && fs.readFileSync(commentBodyPath, 'utf8').trim())) {
    throw new Error(`--target ${args.target} needs the comment text: ${commentBodyPath} is missing or empty (pass --body <file>).`);
  }
  const { cwd } = repository;
  const adapter = repository.adapter;
  // Review comments belong to the canonical product PR, even from a fork checkout.
  const targetSlug = commentTarget ? repository.canonicalSlug : repository.targetSlug;
  const branch = git(['rev-parse', '--abbrev-ref', 'HEAD'], cwd);
  const images = listImages(prPackage);
  const hasUploads = images.length > 0 || Boolean(qaReport);
  let owner = null;
  let artifactsRepo = null;

  const plan = {
    productRepo: targetSlug,
    canonicalProductRepo: repository.canonicalSlug,
    familySource: repository.familySource,
    adapter,
    visualEvidence: repository.visualEvidence,
    branch,
    images: images.map((x) => x.name),
    report: qaReport ? 'report.html' : null,
    evidencePath: hasUploads ? `evidence/${branch}/` : null,
  };

  if (!hasUploads) {
    console.error(repository.visualEvidence
      ? '[upload] WARN: no images under pr-package/images — only the PR text will be updated.'
      : '[upload] screenshots N/A for this headless repository — only the PR text will be updated.');
  }

  // Resolve an owner only for public image or HTML hosting. Legacy text-only
  // evidence bypasses this block, including headless tasks without an HTML report.
  let repoExists = false;
  let branchDefault = null;
  const urls = [];
  if (hasUploads) {
    // Owner is always the logged-in gh user — never overridable — so uploads and
    // public-repo creation cannot be retargeted at another account/org.
    owner = gh(['api', 'user', '--jq', '.login']);
    if (!owner) throw new Error('Could not resolve the logged-in GitHub user (gh api user). Run `gh auth login` first.');
    artifactsRepo = `${owner}/mm-${adapter}-artifacts`;
    // Never push screenshots to the PUBLIC artifacts repo without an explicit
    // per-run flag, even when the repo already exists.
    if (!args.dryRun && !args.upload) {
      throw new Error(`Refusing to upload ${images.length} screenshot(s)${qaReport ? ' and the HTML report with embedded screenshots' : ''} to the PUBLIC repo ${artifactsRepo} without explicit consent. Re-run with --confirm-public-upload after confirming with the user (public repo; screenshots may show wallet state — addresses/balances/positions). Use --dry-run to preview without uploading.`);
    }
    repoExists = ghRepoExists(artifactsRepo);
  }
  const resolvedPlan = { ...plan, owner, artifactsRepo };
  console.error(`[upload] plan: ${JSON.stringify(resolvedPlan, null, 2)}`);

  if (hasUploads && !repoExists) {
    // dry-run previews without writes and never requires repo-creation consent.
    if (!args.ensureRepo && !args.dryRun) {
      throw new Error(`Artifacts repo ${artifactsRepo} does not exist. Re-run with --ensure-repo ONLY after the user gives informed consent: this creates a PUBLIC GitHub repo and uploads evidence there, including any HTML report and embedded screenshots, which may show wallet state (addresses, balances, positions). Anyone can view a public repo.`);
    }
    if (args.dryRun) {
      console.error(`[upload] dry-run: artifacts repo ${artifactsRepo} does not exist${args.ensureRepo ? ' (would be created with --ensure-repo)' : ' (creating it needs --ensure-repo)'} — no writes.`);
    } else {
      console.error(`[upload] creating PUBLIC artifacts repo ${artifactsRepo} (reports/screenshots may show wallet state — addresses/balances/positions — and are world-readable)`);
      gh(['repo', 'create', artifactsRepo, '--public', '--add-readme', '--description', `MetaMask ${adapter} recipe validation artifacts`]);
      repoExists = true;
    }
  }

  // 2. upload images and the HTML report under the same explicit consent gate
  // The upload is gated above by --confirm-public-upload: it never runs without
  // that explicit per-run flag (or --dry-run, which writes nothing), even when the
  // artifacts repo already exists. The recipe-pretty-pr skill also requires human
  // consent before invoking this script. Do not remove the gate.
  let reportUrl = null;
  if (hasUploads) {
    branchDefault = repoExists || !args.dryRun ? defaultBranch(artifactsRepo) : 'main';
    const encodedBranch = encodePathSegments(branch);
    const encodedDefaultBranch = encodeURIComponent(branchDefault);
    for (const img of images) {
      const repoPath = `evidence/${encodedBranch}/${encodeURIComponent(img.name)}`;
      uploadFile(artifactsRepo, repoPath, img.abs, branchDefault, args.dryRun);
      urls.push({ name: img.name, caption: img.caption, url: `https://raw.githubusercontent.com/${artifactsRepo}/${encodedDefaultBranch}/${repoPath}` });
    }
    if (qaReport) {
      const repoPath = `evidence/${encodedBranch}/report.html`;
      uploadFile(artifactsRepo, repoPath, qaReport.htmlPath, branchDefault, args.dryRun);
      reportUrl = `https://github.com/${artifactsRepo}/blob/${encodedDefaultBranch}/${repoPath}`;
    }
  }

  // 3. build the Screenshots block (images hosted; videos stay local drag/drop)
  const block = !repository.visualEvidence && !images.length
    ? '_Screenshots: N/A — this repository is headless._'
    : buildScreenshotBlock(urls);

  // 4. body: the PR template body from pr-desc.md, or the task report for a comment
  let body = commentTarget
    ? qaReport?.text || fs.readFileSync(commentBodyPath, 'utf8')
    : hasPrDesc ? fs.readFileSync(prDescPath, 'utf8') : `## Summary\n\nSee evidence.\n`;
  if (reportUrl) {
    body += `\n\n[Full HTML report](${reportUrl}) — download and open locally. Text and screenshots are embedded; recordings remain in the retained evidence store.\n`;
  }
  body = injectScreenshots(body, block);
  const bodyFile = path.join(prPackage, commentTarget ? 'comment-body.uploaded.md' : 'pr-body.uploaded.md');
  if (!args.dryRun) fs.writeFileSync(bodyFile, body);

  // 5. write the target: a PR comment (the flag is the consent), or the PR (only when --create-pr)
  let prUrl = '';
  let commentUrl = '';
  if (commentTarget) {
    const endpoint = args.target === 'comment'
      ? `repos/${targetSlug}/issues/comments/${args.comment}`
      : `repos/${targetSlug}/issues/${args.pr}/comments`;
    const method = args.target === 'comment' ? 'PATCH' : 'POST';
    console.error(`[upload] ${args.dryRun ? 'dry-run: would ' : ''}${method} ${endpoint}`);
    if (!args.dryRun) {
      commentUrl = gh(['api', '-X', method, endpoint, '-F', `body=@${bodyFile}`, '--jq', '.html_url'], { cwd });
    }
  } else if (args.createPr) {
    let prRef = args.pr;
    if (!prRef) {
      try { prRef = gh(['pr', 'view', branch, '--repo', targetSlug, '--json', 'number', '--jq', '.number'], { cwd }); } catch { prRef = ''; }
    }
    if (prRef) {
      console.error(`[upload] editing PR #${prRef}`);
      if (!args.dryRun) gh(['pr', 'edit', String(prRef), '--repo', targetSlug, '--body-file', bodyFile], { cwd });
      if (!args.dryRun) prUrl = gh(['pr', 'view', String(prRef), '--repo', targetSlug, '--json', 'url', '--jq', '.url'], { cwd });
    } else {
      const title = args.title || git(['log', '-1', '--pretty=%s'], cwd);
      console.error(`[upload] creating PR "${title}"`);
      if (!args.dryRun) prUrl = gh(['pr', 'create', '--repo', targetSlug, '--title', title, '--body-file', bodyFile], { cwd });
    }
  } else {
    console.error(images.length
      ? '[upload] --create-pr not set: uploaded assets + wrote pr-body.uploaded.md; PR not created/edited.'
      : '[upload] --create-pr not set: wrote local pr-body.uploaded.md only; PR not created/edited.');
  }

  console.log(JSON.stringify({ ...resolvedPlan, target: args.target, defaultBranch: branchDefault, urls, reportUrl, prBodyFile: args.dryRun ? null : bodyFile, prUrl: prUrl || null, commentUrl: commentUrl || null, dryRun: args.dryRun }, null, 2));
}

try { main(); } catch (error) {
  console.error(`[upload] FAILED: ${error && error.message ? error.message : error}`);
  process.exit(1);
}
