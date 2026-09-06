# 第三轮选题分析：从“热点追踪”转向“打破默认假设”

> 日期：2026-09-06  
> 目标：为 ICLR 2027/2028 形成可证伪、低同质化、可由 Codex 快速 pilot 的研究主线。  
> 方法：反向拆解 ICLR 2022–2026 Outstanding / Honorable Mention，叠加 2026 最新工作做 collision check，并把“AI 选题同质化”加入选题风险函数。

## 0. Executive decision

第三轮结论与前两轮不同：**Model Editing Locality、Multi-turn Decomposition、Causal Agent Memory 都不再适合直接作为 P0。** 2026 年已经出现与这些核心假设高度接近的工作，继续按原表述推进很容易成为 contemporaneous follow-up。

当前最值得做 24–48h falsifiable pilot 的问题是：

> **共享的文献检索与 LLM 筛选流程，是否会让独立科研 agent / 研究者在“单个 idea 看起来新颖”的同时，在群体层面收敛到相似 research questions？如果会，diversity 主要在 retrieval、generation、selection 还是 refinement 阶段丢失？**

工作题目：

**From Retrieval to Selection: Where Scientific Idea Diversity Disappears in LLM Research Pipelines**

备选标题：

**Novel but the Same: Population-Level Collapse in LLM-Assisted Scientific Ideation**

这里**不把“LLM 输出会同质化”本身当新发现**。已有文献已经证明 scientific ideation 存在 diversity/self-evaluation 问题，也已有一般 creativity homogenization 证据。真正可能形成贡献的是：

1. realistic literature-grounded scientific ideation pipeline 的 **stage-wise causal decomposition**；
2. 检验 **shared retrieval exposure** 是否是 population convergence 的机制；
3. 检验 **LLM judge / reranking** 是否进一步压缩长尾 research questions；
4. 用简单 intervention 恢复 portfolio diversity，同时保持 feasibility / scientific quality；
5. 不依赖一个新造指标成立，而用多种成熟 diversity 指标 + structural collision + 人工子集验证。

---

## 1. ICLR 给出的目标函数

ICLR 2027 Reviewer Guide 要 reviewer 判断：问题是否明确、是否正确定位到已有文献、claims 是否由严谨证据支持、是否贡献足够有意义的新知识。官方同时明确：**SOTA 不是必要条件；interesting、surprising、可能打开新方向的结果同样有价值。**

- Reviewer Guide: https://iclr.cc/Conferences/2027/ReviewerGuidelines
- CFP: https://iclr.cc/Conferences/2027/CallForPapers

ICLR 2027 Program Chairs 在 2026-09-02 的政策说明中进一步直言：AI 降低了制造“paper-shaped object”的门槛，但当前 AI 对 research questions 的 taste 仍然较差；CFP 还鼓励 veteran submitters 做更 ambitious 的 “slow science”，而不是用 AI 更快重复过去五年的项目范式。

- Submission policies: https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/

因此我们的目标函数应从：

> 热门主题 × 新模块 × benchmark +1%

切换成：

> **重要默认假设 × 可证伪反例 × 机制解释 × 排除替代解释 × 简单修复 / 新原则**

---

## 2. ICLR 2022–2026 award papers：反向拆解

本轮对 2022–2026 共 **44 篇**官方 Outstanding / Honorable Mention 做人工多标签编码。**这是项目内部编码，不是 ICLR 官方统计；同一 paper 可有多个标签，因此计数不可相加。**

| archetype | count / 44 | 含义 |
|---|---:|---|
| mechanism / theory | 18 | 解释为什么发生，而不只报告现象 |
| theory-to-practice | 11 | 原理直接转化为可用方法 |
| simple & principled intervention | 11 | 修复简单但由机制支撑 |
| blind-spot discovery | 10 | 暴露 protocol / assumption 漏洞 |
| unification | 10 | 用统一机制解释分散现象 |
| cross-paradigm transfer | 10 | 从另一范式借工具形成新视角 |
| efficiency / compute reformulation | 9 | 改变计算问题，而不仅是工程优化 |
| surprising observation | 7 | 系统证据支持违背直觉的结果 |
| new-direction potential | 7 | 能打开后续研究方向 |
| reformulation | 6 | 重新定义目标，使问题可求解 |
| realistic protocol / deployment gap | 5 | 揭示实验设定与真实使用不一致 |

几个尤其值得模仿的“论文逻辑”：

| Paper | 默认假设 | 打破方式 | 可复用研究结构 |
|---|---|---|---|
| Never Train from Scratch (ICLR 2024) | random-init 架构比较代表模型家族优劣 | 预训练后结论显著变化 | protocol flaw → systematic comparison → conclusion reversal |
| Vision Transformers Need Registers (ICLR 2024) | feature artifact 只是噪声 | 找到内部计算机制并用简单 registers 修复 | anomaly → mechanism → simple fix |
| Safety Alignment Should be More Than a Few Tokens Deep (ICLR 2025) | 表面拒答≈深层 policy 安全 | 浅层 token 机制统一解释多种 vulnerability | failures → unifying mechanism |
| Data Shapley in One Training Run (ICLR 2025 HM) | data value 需要大量重训练 | 改写 attribution target，使一次训练可估计 | reformulation → tractability |
| LLMs Get Lost in Multi-Turn Conversation (ICLR 2026) | single-turn 能力能外推到真实多轮 | scalable realistic protocol 揭示显著 degradation | deployment mismatch → measurement → diagnosis |
| Polar Express / Muon (ICLR 2026 HM) | optimizer 近似主要是抽象数学问题 | approximation 明确结合 GPU / low precision | principle + hardware reality |

官方来源：

- 2022: https://blog.iclr.cc/2022/04/20/announcing-the-iclr-2022-outstanding-paper-award-recipients/
- 2023: https://blog.iclr.cc/2023/03/21/announcing-the-iclr-2023-outstanding-paper-award-recipients/
- 2024: https://blog.iclr.cc/2024/05/06/iclr-2024-outstanding-paper-awards/
- 2025: https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/
- 2026: https://blog.iclr.cc/2026/04/23/announcing-the-iclr-2026-outstanding-papers/

**项目结论：**高认可工作并不集中于某个关键词；更稳定的模式是把社区直觉变成一个清晰、可证伪、可测量并可解释的 scientific claim。

---

## 3. 上一轮 TOP ideas：collision check

### 3.1 Model Editing Locality Stress — 从 P0 降级

原想法：传统 locality 太弱，应加入 compositional / multi-hop / multi-turn collateral effects。

直接碰撞：

- Wei Liu et al., **Are We Evaluating the Edit Locality of LLM Model Editing Properly?**, arXiv:2601.17343：明确指出现有 locality/specificity protocol 的基础问题、指标敏感度不足，并提出新的 evaluation protocol。  
  https://arxiv.org/abs/2601.17343

此外，2026 的 large-scale / lifelong editing work 已经把 multi-hop/locality 纳入更复杂评测。

**决定：**仅做“locality metric 弱 + multi-hop stress test”不足。只有找到新的 causal boundary（例如某种内部传播机制能预测 collateral effects，并通过 intervention 验证）才重新进入 P0。

### 3.2 Multi-turn Failure Decomposition — 从 P0 降级

ICLR 2026 Outstanding paper 已经不只是“性能下降”：它对 premature assumptions、prior wrong attempts 等因素做了分析。2026 随后的工作又开始显式讨论 state drift、constraint reasoning、hidden-state trajectory drift。

**决定：**“state drift + instruction dilution + error accumulation”三分法太接近当前前沿。若无新的可操作 latent variable 或能改变模型排序的 intervention，不继续。

### 3.3 Causal Agent Memory Utility — 降级

近期已经出现：

- relevance 与 model-specific utility 不等价的 RAG 研究；
- streaming / lifelong memory benchmarks；
- memory contamination、temporal intervention、retrieval/application divergence。

**决定：**“similarity != utility”不再是低碰撞 claim；不能只造一个 causal utility score。

### 3.4 Generic Construct Validity — reject as too broad

2025–2026 已有多篇 work 研究 benchmark construct validity、judge reliability、calibration ranking reversal、benchmark fragility。

**决定：**除非 measurement failure 能明确改变领域结论/方法排序，否则“Are we measuring what we think?” 太泛。

---

## 4. 为什么“AI 选题收敛”值得继续，但必须换一个更尖的问题

已有直接证据：

1. **Si et al., ICLR 2025**：LLM ideas 在专家评审中可表现出较强 novelty，但作者明确识别出 self-evaluation failure 与 generation diversity 不足。  
   https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html
2. **LiveIdeaBench, Nature Communications 2026**：专门测 scientific divergent thinking，说明 general intelligence benchmark 并不能简单预测 scientific ideation creativity。  
   https://www.nature.com/articles/s41467-026-70245-1
3. **On the Limits of LLM-as-Judge for Scientific Novelty Assessment (2026)**：LLM novelty judge 可产生明显 “novelty mirage”，和专家判断相悖。  
   https://arxiv.org/abs/2606.12071
4. **Examining and Addressing Barriers to Diversity in LLM-Generated Ideas (2026)**：从 fixation / knowledge partitioning 解释 LLM idea diversity 问题。  
   https://arxiv.org/abs/2602.20408
5. 通用 creativity 文献已经显示 population-level homogenization，因此不能把“LLM 比人更同质”本身包装成 novel claim。

本轮检索**没有找到一篇直接相关工作同时完成**下面四点（这不是证明绝对不存在；正式投稿前必须持续 scan）：

- 研究 literature-grounded scientific ideation，而非单纯 creativity task；
- 把 pipeline 拆成 retrieval → generation → selection/judge → refinement；
- 用 controlled intervention 做 stage-wise causal attribution；
- 把“独立研究者共享相似 evidence exposure”作为 population-level convergence mechanism 直接检验。

因此 P0 应从宽泛的 “Research Idea Collapse” 收紧为：

# Shared-Retrieval Research Monoculture

---

## 5. P0 scientific formulation

### RQ

> 当大量科研 agent / 研究者使用相似 LLM + literature retriever 时，top-relevance retrieval 是否会把独立 runs 暴露到高度重合的文献邻域，从而把可探索的 research-question space 压缩到少数显眼 gap？

进一步：

> generator prior、retrieval exposure、judge selection、iterative refinement 各贡献多少？

### Hidden assumption

大量 scientific ideation pipelines 默认：

> **more relevant retrieval → better idea generation.**

它在单个 idea quality 上可能成立，但在 population/portfolio 层面可能存在目标错配：

> **individual novelty / feasibility ↑，collective diversity ↓，idea collision ↑。**

如果成立，这不是“模型不够 creative”，而是一个**individual objective 与 collective scientific objective 的错配**。

### Falsifiable hypotheses

- **H1 Retrieval concentration**：top-k relevance 会让独立 runs 的 source-set overlap 显著高于 diversified retrieval。
- **H2 Causal link**：操纵 source exposure overlap 会导致 problem–method idea overlap 同方向变化。
- **H3 Selection pressure**：固定 candidate pool 后，LLM judge top-k selection 会进一步降低 portfolio diversity。
- **H4 Same-family effect**：generator 与 judge 同模型家族时，selection contraction 可能更强。
- **H5 Diversity without quality collapse**：MMR / coverage-constrained / disjoint-neighborhood retrieval 能恢复明显 diversity，而不显著破坏 feasibility / technical depth。
- **H6 Cross-model is not enough**：只换 generator model 可能仍无法解决共享 evidence neighborhood 带来的 convergence。

---

## 6. 24–48h pilot

选 3 个 ICLR 活跃子领域，各建立同一份近年 paper-title/abstract corpus。

最小实验条件：

1. `topic_only_no_retrieval`
2. `topk_relevance_retrieval`
3. `diversified_retrieval_mmr_or_disjoint`
4. 可选 `topk + llm_judge_rerank`

每条件至少 30 independent seeds，至少 2 个 model families。

完整保存：

```text
run_id
seed
model + exact version
prompt_hash
retrieval_query
retrieved_paper_ids + scores
generated research question
claimed gap
proposed method
selection score/rank
refined idea
```

### Metrics：不靠一个新指标

同时用：

- retrieval Jaccard / weighted overlap
- source exposure Gini / HHI / coverage
- pairwise semantic distance
- cluster entropy / effective cluster count
- Diversity Growth Rate（已有文献）
- structured `problem × method` tuple collision
- nearest-literature distance（仅 proxy）
- blind human duplicate/distinctness annotation on a stratified subset
- feasibility / technical-depth validation，不能只用同一个 LLM judge

### Main figure target

画 pipeline stage：

```text
retrieval → generation → selection → refinement
```

同时画：

- portfolio diversity
- individual quality / feasibility

最强故事不是 “diversity 低”，而是：

> **系统优化单个 idea 时质量上升，但 portfolio diversity 在某个 stage 明显下降。**

然后用 intervention 证明具体 stage 的 causal effect。

---

## 7. Baselines / controls

必须至少覆盖：

- no retrieval
- random relevant retrieval
- top-k relevance
- MMR / coverage-constrained retrieval
- disjoint source neighborhoods
- high-temperature generation
- persona prompting
- multi-model generation
- generate-many + random select
- generate-many + LLM judge select
- generate-many + diversity-aware select

不要把“MMR 一定更好”写成预设结论；它只是 control/mitigation。

---

## 8. Kill / Continue gate

### Kill immediately if

1. diversified retrieval 只改变 wording，不改变 problem/method-level diversity；
2. 操纵 retrieval overlap 对 idea overlap 没有稳定影响；
3. effect 只在一个 embedding metric 上成立；
4. prompt paraphrase 可把 effect 完全抹掉；
5. diversity gain 伴随明显 scientific quality collapse；
6. collision scan 找到已有论文已做同样的 stage-wise causal decomposition。

### Continue only if 至少满足 3 条

- >=2 model families 都复现 retrieval concentration → idea concentration；
- >=2 非等价 diversity metrics + 人工子集方向一致；
- fixed-candidate-pool 证明 selection 有独立 contraction effect；
- simple intervention 恢复 diversity 且质量损失有限；
- effect 跨 >=3 research areas；
- reviewer 可以一句话复述 main claim，而且 negative/alternative outcome 仍有知识价值。

---

## 9. 最近工作的定位

### vs. Si et al. ICLR 2025

他们问：LLM 能否生成 expert-level novel ideas，并把 diversity/self-evaluation 列为开放问题。

我们要问：**在 literature-grounded pipeline 中，collective diversity 到底在哪个 stage 丢失，retrieval/selection 是否具有 causal contribution？**

### vs. LiveIdeaBench 2026

它测试 minimal-context divergent thinking；我们测试 rich-context literature-grounded pipeline 和 population behavior。

### vs. RQ-Bench / novelty judge work

它们测试 judge 能否正确判断 novelty；我们测试 **judge selection 作为 selection pressure 是否改变最终 research portfolio**。

### vs. generic homogenization work

它们证明 LLM creative outputs 可同质化；我们必须进一步证明：

- scientific problem/method choice 而非文本 style 在收敛；
- source exposure / selection 可被干预并产生因果变化；
- 这个 effect 对 scientific ideation pipeline 的设计有实际后果。

### vs. Graph2Idea / Nova / IDEAgent 等 ideation systems

这些 work 的目标多为造更好的 ideation agent。我们的主贡献应是：

> **system-level failure discovery + causal decomposition + minimal correction**

而不是 another agent framework。

---

## 10. Anti-collapse topic filter v2

以后每个 candidate 必须先过：

```text
A. 普通 LLM brainstorm 是否高概率推荐？
   yes -> saturation penalty

B. 最近 8 个月是否已有相同 hidden assumption？
   yes -> collision penalty

C. 核心是否只是 new framework / benchmark / metric？
   yes -> weak，除非改变科学结论

D. 能否写成：
   “The field assumes X. Under controlled intervention Y, X fails because Z.”
   no -> mechanism penalty

E. 是否有 24–48h falsifiable pilot？
   no -> execution penalty

F. negative result 是否仍有知识价值？
   no -> fragility penalty

G. reviewer 能否一句话复述 main claim？
   no -> clarity penalty
```

---

## 11. 第三轮排序

1–5 分；Collision Risk 越高越差。

| Rank | Topic | Novelty | Mechanism | 48h pilot | ICLR fit | Collision Risk | Decision |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | **Shared-Retrieval Research Monoculture / stage-wise idea collapse** | 4.5 | 5 | 5 | 5 | 3 | **P0 pilot** |
| 2 | Judge-induced selection conservatism | 3.5 | 4.5 | 5 | 5 | 4 | merge into P0 RQ |
| 3 | Scaffold × backbone agent-ranking instability | 3 | 4 | 4 | 5 | 4.5 | backup |
| 4 | Model Editing locality stress | 2.5 | 4 | 5 | 5 | 4.5 | pause |
| 5 | Multi-turn state/error decomposition | 2.5 | 4 | 4 | 5 | 5 | pause |
| 6 | Causal memory utility | 2.5 | 4 | 4 | 5 | 5 | pause |
| 7 | Generic construct-validity benchmark | 2 | 3 | 4 | 4 | 5 | reject |

这些是研究决策分，不是录用概率。

---

## 12. ICLR 2027 deadline reality

截至 2026-09-06：

- Abstract: **2026-09-18 11:59 PM AoE**
- Full paper: **2026-09-25 11:59 PM AoE**

官方 CFP 明确提醒：典型 ICLR paper 的工作量显著高于 course project 或当前 AI agent 能自主完成的工作，并鼓励不够完整的工作继续打磨。

执行 gate：

```text
Sep 6–8   P0 pilot + latest collision scan
Sep 8     hard kill/continue
Sep 9–12  scale + mechanism ablation
Sep 12    claim freeze
Sep 13–17 human validation + figures + related-work lock
Sep 18    submit abstract only if evidence chain already strong
Sep 18–25 robustness + writing + reviewer red-team
```

**若 Sep 8–10 没有清晰、跨设置可复现的 main effect，转 ICLR 2028 quality-first。** 不因为 AI 能加速就强行提交。

---

## 13. Codex next executable task

Codex 先不要写 paper，也不要搭大一统 research agent。第一阶段只建：

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

第一项任务：

> 固定 3 个主题与一个小型 ICLR abstract corpus，跑 `no_retrieval / topk_retrieval / diversified_retrieval` 三条件各 >=30 seeds，保存完整 source + generation trace，输出 retrieval overlap、idea diversity、problem-method collision 的 bootstrap CI。

在 pilot signal 出来前：**不造复杂 agent、不发明新 metric、不写完整论文。**

---

## 14. Main sources

- ICLR 2027 CFP: https://iclr.cc/Conferences/2027/CallForPapers
- ICLR 2027 Reviewer Guide: https://iclr.cc/Conferences/2027/ReviewerGuidelines
- ICLR 2027 submission policy: https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/
- ICLR 2022 awards: https://blog.iclr.cc/2022/04/20/announcing-the-iclr-2022-outstanding-paper-award-recipients/
- ICLR 2023 awards: https://blog.iclr.cc/2023/03/21/announcing-the-iclr-2023-outstanding-paper-award-recipients/
- ICLR 2024 awards: https://blog.iclr.cc/2024/05/06/iclr-2024-outstanding-paper-awards/
- ICLR 2025 awards: https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/
- ICLR 2026 awards: https://blog.iclr.cc/2026/04/23/announcing-the-iclr-2026-outstanding-papers/
- Si et al., ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html
- LiveIdeaBench: https://www.nature.com/articles/s41467-026-70245-1
- Scientific novelty judge limits: https://arxiv.org/abs/2606.12071
- Diversity mechanisms: https://arxiv.org/abs/2602.20408
- Model-editing locality collision: https://arxiv.org/abs/2601.17343
- End-to-end AI research: https://www.nature.com/articles/s41586-026-10265-5

## 15. Evidence limitation

这是选题决策报告，不是 exhaustive systematic review。2026 arXiv / workshop 更新速度很快；任何主线进入 main experiment 前都必须再做一次最近 30–60 天 collision scan。尤其不能把“本轮没搜到直接重复”写成“世界上不存在相关工作”。”