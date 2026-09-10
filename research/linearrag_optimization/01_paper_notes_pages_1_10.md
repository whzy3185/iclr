# LinearRAG 正文 1–10 页精读笔记

## 1. 一句话理解

LinearRAG 的核心不是“用更好的知识图谱做 RAG”，而是**否定传统 GraphRAG 里显式 relation extraction 是必要步骤**：只抽实体，保留原始句子/段落作为关系语义载体，用 entity–sentence 与 entity–passage 的稀疏 incidence structure 建索引，再在查询时做语义传播和 PPR。

这是一种把错误来源从“离线硬结构”转成“在线软权重”的设计。

---

## 2. 第 1 页：问题定义和核心立场

摘要和 Introduction 给出三个关键判断：

1. 普通 RAG 在大规模非结构化语料上遇到的信息碎片化问题，尤其是 multi-hop 场景。
2. GraphRAG 的优势来自显式结构，但 relation extraction 会制造两类结构性噪声：错误关系和不一致关系。
3. 与其进一步修关系，不如取消关系抽取，只保留 entity alignment 与原文。

论文提出的 Tri-Graph 包含 entity / sentence / passage 三种粒度。它强调：

- graph construction 只需要 NER + semantic linking；
- 不需要 LLM token；
- 随 corpus size 线性扩展；
- retrieval 分为 entity activation 和 passage retrieval 两阶段。

### 我对第 1 页的理解

这其实是一个“**结构最小主义**”观点。传统 KG 试图把文本压缩成 `(head, relation, tail)`，LinearRAG 认为这种压缩既贵又会丢失否定、语气、上下文和复合关系。因此它只把“谁和哪个文本单元共现”离散化，把“是什么关系”留在文本里。

这个观点很强，但它隐含一个新依赖：如果不抽 relation，那么系统是否能可靠地通过 query-sentence similarity 找到正确桥接句？也就是说，relation extraction 的误差被换成了 **NER quality + embedding geometry + propagation calibration** 的误差。后续优化应围绕这三项，而不是重新添加 OpenIE。

---

## 3. 第 2 页：三类 RAG 范式与 GraphRAG 失败原因

Figure 1 把系统并列为：

- Naive RAG：chunk → embedding → retrieval；
- GraphRAG：NER + relation extraction → KG → subgraph retrieval；
- LinearRAG：NER + semantic linking → Tri-Graph → passage retrieval。

正文给出 GraphRAG 的两类问题：

- **local inaccuracy**：单条关系抽错；
- **global inconsistency**：各 passage 独立抽关系，没有全局一致性约束。

论文的动机不是说“图没用”，而是说“**关系图的构建方式不稳**”。因此 LinearRAG 仍然保留图式传播，只是把图改成更可靠的 incidence graph。

### 优化启发

如果我们接受作者的诊断，那么任何优化都应通过一个检查：**它是否重新引入了一个和 relation extraction 一样难以验证的离线结构？**

例如让 LLM 给 entity-entity 边打关系标签，很可能违背论文最重要的 design win。相反，query-time 的连续权重、degree correction、local contextualization 不改变索引事实，更符合论文哲学。

---

## 4. 第 3 页：preliminary study 的真正含义

Figure 2(a) 的核心不是 GraphRAG recall 差，而是 **recall 与 relevance 的 trade-off 被破坏**。论文在 Medical 上报告：一些 GraphRAG 方法 evidence recall 很高，但 context relevance 明显低于 Vanilla RAG。作者把这解释为图扩展引入噪声。

Figure 2(b) 用两个例子强调关系错误：

- 否定句被抽成正向事实；
- “AI 的子类/技术/领域”在不同文本里被扁平抽成同一类关系，造成层次错乱。

### 我认为最重要的实验问题

论文后面所有优化都应围绕一个二维目标，而不是只看 answer accuracy：

- `Evidence Recall`：真正需要的证据是否被覆盖；
- `Context Relevance / Precision`：引入了多少噪声。

这也说明我们提出 degree normalization、frontier budget、adaptive top-k 时，必须同时看两者。单纯减少 active entities 可能把 recall 一起砍掉；单纯扩大 frontier 又会复现 GraphRAG 的原始问题。

---

## 5. 第 4 页：Figure 3 和两个中心主张

Figure 3 是整篇论文最重要的图。数据流分成：

### Offline construction

`corpus → passage → sentence → entity → semantic linking → Tri-Graph`

这里的“semantic linking”主要是实体文本/embedding 对齐和 incidence 建边，不是 relation extraction。

### Online stage 1：entity activation

`query → NER → initial entities → query-sentence relevance → iterative semantic propagation → dynamic pruning → activated entities`

### Online stage 2：passage retrieval

`activated entities + query-passage similarity → hybrid passage initialization → PPR on entity-passage graph → top-k passages`

论文在 Sec. 3 前提出两个中心 claim：

1. aligned entities 是跨 passage 连接信息的主要 anchor；
2. contextual relations 最好保留在原文，而不是显式抽取。

### 我对 Figure 3 的再解释

可以把 LinearRAG 看成两个 coupled bipartite systems：

- `S ↔ E` 用于**找桥**；
- `P ↔ E` 用于**聚合证据重要性**。

Sentence 节点不直接作为最终 evidence 返回，passage 节点不直接参与第一阶段传播。这个解耦非常干净，也意味着两阶段可以分别优化、分别做误差诊断。

---

## 6. 第 5 页：Tri-Graph 构建和初始激活

Sec. 3.1 定义两个二值矩阵：

- contain matrix `C ∈ {0,1}^{|P|×|E|}`；
- mention matrix `M ∈ {0,1}^{|S|×|E|}`。

这种表示的优势是：

- 新 passage 到来时只做 sentence segmentation + NER + append edges；
- `C`、`M` 极稀疏；
- 原文 passage 保留，因此构建阶段没有信息压缩损失。

Sec. 3.2.1 的 query 初始化：

- 对 query 做 NER 得到 `E_q`；
- 每个 query entity 在全图 entity 中找最相似的一个；
- 初始激活分数就是这个最大相似度。

然后计算所有 sentence 与 query 的相似度 `σ_q`。

### 第一个明显优化点：seed selection

“每个 query entity 只取一个全局最近邻”对同名异义、简称、实体边界错误很敏感。论文 FAQ 后面说 sentence-level context 可以缓解 polysemy，但如果第一步就选错 seed，正确 sense 的局部邻域可能根本没有机会被传播。

更稳健的方案是：

- 对每个 mention 保留 top-m candidate；
- seed score = entity surface similarity + full-query-to-candidate-context similarity；
- 当 top1-top2 margin 大时退化成单 seed，margin 小时保留多个候选；
- 后续 sentence propagation 再竞争淘汰。

这样仍是 token-free、relation-free。

---

## 7. 第 6 页：Eq. (5) 是最值得优化的地方

论文的 semantic propagation：

```text
a_q^t = MAX(M^T (σ_q ⊙ (M a_q^{t-1})), a_q^{t-1})
```

直观解释：

1. 当前 entity activation 通过 `M` 投影到 sentence；
2. sentence activation 乘 query-sentence relevance；
3. 再通过 `M^T` 投影回 entity；
4. 与上一轮分数取 max，保留已有激活。

论文强调 `M` 稀疏，可用 SpMM；hop 数通常 ≤4。

### 这个公式的潜在 hub bias

原始 `M` 是 binary，求和传播意味着：

- 一个出现在很多句子的高频实体有更多累积路径；
- 一个句子同时连接多个当前 active entity 时，activation 会叠加；
- 高频通用实体可能因为“路径数多”而不是“语义更相关”获得高分。

作者用 threshold `δ` 做 dynamic pruning，但 threshold 解决的是“低分节点”，不直接解决“高 degree 造成的高分”。

因此我把 **degree-normalized semantic bridging** 放在 P1：

```text
raw:        M^T diag(σ) M a
normalized: D_e^{-1} M^T diag(σ) M a
```

或者对称归一化：

```text
D_e^{-1/2} M^T D_s^{-1/2} diag(σ) D_s^{-1/2} M D_e^{-1/2} a
```

注意这不是新增关系，也不增加 LLM 成本。

### 关于 pruning

论文主张 fixed threshold 比“随 hop 衰减 threshold”更好。我的优化建议不是再次做 decay，而是：

- 固定 `δ_floor` 作为语义底线；
- 如果某 hop 超过预算 `B`，再对超过阈值的节点保留 top-B；
- `B` 可以和 query ambiguity / seed count / frontier entropy 相关。

这样避免了论文已经否定的“距离越远阈值越低/高”的手工规则。

---

## 8. 第 6 页下半：PPR 与 passage initialization

第二阶段在 `P ↔ E` 图上做 Personalized PageRank。论文 Eq. (7) 里 passage reset/initial score 同时使用：

- query-passage dense similarity；
- activated entity 的 score；
- entity 在 passage 中的 occurrence count；
- entity hierarchical level；
- passage node weight；
- trade-off coefficient `λ`。

### 第二个 hub bias

如果一个 entity 在很多 passages 里出现，它会把 PPR mass 分散到大量文本；更糟的是在 reset prior 里也可能重复贡献。一个自然的 relation-free correction 是 entity IDF：

```text
idf(e) = log((|P|+1)/(df(e)+1)) + 1
```

然后 entity contribution 乘 `idf(e)` 或除以 degree。这与 IR 里抑制 stopword/common term 的思路相同，但作用在 entity graph 上。

### 局部 PPR 的机会

第一阶段已经给出很小的 activated entity set。理论上第二阶段不一定要在全图上做 PPR；可以用 activated entities 和高分 dense passages 构造 query-induced subgraph，再 local-push PPR。这样 retrieval 复杂度可能从“全图线性”进一步下降为“局部近似”。

---

## 9. 第 7–8 页：实验设计和结果解读

Table 1 使用 HotpotQA、2Wiki、MuSiQue、Medical。所有 RAG 方法统一 embedding（all-mpnet-base-v2）、top-k=5、generator/evaluator GPT-4o-mini。

LinearRAG 在四个数据集上都优于表中 baselines。尤其 2Wiki：

- Contain-Acc 70.20；
- GPT-Acc 63.70。

作者的 Obs. 2 强调 GraphRAG 能找 vanilla RAG 漏掉的结构依赖；Obs. 3 再说传统 GraphRAG 的问题是 graph quality，LinearRAG 通过简化图构建规避。

### 对结果的保守解读

Table 1 支持“在作者评测设置下，relation-free graph retrieval 可以强于显式关系 GraphRAG”。它还不能区分这些收益分别来自：

- Tri-Graph 本身；
- 特定 chunking；
- NER 模型；
- dataset-specific retrieval hyperparameters；
- adjacent passage edges（公开实现里存在，论文正文未描述）；
- generator prompt / evaluator sensitivity。

因此后续复现必须把这些因素拆开。

---

## 10. 第 9 页：效率和 ablation

Table 2 是论文工程价值最强的结果：在 2Wiki 上 LinearRAG 报告：

- indexing 249.78 s；
- average retrieval 0.093 s；
- indexing/retrieval prompt/completion token 均为 0；
- accuracy（Contain/GPT 平均）66.95。

Ablation Figure 4 表明：

- 去掉 entity activation 明显掉点；
- 去掉 global importance aggregation 也掉点；
- 两阶段互补。

### 我最关心的实现问题

“vectorized matrix computation”理论上应更接近 Eq. (5)，但公开实现同时提供 BFS 和 vectorized 两条路径。上游 issue #26 报告 MuSiQue 上 vectorized 模式无法复现 BFS 性能。这个问题比再调一个超参更优先，因为它关系到论文声称的稀疏矩阵加速是否和算法语义一致。

---

## 11. 第 10 页：pruning 和 evaluator robustness

Table 3 比较：

- fixed threshold：Acc 66.95 / 0.093 s；
- no pruning：64.50 / 0.186 s；
- dynamic threshold ×0.5：65.15 / 0.123 s；
- dynamic threshold −0.1：65.35 / 0.095 s。

这很好地说明“更多扩展”并不更好。值得注意的是作者反对的是 **distance-dependent decay**，不是所有 query-adaptive pruning。

Table 4 用三个 evaluator 检验相对排名，LinearRAG 仍保持领先，缓解单一 evaluator bias 的担忧。

---

## 12. 附录补充阅读：只摘与优化有关的点

### Retrieval quality（Appendix E.1）

LinearRAG 的特色是 relevance 与 recall 同时较高。这强化了我们优化时的双目标评价：不能只报 answer accuracy。

### Hyperparameter（E.2）

Figure 5 的 threshold 横轴约在 0.2–0.8；文字末尾却写“set δ = 4”。这与图和公开 `run.sh`（2Wiki/Hotpot threshold 0.4，Medical 0.5，MuSiQue 0.1）不一致，应该视为文稿/实现需要核对的可复现性点，而不是直接接受某个数值。

### Embedding robustness（E.3）

多种 sentence embedding 性能差异不算巨大，说明方法不是强依赖某个唯一 encoder。但这不等于 seed disambiguation 没有优化空间，因为 homonym/margin 是局部失败模式，平均 benchmark 可能掩盖它。

### Scaling（E.4–E.5）

作者报告 indexing 随规模扩展良好，largest graph retrieval 约 0.1 s。即使如此，上游代码仍有明显的 Python nested loops 和 dense conversion，说明还有纯工程加速空间。

### FAQ polysemy / entity-free query

作者承认 polysemy，并依赖 sentence context + passage dense similarity 缓解；query 无可抽 entity 时回退 dense retrieval。这实际上给出了两个很好的 instrumentation 指标：

- `NER fallback rate`；
- `ambiguous seed rate / top1-top2 margin`。

它们应该成为真实实验的标准诊断输出。

---

## 13. 精读后的核心问题清单

我认为最值得真正跑实验回答的不是“还能不能多 1 个点”，而是：

1. LinearRAG 的收益在统一的原始 benchmark chunking 下还能保留多少？
2. BFS 与 vectorized retrieval 是否能做到逐 query、逐 hop 的 activation 等价？
3. 高频 entity hub 是不是主要噪声来源之一？degree correction 是否能改善 relevance 而不损 recall？
4. query entity top-1 matching 的错误率有多高？context-conditioned top-m seeds 是否主要帮助 polysemy/alias query？
5. PPR 的增益来自真正的 global aggregation，还是来自 passage initialization 本身？
6. 公开实现的 passage-passage adjacent edges 对结果贡献多少？它们是否跨文档误连？
7. domain-specific NER（如 SciSpacy）能否系统降低 fallback，并让 Medical 上的 graph stage 真正参与而不是退化为 dense RAG？
8. 若第二阶段改成 local-push PPR，能否保持质量同时把 0.1 s 进一步压到更低，并随 corpus 增长保持近似局部复杂度？
