// =============================================================================
// acp serve start   — Start seller runtime (daemonized)
// acp serve stop    — Stop seller runtime
// acp serve status  — Show runtime process info
// =============================================================================

import { spawn } from "child_process";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import * as output from "../lib/output.js";
import { getMyAgentInfo } from "../lib/wallet.js";
import {
  findSellerPid,
  isProcessRunning,
  removePidFromConfig,
  ROOT,
  LOGS_DIR,
} from "../lib/config.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// -- Start --

const SELLER_LOG_PATH = path.resolve(LOGS_DIR, "seller.log");
const OFFERINGS_ROOT = path.resolve(ROOT, "src", "seller", "offerings");

function ensureLogsDir(): void {
  if (!fs.existsSync(LOGS_DIR)) {
    fs.mkdirSync(LOGS_DIR, { recursive: true });
  }
}

function offeringHasLocalFiles(offeringName: string): boolean {
  const dir = path.join(OFFERINGS_ROOT, offeringName);
  return (
    fs.existsSync(path.join(dir, "handlers.ts")) &&
    fs.existsSync(path.join(dir, "offering.json"))
  );
}

export async function start(): Promise<void> {
  const pid = findSellerPid();
  if (pid !== undefined) {
    output.log(`  Seller already running (PID ${pid}).`);
    return;
  }

  // Warn if no offerings are listed on ACP, or if any registered offering is missing local handlers.ts or offering.json
  try {
    const agentInfo = await getMyAgentInfo();
    if (!agentInfo.jobs || agentInfo.jobs.length === 0) {
      output.warn(
        "No offerings registered on ACP. Run `acp sell create <name>` first.\n"
      );
    } else {
      const missing = agentInfo.jobs
        .filter((job) => !offeringHasLocalFiles(job.name))
        .map((job) => job.name);
      if (missing.length > 0) {
        output.warn(
          `No local offering files for ${
            missing.length
          } offering(s) registered on ACP: ${missing.join(", ")}. ` +
            `Each needs src/seller/offerings/<name>/handlers.ts and offering.json, or jobs for these offerings will fail at runtime.\n`
        );
      }
    }
  } catch {
    // Non-fatal — proceed with starting anyway
  }

  const sellerScript = path.resolve(
    __dirname,
    "..",
    "seller",
    "runtime",
    "seller.ts"
  );
  const tsxBin = path.resolve(ROOT, "node_modules", ".bin", "tsx");

  ensureLogsDir();
  const logFd = fs.openSync(SELLER_LOG_PATH, "a");

  const sellerProcess = spawn(tsxBin, [sellerScript], {
    detached: true,
    stdio: ["ignore", logFd, logFd],
    cwd: ROOT,
  });

  if (!sellerProcess.pid) {
    fs.closeSync(logFd);
    output.fatal("Failed to start seller process.");
  }

  sellerProcess.unref();
  fs.closeSync(logFd);

  output.output({ pid: sellerProcess.pid, status: "started" }, () => {
    output.heading("Seller Started");
    output.field("PID", sellerProcess.pid!);
    output.field("Log", SELLER_LOG_PATH);
    output.log("\n  Run `acp serve status` to verify.");
    output.log("  Run `acp serve logs` to tail output.\n");
  });
}

// -- Stop --

export async function stop(): Promise<void> {
  const pid = findSellerPid();

  if (pid === undefined) {
    output.log("  No seller process running.");
    return;
  }

  output.log(`  Stopping seller process (PID ${pid})...`);

  try {
    process.kill(pid, "SIGTERM");
  } catch (err: any) {
    output.fatal(`Failed to send SIGTERM to PID ${pid}: ${err.message}`);
  }

  // Wait and verify
  let stopped = false;
  for (let i = 0; i < 10; i++) {
    const start = Date.now();
    while (Date.now() - start < 200) {
      /* busy wait 200ms */
    }
    if (!isProcessRunning(pid)) {
      stopped = true;
      break;
    }
  }

  if (stopped) {
    removePidFromConfig();
    output.output({ pid, status: "stopped" }, () => {
      output.log(`  Seller process (PID ${pid}) stopped.\n`);
    });
  } else {
    output.error(
      `Process (PID ${pid}) did not stop within 2 seconds. Try: kill -9 ${pid}`
    );
  }
}

// -- Status --

export async function status(): Promise<void> {
  const pid = findSellerPid();
  const running = pid !== undefined;

  output.output({ running, pid: pid ?? null }, () => {
    output.heading("Seller Runtime");
    if (running) {
      output.field("Status", "Running");
      output.field("PID", pid!);
    } else {
      output.field("Status", "Not running");
    }
    output.log("\n  Run `acp sell list` to see offerings.\n");
  });
}

// -- Logs --

export async function logs(follow: boolean = false): Promise<void> {
  if (!fs.existsSync(SELLER_LOG_PATH)) {
    output.log(
      "  No log file found. Start the seller first: `acp serve start`\n"
    );
    return;
  }

  if (follow) {
    // Tail -f equivalent: stream new lines as they appear
    const tail = spawn("tail", ["-f", SELLER_LOG_PATH], {
      stdio: "inherit",
    });
    // Keep running until user hits Ctrl+C
    await new Promise<void>((resolve) => {
      tail.on("close", () => resolve());
      process.on("SIGINT", () => {
        tail.kill();
        resolve();
      });
    });
  } else {
    // Show the last 50 lines
    const content = fs.readFileSync(SELLER_LOG_PATH, "utf-8");
    const lines = content.split("\n");
    const last50 = lines.slice(-51).join("\n"); // -51 because trailing newline
    if (last50.trim()) {
      output.log(last50);
    } else {
      output.log("  Log file is empty.\n");
    }
  }
}
