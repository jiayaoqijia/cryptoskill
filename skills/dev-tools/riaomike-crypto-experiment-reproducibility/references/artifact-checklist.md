# Artifact Checklist

## Availability

- stable or review-appropriate access; anonymized when required;
- license, data rights, privacy, embargo/disclosure constraints;
- versioned source/data/configuration and integrity hashes;
- explicit omissions and reasons.

## Functionality

- clean-machine installation or environment definition;
- no undocumented absolute paths, credentials, private services, or author infrastructure;
- smoke test and expected output;
- deterministic orchestration where possible;
- hardware/software/runtime/storage requirements;
- actionable failure diagnostics.

## Reproducibility

- every paper claim/table/figure links to an artifact step;
- raw inputs/outputs and processing scripts;
- seeds, repetitions, warmup, outlier rule, uncertainty/statistical test;
- baseline versions/configuration and fair resource limits;
- accepted tolerance and explanation of nondeterminism;
- full and evaluator-scale experiment relationship.

## Cryptography specifics

- security parameter and concrete parameter file;
- test vectors and correctness/failure cases;
- estimator/proof-checker versions and raw outputs;
- setup/ceremony/trusted material boundaries;
- constant-time and side-channel scope;
- no secret keys, toxic waste, personal data, active exploits, or reviewer tracking.

## Evidence grades

Available, functional, results reproduced, supported with limitations, or not assessable. Do not award a grade the actual run did not establish.

