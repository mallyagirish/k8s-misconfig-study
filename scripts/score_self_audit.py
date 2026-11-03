#!/usr/bin/env python3
"""Score the single-author self-audit against the retained AI pre-labels.

Usage: python3 scripts/score_self_audit.py [path/to/filled_audit_sample.csv]

Reads the filled audit_sample.csv (audit_label column) and the sealed key
(results/self_audit/KEY_sealed.csv, author-side), and prints the overall
label-change rate with a 95% Wilson interval, change rates per rule family
(manuscript Section 3.2) and per rule, the direction of changes, and every
changed row with both labels. Rows the audit marked `unsure` are reported
separately and excluded from the change rate.

This measures annotation stability of the retained pre-labels under a blind
second pass by the same author. It is NOT inter-rater reliability and NOT
independent validation. Stdlib only.
"""
import csv
import math
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
    pairs.append((r["audit_label"].strip().upper(), k["final_label"].strip().upper(), r, k))

unsure = [p for p in pairs if p[0] == "UNSURE"]
decided = [p for p in pairs if p[0] != "UNSURE"]
changed = [p for p in decided if p[0] != p[1]]
print(f"returned = {len(pairs)}   audit-unsure = {len(unsure)}   decided = {len(decided)}")

lo, hi = wilson(len(changed), len(decided))
print(f"\nlabel-change rate = {len(changed)}/{len(decided)} = "
      f"{len(changed) / len(decided):.1%}  [95% Wilson CI {lo:.1%}, {hi:.1%}]")
print("direction: " + (", ".join(f"{a}->{b}: {n}" for (a, b), n in
      sorted(Counter((orig, aud) for aud, orig, _, _ in changed).items())) or "no changes"))

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
