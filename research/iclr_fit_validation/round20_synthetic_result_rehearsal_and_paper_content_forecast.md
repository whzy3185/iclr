# Research Round 20 — Synthetic Result Rehearsal and Paper Content Forecast

## 1. Purpose

This document contains **synthetic, hypothetical numbers only**. No values below are project results.

The goal is to rehearse what different empirical outcomes would mean before any scientific treatment generation exists, and to prevent result-contingent storytelling.

The experiment is considered valuable only if the observed data support a predeclared scientific interpretation that survives the main validity controls.

---

# 2. Common setup for the synthetic examples

For a seed-local route pair `(A,B)`:

```text
alpha = fraction of route-A evidence in a matched packet
alpha in {0, .25, .50, .75, 1}
```

Primary labels:

```text
A_LEANING
B_LEANING
MIXED
NEITHER
INVALID
```

Directional response:

```text
D(alpha) = P(A_LEANING) - P(B_LEANING)
```

All values below are illustrative only.

---

# 3. Branch S — Strong scientific choice response

## 3.1 Synthetic example

Hypothetical pooled valid unconditional probabilities:

| alpha(A evidence) | P(A) | P(B) | P(Mixed) | P(Neither/Invalid) | D(alpha) |
|---:|---:|---:|---:|---:|---:|
| 0.00 | .16 | .62 | .12 | .10 | -.46 |
| 0.25 | .27 | .51 | .13 | .09 | -.24 |
| 0.50 | .41 | .38 | .13 | .08 | +.03 |
| 0.75 | .57 | .25 | .11 | .07 | +.32 |
| 1.00 | .69 | .16 | .09 | .06 | +.53 |

Extreme directional shift:

```text
Delta_extreme = +0.99
```

Again: this is a deliberately clear synthetic scenario, not an expected effect size.

### Content-normalized robustness example

| alpha | D_RAW | D_NORMALIZED |
|---:|---:|---:|
| 0.00 | -.46 | -.34 |
| 0.25 | -.24 | -.18 |
| 0.50 | +.03 | +.01 |
| 0.75 | +.32 | +.22 |
| 1.00 | +.53 | +.36 |

Interpretation:

- some RAW effect is attributable to direct route cues;
- a substantial directional effect remains when obvious lexical/future-work cues are reduced;
- therefore the phenomenon cannot be summarized only as copying route words.

## 3.2 What would make this ICLR-level rather than obvious priming

Need at least two of:

1. same evidence composition has different leverage depending on independently measured baseline route propensity;
2. response curve is nonlinear / thresholded / asymmetric in a repeatable way;
3. cross-route swaps are much larger than within-route document swaps;
4. normalized evidence preserves a meaningful effect;
5. controlled response predicts held-out natural-RAG route choices.

## 3.3 Likely paper identity

Candidate neutral title:

> **Same Relevance, Different Research Choices: How Scientific Evidence Shapes LLM Hypothesis Search**

Alternative if predictive mechanism is especially strong:

> **From Evidence Composition to Research Choice: Predicting Literature-Conditioned LLM Scientific Search**

Avoid claiming generic discovery of context steerability.

## 3.4 Abstract-level content

Possible abstract logic, conditional on real evidence:

1. Literature-grounded research agents are usually evaluated by citation correctness, final quality, novelty, or duplicate diversity.
2. These metrics do not tell us whether literature changes the high-level research strategy selected by the model.
3. Construct temporally clean ICLR question/evidence blocks with two independently frozen, equally admissible scientific routes and matched relevance.
4. Vary only evidence-route composition.
5. Find a reproducible evidence-conditioned redistribution of research choices.
6. Show that the magnitude depends on baseline route propensity and survives anti-copy controls.
7. Use the controlled response law to predict route choices under ordinary retrieval on held-out questions.
8. Conclude that literature composition is a measurable control variable over scientific search behavior, not merely a source of facts/citations.

---

# 4. Branch H — Hierarchical evidence uptake / weak high-level movement

## 4.1 Synthetic example

Suppose the route-choice curve is much weaker:

| alpha | P(A) | P(B) | D(alpha) |
|---:|---:|---:|---:|
| 0.00 | .24 | .50 | -.26 |
| 0.25 | .28 | .47 | -.19 |
| 0.50 | .32 | .43 | -.11 |
| 0.75 | .36 | .40 | -.04 |
| 1.00 | .40 | .36 | +.04 |

But evidence uptake by abstraction level is hypothetically:

| Uptake level | Rate |
|---|---:|
| source / named evidence | .88 |
| scientific concept/finding | .79 |
| concrete method family | .56 |
| high-level route | .28 |
| central problem framing | .19 |

This is synthetic only.

## 4.2 Potential scientific interpretation

The model is sensitive to literature, but sensitivity attenuates with the level of decision abstraction.

This would be stronger if:

- the attenuation reproduces across model families;
- low-level uptake remains high after source/order controls;
- high-level movement is especially weak against a strong baseline route propensity;
- instruction-tuned models show stronger attenuation than matched base models;
- natural RAG is accurately described as highly grounded but only weakly route-changing.

## 4.3 Paper viability

Potentially strong, but only if there is a **structured hierarchy or interaction**, not merely a null high-level effect.

Candidate title should avoid crowded `grounding without ...` language.

Possible:

> **Where Scientific Context Stops Mattering: Hierarchical Evidence Reliance in LLM Research Ideation**

or

> **Reading Is Not Redirecting: Abstraction-Dependent Context Reliance in LLM Scientific Search**

These are placeholders, not frozen titles.

## 4.4 Required additional experiments

- content-normalized context;
- direct-copy exclusion;
- base vs instruction-tuned checkpoint pair;
- same evidence packet across models with different baseline route propensity;
- natural-RAG placement on the controlled response curve.

Without these, a weak route response is too easy to interpret as noisy annotation or inadequate treatment.

---

# 5. Branch P — Raw priming only: statistically strong but scientifically weak

## 5.1 Synthetic example

RAW abstracts:

| alpha | D_RAW |
|---:|---:|
| 0.00 | -.50 |
| 0.25 | -.25 |
| 0.50 | .00 |
| 0.75 | +.28 |
| 1.00 | +.55 |

Content-normalized evidence:

| alpha | D_NORMALIZED |
|---:|---:|
| 0.00 | -.07 |
| 0.25 | -.04 |
| 0.50 | .00 |
| 0.75 | +.03 |
| 1.00 | +.05 |

Direct method copying accounts for most A/B-labeled outputs.

## 5.2 Decision

**KILL intended paper.**

Do not claim scientific choice steering.

Interpretation is simply that route-indicating words/method descriptions prime corresponding text.

This can be an appendix diagnostic or a negative result guiding a different topic, but not the intended ICLR contribution.

---

# 6. Branch N — Genuine null

## 6.1 Synthetic example

| alpha | D(alpha) |
|---:|---:|
| 0.00 | -.05 |
| 0.25 | -.03 |
| 0.50 | -.04 |
| 0.75 | -.01 |
| 1.00 | +.00 |

Low-level evidence uptake may or may not occur.

## 6.2 Decision

Two possibilities:

### N1 — high grounding, zero route response

Potentially interesting **only** if a robust abstraction hierarchy and baseline-resistance mechanism exists.

### N2 — little grounding and no route response

KILL. The treatment likely does not engage the model strongly enough or the question is uninformative.

Do not force an evaluation paper out of a generic null.

---

# 7. Branch F — Feasibility failure before model generation

Possible source-only outcomes:

- temporally clean ICLR 2025 corpus becomes too small after first-public-date filtering;
- most seeds have only one scientifically plausible route with enough relevant papers;
- A/B evidence cannot be matched on relevance;
- global route taxonomy cannot be annotated reliably;
- source-only route pairs are dominated by one subfield or one route contrast.

### Decision

KILL or redesign before generation.

This is a successful use of preregistration: avoiding a large, uninterpretable LLM experiment.

---

# 8. Current subjective planning prior

Not data and not a formal Bayesian prior.

The most plausible empirical shape is currently judged to be between Branch S and Branch H:

> evidence will probably produce measurable movement, but high-level research-route choice will be substantially less responsive than low-level content uptake and will vary strongly by model/seed.

Reasons for this expectation from neighboring work:

- default scientific-method suggestions are highly concentrated across strong LLMs;
- external stimuli can move algorithm ideation outside familiar solution regions;
- models can nevertheless ignore or under-use evidence in scientific-agent settings;
- post-training can reduce in-context distributional steerability;
- small semantic/context-description changes can have large choice effects, making some RAW movement likely.

Therefore the **scientifically informative object is likely heterogeneity and attenuation**, not a simple yes/no effect.

---

# 9. What the final main figures would probably be

If the intended paper survives:

## Figure 1 — Experimental design + response curve

One visual:

```text
same seed
same relevance
same k
A/B evidence composition changes
        ↓
open-ended research proposal
        ↓
blinded A/B route label
```

plus pooled dose-response.

## Figure 2 — Baseline propensity × evidence response

Demonstrate why the phenomenon is more than content priming.

## Figure 3 — RAW vs normalized / within-route swap controls

Show what fraction of response survives obvious textual explanations.

## Figure 4 — Abstraction profile

Source/concept/method/route/problem-framing uptake.

## Figure 5 — Held-out natural RAG

Predictive calibration / log-loss comparison:

```text
baseline-only
vs
baseline + evidence composition
```

## Main Table — Block eligibility and treatment validity

Report the denominator and exclusions prominently.

---

# 10. Forecast paper section structure

```text
1 Introduction
2 Related Work
   2.1 Context vs parametric/default behavior
   2.2 Scientific ideation and methodology concentration
   2.3 Literature-grounded research agents
3 Measuring Evidence-Conditioned Scientific Choice
   3.1 ICLR seed/evidence construction
   3.2 Route admissibility and treatment freeze
   3.3 Outcomes and annotation
4 Controlled Evidence-Composition Experiments
5 Baseline-Dependent Response and Abstraction Effects
6 Predicting Natural Retrieval Behavior
7 Robustness: Matching, Copying, Lexical and Prompt Controls
8 Discussion and Limitations
```

The paper should not lead with `AI monoculture` or `better RAG`.

---

# 11. Decision rule frozen by this rehearsal

A statistically significant treatment coefficient is not sufficient.

For the intended ICLR paper, at least one of the following must be strong and replicated in addition to a valid route response:

1. baseline-dependent response;
2. abstraction-dependent evidence uptake;
3. robust non-lexical route response;
4. held-out natural-RAG predictive gain.

Preferably two or more.

If the final story can still be summarized as:

> “the model tends to propose the kind of method described in its context,”

then the intended paper has failed.

---

## 12. Status

**KEEP / CONDITIONAL GO.**

No project treatment outcomes existed when this synthetic rehearsal was written.
