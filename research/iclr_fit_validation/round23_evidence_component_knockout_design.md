# Research Round 23 — Evidence Component Knockout Design

## 1. Trigger

Rounds 19–22 establish a viable primary experiment based on matched A/B scientific routes and controlled evidence-mixture dose response. The remaining mechanism risk is that any observed high-level route shift may still be driven by superficial route markers in paper abstracts (e.g., "we propose", "benchmark", "failure", "mechanism") rather than by scientific evidence in a meaningful sense.

Recent adjacent evidence reinforces the need to decompose context. ACL 2026 work on scientific feasibility finds that experiment descriptions and outcome evidence affect LLM judgments differently. ICLR RAG work also shows that context sufficiency, distracting content, and specific context segments strongly affect model behavior. Therefore, evidence should not be treated as an indivisible text blob.

## 2. Research question added by this round

> Which components of scientific literature are responsible for evidence-conditioned changes in LLM research choices?

This is a secondary mechanism question. It does not replace the primary matched-evidence experiment.

## 3. Standardized evidence card representation

For a pre-specified robustness subset, transform each source paper into an audited evidence card with four fields:

```text
P — PROBLEM / CONTEXT
    What scientific problem or limitation is being studied?

F — FINDING / OBSERVATION
    What empirical or theoretical result is established?

M — METHOD / INTERVENTION
    What method, experimental intervention, or solution family is used?

L — LIMITATION / IMPLICATION
    What limitation, boundary condition, unresolved issue, or implication is supported by the paper?
```

Rules:

- no title or author names;
- no explicit research-mode label;
- no unsupported future-work recommendation;
- no statement that tells the generator which route to choose;
- preserve source paper ID separately;
- every card is auditable against source text;
- token budget standardized within a narrow range;
- card extraction is frozen before generation.

## 4. Component conditions

Do not create a combinatorial explosion. Use four pre-specified representations on a stratified subset of seed-route blocks.

### R0 — RAW ABSTRACT

Original abstract (baseline ecological condition).

### R1 — PF

```text
Problem + Finding only
```

Removes explicit method identity and explicit limitation/future-work framing.

Interpretation: can empirical content itself move high-level research choice?

### R2 — PFM

```text
Problem + Finding + Method
```

Adds method content while withholding explicit limitation/implication framing.

Contrast `PFM - PF` estimates the incremental leverage of method information.

### R3 — PFL

```text
Problem + Finding + Limitation/Implication
```

Withholds explicit method identity while preserving scientifically supported limitation/boundary information.

Contrast `PFL - PF` estimates whether problem/limitation framing steers research choice without direct method imitation.

Optional `PFML` is unnecessary if RAW is already present unless normalization quality requires a fully standardized full-information control.

## 5. Main mechanism contrasts

For each condition estimate the A/B route dose-response.

Define:

```text
Delta_R = D_R(alpha=1) - D_R(alpha=0)
```

where `D_R` is the blinded A-vs-B directional outcome under evidence representation R.

Key pre-specified comparisons:

```text
Method leverage      = Delta_PFM - Delta_PF
Limitation leverage  = Delta_PFL - Delta_PF
Raw excess           = Delta_RAW - Delta_PF
```

These are not assumed positive.

## 6. Result patterns and interpretation

### Pattern A — PF retains most of RAW effect

```text
Delta_PF ≈ Delta_RAW
```

Interpretation:

The route response is not primarily driven by explicit method words or future-work cues. Scientific problem/finding content itself is sufficient to redirect model research choice.

This is the strongest anti-priming result.

### Pattern B — PFL restores effect, PFM does not

```text
Delta_PF small
Delta_PFL large
Delta_PFM small/moderate
```

Interpretation:

Models respond to limitations/boundaries rather than copying method families. This would support a strong scientific-framing mechanism.

### Pattern C — PFM drives nearly all effect

```text
Delta_PFM large
Delta_PFL ≈ Delta_PF ≈ 0
```

Interpretation:

Most of the apparent route steering is method priming / imitation. This substantially weakens the ICLR story.

Unless a deeper baseline interaction or natural-RAG predictive result survives, this should be a KILL or major downgrade.

### Pattern D — RAW large, all standardized conditions weak

Interpretation:

Effect is likely abstract style, direct lexical markers, or extraction artifacts. KILL the high-level scientific-evidence claim.

## 7. Direct-copy diagnostic

For each generated proposal, separately score:

```text
EXACT_METHOD_COPY
NEAR_METHOD_COPY
METHOD_FAMILY_TRANSFER
CONCEPTUAL_TRANSFER
NO_DIRECT_TRANSFER
```

Primary route effects should be recomputed after removing `EXACT_METHOD_COPY` and, as sensitivity, `NEAR_METHOD_COPY` outputs.

A paper-worthy effect should not disappear entirely after this exclusion.

## 8. Evidence-card extraction validity

The standardized card itself can introduce bias. Before generation:

- double-audit a stratified sample against source abstracts/full text;
- verify that P/F/M/L fields contain no invented claims;
- verify that PFL cards do not leak method identity through method-specific proper nouns when avoidable;
- verify that PF cards remain scientifically intelligible;
- measure card-level route lexical separability with a simple bag-of-words classifier.

If the treatment route is nearly perfectly recoverable from a tiny lexicon even in PF, interpretation must remain conservative.

## 9. Relationship to primary paper claim

This experiment is not required to prove that evidence composition affects outputs. It is required to elevate the work from a controlled behavioral phenomenon to a more informative mechanism statement.

Strong paper:

```text
matched scientific evidence
→ high-level research-choice response
→ survives normalization / copy controls
→ component analysis identifies what evidence drives the response
→ baseline propensity modulates response
→ controlled law predicts natural RAG
```

Weak paper:

```text
matched abstracts
→ different proposal words
```

## 10. Priority and sequencing

Do not run the component knockout in the first engineering pilot.

Sequence:

1. source-only feasibility;
2. taxonomy/A-B annotation audit;
3. small RAW matched-evidence pilot;
4. only if RAW high-level response exists, run component knockout on a stratified subset;
5. use component results to decide whether full-scale study is scientifically meaningful.

## 11. Decision

**KEEP / ADD AS SECONDARY MECHANISM EXPERIMENT.**

The component knockout materially strengthens the ability to distinguish scientific evidence use from lexical/method priming, but it should not expand the project before the primary response is shown to exist.