# Research Round 57 — Experimental Scale Benchmark Against Closest Related Work

Date: 2026-09-08

## Purpose

Benchmark the scale and structure of experiments in the closest scientific-ideation, steerability, and controlled-choice papers, and use them to calibrate the target scale of our study.

## Closest experiment archetypes

### Si et al., ICLR 2025 — Can LLMs Generate Novel Research Ideas?

- 7 NLP topics.
- 49 human-written ideas, 49 AI ideas, 49 AI+human-rerank ideas.
- 79 expert reviewers; 104 unique human participants across writing/reviewing.
- Nearly 300 blind reviews.
- Heavy emphasis on controlling topic distribution, writeup format, and blind human evaluation.

Takeaway: scientific ideation papers can be relatively small in number of independent research ideas if human evaluation and confound control are unusually strong.

### Ideation Arena, 2026

- 14 frontier LLMs.
- 5 research-agent architectures built on 2 base models.
- Shared literature contexts.
- >6,000 double-blind pairwise comparisons.
- 105 active CS researchers.

Takeaway: when the question is system ranking / expert preference, experimental credibility comes from many systems plus large-scale human comparisons rather than huge numbers of research problems.

### Lit2Test, 2026

- 200 real-paper neighborhoods.
- 4 frontier models.
- 1,200 blind pairwise comparisons, evaluated in both presentation orders.
- 3 human annotators for calibration/corroboration.
- 10,000 bootstrap replicates for ranking robustness.

Takeaway: a few hundred independent scientific contexts can support a strong benchmark when the task and evaluation contract are tightly specified.

### Spectrum Tuning, ICLR 2026

- >40 data sources.
- >90 tasks.
- 3 model families.
- Evaluates distributional coverage, alignment, and in-context steerability, including held-out evaluation.

Takeaway: broad behavioral claims require broad task coverage; our narrower scientific-choice claim need not match 90 tasks, but must compensate with stronger per-seed construct validity and causal controls.

### CLASH, ICLR 2026

- 345 high-stakes dilemmas.
- 3,795 individual perspectives.
- Current ICLR version benchmarks 14 models.
- Studies baseline preference, perspective steering, ambivalence, and value shifts.

Takeaway: context/preference-steering papers typically combine hundreds of independent situations with many models; if we use only 2 models, our treatment identification and repeated packet intervention must be correspondingly stronger.

### BiasBusters, ICLR 2026

- 7 LLMs.
- Multiple categories of functionally equivalent tools.
- Controlled perturbations of metadata, descriptions, order, and pretraining exposure.

Takeaway: controlled-choice papers are accepted when alternatives are carefully matched and nuisance variables are manipulated explicitly; very large task counts are not the only route to strength.

### MetaMuse, ICLR 2026

- 2 high-impact algorithmic problems.
- 3 main LLM backbones (GPT-4o, Llama-3.3-70B, DeepSeek-V3).
- 21 baselines overall.
- Each method targets 350 executable solutions per experiment.
- Evaluation on 96 cache workloads and 288 bin-packing workloads.

Takeaway: a paper can study only two problem families if it has high experimental depth, strong executable evaluation, many baselines, and repeated solutions.

## Implication for our study

Our unit is more expensive than a benchmark item because each confirmatory unit requires:

1. a human-certified open scientific seed;
2. two plausible, non-subsumed research routes;
3. matched literature slots;
4. repeated packet realizations;
5. multiple stochastic generations;
6. blind human route annotation.

Therefore matching Spectrum/CLASH in raw task count is unnecessary. We should target depth similar to controlled behavior work and independent-seed breadth sufficient for seed-level inference.

## Recommended scale

### Development pilot

- 8–12 certified seeds.
- 2 model families.
- alpha = 0, 0.5, 1.
- 2–3 independent packet realizations per seed/route/model/alpha.
- 6–10 generations per packet.

Approximate generation count: 600–2,200. This stage is for variance, annotation reliability, invalid rates, packet noise, and engineering validation, not paper claims.

### Minimum defensible confirmatory core

- 24–30 independent certified seeds.
- 2 model families.
- 5 alpha levels.
- >=2 packet realizations.
- 6–8 generations per packet.

Approximate generation count: 3,000–5,000.

This can be publishable only if seed/route certification is strong, effect is replicated across both model families, and anti-priming controls survive.

### Recommended ICLR-scale core

- 30–50 independent certified seeds.
- 2–3 model families.
- 5 alpha levels.
- 3 packet realizations.
- 5–8 generations per packet.

Typical generation count: roughly 5,000–18,000.

A concrete balanced target is:

36 seeds × 2 models × 5 alpha × 3 packet banks × 5 generations = 5,400 generations.

A stronger version:

40 seeds × 3 models × 5 alpha × 3 packet banks × 8 generations = 14,400 generations.

## Human annotation recommendation

Do not double-label every generation by default. Use:

- all outputs receive one blind primary route label;
- 20–30% stratified random subset receives an independent second label;
- all disagreements in the reliability subset are adjudicated;
- increase double-label fraction only if agreement is below the frozen F1 threshold.

This provides a human anchor without requiring Ideation-Arena-level 6,000 pairwise expert comparisons.

## Model breadth recommendation

Two independent model families are sufficient for the minimum causal paper if both replicate. Three models/families make the paper substantially stronger. More than 3–4 is lower priority than adding independent certified seeds.

## Main calibration conclusion

The closest ICLR papers fall into three successful scale regimes:

1. **small independent scientific sample + expensive expert evaluation** (Si et al.);
2. **hundreds of contexts + many models** (CLASH, Lit2Test, Spectrum);
3. **few problem families + very deep executable repeated evaluation** (MetaMuse).

Our best strategy is a hybrid: 30–50 independent human-certified scientific seeds, 2–3 model families, repeated matched-packet interventions, and a targeted human annotation reliability layer. We should not chase hundreds of seeds if certification becomes weak, nor rely on 5–10 seeds with thousands of generations.

## Decision

Target the 30–50 seed regime after F1 certification. If F1 yields <20 high-quality independent seeds, narrow the claim or expand the source universe before launching a full confirmatory study. If 30–50 survive, the proposed experiment is within the scale of accepted adjacent ICLR work, with stronger causal control than most ideation benchmarks.