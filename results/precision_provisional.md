# Provisional precision under protocol v3 + addendum (2026-10-27)

**Status: PROVISIONAL.** Computed from the v2 pre-labels with the 92 divergence rows
replaced by their v3/addendum recommendations (`results/verification_divergence.csv`).
These numbers become final only after the author's verification pass; any override
recomputes from the same script inputs. Non-divergence rows carry their pre-labels.

**Overall precision: 0.630 [95% Wilson CI 0.584, 0.673]** over 279 TP / 164 FP decided rows
(7 TP-hardening in their own tier, 7 evidence-absent rows excluded). For comparison, the
v2 definitional draft precision was ~0.73; the drop is the v3 contextual standards at work
(production scoping of RES/REL rules, the credential-material test, the infra class,
least-privilege capability exclusions), concentrated in the rows below.

Adjusted true-findings estimate: 19,062 of 27,460 raw engine-v3 findings.

| rule | TP | FP | hard. | excl. | precision | 95% CI | pop. | adjusted |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| DEPRECATED_API | 14 | 0 | 0 | 0 | 1.000 | [0.78, 1.00] | 256 | 256 |
| HOST_IPC | 10 | 7 | 0 | 0 | 0.588 | [0.36, 0.78] | 16 | 9 |
| HOST_NETWORK | 4 | 12 | 0 | 0 | 0.250 | [0.10, 0.49] | 335 | 84 |
| HOST_PID | 3 | 11 | 0 | 0 | 0.214 | [0.08, 0.48] | 31 | 7 |
| IMG_LATEST | 15 | 0 | 0 | 0 | 1.000 | [0.80, 1.00] | 335 | 335 |
| IMG_NO_DIGEST | 7 | 0 | 7 | 0 | 1.000 | [0.65, 1.00] | 2945 | 2,945 |
| IMG_UNTAGGED | 9 | 2 | 0 | 4 | 0.818 | [0.52, 0.95] | 589 | 482 |
| RBAC_CLUSTER_ADMIN_BINDING | 16 | 4 | 0 | 1 | 0.800 | [0.58, 0.92] | 20 | 16 |
| RBAC_WILDCARD_RESOURCES | 11 | 6 | 0 | 0 | 0.647 | [0.41, 0.83] | 138 | 89 |
| RBAC_WILDCARD_VERBS | 11 | 4 | 0 | 0 | 0.733 | [0.48, 0.89] | 186 | 136 |
| REL_NO_LIVENESS_PROBE | 3 | 11 | 0 | 0 | 0.214 | [0.08, 0.48] | 1893 | 406 |
| REL_NO_READINESS_PROBE | 7 | 8 | 0 | 0 | 0.467 | [0.25, 0.70] | 1900 | 887 |
| RES_NO_CPU_LIMIT | 6 | 8 | 0 | 0 | 0.429 | [0.21, 0.67] | 2731 | 1,170 |
| RES_NO_MEM_LIMIT | 6 | 10 | 0 | 0 | 0.375 | [0.18, 0.61] | 2709 | 1,016 |
| RES_NO_REQUESTS | 8 | 9 | 0 | 0 | 0.471 | [0.26, 0.69] | 2347 | 1,104 |
| SA_TOKEN_AUTOMOUNTED | 12 | 2 | 0 | 1 | 0.857 | [0.60, 0.96] | 2676 | 2,294 |
| SECRET_COMMITTED | 2 | 14 | 0 | 0 | 0.125 | [0.03, 0.36] | 415 | 52 |
| SECRET_LITERAL_ENV | 6 | 9 | 0 | 0 | 0.400 | [0.20, 0.64] | 144 | 58 |
| SEC_APE_NOT_DISABLED | 15 | 0 | 0 | 0 | 1.000 | [0.80, 1.00] | 2549 | 2,549 |
| SEC_CAPABILITY_ADDED | 4 | 13 | 0 | 0 | 0.235 | [0.10, 0.47] | 54 | 13 |
| SEC_DANGEROUS_CAPABILITY | 14 | 3 | 0 | 0 | 0.824 | [0.59, 0.94] | 41 | 34 |
| SEC_NO_SECCOMP | 17 | 0 | 0 | 0 | 1.000 | [0.82, 1.00] | 2561 | 2,561 |
| SEC_PRIVILEGED | 48 | 31 | 0 | 0 | 0.608 | [0.50, 0.71] | 74 | 45 |
| SEC_ROOT_NOT_PREVENTED | 14 | 0 | 0 | 1 | 1.000 | [0.78, 1.00] | 2475 | 2,475 |
| SEC_RUN_AS_ROOT_EXPLICIT | 17 | 0 | 0 | 0 | 1.000 | [0.82, 1.00] | 40 | 40 |

## Caveats for the final run

- **Frame drift:** the validation sample was drawn from engine-v2 findings; the population
  column is engine v3. For small-count rules the sample can exceed the v3 population
  (SEC_PRIVILEGED 79 sampled vs 74 in v3; HOST_IPC 17 vs 16). Precision (a within-sample
  quantity) is unaffected; adjusted prevalence for those rules is unreliable until the
  sample is reconciled against v3 findings row by row.
- DEPRECATED_API and the IMG_NO_DIGEST hardening tier are reported as separate tiers
  per v3 amendments 4 and 1; they are included in the table but the paper's headline
  misconfiguration precision should be quoted with the tier treatment stated.
- K8S-012 (flagged in addendum amendment 11) resolved on per-grant inspection: one
  wildcard grant sits in the core group (verbs * on secrets), so the own-groups test
  fails and the row stays TP. No label change.
