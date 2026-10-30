import assert from 'node:assert/strict';
import { createHash, randomUUID } from 'node:crypto';
import { mkdir, open, readFile, realpath, rename, unlink, writeFile } from 'node:fs/promises';
import path from 'node:path';

const bytes = (value) => JSON.stringify(value, null, 2) + '\n';
const digest = (value) => createHash('sha256').update(value).digest('hex');

/** Advance the existing farm binding only after retaining and validating its successor. */
export async function reselectQa(task, index, finalizeQa) {
  task = await realpath(task);
  const artifacts = await realpath(path.join(task, 'artifacts'));
  assert.equal(artifacts, path.join(task, 'artifacts'), 'QA artifact root is redirected');
  const lockPath = path.join(artifacts, '.qa-reselection.lock');
  const lock = await open(lockPath, 'wx');
  const temporary = path.join(artifacts, `.qa-result-${randomUUID()}.tmp`);
  let temporaryCreated = false;
  try {
    const selectedPath = path.join(artifacts, 'qa-result.json');
    assert.equal(await realpath(selectedPath), selectedPath, 'QA selection is redirected');
    const previousBytes = await readFile(selectedPath, 'utf8');
    const previous = JSON.parse(previousBytes);
    const input = JSON.parse(await readFile(path.join(task, 'inputs/qa.json'), 'utf8'));
    assert.equal(previous.version, 1, 'Unsupported QA result');
    assert.equal(previous.runId, input.runId, 'QA run identity changed');
    assert.deepEqual(previous.qa, { profile: input.profile, inputs: input.inputs }, 'QA preset or inputs changed');
    assert.notDeepEqual(index.packages, previous.packages, 'QA attempt selection is unchanged');

    const history = path.join(artifacts, 'qa-registrations');
    await mkdir(history, { recursive: true });
    assert.equal(await realpath(history), history, 'QA registration history is redirected');
    const revision = `qa-registrations/${randomUUID()}`;
    const revisionDir = path.join(artifacts, revision);
    await mkdir(revisionDir);
    const proof = await finalizeQa(task, index, `${revision}/suite`, false, { previous });
    const result = { version: 1, runId: previous.runId, qa: previous.qa, ...proof };
    const proofPath = path.join(revisionDir, 'qa-proof.json');
    const resultBytes = bytes(result);
    await writeFile(proofPath, bytes(proof), { flag: 'wx' });
    await writeFile(path.join(revisionDir, 'qa-result.json'), resultBytes, { flag: 'wx' });

    const retained = path.join(history, digest(previousBytes));
    await mkdir(retained, { recursive: true });
    assert.equal(await realpath(retained), retained, 'Prior QA registration is redirected');
    const priorPath = path.join(retained, 'qa-result.json');
    try {
      await writeFile(priorPath, previousBytes, { flag: 'wx' });
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      assert.equal(await realpath(priorPath), priorPath, 'Prior QA registration is redirected');
      assert.equal(await readFile(priorPath, 'utf8'), previousBytes, 'Prior QA registration changed');
    }
    await writeFile(path.join(revisionDir, 'reselection.json'), bytes({
      version: 1,
      previous: { path: `qa-registrations/${digest(previousBytes)}/qa-result.json`, sha256: digest(previousBytes) },
      selected: { path: `${revision}/qa-result.json`, sha256: digest(resultBytes) },
    }), { flag: 'wx' });
    assert.equal(await readFile(selectedPath, 'utf8'), previousBytes, 'QA selection changed during reselection');
    assert.deepEqual(JSON.parse(await readFile(path.join(task, 'inputs/qa.json'), 'utf8')), input, 'QA inputs changed during reselection');
    await writeFile(temporary, resultBytes, { flag: 'wx' });
    temporaryCreated = true;
    await rename(temporary, selectedPath);
    temporaryCreated = false;
    return proofPath;
  } finally {
    if (temporaryCreated) await unlink(temporary);
    await lock.close();
    await unlink(lockPath);
  }
}
