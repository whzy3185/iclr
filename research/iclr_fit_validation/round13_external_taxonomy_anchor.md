# Research Round 13 — External Taxonomy Anchor for Scientific Route Measurement

## 1. Trigger

Round 12 reduced the primary outcome to seed-local A/B route attribution so the paper does not depend entirely on a custom six-way taxonomy.

The remaining concern is reviewer arbitrariness:

> Are our route labels simply a taxonomy invented to make the treatment effect visible?

This round searches for an independently developed taxonomy of scientific contributions that can serve as an external anchor.

## 2. New evidence

### The Nature of NLP: Analyzing Contributions in NLP Papers — ACL 2025

Pramanick et al. introduce a manually annotated taxonomy of research contributions and a corpus of roughly 2k annotated NLP papers (the released dataset description reports 2,888 peer-reviewed papers in the broader released resource).

Primary source:
https://aclanthology.org/2025.acl-long.1224/

Dataset/resource:
https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/4678

The taxonomy first separates contributions into two broad families:

```text
ARTIFACT
  - new method/model
  - new dataset
  - new task

KNOWLEDGE
  - knowledge about method
  - knowledge about dataset
  - knowledge about task
  - knowledge about language
  - knowledge about people
```

The exact NLP-specific subtypes are not automatically transferable to ICLR, but the top-level distinction is useful:

> **Does the proposal primarily create a new artifact, or primarily create new knowledge about an existing object/phenomenon?**

## 3. Why this matters for our design

Our custom research modes approximately contain two different levels:

```text
BUILD_IMPROVE
OPTIMIZE_EFFICIENCY
    -> often artifact-oriented

DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
VERIFY_FALSIFY_REPLICATE
    -> often knowledge-oriented
```

This mapping is not exact and must not be forced.

However, an independently motivated coarse axis can provide a robustness layer:

```text
local seed-specific route choice
        +
external coarse contribution family
        +
custom finer scientific-move taxonomy
```

If all three tell the same story, the result is harder to dismiss as taxonomy engineering.

## 4. Measurement hierarchy update

### Primary causal endpoint — unchanged

For each frozen seed-specific route pair `(A,B)`:

```text
A-leaning
B-leaning
MIXED
NEITHER
INVALID
```

This remains the cleanest treatment-specific outcome.

### Independent coarse robustness axis — add

Annotate proposals and source papers with:

```text
ARTIFACT
KNOWLEDGE
BOTH
UNCLEAR
```

This coding should be based on a written adaptation protocol derived from the ACL 2025 taxonomy, with examples drawn from ICLR papers before treatment outcomes are inspected.

### Fine-grained cross-seed taxonomy — secondary

Retain:

```text
BUILD_IMPROVE
DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
OPTIMIZE_EFFICIENCY
VERIFY_FALSIFY_REPLICATE
```

but do not require the paper's main claim to survive only under these categories.

## 5. New pre-treatment audit

Before any scientific generation, manually annotate an ICLR source-paper sample on both:

```text
coarse family: ARTIFACT / KNOWLEDGE / BOTH / UNCLEAR
fine route: custom six-way mode
```

Measure agreement separately.

Desired outcome:

- coarse contribution-family agreement should be materially higher than fine-route agreement;
- if coarse family itself is unreliable on ICLR papers, do not use it as a confirmatory endpoint;
- if fine routes are unreliable but coarse family is reliable, retain fine routes only as exploratory.

## 6. Lexical shortcut warning

Artifact papers may disproportionately contain phrases such as:

```text
we propose
new model
new method
outperforms
```

Knowledge papers may contain:

```text
we find
we show
analysis
failure
mechanism
```

Therefore, route-family steering could be a superficial discourse-style priming effect.

Required protections remain:

1. simple lexical classifier baseline on source packets;
2. content-normalized evidence summaries for a pre-specified subset;
3. generated-output classification based on the proposal's substantive goal, not opening verbs;
4. human audit with treatment hidden;
5. within-family paper-swap negative control.

## 7. Impact on novelty claim

This round does not change the core novelty boundary.

It improves measurement validity by triangulating the output using:

- a local treatment-specific decision;
- an externally motivated coarse contribution taxonomy;
- our finer scientific-move taxonomy.

The paper should not claim the Artifact/Knowledge taxonomy as ours.

## 8. Decision

**MODIFY + CONTINUE.**

Use the external Artifact-vs-Knowledge distinction as a robustness / abstraction layer, not as a replacement for the seed-local causal endpoint.

## 9. Next action

Amend the source-only Codex feasibility audit to record the coarse contribution family and measure whether it is more reliably auditable than the fine route labels. Do not generate scientific outcomes.
