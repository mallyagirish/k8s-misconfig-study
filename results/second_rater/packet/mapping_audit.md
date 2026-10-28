# Scanner check-to-rule mapping audit (optional second task)

The study compares four scanners (kube-linter, kubeaudit, Polaris, Checkov)
against its own 25 rules. The mapping below — which scanner check stands for
which rule — was built by the author from the tools' documentation and output.
It is partly judgment-based. Please sanity-check it, especially the flagged
calls in the second section: for each, mark **agree** / **disagree** and add a
note if you would map it differently. If you spot a check that is mis-assigned
or a rule a tool *does* cover that is shown as uncovered, note that too.

## The mapping (counts are the tool's findings on the study's Helm corpus)

| Our rule (our findings) | kube-linter | kubeaudit | Polaris | Checkov |
|---|---|---|---|---|
| SA_TOKEN_AUTOMOUNTED (342) | — | AutomountSATokenTrueAndDefaultSA: 91 (narrower: default SA only) | — | CKV_K8S_38: 356 |
| IMG_NO_DIGEST (576) | — | — | — (pullPolicyNotAlways: 517 is a proxy, not pinning) | CKV_K8S_43: 391 — **only tool that checks** |
| IMG_UNTAGGED (14) | merged ↓ | ImageTagMissing: 14 (exact) | tagNotSpecified: 55 (merged) | merged ↓ |
| IMG_LATEST (41) | latest-tag: 55 (= 41 latest + 14 untagged, exact reconciliation) | — | merged ↑ | CKV_K8S_14: 51 (merged) |
| RES_NO_CPU_LIMIT (502) | unset-cpu-requirements: 416 (merged w/ requests) | LimitsCPUNotSet: 76; LimitsNotSet: 421 (pod-level units) | cpuLimitsMissing: 411 | CKV_K8S_11: 343 |
| RES_NO_MEM_LIMIT (479) | unset-memory-requirements: 479 (**exact**) | LimitsMemoryNotSet: 53; LimitsNotSet: 421 | memoryLimitsMissing: 388 | CKV_K8S_13: 327 |
| RES_NO_REQUESTS (414) | merged into unset-* | — (no requests auditor) | cpuRequestsMissing: 335; memoryRequestsMissing: 334 | CKV_K8S_10: 177; CKV_K8S_12: 178 |
| SEC_NO_SECCOMP (370) | — | SeccompProfileMissing: 239 | linuxHardening: 298 (composite) | CKV_K8S_31: 240 |
| SEC_APE_NOT_DISABLED (309) | privilege-escalation-container: 34 | APE Nil: 295 + True: 10 = 305 | privilegeEscalationAllowed: 309 (**exact**) | CKV_K8S_20: 201 |
| SEC_ROOT_NOT_PREVENTED (293) | run-as-non-root: 280 | RunAsNonRootNil: 254 (+CSCRoot: 21) | runAsRootAllowed: 280 | CKV_K8S_23: 162 (narrower) |
| SEC_RUN_AS_ROOT_EXPLICIT (23) | merged ↑ | RunAsUserCSCRoot: 21 + PSCRoot: 1 = 22 | merged ↑ | merged ↑ |
| SEC_PRIVILEGED (27) | privileged-container: 27 (**exact**) | PrivilegedTrue: 26 | runAsPrivileged: 27 (**exact**) | CKV_K8S_16: 22 |
| SEC_CAPABILITY_ADDED (15) | drop-net-raw-capability: 15 (NET_RAW only) | CapabilityAdded: 58 (any capability) | insecureCapabilities: 313 (incl. not dropping) | CKV_K8S_37: 205 (incl. defaults) |
| SEC_DANGEROUS_CAPABILITY (12) | unsafe-sysctls/docker-sock: ~2 | CapabilityShouldDropAll: 11 | dangerousCapabilities: 12 (**exact**) | CKV_K8S_39 (SYS_ADMIN): 8 |
| HOST_NETWORK (23) | host-network: 23 (**exact**) | NamespaceHostNetworkTrue: 23 (**exact**) | — (hostPortSet: 3 is a different property) | CKV_K8S_19: 23 (**exact**) |
| HOST_PID (9) | host-pid: 9 (**exact**) | NamespaceHostPIDTrue: 9 (**exact**) | — | CKV_K8S_17: 9 (**exact**) |
| HOST_IPC (1) | host-ipc: 1 (**exact**) | NamespaceHostIPCTrue: 1 (**exact**) | — | CKV_K8S_18: 1 (**exact**) |
| REL_NO_LIVENESS_PROBE (211) | liveness-port: 26 — checks probe *port validity*, NOT missing probes | — | livenessProbeMissing: 211 | CKV_K8S_8: 157 |
| REL_NO_READINESS_PROBE (204) | readiness-port: 24 — same caveat | — | readinessProbeMissing: 205 | CKV_K8S_9: 144 |
| SECRET_LITERAL_ENV (29) | env-var-secret: 14 | — | sensitiveContainerEnvVar: 30 | CKV_K8S_35: 84 (broader) |
| SECRET_COMMITTED (122) | — | — | — | — (**no tool flags committed Secret objects**) |
| RBAC_WILDCARD_VERBS (91) | — | — | — (RBAC checks target exec/cluster-admin patterns) | CKV_K8S_49: 29 (partial, merged w/ resources) |
| RBAC_WILDCARD_RESOURCES (64) | — | — | — | merged ↑ |
| RBAC_CLUSTER_ADMIN_BINDING (7) | — | — | clusterrolebindingClusterAdmin: 21 + rolebindingClusterAdminRole: 10 (broader) | CKV2 graph checks: ~4–23 (partial) |
| DEPRECATED_API (2) | deprecated-service-account-field: 3 (a field, not an API version) | DeprecatedAPIUsed: 4 | — | — |

## Judgment calls to audit

1. kube-linter `liveness-port` / `readiness-port` validate probe *ports*, not probe absence — treated as **no check** for REL_NO_LIVENESS_PROBE / REL_NO_READINESS_PROBE.
   - [ ] agree  [ ] disagree — notes: ______

2. kube-linter `deprecated-service-account-field` flags a deprecated field, not token automounting — treated as **no check** for SA_TOKEN_AUTOMOUNTED.
   - [ ] agree  [ ] disagree — notes: ______

3. kube-linter `unsafe-sysctls` / `docker-sock` cover adjacent dangers, not added capabilities per se — treated as **no check** for SEC_DANGEROUS_CAPABILITY.
   - [ ] agree  [ ] disagree — notes: ______

4. Polaris `pullPolicyNotAlways` is a proxy for, not a test of, digest pinning — treated as **no check** for IMG_NO_DIGEST.
   - [ ] agree  [ ] disagree — notes: ______

5. Checkov's cluster-admin-binding coverage would have to come from unspecified CKV2 graph checks; none of CKV2_K8S_1–5 in the output is a cluster-admin-binding check — treated as **unmappable / no check** for RBAC_CLUSTER_ADMIN_BINDING.
   - [ ] agree  [ ] disagree — notes: ______

6. kube-linter `latest-tag` fires on both untagged and `:latest` images — a `latest-tag` report counts as detection for **both** IMG_LATEST and IMG_UNTAGGED (merged).
   - [ ] agree  [ ] disagree — notes: ______

7. kubeaudit `LimitsNotSet` is a pod-level union over CPU and memory — counts toward **both** RES_NO_CPU_LIMIT and RES_NO_MEM_LIMIT.
   - [ ] agree  [ ] disagree — notes: ______

8. Polaris `linuxHardening` is a composite (seccomp among other properties) — mapped to SEC_NO_SECCOMP.
   - [ ] agree  [ ] disagree — notes: ______

9. kubeaudit reports allowPrivilegeEscalation as two auditors (Nil and True) — combined for SEC_APE_NOT_DISABLED.
   - [ ] agree  [ ] disagree — notes: ______

10. Checkov output identifies objects but not containers; kube-linter names the container in its messages — Checkov joins at object level; kube-linter at container level.
   - [ ] agree  [ ] disagree — notes: ______

## Anything else

- A check mapped to the wrong rule: ______
- A rule shown as uncovered that a tool does check: ______
- Other concerns: ______
