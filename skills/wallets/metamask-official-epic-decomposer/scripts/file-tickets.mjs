#!/usr/bin/env node
// file-tickets.mjs: file an epic-decomposer plan in Jira. It creates the epic,
// then the child tickets (with parent, labels, extra fields and a description
// converted by md2adf.mjs), then the Blocks links between them.
//
// Usage:
//   node file-tickets.mjs <plan.json>            dry run: print every request, send nothing
//   node file-tickets.mjs <plan.json> --apply    send the requests to Jira
//
// What it never does:
//   - It never sends the `ai-agent` label. That label starts cloud-agent
//     dispatch; a human adds it to the epic. It is removed from every label list.
//   - It never uses the network in a dry run (the default). With --apply it calls
//     only the Jira REST API at JIRA_BASE_URL, which must be https.
//   - It never prints the API token. The token is read from the environment and
//     only put in the Authorization header.
//   - It never writes any file except plan.json, and only with --apply.
//
// Environment (only read with --apply): JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN.
//
// plan.json (md paths are relative to plan.json, and must be .md files inside its folder):
//   {
//     "project": "ASSETS",
//     "fields": { "customfield_16983": { "value": "Not applicable" } },   (optional, set on every child)
//     "epic": { "summary": "...", "md": "epic.md", "labels": ["quality"] },  (or { "key": "ASSETS-1" } to reuse one)
//     "tickets": [
//       { "id": "P1-A1", "summary": "...", "md": "tickets/P1-A1.md", "labels": ["quality"] },
//       { "id": "P1-A2", "summary": "...", "md": "tickets/P1-A2.md", "labels": ["quality"], "blockedBy": ["P1-A1"] }
//     ]
//   }
//
// Tickets are created blockers first. With --apply, each new key (and each link
// made) is saved back to plan.json straight away, so a run that fails part-way
// can be re-run without creating duplicates. In ticket text, "<P1-A1>" is
// replaced with that ticket's key once it has one.

import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

import { mdToAdf } from './md2adf.mjs';

const FORBIDDEN_LABEL = 'ai-agent';
const MAX_DESCRIPTION_CHARS = 32767; // Jira's limit for a description, measured as ADF JSON
const PROJECT_KEY = /^[A-Z][A-Z0-9_]+$/;
const ISSUE_KEY = /^[A-Z][A-Z0-9_]+-\d+$/;
const USAGE = 'Usage: node file-tickets.mjs <plan.json> [--dry-run | --apply]';

// ---------------------------------------------------------------------------
// Command line
// ---------------------------------------------------------------------------

function parseArgs(args) {
  let apply = false;
  let dryRun = false;
  const files = [];
  for (const arg of args) {
    if (arg === '--apply') {
      apply = true;
    } else if (arg === '--dry-run') {
      dryRun = true;
    } else if (arg.startsWith('-')) {
      throw new Error(`unknown option ${arg}. ${USAGE}`);
    } else {
      files.push(arg);
    }
  }
  if (files.length !== 1 || (apply && dryRun)) {
    throw new Error(USAGE);
  }
  return { planPath: path.resolve(files[0]), apply };
}

// ---------------------------------------------------------------------------
// Plan checks: everything is validated before the first request is sent.
// ---------------------------------------------------------------------------

// An md file must be a .md file inside the plan folder, so a plan can never
// send some other file on this machine to Jira.
function checkMdPath(planDir, mdFile, owner) {
  const file = path.resolve(planDir, String(mdFile));
  const relative = path.relative(planDir, file);
  if (relative.startsWith('..') || path.isAbsolute(relative) || !file.endsWith('.md')) {
    throw new Error(`${owner}: md path must be a .md file inside the plan folder: ${mdFile}`);
  }
}

function checkPlan(plan, planDir) {
  if (!PROJECT_KEY.test(plan.project ?? '')) {
    throw new Error('plan.project must be a Jira project key, for example "ASSETS"');
  }
  if (!plan.epic || (!plan.epic.key && !(plan.epic.summary && plan.epic.md))) {
    throw new Error('plan.epic needs either a key, or a summary and an md file');
  }
  if (plan.epic.key && !ISSUE_KEY.test(plan.epic.key)) {
    throw new Error(`plan.epic.key "${plan.epic.key}" is not a Jira issue key`);
  }
  if (!plan.epic.key) {
    checkMdPath(planDir, plan.epic.md, 'the epic');
  }
  if (!Array.isArray(plan.tickets)) {
    throw new Error('plan.tickets must be a list');
  }
  const ids = new Set();
  for (const ticket of plan.tickets) {
    if (!ticket.id || !ticket.summary || !ticket.md) {
      throw new Error('every ticket needs an id, a summary and an md file');
    }
    checkMdPath(planDir, ticket.md, ticket.id);
    if (ids.has(ticket.id)) {
      throw new Error(`ticket id ${ticket.id} is used twice`);
    }
    if (ticket.key && !ISSUE_KEY.test(ticket.key)) {
      throw new Error(`${ticket.id}: key "${ticket.key}" is not a Jira issue key`);
    }
    ids.add(ticket.id);
  }
  for (const ticket of plan.tickets) {
    for (const blocker of ticket.blockedBy ?? []) {
      if (!ids.has(blocker)) {
        throw new Error(`${ticket.id} is blocked by unknown ticket ${blocker}`);
      }
    }
  }
}

// Returns the tickets so that every ticket comes after all of its blockers.
function blockersFirst(tickets) {
  const ordered = [];
  const done = new Set();
  while (ordered.length < tickets.length) {
    const ready = tickets.find(
      (ticket) => !done.has(ticket.id) && (ticket.blockedBy ?? []).every((blocker) => done.has(blocker)),
    );
    if (!ready) {
      throw new Error('the blockedBy edges form a cycle');
    }
    ordered.push(ready);
    done.add(ready.id);
  }
  return ordered;
}

// ---------------------------------------------------------------------------
// Labels and descriptions
// ---------------------------------------------------------------------------

// Removes `ai-agent` (in any letter case) from a label list.
function withoutAiAgent(labels = []) {
  return labels.filter((label) => String(label).trim().toLowerCase() !== FORBIDDEN_LABEL);
}

// Converts a ticket's markdown to ADF. "<id>" becomes the ticket's key when it
// has one; otherwise it becomes `placeholderKey` (used by the size check, which
// runs before any key exists, so it passes the longest key Jira could return).
function describe(plan, planDir, mdFile, owner, placeholderKey) {
  let markdown = readFileSync(path.resolve(planDir, mdFile), 'utf8');
  for (const ticket of plan.tickets) {
    const key = ticket.key ?? placeholderKey;
    if (key) {
      markdown = markdown.replaceAll(`<${ticket.id}>`, key);
    }
  }
  const adf = mdToAdf(markdown);
  if (JSON.stringify(adf).length > MAX_DESCRIPTION_CHARS) {
    throw new Error(`${owner}: the description is over Jira's ${MAX_DESCRIPTION_CHARS}-character limit. Split the ticket.`);
  }
  return adf;
}

// ---------------------------------------------------------------------------
// Jira client. Only created with --apply.
// ---------------------------------------------------------------------------

function jiraClient(env) {
  const { JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN } = env;
  if (!JIRA_BASE_URL || !JIRA_EMAIL || !JIRA_API_TOKEN) {
    throw new Error('--apply needs JIRA_BASE_URL, JIRA_EMAIL and JIRA_API_TOKEN in the environment');
  }
  const base = new URL(JIRA_BASE_URL);
  if (base.protocol !== 'https:') {
    throw new Error('JIRA_BASE_URL must start with https://');
  }
  const authorization = `Basic ${Buffer.from(`${JIRA_EMAIL}:${JIRA_API_TOKEN}`).toString('base64')}`;

  // apiPath is always one of the fixed /rest/api/3/... paths below, so every
  // request goes to the JIRA_BASE_URL origin.
  return async function post(apiPath, body) {
    const response = await fetch(new URL(apiPath, base.origin), {
      method: 'POST',
      headers: { Authorization: authorization, Accept: 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const text = await response.text();
    if (!response.ok) {
      // Jira's error body never contains our token; cut it short anyway.
      throw new Error(`POST ${apiPath} failed with ${response.status}: ${text.slice(0, 500)}`);
    }
    return text ? JSON.parse(text) : {};
  };
}

// ---------------------------------------------------------------------------
// Filing
// ---------------------------------------------------------------------------

async function main() {
  const { planPath, apply } = parseArgs(process.argv.slice(2));
  const planDir = path.dirname(planPath);
  const plan = JSON.parse(readFileSync(planPath, 'utf8'));
  checkPlan(plan, planDir);
  const tickets = blockersFirst(plan.tickets);

  // Fail on an oversized description before anything is sent.
  const longestKey = `${plan.project}-99999`;
  if (!plan.epic.key) {
    describe(plan, planDir, plan.epic.md, 'the epic', longestKey);
  }
  for (const ticket of tickets) {
    describe(plan, planDir, ticket.md, ticket.id, longestKey);
  }

  const post = apply ? jiraClient(process.env) : null;

  // Prints the request, then sends it only with --apply.
  async function send(apiPath, body) {
    console.log(`${apply ? '' : '[dry-run] '}POST ${apiPath}`);
    console.log(JSON.stringify(body, null, 2));
    if (!apply) {
      return {};
    }
    return post(apiPath, body);
  }

  function savePlan() {
    if (apply) {
      writeFileSync(planPath, `${JSON.stringify(plan, null, 2)}\n`);
    }
  }

  function labelsFor(labels, owner) {
    const kept = withoutAiAgent(labels);
    if (kept.length !== (labels ?? []).length) {
      console.log(`note: removed "${FORBIDDEN_LABEL}" from ${owner}. A human adds it to the epic to start dispatch.`);
    }
    return kept;
  }

  // 1. The epic, unless the plan reuses an existing one.
  if (!plan.epic.key) {
    const created = await send('/rest/api/3/issue', {
      fields: {
        project: { key: plan.project },
        issuetype: { name: 'Epic' },
        summary: plan.epic.summary,
        labels: labelsFor(plan.epic.labels, 'the epic'),
        description: describe(plan, planDir, plan.epic.md, 'the epic'),
      },
    });
    plan.epic.key = created.key;
    savePlan();
  }
  const epicKey = plan.epic.key ?? '<epic>';

  // 2. The children, blockers first, so "<id>" placeholders can be filled in.
  for (const ticket of tickets) {
    if (ticket.key) {
      console.log(`skip ${ticket.id}: already filed as ${ticket.key}`);
      continue;
    }
    const created = await send('/rest/api/3/issue', {
      fields: {
        ...plan.fields,
        project: { key: plan.project },
        issuetype: { name: 'Task' },
        parent: { key: epicKey },
        summary: ticket.summary,
        labels: labelsFor(ticket.labels, ticket.id),
        description: describe(plan, planDir, ticket.md, ticket.id),
      },
    });
    ticket.key = created.key;
    savePlan();
  }

  // 3. The Blocks links, after every child exists. Outward = the blocker.
  const keyOf = (id) => plan.tickets.find((ticket) => ticket.id === id).key ?? `<${id}>`;
  let linkCount = 0;
  for (const ticket of tickets) {
    for (const blocker of ticket.blockedBy ?? []) {
      if ((ticket.linked ?? []).includes(blocker)) {
        continue;
      }
      await send('/rest/api/3/issueLink', {
        type: { name: 'Blocks' },
        outwardIssue: { key: keyOf(blocker) },
        inwardIssue: { key: keyOf(ticket.id) },
      });
      linkCount += 1;
      if (apply) {
        ticket.linked = [...(ticket.linked ?? []), blocker];
        savePlan();
      }
    }
  }

  if (apply) {
    console.log(`Filed under ${epicKey}: ${tickets.length} children, ${linkCount} Blocks links.`);
    console.log(`Add "${FORBIDDEN_LABEL}" to the epic when you want agents to start.`);
  } else {
    console.log(`Dry run: ${tickets.length} children, ${linkCount} Blocks links. Nothing was sent.`);
    console.log('Re-run with --apply to file them.');
  }
}

const runDirectly = process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;
if (runDirectly) {
  main().catch((error) => {
    console.error(`error: ${error.message}`);
    process.exitCode = 1;
  });
}
