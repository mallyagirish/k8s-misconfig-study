# Self-audit adjudication sheet — 16 changed rows

For each row: the original retained label, your blind audit label and your audit note. Fill `final_label` in adjudication.csv (TP / FP / TP-hardening) with the label the reference dataset should carry; add a short note if the decision was not obvious.

## SA-001 (K8S-392) — HOST_NETWORK [helm]

- Original label: **FP** → Audit label: **TP**
- Source: helm/tigera-operator.yaml — Job tigera-operator-uninstall
- Your audit note: The uninstall Job is explicitly configured with host networking. The packet identifies a Tigera operator cleanup task, but it does not show that host networking is required for this cleanup operation. Under the rule, the property is present and no supported infrastructure-necessity exception is established.

## SA-007 (K8S-364) — IMG_UNTAGGED [helm]

- Original label: **FP** → Audit label: **TP**
- Source: helm/gateway.yaml — Deployment pilot
- Your audit note: The rendered image value is `auto`, with no explicit tag or digest visible in the packet. Under the image rule, an image with no tag is a misconfiguration; the packet does not establish that this value is merely an unresolved template.

## SA-012 (K8S-314) — RES_NO_REQUESTS [helm]

- Original label: **TP** → Audit label: **FP** (reason: fixture)
- Source: helm/victoria-metrics-k8s-stack.yaml — Job pilot-victoria-metrics-k8s-stack-sync-job
- Your audit note: This is a one-shot Job. The protocol expressly classifies RES_* findings on Jobs as false positives for this study's production-scoped resource rules, regardless of whether requests are absent.

## SA-024 (K8S-335) — SECRET_LITERAL_ENV [github]

- Original label: **TP** → Audit label: **FP** (reason: fixture)
- Source: github/tektoncd_pipeline__test__git-resolver__gitea.yaml — StatefulSet gitea
- Your audit note: The literal `giteaPassword1234` appears in a Tekton pipeline test fixture used to configure a test Gitea instance. In this test-path context, it is test credential material rather than evidence of a production secret committed in a deployment configuration.

## SA-027 (K8S-325) — SEC_RUN_AS_ROOT_EXPLICIT [helm]

- Original label: **TP** → Audit label: **FP** (reason: infra-need)
- Source: helm/graylog.yaml — StatefulSet opensearch-cluster-master
- Your audit note: The container is named `fsgroup-volume` and runs as UID 0 while the pod-level user is 1000. This is a volume-permissions helper whose function is to adjust filesystem ownership; root is plausibly required for that operation, so the root setting is tied to the helper's infrastructure setup task.

## SA-035 (K8S-033) — SA_TOKEN_AUTOMOUNTED [github]

- Original label: **TP** → Audit label: **FP** (reason: infra-need)
- Source: github/kubernetes_ingress-nginx__docs__examples__static-ip__nginx-ingress-controller.yaml — Deployment ingress-nginx-controller
- Your audit note: This is the ingress-nginx controller. Controllers commonly need Kubernetes API access to watch Ingresses, Services, Secrets, and related resources; the protocol explicitly treats controllers requiring API access as infrastructure-need exceptions. The packet shows inherited/default automount settings rather than an explicit disable.

## SA-039 (K8S-296) — RBAC_CLUSTER_ADMIN_BINDING [github]

- Original label: **FP** → Audit label: **TP**
- Source: github/kubescape_regolibrary__rules__cluster-admin-role__test__clusterrole-rolebinding__input__rolebinding.yaml — RoleBinding pod
- Your audit note: The RoleBinding references the cluster-admin ClusterRole and binds it to a named user. That is a direct cluster-admin grant; the test-fixture path does not negate the privilege represented by the binding under this rule.

## SA-041 (K8S-039) — SECRET_LITERAL_ENV [github]

- Original label: **TP** → Audit label: **FP** (reason: fixture)
- Source: github/kubescape_regolibrary__rules__set-procmount-default__test__cronjob__input__cronjob.yaml — CronJob hello
- Your audit note: The literal MYSQL_ROOT_PASSWORD value appears in a Kubescape rule-test CronJob fixture. It is a canned test value in a test input, not a credential demonstrated to be used by a production workload.

## SA-043 (K8S-428) — RBAC_WILDCARD_RESOURCES [helm]

- Original label: **FP** → Audit label: **TP**
- Source: helm/datadog.yaml — ClusterRole pilot-datadog-orchestrator-explorer
- Your audit note: The role grants wildcard resources for several API groups, including groups not owned by Datadog (for example EKS and Karpenter groups). The protocol's exception requires every wildcard grant to be confined to the same project's own API groups; that condition is not met.

## SA-052 (K8S-245) — SEC_CAPABILITY_ADDED [github]

- Original label: **TP** → Audit label: **FP** (reason: standard-practice)
- Source: github/fugue_regula__rego__tests__rules__k8s__capabilities_assigned__inputs__invalid_example.yaml — Pod invalid2
- Your audit note: The only added capability is NET_RAW, which is part of the conventional default Linux container capability set. The protocol excludes additions limited to default-set capabilities from this rule, so this is not a qualifying added-capability misconfiguration.

## SA-053 (K8S-379) — SEC_PRIVILEGED [github]

- Original label: **TP** → Audit label: **FP** (reason: infra-need)
- Source: github/grafana_loki__operator__hack__addons_dev.yaml — DaemonSet lokistack-dev-addons-promtail
- Your audit note: Promtail is a node-level log-collection DaemonSet component in the Loki operator's development add-ons. Log collectors require host-level access to read node/container logs; the protocol's node-agent infrastructure exception is the closest applicable classification.

## SA-054 (K8S-226) — RBAC_CLUSTER_ADMIN_BINDING [github]

- Original label: **FP** → Audit label: **TP**
- Source: github/fluxcd_flux2__cmd__flux__testdata__create_tenant__tenant-with-service-account.yaml — RoleBinding dev-team-reconciler
- Your audit note: The RoleBinding references cluster-admin and binds it to a user and a service account. The fact that the file is under testdata does not remove the actual cluster-admin binding, and the protocol does not exempt this rule for fixtures.

## SA-073 (K8S-286) — SEC_RUN_AS_ROOT_EXPLICIT [helm]

- Original label: **TP** → Audit label: **FP** (reason: infra-need)
- Source: helm/rocketchat.yaml — StatefulSet pilot-mongodb
- Your audit note: The `volume-permissions` container runs as UID 0 as part of a MongoDB StatefulSet. Its named role is to prepare volume ownership/permissions, a setup task that plausibly requires root to change filesystem ownership; the root setting is tied to that helper function.

## SA-076 (K8S-143) — SA_TOKEN_AUTOMOUNTED [github]

- Original label: **TP** → Audit label: **FP** (reason: infra-need)
- Source: github/grafana_loki__operator__hack__addons_dev.yaml — DaemonSet lokistack-dev-addons-promtail
- Your audit note: Promtail is a Kubernetes log-collection agent and commonly queries the Kubernetes API for pod metadata and discovery. The protocol allows automount where the workload's function requires Kubernetes API access; the packet does not show an explicit automount disable.

## SA-086 (K8S-019) — SA_TOKEN_AUTOMOUNTED [github]

- Original label: **TP** → Audit label: **FP** (reason: infra-need)
- Source: github/kubescape_regolibrary__rules__ensure-that-the-API-Server-only-makes-use-of-Strong-Cryptographic-Ciphers-cis1-10__test__failed__input__1.yaml — Pod kube-apiserver-minikube
- Your audit note: This is a kube-apiserver control-plane pod in kube-system. The API server is itself the Kubernetes control plane and has a legitimate need for API credentials/configuration; the protocol treats control-plane components as infrastructure exceptions where API access is required.

## SA-091 (K8S-008) — RBAC_WILDCARD_VERBS [github]

- Original label: **FP** → Audit label: **TP**
- Source: github/kubernetes_examples__AI__vllm-deployment__hpa__prometheus-adapter.yaml — ClusterRole prometheus-adapter
- Your audit note: The role grants wildcard verbs and resources in `custom.metrics.k8s.io`. The protocol's exception is limited to API groups owned by the same project; this is a Kubernetes aggregated metrics API group rather than an unambiguously project-owned API group in the evidence, so the conservative protocol reading is TP.

