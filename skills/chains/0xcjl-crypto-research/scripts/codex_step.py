#!/usr/bin/env python3
"""Run one Codex CLI step in the foreground (sandboxed, no approval bypass) and log model/effort/time/tokens."""
import argparse, json, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

CODEX = str(Path.home() / ".local/bin/codex")
FORBIDDEN = "--dangerously-bypass-approvals-and-sandbox"


def build_cmd(task_dir, model, effort, prompt, codex=CODEX):
    cmd = [codex, "exec", "--skip-git-repo-check", "-C", str(task_dir), "-s", "workspace-write",
           "-m", model, "-c", f"model_reasoning_effort={effort}", "--json", prompt]
    if FORBIDDEN in cmd: raise ValueError("approval/sandbox bypass is not allowed")
    return cmd


def parse_usage(jsonl_text):
    """Sum usage over turn.completed events; 'unknown' when Codex emitted none."""
    totals, seen = {}, False
    for line in jsonl_text.splitlines():
        try: event = json.loads(line)
        except ValueError: continue
        if isinstance(event, dict) and event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            seen = True
            for key, value in event["usage"].items():
                if isinstance(value, int): totals[key] = totals.get(key, 0) + value
    if not seen: return "unknown"
    totals["total_tokens"] = totals.get("input_tokens", 0) + totals.get("output_tokens", 0)
    return totals


def last_message(jsonl_text):
    text = None
    for line in jsonl_text.splitlines():
        try: event = json.loads(line)
        except ValueError: continue
        item = event.get("item") if isinstance(event, dict) else None
        if isinstance(item, dict) and item.get("type") == "agent_message": text = item.get("text")
    return text


def run(task_dir, model, effort, prompt, step, timeout):
    task_dir = Path(task_dir).resolve()
    started = datetime.now(timezone.utc); t0 = time.monotonic()
    try:
        proc = subprocess.run(build_cmd(task_dir, model, effort, prompt), stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=timeout)
        out, err, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        out, err, code = exc.stdout or "", exc.stderr or "", "timeout"
        out = out.decode() if isinstance(out, bytes) else out
        err = err.decode() if isinstance(err, bytes) else err
    (task_dir / f"{step}.jsonl").write_text(out)
    (task_dir / f"{step}.err").write_text(err)
    message = last_message(out)
    if message is not None: (task_dir / f"{step}.final.txt").write_text(message)  # never clobber files the model wrote
    record = {"step": step, "executor": "codex exec", "model": model, "effort": effort,
              "started_at": started.isoformat().replace("+00:00", "Z"), "elapsed_s": round(time.monotonic() - t0, 1),
              "exit_code": code, "usage": parse_usage(out), "sandbox": "workspace-write", "approval_bypass": False}
    with (task_dir / "steps.jsonl").open("a") as handle: handle.write(json.dumps(record) + "\n")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-dir", required=True); parser.add_argument("--model", required=True)
    parser.add_argument("--effort", required=True); parser.add_argument("--step", required=True)
    parser.add_argument("--prompt-file", required=True); parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()
    record = run(args.task_dir, args.model, args.effort, Path(args.prompt_file).read_text(), args.step, args.timeout)
    print(json.dumps(record, indent=2))
    sys.exit(0 if record["exit_code"] == 0 else 1)


if __name__ == "__main__":
    main()
