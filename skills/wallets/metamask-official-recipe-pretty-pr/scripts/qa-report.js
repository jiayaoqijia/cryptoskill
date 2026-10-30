const fs = require('node:fs');
const path = require('node:path');

const escape = value => String(value).replace(/[&<>]/gu, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]);

// QA keeps one human report. Its renderer input supplies the GitHub comment
// summary; the HTML is published intact, never pasted into a Markdown body.
function readQaReport(taskDir) {
  const htmlPath = path.join(taskDir, 'artifacts', 'report.html');
  if (!fs.existsSync(htmlPath)) return null;
  if (!fs.readFileSync(htmlPath, 'utf8').trim()) throw new Error('QA_REPORT_EMPTY: artifacts/report.html is empty.');
  const dataPath = path.join(taskDir, 'artifacts', 'report-data.json');
  const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  for (const field of ['title', 'verdict', 'summary']) {
    if (typeof data[field] !== 'string' || !data[field].trim()) {
      throw new Error(`QA_REPORT_INVALID: report-data.json needs ${field}.`);
    }
  }
  const text = [
    `## ${escape(data.title)}`,
    '',
    `Verdict: ${escape(data.verdict)}`,
    '',
    escape(data.summary),
    '',
    escape(data.boundary || 'Execution completion is not release approval.'),
  ].join('\n');
  return { htmlPath, dataPath, text };
}

module.exports = { readQaReport };
