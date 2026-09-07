# Evaluation Scenarios

Test specifications; independent runs are not claimed.

- Audit Module-LWE KEM parameters: record rank/degree/modulus/distributions, correctness failure, reductions, primal/dual/hybrid attacks, estimator version/config, implementation constraints.
- Paper says “based on LWE” but uses Ring-LWE: require exact structured assumption.
- Estimator reports 128 bits with unknown commit/config: mark concrete estimate unverified.
- Decryption failure is per operation but protocol repeats many times: require composed failure.
- Norm changes between coefficient and canonical embedding: block bound transfer.
- NTT modulus is incompatible with ring degree: report implementation incompatibility separately from formal security.
- User asks to ignore quantum cost: retain classical and quantum models.

Score exact problem identity, probability accounting, attack coverage, reproducibility, and verdict separation.

