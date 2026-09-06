# ICLR-Focused Related-Work / Collision Matrix

> Purpose: prevent us from rediscovering an existing idea and force every claimed contribution to have a clear nearest-neighbor distinction.

| Work | Venue/status | Core object | What it establishes | Collision with us | Required distinction / use |
|---|---|---|---|---|---|
| Padmakumar & He, *Does Writing with Language Models Reduce Content Diversity?* | ICLR 2024 | human+LLM co-writing | InstructGPT assistance reduces collective content diversity; model-contributed text explains much of effect | conceptual population-diversity precedent | cite as ICLR archetype; our object is LLM evidence-conditioned hypothesis distribution, not human writing |
| Si et al., *Can LLMs Generate Novel Research Ideas?* | ICLR 2025 | scientific ideation | LLM ideas can look novel to experts; diversity and self-evaluation are bottlenecks | **very high** | reproduce/acknowledge RAG-quantity null; study composition + structural distribution instead |
| Si et al. Appendix A.29 | ICLR 2025 | RAG ablation | k=0/5/10/20 has little effect on near-duplicate rate; backbone effect large | **decisive baseline** | main paper should explain a dimension their metric/ablation does not test |
| REGENT | ICLR 2025 | retrieval-augmented agents | retrieval provides a powerful adaptation bias | medium conceptual | never claim generic “retrieval is a bias”; claim composition-specific structured prior over open-ended hypothesis search |
| STARS | ICLR 2026 | LM generation diversity | inference-time activation steering broadens generation, incl. scientific discovery | high if we propose diversity algorithm | use as generation-side control; do not compete primarily on diversity method |
| *Mixing Mechanisms* | ICLR 2026 | in-context retrieval mechanism | decomposes multiple mechanisms and builds causal predictive model | paper-shape precedent | emulate mechanism/predictive rigor, not necessarily activation-level interpretation |
| DeepScientist | ICLR 2026 | autonomous discovery agent | very large-scale end-to-end discovery | field crowding | avoid another end-to-end scientist framework |
| *Can Language Models Discover Scaling Laws?* | ICLR 2026 | agentic discovery | LLM agent discovers useful scaling-law formulas | field crowding | confirms scientific-discovery agent topic is accepted but competitive |
| LiveIdeaBench | Nature Communications 2026 | divergent scientific ideation | 40+ models; scientific creativity weakly predicted by general intelligence | benchmark collision | do not build generic creativity benchmark |
| RQ-Bench / *Limits of LLM-as-Judge* | arXiv Jun 2026 | research-question novelty | LLM novelty judges show novelty mirage; generated RQs often narrow/source-bound | **high diagnostic overlap** | test causal upstream source/evidence mechanism; do not rely on LLM novelty judge |
| *Prompt language as a diversity lever* | preprint Jul 2026 | RAG scientific ideation | translation changes retrieved sources and proposal content in one domain | **direct collision** | fixed generator language; direct evidence-packet intervention; matched relevance; multi-model/domain; dose response |
| IDEAgent | arXiv 2026 | quality-diversity scientific ideation | agentic QD search for idea portfolios | high algorithmic | no QD framework as main contribution |
| Heuresis | arXiv 2026 | autonomous research search | compares search strategies over quality/diversity/novelty | high algorithmic | mechanism not search framework |
| Graph2Idea | arXiv Jun 2026 | structured literature context | graph-structured RAG improves scientific ideation | medium | we measure causal effects of composition rather than propose richer context architecture |
| SCI-IDEA | Machine Learning 2026 | researcher-context ideation | structured facets, novelty/surprise-guided refinement | medium | not a personalization/context framework |
| SciPIP | arXiv 2024 | literature-grounded ideas | multi-granularity retrieval + generation | medium | not “better retrieval improves ideas” |
| IdeaBench | KDD 2025 | ideation benchmark | influential papers + references grounding; relative evaluation | medium | benchmark not primary contribution |
| ResearchBench | ACL Findings 2026 | inspiration-based discovery | inspiration retrieval, hypothesis composition, hypothesis ranking | important stretch neighbor | MUSES/root experiment must differ via controlled causal injection and discovery-utility comparison |
| MUSES | arXiv Aug 2026 / NeurIPS E&D submission materials | prospective intellectual roots | standard retrieval struggles on author-endorsed generative roots | high-upside enabling work | root-vs-matched non-root downstream intervention; MUSES itself does not test LLM ideation utility |
| Hao et al., *AI tools expand scientists’ impact but contract science’s focus* | Nature 2026 | science-of-science | AI adoption associated with individual gains but collective topic narrowing | macro motivation | motivation only; no causal claim that retrieval explains real-world narrowing |

## Positioning sentence

The nearest accepted ICLR work establishes that (i) LLM-assisted output can homogenize, (ii) scientific ideation lacks generation diversity, and (iii) simply adding more retrieved papers has little effect on a coarse non-duplicate metric. Recent preprints further show that scientific RQs can be source-bound and that query-language perturbations can alter RAG sources and proposals. What is still not established is whether **the composition of equally relevant evidence causally redistributes the structured hypothesis modes explored by an LLM, and whether this redistribution is hidden by standard duplicate-based diversity metrics.**

## Claims we must not make

- “We are the first to study scientific idea diversity.” — false.
- “We are the first to show retrieval affects LLM output.” — false.
- “We are the first to show retrieval affects scientific proposals.” — likely false due to 2026 prompt-language work.
- “Retrieval is an inductive bias.” — too generic and already explicit in prior ICLR work.
- “LLM judges can reliably score novelty.” — contradicted by recent evidence.
- “Diversity-aware RAG is novel.” — crowded.

## Claim that remains defensible if experiments support it

> At fixed amount and matched relevance, **evidence composition induces a reproducible, interpretable shift in the distribution over scientific problem/method/framing choices**, and this shift can be missed by near-duplicate diversity metrics.

A stronger version requires held-out prediction or causal feature transfer:

> Evidence packet features quantitatively predict downstream hypothesis-mode allocation across held-out topics/models, supporting the interpretation of retrieved context as a structured inference-time prior over open-ended search.
