#!/usr/bin/env node
// Task folder for a review you launch yourself: a marked checklist, and what each round reviewed.
//   review-task.mjs start <PR number or URL | branch | base..head> [--pr <number>] [--cold]
//   review-task.mjs finish <round folder>
// Rounds live in temp/tasks/review/<target>/r<N>, where `mm-harness status --watch` finds them.
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const skillDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const skillFile = path.join(skillDir, 'SKILL.md');
const checklistId = path.basename(skillDir).replace(/^mms-/, '');
const [command, ...rest] = process.argv.slice(2);
const fail = message => { console.error(`review-task: ${message}`); process.exit(1); };
const git = (...args) => {
  const result = spawnSync('git', args, { encoding: 'utf8', maxBuffer: 1 << 28 });
  return result.status === 0 ? result.stdout.trim() : undefined;
};
const commit = ref => git('rev-parse', '--verify', '--quiet', `${ref}^{commit}`);
const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const run = (file, args) => spawnSync(file, args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });

const root = git('rev-parse', '--show-toplevel') ?? fail('run this inside the repository under review');
process.chdir(root);
const revision = () => createHash('sha256')
  .update(fs.readFileSync(skillFile))
  .update(fs.readFileSync(path.join(skillDir, 'references/review-sources.json')))
  .digest('hex').slice(0, 16);

// A file's change in the PR, without line numbers, so a merge from the default branch is not a change.
function contribution(forkPoint, head) {
  const patch = git('diff', '--no-color', '--no-ext-diff', '--no-renames', forkPoint, head) ?? fail(`cannot diff ${forkPoint}..${head}`);
  return new Map(patch.split(/^(?=diff --git )/m).filter(Boolean).map(text => {
    const name = text.match(/^diff --git a\/(.*) b\/\1$/m)?.[1] ?? text.split('\n', 1)[0];
    return [name, text.replace(/^index .*\n/m, '').replace(/^@@ .*$/gm, '@@')];
  }));
}

function resolveTarget(target, prOption) {
  const range = target.match(/^(.+?)\.\.\.?(.+)$/);
  const pr = prOption ?? target.match(/(?:^|\/pull\/)(\d+)\/?$/)?.[1];
  if (range) {
    const [base, head] = [commit(range[1]), commit(range[2])];
    if (!base || !head) fail(`${target}: fetch both commits first`);
    const forkPoint = git('merge-base', base, head);
    return { pr, head, forkPoint: forkPoint ?? base, forkPointKind: forkPoint ? 'merge-base' : 'given base' };
  }
  let head = commit(target); let baseRef = git('symbolic-ref', '--quiet', 'refs/remotes/origin/HEAD') ?? 'origin/main';
  if (pr) {
    const view = run('gh', ['pr', 'view', target, '--json', 'headRefOid,baseRefName']);
    if (view.status !== 0) fail(`cannot read PR ${pr}; pass base..head with --pr ${pr}`);
    const { headRefOid, baseRefName } = JSON.parse(view.stdout);
    head = commit(headRefOid); baseRef = `origin/${baseRefName}`;
    if (!head) fail(`PR ${pr} head ${headRefOid} is not here; run: git fetch origin pull/${pr}/head`);
  }
  if (!head) fail(`unknown review target: ${target}`);
  const forkPoint = git('merge-base', baseRef, head);
  if (!forkPoint) fail(`no merge base with ${baseRef}; fetch it, or pass base..head`);
  return { pr, head, forkPoint, forkPointKind: 'merge-base' };
}

// Warm only when the earlier round can be trusted to cover what did not change.
function coldReason(previous, head, force) {
  if (force) return 'cold was requested';
  if (!previous) return 'first round';
  if (!previous.verdict) return `r${previous.round} did not finish`;
  if (previous.revision !== revision()) return 'the rules or checklist changed';
  if (previous.head === head) return `the head is the one r${previous.round} reviewed`;
  if (git('merge-base', '--is-ancestor', previous.head, head) === undefined) return `the r${previous.round} head is not part of this branch`;
  return undefined;
}

function start() {
  const args = [...rest];
  const force = args.includes('--cold');
  const prAt = args.indexOf('--pr');
  const prOption = prAt >= 0 ? args.splice(prAt, 2)[1] : undefined;
  const [target] = args.filter(arg => arg !== '--cold');
  if (!target) fail('start needs a PR, a branch or base..head');
  if (prOption !== undefined && !/^\d+$/.test(prOption)) fail('--pr needs a number');
  if (!fs.existsSync(skillFile)) fail('run the installed skill: its SKILL.md carries the repository checks');
  const review = resolveTarget(target, prOption);
  const name = review.pr ? `pr-${review.pr}` : (target.includes('..') ? `head-${review.head.slice(0, 10)}` : target).replace(/[^\w.-]+/g, '-');
  const base = path.join('temp/tasks/review', name);
  fs.mkdirSync(base, { recursive: true });
  fs.writeFileSync('temp/tasks/review/.gitignore', '*\n');
  const rounds = fs.readdirSync(base).map(entry => Number(entry.match(/^r(\d+)$/)?.[1])).filter(Boolean).sort((a, b) => a - b);
  const last = rounds.at(-1);
  const lastFile = last && path.join(base, `r${last}`, 'review.json');
  const previous = lastFile && fs.existsSync(lastFile) ? readJson(lastFile) : undefined;
  if (previous && !previous.verdict && previous.head === review.head && !force) return report(path.join(base, `r${last}`), previous, 'Resuming');

  const round = (last ?? 0) + 1;
  const dir = path.join(base, `r${round}`);
  const reason = coldReason(previous, review.head, force);
  const record = { schemaVersion: 1, skill: checklistId, revision: revision(), target, ...review, round, mode: reason ? 'cold' : 'warm', reason: reason ?? `r${previous.round} finished with ${previous.verdict}`, previous: previous ? `r${previous.round}` : null, startedAt: new Date().toISOString() };
  fs.mkdirSync(path.join(dir, 'inputs'), { recursive: true });
  fs.mkdirSync(path.join(dir, 'artifacts'), { recursive: true });
  const now = contribution(review.forkPoint, review.head);
  if (!reason) {
    const before = contribution(previous.forkPoint, previous.head);
    record.changedFiles = [...new Set([...before.keys(), ...now.keys()])].filter(file => before.get(file) !== now.get(file)).sort();
    const diff = record.changedFiles.length ? git('diff', '--no-color', '--no-ext-diff', previous.head, review.head, '--', ...record.changedFiles) : '';
    fs.writeFileSync(path.join(dir, 'inputs/since-last.diff'), `${diff}\n`);
  }
  record.files = [...now.keys()].sort();
  materialize(dir, record);
  record.checklist = 'CHECKLIST.md';
  record.rows = rowsOf(checklistText()).length;
  fs.writeFileSync(path.join(dir, 'review.json'), `${JSON.stringify(record, null, 2)}\n`);
  report(dir, record, 'Started');
}

const rowsOf = text => [...text.matchAll(/^- \[[ xX]\] (?:\d+\. )?(.*)$/gm)].map(match => match[1]);
const checklistText = () => fs.readFileSync(skillFile, 'utf8').replace(/^[\s\S]*?(?=^## Setup$)/m, '');

// A mark says a row is done; its ledger section says what was found.
function ledgerGaps(text) {
  const sections = new Map(text.split(/^## (?=\d+\. )/m).slice(1).map(section => [Number(section.match(/^\d+/)[0]), section]));
  return rowsOf(checklistText()).flatMap((title, index) => {
    const section = sections.get(index + 1);
    const outcome = section?.match(/^Outcome: *(.*)$/m);
    if (!/^(PASS|FINDING|NOT_APPLICABLE|NOT_CHECKED)\b/.test(outcome?.[1] ?? '')) return [`${index + 1}. ${title}: no outcome`];
    const evidence = outcome[1].replace(/^\w+[\s.:,;-]*/, '') + section.slice(section.indexOf(outcome[0]) + outcome[0].length);
    return evidence.trim() ? [] : [`${index + 1}. ${title}: no evidence`];
  });
}

// mm-harness owns the task and its marks. Without it the checklist is a plain file.
function materialize(dir, record) {
  let number = 0;
  const rows = checklistText().replace(/^- \[ \] /gm, () => `- [ ] ${++number}. `);
  fs.writeFileSync(path.join(dir, 'artifacts/review-ledger.md'), `# Review ledger\n\n${rowsOf(rows).map((title, index) => `## ${index + 1}. ${title}\n\nOutcome:\n`).join('\n')}`);
  if (run('mm-harness', ['--version']).status === 0) {
    const templates = fs.mkdtempSync(path.join(os.tmpdir(), 'review-template-'));
    fs.mkdirSync(path.join(templates, 'review-pr'));
    fs.writeFileSync(path.join(templates, 'review-pr/default.md'), `---\nplatforms: [mobile, extension, core, terminal, web-dapp, cli]\ndescription: Static review with the installed team checklist.\n---\n\n# Static review\n\n${rows}`);
    const init = run('mm-harness', ['task', 'init', dir, '--flow', 'review-pr', '--template', 'review-pr/default', '--dir', templates, '--title', `Review ${record.pr ? `PR ${record.pr}` : record.target} r${record.round}`, '--task-text', `Static review of ${record.forkPoint}..${record.head}`]);
    fs.rmSync(templates, { recursive: true, force: true });
    const mark = path.resolve(dir, 'mark');
    if (init.status === 0 && run(mark, ['start']).status === 0) {
      record.marks = true;
      return;
    }
    console.error(`review-task: mm-harness could not create the task, using a plain checklist: ${(init.stderr || init.stdout).trim().split('\n').filter(line => !/update available|→ .* available/.test(line)).at(-1)}`);
  }
  record.marks = false;
  fs.writeFileSync(path.join(dir, 'CHECKLIST.md'), rows);
}

function report(dir, record, verb) {
  const self = path.relative(root, fileURLToPath(import.meta.url));
  console.log([
    `${verb} ${record.mode} round r${record.round}: ${record.reason}`,
    `folder: ${dir}`,
    `review: git diff ${record.forkPoint} ${record.head} (${record.forkPointKind}, ${record.files.length} files)`,
    ...(record.mode === 'warm' ? [`since ${record.previous}: ${record.changedFiles.length} files, ${dir}/inputs/since-last.diff`] : []),
    ...(record.previous ? [`earlier round: ${path.join(path.dirname(dir), record.previous)}/artifacts`] : []),
    record.marks ? `checklist: ${dir}/CHECKLIST.md; after each row: ${dir}/mark <row>` : `checklist: ${dir}/CHECKLIST.md; tick each row`,
    `ledger: ${dir}/artifacts/review-ledger.md; each Outcome is PASS, FINDING, NOT_APPLICABLE or NOT_CHECKED, then the evidence. A later row may correct an earlier one.`,
    ...(record.marks ? ['watch: mm-harness status --watch'] : []),
    `finish: node ${self} finish ${dir}`,
  ].join('\n'));
}

function finish() {
  const [dir] = rest;
  const file = dir && path.join(dir, 'review.json');
  if (!file || !fs.existsSync(file)) fail('finish needs a round folder');
  const record = readJson(file);
  const artifact = name => path.join(dir, 'artifacts', name);
  for (const name of ['review.md', 'review-ledger.md', 'line-comments.json', 'learnings.md']) if (!fs.existsSync(artifact(name)) || !fs.readFileSync(artifact(name), 'utf8').trim()) fail(`${artifact(name)} is missing or empty`);
  const gaps = ledgerGaps(fs.readFileSync(artifact('review-ledger.md'), 'utf8'));
  if (gaps.length) fail(`review-ledger.md is incomplete for ${gaps.length} rows:\n${gaps.slice(0, 10).join('\n')}`);
  const body = fs.readFileSync(artifact('review.md'), 'utf8');
  const verdict = body.match(/^VERDICT: (APPROVE|COMMENT|REQUEST_CHANGES)\s*$/m)?.[1] ?? fail('review.md needs a VERDICT line');
  if (body.match(/^COMMIT: ([0-9a-f]{40})\s*$/m)?.[1] !== record.head) fail(`review.md must name COMMIT: ${record.head}`);
  const comments = readJson(artifact('line-comments.json'));
  if (comments.recommendation !== undefined && comments.recommendation !== verdict) fail(`line-comments.json recommends ${comments.recommendation}, review.md says ${verdict}`);
  const checklist = path.join(dir, 'CHECKLIST.md');
  const open = (fs.readFileSync(checklist, 'utf8').match(/^- \[ \] /gm) ?? []).length;
  if (open) fail(`${open} rows are still open in ${checklist}`);
  if (record.marks) {
    const mark = path.resolve(dir, 'mark');
    const result = run(mark, ['complete', '--mark-last']);
    if (result.status !== 0) fail((result.stderr || result.stdout).trim());
  }
  fs.writeFileSync(file, `${JSON.stringify({ ...record, verdict, finishedAt: new Date().toISOString() }, null, 2)}\n`);
  console.log(`Finished r${record.round}: ${verdict}. Nothing was posted.`);
}

if (command === 'start') start();
else if (command === 'finish') finish();
else fail('use start or finish');
