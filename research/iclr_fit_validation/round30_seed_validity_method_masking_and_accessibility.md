# Research Round 30 — Seed Validity, Method Masking, and Accessibility

## 1. Trigger

The causal treatment can be clean while the seed question itself is invalid. A seed derived from an ICLR 2026 paper may:

- leak the focal method;
- use wording that already strongly instructs one route (e.g. "design a better architecture");
- contain post-cutoff jargon the causal-core model cannot interpret;
- be so broad that A/B routes are not meaningfully comparable;
- be so narrow that only one scientific route is plausible.

Therefore seed construction needs its own pre-treatment audit.

## 2. Seed is not the focal paper abstract

For focal paper `F`, construct a **method-agnostic research problem context** rather than copying the abstract minus one sentence.

Preferred seed structure:

```text
BACKGROUND
  Minimal technical context required to understand the problem.

OBSERVED PROBLEM / OPEN QUESTION
  What phenomenon, failure, limitation, or uncertainty motivates research?

TASK
  Propose one rigorous ICLR-style research project addressing this problem.
  Do not prescribe whether the project should build, diagnose, measure, explain, optimize, or falsify.
```

The generator task instruction remains globally fixed across seeds.

## 3. Forbidden leakage

Remove or rewrite:

- focal method name/acronym;
- paper title phrase;
- novel dataset/model names introduced by focal paper;
- exact numerical headline result;
- unique method component sequence;
- explicit solution language;
- wording such as `we propose`, `our method`, `we introduce`;
- future-work statement copied from the focal paper.

## 4. Neutral task wording

Avoid route-biased task verbs.

Bad:

```text
Design a new architecture to solve...
Develop a benchmark for...
Explain the mechanism behind...
```

Preferred global task:

> Propose one technically substantive and experimentally testable ICLR-style research project that directly addresses the scientific problem below. Choose the research strategy you consider most appropriate.

This allows route choice to emerge rather than be requested.

## 5. Seed-level audit dimensions

Before model treatment, human/source-only audit each candidate seed on 1–5 scales:

```text
PROBLEM_CLARITY
BACKGROUND_SUFFICIENCY
METHOD_NEUTRALITY
MULTI_ROUTE_OPENNESS
TECHNICAL_SUBSTANCE
ICLR_RELEVANCE
```

Also binary flags:

```text
FOCAL_METHOD_LEAK
DISTINCTIVE_PHRASE_LEAK
POST_CUTOFF_CONCEPT_UNEXPLAINED
SOLUTION_PRESCRIBED
TOO_BROAD
TOO_NARROW
```

## 6. Multiple-route openness gate

A seed is useful only if competent researchers can imagine at least two substantively different, scientifically reasonable approaches before looking at model outputs.

This is separate from evidence availability.

Pipeline:

```text
seed openness
  AND
source evidence supports multiple routes
  AND
route pair passes equipoise
  AND
relevance matching succeeds
→ eligible block
```

## 7. Model accessibility gate

A post-cutoff seed can contain new terminology, but the model must receive enough background to reason about it.

Before scientific treatment, perform an engineering-only comprehension check that does **not** ask for research ideas or route preference.

Possible questions:

- summarize the problem in one sentence;
- identify the target object/constraint;
- list factual definitions supplied in the seed.

This is not a treatment outcome.

If a model cannot parse the problem, route response is uninterpretable.

Accessibility failures remain reported; do not silently rewrite seeds after treatment outcomes.

## 8. Textual fingerprint / focal-paper leakage audit

Compute similarity between seed wording and focal paper:

- title;
- abstract;
- introduction problem statement where available.

Flag unusually high lexical overlap.

Also search for rare distinctive n-grams/acronyms copied from the focal paper.

The goal is not to make the seed semantically distant—the same problem must remain—but to avoid reconstructing a paper-identification key.

## 9. Focal method is not a gold answer

Do not score generations by similarity to the focal ICLR 2026 paper's method.

The focal paper is used only to obtain a realistic later scientific problem and chronology.

A generated route different from the published method can be equally or more scientifically valid.

## 10. Prompt paraphrase robustness

For a pre-specified subset after the main experiment, create 2–3 neutral paraphrases of the same seed problem.

Requirements:

- same technical content;
- no route-specific verbs;
- independently reviewed for meaning preservation.

Measure:

```text
prompt-paraphrase route variance
```

Treatment effect should exceed this nuisance floor.

If the entire result changes under harmless seed paraphrase, the scientific-choice construct is unstable.

## 11. Baseline propensity interpretation

No-context route propensity must be called a **model × seed baseline**, not an intrinsic model-wide scientific prior.

The seed wording and scientific problem legitimately contribute to the baseline distribution.

General model-level conclusions require aggregation across many seeds and robustness to neutral paraphrases.

## 12. Seed difficulty as moderator

Record source-only difficulty proxies, e.g.:

- specificity of problem;
- number of required technical concepts;
- breadth of plausible routes;
- evidence pool size.

Do not tune seed selection for large model effects.

Exploratory question:

> Are evidence-conditioned route responses stronger for underspecified/open problems than for tightly constrained technical problems?

This is secondary.

## 13. Seed attrition reporting

Paper should show:

```text
ICLR 2026 candidate papers
→ extractable method-agnostic problem seeds
→ pass leakage/accessibility audit
→ multi-route open
→ source-matchable
→ equipoise-valid
→ final blocks
```

This prevents hidden hand selection.

## 14. Kill / redesign conditions

Major redesign if:

- most candidate seeds leak focal methods;
- neutralization removes too much technical substance;
- causal-core models cannot understand post-cutoff seed concepts;
- only highly hand-edited seeds pass;
- multi-route openness is rare;
- prompt paraphrase variance is comparable to or larger than evidence-treatment effects.

## 15. Decision

**REQUIRED BEFORE TREATMENT FREEZE.**

The experiment is about how evidence changes research choice for a well-defined scientific problem. If the seed already prescribes or obscures that choice, the causal interpretation fails before retrieval begins.