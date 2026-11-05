# Self-audit label changes applied (2026-11-04)

The 16 findings whose labels changed in the blind self-audit
(`audit_results.md`) had their audit labels adopted as finals under the
author's wholesale adjudication decision ("audit label wins on all 16",
2026-11-04). Each changed finding stands for exactly one reference sample
row (`rows_covered` = 1 in the sealed key), so exactly 16 sample rows were
relabeled — no other labels were touched, and the 6 unsure audit rows keep
their original labels.

Mechanism: the 16 rows were appended to `results/verification_divergence.csv`
with `divergence_class = self_audit_correction` and `recommended_v3` = the
audit label, so the standard final-label construction (pre-label, replaced
by the divergence recommendation where one exists) and the unmodified
pipeline (`scripts/cluster_bootstrap.py`, seed 20261028) produce the
corrected figures. The full audit trail is in `adjudication.csv` (finals)
and the sealed key.

| Audit ID | Sample row | Rule | Arm | Old label | New label |
|---|---|---|---|---|---|
| SA-001 | K8S-392 | HOST_NETWORK | helm | FP | TP |
| SA-007 | K8S-364 | IMG_UNTAGGED | helm | FP | TP |
| SA-012 | K8S-314 | RES_NO_REQUESTS | helm | TP | FP |
| SA-024 | K8S-335 | SECRET_LITERAL_ENV | github | TP | FP |
| SA-027 | K8S-325 | SEC_RUN_AS_ROOT_EXPLICIT | helm | TP | FP |
| SA-035 | K8S-033 | SA_TOKEN_AUTOMOUNTED | github | TP | FP |
| SA-039 | K8S-296 | RBAC_CLUSTER_ADMIN_BINDING | github | FP | TP |
| SA-041 | K8S-039 | SECRET_LITERAL_ENV | github | TP | FP |
| SA-043 | K8S-428 | RBAC_WILDCARD_RESOURCES | helm | FP | TP |
| SA-052 | K8S-245 | SEC_CAPABILITY_ADDED | github | TP | FP |
| SA-053 | K8S-379 | SEC_PRIVILEGED | github | TP | FP |
| SA-054 | K8S-226 | RBAC_CLUSTER_ADMIN_BINDING | github | FP | TP |
| SA-073 | K8S-286 | SEC_RUN_AS_ROOT_EXPLICIT | helm | TP | FP |
| SA-076 | K8S-143 | SA_TOKEN_AUTOMOUNTED | github | TP | FP |
| SA-086 | K8S-019 | SA_TOKEN_AUTOMOUNTED | github | TP | FP |
| SA-091 | K8S-008 | RBAC_WILDCARD_VERBS | github | FP | TP |

Direction: 10 TP → FP, 6 FP → TP. Matched-frame totals move from
279 TP / 162 FP to 275 TP / 166 FP (441 decided rows, unchanged).
