#!/usr/bin/env python3
"""Score the single-author self-audit against the retained AI pre-labels.

Usage: python3 scripts/score_self_audit.py [path/to/filled_audit_sample.csv]

Reads the filled audit_sample.csv (audit_label column) and the sealed key
(results/self_audit/KEY_sealed.csv, author-side), and prints the overall
label-change rate with a 95% Wilson interval, a design-weighted estimate of
the change rate over the retained population (the draw was stratified by
rule, so the unweighted rate describes the sample, not the population),
change rates per rule family (manuscript Section 3.2) and per rule, the
direction of changes, and every changed row with both labels. Rows the audit
marked `unsure` are reported separately and excluded from the change rate.

This measures annotation stability of the retained pre-labels under a blind
second pass by the same author. It is NOT inter-rater reliability and NOT
independent validation. Stdlib only.
"""
import csv
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "results" / "self_audit" / "packet" / "audit_sample.csv"
key = {r["audit_id"]: r for r in csv.DictReader(open(ROOT / "results" / "self_audit" / "KEY_sealed.csv"))}

FAMILY = {}
for fam, rules in {
    "images": ["IMG_UNTAGGED", "IMG_LATEST", "IMG_NO_DIGEST"],
    "resources": ["RES_NO_CPU_LIMIT", "RES_NO_MEM_LIMIT", "RES_NO_REQUESTS"],
    "reliability": ["REL_NO_LIVENESS_PROBE", "REL_NO_READINESS_PROBE"],
    "security context": ["SEC_PRIVILEGED", "SEC_ROOT_NOT_PREVENTED", "SEC_RUN_AS_ROOT_EXPLICIT",
                         "SEC_APE_NOT_DISABLED", "SEC_CAPABILITY_ADDED",
                         "SEC_DANGEROUS_CAPABILITY", "SEC_NO_SECCOMP"],
    "host access": ["HOST_NETWORK", "HOST_PID", "HOST_IPC", "SA_TOKEN_AUTOMOUNTED"],
    "RBAC and secrets": ["RBAC_WILDCARD_VERBS", "RBAC_WILDCARD_RESOURCES",
                         "RBAC_CLUSTER_ADMIN_BINDING", "SECRET_COMMITTED", "SECRET_LITERAL_ENV"],
    "API currency": ["DEPRECATED_API"],
}.items():
    for r in rules:
        FAMILY[r] = fam


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


rows = [r for r in csv.DictReader(open(path)) if r.get("audit_label", "").strip()]
if not rows:
    sys.exit("No audit labels filled in yet.")

pairs = []  # (audit_label, original_label, csv row, key row)
for r in rows:
    k = key[r["audit_id"]]
    pairs.append((r["audit_label"].strip().upper(), k["original_label"].strip().upper(), r, k))

unsure = [p for p in pairs if p[0] == "UNSURE"]
decided = [p for p in pairs if p[0] != "UNSURE"]
changed = [p for p in decided if p[0] != p[1]]
print(f"returned = {len(pairs)}   audit-unsure = {len(unsure)}   decided = {len(decided)}")

lo, hi = wilson(len(changed), len(decided))
print(f"\nlabel-change rate = {len(changed)}/{len(decided)} = "
      f"{len(changed) / len(decided):.1%}  [95% Wilson CI {lo:.1%}, {hi:.1%}]")
print("direction: " + (", ".join(f"{a}->{b}: {n}" for (a, b), n in
      sorted(Counter((orig, aud) for aud, orig, _, _ in changed).items())) or "no changes"))

# --- design-weighted estimate over the retained population -------------------
# The unweighted rate above describes the 94 decided findings as drawn. The
# draw was stratified, though: allocation was fixed per rule in proportion to
# the rule's share of the 301 distinct retained findings (floor 2, cap 14 --
# SEC_PRIVILEGED was capped at 14 of its 72 findings), so sampling fractions
# differ by rule and the unweighted rate is not the population estimate. The
# estimate below reweights at the rule level: the level at which allocation
# was set, and the finest level at which every stratum but one has decided
# rows. (Within a rule the allocation was split across source groups in
# proportion to group size -- self-weighting up to integer rounding -- and 11
# rule x source-group cells of one finding received no draw at all, so the
# finer grid cannot carry the estimate; it is reported as a sensitivity.)
# Stratum populations are reconstructed exactly as in
# scripts/build_self_audit_packet.py. The 16 self_audit_correction rows the
# recompute later appended to verification_divergence.csv postdate the draw
# and are excluded, so the frame is the one the packet was drawn from.
RES = ROOT / "results"
_pre = {r["sample_id"]: r for r in csv.DictReader(open(RES / "labeling_sample_v2_prelabelled.csv"))}
_div = {r["sample_id"]: r["recommended_v3"] for r in csv.DictReader(open(RES / "verification_divergence.csv"))
        if r["divergence_class"] != "self_audit_correction"}
_blind = {r["sample_id"] for r in csv.DictReader(open(RES / "kappa_subset" / "blind_sample.csv"))}
_findings = set()
for _line in open(RES / "findings_v3.jsonl"):
    _f = json.loads(_line)
    _findings.add((_f["arm"], _f["source"], _f["kind"], _f["name"], _f["container"] or "", _f["rule"]))
_matched = {}
for _sid, _r in _pre.items():
    if (_r["arm"], _r["source_file"], _r["kind"], _r["name"], _r["container"], _r["rule"]) in _findings:
        _matched[_sid] = _r
_author = (set(_div) | _blind) & set(_matched)
_pop_rows = {_sid: _matched[_sid] for _sid in _matched if _sid not in _author}
_by_key = {}
for _sid in sorted(_pop_rows):
    _r = _pop_rows[_sid]
    _by_key.setdefault((_r["source_file"], _r["kind"], _r["name"], _r["container"], _r["rule"]), _sid)
assert (len(_matched), len(_pop_rows), len(_by_key)) == (451, 340, 301), "audit frame drifted"
_deduped = [_pop_rows[_sid] for _sid in _by_key.values()]

pop_rule = Counter(r["rule"] for r in _deduped)
tab_rule = defaultdict(lambda: [0, 0, 0])  # rule -> [decided, changed, unsure]
for aud, orig, r, _k in pairs:
    t = tab_rule[r["rule"]]
    if aud == "UNSURE":
        t[2] += 1
    else:
        t[0] += 1
        if aud != orig:
            t[1] += 1
dec_rules = {ru: t for ru, t in tab_rule.items() if t[0] > 0}
cov_dec = sum(pop_rule[ru] for ru in dec_rules)
w_est = sum(pop_rule[ru] * t[1] / t[0] for ru, t in dec_rules.items()) / cov_dec

_rng = random.Random(20261104)  # bootstrap seed, documented in audit_results.md
_strata = [(pop_rule[ru], [1] * t[1] + [0] * (t[0] - t[1])) for ru, t in sorted(dec_rules.items())]
_reps = []
for _ in range(2000):
    _num = 0.0
    for _N, _vals in _strata:
        _n = len(_vals)
        _num += _N * sum(_vals[_rng.randrange(_n)] for _ in range(_n)) / _n
    _reps.append(_num / cov_dec)
_reps.sort()
b_lo, b_hi = _reps[int(0.025 * 2000)], _reps[int(0.975 * 2000) - 1]

samp_rules = {ru: t for ru, t in tab_rule.items() if t[0] + t[2] > 0}
cov_samp = sum(pop_rule[ru] for ru in samp_rules)
wb_lo = sum(pop_rule[ru] * t[1] / (t[0] + t[2]) for ru, t in samp_rules.items()) / cov_samp
wb_hi = sum(pop_rule[ru] * (t[1] + t[2]) / (t[0] + t[2]) for ru, t in samp_rules.items()) / cov_samp
uw_lo = len(changed) / len(pairs)
uw_hi = (len(changed) + len(unsure)) / len(pairs)

print("\ndesign-weighted estimate (stratified by rule; the unweighted rate above")
print("describes the sample as drawn, this estimates the retained population):")
print(f"  population-weighted change rate = {w_est:.1%}  [stratified bootstrap 95% CI "
      f"{b_lo:.1%}, {b_hi:.1%}; 2,000 replicates, seed 20261104]")
print(f"  coverage: strata with decided rows hold {cov_dec} of the 301 distinct retained findings")
_no_dec = sorted(set(pop_rule) - set(dec_rules))
if _no_dec:
    print(f"  no decided rows: {', '.join(_no_dec)} "
          f"({sum(pop_rule[ru] for ru in _no_dec)} findings; all their draws were unsure)")
print(f"  unsure sensitivity: weighted [{wb_lo:.1%}, {wb_hi:.1%}] if all {len(unsure)} unsure "
      f"count as unchanged vs changed; unweighted [{uw_lo:.1%}, {uw_hi:.1%}]")

# Sensitivity at the finer rule x source-group grid (reduced coverage, see above).
pop_grp = Counter((r["rule"], r["source_group"]) for r in _deduped)
tab_grp = defaultdict(lambda: [0, 0, 0])
for aud, orig, r, _k in pairs:
    t = tab_grp[(r["rule"], r["source_group"])]
    if aud == "UNSURE":
        t[2] += 1
    else:
        t[0] += 1
        if aud != orig:
            t[1] += 1
dec_grp = {s: t for s, t in tab_grp.items() if t[0] > 0}
cov_grp = sum(pop_grp[s] for s in dec_grp)
w_grp = sum(pop_grp[s] * t[1] / t[0] for s, t in dec_grp.items()) / cov_grp
print(f"  sensitivity, rule x source-group strata: {w_grp:.1%} over {cov_grp} of 301 findings")

for name, group_of in (("per rule family", lambda r: FAMILY[r["rule"]]),
                       ("per rule", lambda r: r["rule"])):
    tab = defaultdict(lambda: [0, 0])
    for aud, orig, r, _ in decided:
        g = group_of(r)
        tab[g][1] += 1
        if aud != orig:
            tab[g][0] += 1
    print(f"\n{name} (decided rows):")
    for g in sorted(tab):
        c, t = tab[g]
        glo, ghi = wilson(c, t)
        print(f"  {g:<28} {c}/{t} changed  [{glo:.0%}, {ghi:.0%}]")

print("\nchanged rows (original -> audit):")
for aud, orig, r, k in sorted(changed, key=lambda p: p[2]["audit_id"]):
    print(f"  {r['audit_id']} ({k['sample_id']}) {r['rule']:<28} {orig} -> {aud} "
          f"reason={r.get('audit_reason', '')} notes={r.get('audit_notes', '')} :: {r['source_file']}")

covered = sum(int(k["rows_covered"]) for _, _, _, k in decided)
print(f"\ndecided rows stand for {covered} of the 340 retained sample rows "
      f"(duplicate findings counted once in this audit).")
