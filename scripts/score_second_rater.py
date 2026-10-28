#!/usr/bin/env python3
"""Score the independent second-rater packet against the author-verified labels.

Usage: python3 scripts/score_second_rater.py [path/to/returned_blind_sample.csv]

Reads the returned blind_sample.csv (blind_label filled in) and the sealed
key (results/second_rater/KEY_sealed.csv, author-side), and prints raw
agreement, Cohen's kappa (three-class and binary), the confusion matrix,
per-rule agreement, and every disagreement for adjudication. Stdlib only.
"""
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "results" / "second_rater" / "packet" / "blind_sample.csv"
key = {r["blind_id"]: r for r in csv.DictReader(open(ROOT / "results" / "second_rater" / "KEY_sealed.csv"))}

rows = [r for r in csv.DictReader(open(path)) if r.get("blind_label", "").strip()]
if not rows:
    sys.exit("No blind labels filled in yet.")

pairs = []  # (rater, author, row)
for r in rows:
    k = key[r["blind_id"]]
    pairs.append((r["blind_label"].strip().upper(), k["final_label"].strip().upper(), r))

unsure = [p for p in pairs if p[0] == "UNSURE"]
decided = [p for p in pairs if p[0] != "UNSURE"]
print(f"returned = {len(pairs)}   rater-unsure = {len(unsure)}   decided = {len(decided)}")


def kappa(subset, fold=None):
    f = fold or (lambda x: x)
    n = len(subset)
    agree = sum(1 for a, b, _ in subset if f(a) == f(b))
    labels = sorted({f(a) for a, _, _ in subset} | {f(b) for _, b, _ in subset})
    ca, cb = Counter(f(a) for a, _, _ in subset), Counter(f(b) for _, b, _ in subset)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in labels)
    po = agree / n
    k = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return agree, n, po, k, labels


agree, n, po, k3, labels = kappa(decided)
print(f"\nthree-class (TP / FP / TP-HARDENING): agreement = {agree}/{n} = {po:.1%}   Cohen's kappa = {k3:.3f}")
agree2, _, po2, k2, _ = kappa(decided, fold=lambda x: "TP" if x.startswith("TP") else x)
print(f"binary (TP-hardening counted as TP):  agreement = {agree2}/{n} = {po2:.1%}   Cohen's kappa = {k2:.3f}")

print("\nconfusion (rater rows x author cols):")
print("        " + "".join(f"{l:>14}" for l in labels))
for l in labels:
    print(f"{l:>8}" + "".join(f"{sum(1 for a, b, _ in decided if a == l and b == m):>14}" for m in labels))

by_rule = defaultdict(lambda: [0, 0])
for a, b, r in decided:
    by_rule[r["rule"]][1] += 1
    if a == b:
        by_rule[r["rule"]][0] += 1
print("\nper-rule agreement (decided rows):")
for rule in sorted(by_rule):
    a, t = by_rule[rule]
    print(f"  {rule:<28} {a}/{t}")

print("\ndisagreements (for adjudication):")
for a, b, r in decided:
    if a != b:
        print(f"  {r['blind_id']} {r['rule']:<28} rater={a} author={b} "
              f"reason={r.get('blind_reason', '')} notes={r.get('blind_notes', '')} :: {r['source_file']}")
