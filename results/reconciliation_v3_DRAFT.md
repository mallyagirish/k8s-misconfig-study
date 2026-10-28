# Sample-to-v3 reconciliation (2026-10-28)

**Status: adopted 2026-10-28 as the basis for the manuscript's figures**
(the precision file's caveat section and readiness row are updated accordingly).
Prepared 2026-10-28 by matching every row of `results/labeling_sample_v2.csv`
(457 rows) against `results/findings_v3.jsonl` (27,460 findings) on the key
(arm, source, kind, name, container, rule). Final labels are the author-verified
set from `results/precision_provisional.md`: pre-labels with the 92 divergence
rows replaced by their v3/addendum recommendations (accepted without override
2026-10-27, commit 6cc1ce3).

## Headline

- **451 of 457 sampled rows still exist in engine v3; 6 do not.**
- Overall precision on the 451 matched rows: **0.633 [0.587, 0.676]**
  (279 TP / 162 FP decided; 7 TP-hardening, 3 EXCLUDED among the matched rows),
  vs 0.630 [0.584, 0.673] provisional — essentially unchanged.
- Recomputed adjusted true findings, same per-rule method as the provisional
  file (precision x v3 population, summed): **19,199**, vs 19,062 provisional
  (+137; +136 from REL_NO_READINESS_PROBE, +1 rounding across rules).
- The frame-drift caveat in `precision_provisional.md` is therefore resolved
  on a row basis, with one rule's numbers moving.

## The 6 rows that left v3

| sample | rule | final label | source |
|---|---|---|---|
| K8S-113 | IMG_UNTAGGED | EXCLUDED | github/argoproj_argo-cd__examples__known-hosts__argocd-known-hosts-mounts.yaml, Deployment argocd-application-controller |
| K8S-207 | IMG_UNTAGGED | EXCLUDED | same file, Deployment argocd-server |
| K8S-236 | IMG_UNTAGGED | EXCLUDED | github/Yolean_kubernetes-kafka__variants__scale-6-9__zoo-9.yaml, StatefulSet zoo, init-config |
| K8S-371 | IMG_UNTAGGED | EXCLUDED | same Yolean file/container (duplicate key of K8S-236) |
| K8S-202 | REL_NO_READINESS_PROBE | FP | helm/qdrant.yaml, StatefulSet pilot-qdrant, ensure-dir-ownership |
| K8S-213 | REL_NO_READINESS_PROBE | FP | github/kubernetes-sigs_kustomize__examples__transformerconfigs__images__resources.yaml, Deployment deploy1, nginx2 |

Four of the six were already EXCLUDED, so they carry no precision weight.
Only REL_NO_READINESS_PROBE moves: 7 TP / 6 FP matched (was 7/8),
precision **0.467 -> 0.538 [0.291, 0.768]**, adjusted **887 -> 1,023**
of a 1,900 v3 population. IMG_UNTAGGED is unchanged (9 TP / 2 FP in
both the full and matched sets; its 4 dropped rows were all EXCLUDED).
Every other rule's matched precision equals its provisional precision.

## The sample > population paradox, resolved

The provisional caveat flagged SEC_PRIVILEGED (79 sampled vs 74 in v3) and
HOST_IPC (17 vs 16). Both are explained by the sample's construction, not
by frame drift: the 2026-10-21 sample build took ALL SEC_PRIVILEGED (74)
and RBAC_CLUSTER_ADMIN_BINDING (20) findings plus stratified samples of
the other rules, with **~10% hidden duplicate rows included by design**.
On distinct finding keys:

- SEC_PRIVILEGED: 79 rows = **74 distinct keys = the 74 v3 findings**
  (the 5 extra rows are the intentional duplicates).
- HOST_IPC: 17 rows = 14 distinct keys < 16 v3 findings.
- Across the sample: 457 rows = **413 distinct keys**, with 44 duplicate
  key pairs. All 44 duplicate pairs carry the **same** final label, so
  the duplicates never flip a finding's verdict.

Row-basis reporting is therefore the design-correct primary (it is how
the sample was drawn and how the provisional figures were computed).
Distinct-finding sensitivity check (one vote per key, matched subset):
overall precision **0.626** (249 TP / 149 FP over 408 matched distinct keys),
vs 0.633 row-basis — the same story, not a different one. It is a
sensitivity note for the methods section, not a replacement for the
row-basis figures.

## What this draft does NOT change

- Precision figures and labels in `precision_provisional.md` remain the
  verified record; on adoption (2026-10-28) its caveat section was updated,
  the REL_NO_READINESS_PROBE row and the adjusted total were replaced with
  the reconciled figures, and the distinct-key sensitivity note was added.
