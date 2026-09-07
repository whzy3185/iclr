# Research Round 47 — Lit2Test Collision and Prompt Adjustment

## 1. Trigger

A late-August 2026 direct-neighbor search surfaced:

**What Proves You Wrong: Benchmarking Language Models on Falsifiable Research Ideation** (Lit2Test), arXiv:2608.22948, Aug 24 2026.

Lit2Test builds 200 real-paper neighborhoods and evaluates proposals through a six-field contract organized around an explicit falsifying outcome, with 1,200 blind pairwise comparisons and human calibration.

This does not perform our matched evidence-composition intervention, but it materially occupies the `literature → falsifiable proposal` evaluation space.

## 2. Collision map

### Lit2Test already establishes / occupies

- research proposal generation from real literature neighborhoods;
- explicit falsifiability as a proposal-quality contract;
- blind comparison of model-generated proposals;
- bounded human calibration of proposal evaluation;
- critique of style/position-sensitive free-form judging;
- critique of using the later real paper as the unique gold trajectory.

### Lit2Test does NOT appear to establish from the inspected description

- source-selected competing scientific route pairs;
- matched A/B evidence alternatives for the same seed;
- randomized evidence composition at fixed context size/relevance;
- independent no-context route baseline;
- evidence × baseline route interaction;
- route-level choice response curves;
- controlled-to-natural RAG prediction.

Therefore it is a high-value adjacent evaluation paper, not a direct collision with H1–H3.

## 3. New prohibited novelty claims

Do not claim:

- first literature-to-test research ideation benchmark;
- first falsifiability-centered proposal protocol;
- first proposal evaluation with an explicit falsifying outcome;
- first real-paper-neighborhood scientific ideation test;
- first human-calibrated falsifiability evaluation.

## 4. Implication for our output prompt

Round 43 proposed an output field:

> `What result would support or falsify the central claim`

This remains scientifically sensible, but it now looks closer to an existing specific evaluation intervention.

More importantly, requiring every proposal to foreground falsification could itself alter the research-route distribution, especially increasing DIAGNOSE/VERIFY-style outputs.

Therefore the primary generator instrument should become slightly more neutral.

## 5. Revised primary output structure

Preferred primary format:

```text
1. Scientific objective
2. Core research question or claim
3. Study design / technical approach
4. Key experiment or analysis
5. Evaluation and decision criteria
6. Expected scientific contribution
```

`Evaluation and decision criteria` asks how the project would determine whether it succeeds/what conclusions evidence supports without forcing the proposal into a named falsification contract.

A proposal can still be genuinely falsifiable.

## 6. Falsifiability remains a quality guardrail

Human/secondary quality audit may still ask:

```text
Is the central claim empirically/theoretically testable?
Is there a result that would count against the proposal's central claim?
```

But this is not the main route outcome and not a novelty contribution.

## 7. Useful methodological lesson from Lit2Test

Lit2Test reinforces two principles already in our design:

### A. The later focal paper is not a gold answer

Research can take multiple valid trajectories. Our focal ICLR 2026 method remains descriptive context only.

### B. Proposal evaluation is vulnerable to style/position bias

Our primary route effect therefore uses a narrowly defined blinded A/B route judgment rather than a broad `which idea is better?` score.

This is complementary rather than competitive.

## 8. Possible external robustness, not core

After the main paper is viable, Lit2Test-style falsifiability fields could be used as a **quality validity check**:

> Does evidence-induced route movement preserve proposal testability/falsifiability?

This should not become another main experiment unless route movement appears to trade off sharply with quality.

## 9. Updated nearest-neighbor distinction

A concise distinction:

> Lit2Test studies how to elicit and evaluate falsifiable proposals from literature neighborhoods. We hold the proposal task fixed and instead randomize which equally relevant scientific route is represented in the literature, measuring the causal response of high-level research choice.

## 10. Prompt contract change

Round 43 remains valid except the primary output heading should be updated conceptually from:

```text
What result would support or falsify the central claim
```

to:

```text
Evaluation and decision criteria
```

No treatment outcomes exist, so this change is pre-outcome.

The final prompt file/hashes will be frozen during F1/P0, not retroactively edited in historical research records.

## 11. Decision

**NO DIRECT COLLISION. MODIFY PROMPT WORDING / NOVELTY BOUNDARY.**

Lit2Test raises the scientific-ideation evaluation bar and validates the importance of human-audited, testable proposals, but the controlled evidence-choice mechanism remains distinct.