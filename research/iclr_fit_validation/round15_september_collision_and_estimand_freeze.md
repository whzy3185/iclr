# Research Round 15 — September Collision Scan and Estimand Freeze

## 1. Trigger

Continue ICLR-specific validation after Round 14. This round asks two questions:

1. Has September 2026 work closed the remaining novelty gap?
2. What exact statistical/behavioral object should be frozen before source-only feasibility and later model generation?

The goal is to remove overloaded language such as `prior`, `steerability`, and `idea diversity` from the primary estimand unless the data directly support those interpretations.

---

## 2. New evidence

### 2.1 IdeaForecastBench — EMNLP 2026

*Can Large Language Models Forecast What Researchers Study Next?* (arXiv:2609.00747; accepted EMNLP 2026) evaluates research-idea forecasting over 624 rolling episodes and 52 topics. It varies how historical literature is represented/compressed and scores generated ideas against later papers.

Sources:

- https://arxiv.org/abs/2609.00747
- https://fenghaili.com/papers/idea-forecast-bench/

Implication:

- future-paper prediction / scientific forecasting is now a crowded neighboring task;
- our held-out natural-RAG experiment must **not** be framed as forecasting what researchers will do next;
- our held-out target is the LLM's own evidence-conditioned research-choice distribution under natural retrieval.

### 2.2 PreScience — 2026

PreScience decomposes scientific forecasting into prior-work selection, contribution generation, collaborator prediction, and impact prediction. Its end-to-end synthetic scientific corpus is less diverse and less novel than matched human-authored research.

Source:

- https://arxiv.org/abs/2602.20459

Implication:

- generic `AI-generated science is less diverse` is not a contribution;
- diversity remains motivation only.

### 2.3 MetaMuse — ICLR 2026

MetaMuse finds LLM algorithm generation biased toward familiar designs and uses external stimuli to move search into less familiar regions.

Source:

- https://proceedings.iclr.cc/paper_files/paper/2026/hash/85632be2cd69e9a0ef4ba054c096fac9-Abstract-Conference.html

Implication:

- `LLMs have familiar-solution bias` is not new;
- `external stimuli can steer ideation` is not new;
- our claim must depend on **real scientific evidence, route-matched counterfactual packets, independent baseline measurement, and predictive structure**.

### 2.4 Spectrum Tuning — ICLR 2026

Spectrum Tuning explicitly defines *in-context steerability* as using context to override model priors and move toward a novel output distribution.

Source:

- https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html

Implication:

- `in-context steerability` is prior terminology, not ours;
- our experiment is unusual because scientific literature provides an **implicit** signal and there is no oracle target distribution saying a 75% A packet should yield exactly 75% A proposals.

### 2.5 Context-vs-prior work — ICLR 2025

*Controllable Context Sensitivity and the Knob Behind It* and *Context-Parametric Inversion* already study context versus model knowledge/prior behavior in factual conflicts and instruction tuning.

Sources:

- https://proceedings.iclr.cc/paper_files/paper/2025/hash/c9d780d1e2d57d4b70e807608a72501b-Abstract-Conference.html
- https://proceedings.iclr.cc/paper_files/paper/2025/hash/aa27ac7aca4e462da1439b43ceebc04c-Abstract-Conference.html

Implication:

- `context competes with prior` is not new;
- novelty must be in open-ended scientific choices with multiple valid strategies and matched real-literature interventions.

### 2.6 MUSES — Aug/Sep 2026

MUSES shows prospective retrieval becomes much harder when the target is an author-endorsed generative intellectual root rather than ordinary/familiar citation relevance.

Source:

- https://arxiv.org/abs/2609.00313

Implication:

- `relevance != generative inspiration` now has direct retrieval-side evidence;
- root-vs-matched-non-root downstream injection remains a possible extension, but not the primary experiment.

### 2.7 Citing Less Critically — Sep 2026

A new scientific-writing study reports that LLMs differ from humans in citation rhetoric and disproportionately cite popular/older work.

Source:

- https://arxiv.org/abs/2609.01432

Implication:

- this is useful motivation that LLM-mediated literature use is systematically structured;
- it is not a direct collision because it studies citation production, not evidence-conditioned hypothesis choice.

---

## 3. Collision verdict

No source found in this round simultaneously establishes the following full object:

1. open-ended scientific problem with multiple valid research routes;
2. real scientific literature as context;
3. fixed context amount and matched topical relevance;
4. route/treatment definition frozen before observing model output;
5. independent no-context behavior measurement;
6. output measured at high-level scientific-choice rather than only lexical/embedding similarity;
7. evidence-response dependence on baseline model choice propensity;
8. controlled response used to predict held-out natural-RAG model behavior.

**Decision: KEEP / CONDITIONAL GO.**

Novelty is not a new vocabulary term. It is the combination of causal design + scientific-choice endpoint + held-out prediction.

---

## 4. Terminology freeze

### 4.1 Replace formal `scientific prior` with `baseline route propensity`

For route pair `(A,B)` and seed `x`, define a no-context baseline distribution from an independent generation batch:

```text
B_M(A,B | x) = P_M(route=A or B | x, C=empty)
```

Use `default scientific prior` only as informal motivation when directly linked to prior work. In methods/statistics, prefer:

- baseline route propensity;
- no-context route distribution;
- baseline choice distribution.

Reason: `prior` is overloaded with Bayesian and parametric-knowledge meanings.

### 4.2 Do not make `steerability` the primary estimand

Use:

> **evidence-conditioned scientific choice response**

because Spectrum Tuning already formalizes in-context steerability around target distributions.

If our response curves are strong, predictable, and replicate natural RAG, the discussion may interpret this as a form of scientific-context steerability.

### 4.3 Diversity is secondary

Do not use generic `idea diversity` as the core endpoint. It remains a compatibility/motivation analysis.

---

## 5. Primary experiment object

For model `M`, seed `x`, a source-defined route pair `(A,B)`, evidence mixture level `alpha`, and generated open-ended proposal `Y`:

```text
Y ~ P_M(Y | x, C_alpha)
```

where:

```text
alpha = fraction of A-route evidence in the packet
alpha ∈ {0, .25, .50, .75, 1}
```

The route pair and source packets are selected using source literature only, before any no-context model output is observed.

### Blinded output categories

For each generated proposal, the seed-local primary label is:

```text
A_LEANING
B_LEANING
MIXED
NEITHER
INVALID
```

The global six-way scientific-move taxonomy is a secondary/generalization layer, not the sole primary outcome.

---

## 6. Primary estimand

The cleanest primary directional contrast is the within-`model × seed × route-pair` change in relative A-vs-B choice as A evidence increases.

Use a multinomial model for all five outcomes, but define a pre-specified A-vs-B log-odds contrast:

```text
L(alpha) = log( P(A_LEANING | alpha) / P(B_LEANING | alpha) )
```

Primary evidence-response coefficient:

```text
beta_evidence = slope of L(alpha) with alpha
```

A publishable treatment effect requires:

- directionally consistent non-zero response across multiple seeds/models;
- effect larger than within-route packet-swap and prompt/order nuisance;
- no dependence on one lexical classifier or one embedding metric.

### Route-engagement guardrail

Separately model:

```text
P(A_LEANING or B_LEANING)
```

so an apparent A-vs-B shift cannot be caused by collapsing validity or producing more `NEITHER/INVALID` outputs in one condition.

---

## 7. Baseline-propensity interaction

After route treatments are frozen, independently estimate no-context A/B propensity:

```text
b = log( (P0(A)+eps) / (P0(B)+eps) )
```

Then test whether evidence response depends on `b` without using `b` to choose the treatment.

Primary scientific interpretation if supported:

> The same matched evidence composition has different leverage depending on the model's independently measured baseline scientific-choice distribution.

This is stronger than simply showing priming.

### Measurement-error caution

`b` is estimated from samples, so it is noisy. Full analysis should either:

- propagate binomial/multinomial uncertainty in a hierarchical model; or
- use independent split batches and sensitivity analysis over baseline uncertainty.

Do not treat empirical proportions as noiseless covariates.

---

## 8. Held-out natural-RAG target

Fit response coefficients using controlled packets only.

Then freeze the analysis and, for held-out seeds, compare:

```text
Model 0: baseline route propensity only
Model 1: baseline route propensity + natural retrieved packet composition
```

Target:

> predict the model's route-choice distribution under ordinary top-k retrieval.

Do **not** claim to predict what human researchers will study next.

---

## 9. What would kill the current mechanism claim

KILL / major pivot if any of the following dominates:

1. response exists only under explicit route words or obvious method copying;
2. A/B route-engagement/validity differs so strongly that directional contrast is uninterpretable;
3. effect disappears under relevance/topic/date balance;
4. within-route document swaps are as large as cross-route swaps;
5. baseline propensity does not replicate across independent batches and no stable baseline quantity can be estimated;
6. controlled response fails to improve held-out natural-RAG prediction beyond baseline-only;
7. a direct concurrent paper implements the same matched source-defined route intervention and baseline interaction.

---

## 10. Codex status

As of this round, the repository still contains no `FEASIBILITY_RESULT.md` from the source-only Codex task.

Therefore:

- no scientific generation is authorized;
- Codex source-only corpus / route-matchability audit remains the next permitted engineering work;
- web research continues in parallel.

---

## 11. Decision

**KEEP / CONDITIONAL GO.**

The paper should now be described neutrally as:

> **A controlled study of how matched scientific evidence composition changes LLM research-route choice, and how that response interacts with independently measured baseline route propensities.**

Candidate result-language such as `grounded but prior-bound`, `scientific steerability`, or `retrieval-induced monoculture` must remain outcome-conditioned.
