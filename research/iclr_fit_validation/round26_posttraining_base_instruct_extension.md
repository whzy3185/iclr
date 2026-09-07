# Research Round 26 — Post-Training / Base-vs-Instruct Extension

## 1. Trigger

The core study can establish evidence-conditioned scientific-choice response, but a stronger ICLR contribution would connect this behavior to a general property of model post-training.

ICLR 2025 Context-Parametric Inversion reports that instruction finetuning can eventually reduce context reliance. ICLR 2026 Spectrum Tuning reports that post-training can reduce in-context steerability and distributional coverage. These results motivate—but do not determine—the following scientific extension:

> Does instruction/post-training alter how strongly scientific evidence can redirect high-level research choices?

This is pre-result motivation, not a prediction that instruction-tuned models must be less steerable.

## 2. Paired-family design

Where feasible, evaluate paired checkpoints from the same family:

```text
Family 1:
  pretrained/base checkpoint
  instruction-tuned checkpoint

Family 2:
  pretrained/base checkpoint
  instruction-tuned checkpoint
```

Preferred families remain those with auditable data/knowledge cutoffs and accessible weights.

Exact checkpoint IDs must be frozen before scientific generation.

## 3. Important validity issue: task coherence

Base models may be worse at following the research-proposal instruction. Therefore raw variability is not evidence of scientific steerability.

For every checkpoint report:

```text
VALID_OUTPUT_RATE
SEED_RELEVANCE
FORMAT_COMPLIANCE
SCIENTIFIC_COHERENCE
```

Primary post-training comparison should include:

1. unconditional treatment response;
2. treatment response conditional on valid/relevant output;
3. invalid-rate difference as a separate outcome.

Do not interpret incoherent base-model outputs as broader exploration.

## 4. Shared treatment packets

The most important control is that base and instruct checkpoints receive the **same frozen seed-route blocks and identical evidence packets** whenever context length permits.

This creates a matched comparison:

```text
same family
same seed
same evidence packet
same alpha
same source literature
↓
training state differs
```

This is much cleaner than comparing unrelated model families.

## 5. Response quantities

For each checkpoint estimate:

```text
Delta_route
  = route-score change from all-B to all-A evidence

Slope_route
  = dose-response slope / monotonic contrast

Baseline_propensity
  = no-context A-vs-B route tendency

Uptake_profile
  = L0/L1/L2/L3/L4 context-uptake response
```

Compare:

```text
Delta_instruct - Delta_base
```

within family and block.

## 6. Pre-specified possible outcomes

### Outcome PT-A — instruction tuning reduces high-level evidence response

If:

```text
Delta_instruct < Delta_base
```

while instruct outputs are more coherent and lower-level grounding remains strong, this would align with the broader ICLR finding that post-training can strengthen task-following while reducing flexible distributional adaptation.

A strong version would be:

```text
source/concept uptake similar or higher after instruction tuning
but high-level route response lower
```

This would be a compelling extension.

### Outcome PT-B — instruction tuning increases scientific evidence response

This is equally scientifically valid.

Interpretation:

Research ideation may differ from factual context-conflict tasks because instruction tuning teaches models to use complex literature context more effectively.

This would show task-dependent context adaptation rather than reproduce Spectrum/Context-Parametric results.

### Outcome PT-C — no consistent post-training effect

Then model-family-specific baseline/evidence interaction remains the main story. Do not force a post-training claim.

### Outcome PT-D — base outputs mostly invalid

Then base-vs-instruct is not an interpretable primary comparison and should remain a limitation/secondary appendix result.

## 7. Interaction with baseline propensity

Post-training may change both:

```text
baseline route propensity
and
evidence response
```

Therefore do not compare slopes without accounting for changed baseline.

Useful model:

```text
route_score
 ~ evidence_exposure
 + baseline_propensity
 + evidence_exposure × baseline_propensity
 + tuning_state
 + evidence_exposure × tuning_state
 + block effects
```

The central post-training question is whether tuning state explains residual evidence response after baseline route tendency is included.

## 8. Same-family natural-RAG validation

If both base and instruct models yield valid enough outputs, apply the same controlled-fit → natural-RAG prediction pipeline separately.

Interesting result:

```text
instruction-tuned model has higher proposal quality
but lower gain from evidence-composition features over baseline-only prediction
```

or the reverse.

Again, no direction is assumed.

## 9. Avoid over-expansion

This extension should not block the core experiment.

Recommended order:

1. validate source-only feasibility;
2. run core instruct-model pilot;
3. confirm primary evidence response / interpretable null;
4. add base checkpoint on a representative block subset;
5. scale paired-family comparison only if base output validity is sufficient.

## 10. Paper value

Without this experiment, the paper can still be an ICLR controlled behavioral/mechanistic study.

With a robust same-family post-training effect, the paper becomes more general:

> scientific evidence response is not merely an application-specific property of research agents; it is systematically shaped by model post-training.

## 11. Decision

**HIGH-VALUE SECONDARY EXTENSION; DO NOT BLOCK CORE PILOT.**

The paired base-vs-instruct study is worth pre-registering because it directly connects the scientific ideation setting to established ICLR questions about context reliance and distributional steerability.