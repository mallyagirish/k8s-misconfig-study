#!/usr/bin/env python3
"""Build the blinded independent second-rater packet.

Draws a seeded, rule-stratified subsample (150 rows: Batch A 100 + Batch B 50)
from the author-verified validation sample, re-keys it under blinded IDs, and
emits the rater-facing packet (no labels anywhere) plus the author-side sealed
key and sampling manifest.

Frame: final verified labels = prelabel, overridden by verification_divergence
recommended_v3 for the 92 divergence rows; rows whose final label is EXCLUDED
(or prelabel 'unsure' with no override) are out of frame. Deduped to distinct
finding keys (source_file, kind, name, container, rule), mirroring the
kappa-subset design. Allocation per rule is proportional to the deduped frame
with a floor of 2 and a cap of 14, largest-remainder to exactly 150.

Usage: python3 scripts/build_second_rater_packet.py
Outputs: results/second_rater/packet/{blind_sample.csv,packets.jsonl,packets.md,
mapping_audit.md} (README.md and protocol_for_rater.md are hand-written),
results/second_rater/{KEY_sealed.csv,sample_manifest.md} (author-side).
"""
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
OUT = RES / "second_rater"
PKT = OUT / "packet"
SEED = 20261028
TARGET, CAP, FLOOR = 150, 14, 2

# --- frame -----------------------------------------------------------------
pre = {r["sample_id"]: r for r in csv.DictReader(open(RES / "labeling_sample_v2_prelabelled.csv"))}
div = {r["sample_id"]: r["recommended_v3"] for r in csv.DictReader(open(RES / "verification_divergence.csv"))}
frame = {}
for sid, r in pre.items():
    final = div.get(sid, r["prelabel"])
    if final in ("TP", "FP", "TP-hardening"):
        frame[sid] = {**r, "final_label": final}

# --- dedupe to distinct finding keys ---------------------------------------
by_key = {}
for sid in sorted(frame):
    r = frame[sid]
    key = (r["source_file"], r["kind"], r["name"], r["container"], r["rule"])
    by_key.setdefault(key, sid)
deduped = {sid: frame[sid] for sid in by_key.values()}

# --- stratified allocation --------------------------------------------------
by_rule = defaultdict(list)
for sid, r in deduped.items():
    by_rule[r["rule"]].append(sid)
total = len(deduped)
raw = {rule: len(sids) * TARGET / total for rule, sids in by_rule.items()}
alloc = {rule: min(CAP, max(min(FLOOR, len(by_rule[rule])), int(raw[rule]))) for rule in by_rule}
# largest-remainder adjust to exactly TARGET, respecting floor/cap
while sum(alloc.values()) != TARGET:
    if sum(alloc.values()) < TARGET:
        cands = sorted(by_rule, key=lambda ru: (-(raw[ru] - alloc[ru]), ru))
        progressed = False
        for ru in cands:
            if alloc[ru] < min(CAP, len(by_rule[ru])):
                alloc[ru] += 1
                progressed = True
                break
        if not progressed:
            break
    else:
        cands = sorted(by_rule, key=lambda ru: (-(alloc[ru] - raw[ru]), ru))
        for ru in cands:
            if alloc[ru] > min(FLOOR, len(by_rule[ru])):
                alloc[ru] -= 1
                break

rng = random.Random(SEED)
drawn = []  # (sample_id, batch)
for rule in sorted(by_rule):
    sids = sorted(by_rule[rule])
    rng.shuffle(sids)
    take = sids[: alloc[rule]]
    n_a = round(len(take) * 2 / 3)
    drawn += [(s, "A") for s in take[:n_a]] + [(s, "B") for s in take[n_a:]]

# --- blinded IDs -------------------------------------------------------------
blind = {}  # sample_id -> blind_id
for batch, prefix in (("A", "R2-A"), ("B", "R2-B")):
    ids = sorted(s for s, b in drawn if b == batch)
    rng.shuffle(ids)
    for i, sid in enumerate(ids, 1):
        blind[sid] = f"{prefix}{i:03d}"
order = sorted(drawn, key=lambda sb: blind[sb[0]])

# --- packet records -----------------------------------------------------------
packets = {}
for line in open(RES / "labeling_packets.jsonl"):
    p = json.loads(line)
    if p["sample_id"] in blind:
        q = {k: v for k, v in p.items() if k != "sample_id"}
        q = {"blind_id": blind[p["sample_id"]], **q}
        packets[blind[p["sample_id"]]] = q

# --- blind_sample.csv ----------------------------------------------------------
PKT.mkdir(parents=True, exist_ok=True)
with open(PKT / "blind_sample.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["blind_id", "batch", "arm", "source_group", "source_file", "kind",
                "name", "container", "rule", "blind_label", "blind_reason", "blind_notes"])
    for sid, batch in order:
        r = frame[sid]
        w.writerow([blind[sid], batch, r["arm"], r["source_group"], r["source_file"],
                    r["kind"], r["name"], r["container"], r["rule"], "", "", ""])

with open(PKT / "packets.jsonl", "w") as fh:
    for sid, _ in order:
        fh.write(json.dumps(packets[blind[sid]]) + "\n")

# --- packets.md (print_packets-style rendering, blinded order) ------------------
def render(p):
    rule = p["rule"]
    f = p["file"].split("/", 1)[1] if "/" in p["file"] else p["file"]
    head = f'### {p["blind_id"]} — {rule} · {p["group"]}\n`{f}` :: {p["kind"]}/{p["name"]}' + \
           (f' :: container `{p["container"]}`' if p.get("container") else "")
    if p.get("not_found"):
        return head + "\n- OBJECT NOT FOUND IN FILE (evidence-absent?)"
    if "secret" in p:
        return head + f'\n- secret type={p["secret"]["type"]} values={json.dumps(p["secret"]["values"])}'
    if "rbac_rules" in p:
        return head + f'\n- rules={json.dumps(p["rbac_rules"])}'
    if "roleRef" in p:
        subs = ",".join(f'{s.get("kind")}:{s.get("name")}' for s in (p.get("subjects") or []))
        return head + f"\n- roleRef={p['roleRef']} subjects={subs}"
    pod_sc = p.get("pod_sc") or {}
    parts = [f'ns={p.get("ns")}', f'sa={p.get("sa")}']
    if rule == "SA_TOKEN_AUTOMOUNTED":
        parts += [f'pod_auto={p.get("pod_automount")}', f'sa_auto={p.get("sa_automount")}']
    if rule.startswith("HOST"):
        parts.append(f'host={p.get("host")}')
    if rule == "SEC_NO_SECCOMP":
        parts.append(f'ann={json.dumps(p.get("annotations"))} pod_seccomp={pod_sc.get("seccompProfile")}')
    lines = [head, "- " + " ".join(parts)]
    for c in p.get("containers") or []:
        sc = c.get("sc") or {}
        if rule == "SEC_PRIVILEGED":
            focus = f'priv={sc.get("privileged")}'
        elif rule == "SEC_APE_NOT_DISABLED":
            focus = f'ape={sc.get("allowPrivilegeEscalation")} pod_ape={pod_sc.get("allowPrivilegeEscalation")}'
        elif rule in ("SEC_ROOT_NOT_PREVENTED", "SEC_RUN_AS_ROOT_EXPLICIT"):
            focus = (f'rnr={sc.get("runAsNonRoot")} user={sc.get("runAsUser")} '
                     f'pod_rnr={pod_sc.get("runAsNonRoot")} pod_user={pod_sc.get("runAsUser")}')
        elif rule == "SEC_NO_SECCOMP":
            focus = f'seccomp={sc.get("seccompProfile")}'
        elif rule.startswith("SEC_CAP") or rule == "SEC_DANGEROUS_CAPABILITY":
            focus = f'caps={json.dumps(sc.get("capabilities"))}'
        elif rule.startswith("RES"):
            focus = f'res={json.dumps(c.get("resources"))}'
        elif rule.startswith("REL"):
            focus = f'probes={c["probes"]}'
        elif rule.startswith("IMG"):
            focus = ""
        elif rule == "SECRET_LITERAL_ENV":
            focus = f'env={json.dumps(c["env_values"])}'
        else:
            focus = f'sc={json.dumps(sc)} res={json.dumps(c.get("resources"))}'
        lines.append(f'- container `{c["name"]}` img={c["image"]} {focus}'.rstrip())
    return "\n".join(lines)

with open(PKT / "packets.md", "w") as fh:
    fh.write("# Evidence packets (same order as blind_sample.csv)\n\n")
    fh.write("\n\n".join(render(packets[blind[sid]]) for sid, _ in order) + "\n")

# --- mapping_audit.md -------------------------------------------------------------
matrix = (RES / "tool_coverage_matrix.md").read_text().splitlines()
table = [l for l in matrix if l.startswith("|")]
calls = [
    ("kube-linter `liveness-port` / `readiness-port` validate probe *ports*, not probe absence",
     "treated as **no check** for REL_NO_LIVENESS_PROBE / REL_NO_READINESS_PROBE"),
    ("kube-linter `deprecated-service-account-field` flags a deprecated field, not token automounting",
     "treated as **no check** for SA_TOKEN_AUTOMOUNTED"),
    ("kube-linter `unsafe-sysctls` / `docker-sock` cover adjacent dangers, not added capabilities per se",
     "treated as **no check** for SEC_DANGEROUS_CAPABILITY"),
    ("Polaris `pullPolicyNotAlways` is a proxy for, not a test of, digest pinning",
     "treated as **no check** for IMG_NO_DIGEST"),
    ("Checkov's cluster-admin-binding coverage would have to come from unspecified CKV2 graph checks; none of CKV2_K8S_1–5 in the output is a cluster-admin-binding check",
     "treated as **unmappable / no check** for RBAC_CLUSTER_ADMIN_BINDING"),
    ("kube-linter `latest-tag` fires on both untagged and `:latest` images",
     "a `latest-tag` report counts as detection for **both** IMG_LATEST and IMG_UNTAGGED (merged)"),
    ("kubeaudit `LimitsNotSet` is a pod-level union over CPU and memory",
     "counts toward **both** RES_NO_CPU_LIMIT and RES_NO_MEM_LIMIT"),
    ("Polaris `linuxHardening` is a composite (seccomp among other properties)",
     "mapped to SEC_NO_SECCOMP"),
    ("kubeaudit reports allowPrivilegeEscalation as two auditors (Nil and True)",
     "combined for SEC_APE_NOT_DISABLED"),
    ("Checkov output identifies objects but not containers; kube-linter names the container in its messages",
     "Checkov joins at object level; kube-linter at container level"),
]
with open(PKT / "mapping_audit.md", "w") as fh:
    fh.write("# Scanner check-to-rule mapping audit (optional second task)\n\n")
    fh.write("The study compares four scanners (kube-linter, kubeaudit, Polaris, Checkov)\n"
             "against its own 25 rules. The mapping below — which scanner check stands for\n"
             "which rule — was built by the author from the tools' documentation and output.\n"
             "It is partly judgment-based. Please sanity-check it, especially the flagged\n"
             "calls in the second section: for each, mark **agree** / **disagree** and add a\n"
             "note if you would map it differently. If you spot a check that is mis-assigned\n"
             "or a rule a tool *does* cover that is shown as uncovered, note that too.\n\n")
    fh.write("## The mapping (counts are the tool's findings on the study's Helm corpus)\n\n")
    fh.write("\n".join(table) + "\n\n")
    fh.write("## Judgment calls to audit\n\n")
    for i, (what, treated) in enumerate(calls, 1):
        fh.write(f"{i}. {what} — {treated}.\n   - [ ] agree  [ ] disagree — notes: ______\n\n")
    fh.write("## Anything else\n\n- A check mapped to the wrong rule: ______\n"
             "- A rule shown as uncovered that a tool does check: ______\n"
             "- Other concerns: ______\n")

# --- sealed key + manifest (author-side) -------------------------------------------
with open(OUT / "KEY_sealed.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["blind_id", "sample_id", "final_label", "batch", "rule"])
    for sid, batch in order:
        w.writerow([blind[sid], sid, frame[sid]["final_label"], batch, frame[sid]["rule"]])

na = sum(1 for _, b in drawn if b == "A")
dist = Counter(frame[sid]["final_label"] for sid, _ in drawn)
with open(OUT / "sample_manifest.md", "w") as fh:
    fh.write("# Second-rater subsample — sampling manifest (AUTHOR-SIDE; contains label distribution)\n\n")
    fh.write(f"- Built by `scripts/build_second_rater_packet.py`, seed {SEED}.\n")
    fh.write(f"- Frame: {len(frame)} rows with final verified labels (TP/FP/TP-hardening); "
             f"deduped to {len(deduped)} distinct finding keys.\n")
    fh.write(f"- Drawn: {len(drawn)} (Batch A {na}, Batch B {len(drawn) - na}); "
             f"allocation per rule proportional to the deduped frame, floor {FLOOR}, cap {CAP}.\n")
    fh.write(f"- Label distribution of the draw (author-side only): {dict(dist)}.\n\n")
    fh.write("| Rule | Frame (deduped) | Drawn |\n|---|---:|---:|\n")
    for rule in sorted(by_rule):
        fh.write(f"| {rule} | {len(by_rule[rule])} | {alloc[rule]} |\n")
    fh.write("\nScoring once labels return: `python3 scripts/score_second_rater.py <returned csv>`.\n"
             "The key (KEY_sealed.csv) stays out of git until the rater returns the sheet;\n"
             "it is published with the replication package afterwards.\n")

print(f"frame={len(frame)} deduped={len(deduped)} drawn={len(drawn)} (A={na}, B={len(drawn) - na})")
print("draw label distribution (author-side):", dict(dist))
