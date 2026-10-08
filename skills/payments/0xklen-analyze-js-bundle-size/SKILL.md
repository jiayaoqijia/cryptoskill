---
name: analyze-js-bundle-size
description: Use when JavaScript payload grows without an obvious cause. Breaks a build down by module with source-map-explorer and webpack-bundle-analyzer.
---

# Analyze JavaScript Bundle Size

"Which import added 300 kB" is answerable in two commands; guessing wrong wastes a day. Measure the parsed size, not the gzipped file listing.

## Procedure

1. Record the baseline first:

       du -sh dist/assets/*.js | sort -h | tail -20

2. Emit a stats file from the bundler, then open the treemap:

       npx webpack --profile --json > dist/stats.json
       npx webpack-bundle-analyzer dist/stats.json

3. For a source-accurate view, keep source maps in the build and map every chunk back to modules:

       npx source-map-explorer 'dist/assets/*.js' --gzip

4. Sort by gzip size, then inspect the top three. A duplicate copy of a library (two React versions) shows as two adjacent nodes.
5. Check side-effect flags; a package without `"sideEffects":false` defeats tree-shaking and drags whole barrels in.
6. Replace a heavy leaf dependency only after measuring it: moment -> date-fns/dayjs, lodash -> `lodash-es` named imports, axios -> `fetch`.
7. Re-run step 3 and record the delta; a bundle action without a before/after number is not a result.

## Pitfalls

- Reading the network panel's transfer size and calling it runtime cost; parse and compile time scale with the uncompressed size.
- Analyzing production builds with `mode: development`, where nothing is minified and the numbers are 5x inflated.
- Removing source maps to shrink the build, which blinds every future analysis.
- Chasing the largest chunk while a 40 kB synchronous module sits in the critical path and blocks first paint.
- Importing from a package root (`import {x} from 'lib'`) when only one function is needed, pulling the whole barrel.

## Verification

    npx source-map-explorer 'dist/assets/*.js' --gzip --json | jq '.results[0].totalBytes'

The total gzipped bytes must be at or below the recorded baseline minus the intended reduction. Report the metric name, the before/after bytes, and the module that moved.
