# Self-audit packet — re-labeling the retained AI pre-labels, blind

**What this is.** In the study's validation pass, 340 of the 451 matched
sample rows kept their AI pre-labels under the protocol's blank-equals-accept
rule; the other 111 rows carry labels the author produced blind (30) or
adjudicated individually (87) — see Section 3.4 of the manuscript and
`results/precision_provisional.md`. This packet is a second look at the
retained set: 100 of its 301 distinct findings, drawn at random (seed
20261103, stratified by rule and source group), to be re-labeled by the
author from the evidence alone — the original pre-label and the AI's reason
are not shown anywhere in this packet. The scorer then reports how often the
second-pass label differs from the original.

**What it is not.** This is a single-author annotation-stability audit: same
person, same frozen protocol, second pass, blind to the first answer. It is
**not** inter-rater reliability (there is no second rater) and **not**
independent validation. A low change rate would show the retained labels are
stable under re-judgment by their own standard; it cannot show they are
right, and it will be reported as exactly that, no more.

## Contents

- `protocol_for_audit.md` — the frozen v3 protocol in labeling form (a
  verbatim copy of the second-rater packet's protocol edition; canonical
  sources: `results/labeling_protocol_v3.md` and
  `results/labeling_protocol_v3_addendum.md`). Every decision rule you need
  is in it.
- `audit_sample.csv` — the 100 rows to label.
- `packets.md` — one evidence packet per row, in the same order as the CSV
  (`packets.jsonl` is the same content in machine-readable form).

## How to label

1. Read `protocol_for_audit.md` first (~10 minutes).
2. For each row: find its packet, apply the protocol's test for that rule,
   and fill in three columns of `audit_sample.csv`:
   - `audit_label`: `TP`, `FP`, `TP-hardening`, or `unsure`
   - `audit_reason`: for FPs, the reason code from the protocol
     (`infra-need`, `placeholder`, `fixture`, `standard-practice`,
     `parser-artifact`, `not-exploitable`); leave blank otherwise
   - `audit_notes`: anything that made the row hard, in a few words
3. Work from the packet and the protocol alone. If a row still can't be
   decided, mark it `unsure` rather than guessing.

**Stay blind until the sheet is complete.** Do not open
`results/labeling_sample_v2_prelabelled.csv`, `results/prelabels.json`,
`results/verification_divergence.csv`, `results/self_audit/sample_manifest.md`,
or `results/self_audit/KEY_sealed.csv` before finishing. Looking first turns
this back into a verification pass and destroys the measurement — the same
warning the kappa subset carried.

Budget: ~100 rows × 1–2 min ≈ 2–3 hours; the sheet can be filled across
sittings.

## Scoring

When all 100 rows are filled:

```
python3 scripts/score_self_audit.py
```

It prints the overall label-change rate with a 95% Wilson interval, the
change rate per rule family (and per rule), the direction of the changes,
and every changed row with both labels — the input for deciding whether any
change is a correction to adopt or a second-pass error. Nothing is applied
to the study's labels automatically.
