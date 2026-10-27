# Verification pass — divergence rows (92)

Worklist for the author's verification pass under protocol v3 + the 2026-10-27 addendum. `recommended_v3` is the label the governing protocol produces; blank `your_label` in the CSV accepts it, any entry overrides. Full row data: `results/verification_divergence.csv`.

## Class A — IMG_NO_DIGEST re-tier (v3 amendment 1) — 14 rows

- **K8S-009** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP-hardening** — image: nginx:1.16
  src: `github/MasayaAoyama_kubernetes-perfect-guide__samples__chapter09__sample-resource.yaml`
- **K8S-041** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP-hardening** — image: nginx:1.16
  src: `github/MasayaAoyama_kubernetes-perfect-guide__samples__chapter07__sample-secret-single-env.yaml`
- **K8S-066** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP-hardening** — image: index.docker.io/rancher/hardened-kubernetes:v1.32.11-rke2r1
  src: `github/kubescape_regolibrary__rules__ensure-that-the-api-server-request-timeout-argument-is-set-as-a`
- **K8S-080** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP** — image: nginx
  src: `github/kubescape_regolibrary__rules__workload-mounted-pvc__test__failed_pod_mounted__input__pod.yaml`
- **K8S-167** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP** — image: quay.io/argoproj/argocd:latest
  src: `github/argoproj_argo-cd__manifests__ha__install.yaml`
- **K8S-235** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP** — image: k8s.gcr.io/pause
  src: `github/fugue_regula__rego__tests__rules__k8s__seccomp_profile__inputs__valid_example.yaml`
- **K8S-244** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP** — image: nginx
  src: `github/kubescape_regolibrary__rules__rule-allow-privilege-escalation__test__cronjob-initcontainer__i`
- **K8S-253** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP** — image: test:latest
  src: `github/kubescape_regolibrary__rules__ingress-and-egress-blocked__test__cnp-specs-list-passed__input_`
- **K8S-259** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP-hardening** — image: docker.io/nats:2.9.17-alpine
  src: `helm/openebs.yaml`
- **K8S-330** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP** — image: quay.io/argoproj/argocd:latest
  src: `github/argoproj_argo-cd__manifests__ha__namespace-install-with-hydrator.yaml`
- **K8S-383** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP-hardening** — image: nginx:stable
  src: `github/tommy351_kosko__website__src__modules__home__components__DeployEverywhere__examples__results_`
- **K8S-396** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP-hardening** — image: busybox:1.28
  src: `github/argoproj_argo-cd__resource_customizations__batch__CronJob__testdata__never-succeeded.yaml`
- **K8S-449** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP** — image: redis
  src: `github/koki_short__testdata__replication_controllers__replication_controller_spec_with_pod_template.`
- **K8S-455** IMG_NO_DIGEST: v2 pre-label TP -> recommended **TP-hardening** — image: registry.k8s.io/sig-storage/csi-snapshotter:v8.6.0
  src: `helm/ceph-csi-cephfs.yaml`

## Class B — RES/REL production scoping (v3 amendment 2, addendum 12) — 42 rows

- **K8S-035** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__ensure-that-the-api-server-encryption-provider-config-argument-`
- **K8S-047** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__etcd-peer-auto-tls-disabled__test__pass-argument-not-set__input`
- **K8S-086** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__non-existent-service-account__test__success_empty_service_accou`
- **K8S-092** RES_NO_CPU_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__volumes__flexvolume__nginx-nfs.yaml`
- **K8S-100** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__volumes__rbd__rbd.yaml`
- **K8S-112** REL_NO_READINESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__exposed-sensitive-interfaces-v1__test__pod__input__pod.yaml`
- **K8S-122** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__etcd-auto-tls-disabled__test__pass-argument-not-set__input__etc`
- **K8S-138** RES_NO_CPU_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__etcd-unique-ca__test__rke2-args-fail__input__apiserverpod.yaml`
- **K8S-152** RES_NO_CPU_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__javaee__wildfly-rc.yaml`
- **K8S-153** REL_NO_READINESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__workload-mounted-secrets__test__success__input__pod.yaml`
- **K8S-154** REL_NO_LIVENESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__rule-credentials-in-env-var__test__deployment__input__deploymen`
- **K8S-163** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/MasayaAoyama_kubernetes-perfect-guide__samples__chapter05__sample-job.yaml`
- **K8S-177** REL_NO_LIVENESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/fugue_regula__rego__tests__rules__k8s__net_raw_capability__inputs__invalid_example.yaml`
- **K8S-183** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/argoproj_argo-cd__test__e2e__testdata__guestbook-with-namespace__guestbook-ui-deployment-ns.y`
- **K8S-195** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__linux-hardening__test__cronjob__input__cronjob.yaml`
- **K8S-212** REL_NO_LIVENESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__volumes__iscsi__iscsi-chap.yaml`
- **K8S-213** REL_NO_READINESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes-sigs_kustomize__examples__transformerconfigs__images__resources.yaml`
- **K8S-217** REL_NO_READINESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/MasayaAoyama_kubernetes-perfect-guide__samples__chapter07__sample-pvc-pod.yaml`
- **K8S-224** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__rule-privileged-container__test__cronjob-initcontainer__input__`
- **K8S-242** REL_NO_READINESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/fugue_regula__rego__tests__rules__k8s__privileged_containers__inputs__valid_example.yaml`
- **K8S-270** RES_NO_CPU_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__javaweb-tomcat-sidecar__javaweb-2.yaml`
- **K8S-277** RES_NO_CPU_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__rule-credentials-in-env-var__test__cronjob-initcontainer-env-ke`
- **K8S-282** REL_NO_LIVENESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__rule-credentials-in-env-var__test__deployment-env-with-filepath`
- **K8S-284** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__etcd-peer-auto-tls-disabled__test__pass-argument-not-set__input`
- **K8S-285** REL_NO_LIVENESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/MasayaAoyama_kubernetes-perfect-guide__samples__chapter14__kustomize__name-sample__sample-dep`
- **K8S-297** REL_NO_LIVENESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/argoproj_argo-rollouts__pkg__kubectl-argo-rollouts__info__testdata__blue-green__active-pod2.y`
- **K8S-309** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__image-not-pinned-to-digest__test__pod-sha256-uppercase__input__`
- **K8S-323** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__mismatching-selector__test__match_expressions__input__deploymen`
- **K8S-326** REL_NO_LIVENESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__exposure-to-internet__test__failed_with_ingress__input__deploym`
- **K8S-343** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__set-hostprocess-true__test__pod__input__pass.yaml`
- **K8S-344** REL_NO_READINESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/MasayaAoyama_kubernetes-perfect-guide__samples__chapter07__sample-pvc-dynamic-pod.yaml`
- **K8S-345** RES_NO_CPU_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__volumes__azure_disk__claim__blob-based-disk__account-specifie`
- **K8S-358** RES_NO_CPU_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__ensure-that-the-api-server-request-timeout-argument-is-set-as-a`
- **K8S-363** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/argoproj_argocd-example-apps__helm-hooks__manifests.yaml`
- **K8S-369** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__selenium__selenium-hub-deployment.yaml`
- **K8S-375** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/yannh_kubeconform__fixtures__duplicates-with-namespace.yaml`
- **K8S-422** REL_NO_READINESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/GoogleCloudPlatform_bank-of-anthos__src__accounts__accounts-db__k8s__overlays__development__a`
- **K8S-429** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__volumes__rbd__rbd.yaml`
- **K8S-439** REL_NO_LIVENESS_PROBE: v2 pre-label TP -> recommended **FP**
  src: `github/MasayaAoyama_kubernetes-perfect-guide__samples__chapter04__merge-sample__apply.yaml`
- **K8S-445** RES_NO_CPU_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/kubescape_regolibrary__rules__ensure-that-the-admission-control-plugin-SecurityContextDeny-is`
- **K8S-446** RES_NO_MEM_LIMIT: v2 pre-label TP -> recommended **FP**
  src: `github/argoproj_argo-cd__gitops-engine__pkg__diff__testdata__smd-deploy2-config.yaml`
- **K8S-457** RES_NO_REQUESTS: v2 pre-label TP -> recommended **FP**
  src: `github/kubernetes_examples___archived__volumes__nfs__nfs-busybox-deployment.yaml`

## Class C — escalation-path check (v3 amendment 3) — 29 rows

- **K8S-003** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/argoproj_argo-cd__applicationset__examples__applications-sync-policies__guestbook__engineerin`
- **K8S-028** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__rule-can-ssh-to-pod-v1__test__workloads__input__deployment.yaml`
- **K8S-065** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `helm/home-assistant.yaml`
- **K8S-095** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__ensure-that-the-admission-control-plugin-SecurityContextDeny-is`
- **K8S-104** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubernetes_examples___archived__javaweb-tomcat-sidecar__javaweb-2.yaml`
- **K8S-105** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/GoogleCloudPlatform_bank-of-anthos__extras__cloudsql__populate-jobs__populate-accounts-db.yam`
- **K8S-134** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `helm/ceph-csi-cephfs.yaml`
- **K8S-161** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `helm/nats.yaml`
- **K8S-165** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/Yolean_kubernetes-kafka__cruise-control__50cruise-control.yml`
- **K8S-171** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/isovalent_cilium-up-and-running__chapter03__unauthorized-client.yaml`
- **K8S-186** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/argoproj_argo-cd__test__e2e__testdata__crd-validation__deployment.yaml`
- **K8S-198** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/Yolean_kubernetes-kafka__events-kube__topic-create.yaml`
- **K8S-205** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__rule-credentials-in-env-var__test__cronjob__input__cronjob.yaml`
- **K8S-251** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `helm/jenkins.yaml`
- **K8S-258** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/valencenet_valence-manifests__valence.yaml`
- **K8S-275** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `helm/mariadb-operator.yaml`
- **K8S-303** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__resources-cpu-limits__test__pod__input__pod.yaml`
- **K8S-317** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/argoproj_argo-cd__test__e2e__testdata__hook-and-deployment__deployment.yaml`
- **K8S-318** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/argoproj_argocd-example-apps__sock-shop__base__rabbitmq-dep.yaml`
- **K8S-346** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__image-not-pinned-to-digest__test__pod-sha512-short__input__pod.`
- **K8S-362** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `helm/jenkins.yaml`
- **K8S-366** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `helm/ceph-csi-cephfs.yaml`
- **K8S-376** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubernetes_examples___archived__storage__hazelcast__hazelcast-deployment.yaml`
- **K8S-382** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__dangling-networkpolicy__test__success_matches_matchexpressions_`
- **K8S-390** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__CVE-2021-25741__test__workloads__input__deployment.yaml`
- **K8S-416** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__ingress-and-egress-blocked__test__mixed-np-cnp__input__pod.yaml`
- **K8S-420** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/kubescape_regolibrary__rules__exposed-sensitive-interfaces-v1__test__workloads__input__deploy`
- **K8S-438** SEC_ROOT_NOT_PREVENTED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/grafana_loki__operator__hack__addon_grafana_gateway_ocp.yaml`
- **K8S-456** SEC_APE_NOT_DISABLED: v2 pre-label TP -> recommended **TP** — runAsNonRoot=None, runAsUser=None, caps_add=[], readOnlyRootFS=None, allowPrivEsc=None
  src: `github/valencenet_valence-manifests__valence.yaml`

## Class D — evidence-absent (excluded, no judgment needed) — 7 rows

- **K8S-113** IMG_UNTAGGED: v2 pre-label unsure -> recommended **EXCLUDED**
  src: `github/argoproj_argo-cd__examples__known-hosts__argocd-known-hosts-mounts.yaml`
- **K8S-189** RBAC_CLUSTER_ADMIN_BINDING: v2 pre-label unsure -> recommended **EXCLUDED**
  src: `github/tektoncd_pipeline__examples__v1__pipelineruns__pipelinerun.yaml`
- **K8S-207** IMG_UNTAGGED: v2 pre-label unsure -> recommended **EXCLUDED**
  src: `github/argoproj_argo-cd__examples__known-hosts__argocd-known-hosts-mounts.yaml`
- **K8S-236** IMG_UNTAGGED: v2 pre-label unsure -> recommended **EXCLUDED**
  src: `github/Yolean_kubernetes-kafka__variants__scale-6-9__zoo-9.yaml`
- **K8S-341** SEC_ROOT_NOT_PREVENTED: v2 pre-label unsure -> recommended **EXCLUDED**
  src: `github/kubescape_regolibrary__rules__set-gmsacredentialspecname-value__test__workload__input__deploy`
- **K8S-371** IMG_UNTAGGED: v2 pre-label unsure -> recommended **EXCLUDED**
  src: `github/Yolean_kubernetes-kafka__variants__scale-6-9__zoo-9.yaml`
- **K8S-436** SA_TOKEN_AUTOMOUNTED: v2 pre-label unsure -> recommended **EXCLUDED**
  src: `helm/k10.yaml`

