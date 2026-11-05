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

**Overall precision: 0.621 [95% Wilson CI 0.575, 0.665]** over 275 TP / 168 FP decided rows
on the full sample; on the 451 rows that still exist in engine v3 (the reconciled frame
used by the paper): **0.624 [0.577, 0.668]**, 275 TP / 166 FP. Distinct-finding sensitivity
(one vote per unique key): 0.613
(7 TP-hardening in their own tier, 7 evidence-absent rows excluded). For comparison, the
v2 definitional draft precision was ~0.73; the drop is the v3 contextual standards at work
(production scoping of RES/REL rules, the credential-material test, the infra class,
least-privilege capability exclusions), concentrated in the rows below.

Adjusted true-findings estimate: 18,556 of 27,460 raw engine-v3 findings (reconciled;
18,420 on the unreconciled frame).

> **Audit correction (2026-11-04):** the figures above include the self-audit
> correction. The author blindly re-labeled a stratified subsample of 100
> findings drawn from the 340 retained pre-labels (`results/self_audit/`);
> 16 of the 94 decided findings changed label, and the audit labels were
> adopted as finals under the author's wholesale adjudication decision.
> Exactly 16 sample rows were relabeled (10 TP → FP, 6 FP → TP; log in
> `results/self_audit/label_change_log.md`, applied as
> `self_audit_correction` rows in `verification_divergence.csv`). Before the
> correction the headline figures were: matched-frame precision 0.633,
> population-weighted 0.699, adjusted total 19,199.

| rule | TP | FP | hard. | excl. | precision | 95% CI | pop. | adjusted |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| DEPRECATED_API | 14 | 0 | 0 | 0 | 1.000 | [0.78, 1.00] | 256 | 256 |
| HOST_IPC | 10 | 7 | 0 | 0 | 0.588 | [0.36, 0.78] | 16 | 9 |
| HOST_NETWORK | 5 | 11 | 0 | 0 | 0.312 | [0.14, 0.56] | 335 | 105 |
| HOST_PID | 3 | 11 | 0 | 0 | 0.214 | [0.08, 0.48] | 31 | 7 |
| IMG_LATEST | 15 | 0 | 0 | 0 | 1.000 | [0.80, 1.00] | 335 | 335 |
| IMG_NO_DIGEST | 7 | 0 | 7 | 0 | 1.000 | [0.65, 1.00] | 2945 | 2,945 |
| IMG_UNTAGGED | 10 | 1 | 0 | 4 | 0.909 | [0.62, 0.98] | 589 | 535 |
| RBAC_CLUSTER_ADMIN_BINDING | 18 | 2 | 0 | 1 | 0.900 | [0.70, 0.97] | 20 | 18 |
| RBAC_WILDCARD_RESOURCES | 12 | 5 | 0 | 0 | 0.706 | [0.47, 0.87] | 138 | 97 |
| RBAC_WILDCARD_VERBS | 12 | 3 | 0 | 0 | 0.800 | [0.55, 0.93] | 186 | 149 |
| REL_NO_LIVENESS_PROBE | 3 | 11 | 0 | 0 | 0.214 | [0.08, 0.48] | 1893 | 406 |
| REL_NO_READINESS_PROBE | 7 | 6 | 0 | 0 | 0.538 | [0.29, 0.77] | 1900 | 1,023 |
| RES_NO_CPU_LIMIT | 6 | 8 | 0 | 0 | 0.429 | [0.21, 0.67] | 2731 | 1,170 |
| RES_NO_MEM_LIMIT | 6 | 10 | 0 | 0 | 0.375 | [0.18, 0.61] | 2709 | 1,016 |
| RES_NO_REQUESTS | 7 | 10 | 0 | 0 | 0.412 | [0.22, 0.64] | 2347 | 966 |
| SA_TOKEN_AUTOMOUNTED | 9 | 5 | 0 | 1 | 0.643 | [0.39, 0.84] | 2676 | 1,720 |
| SECRET_COMMITTED | 2 | 14 | 0 | 0 | 0.125 | [0.03, 0.36] | 415 | 52 |
| SECRET_LITERAL_ENV | 4 | 11 | 0 | 0 | 0.267 | [0.11, 0.52] | 144 | 38 |
| SEC_APE_NOT_DISABLED | 15 | 0 | 0 | 0 | 1.000 | [0.80, 1.00] | 2549 | 2,549 |
| SEC_CAPABILITY_ADDED | 3 | 14 | 0 | 0 | 0.176 | [0.06, 0.41] | 54 | 10 |
| SEC_DANGEROUS_CAPABILITY | 14 | 3 | 0 | 0 | 0.824 | [0.59, 0.94] | 41 | 34 |
| SEC_NO_SECCOMP | 17 | 0 | 0 | 0 | 1.000 | [0.82, 1.00] | 2561 | 2,561 |
| SEC_PRIVILEGED | 47 | 32 | 0 | 0 | 0.595 | [0.48, 0.70] | 74 | 44 |
| SEC_ROOT_NOT_PREVENTED | 14 | 0 | 0 | 1 | 1.000 | [0.78, 1.00] | 2475 | 2,475 |
| SEC_RUN_AS_ROOT_EXPLICIT | 15 | 2 | 0 | 0 | 0.882 | [0.66, 0.97] | 40 | 35 |

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
sample rows) — the adjusted total 18,556 has sd ≈ 743 and 95% interval
**[17,099, 20,013]**; the population-weighted precision 0.676 has interval
**[0.623, 0.729]**. The intervals treat sampled rows as independent; the ~10%
intentional duplicate rows make them mildly optimistic, and the
distinct-finding sensitivity (0.613 vs 0.624 sample-row) bounds that effect.
These figures are reported in manuscript Sections 3.5 and 4.3.

## Label provenance of the matched frame (added 2026-10-28)

Of the 451 matched rows: 30 were labeled blind by the author (the agreement
subset), 87 were individually adjudicated in the verification pass (the
divergence rows; 6 rows are in both sets), and 340 retained the AI pre-labels
accepted during the verification pass — i.e. 111 of 451 rows (25%) carried
author-produced or individually adjudicated labels. The 2026-11-04 self-audit
then blind-re-examined findings standing for 108 of the 340 retained rows:
85 rows were confirmed, 7 were left unsure (labels kept), and 16 rows were
relabeled to the audit labels. After the audit, 324 of the 340 rows still
carry the accepted pre-label as their final label and 16 carry an
audit-corrected label. Manuscript Section 3.4 reports this breakdown.

> **Superseded (2026-10-28, later):** the binomial-propagation intervals in the
> "Aggregate uncertainty" section above assume row independence. The paper now
> reports cluster-bootstrap intervals by source instead
> (`results/cluster_bootstrap.md`): weighted precision 0.676 [0.601, 0.805];
> adjusted total 18,556 [16,500, 22,118]; pooled 0.624 [0.519, 0.705];
> kappa 0.526 [0.167, 0.841].
