# Research Round 16 — Treatment Validity and Anti-Lexical-Priming Design

## 1. Trigger

Round 15 froze a neutral estimand: evidence-conditioned research-route choice under source-defined A/B treatments.

The strongest remaining reviewer attack is now:

> “Your model simply copies the rhetoric/method words in the abstracts it sees. This is not a meaningful scientific-search effect.”

This round designs the experiment so that a positive result must survive that attack.

---

## 2. ICLR design precedent

### BiasBusters — ICLR 2026

BiasBusters studies tool-selection bias using functionally equivalent tools and controlled perturbations of metadata/order/pretraining exposure. It shows that small semantic changes in tool descriptions can move selections substantially.

Source:

- https://proceedings.iclr.cc/paper_files/paper/2026/hash/a79875cc0d046ce7ce65f03f3affaa9e-Abstract-Conference.html

Lesson for us:

- text features can legitimately cause model choices;
- but to make a stronger mechanism claim we need matched alternatives, nuisance controls, and a decomposition of *what aspect of evidence* drives the change.

### Does Writing with Language Models Reduce Content Diversity? — ICLR 2024

This paper isolates a population-level behavioral effect using a controlled intervention and traces the effect specifically to model-contributed text.

Source:

- https://proceedings.iclr.cc/paper_files/paper/2024/hash/02dec8877fb7c6aa9a79f81661baca7c-Abstract-Conference.html

Lesson:

- an ICLR behavioral paper can succeed without architecture novelty if the causal attribution is clean and the object is measured directly.

---

## 3. What is and is not a confound

A scientific route necessarily differs in semantic content. We should **not** attempt to make A and B text semantically identical; that would erase the treatment.

The confound to rule out is narrower:

> The effect is explained by superficial route-signaling language or exact method imitation rather than the scientific evidence/content supporting a research direction.

Examples of trivial cues:

```text
A packet repeatedly says: “we propose / improve / outperform”
B packet repeatedly says: “failure / benchmark / stress test / diagnose”
```

If output labels merely mirror those words, the paper is weak.

---

## 4. Treatment hierarchy

Use two versions of the same pre-frozen evidence treatment.

### T1 — RAW scientific context

Primary ecological condition:

- real ICLR title removed or optionally retained only in a secondary analysis;
- real abstract or fixed evidence excerpt;
- no generated future-work suggestion;
- packet length matched.

RAW answers the realistic RAG question.

### T2 — CONTENT-NORMALIZED evidence cards

Secondary anti-priming condition on a pre-specified subset.

Each source paper is converted to a fixed-slot evidence card:

```text
Problem:
Finding / empirical observation:
Mechanism or limitation supported by the paper:
Scope / boundary:
```

Forbidden fields:

- paper title/author;
- explicit “we propose / we evaluate / we introduce” boilerplate;
- future-work prescriptions;
- route category name;
- imperative recommendations to the generator;
- exact new method name where not necessary to preserve the finding.

### Construction rule

Because automatic rewriting can itself introduce bias:

1. create cards before any treatment outcomes;
2. use one frozen extraction/rewrite protocol across all routes;
3. human-audit a stratified sample for factual fidelity and route-neutral wording;
4. hash/freeze the card corpus before generation;
5. retain source abstract and card pair for audit.

If human resources are available, manually author/verify the confirmatory subset. Given the project is not time-constrained, this is preferred over relying only on an LLM normalization pass.

---

## 5. Lexical-separability diagnostic

Before scientific generation, train/evaluate simple text classifiers that predict source route from packet text.

At minimum:

- bag-of-words / TF-IDF logistic regression;
- cue-lexicon classifier;
- optional small frozen embedding classifier.

Report route predictability for:

```text
RAW packets
CONTENT-NORMALIZED packets
```

Purpose is diagnostic, not a requirement that route be lexically unpredictable.

Interpretation:

- high RAW separability is expected;
- a strong paper is helped if normalization substantially reduces trivial lexical separability while preserving the evidence-conditioned output effect.

Never choose a normalization pipeline because it maximizes the downstream treatment effect.

---

## 6. Exact-copy / source-transfer audit

For every generated proposal, measure separately:

### C0 — no evident source transfer

No identifiable supplied method/finding is reused.

### C1 — source/finding uptake

Uses an empirical finding, limitation, or mechanism from the evidence.

### C2 — direct method copy

Reuses a supplied method with little substantive adaptation.

### C3 — recombination

Combines components across supplied sources.

### C4 — transfer

Uses a supplied finding/framing on a new target or proposes a route not explicitly stated by one source.

The primary route effect should be reported both:

- on all valid outputs;
- on the subset excluding obvious direct method copies.

If the effect disappears entirely after excluding C2, downgrade the claim to contextual imitation and likely KILL the ICLR mechanism paper.

---

## 7. Four key controls

### Control N1 — Within-route packet swap

Hold A/B route proportion fixed but replace papers with other matched papers from the same route and relevance strata.

This estimates document-identity sensitivity.

Desired pattern:

```text
cross-route composition effect
>
within-route paper-identity effect
```

If not, the route abstraction has little explanatory value.

### Control N2 — Evidence order permutation

Randomize document order across replicates.

If order effects are comparable to route composition effects, model order explicitly and weaken causal interpretation.

### Control N3 — Prompt paraphrase

Use pre-frozen semantically equivalent generator prompts on a subset.

Treatment effect should exceed prompt-induced route variance.

### Control N4 — Sampling breadth

Compare standard and high-temperature generation.

Question:

> Does increasing within-context diversity remove the directional evidence effect, or only broaden sampling around an evidence-conditioned center?

This separates generic sampling diversity from context-driven direction.

---

## 8. Relevance and scientific-plausibility matching

ICLR acceptance controls venue/quality tier only imperfectly. Packet matching therefore needs a stronger gate.

For each seed-route pair, every candidate evidence paper must pass:

1. **topic relevance floor** to the seed;
2. **scientific applicability audit** — the paper provides information that could reasonably inform the seed problem;
3. temporal cleanliness;
4. no focal-paper leakage.

Then match A/B on:

- dense relevance;
- cross-encoder/reranker relevance;
- topic cluster / local semantic neighborhood;
- token length;
- first-public date;
- optional frozen popularity proxy if available and not too sparse.

### Packet-level balance criterion

Report distributional balance, not only mean similarity.

Candidate tools:

- standardized mean differences;
- Wasserstein distance / overlap plots;
- matching with calipers;
- optimal-transport or min-cost assignment within seed.

Do not loosen the relevance gate to make a rare route matchable.

---

## 9. Route-pair inclusion policy

Avoid choosing one narratively attractive A/B pair per seed.

Predefine a global contrast roster, e.g.:

```text
BUILD ↔ DIAGNOSE
BUILD ↔ MEASURE
BUILD ↔ EXPLAIN
DIAGNOSE ↔ EXPLAIN
```

For each seed, include **every** contrast from the roster that passes the source-only count + matching gate, subject to a predeclared maximum if compute later becomes prohibitive.

This is preferable to selecting the pair with the expected largest model displacement.

### Why this matters

It makes the scientific target an average response over a predeclared feasible treatment population, not a collection of best-looking anecdotes.

---

## 10. Human-blinded route judgment

For the confirmatory subset, annotators receive:

- seed research question;
- generated proposal;
- definitions of route A and route B for that seed/contrast;

They do **not** receive:

- treatment condition;
- evidence packet;
- model identity where blinding is practical;
- alpha level.

Primary label:

```text
A_LEANING / B_LEANING / MIXED / NEITHER / INVALID
```

This seed-local judgment avoids requiring annotators to accept our global taxonomy as ground truth.

### Reliability gate

Pre-treatment examples and a small engineering-only calibration set should establish whether humans can distinguish the A/B routes.

If blinded reliability is weak for a route pair, that pair is not a valid confirmatory treatment object.

---

## 11. Strong result ladder

### Weak / insufficient

> RAW packets shift output route labels.

Could be lexical priming.

### Better

> Effect exceeds within-route swaps and prompt/order noise, with relevance matched.

### Strong

> Effect persists in content-normalized packets and after excluding exact method copies.

### Stronger

> Same frozen packet produces different response curves across models as predicted by independently measured baseline route propensity.

### Strongest

> Controlled response coefficients predict held-out natural-RAG route choice.

The paper should not advance to the strongest language without climbing this ladder empirically.

---

## 12. Kill criteria added this round

KILL / downgrade if:

1. treatment route is nearly synonymous with a tiny cue lexicon and no normalized-condition effect survives;
2. direct method copying explains the route shift;
3. within-route paper swaps are comparable to or larger than cross-route composition changes;
4. A/B relevance/applicability cannot be balanced for enough seeds;
5. human seed-local A/B labels are not reliable;
6. route effects appear only in RAW abstracts and vanish under any reasonable content normalization;
7. scientific validity/testability drops materially under one route, meaning the alternative is not genuinely plausible.

---

## 13. Codex implication

The existing source-only feasibility task should answer several prerequisites before any generation:

- route-pair counts by seed;
- matching feasibility under relevance calipers;
- whether global route contrasts have sufficient coverage;
- packet lexical separability diagnostics can be prepared but not optimized against outcomes.

**No scientific generation is authorized until source-only feasibility is reviewed.**

---

## 14. Decision

**KEEP / CONDITIONAL GO.**

The experiment is scientifically defensible only if we can demonstrate that evidence-conditioned route choice is more than document identity, lexical cueing, or direct method copying.

This round makes `content-normalized robustness + within-route swap + blinded A/B judgment` the minimum anti-priming package for a strong ICLR claim.
