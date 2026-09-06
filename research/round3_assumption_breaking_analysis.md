# 第三轮选题分析：从“热点追踪”转向“打破默认假设”

> 日期：2026-09-06  
> 目标：为 ICLR 2027/2028 形成可证伪、低同质化、可由 Codex 快速 pilot 的研究主线。  
> 方法：反向拆解 ICLR 2022–2026 Outstanding / Honorable Mention，叠加 2026 年最新相关工作做 collision check，并把“AI 选题同质化”作为独立风险维度。

## 0. Executive decision

第三轮结论与前两轮不同：**不能再直接把 Model Editing Locality、Multi-turn Decomposition、Causal Agent Memory 当作首选题。** 2026 年已经出现了与这些核心假设高度相近的工作，继续按原表述推进容易成为 contemporaneous follow-up，而不是清晰的新知识。

本轮最值得进入 24–48h pilot 的方向来自一个更具体的问题：

> **共享的文献检索与 LLM 筛选流程，是否会让独立科研 agent / 研究者在“单个 idea 看起来新颖”的同时，群体层面的研究问题发生收敛？如果会，收敛主要发生在 generation、retrieval、selection 还是 refinement 阶段？**

暂定工作题目：

**From Retrieval to Selection: Where Scientific Idea Diversity Disappears in LLM Research Pipelines**

更尖锐的备选标题：

**Novel but the Same: Population-Level Collapse in LLM-Assisted Scientific Ideation**

这里不把“AI 会同质化”本身当作新发现——已有工作已经提供了相关证据；真正需要贡献的是：

1. 在真实的 literature-grounded scientific ideation pipeline 中做 **stage-wise causal decomposition**；
2. 检验 **shared retrieval exposure** 是否是群体收敛的机制，而不只是模型采样分布；
3. 检验 **LLM judge / reranking** 是否进一步压掉长尾研究问题；
4. 用简单 intervention 恢复 portfolio diversity，同时不明显牺牲 feasibility / scientific quality；
5. 不依赖一个新的“花哨指标”成立，而使用多种已有 diversity / quality 测量和人工子集验证。

---

## 1. 为什么要从“高分论文做了什么”改成“打破了什么默认假设”

ICLR 2027 Reviewer Guide 明确要求 reviewer 判断：问题是否明确、定位是否正确、claims 是否由严谨证据支持、是否带来有意义的新知识；并特别强调**不要求 SOTA，interesting / surprising / new-direction results 同样有价值**。

- Reviewer Guide: https://iclr.cc/Conferences/2027/ReviewerGuidelines
- CFP: https://iclr.cc/Conferences/2027/CallForPapers

ICLR 2027 Program Chairs 进一步直接指出：AI 降低了制造“paper-shaped object”的门槛，但当前 AI 对 research question 的 taste 仍然较差；他们希望看到更 ambitious、complete、exciting 的 “slow science”，而不是把过去五年的项目模式更快地复制一遍。

- Submission policies for ICLR 2027: https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/

这意味着我们的目标函数不该是：

> 热门主题 × 新模块 × benchmark +1%

而应该是：

> **重要默认假设 × 可证伪反例 × 机制解释 × 排除替代解释 × 简单修复 / 新原则**

---

## 2. ICLR 2022–2026 award papers 的反向拆解

### 2.1 本轮人工多标签编码

本轮对 2022–2026 共 44 篇官方 Outstanding / Honorable Mention 进行人工多标签归类。**这是研究用手工编码，不是 ICLR 官方统计；一个 paper 可以同时属于多个标签，因此数量不能相加为 44。**

| archetype | count / 44 | 典型含义 |
|---|---:|---|
| mechanism / theory | 18 | 解释现象为什么发生，而不是只报告现象 |
| theory-to-practice | 11 | 原理直接转为可用方法 / 计算方案 |
| simple & principled intervention | 11 | 修复很简单，但建立在清晰机制上 |
| blind-spot discovery | 10 | 指出现有 protocol / assumption 漏掉关键问题 |
| unification | 10 | 把看似分散的方法/现象纳入统一视角 |
| cross-paradigm transfer | 10 | 从另一领域/范式借来关键工具形成新视角 |
| efficiency / compute reformulation | 9 | 改变计算问题本身，而不是只优化实现 |
| surprising observation | 7 | 结果违背社区直觉，并被系统实验支撑 |
| new-direction potential | 7 | 能打开新研究路径 |
| reformulation | 6 | 重新定义问题，使原本昂贵/模糊的对象可求解 |
| measurement / evaluation reframe | 约 6–9 | 改变“应该如何比较/测量”的问题定义 |
| realistic protocol / deployment gap | 5 | 指出现有实验与真实使用条件不一致 |

### 2.2 典型“打破假设”实例

| Paper / year | 默认假设 | 被打破的地方 | 论文结构 |
|---|---|---|---|
| Never Train from Scratch (2024) | 随机初始化下的架构比较可代表模型家族优劣 | 预训练后 Transformer 与 SSM 的差距大幅改变，random-init protocol 会误导结论 | protocol flaw → systematic comparison → ranking/conclusion change |
| Vision Transformers Need Registers (2024) | feature artifact 只是噪声/无关异常 | artifact 对应模型内部计算行为；简单 register token 可修复 | anomaly → mechanism hypothesis → simple fix |
| Safety Alignment Should be More Than a Few Tokens Deep (2025) | 拒答安全代表更深层 policy 安全 | safety 行为集中在很浅的 token 区域，解释多种脆弱性 | common failures → unifying mechanism |
| Data Shapley in One Training Run (2025) | data value 必须通过大量重训练估计 | 把问题改成针对一次 training run 的 attribution，可大幅降低成本 | reformulate target → tractable estimator |
| LLMs Get Lost in Multi-Turn Conversation (2026) | 单轮能力大致能外推到真实多轮使用 | 多轮条件造成显著 aptitude / reliability degradation | deployment mismatch → scalable evaluation → diagnosis |
| Muon / Polar Express (2026 HM) | optimizer 近似只看抽象数学即可 | 近似设计直接结合 GPU 与低精度数值约束 | principled approximation + hardware reality |

官方 award sources：

- ICLR 2022: https://blog.iclr.cc/2022/04/20/announcing-the-iclr-2022-outstanding-paper-award-recipients/
- ICLR 2023: https://blog.iclr.cc/2023/03/21/announcing-the-iclr-2023-outstanding-paper-award-recipients/
- ICLR 2024: https://blog.iclr.cc/2024/05/06/iclr-2024-outstanding-paper-awards/
- ICLR 2025: https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/
- ICLR 2026: https://blog.iclr.cc/2026/04/23/announcing-the-iclr-2026-outstanding-papers/

**关键结论：**高认可工作的共同点不是“都做 LLM / 都做某个热门技术”，而是经常把一个模糊的社区直觉变成可被证伪、可被测量、可被解释的 claim。

---

## 3. 对上一轮 TOP ideas 的 collision check

### 3.1 Model Editing Locality Stress Test — 降级

上一轮想法：传统 locality 太弱，应测试 compositional / multi-hop / multi-turn collateral effects。

2026 年已有直接碰撞：

- *Are We Evaluating the Edit Locality of LLM Model Editing Properly?* 已明确指出现有 locality protocol 的基础性问题，并提出新评测协议： https://arxiv.org/abs/2601.XXXX （正式使用时需从源数据补全 arXiv ID，不在论文中保留占位符）
- WikiBigEdit 等近期工作已经把 multi-hop / locality 放入更大规模 lifelong editing evaluation。

**结论：**仅做“locality metric 不够 + multi-hop stress test”不足。除非找到新的 causal boundary（例如 edit 的哪种内部传播机制决定 collateral effect，并能预测 failure），否则不进 P0。

### 3.2 Multi-turn Failure Decomposition — 降级

ICLR 2026 Outstanding paper 本身已经不只报告下降，还分析 premature assumptions、先前错误依赖等原因。2026 年后续工作又开始显式讨论 state drift、constraint reasoning、hidden-state trajectory drift。

**结论：**“state drift + instruction dilution + error accumulation”作为三分法已经太接近当前前沿表述。只有发现一个**新的可操作 latent variable / intervention**，且能改变模型排序或恢复能力，才值得继续。

### 3.3 Causal Agent Memory Utility — 降级

近期已经出现：

- “relevance != model-specific utility”的 RAG 观点；
- streaming / lifelong memory benchmarks；
- temporal intervention、memory contamination、retrieval/application divergence 等诊断。

**结论：**“similarity != utility”已经不是低碰撞 claim。若继续，必须研究更具体的新机制，而不是再提出一个 causal utility score。

### 3.4 Generic Benchmark Construct Validity — 降级

2025–2026 已有大量 work 对 construct validity、judge reliability、calibration ranking reversal、benchmark fragility 做系统研究。

**结论：**“Are we measuring what we think we measure?” 太宽，容易变成 another benchmark paper。需要具体到一个会**改变领域结论或方法排序**的 measurement failure。

---

## 4. 用户提出的“AI 选题会不会导致重复”为什么值得进一步研究

这不是空想，已有四组相关证据：

1. **ICLR 2025** 的科研 ideation 人类对照实验发现，LLM ideas 可以被评为更 novel，但 agent baseline 存在 self-evaluation failure 和 generation diversity 不足：
   https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html
2. **Nature Communications 2026 LiveIdeaBench** 专门测 scientific divergent thinking，说明 general intelligence benchmark 并不能预测 scientific ideation creativity：
   https://www.nature.com/articles/s41467-026-70245-1
3. **2026 novelty-judge work** 发现 LLM judge 对科学 research question 的 novelty 判断可产生 “novelty mirage”，与专家判断方向相反：
   https://arxiv.org/abs/2606.12071
4. 更一般的 creativity 文献已经发现群体层面 homogenization；LLM output 即使单条很“creative”，大量样本累积时仍可能快速收敛。

因此，**“同质化存在”本身已经不是足够的新 claim。**

本轮检索尚未发现一篇直接相关工作同时完成以下四件事（这不是“绝对不存在”的证明，正式投稿前仍需持续 collision scan）：

- 针对 literature-grounded scientific ideation，而非通用 creativity task；
- 把 pipeline 拆成 retrieval → generation → judge/selection → refinement；
- 用 controlled intervention 定量归因每个阶段造成的 portfolio diversity loss；
- 研究“不同独立研究者共享相似 retrieval/expert model”造成的 population-level convergence，而不是只测单个 agent 的 idea quality。

这就是当前可进入 pilot 的 gap。

---

## 5. 推荐 P0：Shared-Retrieval Research Monoculture

### 5.1 Research question

> 当许多科研 agent / 研究者使用相同或相似的 LLM + 文献检索器时，**top-relevance retrieval 是否会把他们暴露到高度相同的文献邻域，从而把原本可探索的 research-question space 压缩到少数“显眼 gap”上？**

进一步：

> 这种收敛是 generator prior 导致，还是 retrieval exposure 导致？LLM judge / refinement 会缓解还是加剧？

### 5.2 Hidden assumption

当前多数 scientific ideation pipeline 默认：

> 更相关、更强的 literature retrieval → 更好的 idea generation。

这个假设在**单个 idea quality**上可能成立，但在**群体 science portfolio**上未必成立。

潜在悖论：

> individual novelty ↑ / feasibility ↑，但 collective diversity ↓ / collision rate ↑。

这比单纯“LLM 不够 creative”更有科学价值，因为它指出的是**目标函数层级错配：individual objective ≠ population objective**。

### 5.3 Falsifiable hypotheses

- **H1 Retrieval concentration:** 标准 top-k relevance retrieval 会让独立 runs 的 source-set overlap 明显高于 diversified retrieval。
- **H2 Mediation:** source-set overlap 越高，最终 problem–method idea overlap 越高；控制 model/prompt 后仍成立。
- **H3 Selection pressure:** 在固定 candidate pool 上，LLM judge top-k selection 会进一步降低 portfolio diversity，尤其当 judge 与 generator 同模型家族时。
- **H4 Quality-diversity trade-off is not necessary:** MMR / disjoint-neighborhood / coverage-aware selection 能显著恢复 diversity，同时保留大部分 feasibility / quality。
- **H5 Cross-model alone is insufficient:** 换不同 LLM 可能仍因共享高频 literature neighborhood 而产生收敛；真正有效的杠杆可能是 evidence exposure diversity。

### 5.4 最小 pilot（24–48h）

选择 3 个 ICLR 活跃子领域，每个领域建立同一份近年论文摘要库。

最小条件：

1. `topic-only / no retrieval`
2. `top-k relevance RAG`
3. `diversified retrieval (MMR or disjoint source subsets)`
4. 可选：`top-k RAG + judge rerank`

每个条件至少 30 independent seeds；至少 2 个模型家族。

第一阶段不需要训练模型。

记录完整 trace：

```text
seed
model/version
prompt_hash
retrieval_query
retrieved_paper_ids + scores
generated research question
proposed method
claimed gap
judge scores/ranking
refined idea
```

### 5.5 Metrics：避免“造一个新 metric 就写论文”

至少同时使用：

- retrieval source overlap: Jaccard / weighted overlap
- exposure concentration: Gini / Herfindahl / source coverage
- semantic pairwise distance
- cluster entropy / effective number of clusters
- Diversity Growth Rate（引用已有 homogenization work）
- structured problem–method tuple collision rate
- nearest-neighbor distance to actual literature（只作为一个 proxy）
- blind human duplicate / distinctness annotation on stratified subset
- feasibility / technical-depth human or cross-family evaluation（不能只靠同一个 LLM judge）

### 5.6 最关键的一张 Figure

横轴：pipeline stage

```text
retrieval → generation → selection → refinement
```

纵轴同时画：

- portfolio diversity
- individual quality / feasibility

理想现象：

```text
quality       ────╮──────
                  ╰──────
diversity    ───────╲____
                       ^
                 selection/refinement
```

如果能显示“单个 idea 质量上升、群体 diversity 下降”，故事非常清楚。

### 5.7 Mechanism figure

```text
shared corpus
   ↓
relevance-ranked retrieval
   ↓
source exposure concentration
   ↓
problem framing concentration
   ↓
LLM judge selects conventional / easy-to-defend candidates
   ↓
research idea collision
```

必须用 intervention 而不是相关性支持箭头。

### 5.8 Strong baselines

- no retrieval
- random relevant papers
- top-k cosine relevance
- BM25/top-k lexical (若适用)
- MMR retrieval
- disjoint / coverage-constrained retrieval
- persona prompting
- high-temperature generation
- multi-model generation
- generate-many + random selection
- generate-many + LLM judge selection
- generate-many + MMR/quality-diversity selection

### 5.9 Kill criteria

24–48h pilot 出现任一情况则停止：

1. diversified retrieval 只改变措辞，不改变 problem/method-level diversity；
2. retrieval overlap 与 idea overlap 在控制 model/prompt 后基本无关联；
3. 任何结论只在一个 embedding metric 上成立；
4. 不同 prompt paraphrase 即可把效应完全抹掉；
5. quality 明显崩溃，证明所谓“diversity gain”只是随机噪声；
6. 最新 collision scan 找到已有论文已经做了同样的 stage-wise causal decomposition。

### 5.10 Continue criteria

满足以下至少 3 条才进入完整论文：

- >2 model families 重复出 retrieval-concentration → idea-concentration；
- 至少 2 个非等价 diversity metrics + 人工子集一致；
- fixed-candidate-pool 证明 selection stage 有独立效应；
- 简单 intervention 恢复 diversity 且质量损失小；
- effect 在 >=3 子领域存在，且 magnitude 足够大；
- 能构成一个清晰的“现有 scientific ideation system objective 有盲点”的 claim。

---

## 6. 与最近工作怎么区分

### vs. Si et al., ICLR 2025

他们问：**LLM 能否产生 expert-level novel research ideas？** 并发现 diversity / self-evaluation 是开放问题。

我们应问：**在 realistic literature-grounded pipeline 中，collective diversity 在哪一个 stage 被压掉，以及 retrieval/selection 是否具有 causal contribution？**

### vs. LiveIdeaBench, Nature Communications 2026

LiveIdeaBench 主要测 minimal-context divergent thinking、跨模型 creative capability。

我们关注的是：**rich-context / literature-grounded pipeline 的 population behavior 与 stage-wise mechanism**。

### vs. RQ-Bench / novelty-judge papers

它们主要研究：**LLM 能否正确判断 novelty。**

我们研究：**judge selection 会不会作为 selection pressure 改变整个 research portfolio 的 diversity，并与 retrieval exposure 交互。**

### vs. general creative homogenization

通用 creative writing / AUT 证明 LLM output 可以 homogeneous。

我们必须进一步证明：

- scientific pipeline 中也存在；
- 它不是纯文本 style similarity；
- 可以追踪到 source exposure / selection；
- 对 research-question / method choice 有实际影响。

### vs. Graph2Idea / Nova / IDEAgent 等 diversity-enhancing systems

这些 work 多数目标是“做出更好的 ideation system”。

我们的主贡献不应是 another agent framework，而应是：

> **发现一个系统级 failure + 因果拆解 + 简单 correction。**

---

## 7. Anti-collapse topic filter v2

后续每个候选题都先回答以下问题：

```text
A. 一次普通 ChatGPT / Claude / Gemini brainstorm 是否高概率给出这个题？
   yes -> saturation penalty

B. 最近 8 个月是否已有 paper 使用几乎相同的 hidden assumption？
   yes -> collision penalty

C. 题目的核心贡献是否只是 new framework / benchmark / metric？
   yes -> weak unless it changes a scientific conclusion

D. 是否能写成：
   “The field assumes X. Under controlled intervention Y, X fails because Z.”
   no -> mechanism penalty

E. 是否存在 24–48h falsifiable pilot？
   no -> deadline penalty

F. negative result 是否仍有知识价值？
   no -> fragility penalty

G. reviewer 能否用一句话复述 main claim？
   no -> clarity penalty
```

优先选择：

> **low saturation + high falsifiability + high mechanism clarity + low ambiguity + multiple outcomes still informative**

---

## 8. 当前候选排序（第三轮）

评分 1–5；Collision Risk 越高越差。

| Rank | Topic | Novelty | Mechanism potential | 48h pilot | ICLR fit | Collision risk | Decision |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | **Shared-Retrieval Research Monoculture / stage-wise idea collapse** | 4.5 | 5 | 5 | 5 | 3 | **P0 pilot** |
| 2 | Judge-induced scientific selection conservatism | 3.5 | 4.5 | 5 | 5 | 4 | merge into P0 as RQ, not standalone |
| 3 | Scaffold × backbone interaction causing agent-ranking instability | 3 | 4 | 4 | 5 | 4.5 | backup only |
| 4 | Model Editing locality stress | 2.5 | 4 | 5 | 5 | 4.5 | pause |
| 5 | Multi-turn state/error decomposition | 2.5 | 4 | 4 | 5 | 5 | pause |
| 6 | Causal memory utility | 2.5 | 4 | 4 | 5 | 5 | pause |
| 7 | Generic benchmark construct validity | 2 | 3 | 4 | 4 | 5 | reject as too broad |

注：这些是基于当前检索的研究决策分，不是录用概率。

---

## 9. ICLR 2027 deadline reality

截至 2026-09-06：

- Abstract deadline: 2026-09-18 11:59 PM AoE
- Full paper deadline: 2026-09-25 11:59 PM AoE

官方 CFP 也明确提醒：典型 ICLR paper 的工作量显著高于课程项目或当前 AI agent 能自主产生的水平；如果工作还不完整或不完全确定正确，应继续打磨，而不是为了 deadline 强投。

因此执行策略：

```text
Sep 6–8   P0 pilot + latest collision scan
Sep 8     kill/continue gate
Sep 9–12  scale across models/topics + mechanism ablation
Sep 12    paper claim freeze
Sep 13–17 human validation + main figures + related work lock
Sep 18    abstract only if evidence chain already strong
Sep 18–25 robustness / paper / reviewer red-team
```

**如果 Sep 8–10 仍没有清晰、跨设置可复现的 main effect，转 ICLR 2028 quality-first，不用“AI 加速”强行拼一个 2027 submission。**

---

## 10. Codex next task

Codex 不应先写论文，也不应先搭“大一统 research agent”。只需要做最小实验基础设施：

```text
experiments/idea_collapse/
├── README.md
├── configs/
├── corpus/
├── retrieval/
├── generation/
├── selection/
├── metrics/
├── runs/
└── analysis/
```

第一个 executable task：

> 固定 3 个主题和一个小型 ICLR abstract corpus，生成 `no_retrieval / topk_retrieval / diversified_retrieval` 三个条件各 30 seeds，保存完整 retrieval + generation trace，并输出 source-overlap 与 idea-diversity 的 bootstrap CI。

在这个结果出来前，不实现复杂 agent，不发明新 metric，不写完整 paper。

---

## 11. 主要参考

- ICLR 2027 CFP: https://iclr.cc/Conferences/2027/CallForPapers
- ICLR 2027 Reviewer Guide: https://iclr.cc/Conferences/2027/ReviewerGuidelines
- ICLR 2027 submission policy / AI-era research taste: https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/
- ICLR 2022 Outstanding Papers: https://blog.iclr.cc/2022/04/20/announcing-the-iclr-2022-outstanding-paper-award-recipients/
- ICLR 2023 Outstanding Papers: https://blog.iclr.cc/2023/03/21/announcing-the-iclr-2023-outstanding-paper-award-recipients/
- ICLR 2024 Outstanding Papers: https://blog.iclr.cc/2024/05/06/iclr-2024-outstanding-paper-awards/
- ICLR 2025 Outstanding Papers: https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/
- ICLR 2026 Outstanding Papers: https://blog.iclr.cc/2026/04/23/announcing-the-iclr-2026-outstanding-papers/
- Si et al., *Can LLMs Generate Novel Research Ideas?*, ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html
- Ruan et al., *Evaluating LLMs' divergent thinking capabilities for scientific idea generation with minimal context*, Nature Communications 2026: https://www.nature.com/articles/s41467-026-70245-1
- *On the Limits of LLM-as-Judge for Scientific Novelty Assessment*, 2026: https://arxiv.org/abs/2606.12071
- *Examining and Addressing Barriers to Diversity in LLM-Generated Ideas*, 2026: https://arxiv.org/abs/2602.20408
- *Homogenizing effect of LLMs on creative diversity*, 2025: https://doi.org/10.1016/j.chbah.2025.100207
- *Towards end-to-end automation of AI research*, Nature 2026: https://www.nature.com/articles/s41586-026-10265-5

## 12. Evidence limitation

本文件是“选题决策报告”，不是系统综述。我们已经针对主要候选方向做了 2026 collision scan，但 arXiv / workshop 发展非常快。任何 topic 在进入正式 main experiment 前都必须再做一次最近 30–60 天检索，尤其检查 contemporaneous papers。