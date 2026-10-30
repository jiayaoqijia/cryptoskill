#!/usr/bin/env node
// Presentation only: consumes recorded verdicts; never evaluates or changes proof.
import { readFile, realpath, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[c]);
const required = (value, label) => {
  if (typeof value !== 'string' || !value.trim()) throw new Error(`${label} is required`);
  return value;
};
// Encode artifact-relative links; reject absolute paths, backslashes and empty/dot segments.
function artifactHref(relative) {
  if (path.isAbsolute(relative) || relative.includes('\\') || relative.split('/').some(part => !part || part === '.' || part === '..')) return null;
  return relative.split('/').map(encodeURIComponent).join('/');
}
function link(url, label) {
  if (!url) return escape(label);
  if (!URL.canParse(url)) {
    const href = artifactHref(url);
    if (!href) throw new Error('Unsupported report link: evidence paths must stay inside the artifact directory');
    return `<a href="${escape(href)}" target="_blank" rel="noopener noreferrer">${escape(label)}</a>`;
  }
  const parsed = new URL(url);
  if (!['https:', 'http:', 'farmslot:', 'farmslot-dev:'].includes(parsed.protocol) || parsed.username || parsed.password)
    throw new Error('Unsupported report link');
  return `<a href="${escape(url)}" target="_blank" rel="noopener noreferrer">${escape(label)}</a>`;
}
const badge = verdict => `<span class="badge ${verdict === 'PASS' ? 'pass' : verdict === 'FAIL' ? 'fail' : verdict === 'UNTESTABLE' ? 'unknown' : 'gap'}">${escape(verdict === 'UNTESTABLE' ? 'NOT PROVED' : verdict)}</span>`;
function coverage(criteria) {
  const passed = criteria.filter(c => c.verdict === 'PASS').length;
  const failed = criteria.filter(c => c.verdict === 'FAIL').length;
  return { passed, total: criteria.length, tone: failed ? 'fail' : passed === criteria.length && criteria.length ? 'pass' : passed ? 'gap' : 'unknown',
    label: failed ? 'Failure found' : passed === criteria.length && criteria.length ? 'Fully validated' : passed ? 'Partially validated' : 'Not validated' };
}
// One grouping of criteria by source for the HTML sections, contents and pr-verdicts.json.
const criteriaFor = (data, sourceId) => data.criteria.filter(c => c.sourceId === sourceId);
const coverageBadge = rows => { const c = coverage(rows); return `<span class="badge ${c.tone}">${c.label}</span> <span class="coverage-count">${c.passed}/${c.total} criteria proved</span>`; };

const criterionBadge = criterion => criterion.verdict !== 'UNTESTABLE' ? badge(criterion.verdict) : `<span class="badge ${criterion.coverageState === 'blocked' ? 'gap' : 'unknown'}">${escape(({ 'not-run': 'NOT RUN', 'incomplete-evidence': 'INCOMPLETE PROOF', blocked: 'BLOCKED' })[criterion.coverageState] ?? 'NOT PROVED')}</span>`;


export async function renderReport(data, assetRoot) {
  required(data.title, 'Report title');
  required(data.verdict, 'Recorded overall verdict');
  required(data.summary, 'Reader summary');
  const build = data.testedBuild;
  if (build != null) {
    for (const field of ['name', 'version', 'branch', 'commit']) required(build[field], `Tested build ${field}`);
    if (!/^[a-f0-9]{40}$/i.test(build.commit)) throw new Error('Tested build commit must be the full HEAD SHA');
  }
  const buildIdentity = build
    ? `${escape(build.name)} ${escape(build.version)} · ${escape(build.branch)} @ <abbr title="${escape(build.commit)}">${escape(build.commit.slice(0, 8))}</abbr>`
    : 'Tested app version, branch and HEAD were not recorded.';
  if (!Array.isArray(data.sources) || !Array.isArray(data.criteria) || !data.criteria.length)
    throw new Error('Sources and frozen criteria are required');
  const sources = new Map();
  for (const source of data.sources) {
    required(source.id, 'Source id'); required(source.title, 'Human-readable source title');
    if (sources.has(source.id)) throw new Error(`Duplicate source ${source.id}`);
    sources.set(source.id, source);
  }
  const ids = new Set();
  for (const criterion of data.criteria) {
    required(criterion.id, 'Criterion id'); required(criterion.text, 'Frozen criterion text');
    if (ids.has(criterion.id)) throw new Error(`Duplicate criterion ${criterion.id}`);
    ids.add(criterion.id);
    if (!sources.has(criterion.sourceId)) throw new Error(`Missing readable source for ${criterion.id}`);
    if (!['PASS', 'FAIL', 'UNTESTABLE'].includes(criterion.verdict)) throw new Error(`Unknown verdict for ${criterion.id}`);
    required(criterion.detail, `Evidence or gap for ${criterion.id}`);
    if (criterion.coverageState !== undefined && !['not-run','incomplete-evidence','blocked'].includes(criterion.coverageState))
      throw new Error(`Classify the coverage gap for ${criterion.id}`);
    if (criterion.coverageState === 'blocked' && !criterion.blockerEvidence?.length)
      throw new Error(`Retained prerequisite/capability evidence is required for blocked ${criterion.id}`);
    for (const evidence of criterion.blockerEvidence ?? []) required(evidence.label, 'Blocker evidence label');
  }
  // Selection is supplied by the retained pre-execution plan, never inferred
  // from whichever cases happened to pass. Legacy exports have no plan.
  let selectedIds;
  const exclusions = new Map();
  if (data.plan) {
    required(data.plan.level, 'Assurance level');
    required(data.plan.evidence?.label, 'Retained plan evidence');
    if (!Array.isArray(data.plan.selectedCriterionIds) || !data.plan.selectedCriterionIds.length || !Array.isArray(data.plan.exclusions))
      throw new Error('Plan requires selected criteria and explicit exclusions');
    selectedIds = new Set(data.plan.selectedCriterionIds);
    if (selectedIds.size !== data.plan.selectedCriterionIds.length)
      throw new Error('Duplicate selected criterion');
    for (const excluded of data.plan.exclusions) {
      required(excluded.reason, 'Pre-execution exclusion rationale');
      if (selectedIds.has(excluded.criterionId) || exclusions.has(excluded.criterionId))
        throw new Error('Plan selections and exclusions must not overlap');
      exclusions.set(excluded.criterionId, excluded.reason);
    }
    const plannedIds = new Set([...selectedIds, ...exclusions.keys()]);
    if (plannedIds.size !== ids.size || [...plannedIds].some(id => !ids.has(id)))
      throw new Error('Plan must account for every inventoried criterion exactly once');
  }
  const displayBadge = c => exclusions.has(c.id) && c.verdict === 'UNTESTABLE' ? '<span class="badge unknown">OUTSIDE THIS PLAN</span>' : criterionBadge(c);
  const planCoverage = (rows, includeUnselectedFailures = false) => {
    const selected = rows.filter(c => selectedIds.has(c.id));
    const passed = selected.filter(c => c.verdict === 'PASS').length;
    const failed = (includeUnselectedFailures ? rows : selected).some(c => c.verdict === 'FAIL');
    const complete = selected.length > 0 && passed === selected.length;
    return `<span class="badge ${failed ? 'fail' : complete ? 'pass' : selected.length ? 'gap' : 'unknown'}">${failed ? (includeUnselectedFailures ? 'Failure found' : 'Selected checks failed') : complete ? 'Selected checks passed' : selected.length ? 'Selected checks incomplete' : 'Outside this plan'}</span> <span class="coverage-count">${passed}/${selected.length} selected checks proved; ${rows.filter(c => c.verdict === 'PASS').length}/${rows.length} full criteria proved</span>`;
  };
  const sourceCoverage = rows => selectedIds ? planCoverage(rows, true) : coverageBadge(rows);
  const images = [];
  const root = await realpath(assetRoot);
  for (const asset of data.images ?? []) {
    required(asset.caption, 'Evidence caption');
    const file = await realpath(path.resolve(root, asset.path));
    if (!file.startsWith(root + path.sep)) throw new Error('Images must be inside the report asset directory');
    const bytes = await readFile(file);
    const mime = bytes.subarray(0, 8).equals(Buffer.from([137,80,78,71,13,10,26,10])) ? 'image/png'
      : bytes[0] === 255 && bytes[1] === 216 && bytes[2] === 255 ? 'image/jpeg' : null;
    if (!mime) throw new Error('Only PNG and JPEG evidence may be embedded');
    const criterionIds = asset.criterionIds ?? [];
    if (criterionIds.some(id => !ids.has(id))) throw new Error('Image references an unknown criterion');
    images.push({ criterionIds, html: `<figure><img src="data:${mime};base64,${bytes.toString('base64')}" alt="${escape(asset.caption)}"><figcaption>${escape(asset.caption)}</figcaption></figure>` });
  }
  const media = [];
  for (const video of data.videos ?? []) {
    required(video.path, 'Recording path'); required(video.caption, 'Recording caption');
    const href = artifactHref(video.path);
    if (!href || !/\.(mp4|webm|mov)$/i.test(video.path))
      throw new Error('Recording must be a relative media path inside the artifact directory');
    const file = await realpath(path.join(root, video.path));
    if (!file.startsWith(root + path.sep)) throw new Error('Recording escapes the artifact directory');
    const criterionIds = video.criterionIds ?? [];
    if (criterionIds.some(id => !ids.has(id))) throw new Error('Recording references an unknown criterion');
    let markers = [];
    if (video.timelinePath) {
      const timelineFile = await realpath(path.resolve(root, video.timelinePath));
      if (!timelineFile.startsWith(root + path.sep)) throw new Error('Timeline escapes the artifact directory');
      const timeline = JSON.parse(await readFile(timelineFile, 'utf8'));
      const lock = JSON.parse(await readFile(path.join(root, 'harness-provenance.json'), 'utf8'));
      const require = createRequire(path.join(lock.source.packageRoot, 'package.json'));
      const protocol = await import(pathToFileURL(require.resolve('@farmslot/protocol')).href);
      if (typeof protocol.validateRecipeRecordingTimelineDocument !== 'function' || protocol.validateRecipeRecordingTimelineDocument(timeline).status !== 'valid')
        throw new Error('Locked protocol must validate the recording timeline');
      const hash = createHash('sha256');
      for await (const bytes of createReadStream(file)) hash.update(bytes);
      if (timeline.videoDigest !== `sha256:${hash.digest('hex')}`) throw new Error('Timeline video digest mismatch');
      if (video.path !== timeline.videoPath && !video.path.endsWith('/' + timeline.videoPath)) throw new Error('Timeline video path mismatch');
      const packageRoot = video.path.slice(0, video.path.length - timeline.videoPath.length);
      const traceFile = await realpath(path.join(root, packageRoot, 'trace.json'));
      if (!traceFile.startsWith(root + path.sep)) throw new Error('Trace escapes the artifact directory');
      const raw = JSON.parse(await readFile(traceFile, 'utf8'));
      const trace = Array.isArray(raw) ? raw : raw.entries;
      if (!Array.isArray(trace) || protocol.digestRecipeDocument(trace) !== timeline.traceDigest) throw new Error('Timeline trace digest mismatch');
      markers = (video.markers ?? []).map(reference => {
        const marker = timeline.markers.find(marker => marker.traceIndex === reference.traceIndex);
        const entry = trace[reference.traceIndex];
        if (!marker || marker.nodeId !== entry?.nodeId || marker.action !== entry?.action || marker.ok !== entry?.ok) throw new Error('Recording marker is not in its execution trace');
        if (!(reference.criterionIds ?? []).length || reference.criterionIds.some(id => !criterionIds.includes(id))) throw new Error('Marker criterion must belong to this recording');
        const at = Date.parse(entry.endedAt);
        const start = at - timeline.clock.latestZeroUnixMs, end = at - timeline.clock.earliestZeroUnixMs;
        if (!Number.isFinite(at) || start !== marker.endRangeMs[0] || end !== marker.endRangeMs[1]) throw new Error('Recording marker time mismatch');
        const seconds = (start + end) / 2000;
        const label = required(reference.label, 'Readable video marker label');
        return { criterionIds: reference.criterionIds, html: seconds < 0 || seconds * 1000 >= timeline.durationMs
          ? `<p>${escape(label)}: outside recorded footage.</p>`
          : `<p><a href="${escape(href)}#t=${seconds.toFixed(3)}" data-trace-index="${marker.traceIndex}" data-trace-phase="end">Watch ${escape(label)} at ${seconds.toFixed(2)}s</a> <small>Clock window ${Math.ceil(end - start)} ms; visual capture can be sparser. ${escape(entry.nodeId)}</small></p>` };
      });
    } else if (video.markers?.length) throw new Error('Recording markers require a retained timeline');
    media.push({ criterionIds, html: `<figure><video controls preload="metadata" src="${escape(href)}" aria-label="${escape(video.caption)}"></video><figcaption>${escape(video.caption)}</figcaption></figure>`, markers });
  }
  const count = verdict => data.criteria.filter(c => c.verdict === verdict).length;
  const sections = [...sources.values()].map((source, sourceIndex) => {
    const criteria = criteriaFor(data, source.id);
    const relevant = criteria.filter(c => !exclusions.has(c.id) || c.verdict !== 'UNTESTABLE');
    const passed = relevant.filter(c => c.verdict === 'PASS').length;
    const rows = criteria.map(c => `<details${exclusions.has(c.id) && c.verdict === 'UNTESTABLE' ? '' : ' open'} class="criterion" data-verdict="${c.verdict}" data-outside-plan="${exclusions.has(c.id)}">
      <summary>${displayBadge(c)}<strong>${escape(c.title || c.text.split('\n')[0].replace(/^Scenario:\s*/, ''))}</strong><code>${escape(c.id)}</code></summary>
      <div id="ac-${data.criteria.indexOf(c)+1}" class="criterion-body"><p class="note">Recorded verdict: ${escape(c.verdict)}${c.verdict === 'UNTESTABLE' ? ' · A missing proof is not evidence that this interaction is impossible to test.' : ''}</p><p class="eyebrow">Frozen acceptance criterion</p><div class="verbatim">${escape(c.text)}</div>
      <p><strong>${c.verdict === 'PASS' ? 'What was proved' : c.verdict === 'FAIL' ? 'What failed' : 'What remains unproved'}:</strong> ${escape(c.detail)}</p>
      ${exclusions.has(c.id) ? `<p><strong>Outside this run's plan:</strong> ${escape(exclusions.get(c.id))}</p>` : ''}
      ${(c.evidence ?? []).length ? `<ul>${c.evidence.map(e => `<li>${link(e.url, required(e.label, 'Evidence label'))}${e.note ? ` · ${escape(e.note)}` : ''}</li>`).join('')}</ul>` : ''}
      ${(c.blockerEvidence ?? []).length ? `<p><strong>Observed blocker evidence</strong></p><ul>${c.blockerEvidence.map(e => `<li>${link(e.url, e.label)}</li>`).join('')}</ul>` : ''}
      ${images.filter(image => image.criterionIds.includes(c.id)).map(image => image.html).join('')}
      ${media.filter(video => video.criterionIds.includes(c.id)).map(video => video.html + video.markers.filter(marker => marker.criterionIds.includes(c.id)).map(marker => marker.html).join('')).join('')}
      </div></details>`).join('');
    return `<section id="change-${sourceIndex+1}" class="change" data-status="${!relevant.length ? 'OUTSIDE' : passed === relevant.length ? 'PASS' : 'GAP'}"><header><div><p class="eyebrow">${escape(source.label || source.id)}</p><h2>${link(source.url, source.title)}</h2></div><span class="coverage">${sourceCoverage(criteria)}</span></header>${rows || '<p>No criteria recorded for this selected change.</p>'}</section>`;
  }).join('\n');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(data.title)}</title>
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; media-src 'self'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
  <style>
  :root{color-scheme:light;font:16px/1.55 system-ui,-apple-system,sans-serif;color:#202b3b;background:#f2f5f8}*{box-sizing:border-box}html{scroll-padding-top:78px}.quick-nav{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid #cdd8e5;display:flex;align-items:center;gap:18px;padding:12px 24px;box-shadow:0 2px 8px #2030500a}.quick-nav>a{font-size:14px;font-weight:650;white-space:nowrap}.quick-nav>details{position:relative;font-size:14px;flex:1}.quick-nav summary{cursor:pointer;font-weight:650}.quick-nav ol{position:absolute;top:25px;left:0;max-height:65vh;width:min(650px,80vw);overflow:auto;margin:0;padding:16px 28px;background:#fff;border:1px solid #cdd8e5;border-radius:8px;box-shadow:0 8px 24px #20305020}.quick-nav li{padding:6px 0}.quick-nav .badge{display:inline-block;margin-top:4px}.quick-nav .coverage-count{display:inline}.quick-nav a:focus-visible{outline:2px solid #2452b8;outline-offset:3px}body{margin:0}main{max-width:1100px;margin:auto;padding:40px 24px 80px}h1{font-size:clamp(26px,4vw,42px);line-height:1.2;letter-spacing:-.035em;margin:10px 0 20px}h2{font-size:20px;line-height:1.35;margin:0}a{color:#2452b8;text-decoration-thickness:1px;text-underline-offset:3px}p{margin:12px 0}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.09em;color:#526274;margin:0 0 6px}.intro,.change,.findings,.scope,.next,.evidence,.toc{background:#fff;border:1px solid #dae2eb;border-radius:12px;padding:24px;margin:18px 0}.intro{border-top:5px solid #b96a08}.badge{font-size:12px;font-weight:750;border-radius:5px;padding:4px 8px;white-space:nowrap}.pass{color:#14623e;background:#dff4e7}.fail{color:#9d263b;background:#fde3e8}.gap{color:#80520c;background:#fff0cd}.unknown{color:#435266;background:#e9eef4}.coverage-count{font-size:12px;color:#526274;display:block;margin-top:5px}.toc li{padding:8px 0}.toc .badge{display:inline-block;margin:6px 4px 6px 0}.toc summary{cursor:pointer}.toc li:has(> .badge.pass){border-left:4px solid #269761}.toc li:has(> .badge.gap){border-left:4px solid #c38818}.toc li:has(> .badge.unknown){border-left:4px solid #8b98a8}.toc li:has(> .badge.fail){border-left:4px solid #b93850}.toc>ol>li{padding-left:12px}.metrics{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}.metric{background:#f5f7fa;border-radius:8px;padding:12px 18px;min-width:130px}.metric b{font-size:28px;display:block}.metric span{font-size:13px;color:#526274}.note{font-size:14px;color:#526274}.change>header{display:flex;align-items:flex-start;justify-content:space-between;gap:24px;margin-bottom:18px}.coverage{font-weight:700;white-space:nowrap}.criterion{border-top:1px solid #e3e8ef;padding:12px 0}.criterion summary{cursor:pointer;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}.criterion summary strong{flex:1;min-width:200px}.criterion code{color:#66768a;font-size:11px}.criterion:has(.criterion-body:target){outline:3px solid #7aa7e6;outline-offset:4px;display:block!important}.criterion:has(.criterion-body:target)>:not(summary){display:block!important}.change:has(.criterion-body:target){display:block!important}.criterion-body{padding:12px 0 4px 12px}.verbatim{white-space:pre-wrap;background:#f5f7fa;border-radius:8px;padding:16px;font-size:14px}.finding{border-top:1px solid #e3e8ef;margin-top:16px;padding-top:16px}.filter{display:inline-flex;gap:8px;border:1px solid #ccd6e2;border-radius:8px;padding:8px 14px;margin:8px 8px 8px 0;cursor:pointer;background:white}.report:has(#filter-gaps:checked) .criterion[data-outside-plan=true][data-verdict=UNTESTABLE],.report:has(#filter-gaps:checked) .change[data-status=OUTSIDE],.report:has(#filter-gaps:checked) .criterion[data-verdict=PASS],.report:has(#filter-gaps:checked) .change[data-status=PASS]{display:none}.report:has(#filter-pass:checked) .criterion:not([data-verdict=PASS]){display:none}.scope dl{display:grid;grid-template-columns:170px 1fr;gap:12px}.scope dt{font-weight:650}.scope dd{margin:0;overflow-wrap:anywhere}.scope summary{cursor:pointer;font-weight:700}figure{margin:24px 0}figure video{display:block;max-width:100%;max-height:600px;margin:auto}figure img{display:block;max-height:600px;max-width:100%;margin:auto;border:1px solid #d5dfe8;border-radius:8px}figcaption{font-size:14px;color:#526274;margin-top:10px;text-align:center}footer{font-size:12px;color:#66768a;overflow-wrap:anywhere}li{margin:8px 0}@media(max-width:600px){.quick-nav{gap:10px;padding:10px 12px;flex-wrap:wrap}.quick-nav>details{flex:initial}main{padding:20px 12px}.intro,.change,.findings,.scope,.next,.evidence,.toc{padding:16px}.scope dl{grid-template-columns:1fr}.change>header{gap:12px;flex-wrap:wrap}}@media print{.quick-nav{display:none}body{background:white}main{padding:0}.filter{display:none}.criterion-body{display:block!important}.change{break-inside:avoid}}
  </style></head><body><nav class="quick-nav" aria-label="Quick report navigation"><a href="#report-summary">Summary</a><a href="#report-findings">Findings</a><a href="#report-contents">Contents</a><details><summary>Jump to a change</summary><ol>${[...sources.values()].map((source,index) => `<li><a href="#change-${index+1}">${escape(source.label || source.id)} · ${escape(source.title)}</a> ${sourceCoverage(criteriaFor(data, source.id))}</li>`).join('')}</ol></details><a href="#report-next">Next steps</a></nav><main class="report"><p class="eyebrow">${escape(data.subtitle || 'QA validation report')}</p><h1>${escape(data.title)}</h1><p class="build-identity">${buildIdentity}</p>
  <section id="report-summary" class="intro">${badge(data.verdict)}<p>${escape(data.summary)}</p><div class="metrics"><div class="metric"><b>${data.criteria.length}</b><span>frozen criteria</span></div><div class="metric"><b>${count('PASS')}</b><span>proved</span></div><div class="metric"><b>${count('UNTESTABLE')}</b><span>not proved</span></div><div class="metric"><b>${count('FAIL')}</b><span>failed criteria</span></div></div><p class="note">${escape(data.boundary || 'Completion of the QA session does not imply every criterion passed or approval to release.')}</p></section>
  ${selectedIds ? `<section class="scope"><h2>Selected plan: ${escape(data.plan.level)}</h2><p>${planCoverage(data.criteria)}</p><p>Selection recorded in ${link(data.plan.evidence.url, data.plan.evidence.label)}. Full acceptance coverage remains separate from this plan's result.</p></section>` : ''}
  <section id="report-next" class="next"><h2>What happens next</h2><ol>${(data.nextSteps ?? []).map(s => `<li>${escape(s)}</li>`).join('')}</ol></section>
  <section id="report-findings" class="findings"><h2>Findings and coverage gaps</h2>${(data.findings ?? []).map(f => `<article class="finding"><p class="eyebrow">${escape(f.kind)} · ${escape(f.id)}</p><h2>${escape(f.title)}</h2><p>${escape(f.detail)}</p><p><strong>Next action:</strong> ${escape(f.nextAction)}</p></article>`).join('') || '<p>No findings recorded. Consult coverage below for unproved criteria.</p>'}</section>
  <nav id="report-contents" class="toc" aria-label="Report contents"><h2>Contents · validation by change</h2><p class="note">Statuses reflect all frozen criteria listed for each source in this run. They do not extend proof to another platform or build.</p><ol>${[...sources.values()].map((source,index) => `<li><a href="#change-${index+1}">${escape(source.label || source.id)} · ${escape(source.title)}</a><br>${sourceCoverage(criteriaFor(data, source.id))}<details open><summary>Acceptance criteria</summary><ul>${criteriaFor(data, source.id).map(c => `<li><a href="#ac-${data.criteria.indexOf(c)+1}">${escape(c.title || c.text.split('\n')[0])}</a> · ${displayBadge(c)}</li>`).join('')}</ul></details></li>`).join('')}</ol></nav>
  <h2>Changes and acceptance criteria</h2><p class="note">Each heading identifies its source. Criteria are expanded by default; collapse any scenario to shorten the report. IDs are traceability references, not the description.</p>
  <label class="filter"><input id="filter-all" type="radio" name="coverage" checked>All criteria</label><label class="filter"><input id="filter-gaps" type="radio" name="coverage">Needs follow-up</label><label class="filter"><input id="filter-pass" type="radio" name="coverage">Proved</label>
  ${sections}
  ${media.some(video => !video.criterionIds.length) ? `<section class="evidence"><h2>Recipe recordings</h2>${media.filter(video => !video.criterionIds.length).map(video => video.html).join('')}</section>` : ''}
  ${images.some(image => !image.criterionIds.length) ? `<section class="evidence"><h2>Reviewed screenshots</h2>${images.filter(image => !image.criterionIds.length).map(image => image.html).join('')}</section>` : ''}
  <details class="scope"><summary>Scope, build and provenance</summary><dl>${(data.scope ?? []).map(row => `<dt>${escape(row.label)}</dt><dd>${escape(row.value)}</dd>`).join('')}</dl></details>
  <footer><p>${escape(data.exportNote || 'This self-contained report embeds its text and screenshots. Linked raw traces and recordings remain in the original evidence store and require access to it.')}</p><p>${escape(data.provenance || '')}</p></footer></main></body></html>`;
}

// Roll up the worst recorded cause; excluded passes retain their prior-evidence label.
const ROLLUP_ORDER = ['FAIL', 'BLOCKED', 'NOT PROVED', 'DEFERRED', 'PASS (prior evidence)', 'PASS'];
export function prVerdicts(data, generatedFrom, generatedAt = new Date().toISOString()) {
  const excluded = new Set((data.plan?.exclusions ?? []).map(e => e.criterionId));
  const rollup = c => c.verdict === 'FAIL' ? 'FAIL' : c.verdict === 'PASS' ? (excluded.has(c.id) ? 'PASS (prior evidence)' : 'PASS')
    : c.coverageState === 'blocked' ? 'BLOCKED' : c.coverageState === 'not-run' || (!c.coverageState && excluded.has(c.id)) ? 'DEFERRED' : 'NOT PROVED';
  return { version: 1, generatedAt, generatedFrom, verdict: data.verdict, prs: data.sources.map(source => {
    const criteria = criteriaFor(data, source.id);
    const states = criteria.map(rollup);
    const { passed, total } = coverage(criteria);
    return { id: source.id, title: source.title, url: source.url ?? null, verdict: ROLLUP_ORDER.find(v => states.includes(v)) ?? 'NOT PROVED',
      proved: passed, total,
      criteria: criteria.map(c => ({ id: c.id, verdict: c.verdict, coverageState: c.coverageState ?? null, outsidePlan: excluded.has(c.id) })) };
  }) };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const option = name => args[args.indexOf(name) + 1];
  if (!args.includes('--input') || !args.includes('--out')) throw new Error('Usage: render-report.mjs --input report-data.json --out report.html [--assets artifacts-dir]');
  const input = path.resolve(option('--input'));
  const out = path.resolve(option('--out'));
  const bytes = await readFile(input);
  const data = JSON.parse(bytes.toString('utf8'));
  const output = await renderReport(data, path.resolve(args.includes('--assets') ? option('--assets') : path.dirname(input)));
  await writeFile(out, output);
  // Rewrite rollups with the HTML after every verdict change.
  const verdictsPath = path.join(path.dirname(out), 'pr-verdicts.json');
  const generatedFrom = { path: path.relative(path.dirname(verdictsPath), input), digest: `sha256:${createHash('sha256').update(bytes).digest('hex')}` };
  await writeFile(verdictsPath, JSON.stringify(prVerdicts(data, generatedFrom), null, 2) + '\n');
  console.log(`Rendered ${data.criteria.length} recorded criteria to ${option('--out')} and ${verdictsPath}`);
}
