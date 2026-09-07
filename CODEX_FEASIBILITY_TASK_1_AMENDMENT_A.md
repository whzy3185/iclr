# Codex Feasibility Task 1 — Amendment A: External Contribution-Family Audit

> Applies to: `CODEX_FEASIBILITY_TASK_1.md`
> Status: PRE-OUTCOME SOURCE-ONLY AMENDMENT
> Scientific generation remains FORBIDDEN.

## Trigger

Research Round 13 identified an independently developed research-contribution taxonomy from Pramanick et al., ACL 2025, that can reduce dependence on our custom six-way route labels.

Source:
https://aclanthology.org/2025.acl-long.1224/

Dataset:
https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/4678

## Required additional source annotation

For every source paper receiving a provisional fine route label, also record a coarse contribution family:

```text
ARTIFACT
KNOWLEDGE
BOTH
UNCLEAR
```

Adaptation principle:

- `ARTIFACT`: central contribution creates a new method/model, dataset/resource, task/benchmark, or comparable research artifact;
- `KNOWLEDGE`: central contribution primarily produces new understanding/analysis/measurement about an existing object, method, dataset, task, phenomenon, mechanism, or behavior;
- `BOTH`: both are genuinely central and cannot be reduced to one;
- `UNCLEAR`: insufficient or ambiguous evidence.

Do not force the ACL paper's NLP-specific subtypes onto all ICLR topics.

## Audit requirement

Add to the human audit packet:

- `coarse_contribution_family_provisional`
- `fine_route_label_provisional`
- source abstract/text excerpt
- confidence

Report separately:

- coarse-family distribution;
- fine-route distribution;
- ambiguity rate at each level;
- human/parser agreement when available;
- relationship between coarse and fine labels.

## Lexical shortcut diagnostic

Measure whether simple lexical features can predict:

1. coarse contribution family;
2. fine route label.

Do not treat high lexical predictability as invalidating by itself, but flag it as a priming risk requiring content-normalized robustness later.

## Feasibility result addition

`FEASIBILITY_RESULT.md` must additionally answer:

> Is the coarse Artifact/Knowledge/Both/Unclear distinction materially easier to audit than the fine route taxonomy on ICLR source papers?

No scientific generation may be run under this amendment.
