#!/usr/bin/env node
//
// analyze-cpuprofile.js — aggregate self/total JS time from a Hermes /
// React Native Release Profiler CPU capture recorded on the swaps/bridge
// screens, splitting it into swaps-owned code (the paths in
// DEFAULT_SCOPE_ROOTS, i.e. app/components/UI/Bridge/** plus the swaps
// redux/selector/controller/util paths) and the surrounding non-swaps
// context that also burned time during the capture.
//
// Every frame is classified by its relation to the swaps call stacks, so a
// slow dependency that swaps merely *uses* (navigation, redux store, design
// system, a controller) is attributed instead of silently dropped:
//
//   Swaps-owned       frame's source path matches a swaps scope root
//   Called by swaps   non-swaps frame that ran with a swaps frame below it
//                     on the stack (swaps code invoked it)
//   Hosts swaps       non-swaps frame that was on the stack when a swaps
//                     frame was pushed (it renders/hosts the swaps screen —
//                     React reconciler, navigator, providers)
//   Concurrent        non-swaps frame that never shares a stack with swaps
//                     code (background/polling work that still competes for
//                     the JS thread while the user sits on a swaps screen)
//
// Read-only: it only reads the profile (and prints/writes a report). It
// never touches a device, Metro, or the repository.
//
// Input (auto-detected):
//   1. Preferred — the Chrome-trace JSON produced by:
//        yarn react-native-release-profiler --local <profile.cpuprofile> \
//          --sourcemap-path <sourcemaps-dir>/index.js.map
//      i.e. a JSON ARRAY of Begin/End duration events (the "*-converted.json"
//      file). With sourcemaps applied, `args.url`/`args.line`/`args.column`
//      point at ORIGINAL app source, which is what makes swaps-tree scoping
//      possible. Without `--sourcemap-path`, the array still parses, but
//      names/paths stay at the minified-bundle level and almost nothing will
//      match `--scope`.
//   2. Fallback — a raw Hermes `.cpuprofile` (an OBJECT with `samples` and
//      `stackFrames`), i.e. the file before conversion. No sourcemap
//      resolution is attempted in this mode; only usable when the recorded
//      build already preserved readable names/paths (dev-ish bundles).
//
// Usage:
//   node analyze-cpuprofile.js --profile <path> \
//     [--scope <substring>] [--top <n>] [--context-min-pct <n>] \
//     [--trigger-min-pct <n>] [--swaps-only] [--out <path>] [--json]
//
// Exit code is always 0 on a successful parse (there is nothing to "fail" —
// an empty swaps-owned result is a valid, reportable finding). Exit 1 on a
// missing/unparseable file.

'use strict';

const fs = require('fs');
const path = require('path');

// Everything owned by the swaps/bridge team in metamask-mobile, mirroring the
// breadth of a CODEOWNERS-style boundary (e.g. `**/bridge/**`,
// `**/bridge-status/**`, `ui/pages/swaps`, `app/scripts/controllers/swaps` in
// metamask-extension's `.github/CODEOWNERS`) rather than just the
// `app/components/UI/Bridge/**` screen tree. Re-verify with
// `find app -type d \( -iname '*bridge*' -o -iname '*swap*' \)` if the tree
// has been restructured since this was written.
const DEFAULT_SCOPE_ROOTS = [
  'components/UI/Bridge',
  'core/redux/slices/bridge',
  'reducers/swaps',
  'selectors/bridgeController',
  'selectors/bridgeStatusController',
  'selectors/featureFlagController/swapsChainValueOrderOverride',
  'core/Engine/controllers/bridge-controller',
  'core/Engine/controllers/bridge-status-controller',
  'core/Engine/messengers/bridge-controller-messenger',
  'core/Engine/messengers/bridge-status-controller-messenger',
  'util/bridge',
  'util/notifications/notification-states/swap-completed',
  'components/UI/MultichainBridgeTransactionListItem',
  'components/UI/HardwareWallet/Swaps',
  'components/Views/confirmations/components/rows/bridge-fee-row',
  'components/Views/confirmations/components/rows/bridge-time-row',
  'components/Views/confirmations/components/activity/transaction-details-bridge-fee-row',
];

function parseArgs(argv) {
  const args = {
    scope: DEFAULT_SCOPE_ROOTS.join(','),
    top: 40,
    contextMinPct: 0.5,
    triggerMinPct: 5,
    swapsOnly: false,
    json: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--profile') args.profile = argv[++i];
    else if (a === '--scope') args.scope = argv[++i];
    else if (a === '--top') args.top = Number(argv[++i]);
    else if (a === '--context-min-pct') args.contextMinPct = Number(argv[++i]);
    else if (a === '--trigger-min-pct') args.triggerMinPct = Number(argv[++i]);
    else if (a === '--swaps-only') args.swapsOnly = true;
    else if (a === '--out') args.out = argv[++i];
    else if (a === '--json') args.json = true;
    else if (a === '--help' || a === '-h') args.help = true;
  }
  return args;
}

function printHelp() {
  const lines = [];
  for (const line of fs.readFileSync(__filename, 'utf8').split('\n')) {
    if (line.startsWith('#!')) continue; // shebang
    if (!line.startsWith('//')) break; // leading header comment block only
    lines.push(line.replace(/^\/\/ ?/, ''));
  }
  process.stderr.write(lines.join('\n') + '\n');
}

// Ordered, most-specific first. Matched as a substring of the resolved
// source path. Mirrors app/components/UI/Bridge/** in metamask-mobile —
// re-verify against `find app/components/UI/Bridge -maxdepth 2 -type d` if
// that tree has been restructured since this was written.
const AREA_MAP = [
  ['Views/BridgeView', 'Swaps/Bridge screen (BridgeView)'],
  ['components/BridgeTokenSelector', 'Asset picker (token selector modal)'],
  ['components/QuoteSelectorView', 'Quote select screen'],
  ['components/QuoteDetailsRecipientKeyValueRow', 'Quote details card'],
  ['components/QuoteDetailsCard', 'Quote details card'],
  ['components/QuoteCountdownTimer', 'Quote countdown timer'],
  ['components/PostTradeBottomSheet', 'Post-trade modal'],
  ['components/TransactionDetails', 'Post-trade modal'],
  ['Views/BatchSellReview', 'Batch sell \u2014 review'],
  ['Views/BatchSellTokenSelect', 'Batch sell \u2014 token select'],
  ['components/BatchSellDestinationTokenSelectorModal', 'Batch sell \u2014 destination token selector'],
  ['components/BatchSellFinalReviewModal', 'Batch sell \u2014 final review modal'],
  ['components/BatchSellMinimumReceivedInfoModal', 'Batch sell \u2014 info modal'],
  ['components/BatchSellNetworkFeeInfoModal', 'Batch sell \u2014 info modal'],
  ['components/BatchSellPriceImpactInfoModal', 'Batch sell \u2014 info modal'],
  ['components/BatchSellQuoteDetailsModal', 'Batch sell \u2014 quote details modal'],
  ['components/TokenInputArea', 'Token input area'],
  ['components/SwapsKeypad', 'Keypad'],
  ['components/SlippageModal', 'Slippage modal'],
  ['components/FlipQuoteButton', 'Flip quote button'],
  ['components/BlockaidModal', 'Security alert modal'],
  ['components/HighRateAlertModal', 'Security alert modal'],
  ['components/PriceImpactModal', 'Price impact modal'],
  ['components/MissingPriceModal', 'Missing price modal'],
  ['components/TokenWarningModal', 'Token warning modal'],
  ['components/MarketClosedBottomSheets', 'Market closed modal'],
  ['components/RecipientSelectorModal', 'Recipient selector modal'],
  ['components/GaslessQuickPickOptions', 'Gasless quick-pick options'],
  ['components/SwapDiscoveryFeed', 'Swap discovery feed'],
  ['components/BridgeTrendingTokensSection', 'Trending tokens section'],
  ['components/RobinhoodSwapsBanner', 'Robinhood banner'],
  ['components/SwapsConfirmButton', 'Confirm button'],
  ['components/InputStepper', 'Input stepper'],
  ['components/CollapsibleBottomSheet', 'Collapsible bottom sheet'],
  // Swaps/bridge-owned code outside the `components/UI/Bridge` screen tree
  // (redux state, selectors, controller wiring, app-level utils,
  // confirmations rows, notifications). See DEFAULT_SCOPE_ROOTS above.
  ['core/redux/slices/bridge', 'Bridge redux state'],
  ['reducers/swaps', 'Swaps redux state (legacy)'],
  ['selectors/bridgeStatusController', 'Bridge status selectors'],
  ['selectors/bridgeController', 'Bridge controller selectors'],
  ['selectors/featureFlagController/swapsChainValueOrderOverride', 'Swaps feature-flag selectors'],
  ['core/Engine/controllers/bridge-status-controller', 'BridgeStatusController wiring'],
  ['core/Engine/controllers/bridge-controller', 'BridgeController wiring'],
  ['core/Engine/messengers/bridge-status-controller-messenger', 'BridgeStatusController messenger'],
  ['core/Engine/messengers/bridge-controller-messenger', 'BridgeController messenger'],
  ['util/notifications/notification-states/swap-completed', 'Swap-completed notification'],
  ['util/bridge', 'Bridge utils (app-level)'],
  ['components/UI/MultichainBridgeTransactionListItem', 'Multichain bridge tx history item'],
  ['components/UI/HardwareWallet/Swaps', 'Hardware wallet swaps'],
  ['components/Views/confirmations/components/rows/bridge-fee-row', 'Confirmations \u2014 bridge fee row'],
  ['components/Views/confirmations/components/rows/bridge-time-row', 'Confirmations \u2014 bridge time row'],
  [
    'components/Views/confirmations/components/activity/transaction-details-bridge-fee-row',
    'Confirmations \u2014 bridge fee row (tx details)',
  ],
  ['hooks/', 'Bridge hooks'],
  ['utils/', 'Bridge utils'],
];

// Non-swaps code that shows up in a capture recorded on the swaps screens.
// Ordered, most-specific first; matched as a substring of the resolved source
// path. This exists so a slow dependency the swaps screens merely *use*
// (navigation, redux, the design system, a controller) is named in the report
// instead of being dropped, and so the report can say plainly that it is not
// swaps-owned. Anything not listed falls back to a path-derived label
// (see contextAreaFor), so the map only needs the high-signal cases.
const CONTEXT_AREA_MAP = [
  // Rendering / animation runtimes
  ['react-native/Libraries/Renderer', 'React Native renderer'],
  ['react-native-reanimated', 'Reanimated (animations)'],
  ['react-native-gesture-handler', 'Gesture handler'],
  ['node_modules/react/', 'React runtime'],
  ['node_modules/scheduler', 'React scheduler'],
  ['react-native/Libraries', 'React Native core'],
  // Navigation
  ['@react-navigation', 'React Navigation (library)'],
  ['app/components/Nav', 'Navigation (app nav stack)'],
  ['app/core/NavigationService', 'Navigation service'],
  // State management
  ['node_modules/react-redux', 'react-redux'],
  ['node_modules/@reduxjs/toolkit', 'Redux Toolkit'],
  ['node_modules/redux', 'Redux runtime'],
  ['node_modules/reselect', 'Reselect'],
  ['node_modules/redux-persist', 'redux-persist'],
  ['app/store', 'Redux store (app)'],
  ['app/selectors', 'App selectors'],
  // Engine / controllers. The polling controllers are listed separately
  // because they are the usual source of "Concurrent" time — work that runs
  // on a timer regardless of which screen the user is on.
  ['controllers/token-detection', 'Token detection (polling)'],
  ['controllers/token-balances', 'Token balances (polling)'],
  ['controllers/token-rates', 'Token rates (polling)'],
  ['controllers/currency-rate', 'Currency rates (polling)'],
  ['controllers/account-tracker', 'Account tracker (polling)'],
  ['controllers/nft', 'NFT controllers'],
  ['app/core/Engine', 'Engine / controller wiring'],
  ['@metamask/transaction-controller', 'TransactionController'],
  ['@metamask/assets-controllers', 'Assets controllers (tokens/prices)'],
  ['@metamask/accounts-controller', 'AccountsController'],
  ['@metamask/network-controller', 'NetworkController'],
  ['@metamask/keyring', 'Keyring'],
  // UI shared surfaces
  ['app/component-library', 'Design system (component-library)'],
  ['app/components/UI/Tokens', 'Token list UI'],
  ['app/components/UI/AssetOverview', 'Asset overview'],
  ['app/components/Views/confirmations', 'Confirmations'],
  ['app/components/hooks', 'Shared app hooks'],
  // Cross-cutting app code
  ['app/core/Analytics', 'Analytics / metrics'],
  ['app/util/metrics', 'Analytics / metrics'],
  ['app/util', 'App utils'],
  ['node_modules/lodash', 'lodash'],
  ['node_modules/bn.js', 'bn.js / big-number math'],
  ['node_modules/bignumber.js', 'bn.js / big-number math'],
];

const RELATION = {
  SWAPS: 'Swaps-owned',
  CALLED_BY_SWAPS: 'Called by swaps',
  HOSTS_SWAPS: 'Hosts swaps screen',
  CONCURRENT: 'Concurrent (off swaps path)',
  RUNTIME: 'Runtime / idle',
};

// Ranking used when collapsing the mixed relations inside one area bucket
// down to a single label, and when ordering rows of equal weight.
const RELATION_RANK = {
  [RELATION.SWAPS]: 0,
  [RELATION.CALLED_BY_SWAPS]: 1,
  [RELATION.HOSTS_SWAPS]: 2,
  [RELATION.CONCURRENT]: 3,
  [RELATION.RUNTIME]: 4,
};

// Synthetic bookkeeping frames the engine emits: `[root]`, `[global]`,
// `[GC young gen]`, `(program)`, `(garbage collector)`, ... They are not
// anyone's code. `[root]` in particular owns all the wall time when no JS is
// running, so on a capture where the user mostly sat still it dwarfs every
// real frame. Counting it as normal self time makes every percentage
// meaningless and (because a swaps frame is pushed under it at some point)
// mislabels pure idle as time spent hosting the swaps screen — so these
// frames are split out and excluded from the attributable totals.
const SYNTHETIC_FRAME_NAME =
  /^(\[[^\]]*\]|\((?:root|program|idle|anonymous|garbage collector|unknown)\))$/iu;

function isRuntimeFrame(frame) {
  const name = (frame.name || '').trim();
  if (SYNTHETIC_FRAME_NAME.test(name)) return true;
  // Only trust the category when nothing resolved to a real file: a frame with
  // a source path is somebody's code regardless of how it was categorised.
  if (frame.url) return false;
  const category = (frame.category || '').toLowerCase();
  return category === 'gc' || category === 'metadata';
}

function runtimeAreaFor(frame) {
  const name = (frame.name || '').trim();
  if (/gc|garbage/iu.test(name) || (frame.category || '').toLowerCase() === 'gc') {
    return 'Garbage collection';
  }
  if (/^\[?root\]?$/iu.test(name) || /^\((?:root|program|idle)\)$/iu.test(name)) {
    return 'Idle / unattributed (root span)';
  }
  return `Runtime (${name || 'unnamed'})`;
}

function isSwapsOwned(sourcePath, scopeRoots) {
  if (!sourcePath) return false;
  return scopeRoots.some((root) => sourcePath.includes(root));
}

function swapsAreaFor(sourcePath) {
  for (let i = 0; i < AREA_MAP.length; i += 1) {
    if (sourcePath.includes(AREA_MAP[i][0])) return AREA_MAP[i][1];
  }
  return 'Bridge (other / unmapped subfolder)';
}

// Label for a frame that is NOT swaps-owned. Falls back to a path-derived
// bucket so unmapped code still lands somewhere readable and reportable
// rather than being lumped into one giant "other".
function contextAreaFor(sourcePath) {
  if (!sourcePath) return 'Unknown (unsymbolicated)';
  for (let i = 0; i < CONTEXT_AREA_MAP.length; i += 1) {
    if (sourcePath.includes(CONTEXT_AREA_MAP[i][0])) return CONTEXT_AREA_MAP[i][1];
  }
  const pkg = /node_modules\/((?:@[^/]+\/)?[^/]+)/.exec(sourcePath);
  if (pkg) return `${pkg[1]} (dependency)`;
  const segments = sourcePath.replace(/^\.?\//, '').split('/').filter(Boolean);
  if (segments.length > 1) return segments.slice(0, 3).join('/');
  return sourcePath;
}

// Classifies a frame after the whole capture has been replayed: swaps-owned
// by path, otherwise by how its stacks related to swaps code.
function classify(frame, scopeRoots) {
  const sourcePath = frame.url || frame.name;
  if (isSwapsOwned(sourcePath, scopeRoots)) {
    return { ownedBySwaps: true, relation: RELATION.SWAPS, area: swapsAreaFor(sourcePath) };
  }
  if (isRuntimeFrame(frame)) {
    return { ownedBySwaps: false, relation: RELATION.RUNTIME, area: runtimeAreaFor(frame) };
  }
  let relation = RELATION.CONCURRENT;
  if (frame.selfUnderSwapsMicros > 0) relation = RELATION.CALLED_BY_SWAPS;
  else if (frame.hostsSwaps) relation = RELATION.HOSTS_SWAPS;
  return { ownedBySwaps: false, relation, area: contextAreaFor(frame.url) };
}

// Best-effort recovery of `(path:line:col)` out of a Hermes-style function
// name when no source map was available to resolve `args.url` properly.
function extractPathFromName(name) {
  if (!name) return null;
  const m = /\(([^()]+):(\d+):(\d+)\)\s*$/.exec(name);
  if (!m) return null;
  return { url: m[1], line: Number(m[2]), column: Number(m[3]) };
}

function newFrame(key, name, url, line, category, swapsOwned) {
  return {
    key,
    name,
    url: url || null,
    line: line || null,
    category: category || 'unknown',
    selfMicros: 0,
    totalMicros: 0,
    calls: 0,
    // Self time this frame accrued while a swaps-owned frame sat below it on
    // the stack — i.e. swaps code called into it.
    selfUnderSwapsMicros: 0,
    // True if this frame was on the stack when a swaps-owned frame was
    // pushed — i.e. it renders/hosts the swaps screen.
    hostsSwaps: false,
    swapsOwned,
  };
}

// --- Path 1: converted Chrome-trace JSON (array of B/E duration events) ---
//
// Produced by `hermes-profile-transformer` via the `react-native-release-profiler`
// CLI. Events are emitted in a strictly nested (LIFO) B/E stream in ts order,
// so a single-pass stack replay recovers both self time (whichever frame is
// on top of the stack between two consecutive events owns that time slice)
// and total/inclusive time (span from a frame's B to its matching E).
//
// The same replay records each frame's relation to swaps code: how much self
// time it burned with a swaps frame below it on the stack, and whether it was
// itself on the stack when swaps code was entered.
function analyzeConverted(events, scopeRoots) {
  const frames = new Map();
  const stack = [];
  let swapsDepth = 0;
  let lastTs = events.length > 0 ? Number(events[0].ts) : 0;
  const firstTs = lastTs;
  let maxTs = lastTs;

  const keyFor = (ev) => {
    const args = ev.args || {};
    // When no source map was applied, the transformer sets `args.url` to the
    // raw Hermes frame *name* (`fn(path:line:col)`), not a path — so prefer
    // the path recovered out of that shape, and fall back to `args.url` only
    // when it really is a plain path (the symbolicated case).
    const recovered = extractPathFromName(args.url) || extractPathFromName(ev.name);
    const url = recovered ? recovered.url : args.url || null;
    const line = args.line != null ? Number(args.line) : recovered ? recovered.line : null;
    const name = args.params || ev.name || args.allocatedName || 'anonymous';
    const category = args.node_module || args.allocatedCategory || ev.cat || 'unknown';
    return { key: `${name}::${url || category}::${line || ''}`, name, url, line, category };
  };

  for (const ev of events) {
    const ts = Number(ev.ts);
    const dt = ts - lastTs;
    if (stack.length > 0 && dt > 0) {
      const top = stack[stack.length - 1].frame;
      top.selfMicros += dt;
      if (!top.swapsOwned && swapsDepth > 0) top.selfUnderSwapsMicros += dt;
    }
    lastTs = ts;
    if (ts > maxTs) maxTs = ts;

    if (ev.ph === 'B') {
      const info = keyFor(ev);
      let frame = frames.get(info.key);
      if (!frame) {
        const swapsOwned = isSwapsOwned(info.url || info.name, scopeRoots);
        frame = newFrame(info.key, info.name, info.url, info.line, info.category, swapsOwned);
        frames.set(info.key, frame);
      }
      if (frame.swapsOwned) {
        // Only the 0 -> 1 transition needs the walk: everything pushed while
        // swaps is already on the stack is "called by swaps" anyway, which
        // outranks "hosts swaps" in classify().
        if (swapsDepth === 0) {
          for (const entry of stack) entry.frame.hostsSwaps = true;
        }
        swapsDepth += 1;
      }
      stack.push({ frame, beginTs: ts });
    } else if (ev.ph === 'E') {
      const popped = stack.pop();
      if (popped) {
        popped.frame.totalMicros += ts - popped.beginTs;
        popped.frame.calls += 1;
        if (popped.frame.swapsOwned) swapsDepth = Math.max(0, swapsDepth - 1);
      }
    }
  }

  return { frames, durationMicros: maxTs - firstTs };
}

// --- Path 2: raw Hermes .cpuprofile (samples + stackFrames), no conversion ---
//
// `samples[i].sf` names the leaf stack frame active at sample i; `stackFrames`
// is a flat map with a `parent` pointer per frame. Self time is credited to
// the leaf; total time is credited to every frame on the leaf's ancestor
// chain. Relation to swaps is read off the same chain: a swaps frame among
// the leaf's ancestors means the leaf was called by swaps, and any frame with
// a swaps frame between it and the leaf hosts swaps code. No source-map
// resolution happens here — run the CLI conversion first (see skill docs)
// whenever you have sourcemaps, and reserve this path for when you don't.
function analyzeRawHermes(profile, scopeRoots) {
  const { samples, stackFrames } = profile;
  const frames = new Map();
  const ancestorCache = new Map();

  const ancestorsOf = (sf) => {
    if (ancestorCache.has(sf)) return ancestorCache.get(sf);
    const chain = [];
    let cur = sf;
    const guard = new Set();
    while (cur != null && stackFrames[cur] && !guard.has(cur)) {
      guard.add(cur);
      chain.push(cur);
      cur = stackFrames[cur].parent;
    }
    ancestorCache.set(sf, chain);
    return chain;
  };

  const frameFor = (sf) => {
    const raw = stackFrames[sf];
    if (!raw) return null;
    const recovered = extractPathFromName(raw.name);
    const url = recovered ? recovered.url : null;
    const line = raw.line != null ? Number(raw.line) : recovered ? recovered.line : null;
    const key = `${raw.name}::${sf}`;
    let frame = frames.get(key);
    if (!frame) {
      frame = newFrame(
        key,
        raw.name || 'anonymous',
        url,
        line,
        raw.category,
        isSwapsOwned(url || raw.name, scopeRoots),
      );
      frames.set(key, frame);
    }
    return frame;
  };

  let firstTs = null;
  let lastTs = null;
  let prevTs = null;
  for (const sample of samples) {
    const ts = Number(sample.ts);
    if (firstTs === null) firstTs = ts;
    lastTs = ts;
    const dt = prevTs === null ? 0 : Math.max(ts - prevTs, 0);
    prevTs = ts;
    if (dt === 0) continue;

    // chain[0] is the leaf; higher indices walk up towards the root, so a
    // frame's ancestors sit *below* it on the conceptual stack.
    const chain = ancestorsOf(sample.sf).map(frameFor).filter(Boolean);
    let swapsBelowLeaf = false;
    let swapsSeenTowardsLeaf = false;
    for (let i = 0; i < chain.length; i += 1) {
      const frame = chain[i];
      if (swapsSeenTowardsLeaf && !frame.swapsOwned) frame.hostsSwaps = true;
      if (frame.swapsOwned) {
        swapsSeenTowardsLeaf = true;
        if (i > 0) swapsBelowLeaf = true;
      }
      frame.totalMicros += dt;
      frame.calls += 1;
    }

    const leaf = chain[0];
    if (leaf) {
      leaf.selfMicros += dt;
      if (!leaf.swapsOwned && swapsBelowLeaf) leaf.selfUnderSwapsMicros += dt;
    }
  }

  return { frames, durationMicros: (lastTs || 0) - (firstTs || 0) };
}

function loadProfile(profilePath, scopeRoots) {
  const raw = fs.readFileSync(profilePath, 'utf8');
  const data = JSON.parse(raw);
  if (Array.isArray(data)) {
    return { format: 'converted', ...analyzeConverted(data, scopeRoots) };
  }
  if (data && Array.isArray(data.samples) && data.stackFrames) {
    return { format: 'raw-hermes', ...analyzeRawHermes(data, scopeRoots) };
  }
  throw new Error(
    'Unrecognised profile shape: expected either an array of B/E trace events ' +
      '(the "-converted.json" from `yarn react-native-release-profiler`) or a raw ' +
      'Hermes .cpuprofile object with `samples` + `stackFrames`.',
  );
}

function bucketByArea(framesList) {
  const byArea = new Map();
  for (const f of framesList) {
    if (!byArea.has(f.area)) {
      byArea.set(f.area, {
        area: f.area,
        ownedBySwaps: f.ownedBySwaps,
        selfMicros: 0,
        totalMicros: 0,
        byRelation: new Map(),
        frames: [],
      });
    }
    const bucket = byArea.get(f.area);
    bucket.selfMicros += f.selfMicros;
    bucket.totalMicros = Math.max(bucket.totalMicros, f.totalMicros);
    bucket.byRelation.set(f.relation, (bucket.byRelation.get(f.relation) || 0) + f.selfMicros);
    bucket.frames.push(f);
  }
  // One area can mix relations (e.g. a navigator that both hosts the swaps
  // screen and gets called back into by it). Report the relation holding the
  // most self time; the per-frame tables keep the exact detail.
  for (const bucket of byArea.values()) {
    bucket.relation = Array.from(bucket.byRelation.entries()).sort(
      (a, b) => b[1] - a[1] || RELATION_RANK[a[0]] - RELATION_RANK[b[0]],
    )[0][0];
    delete bucket.byRelation;
  }
  return Array.from(byArea.values()).sort((a, b) => b.selfMicros - a.selfMicros);
}

function buildReport(analysis, opts) {
  const { frames, durationMicros, format } = analysis;
  const scope = opts.scope;
  const scopeRoots = scope
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
  const all = Array.from(frames.values());
  for (const f of all) {
    Object.assign(f, classify(f, scopeRoots));
  }
  all.sort((a, b) => b.selfMicros - a.selfMicros);

  const swapsFrames = all.filter((f) => f.ownedBySwaps);
  const runtimeFrames = all.filter((f) => !f.ownedBySwaps && f.relation === RELATION.RUNTIME);
  const contextFrames = all.filter((f) => !f.ownedBySwaps && f.relation !== RELATION.RUNTIME);
  const onPath = contextFrames.filter((f) => f.relation !== RELATION.CONCURRENT);
  const concurrent = contextFrames.filter((f) => f.relation === RELATION.CONCURRENT);

  const sumSelf = (list) => list.reduce((s, f) => s + f.selfMicros, 0);
  const swapsSelfMicros = sumSelf(swapsFrames);
  const contextSelfMicros = sumSelf(contextFrames);
  const runtimeSelfMicros = sumSelf(runtimeFrames);
  // "Attributable" = real JS work someone owns. Idle and GC are excluded so
  // the splits below describe the work, not how long the user sat still.
  const attributableSelfMicros = swapsSelfMicros + contextSelfMicros;
  const totalSelfMicros = attributableSelfMicros + runtimeSelfMicros;

  const minMicros = ((opts.contextMinPct || 0) / 100) * attributableSelfMicros;
  // A frame with no self time did no work of its own, so it is only a finding
  // when the work it *triggered* is significant — a screen whose module merely
  // got evaluated would otherwise show up as a row that means nothing. Hence a
  // much higher bar for zero-self rows than the ordinary noise floor.
  const triggerMinMicros = ((opts.triggerMinPct || 0) / 100) * attributableSelfMicros;
  const reportableSwaps = swapsFrames.filter(
    (f) => f.selfMicros > 0 || f.totalMicros >= triggerMinMicros,
  );
  const reportableContext = opts.swapsOnly
    ? []
    : contextFrames.filter((f) => f.selfMicros >= minMicros);
  const reportableRuntime = opts.swapsOnly ? [] : runtimeFrames.filter((f) => f.selfMicros > 0);

  const durationMs = durationMicros / 1000;

  return {
    format,
    scope,
    swapsOnly: Boolean(opts.swapsOnly),
    contextMinPct: opts.contextMinPct,
    triggerMinPct: opts.triggerMinPct,
    durationMs,
    durationSeconds: durationMs / 1000,
    totalFrames: all.length,
    totalSelfMicros,
    attributableSelfMicros,
    runtimeSelfMicros,
    swapsSelfMicros,
    // Widest inclusive swaps span: a lower bound on how much work swaps code
    // set in motion, which is the number that matters when swaps self time is
    // ~0 but swaps frames are all over the stacks.
    swapsInclusiveMicros: swapsFrames.reduce((m, f) => Math.max(m, f.totalMicros), 0),
    contextOnPathSelfMicros: sumSelf(onPath),
    contextConcurrentSelfMicros: sumSelf(concurrent),
    // Kept under the previous names so anything already reading --json keeps
    // working; the split area lists below are the new, wider view.
    inScopeSelfMicros: swapsSelfMicros,
    outOfScopeSelfMicros: contextSelfMicros,
    areas: bucketByArea(reportableSwaps),
    contextPathAreas: bucketByArea(reportableContext.filter((f) => f.relation !== RELATION.CONCURRENT)),
    contextConcurrentAreas: bucketByArea(
      reportableContext.filter((f) => f.relation === RELATION.CONCURRENT),
    ),
    runtimeAreas: bucketByArea(reportableRuntime),
    topInScope: reportableSwaps.slice(0, opts.top),
    topContext: reportableContext.slice(0, opts.top),
  };
}

function ms(micros) {
  return (micros / 1000).toFixed(2);
}

function pct(part, whole) {
  if (!whole) return '0.0';
  return ((part / whole) * 100).toFixed(1);
}

function sourceOf(frame) {
  if (!frame.url) return '(unsymbolicated)';
  return `${frame.url}${frame.line ? ':' + frame.line : ''}`;
}

function renderMarkdown(report) {
  const lines = [];
  const scopeRoots = report.scope.split(',').map((s) => s.trim()).filter(Boolean);
  const scopeLabel = scopeRoots.length > 1 ? `${scopeRoots.length} swaps/bridge-owned paths` : scopeRoots[0];
  lines.push('# CPU profile audit \u2014 swaps/bridge + on-screen context');
  lines.push('');
  lines.push(`Swaps ownership determined by: ${scopeLabel}.`);
  if (scopeRoots.length > 1) {
    lines.push('');
    lines.push('<details><summary>Scope roots</summary>');
    lines.push('');
    for (const r of scopeRoots) lines.push(`- \`${r}\``);
    lines.push('');
    lines.push('</details>');
  }
  lines.push('');
  const totalSelf = report.totalSelfMicros || 1;
  const jsWork = report.attributableSelfMicros || 1;
  lines.push('| Metric | Value |');
  lines.push('|---|---|');
  lines.push(`| Format detected | ${report.format} |`);
  lines.push(`| Capture length | ~${Math.round(report.durationSeconds)}s |`);
  lines.push(`| Distinct frames sampled | ${report.totalFrames} |`);
  lines.push(`| JS work sampled (attributable) | ${ms(report.attributableSelfMicros)} ms |`);
  lines.push(
    `| Runtime & idle (root span, GC) | ${ms(report.runtimeSelfMicros)} ms (${pct(report.runtimeSelfMicros, totalSelf)}% of capture) \u2014 excluded from the splits below |`,
  );
  lines.push(
    `| Swaps-owned code | ${ms(report.swapsSelfMicros)} ms (${pct(report.swapsSelfMicros, jsWork)}% of JS work) |`,
  );
  lines.push(
    `| \u21b3 widest swaps-owned span (inclusive) | ${ms(report.swapsInclusiveMicros)} ms \u2014 work swaps code set in motion, including callees |`,
  );
  lines.push(
    `| Non-swaps code on the swaps path | ${ms(report.contextOnPathSelfMicros)} ms (${pct(report.contextOnPathSelfMicros, jsWork)}% of JS work) |`,
  );
  lines.push(
    `| Non-swaps code running concurrently | ${ms(report.contextConcurrentSelfMicros)} ms (${pct(report.contextConcurrentSelfMicros, jsWork)}% of JS work) |`,
  );
  lines.push('');
  lines.push('## Swaps-owned areas (self time)');
  lines.push('');
  lines.push('| Area | Time (ms) | % of swaps time | Inclusive (ms) | # of hot spots |');
  lines.push('|---|---|---|---|---|');
  for (const a of report.areas) {
    lines.push(
      `| ${a.area} | ${ms(a.selfMicros)} | ${pct(a.selfMicros, report.swapsSelfMicros)}% | ${ms(a.totalMicros)} | ${a.frames.length} |`,
    );
  }
  if (report.areas.length === 0) {
    lines.push(
      `| *no swaps-owned frame did measurable work, nor triggered \u2265${report.triggerMinPct}% of JS work* | \u2014 | \u2014 | \u2014 | \u2014 |`,
    );
  }
  if (report.swapsSelfMicros === 0 && report.swapsInclusiveMicros > 0) {
    lines.push('');
    lines.push(
      '> Swaps-owned frames appear in the stacks but never as the leaf: they' +
        ' burned no time themselves, and the cost sits in what they called.' +
        ' Read the `Inclusive (ms)` column and the non-swaps tables below to' +
        ' see where it went, and check the swaps call sites before concluding' +
        ' this is another team\u2019s problem.',
    );
  }
  lines.push('');
  if (!report.swapsOnly) {
    const contextTable = (title, note, areas, withRelation) => {
      lines.push(`## ${title}`);
      lines.push('');
      if (note) {
        lines.push(note);
        lines.push('');
      }
      if (withRelation) {
        lines.push('| Area | Relation to swaps | Time (ms) | % of JS work | # of hot spots |');
        lines.push('|---|---|---|---|---|');
      } else {
        lines.push('| Area | Time (ms) | % of JS work | # of hot spots |');
        lines.push('|---|---|---|---|');
      }
      for (const a of areas) {
        lines.push(
          withRelation
            ? `| ${a.area} | ${a.relation} | ${ms(a.selfMicros)} | ${pct(a.selfMicros, jsWork)}% | ${a.frames.length} |`
            : `| ${a.area} | ${ms(a.selfMicros)} | ${pct(a.selfMicros, jsWork)}% | ${a.frames.length} |`,
        );
      }
      if (areas.length === 0) {
        const empty = `*nothing above the ${report.contextMinPct}% noise floor*`;
        lines.push(withRelation ? `| ${empty} | \u2014 | \u2014 | \u2014 | \u2014 |` : `| ${empty} | \u2014 | \u2014 | \u2014 |`);
      }
      lines.push('');
    };
    contextTable(
      'Non-swaps areas on the swaps path (self time)',
      'Not swaps-owned, but either called by swaps code or hosting/rendering the swaps screen.',
      report.contextPathAreas,
      true,
    );
    contextTable(
      'Non-swaps areas running concurrently (self time)',
      'Never shares a stack with swaps code \u2014 it competed for the JS thread while the user was on a swaps screen.',
      report.contextConcurrentAreas,
      false,
    );
    if (report.runtimeAreas.length > 0) {
      lines.push('## Runtime & idle (nobody\u2019s code)');
      lines.push('');
      lines.push(
        'Engine bookkeeping, not a team\u2019s work. `[root]` is wall time with no' +
          ' JS on the stack (the user sitting still), so it is excluded from' +
          ' every percentage above. GC volume can still be a symptom worth' +
          ' mentioning \u2014 never a row in the fix table.',
      );
      lines.push('');
      lines.push('| Area | Time (ms) | % of capture |');
      lines.push('|---|---|---|');
      for (const a of report.runtimeAreas) {
        lines.push(`| ${a.area} | ${ms(a.selfMicros)} | ${pct(a.selfMicros, totalSelf)}% |`);
      }
      lines.push('');
    }
  }
  lines.push('## Top swaps-owned frames by self time');
  lines.push('');
  lines.push('| # | Time (ms) | Total (ms) | Calls | Area | Function | Source |');
  lines.push('|---|---|---|---|---|---|---|');
  report.topInScope.forEach((f, i) => {
    lines.push(
      `| ${i + 1} | ${ms(f.selfMicros)} | ${ms(f.totalMicros)} | ${f.calls} | ${f.area} | \`${f.name}\` | ${sourceOf(f)} |`,
    );
  });
  if (report.topInScope.length === 0) {
    lines.push('| \u2014 | \u2014 | \u2014 | \u2014 | \u2014 | *no frame under this scope matched* | \u2014 |');
  }
  lines.push('');
  if (report.swapsOnly) {
    lines.push('*Non-swaps context suppressed (`--swaps-only`).*');
    return lines.join('\n');
  }
  lines.push('## Top non-swaps frames by self time (context)');
  lines.push('');
  lines.push(
    'Not owned by the swaps team. Reported because they burned JS-thread time' +
      ' during a capture taken on the swaps screens \u2014 either on the swaps call' +
      ' path or concurrently with it.',
  );
  lines.push('');
  lines.push('| # | Time (ms) | Total (ms) | Calls | Relation to swaps | Area | Function | Source |');
  lines.push('|---|---|---|---|---|---|---|---|');
  report.topContext.forEach((f, i) => {
    lines.push(
      `| ${i + 1} | ${ms(f.selfMicros)} | ${ms(f.totalMicros)} | ${f.calls} | ${f.relation} | ${f.area} | \`${f.name}\` | ${sourceOf(f)} |`,
    );
  });
  if (report.topContext.length === 0) {
    lines.push(
      `| \u2014 | \u2014 | \u2014 | \u2014 | \u2014 | \u2014 | *no non-swaps frame above the ${report.contextMinPct}% noise floor* | \u2014 |`,
    );
  }
  return lines.join('\n');
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.profile) {
    printHelp();
    process.exit(args.help ? 0 : 1);
  }

  const profilePath = path.resolve(args.profile);
  if (!fs.existsSync(profilePath)) {
    process.stderr.write(`No such file: ${profilePath}\n`);
    process.exit(1);
  }

  const scopeRoots = args.scope
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);

  let analysis;
  try {
    analysis = loadProfile(profilePath, scopeRoots);
  } catch (e) {
    process.stderr.write(`Failed to parse ${profilePath}: ${e.message}\n`);
    process.exit(1);
  }

  const report = buildReport(analysis, args);

  const output = args.json ? JSON.stringify(report, null, 2) : renderMarkdown(report);
  if (args.out) {
    fs.writeFileSync(path.resolve(args.out), output, 'utf-8');
    process.stderr.write(`Wrote report to ${path.resolve(args.out)}\n`);
  } else {
    process.stdout.write(output + '\n');
  }
}

main();
