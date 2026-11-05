#!/usr/bin/env python3
"""Build the single-author self-audit packet for the retained AI pre-labels.

Design (logged in LAB_NOTEBOOK.md, 2026-11-03): of the 451 matched validation
rows, 111 carry author-produced or individually adjudicated labels (30 blind +
87 divergence, 6 in both) and 340 retain the AI pre-labels accepted in the
verification pass (manuscript Section 3.4). This packet draws 100 of the
retained findings for the author to re-label blind -- no original label, no AI
rationale -- under the frozen v3 protocol, so the label-change rate of the
retained set can be measured. It is an annotation-stability audit by the same
author, NOT inter-rater reliability and NOT independent validation.

Population derivation (verified by assertion below, against the published
accounting in results/precision_provisional.md and
results/reconciliation_v3_DRAFT.md):
- final label = prelabel (results/labeling_sample_v2_prelabelled.csv),
  overridden by recommended_v3 for the 92 rows in
  results/verification_divergence.csv;
- matched frame = sample rows whose (arm, source, kind, name, container,
  rule) key still exists in results/findings_v3.jsonl -> 451 rows, finals
  279 TP / 162 FP / 7 TP-hardening / 3 EXCLUDED;
- author set = divergence rows + kappa blind subset
  (results/kappa_subset/blind_sample.csv) within the frame -> 111 rows;
- population = frame minus author set -> 340 rows (finals all TP/FP, each
  equal to its prelabel), deduped to 301 distinct finding keys (the kappa
  and second-rater subsamples also drew over distinct keys).

Draw: seed 20261103; allocation per rule proportional to the deduped
population, floor 2, cap 14, largest-remainder to exactly 100; within a rule,
the allocation is split across source groups proportionally (largest
remainder), mirroring the group stratification of scripts/build_labeling_
sample.py, then a seeded shuffle within each group.

Usage: python3 scripts/build_self_audit_packet.py
Outputs: results/self_audit/packet/{audit_sample.csv,packets.jsonl,packets.md,
protocol_for_audit.md} (packet/README.md is hand-written),
results/self_audit/{KEY_sealed.csv,sample_manifest.md} (author-side; the key
is gitignored until the audit is scored).
"""
import csv
import json
import random
import shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
OUT = RES / "self_audit"
PKT = OUT / "packet"
SEED = 20261103
TARGET, CAP, FLOOR = 100, 14, 2
DROPPED_IDS = {"K8S-113", "K8S-202", "K8S-207", "K8S-213", "K8S-236", "K8S-371"}

# --- reconstruct the frame, verifying the published accounting --------------
pre = {r["sample_id"]: r for r in csv.DictReader(open(RES / "labeling_sample_v2_prelabelled.csv"))}
div = {r["sample_id"]: r["recommended_v3"] for r in csv.DictReader(open(RES / "verification_divergence.csv"))}
blind = {r["sample_id"] for r in csv.DictReader(open(RES / "kappa_subset" / "blind_sample.csv"))}
assert len(pre) == 457 and len(div) == 92 and len(blind) == 30

findings = set()
for line in open(RES / "findings_v3.jsonl"):
    f = json.loads(line)
    findings.add((f["arm"], f["source"], f["kind"], f["name"], f["container"] or "", f["rule"]))


def final_of(sid):
    return div.get(sid, pre[sid]["prelabel"])


matched, dropped = {}, set()
for sid, r in pre.items():
    key = (r["arm"], r["source_file"], r["kind"], r["name"], r["container"], r["rule"])
    (matched.__setitem__(sid, r) if key in findings else dropped.add(sid))
assert len(matched) == 451 and dropped == DROPPED_IDS, f"frame mismatch: {len(matched)}, {sorted(dropped)}"
assert Counter(final_of(s) for s in matched) == {"TP": 279, "FP": 162, "TP-hardening": 7, "EXCLUDED": 3}

author = (set(div) | blind) & set(matched)
assert len(set(div) & set(matched)) == 87 and len(blind & set(matched)) == 30
assert len(set(div) & blind & set(matched)) == 6 and len(author) == 111

pop_rows = {sid: matched[sid] for sid in matched if sid not in author}
assert len(pop_rows) == 340
assert all(final_of(s) == pop_rows[s]["prelabel"] for s in pop_rows)  # retained: no override
assert {final_of(s) for s in pop_rows} <= {"TP", "FP"}

# --- dedupe to distinct finding keys ----------------------------------------
by_key = {}
for sid in sorted(pop_rows):
    r = pop_rows[sid]
    by_key.setdefault((r["source_file"], r["kind"], r["name"], r["container"], r["rule"]), sid)
deduped = {sid: pop_rows[sid] for sid in by_key.values()}
rows_per_key = Counter(
    (pop_rows[s]["source_file"], pop_rows[s]["kind"], pop_rows[s]["name"],
     pop_rows[s]["container"], pop_rows[s]["rule"]) for s in pop_rows)
assert len(deduped) == 301

# --- stratified allocation ---------------------------------------------------
by_rule = defaultdict(list)
for sid, r in deduped.items():
    by_rule[r["rule"]].append(sid)
total = len(deduped)
raw = {rule: len(sids) * TARGET / total for rule, sids in by_rule.items()}
alloc = {rule: min(CAP, max(min(FLOOR, len(by_rule[rule])), int(raw[rule]))) for rule in by_rule}
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
drawn = []  # sample_ids
for rule in sorted(by_rule):
    groups = defaultdict(list)
    for sid in by_rule[rule]:
        groups[deduped[sid]["source_group"]].append(sid)
    n_rule = len(by_rule[rule])
    graw = {g: len(gs) * alloc[rule] / n_rule for g, gs in groups.items()}
    gtake = {g: int(graw[g]) for g in groups}
    left = alloc[rule] - sum(gtake.values())
    for g in sorted(groups, key=lambda g: (-(graw[g] - gtake[g]), g)):
        if left <= 0:
            break
        if gtake[g] < len(groups[g]):
            gtake[g] += 1
            left -= 1
    for g in sorted(groups):
        sids = sorted(groups[g])
        rng.shuffle(sids)
        drawn += sids[: gtake[g]]
assert len(drawn) == TARGET

# --- blinded IDs --------------------------------------------------------------
rng.shuffle(drawn)
audit_id = {sid: f"SA-{i:03d}" for i, sid in enumerate(drawn, 1)}
order = sorted(drawn, key=lambda s: audit_id[s])

# --- packet records -------------------------------------------------------------
packets = {}
for line in open(RES / "labeling_packets.jsonl"):
    p = json.loads(line)
    if p["sample_id"] in audit_id:
        q = {k: v for k, v in p.items() if k != "sample_id"}
        q = {"audit_id": audit_id[p["sample_id"]], **q}
        packets[audit_id[p["sample_id"]]] = q
assert len(packets) == TARGET

PKT.mkdir(parents=True, exist_ok=True)
with open(PKT / "audit_sample.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["audit_id", "arm", "source_group", "source_file", "kind",
                "name", "container", "rule", "audit_label", "audit_reason", "audit_notes"])
    for sid in order:
        r = deduped[sid]
        w.writerow([audit_id[sid], r["arm"], r["source_group"], r["source_file"],
                    r["kind"], r["name"], r["container"], r["rule"], "", "", ""])

with open(PKT / "packets.jsonl", "w") as fh:
    for sid in order:
        fh.write(json.dumps(packets[audit_id[sid]]) + "\n")

# --- packets.md (print_packets-style rendering, blinded order) ------------------
def render(p):
    rule = p["rule"]
    f = p["file"].split("/", 1)[1] if "/" in p["file"] else p["file"]
    head = f'### {p["audit_id"]} — {rule} · {p["group"]}\n`{f}` :: {p["kind"]}/{p["name"]}' + \
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
    fh.write("# Evidence packets (same order as audit_sample.csv)\n\n")
    fh.write("\n\n".join(render(packets[audit_id[sid]]) for sid in order) + "\n")

# The frozen v3 protocol in labeling form: verbatim copy of the second-rater
# packet's protocol edition (canonical sources: results/labeling_protocol_v3.md
# and results/labeling_protocol_v3_addendum.md).
shutil.copyfile(RES / "second_rater" / "packet" / "protocol_for_rater.md",
                PKT / "protocol_for_audit.md")

# --- sealed key + manifest (author-side) -----------------------------------------
def key_of(sid):
    r = pop_rows[sid]
    return (r["source_file"], r["kind"], r["name"], r["container"], r["rule"])

with open(OUT / "KEY_sealed.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["audit_id", "sample_id", "original_label", "ai_prelabel", "rule", "arm",
                "source_group", "rows_covered"])
    for sid in order:
        r = deduped[sid]
        w.writerow([audit_id[sid], sid, final_of(sid), r["prelabel"], r["rule"],
                    r["arm"], r["source_group"], rows_per_key[key_of(sid)]])

dist = Counter(final_of(s) for s in drawn)
arm_dist = Counter(deduped[s]["arm"] for s in drawn)
covered = sum(rows_per_key[key_of(s)] for s in drawn)
with open(OUT / "sample_manifest.md", "w") as fh:
    fh.write("# Self-audit subsample — sampling manifest (AUTHOR-SIDE; contains label distribution)\n\n")
    fh.write(f"- Built by `scripts/build_self_audit_packet.py`, seed {SEED}.\n")
    fh.write("- Population: the 340 matched validation rows that retain accepted AI "
             "pre-labels (451 matched minus 111 author-produced/adjudicated: 87 divergence "
             "+ 30 blind, 6 in both), deduped to 301 distinct finding keys.\n")
    fh.write(f"- Drawn: {len(drawn)} distinct findings (allocation per rule proportional to the "
             f"deduped population, floor {FLOOR}, cap {CAP}; within a rule, split across "
             f"source groups proportionally). The draw covers {covered} of the 340 rows "
             "(39 findings appear twice in the retained set by the sample's design).\n")
    fh.write(f"- Draw by arm: {dict(arm_dist)}. Label distribution of the draw "
             f"(author-side only): {dict(dist)}.\n\n")
    fh.write("| Rule | Population (deduped) | Drawn |\n|---|---:|---:|\n")
    for rule in sorted(by_rule):
        fh.write(f"| {rule} | {len(by_rule[rule])} | {alloc[rule]} |\n")
    fh.write("\nScoring once labels are filled: `python3 scripts/score_self_audit.py`.\n"
             "The key (KEY_sealed.csv) stays out of git until the audit is scored;\n"
             "it is published with the replication package afterwards.\n")

absent = sorted({"DEPRECATED_API", "HOST_IPC", "HOST_NETWORK", "HOST_PID", "IMG_LATEST",
                 "IMG_NO_DIGEST", "IMG_UNTAGGED", "RBAC_CLUSTER_ADMIN_BINDING",
                 "RBAC_WILDCARD_RESOURCES", "RBAC_WILDCARD_VERBS", "REL_NO_LIVENESS_PROBE",
                 "REL_NO_READINESS_PROBE", "RES_NO_CPU_LIMIT", "RES_NO_MEM_LIMIT",
                 "RES_NO_REQUESTS", "SA_TOKEN_AUTOMOUNTED", "SECRET_COMMITTED",
                 "SECRET_LITERAL_ENV", "SEC_APE_NOT_DISABLED", "SEC_CAPABILITY_ADDED",
                 "SEC_DANGEROUS_CAPABILITY", "SEC_NO_SECCOMP", "SEC_PRIVILEGED",
                 "SEC_ROOT_NOT_PREVENTED", "SEC_RUN_AS_ROOT_EXPLICIT"} - set(by_rule))
print(f"population rows=340 deduped=301 drawn={len(drawn)} covering {covered} rows")
print("draw by arm:", dict(arm_dist), " draw label distribution (author-side):", dict(dist))
print("rules absent from the retained population:", absent)
print("allocation:", dict(sorted(alloc.items())))
