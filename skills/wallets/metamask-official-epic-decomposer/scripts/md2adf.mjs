#!/usr/bin/env node
// md2adf.mjs: convert epic-decomposer ticket markdown to Atlassian Document Format
// (ADF), the JSON format Jira Cloud uses for issue descriptions.
//
// Usage:   node md2adf.mjs <ticket.md>
// Output:  the ADF document as JSON on stdout.
//
// It never writes files, uses the network, starts processes or evaluates code.
// file-tickets.mjs imports mdToAdf() from here.
//
// Supported markdown: the subset the ticket template uses.
//   # Heading (levels 1-6)           paragraphs (lines joined with a space)
//   **bold**  *italic*  `code`       [label](https://...)
//   - bullet items  /  1. numbered items (an indented line continues the item)
//   | table | rows | (a --- row under the first row makes it a header)
//   ```lang fenced code (kept verbatim)
//   > quote               -> info panel
//   > [!WARN] quote       -> warning panel
// Only http:, https: and mailto: targets become links. Any other target (for
// example javascript: or file:) keeps its label as plain text, because ticket
// text can come from scanned code and is not trusted.

import { readFileSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

// ---------------------------------------------------------------------------
// Inline text: bold, italic, code and links inside one line or paragraph.
// ---------------------------------------------------------------------------

function textNode(text, marks) {
  if (marks.length === 0) {
    return { type: 'text', text };
  }
  return { type: 'text', text, marks };
}

function isSafeLink(target) {
  const lower = target.toLowerCase();
  return lower.startsWith('https://') || lower.startsWith('http://') || lower.startsWith('mailto:');
}

// Turns a string into a list of ADF text nodes. `marks` are the marks of the
// enclosing text (for example bold around a link).
function parseInline(text, marks = []) {
  const nodes = [];
  let plain = '';
  let i = 0;

  function flushPlain() {
    if (plain !== '') {
      nodes.push(textNode(plain, marks));
      plain = '';
    }
  }

  while (i < text.length) {
    // `code`: ADF lets a code mark combine only with a link mark.
    if (text[i] === '`') {
      const end = text.indexOf('`', i + 1);
      if (end > i + 1) {
        flushPlain();
        const linkMarks = marks.filter((mark) => mark.type === 'link');
        nodes.push(textNode(text.slice(i + 1, end), [...linkMarks, { type: 'code' }]));
        i = end + 1;
        continue;
      }
    }

    // **bold**
    if (text.startsWith('**', i)) {
      const end = text.indexOf('**', i + 2);
      if (end > i + 2) {
        flushPlain();
        nodes.push(...parseInline(text.slice(i + 2, end), [...marks, { type: 'strong' }]));
        i = end + 2;
        continue;
      }
    }

    // *italic*. A star followed by a space is plain text, as in "2 * 3".
    if (text[i] === '*' && text[i + 1] !== ' ' && text[i + 1] !== '*') {
      const end = text.indexOf('*', i + 1);
      if (end > i + 1) {
        flushPlain();
        nodes.push(...parseInline(text.slice(i + 1, end), [...marks, { type: 'em' }]));
        i = end + 1;
        continue;
      }
    }

    // [label](target)
    if (text[i] === '[') {
      const labelEnd = text.indexOf('](', i + 1);
      const targetEnd = labelEnd === -1 ? -1 : text.indexOf(')', labelEnd + 2);
      if (labelEnd > i + 1 && targetEnd > labelEnd + 2) {
        flushPlain();
        const label = text.slice(i + 1, labelEnd);
        const target = text.slice(labelEnd + 2, targetEnd);
        const labelMarks = isSafeLink(target) ? [...marks, { type: 'link', attrs: { href: target } }] : marks;
        nodes.push(...parseInline(label, labelMarks));
        i = targetEnd + 1;
        continue;
      }
    }

    plain += text[i];
    i += 1;
  }

  flushPlain();
  return nodes;
}

function paragraph(text) {
  return { type: 'paragraph', content: parseInline(text) };
}

// ---------------------------------------------------------------------------
// Block types. Each read* function starts at lines[start] and returns
// { node, next }, where next is the index of the first line it did not use.
// ---------------------------------------------------------------------------

const LIST_ITEM = /^(\s*)(-|\*|\d+\.)\s+/; // "- item", "* item" or "1. item"

function isBlank(line) {
  return line.trim() === '';
}

function isFence(line) {
  return line.startsWith('```');
}

function headingLevel(line) {
  let level = 0;
  while (line[level] === '#') {
    level += 1;
  }
  return level >= 1 && level <= 6 && line[level] === ' ' ? level : 0;
}

function isQuote(line) {
  return line.startsWith('>');
}

function isTableRow(line) {
  return line.startsWith('|');
}

function isListItem(line) {
  return LIST_ITEM.test(line);
}

function startsBlock(line) {
  return isFence(line) || headingLevel(line) > 0 || isQuote(line) || isTableRow(line) || isListItem(line);
}

function readCodeBlock(lines, start) {
  const language = lines[start].slice(3).trim();
  const body = [];
  let i = start + 1;
  while (i < lines.length && !isFence(lines[i])) {
    body.push(lines[i]);
    i += 1;
  }
  const node = {
    type: 'codeBlock',
    attrs: language ? { language } : {},
    // ADF rejects empty text nodes, so an empty block has no content.
    content: body.length > 0 ? [{ type: 'text', text: body.join('\n') }] : [],
  };
  return { node, next: i + 1 }; // skip the closing fence
}

function readHeading(lines, start) {
  const level = headingLevel(lines[start]);
  const text = lines[start].slice(level + 1).trim();
  return { node: { type: 'heading', attrs: { level }, content: parseInline(text) }, next: start + 1 };
}

// A quote becomes a panel of plain paragraphs (blank quote lines split them).
function readQuote(lines, start) {
  const quoteLines = [];
  let i = start;
  while (i < lines.length && isQuote(lines[i])) {
    let line = lines[i].slice(1);
    if (line.startsWith(' ')) {
      line = line.slice(1);
    }
    quoteLines.push(line);
    i += 1;
  }

  let panelType = 'info';
  if (quoteLines[0].startsWith('[!WARN]')) {
    panelType = 'warning';
    quoteLines[0] = quoteLines[0].slice('[!WARN]'.length).trim();
  }

  const paragraphs = [];
  let current = [];
  for (const line of [...quoteLines, '']) {
    if (isBlank(line)) {
      if (current.length > 0) {
        paragraphs.push(paragraph(current.join(' ')));
        current = [];
      }
    } else {
      current.push(line.trim());
    }
  }
  if (paragraphs.length === 0) {
    paragraphs.push(paragraph(''));
  }

  return { node: { type: 'panel', attrs: { panelType }, content: paragraphs }, next: i };
}

function tableCells(row) {
  let inner = row.trim();
  if (inner.startsWith('|')) {
    inner = inner.slice(1);
  }
  if (inner.endsWith('|')) {
    inner = inner.slice(0, -1);
  }
  return inner.split('|').map((cell) => cell.trim());
}

function isSeparatorRow(row) {
  return tableCells(row).every((cell) => cell !== '' && [...cell].every((char) => char === '-' || char === ':'));
}

function readTable(lines, start) {
  const rows = [];
  let i = start;
  while (i < lines.length && isTableRow(lines[i])) {
    rows.push(lines[i]);
    i += 1;
  }

  const hasHeader = rows.length > 1 && isSeparatorRow(rows[1]);
  const contentRows = hasHeader ? [rows[0], ...rows.slice(2)] : rows;

  const tableRows = contentRows.map((row, rowIndex) => ({
    type: 'tableRow',
    content: tableCells(row).map((cell) => ({
      type: hasHeader && rowIndex === 0 ? 'tableHeader' : 'tableCell',
      content: [paragraph(cell)],
    })),
  }));
  return { node: { type: 'table', content: tableRows }, next: i };
}

function readList(lines, start) {
  const ordered = /\d/.test(lines[start].match(LIST_ITEM)[2]);
  const items = [];
  let i = start;
  while (i < lines.length && isListItem(lines[i])) {
    const marker = lines[i].match(LIST_ITEM);
    if (/\d/.test(marker[2]) !== ordered) {
      break; // a bullet list right after a numbered list starts a new list
    }
    let text = lines[i].slice(marker[0].length);
    i += 1;
    // An indented, non-blank line that is not a new item continues this item.
    while (i < lines.length && lines[i].startsWith(' ') && !isBlank(lines[i]) && !isListItem(lines[i])) {
      text += ` ${lines[i].trim()}`;
      i += 1;
    }
    items.push({ type: 'listItem', content: [paragraph(text)] });
  }
  return { node: { type: ordered ? 'orderedList' : 'bulletList', content: items }, next: i };
}

function readParagraph(lines, start) {
  const parts = [lines[start].trim()];
  let i = start + 1;
  while (i < lines.length && !isBlank(lines[i]) && !startsBlock(lines[i])) {
    parts.push(lines[i].trim());
    i += 1;
  }
  return { node: paragraph(parts.join(' ')), next: i };
}

// ---------------------------------------------------------------------------
// The whole document.
// ---------------------------------------------------------------------------

export function mdToAdf(markdown) {
  const lines = markdown.replaceAll('\r\n', '\n').split('\n');
  const content = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    if (isBlank(line)) {
      i += 1;
      continue;
    }

    let block;
    if (isFence(line)) {
      block = readCodeBlock(lines, i);
    } else if (headingLevel(line) > 0) {
      block = readHeading(lines, i);
    } else if (isQuote(line)) {
      block = readQuote(lines, i);
    } else if (isTableRow(line)) {
      block = readTable(lines, i);
    } else if (isListItem(line)) {
      block = readList(lines, i);
    } else {
      block = readParagraph(lines, i);
    }

    content.push(block.node);
    i = block.next;
  }

  return { type: 'doc', version: 1, content };
}

// Command line: only when run directly, not when imported.
const runDirectly = process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;
if (runDirectly) {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node md2adf.mjs <ticket.md>');
    process.exitCode = 2;
  } else {
    console.log(JSON.stringify(mdToAdf(readFileSync(file, 'utf8')), null, 2));
  }
}
