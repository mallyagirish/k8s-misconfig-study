# Self-audit subsample — sampling manifest (AUTHOR-SIDE; contains label distribution)

- Built by `scripts/build_self_audit_packet.py`, seed 20261103.
- Population: the 340 matched validation rows that retain accepted AI pre-labels (451 matched minus 111 author-produced/adjudicated: 87 divergence + 30 blind, 6 in both), deduped to 301 distinct finding keys.
- Drawn: 100 distinct findings (allocation per rule proportional to the deduped population, floor 2, cap 14; within a rule, split across source groups proportionally). The draw covers 108 of the 340 rows (39 findings appear twice in the retained set by the sample's design).
- Draw by arm: {'helm': 30, 'github': 70}. Label distribution of the draw (author-side only): {'FP': 32, 'TP': 68}.

| Rule | Population (deduped) | Drawn |
|---|---:|---:|
| DEPRECATED_API | 13 | 5 |
| HOST_IPC | 13 | 5 |
| HOST_NETWORK | 12 | 5 |
| HOST_PID | 13 | 5 |
| IMG_LATEST | 12 | 4 |
| IMG_UNTAGGED | 10 | 4 |
| RBAC_CLUSTER_ADMIN_BINDING | 18 | 6 |
| RBAC_WILDCARD_RESOURCES | 12 | 4 |
| RBAC_WILDCARD_VERBS | 11 | 4 |
| REL_NO_LIVENESS_PROBE | 5 | 2 |
| REL_NO_READINESS_PROBE | 6 | 3 |
| RES_NO_CPU_LIMIT | 6 | 3 |
| RES_NO_MEM_LIMIT | 5 | 2 |
| RES_NO_REQUESTS | 5 | 2 |
| SA_TOKEN_AUTOMOUNTED | 12 | 4 |
| SECRET_COMMITTED | 13 | 5 |
| SECRET_LITERAL_ENV | 13 | 5 |
| SEC_CAPABILITY_ADDED | 13 | 5 |
| SEC_DANGEROUS_CAPABILITY | 13 | 5 |
| SEC_NO_SECCOMP | 12 | 4 |
| SEC_PRIVILEGED | 72 | 14 |
| SEC_RUN_AS_ROOT_EXPLICIT | 12 | 4 |

Scoring once labels are filled: `python3 scripts/score_self_audit.py`.
The key (KEY_sealed.csv) was kept out of git while the audit was blind;
now that the audit is scored and adjudicated, it is published here with
the replication package so the scorer can be rerun from a clean checkout.
