# Research Round 21 — Sampling, Precision, and Replication Design

## 1. Trigger

Round 19 defined the core estimands. The next design question is how to allocate generation budget without creating pseudo-replication.

The main scientific unit is the `seed × route-pair block`; repeated generations within a block estimate a conditional distribution.

This round uses simple synthetic simulations only to guide allocation. No project treatment data are used.

---

## 2. Design principle

For heterogeneous scientific questions, **more independent blocks are generally more valuable than extremely deep sampling of a small number of blocks**.

Why:

```text
within-block generations
    -> reduce Monte Carlo uncertainty for one conditional distribution

independent seed-route blocks
    -> reduce uncertainty about the population-level average and heterogeneity
```

If the project samples 1,000 generations from three seeds, it still has only three substantive research-problem replications.

---

## 3. Synthetic planning simulation

A simplified binary endpoint simulation was used only to understand scale:

- blocks have heterogeneous baseline probabilities;
- block-level treatment effects vary around a population mean;
- each endpoint condition is sampled repeatedly;
- inference is performed on block-level treatment differences.

This is not the final statistical model and not empirical data.

### Illustrative findings

Under a synthetic mean endpoint shift around `0.20`, even ~12–18 independent blocks can often identify a population-average directional effect if it is genuinely that large.

For a smaller synthetic average effect around `0.10`, increasing independent blocks matters much more:

```text
~18 blocks: often underpowered / wide uncertainty
~24 blocks: improved but still borderline
~30 blocks: useful planning target
~36 blocks: substantially more stable
~48 blocks: strong precision if feasible
```

Increasing per-condition generations from roughly 30 to 50 helps, but less than adding independent blocks once per-block probabilities are estimated reasonably well.

These are qualitative planning conclusions from a deliberately simplified simulation; do not report these numbers as formal power analysis in the paper.

---

## 4. Proposed staged sampling design

### Stage A — Engineering / annotation pilot

Purpose:

- confirm prompt/output validity;
- estimate invalid/mixed rates;
- estimate annotation agreement;
- verify packet construction;
- estimate within-block variance.

Suggested scale after source-only authorization:

```text
8–12 blocks
× 2 core model families
× 5 alpha levels
× 20–30 generations
```

Do not use Stage A to select favorable route pairs or subfields.

### Stage B — Scientific pilot

Purpose:

- estimate plausible effect and heterogeneity ranges;
- test anti-lexical controls;
- decide final precision-based N before a confirmatory expansion.

Target envelope:

```text
18–24 blocks
× 2 core model families
× 5 alpha levels
× 30–40 generations
```

Include no-context baseline and preregistered control subset.

### Stage C — Confirmatory full study

Preferred target if source coverage permits:

```text
30–40 independent seed-route blocks
```

with:

```text
~40–60 generations per mixture condition
```

for the two core model families.

The exact count should be frozen after Stage B using a precision rule or fixed-N rule. Do not choose N based on which hypothesis is significant.

---

## 5. Precision target

The final sample-size rule should focus on uncertainty of the **population average across blocks**, not raw generation count.

Candidate criterion:

> Choose a fixed number of eligible blocks and generations such that the expected 95% interval for the population-average extreme directional response is sufficiently narrower than the minimum effect regarded as scientifically meaningful, with a preregistered maximum budget.

A practical alternative is simply to freeze all source-feasible eligible blocks up to a predetermined cap, which minimizes selection discretion.

### Preferred policy if enough blocks exist

If source-only feasibility yields `<= 50` eligible high-quality blocks, consider using **all eligible blocks** that pass the frozen gate rather than sampling a favorable subset.

This makes the target population and denominator especially transparent.

---

## 6. Block-level stratification

Do not let the full sample become dominated by one subfield or one route contrast.

Predeclare minimum diversity such as:

- >=3 ICLR subfields;
- >=2 route-pair contrasts in the primary analysis;
- no single subfield >50% of blocks unless the source universe forces it;
- report route-pair and subfield-specific effects before pooling.

If only one route contrast is widely feasible, narrow the paper claim explicitly rather than pretending cross-route generality.

---

## 7. Replicates and seeds

Each generation record must preserve:

```text
block_id
model_id
alpha
packet_id
prompt_id
sampling_seed
decoding parameters
raw output
```

### Sampling seed policy

Use deterministic pre-generated seed lists shared across conditions where technically meaningful.

Do not regenerate selectively after parse failures. Retain invalid outputs.

### Packet replication

For each alpha, use multiple matched packet realizations where source pool permits, rather than one packet repeated hundreds of times.

This separates:

```text
evidence-composition effect
from
idiosyncratic paper-packet identity
```

A useful design is:

```text
3–5 packet realizations per alpha
× 10–15 generations per packet
```

rather than 50–75 generations from one packet.

This is preferable if matching feasibility supports it.

---

## 8. Hierarchical analysis structure

Primary analysis should model at least:

- evidence fraction / treatment composition;
- baseline route propensity;
- evidence × baseline interaction;
- model family;
- route-pair identity;
- subfield;
- seed/block random effects;
- packet realization random effects where applicable.

Do not treat generation-level rows as exchangeable independent observations.

Candidate multilevel multinomial or Bayesian hierarchical model is preferable to thousands of independent chi-square tests.

Block-level bootstrap should resample blocks, not individual generations, for population-level uncertainty.

---

## 9. Heterogeneity is a result, not nuisance only

Predefine heterogeneity questions:

1. Which blocks are highly evidence-responsive?
2. Which blocks are resistant?
3. Does baseline route propensity explain that difference?
4. Does route contrast type explain it?
5. Does subfield explain it?
6. Does model/post-training status explain it?

A strong paper may be driven more by a stable **response law / heterogeneity structure** than by one large average effect.

Do not hide negative blocks.

---

## 10. Natural-RAG held-out set

Natural-RAG validation needs a genuinely separate target set.

Recommended:

- freeze a subset of eligible blocks before treatment fitting;
- do not use their natural-RAG outputs or route outcomes when fitting controlled-response coefficients;
- estimate baseline route propensities independently;
- observe their natural packet composition;
- predict route distributions using the frozen response model.

Potential split:

```text
70–80% controlled-response development/fit
20–30% held-out natural-RAG validation
```

Exact split should be frozen after source-only feasibility reveals the number of eligible blocks.

If the eligible sample is too small to support a credible held-out set, downgrade the natural-RAG claim rather than reusing training blocks.

---

## 11. Base vs instruction-tuned comparison

Do not double the entire main experiment automatically.

Recommended secondary design:

- select a preregistered stratified subset of blocks;
- run paired base/instruct checkpoints on exactly the same packets;
- separately report valid-output rates;
- analyze evidence response conditional and unconditional on valid outputs.

This concentrates compute on a hypothesis strongly motivated by existing ICLR context-reliance results without making the main study intractable.

---

## 12. Multiple-comparison discipline

Primary confirmatory quantities should be limited to:

1. average evidence-conditioned directional response;
2. evidence × baseline propensity interaction;
3. preregistered abstraction-level contrast or hierarchy statistic;
4. held-out natural-RAG predictive improvement.

Everything else should be clearly secondary/exploratory.

Do not fish across dozens of route/subfield/model interactions and promote the strongest post hoc subgroup.

---

## 13. Decision

**KEEP.**

The preferred full-study strategy is breadth-first:

> maximize the number of valid independent seed-route blocks before dramatically increasing generations within a block.

Source-only feasibility remains the immediate bottleneck. No scientific model outcomes are authorized yet.
