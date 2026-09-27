import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

/**
 * The page's "what happens to your locks on October 22" panel ports one
 * function from Aerodrome's migration contract (dromos-labs/metadex-public,
 * V3/src/migration/Migration.sol, `_resolveStake`). There is no TypeScript
 * copy to run it against, so these cases pin the contract's rules directly.
 */

const here = dirname(fileURLToPath(import.meta.url));
const siteSource = readFileSync(resolve(here, "../docs/index.html"), "utf8");

function extractFunction(source: string, name: string): string {
  const start = source.indexOf(`function ${name}(`);
  assert.notEqual(start, -1, `docs/index.html no longer defines ${name}()`);
  let depth = 0;
  let seenBrace = false;
  for (let i = start; i < source.length; i++) {
    if (source[i] === "{") {
      depth++;
      seenBrace = true;
    } else if (source[i] === "}") {
      depth--;
      if (seenBrace && depth === 0) return source.slice(start, i + 1);
    }
  }
  throw new Error(`unbalanced braces while extracting ${name}()`);
}

function extractConst(source: string, name: string): string {
  const match = source.match(new RegExp(`const ${name} = ([^;]+);`));
  assert.ok(match, `docs/index.html no longer defines ${name}`);
  return match[0];
}

type Lock = { amount: number; end: number; isPermanent: boolean; escrowType: number };
type Outcome = { kind: string; weeks?: number };

const migrationOutcome = new Function(
  [
    extractConst(siteSource, "WEEK_SECONDS"),
    extractConst(siteSource, "NEW_MAXTIME"),
    extractFunction(siteSource, "migrationOutcome"),
    "return migrationOutcome;",
  ].join("\n"),
)() as (lock: Lock, atTs: number) => Outcome;

const WEEK = 604800;
const LAUNCH = Date.UTC(2026, 9, 22) / 1000;
const normal = (over: Partial<Lock>): Lock => ({ amount: 100, end: 0, isPermanent: false, escrowType: 0, ...over });

test("the page prices the migration at Aero's launch, 2026-10-22 00:00 UTC", () => {
  assert.match(extractConst(siteSource, "AERO_LAUNCH_TS"), /Date\.UTC\(2026, 9, 22\)/);
});

test("a permanent lock stays permanent, whatever its end field says", () => {
  assert.deepEqual(migrationOutcome(normal({ isPermanent: true }), LAUNCH), { kind: "permanent" });
});

test("a lock that has ended by the time it moves comes out as plain AERO — including one ending exactly then", () => {
  assert.deepEqual(migrationOutcome(normal({ end: LAUNCH - WEEK }), LAUNCH), { kind: "liquid" });
  assert.deepEqual(migrationOutcome(normal({ end: LAUNCH }), LAUNCH), { kind: "liquid" });
});

test("remaining time rounds UP to whole weeks", () => {
  assert.deepEqual(migrationOutcome(normal({ end: LAUNCH + 1 }), LAUNCH), { kind: "stake", weeks: 1 });
  assert.deepEqual(migrationOutcome(normal({ end: LAUNCH + WEEK }), LAUNCH), { kind: "stake", weeks: 1 });
  assert.deepEqual(migrationOutcome(normal({ end: LAUNCH + WEEK + 1 }), LAUNCH), { kind: "stake", weeks: 2 });
});

test("a stake is capped at the new escrow's four-year maximum", () => {
  // LAUNCH falls on a week boundary, so the cap is floor(4 * 365 days / 1 week) = 208.
  assert.equal(LAUNCH % WEEK, 0);
  assert.deepEqual(migrationOutcome(normal({ end: LAUNCH + 5 * 365 * 86400 }), LAUNCH), { kind: "stake", weeks: 208 });
});

test("a lock deposited into a Relay, or a Relay's own veNFT, cannot be moved as it is", () => {
  assert.deepEqual(migrationOutcome(normal({ escrowType: 1, amount: 0 }), LAUNCH), { kind: "relay" });
  assert.deepEqual(migrationOutcome(normal({ escrowType: 2, isPermanent: true }), LAUNCH), { kind: "relay" });
});

test("an emptied lock carries nothing over", () => {
  assert.deepEqual(migrationOutcome(normal({ amount: 0, end: LAUNCH + WEEK }), LAUNCH), { kind: "empty" });
});
