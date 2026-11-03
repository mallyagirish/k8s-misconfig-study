# Labeling protocol — independent rater edition

You are labeling a sample of automated findings from a study of Kubernetes
configuration practices. Each row is one finding: a rule (e.g.
`SEC_PRIVILEGED`) fired on one object (and usually one container) in one
manifest file. Your job is to judge, for each row, whether the finding is a
genuine instance of the misconfiguration the rule names — using **only this
protocol** and the evidence packet provided. This document is the complete
standard; label every row by it, including rows where your instinct differs.

## The labeling question

> **Does this manifest, in context, exhibit the misconfiguration the rule
> names — judged by the per-rule tests below?**

Labels:

- **TP** — yes, per the rule's test.
- **FP** — no. Record the reason in `blind_reason` using one of these codes:
  `infra-need` (the workload's infrastructure function requires it),
  `placeholder` (empty / template / reference content, not real data),
  `fixture` (example or test material, not a real deployment),
  `standard-practice` (an accepted pattern for this class of software),
  `parser-artifact` (the flagged property is not actually present),
  `not-exploitable` (the property is present but no realistic risk path
  exists under the rule's test).
- **TP-hardening** — only where Rule 1 below says so (an image with an
  explicit version tag but no digest pin).
- **unsure** — the packet and protocol genuinely do not decide it. Use this
  sparingly; note why in `blind_notes`. If the flagged property cannot be
  observed in the source file at all (e.g. the image is injected by an
  overlay and never appears), label **unsure** and write `evidence-absent`.

Judge the manifest as written, in its own context: a node-level agent is not
an application workload, an example in a book repository is not a production
deployment, and an operator's own API surface is not a tenant's.

## Decision rules

1. **Image digests are two-tier.** `IMG_UNTAGGED` (no tag at all) and
   `IMG_LATEST` (tag `latest`, explicit or implied) are misconfigurations:
   **TP**. `IMG_NO_DIGEST` where the image carries an *explicit version tag*
   (e.g. `nginx:1.16`) is **TP-hardening** — a hardening gap, not a
   misconfiguration. `IMG_NO_DIGEST` with no tag or `latest` is **TP**.
2. **Resource and probe rules are production-scoped.** For `RES_*` (resource
   requests/limits) and `REL_*` (liveness/readiness probes) rules, findings
   in example- or fixture-sourced files, and findings on one-shot Jobs, are
   **FP** (`fixture`). The same finding in a production-sourced file is
   judged on its merits (usually TP if the property is absent).
3. **Escalation-path test for `SEC_APE_NOT_DISABLED` and
   `SEC_ROOT_NOT_PREVENTED`.** TP requires a real escalation path: the
   container runs as root (or fails to prevent it in a way that binds), adds
   capabilities, or has a writable root filesystem with setuid risk. A
   container pinned non-root with no added capabilities is **FP**
   (`not-exploitable`) even if the specific field the rule names is unset.
4. **`DEPRECATED_API`** (an apiVersion removed in a later Kubernetes
   release) is a factual property of the manifest: if the version is as
   flagged, label **TP**.
5. **`SECRET_COMMITTED` requires credential material.** Empty Secrets,
   operator-populated placeholders, documented placeholder values, template
   or reference values (`${...}`, `<...>`), and credential-free connection
   strings (URLs without a password) are **FP** (`placeholder`). Non-empty
   literal passwords, tokens, or private keys are **TP**.
6. **`SEC_CAPABILITY_ADDED` excludes least-privilege patterns.** Adding only
   default-set capabilities, or `NET_BIND_SERVICE` alongside
   `drop: [ALL]`, is **FP** (`standard-practice`). Genuinely dangerous
   additions are `SEC_DANGEROUS_CAPABILITY`'s scope.
7. **Infrastructure class for host/privileged rules.** `SEC_PRIVILEGED`,
   `HOST_NETWORK`, `HOST_PID`, and `HOST_IPC` findings on node-level agents
   whose function requires the access (CSI/CNI drivers, node exporters,
   control-plane static pods) are **FP** (`infra-need`). The same property
   on an application workload is **TP**.
8. **`SA_TOKEN_AUTOMOUNTED`** is **FP** (`infra-need`) where the workload's
   function requires Kubernetes API access (controllers, operators,
   certificate managers); **TP** for application workloads with no API need.
   Consider both the pod's and the ServiceAccount's own automount settings,
   which the packet shows.
9. **`SECRET_LITERAL_ENV`** (a secret-looking value set as a literal
   environment variable) excludes `*_FILE` paths, secret-name references,
   password-policy settings, and obvious placeholders — those are **FP**
   (`placeholder` / `standard-practice`). An actual credential value is
   **TP**.
10. **`SEC_DANGEROUS_CAPABILITY` joins the infrastructure class** when both
    hold: (a) the container's capability drops include `ALL` (a drop-ALL
    baseline), and (b) the added capabilities are required by the
    container's node-infrastructure function. Then **FP** (`infra-need`).
    Added capabilities beyond that function, or no drop-ALL baseline, are
    **TP**. *Worked example:* a CNI agent's init container adding SYS_ADMIN,
    SYS_CHROOT, and SYS_PTRACE over `drop: [ALL]` to mount the host cgroup
    filesystem — FP. The same capability set on an application container —
    TP.
11. **RBAC wildcards confined to the project's own API groups are a
    standard operator pattern.** For `RBAC_WILDCARD_RESOURCES` and
    `RBAC_WILDCARD_VERBS`: a wildcard grant is **FP** (`standard-practice`)
    when *every* wildcard grant in the role is confined to API groups owned
    by the same project that ships the role — no wildcard apiGroup, and no
    wildcard grant in the core group or in foreign groups. Wildcards
    spanning `*` apiGroups, the core group, or foreign groups are **TP**.
    Apply the test per wildcard grant, not per role. *Worked examples:* a
    Flux controller role with wildcards only inside its own
    `*.toolkit.fluxcd.io` groups — FP. A Crossplane role whose wildcard
    grants include `verbs: ["*"]` on `secrets` in the core group — TP.
12. **Production scoping is determined by content where the path indicates
    test material.** If a file's path places it under test or fixture
    material (e.g. `testdata/`, `fixtures/`, test directories), treat it as
    fixture material for Rule 2 even if its source is a production
    repository. *Worked example:* a missing-liveness-probe finding in a
    kustomize `testdata` tree — FP (`fixture`).

## Reading the evidence packet

`packets.md` (or `packets.jsonl`) holds one packet per row, in the same
order as `blind_sample.csv`: the source file path, object kind/name,
container, the pod's and ServiceAccount's automount settings, the pod
security context, host-namespace flags, and per-container image, security
context, resources, probes, and literal environment values. Secret packets
show the Secret's type and (previews of) its values; RBAC packets show the
role's rules or the binding's roleRef and subjects. The packet is designed
to contain everything the judgment needs.
