# Provisional precision under protocol v3 + addendum (2026-10-27)

**Status: VERIFIED by the author 2026-10-27.** Computed from the v2 pre-labels with the
92 divergence rows replaced by their v3/addendum recommendations
(`results/verification_divergence.csv`). The author reviewed the worklist and these
results and accepted the recommendations without override, so the divergence rows now
carry author-verified labels. Non-divergence rows carry their pre-labels under the
protocol's blank-equals-accept rule; a later spot-check override would recompute from
the same inputs. Adjusted prevalence was reconciled row-by-row against engine v3 on 2026-10-28
(`results/reconciliation_v3_DRAFT.md`, adopted with the manuscript draft): the headline
figures below are the reconciled ones.

**Overall precision: 0.630 [95% Wilson CI 0.584, 0.673]** over 279 TP / 164 FP decided rows
on the full sample; on the 451 rows that still exist in engine v3 (the reconciled frame
used by the paper): **0.633 [0.587, 0.676]**, 279 TP / 162 FP. Distinct-finding sensitivity
(one vote per unique key): 0.626
(7 TP-hardening in their own tier, 7 evidence-absent rows excluded). For comparison, the
v2 definitional draft precision was ~0.73; the drop is the v3 contextual standards at work
(production scoping of RES/REL rules, the credential-material test, the infra class,
least-privilege capability exclusions), concentrated in the rows below.

Adjusted true-findings estimate: 19,199 of 27,460 raw engine-v3 findings (reconciled;
19,062 on the unreconciled frame).

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
| REL_NO_READINESS_PROBE | 7 | 6 | 0 | 0 | 0.538 | [0.29, 0.77] | 1900 | 1,023 |
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

- **Frame drift: RESOLVED 2026-10-28** (`results/reconciliation_v3_DRAFT.md`). The sample
  was drawn from engine-v2 findings; every row was matched against engine v3 on
  (arm, source, kind, name, container, rule): 451 of 457 rows persist in v3. The 6 that
  left (4 already EXCLUDED, 2 REL_NO_READINESS_PROBE FPs) move only that rule's numbers
  (row above). The sample-exceeds-population cases (SEC_PRIVILEGED 79 vs 74, HOST_IPC
  17 vs 16) are explained by the sample's design, not drift: the build took ALL findings
  of those rules plus ~10% intentional duplicate rows (457 rows = 413 distinct keys; all
  44 duplicate pairs agree in final label).
- DEPRECATED_API and the IMG_NO_DIGEST hardening tier are reported as separate tiers
  per v3 amendments 4 and 1; they are included in the table but the paper's headline
  misconfiguration precision should be quoted with the tier treatment stated.
- K8S-012 (flagged in addendum amendment 11) resolved on per-grant inspection: one
  wildcard grant sits in the core group (verbs * on secrets), so the own-groups test
  fails and the row stays TP. No label change.

## Aggregate uncertainty (added 2026-10-28)

Propagating the per-rule binomial sampling variances — Var = Σ Nᵢ²·pᵢ(1−pᵢ)/nᵢ
over the 25 rules (Nᵢ = v3 population, pᵢ = per-rule precision, nᵢ = decided
sample rows) — the adjusted total 19,199 has sd ≈ 708 and 95% interval
**[17,810, 20,587]**; the population-weighted precision 0.699 has interval
**[0.649, 0.750]**. The intervals treat sampled rows as independent; the ~10%
intentional duplicate rows make them mildly optimistic, and the
distinct-finding sensitivity (0.626 vs 0.633 sample-row) bounds that effect.
These figures are reported in manuscript Sections 3.5 and 4.3.

## Label provenance of the matched frame (added 2026-10-28)

Of the 451 matched rows: 30 were labeled blind by the author (the agreement
subset), 87 were individually adjudicated in the verification pass (the
divergence rows; 6 rows are in both sets), and 340 retain the AI pre-labels
accepted during the verification pass — i.e. 111 of 451 rows (25%) carry
author-produced or individually adjudicated labels. Manuscript Section 3.4
reports this breakdown.

> **Superseded (2026-10-28, later):** the binomial-propagation intervals in the
> "Aggregate uncertainty" section above assume row independence. The paper now
> reports cluster-bootstrap intervals by source instead
> (`results/cluster_bootstrap.md`): weighted precision 0.699 [0.623, 0.840];
> adjusted total 19,199 [17,120, 23,071]; pooled 0.633 [0.527, 0.714];
> kappa 0.526 [0.167, 0.841].
