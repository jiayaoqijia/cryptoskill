import assert from "node:assert/strict";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const SCRIPT_ROOT = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = join(SCRIPT_ROOT, "..");
const ALLOWED_COMMAND = /^node <skill-root>\/scripts\/[a-z0-9-]+\.mjs(?:\s+.*)?$/u;

const markdownFiles = (directory) =>
  readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      return markdownFiles(path);
    }
    return entry.name.endsWith(".md") ? [path] : [];
  });

export const terminalExamples = (markdown) =>
  [...markdown.matchAll(/```(?:bash|sh|shell)\n(?<body>[\s\S]*?)```/gu)]
    .flatMap((match) => match.groups.body.split("\n"))
    .map((line) => line.trim())
    .filter(Boolean);

test("reject names discovery commands", () => {
  const skill = readFileSync(join(SKILL_ROOT, "skill.md"), "utf8");
  const reject = skill.split("## Reject")[1] ?? "";
  for (const command of ["ls", "find", "cat", "git", "gh"]) {
    assert.match(reject, new RegExp(`\`${command}\``));
  }
});

test("reject forbids GitHub page fetches", () => {
  const skill = readFileSync(join(SKILL_ROOT, "skill.md"), "utf8");
  const reject = skill.split("## Reject")[1] ?? "";
  for (const phrase of [
    "`github.com`",
    "`raw.githubusercontent.com`",
    "`collect-pr-context.mjs`",
    "`read-frozen-file.mjs`",
  ]) {
    assert.ok(reject.includes(phrase), phrase);
  }
});

test("skill.md links every references markdown file", () => {
  const skill = readFileSync(join(SKILL_ROOT, "skill.md"), "utf8");
  const references = readdirSync(join(SKILL_ROOT, "references")).filter((name) =>
    name.endsWith(".md"),
  );
  assert.ok(references.length > 0);
  for (const name of references) {
    assert.match(skill, new RegExp(`references/${name}`));
  }
});

test("installed review instructions expose only checked-in scripts", () => {
  const mainInstruction = ["skill.md", "RULE.md", "SKILL.md"]
    .map((name) => join(SKILL_ROOT, name))
    .find(existsSync);
  assert.ok(mainInstruction);

  const instructionFiles = [
    mainInstruction,
    ...markdownFiles(join(SKILL_ROOT, "references")),
    ...(existsSync(join(SKILL_ROOT, "repos")) ? markdownFiles(join(SKILL_ROOT, "repos")) : []),
  ];
  const commands = instructionFiles.flatMap((path) => terminalExamples(readFileSync(path, "utf8")));

  assert.ok(commands.length > 0);
  assert.deepEqual(
    commands.filter((command) => !ALLOWED_COMMAND.test(command)),
    [],
  );
});
