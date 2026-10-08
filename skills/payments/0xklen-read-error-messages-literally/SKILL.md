---
name: read-error-messages-literally
description: Use when a command, test, or API call returns an error. Parse the exact text as written, resolve its paths and exit code, and only then form a hypothesis.
---

# Read error messages literally

Most debugging fails at the first sentence: the tool said what was wrong and the reader substituted what they expected. This skill forces a byte-level reading of the message before any theory is allowed.

## Procedure

1. Capture the full message, not the last line. Re-run the failing command with stderr attached: `./build.sh 2>&1 | tee /tmp/err.txt`, then read it back with `read_file("/tmp/err.txt")`.

2. Quote the exact string in your working notes. Do not paraphrase; the wording carries the signal.

3. Decompose the message into literal parts: error code, path, line number, offending token, and which program emitted it.

4. For a stack trace, read upward from the last line — that is the raising frame, not necessarily the root cause. `pytest -x -q --tb=long` prints the assertion and the frame that failed it.

5. Resolve every path the message names: `ls -l /etc/ssl/certs/ca.pem` to confirm the file exists or does not. Do not assume existence either way.

6. Check the numeric exit status separately: `echo $?`. 127 means command not found, 126 not executable, 137 killed (SIGKILL), 139 segfault — map the number before theorising.

7. Only when every literal token in the message is accounted for do you propose a cause. If your cause does not explain each token, it is wrong.

8. Re-run the exact minimal command after any fix and paste the new output; never assume a fix worked because it seems right.

## Pitfalls

- "Connection refused" and "connection timed out" are different faults; conflating them sends you to the wrong layer.
- Truncated logs hide the real line; check `wc -l /tmp/err.txt` against the log's own reported total.
- A missing-file error may be a symptom of an earlier step that wrote to the wrong working directory.
- Trailing whitespace or a smart quote in the message is a hint, not noise.
- A stack trace truncated by a log rotation can end mid-frame; confirm you have the complete record.

## Verification

    ./build.sh 2>&1 | tail -5; echo "exit=$?"

Report the exact string, the exit code, and each resolved path — never a paraphrase of the error.
