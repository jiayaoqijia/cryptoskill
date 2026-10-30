import { closeSync, openSync, writeFileSync } from 'node:fs';

export function writeNewFile(file, contents) {
  const descriptor = openSync(file, 'wx');
  try {
    writeFileSync(descriptor, contents);
  } finally {
    closeSync(descriptor);
  }
}
