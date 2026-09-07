# Research Round 32 — Pre-Result ICLR Paper Storyboard

## 1. Purpose

Define what the paper should look like **before scientific outcomes exist**. This prevents changing the contribution after seeing whichever metric happens to move.

All numerical examples below are hypothetical illustrations, not observed results.

## 2. Neutral pre-result paper identity

Preferred working title before outcomes:

> **Same Relevance, Different Research Choices: How Scientific Evidence Shapes LLM Hypothesis Search**

Alternative neutral title:

> **Evidence-Conditioned Scientific Choice in Large Language Models**

Avoid in the pre-result title:

- `monoculture`;
- `grounded but prior-bound`;
- `relevance is not discovery`;
- `scientific prior` as an intrinsic-model claim;
- `first` claims.

## 3. One-sentence paper question

> Holding scientific question, model, prompt, context amount, and evidence relevance approximately fixed, how does the composition of real scientific literature change the high-level research strategy selected by an LLM, and can this response predict behavior under ordinary retrieval?

## 4. Intended contribution hierarchy

### Contribution C1 — controlled scientific-choice measurement

A temporally clean, matched-evidence protocol for intervening on scientific literature composition while measuring open-ended high-level research choices.

C1 is necessary but insufficient alone.

### Contribution C2 — empirical response law

Evidence composition causes a reproducible change in high-level route choice, with effect heterogeneity explained in part by model × seed baseline route propensity.

This is the preferred main scientific contribution.

### Contribution C3 — controlled-to-natural prediction

The response learned from controlled evidence mixtures improves out-of-sample prediction of the same model's behavior under ordinary top-k retrieval.

This is the strongest bridge from causal control to realistic RAG behavior.

### Contribution C4 — mechanism/robustness

At least one deeper result:

- component knockout;
- abstraction-level uptake profile;
- cross-route > within-route document replacement;
- post-training effect;
- multi-route simplex response.

C4 elevates the paper but must not rescue failure of C2/C3.

## 5. Proposed paper structure

### 1. Introduction

Problem:

Literature-grounded research agents increasingly retrieve papers before proposing hypotheses, but common evaluations ask whether ideas look novel/good or whether answers cite context. These evaluations do not tell us whether retrieved scientific evidence changes *which kind of research project the model chooses to pursue*.

Gap:

Prior work establishes scientific ideation diversity issues, context-vs-parametric reliance, distributional steerability, and retrieval sensitivity separately. Missing is a matched causal study of implicit real-literature composition over multiple valid scientific strategies.

Question:

Can equally relevant evidence redirect high-level research choice, and how does that leverage interact with baseline model behavior?

### 2. Related Work

Organize narrowly:

1. scientific ideation/research agents;
2. context reliance / in-context steerability;
3. RAG context utilization and attribution;
4. controlled choice/bias experiments.

Do not write a broad AI-for-science survey.

### 3. Experimental Framework

3.1 ICLR-only temporal-clean corpus

3.2 method-masked seed construction

3.3 route admissibility/equipoise

3.4 matched evidence pools

3.5 randomized evidence mixtures

3.6 blinded human route measurement

3.7 statistical estimands

### 4. Does Scientific Evidence Change Research Choice?

Main causal dose-response results.

### 5. What Governs Evidence Response?

Baseline propensity interaction + cross-model/subfield heterogeneity.

### 6. What Part of Evidence Matters?

Component knockout / copy controls / local document replacements / uptake hierarchy.

### 7. Does the Controlled Law Predict Ordinary RAG?

Held-out natural-RAG prediction.

### 8. Extensions

Base vs instruct; three-route simplex; frontier model external validity.

### 9. Discussion / Limitations

Target population, route taxonomy, ICLR-only scope, AI-use disclosure, no claim about human scientific ecosystems.

## 6. Figure storyboard

### Figure 1 — Experimental idea + flagship response

Left panel:

```text
same seed
same relevance distribution
same k
same model

0% A evidence ---------------- 100% A evidence
```

Right panel:

```text
mean blinded route score
vs
evidence A fraction
```

Show 2 model families with uncertainty.

The paper should be understandable from this figure.

### Figure 2 — Baseline-dependent evidence response

x-axis:

```text
no-context baseline route propensity
```

y-axis:

```text
block-level evidence-response effect / slope
```

Potential finding branches:

- strong baseline resistance;
- strong baseline-congruent amplification;
- weak/no interaction.

Do not force a direction.

### Figure 3 — Anti-priming / mechanism

Panel A:

```text
RAW
PF
PFM
PFL
```

Panel B:

```text
within-route replacement
vs
cross-route replacement
```

Panel C optional:

```text
L0 source → L4 problem framing uptake
```

### Figure 4 — Held-out Natural RAG

Predicted vs observed route propensity.

Compare:

```text
baseline-only
vs
baseline + natural evidence composition
```

Report held-out log loss/Brier/calibration.

### Figure 5 — Post-training or simplex extension

Only if strong enough.

## 7. Main table storyboard

### Table 1 — Dataset / attrition / validity

Columns:

```text
subfield
candidate seeds
method-neutral seeds
multi-route seeds
matchable blocks
equipoise-valid blocks
final blocks
```

Also report temporal-clean evidence counts.

### Table 2 — Main effect by model

Hypothetical format:

| Model | Extreme effect | 95% CI | Dose trend | Invalid rate |
|---|---:|---:|---:|---:|
| Model family 1 | +0.xx | [...] | ... | ... |
| Model family 2 | +0.xx | [...] | ... | ... |

No pooled number without within-model rows.

### Table 3 — Robustness

Rows:

```text
RAW
content normalized
exclude exact copy
within-route packet swap
prompt paraphrase
order permutation
```

Columns: effect size and CI, not only p-values.

### Table 4 — Natural-RAG prediction

Rows:

```text
M0 global
M1 baseline only
M2 evidence only
M3 baseline + evidence
M4 + interaction
```

Columns:

```text
log loss
Brier
calibration
block correlation
```

## 8. Hypothetical successful numerical shape

The following is purely synthetic and exists only to define what a coherent story might look like.

Example route score curve on `[-2,+2]`:

```text
alpha=0.00   -0.45
alpha=0.25   -0.22
alpha=0.50   +0.02
alpha=0.75   +0.27
alpha=1.00   +0.51
```

This would be a clear dose response without implying deterministic control.

A plausible strong robustness shape might be:

```text
RAW extreme effect              0.96
PF normalized effect            0.62
PFM effect                      0.88
PFL effect                      0.74
within-route replacement        0.08
cross-route replacement         0.24 per one-paper swap
```

Again: these are **not targets to optimize toward**.

## 9. Paper branch A — strong steerability

Required evidence:

- robust dose response across >=2 model families;
- survives normalization/copy controls;
- natural-RAG prediction improves over baseline-only;
- validity/quality does not collapse.

Possible title after results:

> **Same Relevance, Different Research Choices: Scientific Evidence Steers LLM Hypothesis Search**

Main claim:

> Real literature composition acts as an implicit control signal over high-level open-ended scientific choices.

## 10. Paper branch B — baseline-conditioned / anisotropic response

Required evidence:

- evidence shifts choices, but effect differs strongly with baseline propensity;
- same packets produce different response curves across models;
- interaction generalizes across blocks;
- natural prediction benefits from baseline × evidence model.

Possible title:

> **When Does Scientific Evidence Change an LLM's Research Direction?**

Main claim:

> Evidence influence is systematically conditioned by the model's baseline research-choice distribution.

This may be the strongest ICLR-shaped outcome.

## 11. Paper branch C — abstraction attenuation

Required evidence:

- source/concept uptake high;
- high-level route/problem response much weaker;
- attenuation robust to component/lexical controls;
- pattern replicated across models;
- preferably related to post-training or baseline strength.

Possible title should avoid overused `grounded without...` phrasing.

Example:

> **From Reading to Research Choice: Where Scientific Context Stops Steering LLMs**

## 12. Paper branch D — priming-only

Observed pattern:

```text
RAW strong
normalized PF/PFL ~ zero
cross-route ~ within-route
copy exclusion removes effect
```

Decision:

**KILL as main ICLR paper.**

Do not rescue using lexical metrics or one model.

## 13. Paper branch E — controlled effect but natural-RAG failure

If causal route response is robust but does not improve natural-RAG prediction:

- the controlled phenomenon may still be real;
- external-validity claim becomes narrow;
- paper may be borderline unless a strong component/post-training mechanism compensates.

Decision depends on novelty/collision at that time.

## 14. Paper branch F — source feasibility failure

If real ICLR literature cannot produce enough relevance-matched, equipoise-valid blocks:

**KILL before generation.**

This is a successful research decision, not an implementation failure.

## 15. What would make this unusually strong

A high-upside result combination is:

```text
1. monotone matched-evidence response
2. robust baseline × evidence interaction across model families
3. route effect survives method/lexical removal
4. cross-route replacements > within-route replacements
5. controlled response predicts held-out natural RAG
6. instruction tuning systematically changes the response profile
```

This would move the paper from `interesting evaluation` toward a general behavioral principle about context-conditioned open-ended model choice.

## 16. Decision

**PAPER SHAPE IS NOW SUFFICIENTLY SPECIFIED TO JUDGE EXPERIMENTS AGAINST IT.**

Future experiments should be added only if they answer a reviewer objection or strengthen one of C1–C4. Avoid uncontrolled scope growth.