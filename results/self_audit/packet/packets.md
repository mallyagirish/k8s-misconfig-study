# Evidence packets (same order as audit_sample.csv)

### SA-001 — HOST_NETWORK · helm
`tigera-operator.yaml` :: Job/tigera-operator-uninstall
- ns=default sa=tigera-operator host={'hostNetwork': True}
- container `cleanup-job` img=quay.io/tigera/operator:v1.44.0 sc={} res=null

### SA-002 — SECRET_LITERAL_ENV · github_example
`kubernetes_examples___archived__storage__mysql-galera__pxc-node2.yaml` :: ReplicationController/pxc-node2 :: container `pxc-node2`
- ns=None sa=None
- container `pxc-node2` img=capttofu/percona_xtradb_cluster_5_6:beta env=[{"name": "GALERA_CLUSTER", "value": "true"}, {"name": "WSREP_CLUSTER_ADDRESS", "value": "gcomm://"}, {"name": "WSREP_SST_USER", "value": "sst"}, {"name": "WSREP_SST_PASSWORD", "value": "sst"}, {"name": "MYSQL_USER", "value": "mysql"}, {"name": "MYSQL_PASSWORD", "value": "mysql"}, {"name": "MYSQL_ROOT_PASSWORD", "value": "c-krit"}]

### SA-003 — SEC_NO_SECCOMP · helm
`solr-operator.yaml` :: Deployment/pilot-zookeeper-operator :: container `pilot-zookeeper-operator`
- ns=default sa=zookeeper-operator ann={} pod_seccomp=None
- container `pilot-zookeeper-operator` img=pravega/zookeeper-operator:0.2.15 seccomp=None

### SA-004 — HOST_IPC · github_fixture
`kubescape_regolibrary__rules__host-pid-ipc-privileges__test__workload__input__deployment.yaml` :: Deployment/my-deployment
- ns=None sa=None host={'hostPID': True, 'hostIPC': True}
- container `mysql` img=mysql sc={} res=null
- container `php` img=php:7.0-apache sc={} res=null

### SA-005 — SEC_PRIVILEGED · github_fixture
`kubescape_regolibrary__rules__containers-mounting-docker-socket__test__workloads-crio__input__deployment.yaml` :: Deployment/my-deployment :: container `test-container2`
- ns=None sa=None
- container `test-container2` img=k8s.gcr.io/test-webserver priv=True

### SA-006 — SEC_CAPABILITY_ADDED · github_production
`kubernetes_ingress-nginx__deploy__static__provider__kind__deploy.yaml` :: Deployment/ingress-nginx-controller :: container `controller`
- ns=ingress-nginx sa=ingress-nginx
- container `controller` img=registry.k8s.io/ingress-nginx/controller:v1.15.1@sha256:594ceea76b01c592858f803f9ff4d2cb40542cae2060410b2c95f75907d659e1 caps={"add": ["NET_BIND_SERVICE"], "drop": ["ALL"]}

### SA-007 — IMG_UNTAGGED · helm
`gateway.yaml` :: Deployment/pilot :: container `istio-proxy`
- ns=default sa=pilot
- container `istio-proxy` img=auto

### SA-008 — SEC_RUN_AS_ROOT_EXPLICIT · github_fixture
`fugue_regula__rego__tests__rules__k8s__root_containers__inputs__valid_example.yaml` :: Pod/valid5 :: container `pause2`
- ns=None sa=None
- container `pause2` img=k8s.gcr.io/pause rnr=None user=0 pod_rnr=True pod_user=None

### SA-009 — HOST_NETWORK · github_fixture
`kubescape_regolibrary__rules__ensure-that-the-admission-control-plugin-SecurityContextDeny-is-set-if-PodSecurityPolicy-is-not-used__test__passed__input__1.yaml` :: Pod/kube-apiserver-minikube
- ns=kube-system sa=None host={'hostNetwork': True}
- container `kube-apiserver` img=k8s.gcr.io/kube-apiserver:v1.24.1 sc={} res={"requests": {"cpu": "250m"}}

### SA-010 — SEC_PRIVILEGED · github_fixture
`sigstore_k8s-manifest-sigstore__pkg__util__testdata__concatenated-manifest.yaml` :: Deployment/sample-deploy :: container `nginx`
- ns=None sa=None
- container `nginx` img=nginx:1.14.2 priv=True

### SA-011 — SEC_PRIVILEGED · github_fixture
`fugue_regula__rego__tests__rules__k8s__privileged_containers__inputs__invalid_example.yaml` :: Pod/privileged :: container `pause2`
- ns=None sa=None
- container `pause2` img=k8s.gcr.io/pause priv=True

### SA-012 — RES_NO_REQUESTS · helm
`victoria-metrics-k8s-stack.yaml` :: Job/pilot-victoria-metrics-k8s-stack-sync-job :: container `sync-job`
- ns=default sa=pilot-victoria-metrics-k8s-stack-sync-job
- container `sync-job` img=ghcr.io/victoriametrics/sync-job:v0.0.17 res=null

### SA-013 — RBAC_WILDCARD_RESOURCES · github_fixture
`kubescape_regolibrary__rules__rule-can-update-configmap-v1__test__clusterrole-clusterrolebinding__input__clusterrole.yaml` :: ClusterRole/test
- rules=[{"apiGroups": ["*"], "resources": ["pods/*", "*", "users"], "verbs": ["update"]}]

### SA-014 — RBAC_WILDCARD_VERBS · helm
`flux2.yaml` :: ClusterRole/crd-controller
- rules=[{"apiGroups": ["source.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["source.extensions.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["kustomize.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["helm.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["notification.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["image.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": [""], "resources": ["namespaces", "secrets", "configmaps", "serviceaccounts"], "verbs": ["get", "list", "watch"]}, {"apiGroups": [""], "resources": ["events"], "verbs": ["create", "patch"]}, {"apiGroups": [""], "resources": ["configmaps"], "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]}, {"apiGroups": [""], "resources": ["configmaps/status"], "verbs": ["get", "update", "patch"]}, {"apiGroups": ["coordination.k8s.io"], "resources": ["leases"], "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]}]

### SA-015 — RBAC_WILDCARD_RESOURCES · github_example
`sigstore_k8s-manifest-sigstore__example__admission-controller__config__rbac__role.yaml` :: ClusterRole/validator-role
- rules=[{"apiGroups": ["*"], "resources": ["*"], "verbs": ["*"]}]

### SA-016 — IMG_UNTAGGED · github_fixture
`kubescape_regolibrary__rules__containers-mounting-docker-socket__test__workloads-containerd__input__deployment.yaml` :: Deployment/my-deployment :: container `test-container2`
- ns=None sa=None
- container `test-container2` img=k8s.gcr.io/test-webserver

### SA-017 — SEC_DANGEROUS_CAPABILITY · github_fixture
`koki_short__testdata__pods__pod_spec_with_init_containers.rekube.yaml` :: Pod/meta_test :: container `container_name`
- ns=test sa=None
- container `container_name` img=container_image caps={"add": ["NET_ADMIN", "PID"], "drop": ["NET_ADMIN", "WALK"]}

### SA-018 — RES_NO_MEM_LIMIT · helm
`vault.yaml` :: Pod/pilot-vault-server-test :: container `pilot-server-test`
- ns=default sa=None
- container `pilot-server-test` img=hashicorp/vault:2.0.4 res=null

### SA-019 — DEPRECATED_API · github_fixture
`koki_short__testdata__pod_disruption_policy__pod_disruption_policy_requirements.yaml` :: PodDisruptionBudget/zk-pdb
- OBJECT NOT FOUND IN FILE (evidence-absent?)

### SA-020 — RES_NO_CPU_LIMIT · github_production
`argoproj_argo-cd__manifests__install.yaml` :: Deployment/argocd-redis :: container `secret-init`
- ns=None sa=argocd-redis
- container `secret-init` img=quay.io/argoproj/argocd:latest res=null

### SA-021 — SEC_NO_SECCOMP · github_fixture
`kubescape_regolibrary__rules__non-root-containers__test__deployment-fail__input__deployment.yaml` :: Deployment/nginx-deployment :: container `nginx`
- ns=None sa=None ann={} pod_seccomp=None
- container `nginx` img=nginx:1.14.2 seccomp=None

### SA-022 — HOST_IPC · github_production
`digitalocean_doks-debug__k8s__deployment.yaml` :: Deployment/doks-debug
- ns=kube-system sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `doks-debug` img=ghcr.io/digitalocean-packages/doks-debug:latest sc={"privileged": true} res={"requests": {"memory": "0", "cpu": "0"}, "limits": {"memory": "500Mi", "cpu": "500m"}}

### SA-023 — SEC_DANGEROUS_CAPABILITY · github_fixture
`fugue_regula__rego__tests__rules__k8s__added_capabilities__inputs__invalid_added_capabilities.yaml` :: Pod/security-context-demo-4 :: container `sec-ctx-4`
- ns=None sa=None
- container `sec-ctx-4` img=gcr.io/google-samples/node-hello:1.0 caps={"add": ["NET_ADMIN", "SYS_TIME"]}

### SA-024 — SECRET_LITERAL_ENV · github_fixture
`tektoncd_pipeline__test__git-resolver__gitea.yaml` :: StatefulSet/gitea :: container `configure-gitea`
- ns=None sa=None
- container `configure-gitea` img=mirror.gcr.io/gitea/gitea:1.25.4 env=[{"name": "GITEA_APP_INI", "value": "/data/gitea/conf/app.ini"}, {"name": "GITEA_CUSTOM", "value": "/data/gitea"}, {"name": "GITEA_WORK_DIR", "value": "/data"}, {"name": "GITEA_TEMP", "value": "/tmp/gitea"}, {"name": "GITEA_ADMIN_USERNAME", "value": "gitea_admin"}, {"name": "GITEA_ADMIN_PASSWORD", "value": "giteaPassword1234"}]

### SA-025 — HOST_PID · github_example
`kubernetes_examples___archived__newrelic__newrelic-daemonset.yaml` :: DaemonSet/newrelic-agent
- ns=None sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `newrelic` img=newrelic/nrsysmond sc={"privileged": true} res={"requests": {"cpu": 0.15}}

### SA-026 — SEC_PRIVILEGED · github_example
`kubernetes_examples___archived__newrelic-infrastructure__newrelic-infra-daemonset.yaml` :: DaemonSet/newrelic-infra-agent :: container `newrelic`
- ns=None sa=None
- container `newrelic` img=newrelic/infrastructure priv=True

### SA-027 — SEC_RUN_AS_ROOT_EXPLICIT · helm
`graylog.yaml` :: StatefulSet/opensearch-cluster-master :: container `fsgroup-volume`
- ns=None sa=None
- container `fsgroup-volume` img=busybox:latest rnr=None user=0 pod_rnr=None pod_user=1000

### SA-028 — REL_NO_LIVENESS_PROBE · helm
`rocketchat.yaml` :: Deployment/pilot-authorization :: container `authorization-service`
- ns=None sa=None
- container `authorization-service` img=rocketchat/authorization-service:8.6.1 probes=[]

### SA-029 — RBAC_WILDCARD_VERBS · github_fixture
`kubescape_regolibrary__rules__rule-can-create-pv__test__clusterrole-rolebinding__input__cluterrole.yaml` :: ClusterRole/test
- rules=[{"apiGroups": [""], "resources": ["pods", "services", "persistentvolumes"], "verbs": ["*", "watch", "list"]}]

### SA-030 — HOST_PID · github_production
`digitalocean_doks-debug__k8s__deployment.yaml` :: Deployment/doks-debug
- ns=kube-system sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `doks-debug` img=ghcr.io/digitalocean-packages/doks-debug:latest sc={"privileged": true} res={"requests": {"memory": "0", "cpu": "0"}, "limits": {"memory": "500Mi", "cpu": "500m"}}

### SA-031 — HOST_PID · helm
`prometheus.yaml` :: DaemonSet/pilot-prometheus-node-exporter
- ns=default sa=pilot-prometheus-node-exporter host={'hostNetwork': True, 'hostPID': True}
- container `node-exporter` img=quay.io/prometheus/node-exporter:v1.12.1 sc={"allowPrivilegeEscalation": false, "readOnlyRootFilesystem": true} res=null

### SA-032 — SEC_PRIVILEGED · helm
`zammad.yaml` :: Deployment/pilot-zammad-nginx :: container `zammad-volume-permissions`
- ns=default sa=None
- container `zammad-volume-permissions` img=alpine:3.24.2 priv=True

### SA-033 — REL_NO_READINESS_PROBE · github_production
`skyhook-io_radar__scripts__calico-demo__01-namespaces-workloads.yaml` :: StatefulSet/db :: container `nginx`
- ns=calico-demo sa=None
- container `nginx` img=nginx:alpine probes=[]

### SA-034 — RBAC_WILDCARD_VERBS · helm
`victoria-metrics-operator.yaml` :: ClusterRole/pilot-victoria-metrics-operator
- rules=[{"nonResourceURLs": ["/metrics", "/metrics/resources", "/metrics/slis"], "verbs": ["get", "watch", "list"]}, {"apiGroups": [""], "resources": ["configmaps", "configmaps/finalizers", "endpoints", "events", "persistentvolumeclaims", "persistentvolumeclaims/finalizers", "pods", "pods/eviction", "secrets", "secrets/finalizers", "services", "services/finalizers", "serviceaccounts", "serviceaccounts/finalizers"], "verbs": ["*"]}, {"apiGroups": [""], "resources": ["configmaps/status", "nodes", "nodes/metrics", "namespaces"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["apps"], "resources": ["daemonsets", "daemonsets/finalizers", "deployments", "deployments/finalizers", "replicasets", "statefulsets", "statefulsets/finalizers", "statefulsets/status"], "verbs": ["*"]}, {"apiGroups": ["monitoring.coreos.com"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["rbac.authorization.k8s.io"], "resources": ["clusterrolebindings", "clusterrolebindings/finalizers", "clusterroles", "clusterroles/finalizers", "roles", "rolebindings"], "verbs": ["*"]}, {"apiGroups": ["storage.k8s.io"], "resources": ["storageclasses"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["policy"], "resources": ["poddisruptionbudgets", "poddisruptionbudgets/finalizers"], "verbs": ["*"]}, {"apiGroups": ["route.openshift.io", "image.openshift.io"], "resources": ["routers/metrics", "registry/metrics"], "verbs": ["get"]}, {"apiGroups": ["autoscaling"], "verbs": ["*"], "resources": ["horizontalpodautoscalers"]}, {"apiGroups": ["networking.k8s.io"], "resources": ["ingresses", "ingresses/finalizers", "networkpolicies"], "verbs": ["*"]}, {"apiGroups": ["apiextensions.k8s.io"], "resources": ["customresourcedefinitions"], "verbs": ["get", "list"]}, {"apiGroups": ["discovery.k8s.io"], "resources": ["endpointslices"], "verbs": ["list", "watch", "get"]}, {"apiGroups": ["operator.victoriametrics.com"], "resources": ["vlagents", "vlagents/finalizers", "vlagents/status", "vlclusters", "vlclusters/finalizers", "vlclusters/status", "vldistributed", "vldistributed/finalizers", "vldistributed/status", "vlogs", "vlogs/finalizers", "vlogs/status", "vlsingles", "vlsingles/finalizers", "vlsingles/status", "vmagents", "vmagents/finalizers", "vmagents/status", "vmalertmanagerconfigs", "vmalertmanagerconfigs/finalizers", "vmalertmanagerconfigs/status", "vmalertmanagers", "vmalertmanagers/finalizers", "vmalertmanagers/status", "vmalerts", "vmalerts/finalizers", "vmalerts/status", "vmanomalies", "vmanomalies/finalizers", "vmanomalies/status", "vmanomalyconfigs", "vmanomalyconfigs/finalizers", "vmanomalyconfigs/status", "vmauths", "vmauths/finalizers", "vmauths/status", "vmclusters", "vmclusters/finalizers", "vmclusters/status", "vmdistributed", "vmdistributed/finalizers", "vmdistributed/status", "vmnodescrapes", "vmnodescrapes/finalizers", "vmnodescrapes/status", "vmpodscrapes", "vmpodscrapes/finalizers", "vmpodscrapes/status", "vmprobes", "vmprobes/finalizers", "vmprobes/status", "vmrules", "vmrules/finalizers", "vmrules/status", "vmscrapeconfigs", "vmscrapeconfigs/finalizers", "vmscrapeconfigs/status", "vmservicescrapes", "vmservicescrapes/finalizers", "vmservicescrapes/status", "vmsingles", "vmsingles/finalizers", "vmsingles/status", "vmstaticscrapes", "vmstaticscrapes/finalizers", "vmstaticscrapes/status", "vmusers", "vmusers/finalizers", "vmusers/status", "vtagents", "vtagents/finalizers", "vtagents/status", "vtclusters", "vtclusters/finalizers", "vtclusters/status", "vtsingles", "vtsingles/finalizers", "vtsingles/status"], "verbs": ["*"]}]

### SA-035 — SA_TOKEN_AUTOMOUNTED · github_example
`kubernetes_ingress-nginx__docs__examples__static-ip__nginx-ingress-controller.yaml` :: Deployment/ingress-nginx-controller
- ns=None sa=None pod_auto=None sa_auto=None
- container `controller` img=registry.k8s.io/ingress-nginx/controller:v1.0.5 sc={} res=null

### SA-036 — SEC_PRIVILEGED · helm
`redpanda.yaml` :: StatefulSet/pilot :: container `tuning`
- ns=default sa=pilot
- container `tuning` img=docker.redpanda.com/redpandadata/redpanda:v26.2.3 priv=True

### SA-037 — HOST_NETWORK · github_fixture
`kubescape_regolibrary__rules__set-seccomp-profile__test__cronjob__input__cronjob.yaml` :: CronJob/hello
- ns=None sa=None host={'hostNetwork': True}
- container `mysql` img=mysql sc={} res=null
- container `php` img=php:7.0-apache sc={} res=null

### SA-038 — SEC_PRIVILEGED · github_fixture
`kubescape_regolibrary__rules__rule-privileged-container__test__workloads-initcontainer__input__deployment.yaml` :: Deployment/priv-initcontainer-deploy :: container `setup`
- ns=default sa=None
- container `setup` img=busybox priv=True

### SA-039 — RBAC_CLUSTER_ADMIN_BINDING · github_fixture
`kubescape_regolibrary__rules__cluster-admin-role__test__clusterrole-rolebinding__input__rolebinding.yaml` :: RoleBinding/pod
- roleRef={'kind': 'ClusterRole', 'name': 'cluster-admin', 'apiGroup': 'rbac.authorization.k8s.io'} subjects=User:jane

### SA-040 — HOST_NETWORK · github_example
`MasayaAoyama_kubernetes-perfect-guide__samples__chapter05__sample-dnspolicy-clusterfirstwithhostnet.yaml` :: Pod/sample-dnspolicy-clusterfirstwithhostnet
- ns=None sa=None host={'hostNetwork': True}
- container `nginx-container` img=nginx:1.16 sc={} res=null

### SA-041 — SECRET_LITERAL_ENV · github_fixture
`kubescape_regolibrary__rules__set-procmount-default__test__cronjob__input__cronjob.yaml` :: CronJob/hello :: container `mysql`
- ns=None sa=None
- container `mysql` img=mysql env=[{"name": "MYSQL_ROOT_PASSWORD", "value": "rootpasswd"}]

### SA-042 — IMG_UNTAGGED · github_production
`kubernetes_ingress-nginx__deploy__prometheus__deployment.yaml` :: Deployment/prometheus-server :: container `prometheus`
- ns=None sa=prometheus-server
- container `prometheus` img=prom/prometheus

### SA-043 — RBAC_WILDCARD_RESOURCES · helm
`datadog.yaml` :: ClusterRole/pilot-datadog-orchestrator-explorer
- rules=[{"apiGroups": [""], "resources": ["namespaces"], "resourceNames": ["kube-system"], "verbs": ["get"]}, {"apiGroups": [""], "resources": ["configmaps"], "resourceNames": ["datadog-cluster-id"], "verbs": ["create", "get", "update"]}, {"apiGroups": [""], "resources": ["pods", "nodes", "namespaces", "limitranges", "services", "persistentvolumes", "persistentvolumeclaims", "serviceaccounts"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["discovery.k8s.io"], "resources": ["endpointslices"], "verbs": ["list", "watch"]}, {"apiGroups": ["autoscaling"], "resources": ["horizontalpodautoscalers"], "verbs": ["list", "watch"]}, {"apiGroups": ["apps"], "resources": ["deployments", "replicasets", "daemonsets", "statefulsets"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["batch"], "resources": ["cronjobs", "jobs"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["networking.k8s.io"], "resources": ["ingresses", "networkpolicies"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["rbac.authorization.k8s.io"], "resources": ["roles", "rolebindings", "clusterroles", "clusterrolebindings"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["storage.k8s.io"], "resources": ["storageclasses"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["autoscaling.k8s.io"], "resources": ["verticalpodautoscalers"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["apiextensions.k8s.io"], "resources": ["customresourcedefinitions"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["policy"], "resources": ["poddisruptionbudgets"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["datadoghq.com", "eks.amazonaws.com", "karpenter.azure.com", "karpenter.k8s.aws", "karpenter.sh"], "resources": ["*"], "verbs": ["list", "watch"]}, {"apiGroups": ["argoproj.io"], "resources": ["rollouts", "applications", "applicationsets"], "verbs": ["list", "watch", "get"]}, {"apiGroups": ["source.toolkit.fluxcd.io"], "resources": ["buckets", "helmcharts", "externalartifacts", "gitrepositories", "helmrepositories", "ocirepositories"], "verbs": ["list", "watch", "get"]}, {"apiGroups": ["kustomize.toolkit.fluxcd.io"], "resources": ["kustomizations"], "verbs": ["list", "watch", "get"]}, {"apiGroups": ["ray.io"], "resources": ["rayclusters", "raycronjobs", "rayjobs", "rayservices"], "verbs": ["list", "watch"]}, {"apiGroups": ["kubeai.org"], "resources": ["models"], "verbs": ["list", "watch"]}, {"apiGroups": ["nvidia.com"], "resources": ["dynamocheckpoints", "dynamocomponentdeployments", "dynamographdeploymentrequests", "dynamographdeployments", "dynamographdeploymentscalingadapters", "dynamomodels", "dynamoworkermetadatas"], "verbs": ["list", "watch"]}, {"apiGroups": ["serving.kserve.io"], "resources": ["clusterstoragecontainers", "llminferenceserviceconfigs", "llminferenceservices", "localmodelcaches", "localmodelnamespacecaches", "localmodelnodegroups", "localmodelnodes", "clusterservingruntimes", "inferencegraphs", "inferenceservices", "servingruntimes", "trainedmodels"], "verbs": ["list", "watch"]}, {"apiGroups": ["gateway.networking.k8s.io"], "resources": ["gatewayclasses", "gateways", "httproutes", "grpcroutes", "backendtlspolicies", "listenersets", "referencegrants", "tcproutes", "tlsroutes", "udproutes"], "verbs": ["list", "watch"]}, {"apiGroups": ["inference.networking.k8s.io"], "resources": ["inferencepools"], "verbs": ["list", "watch"]}, {"apiGroups": ["inference.networking.x-k8s.io"], "resources": ["inferencepools", "inferencepoolimports"], "verbs": ["list", "watch"]}]

### SA-044 — HOST_PID · github_fixture
`tektoncd_pipeline__test__testdata__spire__spire-agent.yaml` :: DaemonSet/spire-agent
- ns=spire sa=spire-agent host={'hostNetwork': True, 'hostPID': True}
- container `spire-agent` img=ghcr.io/spiffe/spire-agent:1.1.1 sc={} res=null
- container `spiffe-csi-driver` img=ghcr.io/spiffe/spiffe-csi-driver:nightly sc={"privileged": true} res=null
- container `node-driver-registrar` img=k8s.gcr.io/sig-storage/csi-node-driver-registrar:v2.0.1 sc={} res=null

### SA-045 — SEC_PRIVILEGED · github_fixture
`sigstore_k8s-manifest-sigstore__pkg__util__testdata__target-manifest.yaml` :: Deployment/sample-deploy-2 :: container `nginx`
- ns=None sa=None
- container `nginx` img=nginx:1.14.2 priv=True

### SA-046 — RBAC_CLUSTER_ADMIN_BINDING · helm
`k10.yaml` :: ClusterRoleBinding/kasten-cluster-admin
- roleRef={'kind': 'ClusterRole', 'name': 'cluster-admin', 'apiGroup': 'rbac.authorization.k8s.io'} subjects=ServiceAccount:controllermanager-svc,ServiceAccount:dashboardbff-svc,ServiceAccount:executor-svc,ServiceAccount:kanister-svc

### SA-047 — SECRET_COMMITTED · github_production
`argoproj_argo-cd__manifests__namespace-install-with-hydrator.yaml` :: Secret/argocd-secret
- secret type=Opaque values={}

### SA-048 — IMG_LATEST · helm
`kubeview.yaml` :: Deployment/pilot-kubeview :: container `kubeview`
- ns=None sa=pilot-kubeview
- container `kubeview` img=ghcr.io/benc-uk/kubeview:latest

### SA-049 — DEPRECATED_API · github_example
`argoproj_argo-cd__applicationset__examples__matrix__cluster-addons__argo-workflows__namespace-install.yaml` :: CustomResourceDefinition/workflows.argoproj.io
- OBJECT NOT FOUND IN FILE (evidence-absent?)

### SA-050 — REL_NO_READINESS_PROBE · github_production
`cloudfoundry_cf-for-k8s__config__eirini___ytt_lib__eirini__rendered.yml` :: Deployment/eirini-task-reporter :: container `task-reporter`
- ns=cf-system sa=eirini-task-reporter
- container `task-reporter` img=index.docker.io/eirini/task-reporter@sha256:c9cf7ebe1ff5190aafb1c58ee91e0da32a83eeaec34aec46cd13d32d30fea232 probes=[]

### SA-051 — DEPRECATED_API · helm
`consul.yaml` :: PodDisruptionBudget/pilot-consul-server
- rules=[{"apiGroups": [""], "resources": ["nodes"], "verbs": ["get"]}]

### SA-052 — SEC_CAPABILITY_ADDED · github_fixture
`fugue_regula__rego__tests__rules__k8s__capabilities_assigned__inputs__invalid_example.yaml` :: Pod/invalid2 :: container `hello`
- ns=None sa=None
- container `hello` img=gcr.io/google-samples/node-hello:1.0 caps={"add": ["NET_RAW"]}

### SA-053 — SEC_PRIVILEGED · github_production
`grafana_loki__operator__hack__addons_dev.yaml` :: DaemonSet/lokistack-dev-addons-promtail :: container `promtail`
- ns=None sa=lokistack-dev-addons-promtail
- container `promtail` img=docker.io/grafana/promtail:3.6 priv=True

### SA-054 — RBAC_CLUSTER_ADMIN_BINDING · github_fixture
`fluxcd_flux2__cmd__flux__testdata__create_tenant__tenant-with-service-account.yaml` :: RoleBinding/dev-team-reconciler
- roleRef={'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'ClusterRole', 'name': 'cluster-admin'} subjects=User:gotk:apps:reconciler,ServiceAccount:flux-tenant

### SA-055 — HOST_IPC · github_fixture
`kubescape_regolibrary__rules__host-ipc-privileges__test__cronjob__input__cronjob.yaml` :: CronJob/hello
- ns=None sa=None host={'hostIPC': True}
- container `mysql` img=mysql sc={} res=null
- container `php` img=php:7.0-apache sc={} res=null

### SA-056 — IMG_LATEST · github_fixture
`helmfile_helmfile__test__integration__test-cases__happypath__output__v3__httpbin__deployment.yaml` :: Deployment/httpbin-httpbin :: container `httpbin`
- ns=None sa=None
- container `httpbin` img=docker.io/citizenstig/httpbin:latest

### SA-057 — SEC_NO_SECCOMP · github_example
`GoogleCloudPlatform_bank-of-anthos__kubernetes-manifests__accounts-db.yaml` :: StatefulSet/accounts-db :: container `accounts-db`
- ns=None sa=default ann={} pod_seccomp=None
- container `accounts-db` img=us-central1-docker.pkg.dev/bank-of-anthos-ci/bank-of-anthos/accounts-db:v0.6.11@sha256:e86d6533bcd05bf9e4d7d495bf03b0a5ca571f526f3a419572b6df2c7913d588 seccomp=None

### SA-058 — IMG_UNTAGGED · github_example
`tektoncd_pipeline__docs__resolver-template__config__demo-resolver-deployment.yaml` :: Deployment/demoresolver :: container `controller`
- ns=tekton-pipelines-resolvers sa=tekton-pipelines-resolvers
- container `controller` img=ko://github.com/tektoncd/pipeline/docs/resolver-template/cmd/demoresolver

### SA-059 — SECRET_COMMITTED · github_fixture
`fluxcd_flux2__cmd__flux__testdata__create_secret__receiver__secret-receiver-gcr.yaml` :: Secret/gcr-secret
- secret type=None values={"audience": "https://flux.example.com/hook/6d6c55e9af\u2026", "email": "sa@project.iam.gserviceaccount.com", "token": "test-token"}

### SA-060 — SEC_RUN_AS_ROOT_EXPLICIT · helm
`zammad.yaml` :: Job/pilot-zammad-run-helm-test-rake-task :: container `zammad-volume-permissions`
- ns=None sa=None
- container `zammad-volume-permissions` img=alpine:3.24.2 rnr=False user=0 pod_rnr=True pod_user=1000

### SA-061 — SEC_PRIVILEGED · helm
`zammad.yaml` :: Job/pilot-zammad-run-helm-test-rake-task :: container `zammad-volume-permissions`
- ns=None sa=None
- container `zammad-volume-permissions` img=alpine:3.24.2 priv=True

### SA-062 — SEC_CAPABILITY_ADDED · helm
`k10.yaml` :: Deployment/catalog-svc :: container `upgrade-init`
- ns=default sa=catalog-svc
- container `upgrade-init` img=gcr.io/kasten-images/upgrade:9.0.8 caps={"add": ["FOWNER", "CHOWN"]}

### SA-063 — SECRET_COMMITTED · github_production
`grafana_loki__operator__hack__lokistack_gateway_dev.yaml` :: Secret/test-oidc
- secret type=None values={"clientID": "lokistack"}

### SA-064 — SECRET_COMMITTED · helm
`openfaas.yaml` :: Secret/basic-auth
- secret type=None values={"basic-auth-user": "admin", "basic-auth-password": "CZanNzN0FVLRrybQTdruEigs0yc29NFD"}

### SA-065 — HOST_IPC · github_example
`kubernetes_examples___archived__newrelic-infrastructure__newrelic-infra-daemonset.yaml` :: DaemonSet/newrelic-infra-agent
- ns=None sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `newrelic` img=newrelic/infrastructure sc={"privileged": true} res={"requests": {"cpu": 0.15}}

### SA-066 — RES_NO_CPU_LIMIT · helm
`jaeger.yaml` :: Deployment/pilot-jaeger :: container `jaeger`
- ns=None sa=pilot-jaeger
- container `jaeger` img=jaegertracing/jaeger:2.22.0 res=null

### SA-067 — RBAC_WILDCARD_RESOURCES · helm
`linkerd-viz.yaml` :: ClusterRole/linkerd-default-tap-admin
- rules=[{"apiGroups": [""], "resources": ["namespaces"], "verbs": ["list"]}, {"apiGroups": ["tap.linkerd.io"], "resources": ["*"], "verbs": ["watch"]}]

### SA-068 — IMG_LATEST · github_production
`grafana_loki__operator__config__overlays__openshift__size-calculator__logfile_metric_daemonset.yaml` :: DaemonSet/log-file-metric-exporter :: container `log-file-metric-exporter`
- ns=None sa=log-file-metric-exporter
- container `log-file-metric-exporter` img=quay.io/openshift-logging/log-file-metric-exporter:latest

### SA-069 — SEC_DANGEROUS_CAPABILITY · github_fixture
`kubescape_regolibrary__rules__drop-capability-netraw__test__pod__input__pod.yaml` :: Pod/audit-pod :: container `test-container`
- ns=None sa=None
- container `test-container` img=hashicorp/http-echo:0.2.3 caps={"add": ["NET_ADMIN", "SYS_TIME"], "drop": ["NET_RAW"]}

### SA-070 — SECRET_COMMITTED · github_example
`tektoncd_pipeline__examples__v1__pipelineruns__mapping-workspaces.yaml` :: Secret/secret-password
- secret type=Opaque values={"password": "hunter2"}

### SA-071 — RBAC_CLUSTER_ADMIN_BINDING · github_production
`WoozyMasta_kube-dump__deploy__cluster-role-admin.yaml` :: ClusterRoleBinding/kube-dump
- roleRef={'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'ClusterRole', 'name': 'cluster-admin'} subjects=ServiceAccount:kube-dump

### SA-072 — IMG_LATEST · github_production
`argoproj_argo-cd__manifests__install-with-hydrator.yaml` :: Deployment/argocd-server :: container `argocd-server`
- ns=None sa=argocd-server
- container `argocd-server` img=quay.io/argoproj/argocd:latest

### SA-073 — SEC_RUN_AS_ROOT_EXPLICIT · helm
`rocketchat.yaml` :: StatefulSet/pilot-mongodb :: container `volume-permissions`
- ns=default sa=pilot-mongodb
- container `volume-permissions` img=docker.io/bitnamilegacy/os-shell:11-debian-11-r72 rnr=None user=0 pod_rnr=None pod_user=None

### SA-074 — SA_TOKEN_AUTOMOUNTED · github_fixture
`kubescape_regolibrary__rules__resources-memory-limit-and-request__test__workload-mixed-unit__input__deployment.yaml` :: Deployment/huge
- ns=default sa=None pod_auto=None sa_auto=None
- container `c` img=nginx sc={} res={"requests": {"memory": "2048Mi"}, "limits": {"memory": "4096Mi"}}

### SA-075 — SECRET_LITERAL_ENV · helm
`eck-operator.yaml` :: StatefulSet/elastic-operator :: container `manager`
- ns=default sa=elastic-operator
- container `manager` img=docker.elastic.co/eck/eck-operator:3.5.0 env=[{"name": "WEBHOOK_SECRET", "value": "elastic-operator-webhook-cert"}]

### SA-076 — SA_TOKEN_AUTOMOUNTED · github_production
`grafana_loki__operator__hack__addons_dev.yaml` :: DaemonSet/lokistack-dev-addons-promtail
- ns=None sa=lokistack-dev-addons-promtail pod_auto=None sa_auto=None
- container `promtail` img=docker.io/grafana/promtail:3.6 sc={"privileged": true, "runAsNonRoot": false, "readOnlyRootFilesystem": true, "capabilities": {"drop": ["ALL"]}} res=null

### SA-077 — RES_NO_CPU_LIMIT · helm
`metallb.yaml` :: DaemonSet/pilot-frr-k8s :: container `reloader`
- ns=default sa=pilot-frr-k8s-controller
- container `reloader` img=quay.io/frrouting/frr:10.4.3 res=null

### SA-078 — RBAC_CLUSTER_ADMIN_BINDING · github_fixture
`kubescape_regolibrary__rules__cluster-admin-role__test__clusterrole-clusterrolebinding__input__clusterrolebinding.yaml` :: ClusterRoleBinding/read-secrets-global
- roleRef={'kind': 'ClusterRole', 'name': 'cluster-admin', 'apiGroup': 'rbac.authorization.k8s.io'} subjects=Group:manager,Group:dev

### SA-079 — RES_NO_MEM_LIMIT · github_production
`knative_docs__code-samples__eventing__bookstore-sample-app__solution__node-server__config__100-deployment.yaml` :: Deployment/node-server :: container `node-server`
- ns=None sa=None
- container `node-server` img=ghcr.io/knative/node-server:latest res=null

### SA-080 — HOST_PID · helm
`netdata.yaml` :: DaemonSet/netdata-child
- ns=default sa=netdata host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `netdata` img=netdata/netdata:v2.12.1 sc={"capabilities": {"add": ["SYS_PTRACE", "SYS_ADMIN"]}} res={}
- container `init-persistence` img=alpine:latest sc={} res={"requests": {"cpu": "10m"}}

### SA-081 — SEC_PRIVILEGED · github_example
`kubernetes_examples___archived__volumes__nfs__nfs-server-deployment.yaml` :: Deployment/nfs-server :: container `nfs-server`
- ns=None sa=None
- container `nfs-server` img=registry.k8s.io/volume-nfs:0.8 priv=True

### SA-082 — SECRET_LITERAL_ENV · github_production
`tektoncd_pipeline__config__webhook.yaml` :: Deployment/tekton-pipelines-webhook :: container `webhook`
- ns=tekton-pipelines sa=tekton-pipelines-webhook
- container `webhook` img=ko://github.com/tektoncd/pipeline/cmd/webhook env=[{"name": "KUBERNETES_MIN_VERSION", "value": "v1.28.0"}, {"name": "CONFIG_LOGGING_NAME", "value": "config-logging"}, {"name": "CONFIG_OBSERVABILITY_NAME", "value": "config-observability"}, {"name": "CONFIG_LEADERELECTION_NAME", "value": "config-leader-election-webhook"}, {"name": "CONFIG_FEATURE_FLAGS_NAME", "value": "feature-flags"}, {"name": "PROBES_PORT", "value": "8080"}, {"name": "WEBHOOK_PORT", "value": "8443"}, {"name": "WEBHOOK_ADMISSION_CONTROLLER_NAME", "value": "webhook.pipeline.tekton.dev"}, {"name": "WEBHOOK_SERVICE_NAME", "value": "tekton-pipelines-webhook"}, {"name": "WEBHOOK_SECRET_NAME", "value": "webhook-certs"}, {"name": "METRICS_DOMAIN", "value": "tekton.dev/pipeline"}]

### SA-083 — SEC_DANGEROUS_CAPABILITY · github_fixture
`kubescape_regolibrary__controls__examples__c046.yaml` :: Pod/security-context-demo-4 :: container `sec-ctx-4`
- ns=None sa=None
- container `sec-ctx-4` img=gcr.io/google-samples/node-hello:1.0 caps={"add": ["NET_ADMIN", "SYS_TIME"]}

### SA-084 — SEC_NO_SECCOMP · github_production
`argoproj_argo-workflows__manifests__quick-start-minimal.yaml` :: Deployment/minio :: container `main`
- ns=None sa=None ann={} pod_seccomp=None
- container `main` img=docker.io/pgsty/silo:RELEASE.2026-09-16T00-00-00Z@sha256:635197cb9f36d01bee221d34d1c7d7960f6a95c48b0b6c01d99cd13bdae51a46 seccomp=None

### SA-085 — HOST_IPC · github_fixture
`kubescape_regolibrary__controls__examples__c038.yaml` :: Pod/ubuntu
- ns=None sa=None host={'hostPID': True, 'hostIPC': True}
- container `ubuntu` img=ubuntu sc={} res=null

### SA-086 — SA_TOKEN_AUTOMOUNTED · github_fixture
`kubescape_regolibrary__rules__ensure-that-the-API-Server-only-makes-use-of-Strong-Cryptographic-Ciphers-cis1-10__test__failed__input__1.yaml` :: Pod/kube-apiserver-minikube
- ns=kube-system sa=None pod_auto=None sa_auto=None
- container `kube-apiserver` img=k8s.gcr.io/kube-apiserver:v1.24.1 sc={} res={"requests": {"cpu": "250m"}}

### SA-087 — REL_NO_READINESS_PROBE · helm
`openebs.yaml` :: Deployment/pilot-lvm-localpv-controller :: container `openebs-lvm-plugin`
- ns=None sa=openebs-lvm-controller-sa
- container `openebs-lvm-plugin` img=docker.io/openebs/lvm-driver:1.11.0-develop probes=[]

### SA-088 — HOST_NETWORK · github_fixture
`kubescape_regolibrary__rules__etcd-peer-auto-tls-disabled__test__pass-argument-set-to-false__input__etcdpod.yaml` :: Pod/kube-apiserver-minikube
- ns=kube-system sa=None host={'hostNetwork': True}
- container `etcd` img=k8s.gcr.io/etcd:3.5.1-0 sc={} res={"requests": {"cpu": "100m", "memory": "100Mi"}}

### SA-089 — SEC_PRIVILEGED · helm
`ceph-csi-rbd.yaml` :: DaemonSet/pilot-ceph-csi-rbd-nodeplugin :: container `liveness-prometheus`
- ns=default sa=pilot-ceph-csi-rbd-nodeplugin
- container `liveness-prometheus` img=quay.io/cephcsi/cephcsi:v3.18.1 priv=True

### SA-090 — SEC_CAPABILITY_ADDED · github_example
`argoproj_argocd-example-apps__sock-shop__base__user-db-dep.yaml` :: Deployment/user-db :: container `user-db`
- ns=None sa=None
- container `user-db` img=weaveworksdemos/user-db:0.3.0 caps={"drop": ["all"], "add": ["CHOWN", "SETGID", "SETUID"]}

### SA-091 — RBAC_WILDCARD_VERBS · github_example
`kubernetes_examples__AI__vllm-deployment__hpa__prometheus-adapter.yaml` :: ClusterRole/prometheus-adapter
- rules=[{"apiGroups": [""], "resources": ["nodes", "namespaces", "pods", "services"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["extensions"], "resources": ["deployments", "replicasets", "ingresses"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["apps"], "resources": ["deployments", "replicasets", "statefulsets"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["custom.metrics.k8s.io"], "resources": ["*"], "verbs": ["*"]}]

### SA-092 — RBAC_CLUSTER_ADMIN_BINDING · helm
`flux2.yaml` :: ClusterRoleBinding/cluster-reconciler
- roleRef={'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'ClusterRole', 'name': 'cluster-admin'} subjects=ServiceAccount:kustomize-controller,ServiceAccount:helm-controller

### SA-093 — SEC_PRIVILEGED · helm
`csi-driver-nfs.yaml` :: DaemonSet/csi-nfs-node :: container `nfs`
- ns=default sa=csi-nfs-node-sa
- container `nfs` img=registry.k8s.io/sig-storage/nfsplugin:v4.13.5 priv=True

### SA-094 — SEC_DANGEROUS_CAPABILITY · github_example
`MasayaAoyama_kubernetes-perfect-guide__samples__chapter13__sample-capabilities.yaml` :: Pod/sample-capabilities :: container `tools-container`
- ns=None sa=None
- container `tools-container` img=amsy810/tools:v2.0 caps={"add": ["SYS_ADMIN"], "drop": ["AUDIT_WRITE"]}

### SA-095 — SEC_CAPABILITY_ADDED · github_production
`kubernetes_ingress-nginx__deploy__static__provider__oracle__deploy.yaml` :: Deployment/ingress-nginx-controller :: container `controller`
- ns=ingress-nginx sa=ingress-nginx
- container `controller` img=registry.k8s.io/ingress-nginx/controller:v1.15.1@sha256:594ceea76b01c592858f803f9ff4d2cb40542cae2060410b2c95f75907d659e1 caps={"add": ["NET_BIND_SERVICE"], "drop": ["ALL"]}

### SA-096 — RES_NO_REQUESTS · github_production
`elastic_cloud-on-k8s__config__dev__registry.yaml` :: DaemonSet/kube-registry-proxy :: container `kube-registry-proxy`
- ns=kube-system sa=None
- container `kube-registry-proxy` img=gcr.io/google_containers/kube-registry-proxy:0.4 res={"limits": {"cpu": "100m", "memory": "50Mi"}}

### SA-097 — DEPRECATED_API · github_production
`valencenet_valence-manifests__tooling__kube-state-metrics__deployment.yaml` :: Deployment/kube-state-metrics
- ns=None sa=kube-state-metrics
- container `kube-state-metrics` img=gcr.io/google_containers/kube-state-metrics:v1.3.1 sc={} res={"requests": {"memory": "300Mi", "cpu": "100m"}, "limits": {"memory": "500Mi", "cpu": "200m"}}

### SA-098 — SEC_PRIVILEGED · github_fixture
`kubescape_regolibrary__rules__immutable-container-filesystem__test__pod-initcontainer__input__pod.yaml` :: Pod/test :: container `init-test2`
- ns=None sa=None
- container `init-test2` img=nginx priv=True

### SA-099 — DEPRECATED_API · github_example
`helm_charts__stable__velero__crds__schedules.yaml` :: CustomResourceDefinition/schedules.velero.io
- OBJECT NOT FOUND IN FILE (evidence-absent?)

### SA-100 — REL_NO_LIVENESS_PROBE · github_fixture
`kubescape_regolibrary__rules__ensure-that-the-api-server-etcd-cafile-argument-is-set-as-appropriate__test__rke2-args__input__1.yaml` :: Pod/kube-apiserver-rke2-server :: container `kube-apiserver`
- ns=kube-system sa=None
- container `kube-apiserver` img=index.docker.io/rancher/hardened-kubernetes:v1.32.11-rke2r1 probes=[]
