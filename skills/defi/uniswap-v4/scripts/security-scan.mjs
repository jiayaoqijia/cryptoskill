#!/usr/bin/env node
/**
 * Security scan — checks for hardcoded secrets, eval(), exec() with user input.
 * Run: node scripts/security-scan.mjs
 */
import { readdir, readFile } from "fs/promises";
import { join } from "path";

const PATTERNS = [
  { name: "eval()", regex: /\beval\s*\(/g, severity: "CRITICAL" },
  { name: "Function()", regex: /\bnew\s+Function\s*\(/g, severity: "CRITICAL" },
  { name: "exec()", regex: /\bexec\s*\(/g, severity: "HIGH" },
  { name: "execSync()", regex: /\bexecSync\s*\(/g, severity: "HIGH" },
  { name: "child_process", regex: /require\(['"]child_process['"]\)/g, severity: "HIGH" },
  { name: "child_process import", regex: /from\s+['"]child_process['"]/g, severity: "HIGH" },
  { name: "hardcoded private key", regex: /0x[0-9a-fA-F]{64}/g, severity: "CRITICAL" },
  { name: "hardcoded mnemonic", regex: /\b(abandon|zoo|rhythm)\b.*\b(abandon|zoo|rhythm)\b/gi, severity: "HIGH" },
  { name: "process.env in template literal", regex: /`[^`]*\$\{process\.env\.\w*KEY/g, severity: "MEDIUM" },
];

// Allowlisted 64-char hex patterns (pool IDs, hashes — not private keys)
const ALLOWLIST = new Set([
  // Add known non-secret 64-char hex values here if needed
]);

async function scanDir(dir) {
  const findings = [];
  const entries = await readdir(dir, { withFileTypes: true, recursive: true });

  for (const entry of entries) {
    if (!entry.isFile()) continue;
    const fullPath = join(entry.parentPath ?? entry.path, entry.name);
    if (fullPath.includes("node_modules") || fullPath.includes(".git") || fullPath.includes("dist")) continue;
    if (!entry.name.endsWith(".ts") && !entry.name.endsWith(".mjs") && !entry.name.endsWith(".js")) continue;

    const content = await readFile(fullPath, "utf-8");
    const lines = content.split("\n");

    for (const pattern of PATTERNS) {
      for (let i = 0; i < lines.length; i++) {
        const matches = lines[i].match(pattern.regex);
        if (matches) {
          for (const match of matches) {
            // Skip allowlisted values
            if (ALLOWLIST.has(match)) continue;
            // Skip test files for private key patterns (test fixtures)
            if (pattern.name === "hardcoded private key" && fullPath.includes("test")) continue;
            findings.push({
              severity: pattern.severity,
              pattern: pattern.name,
              file: fullPath,
              line: i + 1,
              match: match.slice(0, 40) + (match.length > 40 ? "..." : ""),
            });
          }
        }
      }
    }
  }
  return findings;
}

const findings = await scanDir("src");
const testFindings = await scanDir("tests");

// Only report src findings as failures; test findings are informational
console.log("=== Security Scan ===\n");

if (findings.length === 0) {
  console.log("✅ No security issues found in src/\n");
} else {
  console.log(`❌ ${findings.length} issues found in src/:\n`);
  for (const f of findings) {
    console.log(`  [${f.severity}] ${f.pattern} — ${f.file}:${f.line}`);
    console.log(`    Match: ${f.match}`);
  }
  process.exit(1);
}

if (testFindings.length > 0) {
  console.log(`ℹ ${testFindings.length} findings in tests/ (informational):`);
  for (const f of testFindings) {
    console.log(`  [${f.severity}] ${f.pattern} — ${f.file}:${f.line}`);
  }
}
