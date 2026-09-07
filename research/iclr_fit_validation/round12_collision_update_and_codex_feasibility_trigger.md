# Research Round 12 — Collision Update and Codex Feasibility Trigger

## 1. Trigger

Continue ICLR-specific validation after Round 11. This round focuses on two remaining risks:

1. whether recent 2026 work already occupies the scientific-prior / evidence-steering space;
2. whether the A/B scientific-route treatment can be made sufficiently objective and comparable to justify a causal experiment.

## 2. New evidence

### 2.1 MetaMuse — ICLR 2026

MetaMuse studies algorithm generation and finds that repeated LLM sampling concentrates around familiar, well-known heuristics. It then uses external stimuli to push ideation into other regions of the solution space.

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2026/hash/85632be2cd69e9a0ef4ba054c096fac9-Abstract-Conference.html

Important implication for us:

- we cannot claim that LLM ideation has a familiarity/default-solution bias;
- we cannot claim that external stimuli can steer ideation;
- our evidence must be **real, scientifically relevant literature**, not arbitrary stimuli, and the contribution must center on matched evidence, prior interaction, and hierarchical uptake.

### 2.2 AI scientists produce results without reasoning scientifically — 2026 preprint

Across >25k agent runs, this work reports frequent failure to use evidence and weak refutation-driven updating, even when strong reasoning traces are available.

Source:
https://arxiv.org/abs/2604.18805

Implication:

- generic “AI scientists ignore evidence” is not novel;
- a publishable result must be more specific: evidence may be read/grounded at low levels while failing to redirect high-level scientific strategy, or the leverage of evidence may depend systematically on the independently measured prior.

### 2.3 Hypothesis generation and updating in LLMs — 2026 preprint

This work studies hypothesis priors/updating in a controlled number-game setting and finds systematic Bayesian-like biases and an evaluation-generation gap.

Source:
https://arxiv.org/abs/2605.05851

Implication:

- we cannot claim first study of LLM hypothesis priors or hypothesis updating;
- our distinct object is open-ended scientific research strategy under realistic literature context.

### 2.4 PreScience and IdeaForecastBench — 2026

PreScience forecasts future scientific contributions and reports a synthetic scientific corpus that is less diverse/novel than real work.

Source:
https://arxiv.org/abs/2602.20459

IdeaForecastBench evaluates whether LLMs can forecast what a research community studies next using historical literature and compares multiple history-compression strategies.

Source:
https://arxiv.org/abs/2609.00747

Implication:

- future-paper / realized-research grounding is no longer novel by itself;
- our held-out natural-RAG prediction should be framed as **mechanism validation of model behavior**, not forecasting future community research.

### 2.5 Evidence-Informed LLM Beliefs for Continual Scientific Discovery — 2026

This work explicitly updates LLM beliefs using retrieved prior discoveries and uses evidence-informed priors for continual discovery.

Source:
https://arxiv.org/abs/2606.29182

Implication:

- avoid generic terminology such as “evidence-informed prior” as the novelty claim;
- our estimand must remain the interaction between an independently measured no-context research preference and a source-only, pre-frozen literature treatment.

## 3. Previous belief

Before this round, the surviving novelty family was:

> Real scientific literature, matched on relevance and amount, can steer an LLM among multiple valid scientific routes; the response depends on its independently measured scientific prior and may decay with abstraction level.

## 4. Update

The core survives, but the novelty boundary is narrower.

The paper must NOT claim any of the following as new:

- scientific ideation has default/familiar-solution bias;
- context can override a model prior;
- external stimuli can broaden ideation;
- scientific agents can ignore evidence;
- LLMs have hypothesis priors;
- literature history can be used to forecast later research;
- retrieved evidence can update scientific beliefs.

The defensible joint question is now:

> **For multiple scientifically plausible research routes chosen without observing model behavior, how does the composition of equally relevant real scientific literature change open-ended route selection, and how is that response modulated by the model's independently measured no-context preference?**

A secondary high-value question is:

> Does context uptake remain strong for source/concept grounding while weakening for higher-level method/research-route/problem framing?

## 5. Primary outcome redesign

Do not make the six-way global taxonomy the sole primary endpoint.

For each seed-specific frozen route pair `(A, B)`, use a simpler blinded endpoint:

```text
A-leaning
B-leaning
MIXED
NEITHER
INVALID
```

The global scientific-move taxonomy remains useful for cross-seed aggregation and diagnostics, but the causal treatment effect can be defined locally.

This reduces the dependence of the paper on globally disputable category boundaries.

## 6. Route-pair design rule

Use a predeclared global roster of route contrasts, for example:

```text
BUILD_IMPROVE vs DIAGNOSE_STRESS_TEST
BUILD_IMPROVE vs MEASURE_EVALUATE
BUILD_IMPROVE vs EXPLAIN_MECHANISM_THEORY
DIAGNOSE_STRESS_TEST vs EXPLAIN_MECHANISM_THEORY
```

For each seed, include **every predeclared contrast** that satisfies the source-only eligibility and matching rules. Do not choose only the most dramatic pair.

Treatment selection must be completed before measuring the generator's no-context prior.

## 7. Updated causal estimand

For seed `s`, model `m`, route pair `(A,B)`, and evidence mixture `alpha`:

```text
Y ∈ {A, B, MIXED, NEITHER, INVALID}
```

Main response:

```text
P(Y=A | alpha, prior_A, seed, model)
```

with

```text
alpha ∈ {0, .25, .50, .75, 1.0}
```

and `prior_A` estimated only after route/evidence treatments are frozen.

Primary scientific test:

```text
evidence mixture effect
+
no-context prior effect
+
evidence × prior interaction
```

## 8. Why MetaMuse is not a direct collision

MetaMuse deliberately uses external stimuli, often domain-unrelated dictionary words, to induce creative jumps in two algorithm-design tasks. Our proposed design instead uses:

- real ICLR literature;
- scientifically relevant alternatives;
- matched relevance and context amount;
- multiple valid high-level scientific routes;
- treatments selected before observing model outputs;
- independently estimated no-context priors;
- controlled mixture dose response;
- natural-RAG held-out prediction;
- hierarchical source-to-problem uptake.

MetaMuse therefore materially narrows our claim but does not currently invalidate it.

## 9. Codex trigger decision

### Decision: LIMITED CODEX WORK IS NOW JUSTIFIED

The next unresolved question is no longer primarily conceptual:

> **Does the ICLR corpus actually contain enough route-balanced, relevance-matchable evidence to instantiate this design across a meaningful number of seeds/subfields?**

This is a data-engineering / feasibility question and is an appropriate Codex task.

However, Codex must still NOT run scientific-generation outcomes.

### Allowed Codex scope

Codex may now perform a **source-only feasibility audit**:

1. collect/freeze candidate ICLR 2025 evidence metadata and candidate later seed questions;
2. record first-public dates and possible earlier versions where programmatically available;
3. implement the frozen draft route labels only as a provisional source annotation layer;
4. compute, for every seed and every predeclared route pair:
   - eligible paper count per route;
   - relevance distributions;
   - token-length/year distributions;
   - whether matched packets of fixed `k` are feasible;
5. output seed × route-pair matchability tables;
6. retain all failures and exclusions.

### Forbidden Codex scope

Do NOT:

- generate research ideas;
- estimate model priors;
- inspect treatment outcomes;
- tune matching criteria to maximize later effects;
- select route pairs based on model outputs;
- write paper claims.

## 10. Feasibility gate

Continue toward scientific generation only if the source-only audit shows:

- multiple route contrasts are feasible across multiple ICLR subfields;
- matched relevance is achievable without systematically weakening one route;
- route annotations are auditable and not dominated by trivial keywords;
- enough temporally clean evidence remains after first-public-date filtering;
- the design does not collapse to a tiny cherry-picked seed subset.

If these fail, redesign or kill before spending inference budget.

## 11. Decision

**MODIFY + CONTINUE.**

The topic survives the new 2026 collision scan, but only under the narrower prior×matched-evidence / hierarchical-uptake claim. A limited source-only Codex feasibility audit is now scientifically useful and does not contaminate the experiment.

## 12. Next action

1. Write a frozen Codex feasibility task contract.
2. Keep web research running in parallel for direct collisions.
3. Do not authorize scientific generation until the source-only feasibility gate is reviewed.
