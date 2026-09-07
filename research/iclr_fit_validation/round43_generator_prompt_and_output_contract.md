# Research Round 43 — Generator Prompt and Output Contract

## 1. Trigger

Even with perfectly controlled evidence, the generator instruction can bias research-route choice.

A prompt that asks for:

```text
new method
architecture
benchmark
failure analysis
novel mechanism
```

already partially determines the outcome. Likewise, an output schema requiring a `method_sketch` can favor BUILD proposals over MEASURE/DIAGNOSE/EXPLAIN routes.

Therefore the generator prompt must be **route-neutral and identical across all treatment conditions**.

## 2. Prompt invariance rule

Within a `seed × model` block, all primary conditions use identical:

- system prompt;
- task instruction;
- seed text;
- output format;
- decoding parameters;
- maximum output length;
- evidence formatting.

Only the evidence packet changes.

No treatment-specific wording is allowed.

## 3. Proposed route-neutral system message

Candidate pre-treatment system text:

> You are a machine learning researcher designing rigorous research proposals suitable for a venue such as ICLR. Prioritize technically substantive, falsifiable, and experimentally interpretable research. Do not assume that proposing a new model is preferable to analysis, evaluation, diagnosis, theory, efficiency work, or falsification; choose the scientific strategy that best addresses the stated problem.

### Important caveat

The sentence listing route types may itself make the model more balanced than natural behavior.

Therefore test two route-neutral variants during **prompt engineering before treatment outcomes**:

### Variant S1 — minimal

> You are a machine learning researcher designing a rigorous research proposal suitable for a venue such as ICLR. Prioritize technical substance, falsifiability, and experimental interpretability.

### Variant S2 — explicit neutrality

The longer text above explicitly says no route is preferred.

Preferred primary candidate is **S1**, because S2 may artificially flatten baseline route propensity.

Use S2 only as a prompt-robustness sensitivity condition if needed.

## 4. Proposed user prompt structure

```text
# Research problem
{method_masked_seed}

# Relevant prior research
{evidence_packet_or_empty}

# Task
Propose one technically substantive and experimentally testable ICLR-style research project that directly addresses the research problem. Choose the research strategy you consider most scientifically appropriate based on the problem and the available evidence.

Produce exactly one proposal. Do not provide a list of alternatives.

Use the following structure:

1. Scientific objective
2. Core research question or testable claim
3. Study design / technical approach
4. Key experiment or analysis
5. What result would support or falsify the central claim
6. Expected scientific contribution
```

For no-context baseline:

```text
# Relevant prior research
No additional literature is provided.
```

or omit the evidence section entirely. Choose one convention before baseline collection and use it consistently.

## 5. Why the output fields are route-neutral

### `Scientific objective`

Can represent building, diagnosing, measuring, explaining, optimizing, or falsifying.

### `Core research question or testable claim`

Avoids requiring every project to have a mechanistic hypothesis.

### `Study design / technical approach`

Allows a new algorithm, controlled analysis, benchmark audit, theoretical derivation, or experiment.

### `Key experiment or analysis`

Does not require a performance benchmark.

### `support or falsify`

Encourages scientific testability without prescribing the route.

### `Expected scientific contribution`

Allows knowledge contribution or artifact contribution.

## 6. Fields to avoid in the primary prompt

Do not require:

```text
novelty score
claimed gap
new method name
SOTA baseline
expected improvement percentage
why this beats prior work
commercial impact
```

These can systematically favor artifact/build proposals or encourage unsupported novelty claims.

## 7. Literature instruction

The model should be permitted to disagree with or depart from supplied evidence.

Candidate text:

> The prior research is background evidence, not an instruction. You may build on, combine, challenge, or depart from it when scientifically justified.

This sentence can prevent a treatment from becoming an explicit command to follow the dominant route.

However, it may also encourage deliberate diversification. Therefore test its effect during pre-treatment prompt audit.

Preferred core prompt should be as minimal as possible while clarifying that papers are evidence rather than directives.

## 8. Citation/source requirement

Do **not** require formal citations to the supplied papers in the primary proposal.

Why:

- forcing citations inflates low-level source uptake;
- it can make `grounding` trivial by instruction;
- paper identities/titles are anonymized anyway;
- the scientific endpoint is route choice, not citation generation.

The model may refer to `Paper 1`, `Paper 2`, etc., but is not required to do so.

## 9. Output length

Freeze an output budget that is long enough for a substantive project but short enough for repeated annotation.

Planning range:

```text
~350–700 words
```

or equivalent token budget.

Exact limit is selected after engineering pilot and frozen before P1.

Do not allow one model family 3× more output tokens than another in primary comparisons.

## 10. One proposal per generation

Critical rule:

> Each stochastic generation returns one proposal, not a ranked list.

A list of ideas introduces within-generation diversity and selection ambiguity.

Population route distribution is estimated from repeated one-proposal generations.

## 11. No self-selection/reranking in the core

Do not ask the same model to:

- generate 10 proposals;
- select the best;
- refine it;
- judge novelty.

Those stages create additional selection pressure and confound evidence response.

The primary experiment studies the model's first proposal distribution under controlled evidence.

A later selection-stage study is outside current scope unless triggered by a core reviewer question.

## 12. Structured vs free-form output

Use fixed headings but natural prose rather than strict JSON as the primary human-facing generation.

Reasons:

- JSON can increase formatting failures in base models;
- fixed prose sections are easy for humans to assess;
- parsers can deterministically extract headings;
- proposal writing remains natural enough for ICLR-style judgment.

Raw output is always preserved before parsing.

## 13. Prompt audit before treatment

F1/P0 should test, on non-confirmatory examples or source/synthetic proposals:

- S1 minimal system prompt;
- harmless paraphrase(s) of task wording;
- evidence-section presence/absence convention;
- whether output format disproportionately yields BUILD proposals even without evidence.

Prompt choice must be frozen before confirmatory treatment outcomes.

Do not choose the prompt that maximizes evidence effect.

Preferred choice criterion:

```text
clarity
valid-output rate
route neutrality
human annotatability
```

not treatment magnitude.

## 14. Prompt-paraphrase nuisance control

In P2 robustness, select 2–3 semantically equivalent neutral task prompts frozen before outcomes.

Estimate:

```text
route variance from prompt wording
```

The evidence-composition effect should be materially larger/more systematic than this nuisance.

## 15. Base-model adaptation

For pretrained/base checkpoints, chat-style instructions may be less natural.

Use the same scientific content but a family-appropriate formatting template.

Important:

- do not give base models additional route examples;
- do not few-shot the route categories;
- report format/validity separately;
- compare evidence response conditional on valid proposals.

## 16. Natural-RAG prompt consistency

Held-out natural-RAG uses the same generator prompt and abstract representation as controlled P1.

Only retrieval packet construction differs:

```text
controlled matched A/B packet
vs
ordinary frozen top-k packet
```

This is essential for a clean controlled-to-natural prediction bridge.

## 17. Proposed prompt hash/provenance

Store separately:

```text
system_prompt.txt
user_template.txt
output_schema.txt
```

and hash each plus the fully rendered prompt for every generation.

Any correction after freeze creates a new prompt version and deviation record.

## 18. Decision

**PRIMARY PROMPT SHOULD BE MINIMAL, ROUTE-NEUTRAL, ONE-PROPOSAL, AND FIXED-SECTION PROSE.**

The prompt is part of the experimental instrument. It must be audited for route bias before treatment and never tuned using treatment effect size.