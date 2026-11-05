# Self-audit scoring output (2026-11-04)

## Summary — design-weighted estimate (weighting correction, 2026-11-04)

The packet was not a simple random sample: allocation was fixed per rule in
proportion to the rule's share of the 301 distinct retained findings, floor 2,
cap 14 (SEC_PRIVILEGED capped at 14 of its 72 findings), with each rule's
allocation split across source groups proportionally (seed 20261103). The
unweighted rate is therefore a description of the sample as drawn, not an
estimate for the retained population, and the Wilson interval does not match
the design. The scorer now also reports the design-based figures:

- **Population estimate (primary): stratified population-weighted change
  rate 16.4%** [stratified bootstrap 95% CI 10.1%, 23.1%; 2,000 replicates,
  seed 20261104]. Strata are rules; each rule's decided findings are weighted
  by the rule's population of distinct retained findings. Strata with decided
  rows cover **288 of the 301** distinct retained findings.
- **Sample description: 16 of 94 decided findings changed = 17.0%**
  [95% Wilson CI 10.8%, 25.9%] — the unweighted rate over the draw.
- **No decided rows: DEPRECATED_API** — all 5 of its draws were labeled
  unsure, so its 13 findings contribute no decided rows and are outside the
  estimate's coverage.
- **Unsure sensitivity:** treating all 6 unsure findings as unchanged vs
  changed bounds the weighted estimate at **[15.6%, 20.8%]** (unweighted
  bounds [16.0%, 22.0%] over all 100 returned findings).
- Sensitivity at the finer rule × source-group grid: 18.1% over 277 of 301
  findings (11 one-finding cells received no draw, so that grid cannot carry
  the primary estimate).

Full scorer output (`python3 scripts/score_self_audit.py`):

returned = 100   audit-unsure = 6   decided = 94

label-change rate = 16/94 = 17.0%  [95% Wilson CI 10.8%, 25.9%]
direction: FP->TP: 6, TP->FP: 10

design-weighted estimate (stratified by rule; the unweighted rate above
describes the sample as drawn, this estimates the retained population):
  population-weighted change rate = 16.4%  [stratified bootstrap 95% CI 10.1%, 23.1%; 2,000 replicates, seed 20261104]
  coverage: strata with decided rows hold 288 of the 301 distinct retained findings
  no decided rows: DEPRECATED_API (13 findings; all their draws were unsure)
  unsure sensitivity: weighted [15.6%, 20.8%] if all 6 unsure count as unchanged vs changed; unweighted [16.0%, 22.0%]
  sensitivity, rule x source-group strata: 18.1% over 277 of 301 findings

per rule family (decided rows):
  RBAC and secrets             6/24 changed  [12%, 45%]
  host access                  4/19 changed  [9%, 43%]
  images                       1/8 changed  [2%, 47%]
  reliability                  0/5 changed  [0%, 43%]
  resources                    1/7 changed  [3%, 51%]
  security context             4/31 changed  [5%, 29%]

per rule (decided rows):
  HOST_IPC                     0/5 changed  [0%, 43%]
  HOST_NETWORK                 1/5 changed  [4%, 62%]
  HOST_PID                     0/5 changed  [0%, 43%]
  IMG_LATEST                   0/4 changed  [0%, 49%]
  IMG_UNTAGGED                 1/4 changed  [5%, 70%]
  RBAC_CLUSTER_ADMIN_BINDING   2/6 changed  [10%, 70%]
  RBAC_WILDCARD_RESOURCES      1/4 changed  [5%, 70%]
  RBAC_WILDCARD_VERBS          1/4 changed  [5%, 70%]
  REL_NO_LIVENESS_PROBE        0/2 changed  [0%, 66%]
  REL_NO_READINESS_PROBE       0/3 changed  [0%, 56%]
  RES_NO_CPU_LIMIT             0/3 changed  [0%, 56%]
  RES_NO_MEM_LIMIT             0/2 changed  [0%, 66%]
  RES_NO_REQUESTS              1/2 changed  [9%, 91%]
  SA_TOKEN_AUTOMOUNTED         3/4 changed  [30%, 95%]
  SECRET_COMMITTED             0/5 changed  [0%, 43%]
  SECRET_LITERAL_ENV           2/5 changed  [12%, 77%]
  SEC_CAPABILITY_ADDED         1/5 changed  [4%, 62%]
  SEC_DANGEROUS_CAPABILITY     0/4 changed  [0%, 49%]
  SEC_NO_SECCOMP               0/4 changed  [0%, 49%]
  SEC_PRIVILEGED               1/14 changed  [1%, 31%]
  SEC_RUN_AS_ROOT_EXPLICIT     2/4 changed  [15%, 85%]

changed rows (original -> audit):
  SA-001 (K8S-392) HOST_NETWORK                 FP -> TP reason= notes=The uninstall Job is explicitly configured with host networking. The packet identifies a Tigera operator cleanup task, but it does not show that host networking is required for this cleanup operation. Under the rule, the property is present and no supported infrastructure-necessity exception is established. :: helm/tigera-operator.yaml
  SA-007 (K8S-364) IMG_UNTAGGED                 FP -> TP reason= notes=The rendered image value is `auto`, with no explicit tag or digest visible in the packet. Under the image rule, an image with no tag is a misconfiguration; the packet does not establish that this value is merely an unresolved template. :: helm/gateway.yaml
  SA-012 (K8S-314) RES_NO_REQUESTS              TP -> FP reason=fixture notes=This is a one-shot Job. The protocol expressly classifies RES_* findings on Jobs as false positives for this study's production-scoped resource rules, regardless of whether requests are absent. :: helm/victoria-metrics-k8s-stack.yaml
  SA-024 (K8S-335) SECRET_LITERAL_ENV           TP -> FP reason=fixture notes=The literal `giteaPassword1234` appears in a Tekton pipeline test fixture used to configure a test Gitea instance. In this test-path context, it is test credential material rather than evidence of a production secret committed in a deployment configuration. :: github/tektoncd_pipeline__test__git-resolver__gitea.yaml
  SA-027 (K8S-325) SEC_RUN_AS_ROOT_EXPLICIT     TP -> FP reason=infra-need notes=The container is named `fsgroup-volume` and runs as UID 0 while the pod-level user is 1000. This is a volume-permissions helper whose function is to adjust filesystem ownership; root is plausibly required for that operation, so the root setting is tied to the helper's infrastructure setup task. :: helm/graylog.yaml
  SA-035 (K8S-033) SA_TOKEN_AUTOMOUNTED         TP -> FP reason=infra-need notes=This is the ingress-nginx controller. Controllers commonly need Kubernetes API access to watch Ingresses, Services, Secrets, and related resources; the protocol explicitly treats controllers requiring API access as infrastructure-need exceptions. The packet shows inherited/default automount settings rather than an explicit disable. :: github/kubernetes_ingress-nginx__docs__examples__static-ip__nginx-ingress-controller.yaml
  SA-039 (K8S-296) RBAC_CLUSTER_ADMIN_BINDING   FP -> TP reason= notes=The RoleBinding references the cluster-admin ClusterRole and binds it to a named user. That is a direct cluster-admin grant; the test-fixture path does not negate the privilege represented by the binding under this rule. :: github/kubescape_regolibrary__rules__cluster-admin-role__test__clusterrole-rolebinding__input__rolebinding.yaml
  SA-041 (K8S-039) SECRET_LITERAL_ENV           TP -> FP reason=fixture notes=The literal MYSQL_ROOT_PASSWORD value appears in a Kubescape rule-test CronJob fixture. It is a canned test value in a test input, not a credential demonstrated to be used by a production workload. :: github/kubescape_regolibrary__rules__set-procmount-default__test__cronjob__input__cronjob.yaml
  SA-043 (K8S-428) RBAC_WILDCARD_RESOURCES      FP -> TP reason= notes=The role grants wildcard resources for several API groups, including groups not owned by Datadog (for example EKS and Karpenter groups). The protocol's exception requires every wildcard grant to be confined to the same project's own API groups; that condition is not met. :: helm/datadog.yaml
  SA-052 (K8S-245) SEC_CAPABILITY_ADDED         TP -> FP reason=standard-practice notes=The only added capability is NET_RAW, which is part of the conventional default Linux container capability set. The protocol excludes additions limited to default-set capabilities from this rule, so this is not a qualifying added-capability misconfiguration. :: github/fugue_regula__rego__tests__rules__k8s__capabilities_assigned__inputs__invalid_example.yaml
  SA-053 (K8S-379) SEC_PRIVILEGED               TP -> FP reason=infra-need notes=Promtail is a node-level log-collection DaemonSet component in the Loki operator's development add-ons. Log collectors require host-level access to read node/container logs; the protocol's node-agent infrastructure exception is the closest applicable classification. :: github/grafana_loki__operator__hack__addons_dev.yaml
  SA-054 (K8S-226) RBAC_CLUSTER_ADMIN_BINDING   FP -> TP reason= notes=The RoleBinding references cluster-admin and binds it to a user and a service account. The fact that the file is under testdata does not remove the actual cluster-admin binding, and the protocol does not exempt this rule for fixtures. :: github/fluxcd_flux2__cmd__flux__testdata__create_tenant__tenant-with-service-account.yaml
  SA-073 (K8S-286) SEC_RUN_AS_ROOT_EXPLICIT     TP -> FP reason=infra-need notes=The `volume-permissions` container runs as UID 0 as part of a MongoDB StatefulSet. Its named role is to prepare volume ownership/permissions, a setup task that plausibly requires root to change filesystem ownership; the root setting is tied to that helper function. :: helm/rocketchat.yaml
  SA-076 (K8S-143) SA_TOKEN_AUTOMOUNTED         TP -> FP reason=infra-need notes=Promtail is a Kubernetes log-collection agent and commonly queries the Kubernetes API for pod metadata and discovery. The protocol allows automount where the workload's function requires Kubernetes API access; the packet does not show an explicit automount disable. :: github/grafana_loki__operator__hack__addons_dev.yaml
  SA-086 (K8S-019) SA_TOKEN_AUTOMOUNTED         TP -> FP reason=infra-need notes=This is a kube-apiserver control-plane pod in kube-system. The API server is itself the Kubernetes control plane and has a legitimate need for API credentials/configuration; the protocol treats control-plane components as infrastructure exceptions where API access is required. :: github/kubescape_regolibrary__rules__ensure-that-the-API-Server-only-makes-use-of-Strong-Cryptographic-Ciphers-cis1-10__test__failed__input__1.yaml
  SA-091 (K8S-008) RBAC_WILDCARD_VERBS          FP -> TP reason= notes=The role grants wildcard verbs and resources in `custom.metrics.k8s.io`. The protocol's exception is limited to API groups owned by the same project; this is a Kubernetes aggregated metrics API group rather than an unambiguously project-owned API group in the evidence, so the conservative protocol reading is TP. :: github/kubernetes_examples__AI__vllm-deployment__hpa__prometheus-adapter.yaml

decided rows stand for 101 of the 340 retained sample rows (duplicate findings counted once in this audit).
