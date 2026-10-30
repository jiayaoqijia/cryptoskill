import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import path from "node:path";
import test, { describe } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

// Use the same published runtime as the selected harness, without modifying it.
describe("published harness CI templates", {
  skip: !process.env.MM_HARNESS_BIN && "Set MM_HARNESS_BIN to the published harness executable.",
}, async () => {
  const require = createRequire(path.resolve(process.env.MM_HARNESS_BIN));
  const runtime = await import(
    pathToFileURL(require.resolve("@farmslot/agent-runtime")).href
  );
  const protocol = await import(
    pathToFileURL(require.resolve("@farmslot/protocol")).href
  );
  const catalog = fileURLToPath(
    new URL("../../references/templates/", import.meta.url),
  );

  for (const flow of ["dev", "fix-bug"]) {
    for (const platform of ["core", "mobile", "extension"]) {
      for (const enabled of [false, true]) {
        test(`${flow}/${platform} ${enabled ? "omits configured local CI" : "does not invent local CI"}`, async (t) => {
          const root = await mkdtemp(path.join(tmpdir(), "workflow-ci-template-"));
          t.after(() => rm(root, { recursive: true, force: true }));
          const result = await runtime.taskInit({
            taskDir: path.join(root, "task"), flow, platform,
            template: {
              sources: [{ id: "package:consensys-recipe-cook", kind: "package", root: catalog, layout: "flow-tree" }],
              explicitId: `${flow}/${platform}`,
            },
            task: { title: "Declared CI contract", sourceKind: "text" },
            handoff: { surface: "recipe-cook", project: "catalog-proof" },
            vars: enabled ? { "ci.local_check": "printf workflow-ci-pass", CI_PARITY_CHECKLIST: "CHECKLIST.md" } : {},
          });
          const markdown = await readFile(result.checklist, "utf8");
          const contract = JSON.parse(await readFile(result.terminalContract, "utf8"));
          assert.equal(result.executionTemplate.id, `${flow}/${platform}`);
          assert.doesNotMatch(markdown, /\{\{CI_PARITY_STEP\}\}/);
          assert.equal(contract.deterministicChecks?.length ?? 0, 0);
          assert.doesNotMatch(markdown, /DETERMINISTIC: ci\.local_check/);
        });
      }
    }
  }

  for (const enabled of [false, true]) {
    test(`QA materialization ${enabled ? "omits configured local CI" : "preserves projects without local CI"}`, async (t) => {
      const root = await mkdtemp(path.join(tmpdir(), "qa-ci-template-"));
      t.after(() => rm(root, { recursive: true, force: true }));
      const taskDir = path.join(root, "task");
      const result = await runtime.taskInit({
        taskDir,
        flow: "qa",
        platform: "extension",
        runMode: "validation",
        template: {
          sources: [
            {
              id: "package:consensys-recipe-cook",
              kind: "package",
              root: catalog,
              layout: "flow-tree",
            },
          ],
          explicitId: "qa/default",
        },
        task: { title: "Frozen QA scope", sourceKind: "text" },
        handoff: { surface: "recipe-cook", project: "catalog-proof" },
        vars: {
          TASK_DIR: taskDir,
          ...(enabled
            ? {
                "ci.local_check": "printf qa-ci-pass",
                CI_PARITY_CHECKLIST: "CHECKLIST.md",
              }
            : {}),
        },
      });
      const markdown = await readFile(result.checklist, "utf8");
      const steps = protocol.enumerateChecklistCheckboxes(markdown);
      const contract = JSON.parse(
        await readFile(result.terminalContract, "utf8"),
      );
      assert.equal(result.executionTemplate.id, "qa/default");
      assert.match(steps[4].rawLabel, /Execute and assess the selected cases/);
      assert.match(markdown, /sub start qa-cases --step 5/);
      assert.equal(steps.length, 7);
      assert.doesNotMatch(markdown, /\{\{CI_PARITY_STEP\}\}/);
      assert.equal(contract.deterministicChecks?.length ?? 0, 0);
      assert.doesNotMatch(markdown, /DETERMINISTIC: ci\.local_check/);
      assert.match(
        steps.at(-1).rawLabel,
        /Complete through the task's mark wrapper/,
      );
    });
  }
});
