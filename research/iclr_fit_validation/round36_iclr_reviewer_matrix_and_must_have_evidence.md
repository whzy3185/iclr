# Research Round 36 — ICLR Reviewer Matrix and Must-Have Evidence

## 1. Trigger

ICLR 2027 Reviewer Guidelines reduce the accept/reject judgment to four central questions:

1. What specific question/problem is tackled?
2. Is the approach well motivated and well placed in literature?
3. Does the paper rigorously support its claims?
4. Does it contribute new knowledge / sufficient value?

The project should be engineered so each question has a direct answer in the main paper.

## 2. Reviewer Question 1 — Is the problem specific?

### Required one-sentence answer

> For open-ended ICLR research problems with multiple scientifically valid strategies, we test how changing the composition of equally relevant real literature changes an LLM's high-level research choice, and whether that response depends on its independently measured no-context behavior.

### Failure mode

If the paper sounds like:

> "Do LLMs use papers when generating ideas?"

then the problem is too broad/obvious.

### Must-have design elements

- one frozen scientific-choice outcome;
- one frozen evidence-composition intervention;
- explicit target population;
- clear controlled vs natural-RAG distinction.

## 3. Reviewer Question 2 — Is it well placed in literature?

The introduction/related work must explicitly acknowledge that prior work already establishes:

- scientific ideation diversity/evaluation issues;
- shared-context ideation evaluation (Ideation Arena);
- evidence-grounded/corpus-first ideation systems (SGHA and others);
- context-vs-parametric reliance;
- in-context steerability (Spectrum Tuning);
- controlled choice biases (BiasBusters);
- context attribution (ARC-JSD).

### Defensible gap

> Existing works either hold literature fixed to compare systems, design new evidence-grounded ideation pipelines, or study context/prior competition on known-answer/target-distribution tasks. We intervene on matched real literature to measure open-ended scientific-choice response among multiple valid strategies.

### Failure mode

Any `first to show context matters / first literature-grounded ideation` claim will be easy to reject.

## 4. Reviewer Question 3 — Does evidence support the claim?

This is the hardest axis and should dominate experimental effort.

### Must-have E1 — source validity

- temporal-clean evidence;
- seed leakage audit;
- route relevance matching;
- scientific equipoise/admissibility;
- full attrition reporting.

### Must-have E2 — causal response

- fixed context amount;
- randomized matched A/B evidence composition;
- multiple packet realizations;
- dose-response / extreme contrast;
- >=2 model families;
- seed-clustered inference.

### Must-have E3 — human measurement

- blinded route score;
- inter-rater reliability;
- invalid/quality guardrails;
- automated judge only after human calibration.

### Must-have E4 — anti-priming

At least one strong nontrivial control:

- content-normalized PF/PFL effect;
- cross-route > within-route replacement;
- direct-copy exclusion;
- prompt/order nuisance smaller than treatment.

Preferably multiple.

### Must-have E5 — external validity

- controlled-fit response model;
- held-out natural top-k retrieval;
- baseline-only vs baseline+evidence prediction;
- no refitting to natural outcomes.

Without E5, the paper must make a narrower artificial-context claim.

## 5. Reviewer Question 4 — Is it significant / new knowledge?

The paper should not sell significance as "AI science is popular."

Potential real knowledge contribution:

> Evidence grounding and high-level research choice are not the same behavior. Scientific literature exerts a measurable, model-dependent influence over open-ended search strategy, and the controlled response can explain/predict ordinary literature-grounded generation.

or, depending on data:

> High-level scientific choices are substantially less responsive to evidence than low-level source/concept uptake, despite strong grounding.

### Strong significance amplifier

A robust same-family post-training effect would connect the phenomenon to general model training, not merely scientific-agent application design.

## 6. Reviewer #2 attack matrix

| Attack | Severity | Evidence required to survive |
|---|---:|---|
| "Of course models copy the papers you show them" | Critical | PF/PFL normalization, copy exclusion, cross-route > within-route replacement |
| "A/B routes are arbitrary" | Critical | source-derived global roster, human equipoise, route reliability, external coarse taxonomy |
| "One route is simply better" | Critical | pre-treatment relevance/plausibility/equipoise audit |
| "This is HCI/science-of-science, not ML" | High | frozen model conditional behavior, matched context intervention, baseline interaction, post-training extension |
| "Context/prior is already known" | High | open-ended multi-valid scientific choice, implicit real literature, high-level route response, natural RAG |
| "Ideation Arena already uses literature context" | High | they hold context fixed; we randomize composition within fixed model/problem |
| "SGHA/Graph2Idea already ground ideas in evidence" | High | system improvement vs causal evidence-response mechanism |
| "LLM judge is unreliable" | Critical | human-anchored blinded route labels |
| "Temporal leakage / model already knows papers" | High | cutoff audit + post-Aug-2024 evidence + ambiguous subset separation |
| "You cherry-picked easy seeds" | Critical | candidate manifest, attrition waterfall, source-only eligibility, seed-level clustering |
| "Thousands of samples create fake significance" | Critical | seed-clustered effect sizes, packet variance, block/seed hierarchy |
| "Artificial packets do not reflect real RAG" | Critical | held-out natural-RAG prediction |
| "No mechanism" | Medium/High | baseline interaction + component knockout + document replacement; internal activations not strictly required |
| "Effect only one model" | High | >=2 independent families, within-model reporting |
| "Effect is tiny" | High | predeclared smallest effect of interest / CI-based interpretation |

## 7. What must be in the main 9 pages

Because ICLR reviewers are not required to read appendices, the main paper must contain:

1. causal design diagram;
2. corpus/seed attrition summary;
3. evidence balance/equipoise summary;
4. flagship dose-response;
5. within-model effects with uncertainty;
6. one anti-priming result;
7. baseline interaction or abstraction result;
8. natural-RAG held-out prediction;
9. concise collision positioning.

Detailed prompts, full taxonomy, per-seed tables, extra model scales, and extensive robustness can go to appendix.

## 8. Paper should avoid leaderboard framing

ICLR 2027 explicitly notes that valuable papers need not compete on an established leaderboard or produce SOTA.

Therefore do not force:

- idea-quality SOTA;
- a new agent leaderboard;
- a new retrieval algorithm;
- a better novelty score.

The paper's value should be **new empirical/model-behavior knowledge**.

## 9. Reviewer confidence strategy

A skeptical reviewer should be able to reconstruct the causal logic:

```text
routes chosen before model outputs
seed valid
A/B scientifically plausible
papers matched
context amount fixed
composition randomized
human outcome blinded
model baseline independently measured
controlled response replicated
priming alternatives attacked
natural behavior predicted out-of-sample
```

The more of this chain is visible in the main paper, the less the review depends on trusting author judgment.

## 10. AI-era meta-risk

ICLR leadership explicitly warns that AI makes it easy to create paper-shaped objects and encourages ambitious, complete work.

Because this project itself uses ChatGPT/Codex heavily, the paper should over-invest in:

- preregistration provenance;
- frozen decisions before outcomes;
- public negative results;
- reproducible source manifests;
- transparent AI-use disclosure;
- human scientific judgment at key validity gates.

This is not only compliance; it is part of credibility.

## 11. Submission-readiness gate

Do not call the project ICLR-ready unless the answer to all four reviewer questions is strong.

### Q1 specific problem

PASS only if one-sentence claim is stable.

### Q2 literature

PASS only if nearest neighbors are explicitly differentiated without exaggerated `first` language.

### Q3 evidence

PASS only if causal validity + human measurement + anti-priming + natural prediction are present.

### Q4 significance

PASS only if at least one non-obvious general regularity exists beyond raw context sensitivity.

## 12. Decision

**CURRENT STATUS: Q1/Q2 DESIGN PASS; Q3/Q4 PENDING DATA.**

The project is now conceptually ICLR-shaped. Its fate depends almost entirely on source feasibility and whether the controlled evidence response survives the validity chain.