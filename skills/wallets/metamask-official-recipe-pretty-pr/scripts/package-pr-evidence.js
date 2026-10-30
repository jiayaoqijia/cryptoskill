#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { adapterHelp, detectRepositoryPolicy } = require('./repository-policy.js');
const { readQaReport } = require('./qa-report.js');

let incompletePackageDir;

function usage() {
  console.error(`Usage: package-pr-evidence.js --task <task-dir> [--out <task-dir/pr-package>] [--adapter ${adapterHelp()}] [--allow-fail]`);
}

function parseArgs(argv) {
  const args = { task: '', out: '', adapter: '', allowFail: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--task') args.task = argv[++i] || '';
    else if (arg === '--out') args.out = argv[++i] || '';
    else if (arg === '--adapter') args.adapter = argv[++i] || '';
    else if (arg === '--allow-fail') args.allowFail = true;
    else if (arg === '-h' || arg === '--help') { usage(); process.exit(0); }
    else throw new Error(`Unknown arg: ${arg}`);
  }
  return args;
}

function readText(file) {
  try {
    return fs.readFileSync(file, 'utf8');
  } catch (error) {
    if (error && error.code === 'ENOENT') return '';
    throw error;
  }
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    if (error && error.code === 'ENOENT') return null;
    throw error;
  }
}

function mkdirp(dir) { fs.mkdirSync(dir, { recursive: true }); }

function rel(from, to) { return path.relative(from, to).split(path.sep).join('/'); }

function sanitizeName(s) {
  return String(s || 'artifact')
    .toLowerCase()
    .replace(/\.png(?:-\d+)?(?:\.png)?$/i, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80)
    .replace(/^-+|-+$/g, '') || 'artifact';
}

function stripRuntimePngSuffix(name) {
  return name.replace(/\.png-\d+\.png$/i, '.png');
}

function nearestRunDir(file) {
  let dir = path.dirname(file);
  while (dir && dir !== path.dirname(dir)) {
    if (fs.existsSync(path.join(dir, 'summary.json')) || fs.existsSync(path.join(dir, 'screenshots-captions.json'))) return dir;
    dir = path.dirname(dir);
  }
  return path.dirname(file);
}

function captionFor(file) {
  const runDir = nearestRunDir(file);
  const captions = readJson(path.join(runDir, 'screenshots-captions.json')) || {};
  const base = path.basename(file);
  const stripped = stripRuntimePngSuffix(base);
  return captions[base] || captions[stripped] || stripped.replace(/\.png$/i, '').replace(/[-_]+/g, ' ');
}

function firstMatch(text, regex, fallback = '') {
  const match = text.match(regex);
  return match ? match[1].trim() : fallback;
}

function getRepoRoot(taskDir) {
  try {
    return execFileSync('git', ['-C', taskDir, 'rev-parse', '--show-toplevel'], { text: true, stdio: ['ignore', 'pipe', 'ignore'] }).trim();
  } catch {
    let dir = taskDir;
    while (dir && dir !== path.dirname(dir)) {
      if (fs.existsSync(path.join(dir, '.git'))) return dir;
      dir = path.dirname(dir);
    }
    return '';
  }
}

function assertSafeOutDir(taskDir, outDir) {
  const relPath = path.relative(taskDir, outDir);
  if (!relPath || relPath.startsWith('..') || path.isAbsolute(relPath)) {
    throw new Error(`Refusing --out outside task dir or equal to task dir: ${outDir}`);
  }
  const parts = relPath.split(path.sep).filter(Boolean);
  if (parts[0] === 'artifacts' || parts[0] === 'harness') {
    throw new Error(`Refusing --out inside task source/artifact dir: ${outDir}`);
  }
  if (!/^pr-package(?:[-_.][a-zA-Z0-9-]+)?$/.test(path.basename(outDir))) {
    throw new Error(`Refusing --out that is not a generated pr-package directory: ${outDir}`);
  }
}

function findPrTemplate(repoRoot) {
  if (!repoRoot) return null;
  const candidates = [
    '.github/pull-request-template.md',
    '.github/pull_request_template.md',
    '.github/PULL_REQUEST_TEMPLATE.md',
  ];
  for (const relPath of candidates) {
    const abs = path.join(repoRoot, relPath);
    if (fs.existsSync(abs)) return { abs, relPath };
  }
  return null;
}

function insertAfterHeading(markdown, headingPattern, block) {
  const match = markdown.match(headingPattern);
  if (!match || match.index === undefined) return markdown;
  const lineEnd = markdown.indexOf('\n', match.index);
  const insertAt = lineEnd === -1 ? markdown.length : lineEnd + 1;
  return `${markdown.slice(0, insertAt)}\n${block}\n${markdown.slice(insertAt)}`;
}

function insertBeforeHeading(markdown, headingPattern, block) {
  const match = markdown.match(headingPattern);
  if (!match || match.index === undefined) return `${markdown}\n\n${block}\n`;
  return `${markdown.slice(0, match.index)}${block}\n\n${markdown.slice(match.index)}`;
}

function escapeHtml(s) {
  return String(s || '')
    .replace(/&/gu, '&amp;')
    .replace(/</gu, '&lt;')
    .replace(/>/gu, '&gt;')
    .replace(/"/gu, '&quot;');
}

function buildImageSlots(copied, visualEvidence = true) {
  if (!copied.length) {
    if (!visualEvidence) return '_Screenshots: N/A — this repository is headless._\n';
    return '<!-- No screenshot files were found under artifacts/**/screenshots. Add visual evidence before claiming visual ACs. -->\n';
  }
  const rows = [];
  for (let i = 0; i < copied.length; i += 2) {
    const left = copied[i];
    const right = copied[i + 1];
    const col = (item, n) => item
      ? `<td align="center" width="50%"><strong>${escapeHtml(item.caption)}</strong><br/><!-- IMAGE_SLOT_${String(n).padStart(2, '0')}: drag/drop pr-package/images/${item.name} here. --><br/><code>pr-package/images/${item.name}</code></td>`
      : '<td width="50%"></td>';
    rows.push('<tr>', col(left, i + 1), col(right, i + 2), '</tr>');
  }
  return [
    '<table>',
    '<tr><td colspan="2"><strong>Recipe visual evidence</strong><br/>Use concise captions; edit into a clearer before/after table when that helps review.</td></tr>',
    ...rows,
    '</table>',
    '',
  ].join('\n');
}


function buildTemplatePrDesc({ templateText, templateRelPath, task, verdict, taskDir, outDir, copied, checklistExists, visualEvidence, packagedRuns, evidenceName }) {
  const descriptionBlock = [
    '<!-- recipe-pretty-pr suggestion: edit as needed before publishing. -->',
    task ? `This PR addresses ${task}.` : 'This PR addresses the linked task.',
    'See the validation and evidence sections below for recipe-backed proof.',
  ].join('\n');

  const validationBlock = [
    `<!-- recipe-pretty-pr summary: keep reviewer-facing checks concise; full paths stay in pr-package/${evidenceName}. -->`,
    `Recipe evidence: \`${verdict}\``,
    `- Full evidence package: \`pr-package/${evidenceName}\``,
    '- Quality report: `pr-package/recipe-quality.json`',
    ...packagedRuns.map((run) => `- Recipe run: \`pr-package/runs/${run.name}/\``),
  ].join('\n');

  const screenshotBlock = [
    '### **Recipe evidence**',
    '',
    `<!-- Generated from ${templateRelPath}. Drag/drop each local image file at its marker so GitHub uploads and renders it. -->`,
    '',
    buildImageSlots(copied, visualEvidence),
  ].join('\n');

  const artifactBlock = [
    '## **Recipe artifact package**',
    '',
    `Task path: \`${taskDir}\``,
    `PR package: \`${outDir}\``,
    `- Full evidence: \`pr-package/${evidenceName}\``,
    '- Quality report: `pr-package/recipe-quality.json`',
    '- Image files: `pr-package/images/`',
    checklistExists ? '- Checklist: `pr-package/checklist.md`' : '- Checklist: missing `CHECKLIST.md` at package time',
    ...packagedRuns.map((run) => `- Recipe run: \`pr-package/runs/${run.name}/\``),
  ].join('\n');

  let out = templateText;
  out = insertAfterHeading(out, /^## \*\*Description\*\*\s*$/m, descriptionBlock);
  if (task) out = out.replace(/^Fixes:\s*$/m, `Fixes: ${task}\n`);
  out = insertAfterHeading(out, /^## \*\*Manual testing steps\*\*\s*$/m, validationBlock);
  out = insertBeforeHeading(out, /^## \*\*Pre-merge author checklist\*\*\s*$/m, screenshotBlock);
  out = insertBeforeHeading(out, /^## \*\*Pre-merge author checklist\*\*\s*$/m, artifactBlock);
  return out;
}

function levelTwoHeadings(markdown) {
  return markdown.split('\n').filter((line) => /^\s{0,3}##(?!#)\s+\S/.test(line)).map((line) => line.trim());
}

function matchesTemplateHeadings(body, templateText) {
  const required = levelTwoHeadings(templateText);
  const actual = levelTwoHeadings(body);
  return required.every((heading) => actual.includes(heading));
}

// A worker-authored PR description already carries the description and
// validation text; packaging only adds the evidence images and the artifact
// package index it can vouch for.
function augmentAuthoredPrDesc({ authored, templateRelPath, taskDir, outDir, copied, checklistExists, visualEvidence, packagedRuns, evidenceName }) {
  const screenshotBlock = [
    '### **Recipe evidence**',
    '',
    templateRelPath
      ? `<!-- Generated from ${templateRelPath}. Drag/drop each local image file at its marker so GitHub uploads and renders it. -->`
      : '<!-- Drag/drop each local image file at its marker so GitHub uploads and renders it. -->',
    '',
    buildImageSlots(copied, visualEvidence),
  ].join('\n');
  const artifactBlock = [
    '## **Recipe artifact package**',
    '',
    `Task path: \`${taskDir}\``,
    `PR package: \`${outDir}\``,
    `- Full evidence: \`pr-package/${evidenceName}\``,
    '- Quality report: `pr-package/recipe-quality.json`',
    '- Image files: `pr-package/images/`',
    checklistExists ? '- Checklist: `pr-package/checklist.md`' : '- Checklist: missing `CHECKLIST.md` at package time',
    ...packagedRuns.map((run) => `- Recipe run: \`pr-package/runs/${run.name}/\``),
  ].join('\n');
  let out = authored.replace(/\s+$/u, '');
  if (/^## \*\*Screenshots\/Recordings\*\*\s*$/m.test(out)) {
    out = insertAfterHeading(out, /^## \*\*Screenshots\/Recordings\*\*\s*$/m, screenshotBlock);
  } else {
    out = insertBeforeHeading(out, /^## \*\*Pre-merge author checklist\*\*\s*$/m, screenshotBlock);
  }
  out = insertBeforeHeading(out, /^## \*\*Pre-merge author checklist\*\*\s*$/m, artifactBlock);
  return out;
}

const PACKAGE_ARTIFACT_TYPES = new Set(['summary', 'trace', 'report', 'log', 'test']);

// The sibling skill keeps the install prefix of this one (source: recipe-cook; installed: mms-recipe-cook).
function harnessResolver() {
  const cookSkillDir = path.basename(path.resolve(__dirname, '..')).replace(/recipe-pretty-pr$/u, 'recipe-cook');
  return path.resolve(__dirname, '../..', cookSkillDir, 'scripts/resolve-harness');
}

function verifyHarnessReceipt(taskDir) {
  const receipt = readJson(path.join(taskDir, 'artifacts/harness-provenance.json'));
  if (
    receipt?.package?.name !== '@deeeed/metamask-harness'
    || typeof receipt.source?.packageRoot !== 'string'
    || typeof receipt.resolvedExecutable !== 'string'
    || typeof receipt.entrySha256 !== 'string'
    || typeof receipt.packageTreeSha256 !== 'string'
  ) {
    throw new Error('Missing valid artifacts/harness-provenance.json; package evidence only after Recipe Cook locks the harness.');
  }
  try {
    return execFileSync(harnessResolver(), [taskDir, '--verify-only'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch (error) {
    const detail = error?.stderr?.toString().trim() || error.message;
    throw new Error(`Harness provenance no longer matches its recorded executable and package hashes: ${detail}`);
  }
}

function readBoundedTaskText(taskDir, filePath) {
  if (typeof filePath !== 'string' || !filePath.trim()) {
    throw new Error('EVIDENCE_PR_BODY_INVALID: the renderer did not report a rendered PR body path.');
  }
  try {
    const absolute = path.resolve(filePath);
    const root = fs.realpathSync(taskDir);
    const realFile = fs.realpathSync(absolute);
    const relative = path.relative(root, realFile);
    if (!relative || relative.startsWith('..') || path.isAbsolute(relative)) {
      throw new Error('EVIDENCE_PR_BODY_INVALID: rendered PR body must stay inside the task directory.');
    }
    const descriptor = fs.openSync(realFile, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
    try {
      if (!fs.fstatSync(descriptor).isFile()) {
        throw new Error('EVIDENCE_PR_BODY_INVALID: rendered PR body must be a regular file inside the task directory.');
      }
      return fs.readFileSync(descriptor, 'utf8');
    } finally {
      fs.closeSync(descriptor);
    }
  } catch (error) {
    if (error && typeof error.message === 'string' && error.message.startsWith('EVIDENCE_PR_BODY_INVALID')) throw error;
    throw new Error('EVIDENCE_PR_BODY_INVALID: rendered PR body must stay inside the task directory.');
  }
}

// The task's locked harness renders the PR body; its receipt stays frozen.
function renderPrBody(taskDir) {
  const harness = verifyHarnessReceipt(taskDir);
  const out = path.join(taskDir, 'artifacts/pr-body.md');
  let output;
  try {
    output = execFileSync(harness, ['pr-body', 'render', taskDir, '--out', out, '--json'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
  } catch (error) {
    throw new Error(`EVIDENCE_PR_BODY_INVALID: ${error?.stderr?.toString().trim() || error.message}`);
  }
  let result;
  try {
    result = JSON.parse(output);
  } catch {
    throw new Error('EVIDENCE_PR_BODY_INVALID: the renderer did not return JSON.');
  }
  if (result?.command !== 'pr-body' || result.status !== 'ok' || result.out !== out) {
    throw new Error('EVIDENCE_PR_BODY_INVALID: the renderer did not report the requested PR body path.');
  }
  const body = readBoundedTaskText(taskDir, result.out);
  if (!body.trim()) throw new Error('EVIDENCE_PR_BODY_INVALID: the rendered PR body is empty.');
  return body;
}

function validateRecipeRun(taskDir, runDir, validator) {
  try {
    const output = execFileSync(validator, [
      'recipe-validate',
      path.join(runDir, 'recipe.json'),
      '--artifact-manifest',
      path.join(runDir, 'artifact-manifest.json'),
      '--artifact-dir',
      runDir,
      '--json',
    ], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    const result = JSON.parse(output);
    if (result.status !== 'valid') throw new Error('validator did not return valid');
  } catch (error) {
    const detail = error?.stderr?.toString().trim() || error.message;
    throw new Error(`Invalid Recipe v1 artifact package at ${rel(taskDir, runDir)}: ${detail}`);
  }
}

function recipeProvenanceFiles(runDir, manifest) {
  const manifestEntries = new Map(
    manifest.artifacts
      .filter((entry) => entry && typeof entry === 'object' && typeof entry.path === 'string')
      .map((entry) => [entry.path, entry]),
  );
  const recipeFile = safeRelativeFile(runDir, 'recipe.json');
  const resolutionFile = safeRelativeFile(runDir, 'recipe-resolution.json');
  if (!recipeFile || !resolutionFile) return null;
  const resolution = readJson(resolutionFile.absolute);
  if (!resolution || !Array.isArray(resolution.dependencies)) return null;
  const files = [
    { path: 'recipe.json', type: 'recipe', label: 'Executed root recipe' },
    { path: 'recipe-resolution.json', type: 'json', label: 'Recipe dependency resolution' },
  ];
  for (const dependency of resolution.dependencies) {
    if (
      !dependency ||
      typeof dependency !== 'object' ||
      typeof dependency.artifact !== 'string'
    ) return null;
    files.push({ path: dependency.artifact, type: 'recipe', label: 'Resolved recipe dependency' });
  }
  return files.every((entry) => manifestEntries.get(entry.path)?.type === entry.type) ? files : null;
}

function safeRelativeFile(root, relativePath) {
  if (!relativePath || path.isAbsolute(relativePath)) return null;
  const normalized = path.normalize(relativePath);
  if (normalized === '..' || normalized.startsWith(`..${path.sep}`)) return null;
  const absolute = path.resolve(root, normalized);
  const relative = path.relative(path.resolve(root), absolute);
  if (!relative || relative.startsWith('..') || path.isAbsolute(relative)) return null;
  try {
    const stat = fs.lstatSync(absolute);
    if (!stat.isFile() || stat.isSymbolicLink()) return null;
    const realRoot = fs.realpathSync(root);
    const realFile = fs.realpathSync(absolute);
    const realRelative = path.relative(realRoot, realFile);
    if (!realRelative || realRelative.startsWith('..') || path.isAbsolute(realRelative)) return null;
  } catch {
    return null;
  }
  return { absolute, relative: relative.split(path.sep).join('/') };
}

function findArtifactManifests(dir, outDir, acc = []) {
  if (!fs.existsSync(dir)) return acc;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const absolute = path.join(dir, entry.name);
    if (path.resolve(absolute) === path.resolve(outDir)) continue;
    if (entry.isDirectory()) findArtifactManifests(absolute, outDir, acc);
    else if (entry.isFile() && entry.name === 'artifact-manifest.json') acc.push(absolute);
  }
  return acc;
}

function uniqueRunName(taskDir, runDir, used) {
  const relative = rel(taskDir, runDir);
  const base = sanitizeName(relative || path.basename(runDir) || 'run');
  let name = base;
  let suffix = 2;
  while (used.has(name)) {
    name = `${base}-${suffix}`;
    suffix += 1;
  }
  used.add(name);
  return name;
}

function packageManifestRuns(taskDir, outDir) {
  const manifests = findArtifactManifests(path.join(taskDir, 'artifacts'), outDir).sort();
  const validator = verifyHarnessReceipt(taskDir);
  const runsRoot = path.join(outDir, 'runs');
  const usedNames = new Set();
  const packaged = [];
  const screenshots = [];

  for (const manifestPath of manifests) {
    const runDir = path.dirname(manifestPath);
    const manifest = readJson(manifestPath);
    const summary = readJson(path.join(runDir, 'summary.json'));
    const trace = readJson(path.join(runDir, 'trace.json'));
    const provenanceFiles = manifest && Array.isArray(manifest.artifacts)
      ? recipeProvenanceFiles(runDir, manifest)
      : null;
    if (!manifest || manifest.version !== 1 || !Array.isArray(manifest.artifacts) || !summary || !trace) continue;
    if (!provenanceFiles) throw new Error(`Incomplete or digest-invalid Recipe v1 provenance: ${runDir}`);
    validateRecipeRun(taskDir, runDir, validator);
    if (manifest.runStatus && summary.status && manifest.runStatus !== summary.status) continue;

    const selected = new Map();
    for (const required of ['artifact-manifest.json', 'summary.json', 'trace.json']) {
      const safe = safeRelativeFile(runDir, required);
      if (safe) selected.set(safe.relative, { ...safe, type: required.startsWith('artifact-') ? 'manifest' : path.basename(required, '.json') });
    }
    if (selected.size !== 3) continue;

    let provenanceComplete = true;
    for (const entry of provenanceFiles) {
      const safe = safeRelativeFile(runDir, entry.path);
      if (!safe) {
        provenanceComplete = false;
        break;
      }
      selected.set(safe.relative, { ...safe, type: entry.type, label: entry.label });
    }
    if (!provenanceComplete) continue;

    for (const entry of manifest.artifacts) {
      if (!entry || typeof entry !== 'object' || typeof entry.path !== 'string') continue;
      const safe = safeRelativeFile(runDir, entry.path);
      if (!safe) continue;
      if (entry.type === 'screenshot') {
        // The engine stamps "<action> screenshot" when the node gave no label; that
        // names nothing, so the capture file name is the better caption.
        const genericLabel = typeof entry.label === 'string' && /^\S+ screenshot$/u.test(entry.label.trim());
        screenshots.push({
          file: safe.absolute,
          caption: (!genericLabel && entry.label) || captionFor(safe.absolute),
          runDir,
        });
      } else if (PACKAGE_ARTIFACT_TYPES.has(entry.type)) {
        selected.set(safe.relative, { ...safe, type: entry.type, label: entry.label || null });
      }
    }

    const name = uniqueRunName(taskDir, runDir, usedNames);
    const destination = path.join(runsRoot, name);
    const files = [];
    for (const item of [...selected.values()].sort((a, b) => a.relative.localeCompare(b.relative))) {
      const target = path.join(destination, item.relative);
      mkdirp(path.dirname(target));
      fs.copyFileSync(item.absolute, target);
      files.push({ path: rel(outDir, target), type: item.type, label: item.label || undefined });
    }
    packaged.push({ name, source: rel(taskDir, runDir), runStatus: manifest.runStatus || summary.status || 'unknown', files });
  }
  return { packaged, screenshots };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.task) {
    usage();
    process.exit(2);
  }
  const taskDir = path.resolve(args.task);
  if (!fs.existsSync(taskDir) || !fs.statSync(taskDir).isDirectory()) {
    throw new Error(`Task dir not found: ${taskDir}`);
  }
  const repoRoot = getRepoRoot(taskDir);
  const repositoryPolicy = detectRepositoryPolicy([repoRoot || taskDir], args.adapter);
  const visualEvidence = repositoryPolicy.visualEvidence;
  const prTemplate = findPrTemplate(repoRoot);
  const outDir = path.resolve(args.out || path.join(taskDir, 'pr-package'));
  assertSafeOutDir(taskDir, outDir);
  const imagesDir = path.join(outDir, 'images');
  fs.rmSync(outDir, { recursive: true, force: true });
  incompletePackageDir = outDir;
  mkdirp(imagesDir);
  // Dev/fix-bug uses artifacts/pr-description.md; QA uses report.html.
  // report.md remains accepted for older tasks.
  const prDescriptionSrc = path.join(taskDir, 'artifacts', 'pr-description.md');
  const qaReport = fs.existsSync(prDescriptionSrc) ? null : readQaReport(taskDir);
  const evidenceSrc = fs.existsSync(prDescriptionSrc) ? prDescriptionSrc : qaReport?.htmlPath || path.join(taskDir, 'artifacts', 'report.md');
  const evidenceName = qaReport ? 'report.html' : 'evidence.md';
  const evidenceText = qaReport?.text || readText(evidenceSrc);
  if (!evidenceText.trim()) {
    throw new Error('EVIDENCE_REPORT_MISSING: artifacts/pr-description.md, report.html with report-data.json, or legacy report.md must contain the proof summary before packaging.');
  }
  const authoredPrDesc = evidenceSrc === prDescriptionSrc ? renderPrBody(taskDir) : '';
  const qualitySrc = path.join(taskDir, 'artifacts', 'recipe-quality.json');
  const quality = readJson(qualitySrc);
  if (!quality || !['pass', 'warn', 'fail'].includes(quality.verdict)) {
    throw new Error('EVIDENCE_QUALITY_MISSING: artifacts/recipe-quality.json must contain the completed quality verdict before packaging.');
  }
  // A PR body must not ship a failed proof; a QA or review comment exists to
  // show it, so --allow-fail carries the verdict as data for those targets.
  if (quality.verdict === 'fail' && !args.allowFail) {
    throw new Error('EVIDENCE_QUALITY_FAILED: address the named proof gaps in artifacts/recipe-quality.json before packaging (comment targets may pass --allow-fail).');
  }
  const verdict = quality.verdict;
  const packagedEvidence = packageManifestRuns(taskDir, outDir);
  const packagedRuns = packagedEvidence.packaged;
  if (!packagedRuns.length) {
    throw new Error('EVIDENCE_RUN_MISSING: artifacts/ must contain at least one complete, validated Recipe v1 run package.');
  }
  const checklist = readText(path.join(taskDir, 'CHECKLIST.md'));
  const textSource = evidenceText || checklist;
  const handoff = readJson(path.join(taskDir, 'inputs', 'handoff.json'));
  const task = handoff?.task?.ticket || handoff?.task?.title || firstMatch(textSource, /Task:\s*`?([^`\n]+)`?/i, firstMatch(checklist, /Source:\s*`?([^`\n]+)`?/i, ''));
  const branch = firstMatch(textSource, /Branch:\s*`?([^`\n]+)`?/i, firstMatch(checklist, /Run branch:\s*`?([^`\n]+)`?/i, ''));

  // Cook's artifacts/evidence-manifest.json is the strict visual selection
  // (`standalone[].file`). When it names files, only those are hosted; every
  // other indexed capture stays in the run packages for the audit trail.
  const selection = readJson(path.join(taskDir, 'artifacts', 'evidence-manifest.json'));
  const selectedFiles = new Set(
    (Array.isArray(selection?.standalone) ? selection.standalone : [])
      .map((item) => (item && typeof item.file === 'string' ? path.basename(item.file) : ''))
      .filter(Boolean),
  );
  const selectedCaption = new Map(
    (Array.isArray(selection?.standalone) ? selection.standalone : [])
      .filter((item) => item && typeof item.file === 'string' && typeof item.label === 'string')
      .map((item) => [path.basename(item.file), item.label]),
  );
  const screenshots = (visualEvidence ? packagedEvidence.screenshots : [])
    .filter((shot) => selectedFiles.size === 0 || selectedFiles.has(path.basename(shot.file)))
    // A selection names one image per file; when several packages carry that
    // file name (a rerun, a call beside a run), the first in path order is hosted.
    .sort((a, b) => a.file.localeCompare(b.file))
    .filter((shot, index, all) => selectedFiles.size === 0 || all.findIndex((other) => path.basename(other.file) === path.basename(shot.file)) === index)
    .map((shot) => (selectedCaption.has(path.basename(shot.file)) ? { ...shot, caption: selectedCaption.get(path.basename(shot.file)) } : shot))
    .sort((a, b) => a.file.localeCompare(b.file));

  const copied = [];
  const seen = new Set();
  screenshots.forEach((screenshot, index) => {
    const caption = screenshot.caption;
    const baseName = sanitizeName(caption || path.basename(screenshot.file));
    let destName = `${String(index + 1).padStart(2, '0')}-${baseName}${path.extname(screenshot.file).toLowerCase() || '.png'}`;
    let n = 2;
    while (seen.has(destName)) {
      destName = `${String(index + 1).padStart(2, '0')}-${baseName}-${n}${path.extname(screenshot.file).toLowerCase() || '.png'}`;
      n += 1;
    }
    seen.add(destName);
    const dest = path.join(imagesDir, destName);
    fs.copyFileSync(screenshot.file, dest);
    copied.push({ source: screenshot.file, dest, name: destName, caption, runDir: screenshot.runDir });
  });

  fs.copyFileSync(evidenceSrc, path.join(outDir, evidenceName));
  if (qaReport) fs.copyFileSync(qaReport.dataPath, path.join(outDir, 'report-data.json'));
  const evidenceManifestSrc = path.join(taskDir, 'artifacts', 'evidence-manifest.json');
  if (fs.existsSync(evidenceManifestSrc)) fs.copyFileSync(evidenceManifestSrc, path.join(outDir, 'evidence-manifest.json'));
  fs.copyFileSync(qualitySrc, path.join(outDir, 'recipe-quality.json'));
  const checklistSrc = path.join(taskDir, 'CHECKLIST.md');
  const checklistExists = fs.existsSync(checklistSrc);
  if (checklistExists) fs.copyFileSync(checklistSrc, path.join(outDir, 'checklist.md'));

  const imageReadme = [
    '# Evidence images',
    '',
    'Copy or drag/drop these files into the GitHub PR description. Filenames are intentionally stable and reviewer-friendly.',
    '',
    ...copied.flatMap((item) => [
      `## ${item.name}`,
      '',
      item.caption,
      '',
      `Source: \`${rel(outDir, item.source)}\``,
      '',
    ]),
  ].join('\n');
  fs.writeFileSync(path.join(imagesDir, 'README.md'), `${imageReadme}\n`);

  const genericPrDesc = [
    '# PR description draft',
    '',
    '## Description',
    '',
    '<!-- Replace with the human-readable product summary. -->',
    '',
    '## Related Jira',
    '',
    task ? `- ${task}` : '- <!-- Jira/task URL -->',
    '',
    '## Changes',
    '',
    '<!-- Summarize product files changed. Keep generated harness/task artifacts out of the PR diff. -->',
    '',
    '## Validation',
    '',
    `Verdict: \`${verdict}\``,
    '',
    '<!-- Paste concise checks here. Keep raw recipe commands in the evidence package unless the reviewer needs them. -->',
    '',
    '## Evidence',
    '',
    '<!-- Drag/drop each image file at the markers below to let GitHub upload and render them. -->',
    '',
    buildImageSlots(copied, visualEvidence),
    '## Artifact package',
    '',
    `Task path: \`${taskDir}\``,
    `PR package: \`${outDir}\``,
    `- Full evidence: \`pr-package/${evidenceName}\``,
    '- Quality report: `pr-package/recipe-quality.json`',
    checklistExists ? '- Checklist: `pr-package/checklist.md`' : '- Checklist: missing `CHECKLIST.md` at package time',
    ...packagedRuns.map((run) => `- Recipe run: \`pr-package/runs/${run.name}/\``),
    '',
    '## Notes / gaps',
    '',
    '<!-- Preserve warning details, evidence gaps, runtime console noise, blocked states, or cleanup status. -->',
  ].join('\n');

  const prDesc = authoredPrDesc && (!prTemplate || matchesTemplateHeadings(authoredPrDesc, readText(prTemplate.abs)))
    ? augmentAuthoredPrDesc({
        authored: authoredPrDesc,
        templateRelPath: prTemplate ? prTemplate.relPath : '',
        taskDir,
        outDir,
        copied,
        checklistExists,
        visualEvidence,
        packagedRuns,
        evidenceName,
      })
    : prTemplate
    ? buildTemplatePrDesc({
        templateText: readText(prTemplate.abs),
        templateRelPath: prTemplate.relPath,
        task,
        verdict,
        taskDir,
        outDir,
        copied,
        checklistExists,
        visualEvidence,
        packagedRuns,
        evidenceName,
      })
    : genericPrDesc;

  fs.writeFileSync(path.join(outDir, 'pr-desc.md'), `${prDesc}\n`);

  const manifest = {
    taskDir,
    outDir,
    task,
    branch,
    verdict,
    repoRoot,
    repository: {
      canonicalSlug: repositoryPolicy.canonicalSlug,
      targetSlug: repositoryPolicy.targetSlug,
      adapter: repositoryPolicy.adapter,
      visualEvidence: repositoryPolicy.visualEvidence,
      familySource: repositoryPolicy.familySource,
    },
    prTemplate: prTemplate ? prTemplate.relPath : null,
    runs: packagedRuns,
    files: {
      prDescription: path.join(outDir, 'pr-desc.md'),
      evidence: path.join(outDir, evidenceName),
      quality: path.join(outDir, 'recipe-quality.json'),
      checklist: fs.existsSync(checklistSrc) ? path.join(outDir, 'checklist.md') : null,
      images: copied.map((item) => ({ path: path.join(outDir, 'images', item.name), caption: item.caption, source: item.source })),
    },
    generatedAt: new Date().toISOString(),
  };
  fs.writeFileSync(path.join(outDir, 'package-manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);

  const finalReport = [
    '# Final output report',
    '',
    `Task path: \`${taskDir}\``,
    `PR package path: \`${outDir}\``,
    `PR description draft: \`${path.join(outDir, 'pr-desc.md')}\``,
    `Evidence images folder: \`${imagesDir}\``,
    prTemplate ? `PR template source: \`${prTemplate.relPath}\`` : 'PR template source: not found; used generic fallback',
    '',
    copied.length ? 'Images:' : visualEvidence ? 'Images: none found' : 'Images: N/A (headless repository)',
    ...copied.map((item) => `- \`${path.join(outDir, 'images', item.name)}\` — ${item.caption}`),
    '',
    packagedRuns.length ? 'Recipe runs:' : 'Recipe runs: none found',
    ...packagedRuns.map((run) => `- \`${path.join(outDir, 'runs', run.name)}\` — ${run.runStatus}`),
  ].join('\n');
  fs.writeFileSync(path.join(outDir, 'final-report.md'), `${finalReport}\n`);

  console.log(finalReport);
}

try {
  main();
} catch (error) {
  if (incompletePackageDir) fs.rmSync(incompletePackageDir, { recursive: true, force: true });
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
