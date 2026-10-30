import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { prVerdicts, renderReport } from './render-report.mjs';

const report = {
  title: 'Daily <validation>', verdict: 'PARTIAL', summary: 'Recorded summary',
  sources: [{ id: 'change1', title: 'Duplicate submission protection', url: 'https://example.com/pr/1' }],
  criteria: [{ id: 'AC1', sourceId: 'change1', text: 'Double tap submits once.', verdict: 'PASS', detail: 'One recorded request.' },
    { id: 'AC2', sourceId: 'change1', text: 'Retry succeeds after a failure.', verdict: 'UNTESTABLE', coverageState: 'not-run', detail: 'Not attempted; no blocker recorded.' }],
};

test('report shows full criteria, partial coverage, source names and script-free quick navigation', async () => {
  const html = await renderReport(report, os.tmpdir());
  assert.match(html, /Daily &lt;validation&gt;/);
  assert.match(html, /Partially validated/);
  assert.match(html, /1\/2 criteria proved/);
  assert.match(html, /NOT RUN/);
  assert.match(html, /Recorded verdict: UNTESTABLE/);
  assert.match(html, /<details open class="criterion"/);
  assert.match(html, /Quick report navigation/);
  assert.match(html, /position:sticky/);
  assert.match(html, /Double tap submits once\./);
  assert.doesNotMatch(html, /<script\b/i);
  const full = await renderReport({ ...report, criteria: [report.criteria[0]] }, os.tmpdir());
  assert.match(full, /Fully validated/);
  const failed = await renderReport({ ...report, criteria: [{ ...report.criteria[0], verdict: 'FAIL' }] }, os.tmpdir());
  assert.match(failed, /Failure found/);
});

test('header identifies the tested build and keeps missing historical identity explicit', async () => {
  const testedBuild = { name: 'mobile', version: '8.16.0', branch: 'release/8.16.0', commit: '8e8ad1ea' + 'a'.repeat(32) };
  const html = await renderReport({ ...report, testedBuild }, os.tmpdir());
  assert.match(html, /<h1>Daily &lt;validation&gt;<\/h1><p class="build-identity">mobile 8\.16\.0 · release\/8\.16\.0 @ <abbr title="8e8ad1eaa{32}">8e8ad1ea<\/abbr><\/p>/);
  assert.match(await renderReport(report, os.tmpdir()), /Tested app version, branch and HEAD were not recorded/);
  const escaped = await renderReport({ ...report, testedBuild: { ...testedBuild, branch: '<branch>' } }, os.tmpdir());
  assert.match(escaped, /&lt;branch&gt;/);
  await assert.rejects(renderReport({ ...report, testedBuild: { ...testedBuild, version: '' } }, os.tmpdir()), /Tested build version/);
  await assert.rejects(renderReport({ ...report, testedBuild: { ...testedBuild, commit: '8e8ad1ea' } }, os.tmpdir()), /full HEAD SHA/);
});

test('legacy gaps remain unknown, and classified blockers require evidence', async () => {
  const criterion = { ...report.criteria[1] };
  delete criterion.coverageState;
  const html = await renderReport({ ...report, criteria: [criterion] }, os.tmpdir());
  assert.match(html, /NOT PROVED/);
  assert.match(html, /Recorded verdict: UNTESTABLE/);
  assert.doesNotMatch(html, /NOT RUN|INCOMPLETE PROOF|BLOCKED/);
  criterion.coverageState = 'blocked';
  await assert.rejects(renderReport({ ...report, criteria: [criterion] }, os.tmpdir()), /Retained prerequisite/);
  criterion.blockerEvidence = [{}];
  await assert.rejects(renderReport({ ...report, criteria: [criterion] }, os.tmpdir()), /Blocker evidence label/);
});

test('criterion explanations distinguish failures from missing proof', async () => {
  for (const [verdict, heading] of [
    ['PASS', 'What was proved'],
    ['FAIL', 'What failed'],
    ['UNTESTABLE', 'What remains unproved'],
  ]) {
    const html = await renderReport({ ...report, criteria: [
      { ...report.criteria[0], verdict, detail: 'Retained observation.' },
    ] }, os.tmpdir());
    assert.match(html, new RegExp(`<strong>${heading}:</strong> Retained observation\\.`));
    for (const other of ['What was proved', 'What failed', 'What remains unproved']) {
      if (other !== heading) assert.doesNotMatch(html, new RegExp(`<strong>${other}:`));
    }
  }
});

test('report refuses orphan criteria and invented verdicts', async () => {
  await assert.rejects(renderReport({ ...report, sources: [] }, os.tmpdir()), /Missing readable source/);
  await assert.rejects(renderReport({ ...report, criteria: [{ ...report.criteria[0], verdict: 'probably' }] }, os.tmpdir()), /Unknown verdict/);
  await assert.rejects(renderReport({ ...report, sources: [{ ...report.sources[0], url: 'javascript:alert(1)' }] }, os.tmpdir()), /Unsupported report link/);
});

test('evidence links may be paths relative to the artifact directory, never outside it', async () => {
  const withEvidence = url => ({ ...report, criteria: [{ ...report.criteria[0], evidence: [{ label: 'Trace', url }] }, report.criteria[1]] });
  const html = await renderReport(withEvidence('recipe-run/trace 1.json'), os.tmpdir());
  assert.match(html, /<a href="recipe-run\/trace%201\.json"[^>]*>Trace<\/a>/);
  assert.match(await renderReport(withEvidence('%2e%2e/x.json'), os.tmpdir()), /href="%252e%252e\/x\.json"/);
  for (const url of ['../secret.json', 'run/../../secret.json', './x.json', 'a//b.json', '/etc/passwd', '//evil.example/x', 'javascript:alert(1)', 'file:///etc/passwd', 'run\\trace.json'])
    await assert.rejects(renderReport(withEvidence(url), os.tmpdir()), /Unsupported report link/, url);
});

test('selected smoke success stays separate from full acceptance coverage', async () => {
  const plan = {
    level: 'Integration smoke', evidence: { label: 'Retained pre-execution plan' },
    selectedCriterionIds: ['AC1'],
    exclusions: [{ criterionId: 'AC2', reason: 'Unchanged retry path; expand after a smoke failure.' }],
  };
  const html = await renderReport({ ...report, plan }, os.tmpdir());
  assert.match(html, /Selected checks passed/);
  assert.match(html, /1\/1 selected checks proved; 1\/2 full criteria proved/);
  assert.match(html, /OUTSIDE THIS PLAN/);
  assert.match(html, /Unchanged retry path/);
  assert.doesNotMatch(html, /Fully validated/);
  assert.match(html, /Recorded verdict: UNTESTABLE/);
  await assert.rejects(renderReport({ ...report, plan: { ...plan, exclusions: [] } }, os.tmpdir()), /every inventoried criterion/);
  await assert.rejects(renderReport({ ...report, plan: { ...plan, selectedCriterionIds: ['AC1', 'AC2'] } }, os.tmpdir()), /must not overlap/);
  const incidentalFailure = await renderReport({ ...report, plan, verdict: 'FAIL', criteria: [report.criteria[0],
    { ...report.criteria[1], verdict: 'FAIL', detail: 'An observed failure outside the selected plan still needs attention.' }] }, os.tmpdir());
  assert.match(incidentalFailure, /Failure found/);
  assert.match(incidentalFailure, /<details open class="criterion" data-verdict="FAIL"/);
});

test('video references are portable, escaped, and confined to retained artifacts', async t => {
  const root=await mkdtemp(path.join(os.tmpdir(),'report-videos-'));
  const outside=await mkdtemp(path.join(os.tmpdir(),'report-external-videos-'));
  t.after(async()=>{await rm(root,{recursive:true,force:true});await rm(outside,{recursive:true,force:true});});
  await writeFile(path.join(root,'proof clip.mp4'),'retained media fixture');
  const video={path:'proof clip.mp4',caption:'Proof <capture>',criterionIds:['AC1']};
  const html=await renderReport({...report,videos:[video]},root);
  assert.match(html,/src="proof%20clip.mp4"/);
  assert.match(html,/Proof &lt;capture&gt;/);
  assert.doesNotMatch(html,/retained media fixture/);
  await assert.rejects(renderReport({...report,videos:[{...video,path:'../outside.mp4'}]},root),/relative media path/);
  await writeFile(path.join(outside,'private.mp4'),'not retained');
  await symlink(path.join(outside,'private.mp4'),path.join(root,'linked.mp4'));
  await assert.rejects(renderReport({...report,videos:[{...video,path:'linked.mp4'}]},root),/escapes/);
  await assert.rejects(renderReport({...report,videos:[{...video,markers:[{traceIndex:0,label:'Unverified time',criterionIds:['AC1']}]}]},root),/require a retained timeline/);
});

test('embedded evidence cannot escape the declared artifact directory through a symlink', async t => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'report-assets-'));
  const outside = await mkdtemp(path.join(os.tmpdir(), 'report-outside-'));
  t.after(async () => { await rm(root, { recursive: true, force: true }); await rm(outside, { recursive: true, force: true }); });
  await writeFile(path.join(outside, 'private.png'), 'not public');
  await symlink(path.join(outside, 'private.png'), path.join(root, 'linked.png'));
  await assert.rejects(renderReport({ ...report, images: [{ path: 'linked.png', caption: 'Evidence', criterionIds: ['AC1'] }] }, root), /inside the report asset directory/);
});

test('per-PR verdicts roll up only the recorded criterion verdicts', () => {
  const crit = (id, sourceId, verdict, coverageState) => ({ id, sourceId, verdict, ...(coverageState ? { coverageState } : {}), detail: 'Recorded.' });
  const data = {
    verdict: 'PARTIAL',
    sources: ['fresh', 'prior', 'blocked', 'deferred', 'unclassified', 'failed'].map(id => ({ id, title: `Change ${id}` })),
    criteria: [crit('F1', 'fresh', 'PASS'), crit('P1', 'prior', 'PASS'), crit('P2', 'prior', 'PASS'),
      crit('B1', 'blocked', 'UNTESTABLE', 'blocked'), crit('B2', 'blocked', 'UNTESTABLE', 'not-run'), crit('B3', 'blocked', 'PASS'),
      crit('D1', 'deferred', 'UNTESTABLE', 'not-run'), crit('D2', 'deferred', 'UNTESTABLE'),
      crit('U1', 'unclassified', 'UNTESTABLE'), crit('X1', 'failed', 'FAIL'), crit('X2', 'failed', 'UNTESTABLE', 'blocked')],
    plan: { exclusions: [{ criterionId: 'P1' }, { criterionId: 'D2' }] },
  };
  const result = prVerdicts(data, { path: 'report-data.json', digest: 'sha256:x' }, '2026-10-10T00:00:00.000Z');
  assert.equal(result.generatedAt, '2026-10-10T00:00:00.000Z');
  assert.deepEqual(result.generatedFrom, { path: 'report-data.json', digest: 'sha256:x' });
  assert.deepEqual(result.prs.map(p => [p.id, p.verdict, `${p.proved}/${p.total}`]), [
    ['fresh', 'PASS', '1/1'], ['prior', 'PASS (prior evidence)', '2/2'], ['blocked', 'BLOCKED', '1/3'],
    ['deferred', 'DEFERRED', '0/2'], ['unclassified', 'NOT PROVED', '0/1'], ['failed', 'FAIL', '0/2']]);
  // Criterion rows copy the recorded verdict and cause; a missing cause stays null.
  assert.deepEqual(result.prs[3].criteria, [
    { id: 'D1', verdict: 'UNTESTABLE', coverageState: 'not-run', outsidePlan: false },
    { id: 'D2', verdict: 'UNTESTABLE', coverageState: null, outsidePlan: true }]);
  assert.deepEqual(result.prs[4].criteria, [{ id: 'U1', verdict: 'UNTESTABLE', coverageState: null, outsidePlan: false }]);
});

test('every render rewrites pr-verdicts.json from the rendered data; a refused render writes nothing', async t => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'report-verdicts-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const script = fileURLToPath(new URL('./render-report.mjs', import.meta.url));
  const input = path.join(root, 'report-data.json');
  const verdictsPath = path.join(root, 'pr-verdicts.json');
  const render = () => execFileSync(process.execPath, [script, '--input', input, '--out', path.join(root, 'report.html')], { stdio: 'pipe' });
  const blocked = { ...report.criteria[1], coverageState: 'blocked', blockerEvidence: [{ label: 'Gateway refused' }] };
  await writeFile(verdictsPath, JSON.stringify([{ id: 'change1', verdict: 'BLOCKED', criteria: [] }]));
  await writeFile(input, JSON.stringify({ ...report, criteria: [report.criteria[0], blocked] }));
  render();
  let written = JSON.parse(await readFile(verdictsPath, 'utf8'));
  assert.equal(written.prs[0].verdict, 'BLOCKED');
  // A replay passes the blocked criterion: the next render replaces the stale rollup.
  const replayed = JSON.stringify({ ...report, verdict: 'PASS', criteria: [report.criteria[0], { ...report.criteria[1], verdict: 'PASS', coverageState: undefined }] });
  await writeFile(input, replayed);
  render();
  written = JSON.parse(await readFile(verdictsPath, 'utf8'));
  assert.equal(written.verdict, 'PASS');
  assert.deepEqual(written.prs.map(p => [p.id, p.title, p.verdict, p.proved, p.total]), [['change1', 'Duplicate submission protection', 'PASS', 2, 2]]);
  assert.deepEqual(written.generatedFrom, { path: 'report-data.json', digest: `sha256:${createHash('sha256').update(replayed).digest('hex')}` });
  assert.ok(!Number.isNaN(Date.parse(written.generatedAt)));
  const before = await Promise.all([verdictsPath, path.join(root, 'report.html')].map(file => readFile(file, 'utf8')));
  await writeFile(input, JSON.stringify({ ...report, criteria: [{ ...report.criteria[0], verdict: 'probably' }] }));
  assert.throws(render, /Unknown verdict/);
  assert.deepEqual(await Promise.all([verdictsPath, path.join(root, 'report.html')].map(file => readFile(file, 'utf8'))), before);
});
