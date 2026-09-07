# Research Round 51 — Redesign F0 Gates Around ICLR-Style Experimental Rigor

## Trigger

The previous F0 execution prompt used hard source-feasibility thresholds such as `>=30 unique seeds with >=8 matched slots`, fixed subfield counts, and rigid raw calipers. These are operationally clear but scientifically under-justified. They risk turning an engineering feasibility audit into a pseudo-power calculation before any construct/variance pilot exists.

The user requested that hard gates be realistic and that experimental design follow strong ICLR practice.

## ICLR experimental-design references

### BiasBusters — ICLR 2026

Design lesson: construct controlled alternatives that are meaningfully equivalent, isolate exposed factors, and replicate across models. The scientific strength comes from control of the manipulated variable and robustness, not from a magic sample-count threshold.

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2026/hash/a79875cc0d046ce7ce65f03f3affaa9e-Abstract-Conference.html

### Spectrum Tuning — ICLR 2026

Design lesson: evaluate a distributional property across multiple model families/tasks and held-out settings. Breadth/generalization matters, but task count is chosen to support the scientific question rather than serving as a universal acceptance threshold.

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html

### Mixing Mechanisms — ICLR 2026

Design lesson: controlled experiments identify a behavioral regularity; a compact explanatory/causal model is then tested on more natural held-out settings. This supports our controlled-mixture -> natural-RAG prediction paper shape.

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2026/hash/2eeff35664016c7f0f8aa704f0d9a83e-Abstract-Conference.html

### Does Writing with Language Models Reduce Content Diversity? — ICLR 2024

Design lesson: controlled treatment conditions plus mechanism attribution can support an ICLR behavioral finding without a new architecture.

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2024/hash/02dec8877fb7c6aa9a79f81661baca7c-Abstract-Conference.html

### ICLR 2027 reviewer guide

The reviewer guide asks whether the paper has a specific question, is well situated in the literature, rigorously supports its claims, and contributes significant new knowledge. It does not prescribe fixed benchmark/task/sample counts or require SOTA.

Primary source:
https://iclr.cc/Conferences/2027/ReviewerGuidelines

## Main correction

F0 is **not a full-paper sample-size gate**.

F0 asks only:

> Is there enough clean, auditable source structure to justify a construct/variance pilot?

Therefore F0 should not decide that `30 seeds` is scientifically sufficient or that `29 seeds` is insufficient.

Full confirmatory sample size will be frozen only after a construct/variance pilot estimates:

- annotation reliability;
- within-condition route-score variance;
- between-seed heterogeneity;
- block attrition/equipoise rate;
- packet-realization variance.

Then full N should be chosen by a precision target / predeclared maximum budget, not by significance peeking.

## Revised F0 decision categories

### READY_FOR_F1_CONSTRUCT_PILOT

Engineering/source evidence is sufficient to build a meaningful construct pilot.

Operational minimum panel:

- at least 12 unique seeds with at least one route pair supporting `k>=6` under the primary balance rule;
- at least 8 unique seeds among them support `k>=8`;
- at least 2 of R1-R4 are represented by at least 3 seeds each;
- route-clear filtering and temporal cleaning are explicitly reported;
- no obvious systematic relevance imbalance remains under the primary balance diagnostics.

These counts are **pilot-panel engineering minima**, not publication thresholds.

Subfield count is reported but is not a hard F0 gate.

### LIMITED_PILOT_ONLY

- 6–11 unique seeds support `k>=6`, or
- >=12 seeds exist but almost all usable blocks come from one route contrast / one narrow subfield.

This still permits a small construct pilot to learn whether the phenomenon/measurement is worth redesigning, but it does not authorize a broad confirmatory claim.

### REDESIGN_REQUIRED

- fewer than 6 unique seeds support a clean `k>=6` block under the primary matching specification; or
- usable blocks require obviously low-relevance documents; or
- route purity / seed neutrality / temporal cleanliness is too poor to interpret the intervention.

This means redesign corpus/treatment or kill the topic before scientific generation.

### ENGINEERING_BLOCKED

Source/API/model-download/tooling failure prevents a meaningful feasibility conclusion. Do not call this scientific NOT_FEASIBLE.

## Revised matching philosophy

The previous STRICT/BASE/RELAXED raw calipers are demoted from decision authority because absolute values such as `topic cosine <= .20` or `date <=365 days` have no universal scientific interpretation.

### Primary candidate relevance floor

For each seed:

- retrieve/rerank the top 200 temporal-clean candidates;
- primary matching candidates are the top 100 after reranking (dense top 100 if no reranker);
- report sensitivity at top 50 and top 150.

This prevents route matching from manufacturing alternatives from clearly weak/off-topic papers.

### Primary matched-slot procedure

1. Standardize scalar matching covariates within the seed candidate pool:
   - dense relevance;
   - reranker relevance if available;
   - log token length;
   - public-date position/age.
2. Keep topic embedding distance as an explicit pairwise component.
3. Use deterministic minimum-cost bipartite matching without replacement.
4. Matching cost is frozen before outcome generation.
5. Do not tune weights using future scientific effects.

### Block-level balance diagnostics

A block is `PRIMARY_BALANCED` when:

- all selected A/B papers satisfy the primary relevance floor;
- absolute standardized mean differences between all-A and all-B packet endpoints are <=0.25 for dense relevance, reranker relevance (if present), log token length, and temporal position;
- no scalar balance dimension exceeds 0.50 absolute SMD;
- optimal matching mean cost is better than the 25th percentile of a deterministic null distribution from random cross-route pairings for that same candidate bank;
- topic-distance distribution is reported and manually auditable; no universal raw cosine threshold is treated as scientific truth.

`0.25`/`0.50` are balance diagnostics borrowed from standard matching logic, not claims that nature has a threshold. All continuous diagnostics must be reported.

### Sensitivity

Report:

- top-50 / top-100 / top-150 relevance floors;
- route-purity thresholds 0.60 / 0.70 / 0.80;
- alternative reasonable matching cost weighting chosen without outcomes.

Do not choose the version that gives the best later treatment result.

## Equipoise is more important than a numerical matching score

Following the controlled-alternative logic of BiasBusters, the core scientific requirement is that Route A and Route B are both credible responses to the same seed.

F1 human audit therefore remains mandatory before any confirmatory treatment run.

A matched block can pass F0 source engineering but still fail F1 equipoise.

## Full-study breadth should be precision-driven

After F1/P0 construct pilot:

1. freeze primary ordinal route score and human annotation protocol;
2. estimate between-seed and packet-realization variance without outcome-dependent route selection;
3. choose full N to achieve a predeclared confidence-interval precision for the average seed-level treatment contrast and baseline-interaction estimate;
4. stratify reporting across model families / route contrasts / subfields;
5. do not stop once p<.05.

Target breadth such as 30–40 seeds remains a planning aspiration, not an F0 hard gate.

## Revised project interpretation

The experimental standard should be:

> controlled alternatives + auditable construct validity + independent replications + uncertainty + held-out prediction

not:

> pass arbitrary N/caliper thresholds.

## Decision

MODIFY.

The scientific topic remains active. F0 engineering should proceed using the revised gate policy in `CODEX_F0_EXECUTION_PROMPT_V2.md`.
