# Research Round 35 — Model Family and Temporal Core Plan

## 1. Trigger

The causal study requires models whose exposure to evidence papers can be audited well enough that external context has a meaningful interpretation.

Official model cards provide useful cutoff anchors:

- Meta Llama 3.1: knowledge/pretraining data cutoff December 2023; pretrained and instruction-tuned 8B/70B/405B variants.
- Google Gemma 3: training-data knowledge cutoff August 2024; pretrained and instruction-tuned variants including 12B and 27B.

This supports a common clean evidence rule:

```text
first public date > 2024-08-31
```

for primary ICLR 2025 evidence.

## 2. Causal-core family requirements

A core family must have:

1. open/frozen weights or reproducibly fixed checkpoint;
2. documented knowledge/training cutoff;
3. sufficient context window for the evidence packet;
4. strong enough instruction following for valid research proposals;
5. locally reproducible decoding/configuration;
6. preferably both pretrained/base and instruction-tuned variants.

## 3. Recommended core families

### Family A — Llama 3.1

Primary advantages:

- Dec 2023 cutoff;
- 128K context;
- 8B / 70B scales;
- base + instruct pair;
- widely recognized ICLR baseline.

### Family B — Gemma 3

Primary advantages:

- Aug 2024 cutoff;
- 128K context for relevant variants;
- 12B / 27B practical sizes;
- pretrained + instruction-tuned variants;
- independent model family/training stack.

## 4. Pilot checkpoint plan

The engineering/variance pilot should prefer models small enough to run repeated stochastic generations while still producing coherent technical proposals.

Suggested starting pair, subject to infrastructure validation:

```text
Llama-3.1-8B-Instruct
Gemma-3-12B-IT
```

Purpose:

- validate formatting/output quality;
- estimate route-effect variance;
- test annotation pipeline;
- estimate packet and prompt noise;
- verify context length / throughput.

Do not promote pilot checkpoint behavior to a model-wide scientific claim.

## 5. Confirmatory scale plan

If resources allow, stronger confirmatory checkpoints should include:

```text
Llama-3.1-70B-Instruct
Gemma-3-27B-IT
```

with the pilot-scale models retained as scale/replication points rather than silently replaced.

A strong core grid would therefore be:

```text
Llama 3.1: 8B Instruct + 70B Instruct
Gemma 3:   12B IT      + 27B IT
```

This tests:

- family replication;
- within-family scale;
- whether response strength changes with capability.

Exact full grid depends on compute and output-validity results and must be frozen before confirmatory outcomes.

## 6. Base-vs-instruct subset

For Round 26's post-training extension, use matched base/pretrained versions on a subset:

```text
Llama-3.1-8B Base vs Instruct
Gemma-3-12B PT vs IT
```

If larger base models are feasible, add them only after the core paper is viable.

The base-vs-instruct comparison is secondary and conditional on valid output rates.

## 7. Why not use only frontier closed APIs?

Frontier APIs are valuable external-validity checks but weaker causal-core evidence because:

- training corpora/cutoffs may be incompletely documented;
- serving versions may change;
- sampling behavior can change over time;
- raw model access/attribution is limited.

Therefore:

```text
open audited models = causal core
frontier APIs        = external validity extension
```

## 8. Optional third open family

A third open family may be added later only if it offers a clear scientific gain.

Llama 4 has an Aug 2024 cutoff and could provide a more modern family/architecture point, but it is not necessary if Llama 3.1 + Gemma 3 already establish replication.

Avoid adding models merely to increase table width.

## 9. Temporal-clean evidence rule

For the strict shared causal subset:

```text
Evidence paper first-public date > 2024-08-31
AND
no discovered earlier public version before cutoff
```

Record:

- OpenReview first-public/submission date;
- arXiv v1 date;
- workshop/preprint earlier version if found;
- temporal status.

Unknown temporal status should not be silently treated as clean.

## 10. Seed chronology

Prefer ICLR 2026 focal problems first public after the model cutoff.

However, the key causal requirement is stronger for **evidence** than for the seed problem itself:

- evidence should plausibly be new external information;
- seed gives the problem to solve and can contain supplied background.

Still prefer post-cutoff seeds to minimize focal-paper memorization/leakage.

## 11. Contamination diagnostics

Do not ask models "have you seen this paper?" as primary evidence.

Use:

- documented cutoff;
- public-date audit;
- focal method leakage controls;
- masked-title/method identification probes only as exploratory diagnostics;
- separate analysis for any temporally ambiguous evidence.

## 12. Decoding policy

Within each checkpoint, freeze before confirmatory runs:

- temperature;
- top-p;
- max new tokens;
- repetition/penalty settings;
- system/user prompt template;
- chat template/version;
- seed handling if API/framework supports it.

Use stochastic decoding because the object is a route distribution, not one deterministic answer.

Do not compare model families at different arbitrary temperatures as primary evidence.

## 13. Model output validity gate

Before scaling a checkpoint, require reasonable:

- valid-output rate;
- seed relevance;
- proposal coherence;
- completion length stability.

If a small model produces mostly shallow or invalid proposals, do not compensate by relaxing the rubric. Replace/drop the checkpoint before confirmatory freeze and document why.

## 14. Scale-dependent hypotheses are secondary

Possible but not assumed:

- larger models use evidence more effectively;
- larger models have stronger baseline research-route preferences;
- larger models are more or less steerable.

Do not make scale the main paper unless a clean within-family regularity emerges.

## 15. Decision

**CORE MODEL PLAN: LLAMA 3.1 + GEMMA 3, OPEN/AUDITABLE FIRST.**

Use small/mid checkpoints for engineering pilot and larger checkpoints for confirmatory replication if infrastructure supports them. Preserve closed frontier models for later external validity, not causal identification.