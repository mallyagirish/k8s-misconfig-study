# Second-rater subsample — sampling manifest (AUTHOR-SIDE; contains label distribution)

- Built by `scripts/build_second_rater_packet.py`, seed 20261028.
- Frame: 450 rows with final verified labels (TP/FP/TP-hardening); deduped to 407 distinct finding keys.
- Drawn: 150 (Batch A 98, Batch B 52); allocation per rule proportional to the deduped frame, floor 2, cap 14.
- Label distribution of the draw (author-side only): {'TP': 89, 'FP': 59, 'TP-hardening': 2}.

| Rule | Frame (deduped) | Drawn |
|---|---:|---:|
| DEPRECATED_API | 14 | 6 |
| HOST_IPC | 14 | 6 |
| HOST_NETWORK | 14 | 6 |
| HOST_PID | 14 | 6 |
| IMG_LATEST | 14 | 6 |
| IMG_NO_DIGEST | 14 | 6 |
| IMG_UNTAGGED | 11 | 4 |
| RBAC_CLUSTER_ADMIN_BINDING | 19 | 7 |
| RBAC_WILDCARD_RESOURCES | 13 | 5 |
| RBAC_WILDCARD_VERBS | 12 | 5 |
| REL_NO_LIVENESS_PROBE | 14 | 6 |
| REL_NO_READINESS_PROBE | 14 | 6 |
| RES_NO_CPU_LIMIT | 14 | 6 |
| RES_NO_MEM_LIMIT | 14 | 6 |
| RES_NO_REQUESTS | 14 | 6 |
| SA_TOKEN_AUTOMOUNTED | 13 | 5 |
| SECRET_COMMITTED | 14 | 6 |
| SECRET_LITERAL_ENV | 14 | 6 |
| SEC_APE_NOT_DISABLED | 14 | 6 |
| SEC_CAPABILITY_ADDED | 14 | 6 |
| SEC_DANGEROUS_CAPABILITY | 14 | 5 |
| SEC_NO_SECCOMP | 14 | 5 |
| SEC_PRIVILEGED | 74 | 14 |
| SEC_ROOT_NOT_PREVENTED | 13 | 5 |
| SEC_RUN_AS_ROOT_EXPLICIT | 14 | 5 |

Scoring once labels return: `python3 scripts/score_second_rater.py <returned csv>`.
The key (KEY_sealed.csv) stays out of git until the rater returns the sheet;
it is published with the replication package afterwards.
