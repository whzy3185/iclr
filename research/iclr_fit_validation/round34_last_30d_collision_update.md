# Research Round 34 — Latest 30-Day Collision Update

## 1. Trigger

The scientific-ideation literature is moving quickly. This round performs a high-recall scan of late-August / early-September 2026 work before any scientific generation is authorized.

## 2. Ideation Arena — Aug 30, 2026

**Ideation Arena: Evaluating LLM Generated Research Ideas with Battle-style Human Expert Assessment** evaluates 14 frontier LLMs and 5 research-agent architectures using shared literature contexts and >6,000 double-blind comparisons from 105 active computer-science researchers.

Key design detail:

> every compared system receives the same literature context, intentionally removing retrieval variation so evaluation focuses on ideation capability.

### Collision

High on:

- literature-grounded scientific ideation;
- shared/controlled literature context;
- expert human evaluation;
- open-ended research proposals.

### Non-collision / remaining gap

Ideation Arena **holds literature context fixed**. It does not manipulate matched literature composition to estimate how evidence changes research strategy.

Its goal is:

```text
same context
→ compare model/agent quality
```

Our goal is:

```text
same model/problem
+ matched context amount/relevance
+ manipulated scientific-route composition
→ estimate research-choice response
```

### Additional important distinction

Ideation Arena's data filtering explicitly excludes surveys, benchmarks, and pure evaluation papers to preserve methodology-oriented research contexts.

Our scientific object deliberately includes choices such as:

```text
BUILD
vs
DIAGNOSE
vs
MEASURE/EVALUATE
vs
EXPLAIN
```

Therefore their context construction is not suitable for studying the research-mode distribution we care about.

### Implication

Do not claim:

- first shared-context ideation evaluation;
- first expert human evaluation of LLM research ideas;
- first literature-grounded ideation protocol.

Use Ideation Arena as strong support for our human-anchored annotation strategy and as a complementary fixed-context benchmark.

## 3. SGHA — Aug 18, 2026

**SGHA: Evidence-Grounded Research Problem Discovery with Local Language Models** proposes a corpus-first system that structures literature into evidence-linked objects/graphs, detects unresolved structural motifs, verifies candidate gaps, and formulates research-problem families.

### Collision

High on:

- explicit evidence grounding;
- literature structure shaping research-problem generation;
- local/open model scientific ideation;
- assumptions/failures/limitations as scientific evidence objects.

### Remaining gap

SGHA is a **system design / problem-discovery method**. It does not, from the inspected description:

- define equally plausible A/B scientific routes for the same seed;
- match evidence alternatives on relevance;
- randomize route composition at fixed context quantity;
- independently estimate no-context route propensity;
- estimate evidence × baseline response;
- test controlled-to-natural RAG prediction of model choices.

### Useful design inspiration

SGHA's evidence objects reinforce Round 23's idea that source papers can be represented using structured scientific facets such as:

- assumptions;
- failure conditions;
- limitations/contradictions;
- methods/tasks.

However, do not copy SGHA's graph/system as our contribution.

## 4. Ideation evaluation warning strengthens

Recent research-proposal evaluation work continues to show that automated judges do not reliably match domain-expert preferences.

This further supports:

```text
human route annotation = primary anchor
LLM classifier          = calibrated scaling tool only
```

Do not switch back to LLM-only outcome measurement for convenience.

## 5. MoRI / scientific ideation training systems

Recent ACL 2026 work such as motivation-grounded scientific ideation explicitly trains models to reason from research motivation to methodology.

Implication:

- `scientific context → methodology` is an active algorithmic space;
- our novelty cannot be that context matters or motivation grounds methods;
- our work must remain a controlled behavioral/causal study rather than another training framework.

## 6. Updated nearest-neighbor decomposition

Current nearby works cover pieces separately:

```text
Ideation Arena
  shared literature + human expert evaluation

SGHA
  structured evidence + research problem discovery

Si et al. ICLR 2025
  scientific ideation + diversity + RAG quantity

Spectrum Tuning ICLR 2026
  prior-overriding context / distributional steerability

Context-Parametric Inversion ICLR 2025
  post-training and context reliance

BiasBusters ICLR 2026
  controlled semantically equivalent choice alternatives

ARC-JSD ICLR 2026
  context attribution
```

The still-unoccupied combination is:

```text
real scientific literature
+ same open-ended scientific problem
+ multiple independently valid research routes
+ source-only treatment freeze
+ matched relevance / equipoise
+ randomized evidence composition
+ blinded high-level route measurement
+ independently estimated baseline route propensity
+ evidence × baseline interaction
+ anti-lexical/component controls
+ held-out natural-RAG prediction
```

## 7. Claims now explicitly prohibited

Add to prior prohibition list:

- `first shared-context scientific ideation evaluation`;
- `first human expert arena for research ideas`;
- `first evidence-grounded research problem generation`;
- `first corpus-first scientific ideation`;
- `first structured literature representation for ideation`.

## 8. Novelty sentence after this scan

A defensible pre-result novelty statement becomes:

> **Rather than holding literature fixed to compare research agents or designing a new evidence-grounded ideation system, we intervene on the composition of equally relevant real scientific evidence to measure how a fixed LLM redistributes its high-level research choices, and test whether this response depends on its independently measured no-context behavior.**

## 9. Direct-collision criterion tightened

A future paper is genuinely dangerous if it combines most of:

1. same scientific problem;
2. alternative valid research strategies;
3. matched real literature context;
4. controlled/randomized context composition;
5. high-level open-ended proposal choice;
6. no-context baseline behavior;
7. context × baseline interaction;
8. human or strongly human-validated route measurement;
9. natural retrieval generalization.

Shared context or evidence grounding alone is no longer enough to count as direct collision.

## 10. Decision

**KEEP / CONDITIONAL GO REMAINS.**

The latest literature raises the novelty bar but does not erase the controlled causal gap. It also strengthens the case for human-anchored evaluation and for emphasizing research-choice response rather than generic idea quality.