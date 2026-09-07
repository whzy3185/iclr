# Research Round 17 — Target Population, Sampling Frame, and Generalization Freeze

## 1. Trigger

Rounds 15–16 make the causal contrast increasingly clean. A new risk now becomes dominant:

> We may discover a strong effect only on a small set of seeds where two research routes happen to be easy to construct, then accidentally write conclusions as if they applied to all ICLR research questions.

This round freezes the inferential population and sampling logic before any model outcomes exist.

---

## 2. Core principle

The treatment is only well-defined when a seed question admits at least two **scientifically plausible, source-supported, relevance-matchable** research routes.

Therefore the primary target population cannot honestly be:

> all ICLR papers / all scientific questions.

The defensible target is narrower:

> **ICLR-style research questions for which the contemporaneous literature supports at least two distinct, relevance-matched scientific routes under the predeclared route roster.**

Call this the **multi-route support population**.

This restriction must appear in methods, abstract-level caveats if material, and limitations.

---

## 3. Candidate seed sampling frame

Do not hand-pick seeds because they have obvious Build-vs-Diagnose stories.

Construct a source-defined candidate frame from accepted ICLR 2026 papers satisfying temporal and masking criteria.

Recommended procedure:

1. define eligible ICLR areas/subfields using official metadata or a frozen clustering rule;
2. sample/retain candidate focal papers using a predeclared stratified rule;
3. derive method-masked research questions without inspecting any model output;
4. retain every candidate seed in `seed_manifest.json`, including failures;
5. apply route-support and matching gates mechanically.

### Preferred breadth

At minimum include multiple ML research regimes rather than only one narrow LLM topic. Candidate strata could include:

- language models / retrieval / agents;
- training / optimization / post-training;
- representation / architecture / generative modeling;
- robustness / evaluation / reliability.

Exact strata should be frozen from the actual ICLR metadata/corpus before treatment generation.

Do not force a stratum if source-only feasibility shows the route construct is incoherent there.

---

## 4. Seed statuses

Every source-defined candidate seed receives exactly one pre-outcome status such as:

```text
ELIGIBLE_MULTI_ROUTE
MASKING_FAILURE
QUESTION_NOT_OPEN_ENDED
TEMPORAL_CLEANLINESS_FAILURE
INSUFFICIENT_RELEVANT_EVIDENCE
INSUFFICIENT_ROUTE_COVERAGE
MATCHING_FAILURE
ROUTE_AMBIGUITY
DUPLICATE_OR_LEAKAGE
```

No candidate disappears from reporting.

### Required headline number

Report:

```text
eligibility_rate = ELIGIBLE_MULTI_ROUTE / all source-defined candidate seeds
```

with counts by stratum and route pair.

This tells reviewers how broad or selective the experiment really is.

---

## 5. Route-pair population

A single seed may support multiple predeclared route contrasts.

Define a **seed-route block**:

```text
block = (seed_id, route_A, route_B)
```

If multiple contrasts from the frozen roster pass the gate, include all of them subject to any predeclared compute cap.

Do not select the pair with:

- greatest no-context imbalance;
- strongest pilot response;
- cleanest-looking eventual result.

### Primary inferential unit

The conceptual replication unit is the **seed-route block**, not an individual generation.

Repeated LLM samples estimate the conditional distribution inside a block; they do not create thousands of independent scientific questions.

Statistical uncertainty must respect this hierarchy.

---

## 6. Generation counts are Monte Carlo precision, not sample size of science

Suppose a block has 100 generations at each alpha. Those 500 responses provide precise estimation of that block's model distribution, but they are not 500 independent scientific units.

Primary uncertainty should therefore use one or more of:

- hierarchical random effects over seed / route pair / model;
- seed-route-block bootstrap;
- cluster-robust uncertainty at the block level;
- posterior predictive intervals for new eligible blocks.

Avoid treating every generation as an i.i.d. observation when making broad claims.

---

## 7. Primary generalization targets

Freeze three nested targets.

### G1 — Within-block causal response

Narrowest and strongest:

> For a fixed eligible seed-route pair and frozen model, changing matched evidence composition changes the route-choice distribution.

This is the direct randomized/controlled claim.

### G2 — Across eligible ICLR seed-route blocks

Primary paper-level generalization:

> Evidence-conditioned route response is systematic across the predeclared multi-route support population, not confined to one hand-picked seed.

Requires multiple seeds, route pairs, subfields, and models.

### G3 — Natural-RAG predictive generalization

Held-out external validity:

> A response model learned from controlled packets improves prediction of the same LLM's route choice under ordinary retrieval on new eligible seeds.

This bridges the artificial intervention to realistic RAG.

### Explicitly not claimed

Do not infer directly that:

- human scientists change research direction in the same way;
- the scientific field becomes narrower;
- all ICLR questions are steerable;
- the supplied route is better or more innovative;
- future publication choices are predicted.

---

## 8. Eligibility-selection analysis

Eligibility itself may be scientifically informative.

For example, certain subfields may have many Build papers but few Diagnose/Explain papers meeting relevance gates.

Report source-only differences between eligible and ineligible seeds using pre-treatment features:

- subfield;
- corpus size;
- retrieval concentration;
- number of supported routes;
- relevance distribution;
- temporal density.

Purpose:

- characterize where the treatment is defined;
- prevent hidden selection bias;
- avoid pretending the eligible subset is representative when it is not.

Do **not** turn this source-only analysis into a post-hoc story about model behavior.

---

## 9. Route contrast weighting

If some route pair dominates the feasible set, pooled effects can be misleading.

Primary reporting should include:

1. route-pair-specific estimates;
2. macro-average across predeclared route contrasts;
3. block-weighted aggregate as secondary;
4. model-specific estimates before pooled model effects.

This prevents a large BUILD↔DIAGNOSE subset from hiding null or opposite effects elsewhere.

---

## 10. Model generalization

At least two distinct model families are required for the core empirical claim.

Prefer temporally auditable open models for causal validity.

Frontier closed models may be added as external-validity extensions but should not rescue a result that fails on the clean core.

### Same-packet cross-model contrast

The strongest design uses identical frozen evidence packets for different models.

This enables:

```text
same seed
same route pair
same evidence packet
same alpha
but different baseline route propensity
```

If response differences track independently measured baseline propensity, the interaction is substantially more compelling than a between-study comparison.

---

## 11. Quality / plausibility population

Both routes must be genuinely defensible answers to the seed.

A route cannot enter the treatment population merely because enough papers carry that label.

Pre-treatment/source-only gate should ask:

> Could a competent ML researcher reasonably pursue this route for the masked seed question based on the supplied literature?

A human audit on a stratified subset is preferred.

If one route is systematically judged less plausible, the treatment is not an equivalent scientific-choice contrast and should fail the gate.

---

## 12. Relationship to recent forecasting work

IdeaForecastBench (EMNLP 2026) and PreScience already study future scientific contributions and show that literature representation affects generated forecasts / synthetic science.

Our target remains different:

- no human-future ground truth is needed;
- route A/B are both valid possible choices;
- the outcome is the model's conditional choice distribution;
- natural-RAG validation predicts model behavior, not future human publications.

This distinction should be explicit to avoid being reviewed as an incremental scientific-forecasting benchmark.

---

## 13. Minimum breadth gate before scientific generation

Source-only feasibility should not merely return `some matches exist`.

Before authorizing generation, require a minimum viable treatment population such as:

- >= 3 scientific strata/subfields with eligible seeds;
- >= 3 predeclared route contrasts represented overall;
- no single seed contributes a disproportionate share of all blocks;
- enough matched blocks for at least two model families to receive identical packets;
- acceptable relevance/plausibility balance.

Exact numeric thresholds should be frozen after source-only feasibility reveals realistic corpus capacity, but **before** any model generation.

This is one of the legitimate places where source-only Codex results should inform design because no treatment outcome has been observed.

---

## 14. Kill / pivot implications

If source-only feasibility finds that only a tiny, narrow class of seeds is matchable, options are:

1. narrow the paper claim explicitly to that setting;
2. redesign route definitions using an externally grounded coarser contrast;
3. expand the evidence corpus while preserving temporal cleanliness;
4. KILL if the construct only works on hand-picked anecdotes.

Do not weaken matching or cherry-pick seeds to preserve the original broad story.

---

## 15. Codex status

No source-only feasibility result is present in the repository at this round.

Codex remains authorized only for the already-scoped pre-treatment feasibility task. No P0 model generation is authorized.

---

## 16. Decision

**KEEP / CONDITIONAL GO.**

The paper's primary inferential population is now explicitly restricted to the **source-defined, multi-route-support ICLR seed population**.

The main unit of scientific replication is the **seed-route block**, while repeated generations serve to estimate each block's conditional response distribution.

This restriction makes the eventual claim narrower but substantially more defensible.
