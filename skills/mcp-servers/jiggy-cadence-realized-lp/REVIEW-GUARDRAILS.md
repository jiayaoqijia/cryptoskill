# Reading this repo without burning context

Some data files are enormous. Never run an unfiltered recursive grep here.

| file | lines | note |
|---|---|---|
| data/llama-predictions-t0.json | 138,079 | generated, do not read |
| data/spike-hunt8.json | 28,063 | generated, do not read |
| data/corpus.json | 15,129 | generated; read via `node -e` summary only |
| api/pools.json | 1 line, 72KB | single-line blob, will flood a terminal |

## Safe commands

Source only (this is what you want 95% of the time):
    git ls-files '*.js' '*.mjs' '*.html' '*.md' | grep -v node_modules

Search source, never data:
    grep -rn "PATTERN" bin/ lib/ scripts/ test/ --include='*.js'

Inspect a data file's SHAPE, not its contents:
    node -e "const d=require('./data/corpus.json'); console.log(Array.isArray(d)?d.length:Object.keys(d)); console.log(JSON.stringify(Array.isArray(d)?d[0]:d,null,1).slice(0,600))"

Always cap output:
    <command> | head -50
