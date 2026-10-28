# Evidence packets (same order as blind_sample.csv)

### R2-A001 — REL_NO_READINESS_PROBE · github_production
`cloudfoundry_cf-for-k8s__config__eirini___ytt_lib__eirini__rendered.yml` :: Deployment/eirini-task-reporter :: container `task-reporter`
- ns=cf-system sa=eirini-task-reporter
- container `task-reporter` img=index.docker.io/eirini/task-reporter@sha256:c9cf7ebe1ff5190aafb1c58ee91e0da32a83eeaec34aec46cd13d32d30fea232 probes=[]

### R2-A002 — SECRET_COMMITTED · helm
`harbor.yaml` :: Secret/pilot-harbor-trivy
- secret type=Opaque values={"redisURL": "redis://pilot-harbor-redis:6379/5?idle_t\u2026", "gitHubToken": ""}

### R2-A003 — SECRET_LITERAL_ENV · github_production
`argoproj_argo-workflows__manifests__components__mysql__mysql-deployment.yaml` :: Deployment/mysql :: container `main`
- ns=None sa=None
- container `main` img=quay.io/fedora/mysql-80@sha256:4f242c1ea0b77df36293784ed26acc12a1e048457fe6c4037bd5d49a0ec4d186 env=[{"name": "MYSQL_USER", "value": "mysql"}, {"name": "MYSQL_PASSWORD", "value": "password"}, {"name": "MYSQL_DATABASE", "value": "argo"}, {"name": "MYSQL_RANDOM_ROOT_PASSWORD", "value": "yes"}]

### R2-A004 — RBAC_CLUSTER_ADMIN_BINDING · helm
`portainer.yaml` :: ClusterRoleBinding/pilot-portainer
- roleRef={'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'ClusterRole', 'name': 'cluster-admin'} subjects=ServiceAccount:portainer-sa-clusteradmin

### R2-A005 — RES_NO_MEM_LIMIT · helm
`datadog.yaml` :: Deployment/pilot-datadog-cluster-agent :: container `init-volume`
- ns=default sa=pilot-datadog-cluster-agent
- container `init-volume` img=registry.datadoghq.com/cluster-agent:7.84.3 res=null

### R2-A006 — RES_NO_CPU_LIMIT · github_example
`kubernetes_examples___archived__volumes__azure_disk__claim__blob-based-disk__account-specified-hdd__pod-uses-account-hdd.yaml` :: Pod/pod-uses-account-hdd-5g :: container `az-c-01`
- ns=None sa=None
- container `az-c-01` img=nginx res=null

### R2-A007 — RES_NO_CPU_LIMIT · github_production
`argoproj_argo-workflows__manifests__quick-start__base__prometheus__prometheus-deployment.yaml` :: Deployment/prometheus :: container `prometheus`
- ns=None sa=None
- container `prometheus` img=quay.io/prometheus/prometheus:v3.2.1@sha256:6927e0919a144aa7616fd0137d4816816d42f6b816de3af269ab065250859a62 res=null

### R2-A008 — IMG_UNTAGGED · helm
`gateway.yaml` :: Deployment/pilot :: container `istio-proxy`
- ns=default sa=pilot
- container `istio-proxy` img=auto

### R2-A009 — SA_TOKEN_AUTOMOUNTED · github_example
`kubernetes_ingress-nginx__docs__examples__static-ip__nginx-ingress-controller.yaml` :: Deployment/ingress-nginx-controller
- ns=None sa=None pod_auto=None sa_auto=None
- container `controller` img=registry.k8s.io/ingress-nginx/controller:v1.0.5 sc={} res=null

### R2-A010 — SEC_DANGEROUS_CAPABILITY · github_production
`SuchanMadhikarmi_kubernetes-zero-to-production__manifests__13-troubleshooting__debug-pod.yaml` :: Pod/debug-tool :: container `debug`
- ns=default sa=None
- container `debug` img=nicolaka/netshoot:ubuntu caps={"add": ["NET_ADMIN", "NET_RAW", "SYS_ADMIN"]}

### R2-A011 — IMG_LATEST · github_example
`kubernetes_ingress-nginx__docs__examples__auth__oauth-external-auth__oauth2-proxy.yaml` :: Deployment/oauth2-proxy :: container `oauth2-proxy`
- ns=kube-system sa=None
- container `oauth2-proxy` img=quay.io/oauth2-proxy/oauth2-proxy:latest

### R2-A012 — SECRET_LITERAL_ENV · github_fixture
`tektoncd_pipeline__test__git-resolver__gitea.yaml` :: StatefulSet/gitea :: container `configure-gitea`
- ns=None sa=None
- container `configure-gitea` img=mirror.gcr.io/gitea/gitea:1.25.4 env=[{"name": "GITEA_APP_INI", "value": "/data/gitea/conf/app.ini"}, {"name": "GITEA_CUSTOM", "value": "/data/gitea"}, {"name": "GITEA_WORK_DIR", "value": "/data"}, {"name": "GITEA_TEMP", "value": "/tmp/gitea"}, {"name": "GITEA_ADMIN_USERNAME", "value": "gitea_admin"}, {"name": "GITEA_ADMIN_PASSWORD", "value": "giteaPassword1234"}]

### R2-A013 — DEPRECATED_API · github_example
`helm_charts__stable__velero__crds__podvolumebackups.yaml` :: CustomResourceDefinition/podvolumebackups.velero.io
- OBJECT NOT FOUND IN FILE (evidence-absent?)

### R2-A014 — SEC_APE_NOT_DISABLED · github_example
`GoogleCloudPlatform_bank-of-anthos__extras__cloudsql__populate-jobs__populate-accounts-db.yaml` :: Job/populate-accounts-db :: container `sidecar-controller`
- ns=None sa=boa-ksa
- container `sidecar-controller` img=bash@sha256:38697a8e277c4b61f75193f003db16590eda7b096577dd1c2be53afa207954e7 ape=None pod_ape=None

### R2-A015 — SEC_RUN_AS_ROOT_EXPLICIT · helm
`rocketchat.yaml` :: StatefulSet/pilot-mongodb :: container `volume-permissions`
- ns=default sa=pilot-mongodb
- container `volume-permissions` img=docker.io/bitnamilegacy/os-shell:11-debian-11-r72 rnr=None user=0 pod_rnr=None pod_user=None

### R2-A016 — SEC_APE_NOT_DISABLED · github_fixture
`kubescape_regolibrary__rules__dangling-networkpolicy__test__success_matches_matchexpressions_notin__input__pod.yaml` :: Pod/staging-pod :: container `app`
- ns=default sa=None
- container `app` img=nginx:latest ape=None pod_ape=None

### R2-A017 — SECRET_COMMITTED · github_production
`grafana_loki__operator__hack__lokistack_gateway_dev.yaml` :: Secret/test-oidc
- secret type=None values={"clientID": "lokistack"}

### R2-A018 — SEC_PRIVILEGED · github_fixture
`koki_short__testdata__pods__pod_status_with_conditions.rekube.yaml` :: Pod/meta_test :: container `container_name`
- ns=test sa=None
- container `container_name` img=container_image priv=True

### R2-A019 — RBAC_CLUSTER_ADMIN_BINDING · github_production
`WoozyMasta_kube-dump__deploy__cluster-role-admin.yaml` :: ClusterRoleBinding/kube-dump
- roleRef={'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'ClusterRole', 'name': 'cluster-admin'} subjects=ServiceAccount:kube-dump

### R2-A020 — SEC_APE_NOT_DISABLED · helm
`home-assistant.yaml` :: Pod/pilot-home-assistant-test-connection :: container `wget`
- ns=default sa=None
- container `wget` img=busybox ape=None pod_ape=None

### R2-A021 — RES_NO_REQUESTS · github_fixture
`yannh_kubeconform__fixtures__duplicates-with-namespace.yaml` :: ReplicationController/bob :: container `nginx`
- ns=x sa=None
- container `nginx` img=nginx res=null

### R2-A022 — SEC_RUN_AS_ROOT_EXPLICIT · helm
`opensearch.yaml` :: StatefulSet/opensearch-cluster-master :: container `fsgroup-volume`
- ns=None sa=None
- container `fsgroup-volume` img=busybox:latest rnr=None user=0 pod_rnr=None pod_user=1000

### R2-A023 — SA_TOKEN_AUTOMOUNTED · github_fixture
`kubescape_regolibrary__rules__ensure-that-the-API-Server-only-makes-use-of-Strong-Cryptographic-Ciphers-cis1-10__test__failed__input__1.yaml` :: Pod/kube-apiserver-minikube
- ns=kube-system sa=None pod_auto=None sa_auto=None
- container `kube-apiserver` img=k8s.gcr.io/kube-apiserver:v1.24.1 sc={} res={"requests": {"cpu": "250m"}}

### R2-A024 — HOST_IPC · helm
`netdata.yaml` :: DaemonSet/netdata-child
- ns=default sa=netdata host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `netdata` img=netdata/netdata:v2.12.1 sc={"capabilities": {"add": ["SYS_PTRACE", "SYS_ADMIN"]}} res={}
- container `init-persistence` img=alpine:latest sc={} res={"requests": {"cpu": "10m"}}

### R2-A025 — SEC_PRIVILEGED · helm
`openebs.yaml` :: DaemonSet/pilot-lvm-localpv-node :: container `openebs-lvm-plugin`
- ns=None sa=openebs-lvm-node-sa
- container `openebs-lvm-plugin` img=docker.io/openebs/lvm-driver:1.11.0-develop priv=True

### R2-A026 — RBAC_WILDCARD_RESOURCES · helm
`crossplane.yaml` :: ClusterRole/crossplane:aggregate-to-edit
- rules=[{"apiGroups": ["", "events.k8s.io"], "resources": ["events"], "verbs": ["get", "list", "watch"]}, {"apiGroups": [""], "resources": ["secrets"], "verbs": ["*"]}, {"apiGroups": [""], "resources": ["namespaces"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["apiextensions.crossplane.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["pkg.crossplane.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["secrets.crossplane.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["protection.crossplane.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["ops.crossplane.io"], "resources": ["*"], "verbs": ["*"]}]

### R2-A027 — SEC_DANGEROUS_CAPABILITY · github_fixture
`kubescape_regolibrary__controls__examples__c046.yaml` :: Pod/security-context-demo-4 :: container `sec-ctx-4`
- ns=None sa=None
- container `sec-ctx-4` img=gcr.io/google-samples/node-hello:1.0 caps={"add": ["NET_ADMIN", "SYS_TIME"]}

### R2-A028 — RES_NO_REQUESTS · github_fixture
`argoproj_argo-cd__test__e2e__testdata__guestbook-with-namespace__guestbook-ui-deployment-ns.yaml` :: Deployment/guestbook-ui :: container `guestbook-ui`
- ns=namespace sa=None
- container `guestbook-ui` img=quay.io/argoprojlabs/argocd-e2e-container:0.1 res=null

### R2-A029 — HOST_NETWORK · github_example
`MasayaAoyama_kubernetes-perfect-guide__samples__chapter05__sample-dnspolicy-clusterfirstwithhostnet.yaml` :: Pod/sample-dnspolicy-clusterfirstwithhostnet
- ns=None sa=None host={'hostNetwork': True}
- container `nginx-container` img=nginx:1.16 sc={} res=null

### R2-A030 — RES_NO_CPU_LIMIT · helm
`redpanda.yaml` :: Job/pilot-configuration :: container `post-install`
- ns=default sa=pilot
- container `post-install` img=docker.redpanda.com/redpandadata/redpanda-operator:v26.2.4 res={}

### R2-A031 — HOST_PID · github_fixture
`koki_short__testdata__pods__pod_spec_with_host_pid.yaml` :: Pod/meta_test
- ns=test sa=None host={'hostPID': True}

### R2-A032 — REL_NO_READINESS_PROBE · github_production
`skyhook-io_radar__scripts__calico-demo__01-namespaces-workloads.yaml` :: StatefulSet/db :: container `nginx`
- ns=calico-demo sa=None
- container `nginx` img=nginx:alpine probes=[]

### R2-A033 — SEC_ROOT_NOT_PREVENTED · github_fixture
`kubescape_regolibrary__rules__ingress-and-egress-blocked__test__mixed-np-cnp__input__pod.yaml` :: Pod/test :: container `test`
- ns=my-ns sa=None
- container `test` img=test:latest rnr=None user=None pod_rnr=None pod_user=None

### R2-A034 — HOST_NETWORK · github_production
`SuchanMadhikarmi_kubernetes-zero-to-production__manifests__03-workloads__daemonset.yaml` :: DaemonSet/node-exporter
- ns=monitoring sa=None host={'hostNetwork': True}
- container `node-exporter` img=prom/node-exporter:latest sc={} res=null

### R2-A035 — RES_NO_CPU_LIMIT · github_example
`kubernetes_examples___archived__javaee__wildfly-rc.yaml` :: ReplicationController/wildfly-rc :: container `wildfly-rc-pod`
- ns=None sa=None
- container `wildfly-rc-pod` img=arungupta/wildfly-mysql-javaee7:k8s res=null

### R2-A036 — SEC_NO_SECCOMP · github_example
`MasayaAoyama_kubernetes-perfect-guide__samples__chapter14__kustomize__commonmeta-sample__sample-deployment.yaml` :: Deployment/sample-deployment :: container `nginx-container`
- ns=None sa=None ann={} pod_seccomp=None
- container `nginx-container` img=nginx:1.16 seccomp=None

### R2-A037 — IMG_NO_DIGEST · github_fixture
`argoproj_argo-cd__resource_customizations__batch__CronJob__testdata__never-succeeded.yaml` :: CronJob/hello :: container `hello`
- ns=test-cronjob sa=None
- container `hello` img=busybox:1.28

### R2-A038 — SEC_PRIVILEGED · github_example
`kubernetes_examples___archived__volumes__nfs__nfs-server-deployment.yaml` :: Deployment/nfs-server :: container `nfs-server`
- ns=None sa=None
- container `nfs-server` img=registry.k8s.io/volume-nfs:0.8 priv=True

### R2-A039 — IMG_LATEST · github_production
`argoproj_argo-workflows__manifests__base__workflow-controller__workflow-controller-deployment.yaml` :: Deployment/workflow-controller :: container `workflow-controller`
- ns=None sa=argo
- container `workflow-controller` img=quay.io/argoproj/workflow-controller:latest

### R2-A040 — SEC_PRIVILEGED · helm
`openebs.yaml` :: DaemonSet/pilot-csi-node :: container `csi-node`
- ns=default sa=pilot-service-account
- container `csi-node` img=docker.io/openebs/mayastor-csi-node:develop priv=True

### R2-A041 — SECRET_LITERAL_ENV · github_example
`kubernetes_ingress-nginx__docs__examples__auth__oauth-external-auth__vouch-proxy.yaml` :: Deployment/vouch-proxy :: container `vouch-proxy`
- ns=kube-system sa=None
- container `vouch-proxy` img=quay.io/vouch/vouch-proxy:latest env=[{"name": "VOUCH_ALLOWALLUSERS", "value": "True"}, {"name": "VOUCH_COOKIE_DOMAIN", "value": "<Ingress Host>"}, {"name": "VOUCH_LISTEN", "value": "0.0.0.0"}, {"name": "VOUCH_DOCUMENT_ROOT", "value": "oauth2"}, {"name": "OAUTH_PROVIDER", "value": "github"}, {"name": "OAUTH_CLIENT_ID", "value": "<Client ID>"}, {"name": "OAUTH_CLIENT_SECRET", "value": "<Client Secret>"}]

### R2-A042 — HOST_IPC · github_production
`digitalocean_doks-debug__k8s__daemonset.yaml` :: DaemonSet/doks-debug
- ns=kube-system sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `doks-debug` img=ghcr.io/digitalocean-packages/doks-debug:latest sc={"privileged": true} res={"requests": {"memory": "0", "cpu": "0"}, "limits": {"memory": "500Mi", "cpu": "500m"}}

### R2-A043 — HOST_PID · github_fixture
`sigstore_k8s-manifest-sigstore__pkg__util__testdata__concatenated-manifest.yaml` :: Deployment/sample-deploy
- ns=None sa=None host={'hostPID': True}
- container `nginx` img=nginx:1.14.2 sc={"privileged": true} res=null

### R2-A044 — SECRET_COMMITTED · github_fixture
`elastic_cloud-on-k8s__hack__upgrade-test-harness__testdata__v2140__install.yaml` :: Secret/elastic-webhook-server-cert
- secret type=None values={}

### R2-A045 — SECRET_LITERAL_ENV · github_fixture
`kubescape_regolibrary__rules__set-procmount-default__test__cronjob__input__cronjob.yaml` :: CronJob/hello :: container `mysql`
- ns=None sa=None
- container `mysql` img=mysql env=[{"name": "MYSQL_ROOT_PASSWORD", "value": "rootpasswd"}]

### R2-A046 — RES_NO_MEM_LIMIT · helm
`vault.yaml` :: Pod/pilot-vault-server-test :: container `pilot-server-test`
- ns=default sa=None
- container `pilot-server-test` img=hashicorp/vault:2.0.4 res=null

### R2-A047 — SEC_RUN_AS_ROOT_EXPLICIT · github_fixture
`fugue_regula__rego__tests__rules__k8s__root_containers__inputs__valid_example.yaml` :: Pod/valid5 :: container `pause2`
- ns=None sa=None
- container `pause2` img=k8s.gcr.io/pause rnr=None user=0 pod_rnr=True pod_user=None

### R2-A048 — RBAC_CLUSTER_ADMIN_BINDING · github_fixture
`fluxcd_flux2__cmd__flux__testdata__create_tenant__tenant-with-skip-namespace.yaml` :: RoleBinding/dev-team-reconciler
- roleRef={'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'ClusterRole', 'name': 'cluster-admin'} subjects=User:gotk:apps:reconciler,ServiceAccount:dev-team

### R2-A049 — RES_NO_MEM_LIMIT · github_fixture
`kubescape_regolibrary__rules__non-existent-service-account__test__success_empty_service_account__input__pod.yaml` :: Pod/empty-sa-pod :: container `app`
- ns=app sa=None
- container `app` img=nginx res=null

### R2-A050 — SECRET_COMMITTED · github_production
`argoproj_argo-cd__manifests__namespace-install-with-hydrator.yaml` :: Secret/argocd-secret
- secret type=Opaque values={}

### R2-A051 — SEC_CAPABILITY_ADDED · github_example
`argoproj_argocd-example-apps__sock-shop__base__user-db-dep.yaml` :: Deployment/user-db :: container `user-db`
- ns=None sa=None
- container `user-db` img=weaveworksdemos/user-db:0.3.0 caps={"drop": ["all"], "add": ["CHOWN", "SETGID", "SETUID"]}

### R2-A052 — SEC_ROOT_NOT_PREVENTED · helm
`nats.yaml` :: StatefulSet/pilot-nats :: container `reloader`
- ns=None sa=None
- container `reloader` img=natsio/nats-server-config-reloader:0.24.0 rnr=None user=None pod_rnr=None pod_user=None

### R2-A053 — RES_NO_REQUESTS · github_example
`kubernetes_examples___archived__volumes__rbd__rbd.yaml` :: Pod/rbd :: container `rbd-rw`
- ns=None sa=None
- container `rbd-rw` img=kubernetes/pause res=null

### R2-A054 — RES_NO_MEM_LIMIT · github_fixture
`kubescape_regolibrary__rules__etcd-peer-auto-tls-disabled__test__pass-argument-not-set__input__etcdpod.yaml` :: Pod/kube-apiserver-minikube :: container `etcd`
- ns=kube-system sa=None
- container `etcd` img=k8s.gcr.io/etcd:3.5.1-0 res={"requests": {"cpu": "100m", "memory": "100Mi"}}

### R2-A055 — RBAC_WILDCARD_RESOURCES · helm
`flux2.yaml` :: ClusterRole/crd-controller
- rules=[{"apiGroups": ["source.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["source.extensions.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["kustomize.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["helm.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["notification.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": ["image.toolkit.fluxcd.io"], "resources": ["*"], "verbs": ["*"]}, {"apiGroups": [""], "resources": ["namespaces", "secrets", "configmaps", "serviceaccounts"], "verbs": ["get", "list", "watch"]}, {"apiGroups": [""], "resources": ["events"], "verbs": ["create", "patch"]}, {"apiGroups": [""], "resources": ["configmaps"], "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]}, {"apiGroups": [""], "resources": ["configmaps/status"], "verbs": ["get", "update", "patch"]}, {"apiGroups": ["coordination.k8s.io"], "resources": ["leases"], "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]}]

### R2-A056 — REL_NO_LIVENESS_PROBE · github_production
`kubernetes-sigs_kustomize__kyaml__kio__filters__testdata2__dataset1-expected__java__java-deployment-2.resource.yaml` :: Deployment/app :: container `app`
- ns=None sa=None
- container `app` img=gcr.io/project/app:version probes=[]

### R2-A057 — SEC_PRIVILEGED · github_fixture
`kubescape_regolibrary__rules__rule-privileged-container__test__workloads__input__deployment.yaml` :: Deployment/test2 :: container `test-container`
- ns=default sa=None
- container `test-container` img=hashicorp/http-echo:0.2.3 priv=True

### R2-A058 — IMG_NO_DIGEST · github_fixture
`fugue_regula__rego__tests__rules__k8s__seccomp_profile__inputs__valid_example.yaml` :: Pod/valid1 :: container `pause1`
- ns=None sa=None
- container `pause1` img=k8s.gcr.io/pause

### R2-A059 — IMG_UNTAGGED · github_example
`tektoncd_pipeline__docs__resolver-template__config__demo-resolver-deployment.yaml` :: Deployment/demoresolver :: container `controller`
- ns=tekton-pipelines-resolvers sa=tekton-pipelines-resolvers
- container `controller` img=ko://github.com/tektoncd/pipeline/docs/resolver-template/cmd/demoresolver

### R2-A060 — SEC_PRIVILEGED · github_fixture
`koki_short__testdata__pods__pod_status_with_status.rekube.yaml` :: Pod/meta_test :: container `container_name`
- ns=test sa=None
- container `container_name` img=container_image priv=True

### R2-A061 — HOST_IPC · github_production
`digitalocean_doks-debug__k8s__deployment.yaml` :: Deployment/doks-debug
- ns=kube-system sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `doks-debug` img=ghcr.io/digitalocean-packages/doks-debug:latest sc={"privileged": true} res={"requests": {"memory": "0", "cpu": "0"}, "limits": {"memory": "500Mi", "cpu": "500m"}}

### R2-A062 — RBAC_CLUSTER_ADMIN_BINDING · github_fixture
`kubescape_regolibrary__rules__cluster-admin-role__test__clusterrole-rolebinding__input__rolebinding.yaml` :: RoleBinding/pod
- roleRef={'kind': 'ClusterRole', 'name': 'cluster-admin', 'apiGroup': 'rbac.authorization.k8s.io'} subjects=User:jane

### R2-A063 — SEC_CAPABILITY_ADDED · github_fixture
`fugue_regula__rego__tests__rules__k8s__net_raw_capability__inputs__invalid_example.yaml` :: Pod/invalid2 :: container `hello`
- ns=None sa=None
- container `hello` img=gcr.io/google-samples/node-hello:1.0 caps={"add": ["NET_RAW"]}

### R2-A064 — HOST_NETWORK · github_fixture
`kubescape_regolibrary__rules__ensure-that-the-api-server-service-account-lookup-argument-is-set-to-true__test__rke2-args-fail__input__1.yaml` :: Pod/kube-apiserver-rke2-server
- ns=kube-system sa=None host={'hostNetwork': True}
- container `kube-apiserver` img=index.docker.io/rancher/hardened-kubernetes:v1.32.11-rke2r1 sc={} res=null

### R2-A065 — IMG_LATEST · github_fixture
`kubescape_regolibrary__rules__dangling-networkpolicy__test__success_matches_matchexpressions_notin_absent__input__pod.yaml` :: Pod/no-tier-pod :: container `app`
- ns=default sa=None
- container `app` img=nginx:latest

### R2-A066 — REL_NO_READINESS_PROBE · github_fixture
`kubescape_regolibrary__rules__exposed-sensitive-interfaces-v1__test__pod__input__pod.yaml` :: Pod/argo-server :: container `argo-server`
- ns=default sa=None
- container `argo-server` img=argoproj/argocli:latest probes=[]

### R2-A067 — DEPRECATED_API · github_example
`helm_charts__stable__velero__crds__schedules.yaml` :: CustomResourceDefinition/schedules.velero.io
- OBJECT NOT FOUND IN FILE (evidence-absent?)

### R2-A068 — RES_NO_REQUESTS · helm
`zammad.yaml` :: Deployment/pilot-zammad-nginx :: container `zammad-nginx`
- ns=default sa=None
- container `zammad-nginx` img=ghcr.io/zammad/zammad:7.2.2-0012 res=null

### R2-A069 — IMG_NO_DIGEST · github_fixture
`kubescape_regolibrary__rules__workload-mounted-pvc__test__failed_pod_mounted__input__pod.yaml` :: Pod/mypod :: container `myfrontend`
- ns=None sa=None
- container `myfrontend` img=nginx

### R2-A070 — SEC_NO_SECCOMP · github_fixture
`kubescape_regolibrary__rules__rule-identify-blocklisted-image-registries__test__workloads__input__deployment.yaml` :: Deployment/my-deployment :: container `php`
- ns=None sa=None ann={} pod_seccomp=None
- container `php` img=registry.hub.docker.com/php:7.0-apache seccomp=None

### R2-A071 — RBAC_WILDCARD_RESOURCES · helm
`datadog.yaml` :: ClusterRole/pilot-datadog-orchestrator-explorer
- rules=[{"apiGroups": [""], "resources": ["namespaces"], "resourceNames": ["kube-system"], "verbs": ["get"]}, {"apiGroups": [""], "resources": ["configmaps"], "resourceNames": ["datadog-cluster-id"], "verbs": ["create", "get", "update"]}, {"apiGroups": [""], "resources": ["pods", "nodes", "namespaces", "limitranges", "services", "persistentvolumes", "persistentvolumeclaims", "serviceaccounts"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["discovery.k8s.io"], "resources": ["endpointslices"], "verbs": ["list", "watch"]}, {"apiGroups": ["autoscaling"], "resources": ["horizontalpodautoscalers"], "verbs": ["list", "watch"]}, {"apiGroups": ["apps"], "resources": ["deployments", "replicasets", "daemonsets", "statefulsets"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["batch"], "resources": ["cronjobs", "jobs"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["networking.k8s.io"], "resources": ["ingresses", "networkpolicies"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["rbac.authorization.k8s.io"], "resources": ["roles", "rolebindings", "clusterroles", "clusterrolebindings"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["storage.k8s.io"], "resources": ["storageclasses"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["autoscaling.k8s.io"], "resources": ["verticalpodautoscalers"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["apiextensions.k8s.io"], "resources": ["customresourcedefinitions"], "verbs": ["list", "get", "watch"]}, {"apiGroups": ["policy"], "resources": ["poddisruptionbudgets"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["datadoghq.com", "eks.amazonaws.com", "karpenter.azure.com", "karpenter.k8s.aws", "karpenter.sh"], "resources": ["*"], "verbs": ["list", "watch"]}, {"apiGroups": ["argoproj.io"], "resources": ["rollouts", "applications", "applicationsets"], "verbs": ["list", "watch", "get"]}, {"apiGroups": ["source.toolkit.fluxcd.io"], "resources": ["buckets", "helmcharts", "externalartifacts", "gitrepositories", "helmrepositories", "ocirepositories"], "verbs": ["list", "watch", "get"]}, {"apiGroups": ["kustomize.toolkit.fluxcd.io"], "resources": ["kustomizations"], "verbs": ["list", "watch", "get"]}, {"apiGroups": ["ray.io"], "resources": ["rayclusters", "raycronjobs", "rayjobs", "rayservices"], "verbs": ["list", "watch"]}, {"apiGroups": ["kubeai.org"], "resources": ["models"], "verbs": ["list", "watch"]}, {"apiGroups": ["nvidia.com"], "resources": ["dynamocheckpoints", "dynamocomponentdeployments", "dynamographdeploymentrequests", "dynamographdeployments", "dynamographdeploymentscalingadapters", "dynamomodels", "dynamoworkermetadatas"], "verbs": ["list", "watch"]}, {"apiGroups": ["serving.kserve.io"], "resources": ["clusterstoragecontainers", "llminferenceserviceconfigs", "llminferenceservices", "localmodelcaches", "localmodelnamespacecaches", "localmodelnodegroups", "localmodelnodes", "clusterservingruntimes", "inferencegraphs", "inferenceservices", "servingruntimes", "trainedmodels"], "verbs": ["list", "watch"]}, {"apiGroups": ["gateway.networking.k8s.io"], "resources": ["gatewayclasses", "gateways", "httproutes", "grpcroutes", "backendtlspolicies", "listenersets", "referencegrants", "tcproutes", "tlsroutes", "udproutes"], "verbs": ["list", "watch"]}, {"apiGroups": ["inference.networking.k8s.io"], "resources": ["inferencepools"], "verbs": ["list", "watch"]}, {"apiGroups": ["inference.networking.x-k8s.io"], "resources": ["inferencepools", "inferencepoolimports"], "verbs": ["list", "watch"]}]

### R2-A072 — REL_NO_LIVENESS_PROBE · github_example
`MasayaAoyama_kubernetes-perfect-guide__samples__chapter14__kustomize__name-sample__sample-deployment.yaml` :: Deployment/sample-deployment :: container `nginx-container`
- ns=None sa=None
- container `nginx-container` img=nginx:1.16 probes=[]

### R2-A073 — REL_NO_LIVENESS_PROBE · github_production
`elastic_cloud-on-k8s__config__recipes__elastic-agent__fleet-kubernetes-integration-nonroot.yaml` :: DaemonSet/manage-agent-hostpath-permissions :: container `pause`
- ns=None sa=None
- container `pause` img=gcr.io/google-containers/pause-amd64:3.1 probes=[]

### R2-A074 — HOST_PID · helm
`netdata.yaml` :: DaemonSet/netdata-child
- ns=default sa=netdata host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `netdata` img=netdata/netdata:v2.12.1 sc={"capabilities": {"add": ["SYS_PTRACE", "SYS_ADMIN"]}} res={}
- container `init-persistence` img=alpine:latest sc={} res={"requests": {"cpu": "10m"}}

### R2-A075 — SEC_DANGEROUS_CAPABILITY · github_fixture
`kubescape_regolibrary__rules__rule-privileged-container__test__pod__input__pod.yaml` :: Pod/audit-pod :: container `test-container`
- ns=None sa=None
- container `test-container` img=hashicorp/http-echo:0.2.3 caps={"add": ["NET_ADMIN", "SYS_ADMIN"]}

### R2-A076 — DEPRECATED_API · github_fixture
`kubescape_regolibrary__rules__psp-deny-privileged-container__test__pass-no-true__input__psp.yaml` :: PodSecurityPolicy/eks.privileged
- OBJECT NOT FOUND IN FILE (evidence-absent?)

### R2-A077 — SEC_CAPABILITY_ADDED · github_production
`kubernetes_ingress-nginx__deploy__static__provider__oracle__deploy.yaml` :: Deployment/ingress-nginx-controller :: container `controller`
- ns=ingress-nginx sa=ingress-nginx
- container `controller` img=registry.k8s.io/ingress-nginx/controller:v1.15.1@sha256:594ceea76b01c592858f803f9ff4d2cb40542cae2060410b2c95f75907d659e1 caps={"add": ["NET_BIND_SERVICE"], "drop": ["ALL"]}

### R2-A078 — SEC_PRIVILEGED · github_fixture
`koki_short__testdata__pods__pod_status_with_phase.yaml` :: Pod/meta_test :: container `container_name`
- ns=test sa=None
- container `container_name` img=container_image priv=True

### R2-A079 — DEPRECATED_API · github_production
`cloudfoundry_cf-for-k8s__config__eirini___ytt_lib__eirini__rendered.yml` :: PodSecurityPolicy/eirini-event-reporter
- rules=[{"apiGroups": [""], "resources": ["pods", "events"], "verbs": ["get", "list", "watch"]}]

### R2-A080 — HOST_IPC · github_example
`kubernetes_examples___archived__newrelic__newrelic-daemonset.yaml` :: DaemonSet/newrelic-agent
- ns=None sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `newrelic` img=newrelic/nrsysmond sc={"privileged": true} res={"requests": {"cpu": 0.15}}

### R2-A081 — HOST_NETWORK · github_fixture
`kubescape_regolibrary__rules__etcd-peer-auto-tls-disabled__test__pass-argument-set-to-false__input__etcdpod.yaml` :: Pod/kube-apiserver-minikube
- ns=kube-system sa=None host={'hostNetwork': True}
- container `etcd` img=k8s.gcr.io/etcd:3.5.1-0 sc={} res={"requests": {"cpu": "100m", "memory": "100Mi"}}

### R2-A082 — SEC_CAPABILITY_ADDED · github_fixture
`kubescape_regolibrary__rules__drop-capability-netraw__test__pod__input__pod.yaml` :: Pod/audit-pod :: container `test-container1`
- ns=None sa=None
- container `test-container1` img=hashicorp/http-echo:0.2.3 caps={"add": ["SYS_TIME"], "drop": ["NET_ADMIN"]}

### R2-A083 — RBAC_WILDCARD_VERBS · github_fixture
`kubescape_regolibrary__rules__rule-can-approve-cert-signing-request__test__role-rolebinding__input__role.yaml` :: Role/test
- rules=[{"apiGroups": ["*"], "resources": ["rolebindings", "deployments", "pods", "certificatesigningrequests/approval"], "verbs": ["*", "watch", "create", "update"]}]

### R2-A084 — IMG_NO_DIGEST · github_fixture
`kubescape_regolibrary__rules__ingress-and-egress-blocked__test__cnp-specs-list-passed__input__pod.yaml` :: Pod/test :: container `test`
- ns=my-ns sa=None
- container `test` img=test:latest

### R2-A085 — REL_NO_READINESS_PROBE · helm
`openebs.yaml` :: DaemonSet/pilot-csi-node :: container `csi-driver-registrar`
- ns=default sa=pilot-service-account
- container `csi-driver-registrar` img=registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.13.0 probes=[]

### R2-A086 — REL_NO_LIVENESS_PROBE · helm
`openebs.yaml` :: Deployment/pilot-csi-controller :: container `csi-attacher`
- ns=default sa=pilot-service-account
- container `csi-attacher` img=registry.k8s.io/sig-storage/csi-attacher:v4.8.1 probes=[]

### R2-A087 — IMG_LATEST · github_production
`argoproj_argo-cd__manifests__install-with-hydrator.yaml` :: Deployment/argocd-server :: container `argocd-server`
- ns=None sa=argocd-server
- container `argocd-server` img=quay.io/argoproj/argocd:latest

### R2-A088 — RBAC_WILDCARD_VERBS · github_production
`argoproj_argo-cd__manifests__cluster-rbac__application-controller__argocd-application-controller-clusterrole.yaml` :: ClusterRole/argocd-application-controller
- rules=[{"apiGroups": ["*"], "resources": ["*"], "verbs": ["*"]}, {"nonResourceURLs": ["*"], "verbs": ["*"]}]

### R2-A089 — RBAC_WILDCARD_VERBS · github_fixture
`kubescape_regolibrary__rules__rule-can-create-pv__test__clusterrole-rolebinding__input__cluterrole.yaml` :: ClusterRole/test
- rules=[{"apiGroups": [""], "resources": ["pods", "services", "persistentvolumes"], "verbs": ["*", "watch", "list"]}]

### R2-A090 — SEC_NO_SECCOMP · github_fixture
`argoproj_argo-cd__gitops-engine__pkg__diff__testdata__ssd-deploy-with-manual-apply-live.yaml` :: Deployment/manual-apply-test-deployment :: container `idle`
- ns=default sa=None ann={} pod_seccomp=None
- container `idle` img=spurin/idle:latest seccomp=None

### R2-A091 — SA_TOKEN_AUTOMOUNTED · github_fixture
`kubescape_regolibrary__rules__set-runasusername-value__test__workload__input__linux-deployment.yaml` :: Deployment/plain-linux-deployment
- ns=None sa=None pod_auto=None sa_auto=None
- container `nginx` img=nginx:1.25 sc={"runAsNonRoot": true, "allowPrivilegeEscalation": false} res=null

### R2-A092 — SEC_PRIVILEGED · github_production
`digitalocean_doks-debug__k8s__deployment.yaml` :: Deployment/doks-debug :: container `doks-debug`
- ns=kube-system sa=None
- container `doks-debug` img=ghcr.io/digitalocean-packages/doks-debug:latest priv=True

### R2-A093 — HOST_PID · github_example
`Karandash8_make-argocd-fly__examples__monitoring_stack__output__local__k8s__node_exporter__daemonset_node-exporter.yml` :: DaemonSet/node-exporter
- ns=kube-monitoring sa=node-exporter host={'hostNetwork': True, 'hostPID': True}
- container `node-exporter` img=quay.io/prometheus/node-exporter:v1.9.1 sc={"readOnlyRootFilesystem": true} res=null

### R2-A094 — SEC_PRIVILEGED · github_example
`kubernetes_examples___archived__sysdig-cloud__sysdig-rc.yaml` :: ReplicationController/sysdig-agent :: container `sysdig-agent`
- ns=None sa=None
- container `sysdig-agent` img=sysdig/agent priv=True

### R2-A095 — RBAC_CLUSTER_ADMIN_BINDING · helm
`velero.yaml` :: ClusterRoleBinding/pilot-velero-server
- roleRef={'kind': 'ClusterRole', 'name': 'cluster-admin', 'apiGroup': 'rbac.authorization.k8s.io'} subjects=ServiceAccount:pilot-velero-server

### R2-A096 — IMG_UNTAGGED · github_fixture
`kubescape_regolibrary__rules__linux-hardening__test__passed__input__cronjob.yaml` :: CronJob/hello :: container `mysql`
- ns=None sa=None
- container `mysql` img=mysql

### R2-A097 — SEC_ROOT_NOT_PREVENTED · github_fixture
`argoproj_argo-cd__test__e2e__testdata__hook-and-deployment__deployment.yaml` :: Deployment/my-deployment :: container `main`
- ns=None sa=None
- container `main` img=quay.io/argoprojlabs/argocd-e2e-container:0.1 rnr=None user=None pod_rnr=None pod_user=None

### R2-A098 — SEC_APE_NOT_DISABLED · github_fixture
`kubescape_regolibrary__rules__ensure-that-the-admission-control-plugin-SecurityContextDeny-is-set-if-PodSecurityPolicy-is-not-used__test__failed__input__1.yaml` :: Pod/kube-apiserver-minikube :: container `kube-apiserver`
- ns=kube-system sa=None
- container `kube-apiserver` img=k8s.gcr.io/kube-apiserver:v1.24.1 ape=None pod_ape=None

### R2-B001 — SEC_CAPABILITY_ADDED · helm
`k10.yaml` :: Deployment/logging-svc :: container `upgrade-init`
- ns=default sa=logging-svc
- container `upgrade-init` img=gcr.io/kasten-images/upgrade:9.0.8 caps={"add": ["FOWNER", "CHOWN"]}

### R2-B002 — IMG_NO_DIGEST · github_example
`MasayaAoyama_kubernetes-perfect-guide__samples__chapter07__sample-secret-single-env.yaml` :: Pod/sample-secret-single-env :: container `secret-container`
- ns=None sa=None
- container `secret-container` img=nginx:1.16

### R2-B003 — HOST_PID · github_example
`kubernetes_examples___archived__newrelic__newrelic-daemonset.yaml` :: DaemonSet/newrelic-agent
- ns=None sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `newrelic` img=newrelic/nrsysmond sc={"privileged": true} res={"requests": {"cpu": 0.15}}

### R2-B004 — DEPRECATED_API · helm
`consul.yaml` :: PodDisruptionBudget/pilot-consul-connect-injector
- rules=[{"apiGroups": ["consul.hashicorp.com"], "resources": ["servicedefaults", "serviceresolvers", "proxydefaults", "meshes", "exportedservices", "servicerouters", "servicesplitters", "serviceintentions", "ingressgateways", "terminatinggateways", "gatewayclassconfigs", "meshservices", "samenessgroups", "controlplanerequestlimits", "ratelimits", "routeretryfilters", "routetimeoutfilters", "routeauthfilters", "routetlssdsfilters", "routeupstreamlimitsfilters", "routeextprocs", "routeheadermatchinvertfilters", "gatewaypolicies", "customgatewaypolicies", "registrations", "jwtproviders"], "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]}, {"apiGroups": ["consul.hashicorp.com"], "resources": ["servicedefaults/status", "serviceresolvers/status", "proxydefaults/status", "meshes/status", "exportedservices/status", "servicerouters/status", "servicesplitters/status", "serviceintentions/status", "ingressgateways/status", "terminatinggateways/status", "samenessgroups/status", "controlplanerequestlimits/status", "ratelimits/status", "registrations/status", "jwtproviders/status", "routeauthfilters/status", "routetlssdsfilters/status", "routeupstreamlimitsfilters/status", "routeextprocs/status", "routeheadermatchinvertfilters/status", "gatewaypolicies/status", "customgatewaypolicies/status"], "verbs": ["get", "patch", "update"]}, {"apiGroups": ["consul.hashicorp.com"], "resources": ["inferencemodelconfigs", "mcpserverconfigs", "agentconfigs", "inferencepoolconfigs", "inferencegateways"], "verbs": ["get", "list", "update", "watch"]}, {"apiGroups": ["consul.hashicorp.com"], "resources": ["inferencemodelconfigs/status", "mcpserverconfigs/status", "agentconfigs/status", "inferencepoolconfigs/status", "inferencegateways/status"], "verbs": ["get", "patch", "update"]}, {"apiGroups": ["consul.hashicorp.com"], "resources": ["inferencemodelconfigs/finalizers", "mcpserverconfigs/finalizers", "agentconfigs/finalizers", "inferencepoolconfigs/finalizers", "inferencegateways/finalizers"], "verbs": ["update"]}, {"apiGroups": ["gateway.networking.k8s.io"], "resources": ["gatewayclasses", "gateways", "httproutes", "tcproutes", "referencegrants"], "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]}, {"apiGroups": ["gateway.networking.k8s.io"], "resources": ["gatewayclasses/finalizers", "gateways/finalizers", "httproutes/finalizers", "tcproutes/finalizers"], "verbs": ["update"]}, {"apiGroups": ["gateway.networking.k8s.io"], "resources": ["gatewayclasses/status", "gateways/status", "httproutes/status", "tcproutes/status"], "verbs": ["get", "patch", "update"]}, {"apiGroups": ["consul.hashicorp.com"], "resources": ["customgatewayclasses", "cgateways", "chttproutes", "ctcproutes", "creferencegrants"], "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]}, {"apiGroups": ["consul.hashicorp.com"], "resources": ["customgatewayclasses/finalizers", "cgateways/finalizers", "chttproutes/finalizers", "ctcproutes/finalizers"], "verbs": ["update"]}, {"apiGroups": ["consul.hashicorp.com"], "resources": ["customgatewayclasses/status", "cgateways/status", "chttproutes/status", "ctcproutes/status"], "verbs": ["get", "patch", "update"]}, {"apiGroups": ["apps"], "resources": ["deployments"], "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]}, {"apiGroups": ["apps"], "resources": ["statefulsets", "daemonsets"], "verbs": ["get", "list", "update"]}, {"apiGroups": ["apps"], "resources": ["replicasets"], "verbs": ["get", "list"]}, {"apiGroups": ["autoscaling"], "resources": ["horizontalpodautoscalers"], "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]}, {"apiGroups": [""], "resources": ["events"], "verbs": ["create", "patch"]}, {"apiGroups": [""], "resources": ["services"], "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]}, {"apiGroups": [""], "resources": ["secrets", "serviceaccounts"], "verbs": ["create", "delete", "get", "list", "update", "watch"]}, {"apiGroups": [""], "resources": ["endpoints", "namespaces", "nodes", "configmaps"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["discovery.k8s.io"], "resources": ["endpointslices"], "verbs": ["get", "list", "watch"]}, {"apiGroups": [""], "resources": ["pods"], "verbs": ["get", "list", "update", "watch"]}, {"apiGroups": ["rbac.authorization.k8s.io"], "resources": ["roles", "rolebindings"], "verbs": ["create", "delete", "get", "list", "update", "watch"]}, {"apiGroups": ["coordination.k8s.io"], "resources": ["leases"], "verbs": ["create", "get", "list", "update"]}, {"apiGroups": ["policy"], "resources": ["podsecuritypolicies"], "verbs": ["use"]}]

### R2-B005 — SEC_CAPABILITY_ADDED · helm
`metallb.yaml` :: DaemonSet/pilot-frr-k8s :: container `controller`
- ns=default sa=pilot-frr-k8s-controller
- container `controller` img=quay.io/metallb/frr-k8s:v0.0.25 caps={"drop": ["ALL"], "add": ["NET_RAW"]}

### R2-B006 — HOST_IPC · github_example
`kubernetes_examples___archived__newrelic-infrastructure__newrelic-infra-daemonset.yaml` :: DaemonSet/newrelic-infra-agent
- ns=None sa=None host={'hostNetwork': True, 'hostPID': True, 'hostIPC': True}
- container `newrelic` img=newrelic/infrastructure sc={"privileged": true} res={"requests": {"cpu": 0.15}}

### R2-B007 — SEC_PRIVILEGED · helm
`ceph-csi-rbd.yaml` :: DaemonSet/pilot-ceph-csi-rbd-nodeplugin :: container `driver-registrar`
- ns=default sa=pilot-ceph-csi-rbd-nodeplugin
- container `driver-registrar` img=registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.18.0 priv=True

### R2-B008 — SEC_RUN_AS_ROOT_EXPLICIT · github_fixture
`fugue_regula__rego__tests__rules__k8s__host_ipc_namespace__inputs__invalid_example.yaml` :: Pod/ubuntu :: container `example`
- ns=None sa=None
- container `example` img=ubuntu rnr=None user=0 pod_rnr=None pod_user=None

### R2-B009 — SA_TOKEN_AUTOMOUNTED · github_production
`grafana_loki__operator__hack__addons_dev.yaml` :: DaemonSet/lokistack-dev-addons-promtail
- ns=None sa=lokistack-dev-addons-promtail pod_auto=None sa_auto=None
- container `promtail` img=docker.io/grafana/promtail:3.6 sc={"privileged": true, "runAsNonRoot": false, "readOnlyRootFilesystem": true, "capabilities": {"drop": ["ALL"]}} res=null

### R2-B010 — REL_NO_LIVENESS_PROBE · github_fixture
`kubescape_regolibrary__rules__rule-credentials-in-env-var__test__deployment__input__deployment.yaml` :: Deployment/test2 :: container `test-container2`
- ns=default sa=None
- container `test-container2` img=hashicorp/http-echo:0.2.3 probes=[]

### R2-B011 — RES_NO_MEM_LIMIT · github_fixture
`kubescape_regolibrary__rules__linux-hardening__test__cronjob__input__cronjob.yaml` :: CronJob/hello :: container `php`
- ns=None sa=None
- container `php` img=php:7.0-apache res=null

### R2-B012 — RBAC_WILDCARD_RESOURCES · helm
`linkerd-viz.yaml` :: ClusterRole/linkerd-default-tap-admin
- rules=[{"apiGroups": [""], "resources": ["namespaces"], "verbs": ["list"]}, {"apiGroups": ["tap.linkerd.io"], "resources": ["*"], "verbs": ["watch"]}]

### R2-B013 — RES_NO_REQUESTS · github_example
`kubernetes_examples___archived__volumes__nfs__nfs-busybox-deployment.yaml` :: Deployment/nfs-busybox :: container `busybox`
- ns=None sa=None
- container `busybox` img=busybox res=null

### R2-B014 — SEC_ROOT_NOT_PREVENTED · github_example
`argoproj_argo-cd__applicationset__examples__applications-sync-policies__guestbook__engineering-prod__guestbook-ui-deployment.yaml` :: Deployment/guestbook-ui :: container `guestbook-ui`
- ns=None sa=None
- container `guestbook-ui` img=quay.io/argoprojlabs/argocd-e2e-container:0.2 rnr=None user=None pod_rnr=None pod_user=None

### R2-B015 — SEC_PRIVILEGED · helm
`redpanda.yaml` :: StatefulSet/pilot :: container `tuning`
- ns=default sa=pilot
- container `tuning` img=docker.redpanda.com/redpandadata/redpanda:v26.2.3 priv=True

### R2-B016 — SEC_NO_SECCOMP · github_production
`argoproj_argo-workflows__manifests__quick-start-minimal.yaml` :: Deployment/minio :: container `main`
- ns=None sa=None ann={} pod_seccomp=None
- container `main` img=docker.io/pgsty/silo:RELEASE.2026-09-16T00-00-00Z@sha256:635197cb9f36d01bee221d34d1c7d7960f6a95c48b0b6c01d99cd13bdae51a46 seccomp=None

### R2-B017 — IMG_LATEST · helm
`kubeview.yaml` :: Deployment/pilot-kubeview :: container `kubeview`
- ns=None sa=pilot-kubeview
- container `kubeview` img=ghcr.io/benc-uk/kubeview:latest

### R2-B018 — RBAC_WILDCARD_VERBS · github_production
`argoproj_argo-cd__manifests__core-install-with-hydrator.yaml` :: ClusterRole/argocd-application-controller
- rules=[{"apiGroups": [""], "resources": ["secrets", "configmaps"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["argoproj.io"], "resources": ["applications", "applicationsets", "appprojects"], "verbs": ["create", "get", "list", "watch", "update", "patch", "delete"]}, {"apiGroups": [""], "resources": ["events"], "verbs": ["create", "list"]}, {"apiGroups": ["apps"], "resources": ["deployments"], "verbs": ["get", "list", "watch"]}]

### R2-B019 — SECRET_LITERAL_ENV · github_example
`argoproj_argocd-example-apps__sock-shop__base__catalogue-db-dep.yaml` :: Deployment/catalogue-db :: container `catalogue-db`
- ns=None sa=None
- container `catalogue-db` img=weaveworksdemos/catalogue-db:0.3.0 env=[{"name": "MYSQL_ROOT_PASSWORD", "value": "fake_password"}, {"name": "MYSQL_DATABASE", "value": "socksdb"}]

### R2-B020 — SEC_PRIVILEGED · github_fixture
`kubescape_regolibrary__rules__immutable-container-filesystem__test__pod-initcontainer__input__pod.yaml` :: Pod/test :: container `init-test2`
- ns=None sa=None
- container `init-test2` img=nginx priv=True

### R2-B021 — SA_TOKEN_AUTOMOUNTED · github_fixture
`kubescape_regolibrary__rules__rule-secrets-in-env-var__test__workloads-initcontainer-envfrom-secretref__input__deployment.yaml` :: Deployment/initcontainer-secret-deploy
- ns=None sa=None pod_auto=None sa_auto=None
- container `main-container` img=nginx:1.25 sc={} res=null
- container `init-secret` img=busybox:1.36.1 sc={} res=null

### R2-B022 — SEC_APE_NOT_DISABLED · helm
`ceph-csi-cephfs.yaml` :: Deployment/pilot-ceph-csi-cephfs-provisioner :: container `csi-attacher`
- ns=default sa=pilot-ceph-csi-cephfs-provisioner
- container `csi-attacher` img=registry.k8s.io/sig-storage/csi-attacher:v4.13.0 ape=None pod_ape=None

### R2-B023 — SEC_PRIVILEGED · github_fixture
`kubescape_regolibrary__rules__containers-mounting-docker-socket__test__workloads__input__deployment.yaml` :: Deployment/my-deployment :: container `test-container2`
- ns=None sa=None
- container `test-container2` img=k8s.gcr.io/test-webserver priv=True

### R2-B024 — SEC_RUN_AS_ROOT_EXPLICIT · helm
`elasticsearch.yaml` :: StatefulSet/elasticsearch-master :: container `configure-sysctl`
- ns=None sa=None
- container `configure-sysctl` img=docker.elastic.co/elasticsearch/elasticsearch:8.5.1 rnr=None user=0 pod_rnr=None pod_user=1000

### R2-B025 — RBAC_CLUSTER_ADMIN_BINDING · github_fixture
`fluxcd_flux2__cmd__flux__testdata__create_tenant__tenant-with-service-account.yaml` :: RoleBinding/dev-team-reconciler
- roleRef={'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'ClusterRole', 'name': 'cluster-admin'} subjects=User:gotk:apps:reconciler,ServiceAccount:flux-tenant

### R2-B026 — SEC_DANGEROUS_CAPABILITY · github_fixture
`koki_short__testdata__pods__pod_status_with_phase.yaml` :: Pod/meta_test :: container `container_name`
- ns=test sa=None
- container `container_name` img=container_image caps={"add": ["NET_ADMIN", "PID"], "drop": ["NET_ADMIN", "WALK"]}

### R2-B027 — RBAC_CLUSTER_ADMIN_BINDING · github_production
`grafana_loki__tools__helm.yaml` :: ClusterRoleBinding/helm
- roleRef={'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'ClusterRole', 'name': 'cluster-admin'} subjects=ServiceAccount:helm

### R2-B028 — SECRET_COMMITTED · github_production
`argoproj_argo-workflows__manifests__quick-start-minimal.yaml` :: Secret/default.service-account-token
- secret type=kubernetes.io/service-account-token values={}

### R2-B029 — SECRET_COMMITTED · github_example
`tektoncd_pipeline__examples__v1__pipelineruns__propagating-workspaces.yaml` :: Secret/secret-password
- secret type=Opaque values={"password": "hunter2"}

### R2-B030 — HOST_PID · github_fixture
`tektoncd_pipeline__test__testdata__spire__spire-agent.yaml` :: DaemonSet/spire-agent
- ns=spire sa=spire-agent host={'hostNetwork': True, 'hostPID': True}
- container `spire-agent` img=ghcr.io/spiffe/spire-agent:1.1.1 sc={} res=null
- container `spiffe-csi-driver` img=ghcr.io/spiffe/spiffe-csi-driver:nightly sc={"privileged": true} res=null
- container `node-driver-registrar` img=k8s.gcr.io/sig-storage/csi-node-driver-registrar:v2.0.1 sc={} res=null

### R2-B031 — SEC_ROOT_NOT_PREVENTED · github_fixture
`kubescape_regolibrary__rules__rule-can-ssh-to-pod-v1__test__workloads__input__deployment.yaml` :: Deployment/test2 :: container `nginx`
- ns=default sa=None
- container `nginx` img=nginx:1.14.2 rnr=None user=None pod_rnr=None pod_user=None

### R2-B032 — RES_NO_CPU_LIMIT · github_fixture
`kubescape_regolibrary__rules__ensure-that-the-admission-control-plugin-SecurityContextDeny-is-set-if-PodSecurityPolicy-is-not-used__test__passed__input__2.yaml` :: Pod/kube-apiserver-minikube :: container `kube-apiserver`
- ns=kube-system sa=None
- container `kube-apiserver` img=k8s.gcr.io/kube-apiserver:v1.24.1 res={"requests": {"cpu": "250m"}}

### R2-B033 — RBAC_WILDCARD_RESOURCES · github_production
`argoproj_argo-cd__manifests__ha__install-with-hydrator.yaml` :: ClusterRole/argocd-server
- rules=[{"apiGroups": [""], "resources": ["secrets", "configmaps"], "verbs": ["create", "get", "list", "watch", "update", "patch", "delete"]}, {"apiGroups": ["argoproj.io"], "resources": ["applications", "appprojects", "applicationsets"], "verbs": ["create", "get", "list", "watch", "update", "delete", "patch"]}, {"apiGroups": [""], "resources": ["events"], "verbs": ["create", "list"]}]

### R2-B034 — HOST_NETWORK · github_fixture
`kubescape_regolibrary__rules__ensure-that-the-api-server-kubelet-client-certificate-and-kubelet-client-key-arguments-are-set-as-appropriate__test__rke2-args-fail__input__1.yaml` :: Pod/kube-apiserver-rke2-server
- ns=kube-system sa=None host={'hostNetwork': True}
- container `kube-apiserver` img=index.docker.io/rancher/hardened-kubernetes:v1.32.11-rke2r1 sc={} res=null

### R2-B035 — RBAC_WILDCARD_VERBS · github_example
`MasayaAoyama_kubernetes-perfect-guide__samples__chapter17__argocd__install.yaml` :: ClusterRole/argocd-application-controller
- rules=[{"apiGroups": [""], "resources": ["secrets", "configmaps"], "verbs": ["get", "list", "watch"]}, {"apiGroups": ["argoproj.io"], "resources": ["applications", "appprojects"], "verbs": ["create", "get", "list", "watch", "update", "patch", "delete"]}, {"apiGroups": [""], "resources": ["events"], "verbs": ["create", "list"]}]

### R2-B036 — HOST_NETWORK · github_example
`Karandash8_make-argocd-fly__examples__monitoring_stack__output__local__k8s__node_exporter__daemonset_node-exporter.yml` :: DaemonSet/node-exporter
- ns=kube-monitoring sa=node-exporter host={'hostNetwork': True, 'hostPID': True}
- container `node-exporter` img=quay.io/prometheus/node-exporter:v1.9.1 sc={"readOnlyRootFilesystem": true} res=null

### R2-B037 — REL_NO_READINESS_PROBE · github_production
`zimmertr_Kubernetes-Manifests__misc__heimdall.disabled__resources__statefulset.yml` :: StatefulSet/heimdall :: container `heimdall`
- ns=None sa=None
- container `heimdall` img=linuxserver/heimdall probes=[]

### R2-B038 — SECRET_LITERAL_ENV · github_fixture
`elastic_cloud-on-k8s__hack__upgrade-test-harness__testdata__v261__install.yaml` :: StatefulSet/elastic-operator :: container `manager`
- ns=elastic-system sa=elastic-operator
- container `manager` img=docker.elastic.co/eck/eck-operator:2.6.1 env=[{"name": "WEBHOOK_SECRET", "value": "elastic-webhook-server-cert"}]

### R2-B039 — RES_NO_REQUESTS · github_production
`argoproj_argo-workflows__manifests__quick-start-telemetry.yaml` :: Deployment/workflow-controller :: container `workflow-controller`
- ns=argo sa=argo
- container `workflow-controller` img=quay.io/argoproj/workflow-controller:latest res=null

### R2-B040 — SEC_PRIVILEGED · helm
`openebs.yaml` :: DaemonSet/pilot-agent-ha-node :: container `agent-ha-node`
- ns=default sa=None
- container `agent-ha-node` img=docker.io/openebs/mayastor-agent-ha-node:develop priv=True

### R2-B041 — DEPRECATED_API · github_fixture
`kubescape_regolibrary__rules__psp-deny-allowprivilegeescalation__test__pass-no-true__input__psp.yaml` :: PodSecurityPolicy/eks.privileged
- OBJECT NOT FOUND IN FILE (evidence-absent?)

### R2-B042 — RES_NO_MEM_LIMIT · github_fixture
`kubescape_regolibrary__rules__etcd-auto-tls-disabled__test__pass-argument-not-set__input__etcdpod.yaml` :: Pod/kube-apiserver-minikube :: container `etcd`
- ns=kube-system sa=None
- container `etcd` img=k8s.gcr.io/etcd:3.5.1-0 res={"requests": {"cpu": "100m", "memory": "100Mi"}}

### R2-B043 — IMG_LATEST · helm
`nexus3.yaml` :: StatefulSet/pilot-nexus3 :: container `tail-tasks-log`
- ns=default sa=pilot-nexus3
- container `tail-tasks-log` img=cgr.dev/chainguard/bash:latest

### R2-B044 — HOST_IPC · github_fixture
`kubescape_regolibrary__rules__host-ipc-privileges__test__workload__input__deployment.yaml` :: Deployment/my-deployment
- ns=None sa=None host={'hostPID': True, 'hostIPC': True}
- container `mysql` img=mysql sc={} res=null
- container `php` img=php:7.0-apache sc={} res=null

### R2-B045 — IMG_NO_DIGEST · github_production
`argoproj_argo-cd__manifests__ha__namespace-install-with-hydrator.yaml` :: Deployment/argocd-notifications-controller :: container `argocd-notifications-controller`
- ns=None sa=argocd-notifications-controller
- container `argocd-notifications-controller` img=quay.io/argoproj/argocd:latest

### R2-B046 — SEC_DANGEROUS_CAPABILITY · github_fixture
`kubescape_regolibrary__rules__sudo-in-container-entrypoint__test__cronjob__input__cronjob.yaml` :: CronJob/hello :: container `hello`
- ns=None sa=kubernetes-dashboard
- container `hello` img=busybox:latest caps={"add": ["NET_ADMIN", "SYS_TIME", "SYS_ADMIN"]}

### R2-B047 — IMG_UNTAGGED · github_example
`argoproj_argocd-example-apps__sock-shop__base__rabbitmq-dep.yaml` :: Deployment/rabbitmq :: container `rabbitmq-exporter`
- ns=None sa=None
- container `rabbitmq-exporter` img=kbudde/rabbitmq-exporter

### R2-B048 — RES_NO_CPU_LIMIT · helm
`metallb.yaml` :: DaemonSet/pilot-frr-k8s :: container `reloader`
- ns=default sa=pilot-frr-k8s-controller
- container `reloader` img=quay.io/frrouting/frr:10.4.3 res=null

### R2-B049 — SEC_APE_NOT_DISABLED · github_fixture
`kubescape_regolibrary__rules__image-not-pinned-to-digest__test__pod-sha512-short__input__pod.yaml` :: Pod/pod-sha512-short :: container `app`
- ns=None sa=None
- container `app` img=nginx@sha512:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ape=None pod_ape=None

### R2-B050 — REL_NO_READINESS_PROBE · github_example
`GoogleCloudPlatform_bank-of-anthos__src__accounts__accounts-db__k8s__overlays__development__accounts-db.yaml` :: StatefulSet/accounts-db :: container `accounts-db`
- ns=None sa=default
- container `accounts-db` img=accounts-db probes=[]

### R2-B051 — SEC_NO_SECCOMP · helm
`gitea.yaml` :: Deployment/pilot-gitea :: container `configure-gitea`
- ns=default sa=None ann={} pod_seccomp=None
- container `configure-gitea` img=docker.gitea.com/gitea:1.27.0-rootless seccomp=None

### R2-B052 — REL_NO_LIVENESS_PROBE · github_fixture
`argoproj_argo-rollouts__pkg__kubectl-argo-rollouts__info__testdata__blue-green__active-pod2.yaml` :: Pod/bluegreen-demo-6cbccd9f99-kxj8g :: container `bluegreen-demo`
- ns=jesse-test sa=default
- container `bluegreen-demo` img=argoproj/rollouts-demo:blue probes=[]
