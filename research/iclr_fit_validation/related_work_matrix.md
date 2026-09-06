# ICLR-Focused Related-Work / Collision Matrix

> Purpose: prevent us from rediscovering an existing idea and force every claimed contribution to have a clear nearest-neighbor distinction.

| Work | Venue/status | Core object | What it establishes | Collision with us | Required distinction / use |
|---|---|---|---|---|---|
| Padmakumar & He, *Does Writing with Language Models Reduce Content Diversity?* | ICLR 2024 | human+LLM co-writing | InstructGPT assistance reduces collective content diversity; model-contributed text explains much of effect | conceptual population-diversity precedent | cite as ICLR archetype; our object is LLM evidence-conditioned hypothesis distribution, not human writing |
| *Context is Environment* | ICLR 2024 | in-context behavior | context can function as an environment shaping model behavior | conceptual | use only as broad context-behavior precedent; not a novelty claim |
| Si et al., *Can LLMs Generate Novel Research Ideas?* | ICLR 2025 | scientific ideation | LLM ideas can look novel to experts; diversity and self-evaluation are bottlenecks | **very high** | reproduce/acknowledge RAG-quantity null; study composition + structured context response instead |
| Si et al. Appendix A.29 | ICLR 2025 | RAG ablation | k=0/5/10/20 has little effect on near-duplicate rate; backbone effect large | **decisive baseline** | main paper should explain a dimension their metric/ablation does not test |
| *Context-Parametric Inversion* | ICLR 2025 | context-vs-parametric reliance | instruction tuning can eventually reduce reliance on context under knowledge conflicts | **high conceptual** | do not claim first study of prior-vs-context reliance; scientific ideation is open-ended rather than factual conflict, and we study structured search distributions |
| *Controllable Context Sensitivity and the Knob Behind It* | ICLR 2025 | context sensitivity | identifies a model subspace controlling context-vs-prior factual answers | **high conceptual** | our target is distributional/open-ended scientific search, not correctness under counterfactual facts; useful mechanistic control/terminology |
| REGENT | ICLR 2025 | retrieval-augmented agents | retrieval provides a powerful adaptation bias | medium conceptual | never claim generic “retrieval is a bias”; claim composition-specific structured effects over open-ended hypothesis search |
| Spectrum Tuning | ICLR 2026 | conditional distributional modeling | defines **in-context steerability** as using novel context to override a prior and steer toward a new output distribution; post-training can hurt it | **very high conceptual neighbor** | reuse/adapt the steerability framing rather than claim it; ask whether literature context can override scientific-method priors and at what abstraction level |
| BiasBusters | ICLR 2026 | controlled selection bias | functionally equivalent tools + controlled metadata/position/pretraining interventions reveal systematic selection bias across 7 LLMs | **strong design archetype** | emulate matched-alternative interventions and order controls for equally relevant evidence/method families |
| STARS | ICLR 2026 | LM generation diversity | inference-time activation steering broadens generation, incl. scientific discovery | high if we propose diversity algorithm | use as generation-side control; distinguish sampling breadth from context-driven search direction |
| *Mixing Mechanisms* | ICLR 2026 | in-context retrieval mechanism | decomposes multiple mechanisms and builds causal predictive model | paper-shape precedent | emulate mechanism/predictive rigor, not necessarily activation-level interpretation |
| LUMINA | ICLR 2026 | RAG context/knowledge utilization | RAG hallucination tied to imbalance between external context and internal knowledge; quantifies utilization signals | medium/high conceptual | factual hallucination vs open-ended hypothesis search; avoid generic “models ignore RAG” claim |
| *Copy-Paste to Mitigate LLM Hallucinations* | ICLR 2026 | contextual faithfulness | context-faithfulness can be increased by high-copying preference training | medium | helps motivate distinction between surface grounding/copying and high-level search steering |
| DeepScientist | ICLR 2026 | autonomous discovery agent | very large-scale end-to-end discovery | field crowding | avoid another end-to-end scientist framework |
| *Can Language Models Discover Scaling Laws?* | ICLR 2026 | agentic discovery | LLM agent discovers useful scaling-law formulas | field crowding | confirms scientific-discovery agent topic is accepted but competitive |
| Carlon et al., *Thinking Like a Scientist?* | arXiv Jun 2026; SafeAI/UAI workshop poster | default scientific methodology | 3 strong LLMs given 1,000 CS research questions recommend a much narrower method inventory than real papers; inter-LLM method rankings align more strongly than LLM-to-paper rankings | **very high diagnostic neighbor** | treat as evidence for a shared scientific-method prior; new question is whether matched literature context can override it, not whether the default prior exists |
| LiveIdeaBench | Nature Communications 2026 | divergent scientific ideation | 40+ models; scientific creativity weakly predicted by general intelligence | benchmark collision | do not build generic creativity benchmark |
| RQ-Bench / *Limits of LLM-as-Judge* | arXiv Jun 2026 | research-question novelty | LLM novelty judges show novelty mirage; generated RQs often narrow/source-bound | **high diagnostic overlap** | test causal upstream source/evidence mechanism; do not rely on LLM novelty judge |
| *Prompt language as a diversity lever* | preprint Jul 2026 | RAG scientific ideation | translation changes retrieved sources and proposal content in one domain | **direct collision** | fixed generator language; direct evidence-packet intervention; matched relevance; multi-model/domain; dose response; distinguish lexical grounding from high-level steering |
| IDEAgent | arXiv 2026 | quality-diversity scientific ideation | agentic QD search for idea portfolios | high algorithmic | no QD framework as main contribution |
| Heuresis | arXiv 2026 | autonomous research search | compares search strategies over quality/diversity/novelty | high algorithmic | mechanism not search framework |
| Graph2Idea | arXiv Jun 2026 | structured literature context | graph-structured RAG improves scientific ideation | medium | we measure causal effects of composition/reliance rather than propose richer context architecture |
| SCI-IDEA | Machine Learning 2026 | researcher-context ideation | structured facets, novelty/surprise-guided refinement | medium | not a personalization/context framework |
| SciPIP | arXiv 2024 | literature-grounded ideas | multi-granularity retrieval + generation | medium | not “better literature context improves ideas” |
| IdeaBench | KDD 2025 | ideation benchmark | influential papers + references grounding; relative evaluation | medium | benchmark not primary contribution |
| MIR, *Methodology Inspiration Retrieval* | ACL 2025 | methodology inspiration retrieval | retrieval quality/nature matters; builds methodology-lineage graph to retrieve inspiring methods beyond surface similarity | high retrieval neighbor | retrieval side already asks which literature is inspiring; our core must be generator-side uptake/steerability under controlled matched evidence |
| ResearchBench | Findings ACL 2026 | inspiration-based discovery | decomposes scientific discovery into inspiration retrieval, hypothesis composition and ranking across 12 disciplines | important stretch neighbor | can reuse as external dataset/control; not another discovery benchmark |
| TCA-SIR | arXiv Jul 2026 | inspiration retrieval | target-conditioned abstractions predict transferability better than topical similarity | high-upside neighbor | further weakens “relevance is enough”; downstream causal uptake remains open |
| MUSES | arXiv Aug 2026 / NeurIPS E&D submission materials | prospective intellectual roots | standard retrieval struggles on author-endorsed generative roots | high-upside enabling work | root-vs-matched non-root downstream intervention; MUSES itself does not test LLM ideation utility |
| Hao et al., *AI tools expand scientists’ impact but contract science’s focus* | Nature 2026 | science-of-science | AI adoption associated with individual gains but collective topic narrowing | macro motivation | motivation only; no causal claim that retrieval explains real-world narrowing |

## Revised positioning after ICLR-specific research

The nearest accepted ICLR work establishes four pieces separately: (i) LLM assistance can homogenize populations of outputs; (ii) scientific ideation lacks generation diversity and merely adding more RAG papers has little effect on a coarse near-duplicate metric; (iii) models can be resistant to context relative to strong parametric priors; and (iv) **in-context steerability** is a distinct distributional capability that post-training can harm. Recent scientific-ideation work additionally finds that LLMs share a narrow default methodology distribution.

This suggests a sharper missing question than “does retrieval diversify ideas?”:

> **Can literature context actually override the shared methodological prior of scientific LLM ideation, and does evidence uptake weaken as we move from low-level source/concept grounding to high-level problem/method choice?**

A compelling new phenomenon would be **grounding without steering**: retrieved papers are visibly cited/copied and alter concepts, yet the model's high-level research-mode/method distribution remains close to its no-retrieval prior.

A second possible outcome is calibrated steerability: matched evidence mixtures produce predictable dose-response shifts in hypothesis modes. Either outcome is scientifically interpretable if established across models/topics with appropriate controls.

## Claims we must not make

- “We are the first to study scientific idea diversity.” — false.
- “We are the first to show retrieval affects LLM output.” — false.
- “We are the first to show retrieval affects scientific proposals.” — false due to 2026 prompt-language work and prior systems.
- “Retrieval is an inductive bias.” — too generic and already explicit in prior ICLR work.
- “We introduce in-context steerability.” — false; Spectrum Tuning does.
- “LLMs have narrow default scientific-method priors.” — Carlon et al. directly show this.
- “LLM judges can reliably score novelty.” — contradicted by recent evidence.
- “Diversity-aware RAG is novel.” — crowded.

## Defensible claim family if experiments support it

### Outcome A — Context-steerable

> At fixed amount and matched relevance, **evidence composition induces a reproducible, quantitatively predictable redistribution over scientific problem/method/framing choices**, revealing literature-conditioned steerability that coarse duplicate-based diversity metrics miss.

### Outcome B — Grounded but prior-bound

> Retrieval strongly changes source attribution and low-level conceptual content while **failing to proportionally override high-level scientific-method priors**, exposing a hierarchy of context reliance in literature-grounded scientific ideation.

### Stronger requirement for either outcome

Evidence packet features must predict downstream hypothesis-mode allocation on held-out topics/models, or a controlled counterfactual packet intervention must produce the predicted directional shift. Without predictive/causal evidence, the work is only a descriptive ideation study.
