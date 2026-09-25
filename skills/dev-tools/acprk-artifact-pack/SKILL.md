---
name: artifact-pack
description: Use when preparing supplementary code/data for review (anonymous) or for an artifact-evaluation track after acceptance. Produces a reproducible artifact with README, one-command scripts, pinned dependencies, expected outputs with tolerances, a claims-to-commands map, and anonymous hosting during review.
---

# Artifact pack

Template: `templates/README_ARTIFACT.md` (in this skill directory).

## Goals (map to typical badges)

| badge (names vary by venue) | what it needs |
|---|---|
| Available | permanent public location (tagged repository or archive DOI) |
| Functional | documentation, completeness, runs, can be extended by others |
| Reproduced | an evaluator reruns the main experiments and the main claims hold within tolerance |

## Layout

```
artifact/
  README.md               claims → commands → expected outputs → time/resources
  LICENSE
  env/                    Dockerfile or environment pinning (requirements.txt with ==,
                          conda env.yml, or a Nix/Guix file); library commits pinned
  baselines/MANIFEST.md   third-party code: url + pinned commit/tag + build recipe
                          (fetch script, never vendored source trees)
  scripts/
    fetch_baselines.sh    clones pinned commits
    build.sh              builds everything
    smoke.sh              < 10 minutes; checks every component runs and outputs verify
    reproduce_table3.sh   one script per paper table/figure
  expected/               expected outputs (tables as csv, with tolerance notes)
  results/                empty; scripts write here
  EVIDENCE.md             subset of the project ledger: paper number → script → log
```

## Procedure

1. **Claims map.** From `EVIDENCE.md`, list every number/table/figure of the paper and
   the script that regenerates it. Main claims first. Anything that cannot be
   regenerated is marked "not reproduced by the artifact" with the reason.
2. **Pin everything**: compiler version, library commits, Python packages with
   `==`, estimator commit, random seeds. Record CPU/threads assumptions.
3. **Scripts**: one command per table; print the environment (CPU, compiler, commit)
   at the start; write logs to `results/`; verify correctness (decryption/cleartext
   reference) and fail loudly on mismatch.
4. **Expected outputs + tolerance**: absolute times vary by machine; state which
   quantities should match exactly (operation counts, parameters, security
   estimates, correctness) and which only in ratio (speedups, with an expected band).
   Explain that ratios come from interleaved runs in one session.
5. **Resource statement**: RAM, disk, cores, expected wall time per script; offer a
   reduced configuration for small machines.
6. **Smoke test** under 10 minutes; evaluators often start there.
7. **Anonymous hosting during review**: use an anonymising mirror service or a
   zip in the supplementary material. Run `anonymize-check` on the artifact
   directory and the zip (`.git` excluded, no usernames/hosts in logs, README without
   "our previous paper"). Refresh the mirror after the last push and check each file
   URL returns 200. Keep the archive under the venue's supplementary size cap.
8. **After acceptance**: de-anonymise, tag the release, archive (DOI), update the
   paper's artifact URL, submit to the artifact track within its window.

## Common failure modes

- Scripts depend on absolute paths or a local cache directory; use paths relative
  to the artifact root and environment variables with defaults.
- Stale build directories used for measurements; always build from clean in scripts.
- Baseline built with a different, slower configuration than in the paper; document
  flags in `baselines/MANIFEST.md`.
- Numbers in the paper from a noisy session that the artifact cannot reproduce;
  retract or re-measure before release.
- Hidden dependence on a proprietary tool (e.g. a commercial MILP solver or computer algebra system);
  provide a free fallback or state it clearly.
