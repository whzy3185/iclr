# Research Round 19 — Core Experiment Blueprint and Pre-Result Expectations

## 1. Trigger

The research question and novelty boundary are now narrow enough that the next useful step is to design the scientific experiment at executable resolution while still keeping treatment outcomes unseen.

Current scientific object:

> **How does the composition of matched scientific evidence change an LLM's open-ended research-route choice, and how is that response modulated by the model's independently measured baseline route propensity?**

This round does **not** authorize scientific generation. Source-only feasibility remains a hard prerequisite.

---

## 2. Terminology freeze for planning

Avoid overloading established terminology.

Use:

- `baseline route propensity` for the no-context distribution over a frozen seed-local route pair;
- `evidence-conditioned scientific choice response` for the change induced by controlled evidence composition;
- `route A / route B` for two independently selected, scientifically admissible research directions;
- `evidence fraction alpha` for the fraction of packet evidence assigned to route A.

Do not use `scientific prior` or `steerability` as the sole novelty claim. They remain useful connections to prior ICLR work.

---

## 3. Experimental unit

The scientific replication unit is:

```text
seed × route-pair block
```

A block contains:

- one method-masked ICLR research question;
- one route pair `(A,B)` frozen before model outcomes;
- matched evidence pools for A and B;
- repeated model generations across context conditions.

Repeated generations within a block estimate a conditional output distribution. They do not create independent scientific questions.

---

## 4. Route admissibility / scientific equipoise gate

A route pair is not required to be equally optimal. It must satisfy **scientific admissibility**:

1. both routes are plausible responses to the seed question;
2. neither route is obviously off-topic or scientifically dominated by construction;
3. both routes have real, temporally clean ICLR evidence above the frozen relevance floor;
4. matched evidence packets can be built without weakening relevance for one side;
5. the contrast reflects a meaningful research-choice difference rather than synonym-level wording.

Recommended pre-treatment human audit for each candidate block:

```text
Plausibility of route A: 1–5
Plausibility of route B: 1–5
Topical relevance of A evidence: 1–5
Topical relevance of B evidence: 1–5
Are A and B substantively different research strategies? yes/no
Is either route obviously invalid? yes/no
```

Candidate planning gate:

- median plausibility >= 4 for each route;
- no route marked obviously invalid by a majority of annotators;
- difference in mean plausibility <= 0.75 unless justified and modeled;
- evidence relevance balance passes the quantitative matching gate.

Exact thresholds should be frozen after a source-only audit, before model outcomes.

---

## 5. Main conditions

For each eligible block use fixed evidence count `k` after source-only feasibility determines whether `k=6`, `8`, or `12` is broadly supportable.

Primary controlled mixture:

```text
alpha(A) = 0.00, 0.25, 0.50, 0.75, 1.00
```

For `k=8`:

```text
0.00 = 0 A + 8 B
0.25 = 2 A + 6 B
0.50 = 4 A + 4 B
0.75 = 6 A + 2 B
1.00 = 8 A + 0 B
```

Packet size, approximate token budget, relevance distribution, date, topic cluster, and other frozen covariates are matched across mixture levels.

### Required additional conditions

- `C_none`: no evidence; estimates baseline route propensity.
- `C_natural`: ordinary frozen top-k retrieval; held out from treatment-response fitting.
- `C_within_swap`: replace papers with different matched papers from the **same route composition**; document-identity negative control.
- `C_order`: document-order permutations; nuisance control.
- `C_prompt`: small set of semantically equivalent task prompt paraphrases; nuisance control.
- `C_normalized`: content-normalized evidence subset that removes titles, explicit future-work prescriptions, and obvious route-label words where possible while preserving scientific problem/finding/limitation content.

---

## 6. Generator task

The generator should not be told the route labels.

Prompt objective:

> Given the research problem and the supplied literature evidence, propose one concrete, technically substantive research direction that could form the core contribution of a strong ICLR paper. State the research question, central hypothesis or failure mode, method/analysis plan, and decisive experiment.

Output schema:

```json
{
  "research_question": "...",
  "central_claim_or_hypothesis": "...",
  "method_or_analysis": "...",
  "decisive_experiment": "...",
  "expected_failure_or_success_criterion": "..."
}
```

Do not request novelty scores or route names.

---

## 7. Primary outcome annotation

### 7.1 Seed-local directional label — primary

Blind annotators see:

- method-masked seed question;
- route A and route B definitions written before outcome generation;
- generated proposal;
- **not** the treatment condition.

Label:

```text
A_LEANING
B_LEANING
MIXED
NEITHER
INVALID
```

This is the primary scientific outcome because it depends on the predeclared substantive A/B contrast rather than a global self-created taxonomy.

### 7.2 Coarse independent robustness axis

Where feasible annotate an externally anchored coarse contribution axis:

```text
ARTIFACT
KNOWLEDGE
BOTH
UNCLEAR
```

inspired by prior scientific-contribution taxonomy work. This is not a replacement for the seed-local label.

### 7.3 Secondary detailed annotations

- global scientific move taxonomy;
- method inventory;
- problem-framing tuple;
- evidence uptake: source / concept / method / high-level route / central framing;
- recombination class: copy / combine / transfer / new direction.

No secondary annotation may rescue a failed primary outcome post hoc.

---

## 8. Primary estimands

Let:

```text
pA(alpha) = P(A_LEANING | alpha)
pB(alpha) = P(B_LEANING | alpha)
```

### E1 — Directional response margin

```text
D(alpha) = pA(alpha) - pB(alpha)
```

Primary endpoint contrast:

```text
Delta_extreme = D(1.0) - D(0.0)
```

This remains unconditional over all generations; `MIXED`, `NEITHER`, and `INVALID` are not silently dropped.

### E2 — Dose response

Estimate monotonic/nonlinear change of `D(alpha)` over alpha.

Do not require linearity.

Possible shapes:

- approximately linear;
- thresholded;
- saturating;
- asymmetric around alpha=.5;
- flat.

### E3 — Baseline interaction

From independent no-context samples define a block/model baseline contrast, e.g.

```text
B0 = P0(A_LEANING) - P0(B_LEANING)
```

or a smoothed log-odds equivalent.

Test whether evidence response depends systematically on `B0`:

```text
response_strength ~ evidence_fraction × baseline_route_propensity
```

The scientifically interesting question is whether equal evidence has less leverage against a strong opposing baseline propensity.

### E4 — Natural-RAG prediction

Fit a response model on controlled mixture treatments only.

Freeze it.

On held-out seed blocks under ordinary top-k retrieval compare:

```text
Model 0: baseline propensity only
Model 1: baseline propensity + natural evidence composition
```

Primary external-validity target: held-out log loss / Brier score / multinomial predictive likelihood, with route-level calibration plots.

Do not use future human papers as gold outputs.

---

## 9. Anti-triviality controls

A positive RAW result is not sufficient.

### Control A — relevance balance

If route A evidence has systematically higher relevance or better scientific plausibility, the block fails or requires rematching before outcomes.

### Control B — within-route swap

Require:

```text
cross-route composition effect > within-route document-identity effect
```

at a meaningful aggregate level.

### Control C — lexical predictability

Before generation, test how easily A vs B evidence packets can be classified by shallow lexical features.

High lexical separability is not fatal, but then content-normalized robustness becomes essential.

### Control D — direct copying

Measure whether outputs simply reproduce method names/phrases from supplied papers.

The main high-level claim must remain after excluding or stratifying obvious direct-copy outputs.

### Control E — content-normalized context

For a preregistered subset, preserve scientific propositions while reducing obvious route-indicating prose.

A robust high-level response here is substantially stronger evidence than RAW abstract priming.

### Control F — prompt/order noise floor

The primary cross-route effect should materially exceed ordinary prompt paraphrase and evidence-order effects.

---

## 10. Model plan

### Core causal models

Use two independent open model families with auditable cutoffs, exact checkpoints frozen after infrastructure audit.

Current candidates:

- Llama 3.1 Instruct;
- Gemma 3 Instruct.

### High-value secondary comparison

Matched base/pretrained vs instruction-tuned checkpoints, where coherent generation is feasible.

Motivation: accepted ICLR work suggests post-training can change or weaken context reliance / distributional steerability.

Analyze valid-output rate separately so incoherence is not confused with flexibility.

### Frontier models

Only as external-validity extensions if contamination cannot be audited.

---

## 11. Sampling plan — provisional, precision-driven

Do not freeze final N until source-only feasibility and an engineering pilot estimate variance.

### Engineering/statistical pilot after authorization

Illustrative target:

```text
12 seed-route blocks
× 2 core models
× 5 mixture levels
× 30 generations
= 3,600 treatment generations
```

plus:

```text
12 blocks × 2 models × 60 no-context generations
= 1,440 baseline generations
```

and a smaller control subset.

This pilot is for variance, annotation reliability, and treatment-response shape — not for choosing the most favorable hypothesis.

### Full study — planning envelope only

If feasibility permits ~30–40 eligible blocks, a plausible full design is:

```text
36 blocks
× 2 core models
× 5 mixture levels
× 50 generations
= 18,000 treatment generations
```

plus ~7,000 baseline generations and control subsets.

This is a planning envelope, not a commitment.

The final rule should be fixed using either:

- a fixed N decided from the pilot variance; or
- a preregistered confidence-interval width target with a hard maximum.

Never stop when significance appears.

---

## 12. Expected figures if the study succeeds

### Figure 1 — Evidence-response curves

For representative and pooled blocks:

```text
x: route-A evidence fraction
 y: probability / directional margin toward route A
```

Overlay no-context baseline.

### Figure 2 — Baseline-dependent resistance

```text
x: baseline route propensity opposing the treatment
 y: treatment-induced route shift
```

A systematic negative relationship would be a strong mechanism-level regularity.

### Figure 3 — Context-uptake hierarchy

Compare source/concept/method/high-level route/problem-framing response.

Do not force monotonicity.

### Figure 4 — RAW vs normalized evidence

Show whether response survives reduced lexical/direct-route cues.

### Figure 5 — Natural-RAG held-out prediction

Prior/baseline-only predictor vs baseline+evidence-composition predictor.

### Table 1 — Treatment validity

Coverage, seed eligibility, relevance balance, route plausibility balance, matching failures.

This table should appear in the main paper, not be hidden in an appendix, because treatment validity is central to causal interpretation.

---

## 13. Pre-result planning expectations — NOT DATA

The following are subjective planning priors, informed by nearby literature, not empirical results from this project.

### Most plausible qualitative pattern

Current expectation:

1. no-context route propensities will be concentrated and model-dependent;
2. RAW evidence composition will alter route choice detectably;
3. high-level choice response will be weaker than source/concept uptake;
4. instruction-tuned models may be less flexibly redirected than base models on some blocks;
5. effects will vary substantially by seed and route pair;
6. a meaningful fraction of apparent RAW response will disappear under lexical/direct-copy controls, but probably not all;
7. natural top-k RAG prediction will improve modestly when evidence composition is added to baseline propensity, if the controlled mechanism is real.

These expectations are consistent with nearby findings that scientific-method suggestions are concentrated, scientific agents frequently neglect evidence, and post-training can reduce distributional context steerability.

### Subjective outcome branches

Not probabilities of acceptance; rough research-planning priors only:

- **35–45%:** moderate genuine high-level response plus substantial heterogeneity; potentially publishable if baseline interaction or natural-RAG prediction is strong.
- **20–30%:** strong low-level grounding but weak high-level route movement; potentially strong if the abstraction hierarchy is robust and predictive.
- **15–25%:** RAW route effect mostly collapses under lexical/copy controls; likely KILL or major pivot.
- **10–20%:** source-only feasibility / matching coverage is too poor for a broad ICLR causal study; KILL before generation.

These ranges must never be used to reinterpret observed results.

---

## 14. Practical success thresholds — planning gates, not p-value targets

### Strong result

Most of the following:

- clear cross-route response in >=2 model families;
- >=2 route contrasts and multiple subfields;
- response exceeds within-route swap and prompt/order noise;
- material effect survives content-normalized or direct-copy-excluded analysis;
- baseline propensity predicts response heterogeneity;
- held-out natural-RAG prediction improves meaningfully over baseline-only;
- human route annotation is reliable;
- treatment eligibility/coverage is not a tiny hand-selected fraction.

### Borderline result

- reproducible route response but little deeper structure;
- strong RAW effect but much weaker normalized effect;
- only one route contrast generalizes;
- natural-RAG prediction gain is negligible.

This is not enough for the intended paper without an additional mechanistic result.

### Kill result

Any of:

- source-only matching cannot construct enough scientifically admissible blocks;
- treatment effect disappears after matching;
- only lexical/direct copying remains;
- human A/B labels are unreliable;
- model family effects dominate and no within-model route effect replicates;
- controlled response cannot generalize beyond artificial packets;
- a direct contemporary paper closes the causal gap.

---

## 15. Paper content forecast if the moderate/strong branch occurs

Likely paper shape:

### Introduction

Research agents increasingly retrieve scientific literature before proposing hypotheses, but existing evaluations largely measure final idea quality, novelty, or generic diversity. It remains unclear whether real literature actually changes **which scientific strategy a model chooses** when several relevant approaches are plausible.

### Method

Build temporally clean ICLR seed/evidence blocks containing matched alternative scientific routes. Freeze route treatments before model outputs. Estimate no-context baseline route propensities, then intervene on evidence composition while holding context amount and relevance fixed.

### Core result

Evidence composition produces a reproducible route-choice response, but the leverage of evidence varies with model/seed baseline propensity and scientific abstraction level.

### Strong interpretation, only if observed

Scientific evidence is neither ignored nor fully controlling. Models exhibit a structured competition between baseline research tendencies and external literature composition.

### External validity

Controlled response coefficients predict the model's behavior under ordinary top-k RAG on held-out ICLR questions better than baseline propensity alone.

### Implication

Citation/relevance grounding is insufficient to characterize literature-grounded research agents; evaluation should measure whether evidence changes high-level scientific choices.

---

## 16. Decision

**KEEP / CONDITIONAL GO.**

No scientific generation yet.

Immediate dependency remains the source-only feasibility audit: whether real temporally clean ICLR literature supports enough scientifically admissible, relevance-matched multi-route blocks to make this design credible.
