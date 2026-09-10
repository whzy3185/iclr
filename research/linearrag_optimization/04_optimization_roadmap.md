# LinearRAG 优化路线图：从可复现性修复到可发表扩展

## 0. 设计约束

所有优化先遵守四条约束：

1. **不破坏 relation-free indexing。** 不把 LLM relation extraction 加回来。
2. **不牺牲 recall 只换 relevance。** 必须同时报告 evidence recall 与 context relevance/precision。
3. **不把 backend 差异当算法提升。** BFS/vectorized 先对齐。
4. **每个改动都可以单独 ablate。** 避免一次性叠加 5 个 trick 后无法解释。

---

## P0-A：Reference Semantics + Differential Testing

### 问题

当前 BFS 和 matrix/vectorized 路径存在 tier、多路径聚合、duplicate seed 等语义差异，上游 issue #26 已出现实际掉点。

### 改动

写一个 100 行左右的 CPU reference implementation，固定：

- seed aggregation = max；
- per-hop frontier；
- sentence top-k；
- used sentence policy；
- entity score aggregation = max 或 sum（二选一并冻结）；
- first activation hop；
- passage prior。

然后所有 backend 做 differential test。

### 成功标准

```text
activated entity set Jaccard = 1.0
max entity score abs diff < 1e-6
first hop exact match = 100%
passage prior max abs diff < 1e-6
PPR top-20 exact/order-equivalent within tolerance
```

### 研究价值

主要是 correctness / reproducibility，不是新算法，但这是所有后续结论的地基。

---

## P0-B：Chunking-Controlled Evaluation

### 问题

公开 issue 显示 chunking 可能显著影响结果；作者解释使用 merged + fixed-token re-chunk 模拟真实长文本，并对所有 baseline 一致处理。

### 改动

对每个 benchmark 至少同时跑：

- original official chunks；
- author released/reconstructed chunks；
- fixed token 256/512/1000（可选）。

### 新指标

```text
gold_evidence_colocation_rate
mean / p95 chunk tokens
entities per chunk
sentences per chunk
P-E edge degree distribution
```

### 关键问题

如果 LinearRAG 只在某种 re-chunking 下优势显著，论文故事应改成“relation-free retrieval 与 chunk granularity 有强耦合”，而不是宣称普遍优于 GraphRAG。

---

## P0-C：NER Coverage and Fallback Instrumentation

### 问题

LinearRAG 是 entity-anchored；query NER 失败就退化到 dense RAG。Medical 需要 SciSpacy 是合理现象，但必须量化。

### 改动

每个 query 输出：

```json
{
  "query_entities": [],
  "seed_candidates": [],
  "seed_margin": 0.0,
  "fallback": false,
  "activated_entities": 0,
  "hops": 0
}
```

### 成功标准

任何 accuracy 表旁边都能回答：到底多少 query 真正使用了 LinearRAG graph path？

---

## P1-A：Context-Conditioned Multi-Seed Disambiguation

### 假设

top-1 entity text nearest neighbor 对 homonym/alias 易错；用 full query 对候选 entity 的邻接句上下文重排可降低错误 seed。

### 公式草案

```text
score(e|m,q) = α sim(m,e) + (1-α) max_{s∈Nbr(e)} sim(q,s)
```

margin 大：只保留 top1；margin 小：保留 top-m。

### 为什么不违背论文

- 仍用已有 sentence embedding；
- 无 LLM token；
- 无 relation extraction；
- 只增加 query-time scoring。

### 关键 ablation

```text
surface-only top1
surface-only top-m
context rerank top1
context rerank adaptive top-m
```

### 风险

检索候选上下文可能增加 latency。可只在 top1-top2 entity similarity margin 小于阈值时触发。

---

## P1-B：Degree-Normalized Semantic Bridging

### 假设

raw sum propagation 偏向 high-degree entities，导致 hub noise 和 frontier 爆炸。

### 最小改动

```text
b = D_e^{-1} M^T diag(σ) M a
```

更复杂版本再尝试 symmetric normalization。

### 已做最小实验

在构造 hub-noise 图中：

- raw propagation 平均激活 ~289 entities；
- degree-normalized 只激活 4 个 gold-chain entities；
- gold entity recall=1.0；
- top-5 passage recall 在该 toy case 中两者都为 1.0。

所以目前证据只支持“控噪而不伤 toy recall”，不能声称真实 benchmark 提升。

### 真实实验 success criterion

至少满足其一：

- context relevance +2pt 且 evidence recall 下降 <0.5pt；
- answer accuracy +1pt 且 retrieval time 不增加 >10%；
- activated entities / query 降低 >30%，accuracy 持平。

---

## P1-C：Fixed Semantic Floor + Frontier Budget

### 假设

论文已经证明 no-pruning 和 hop-decaying threshold 都较差；但固定阈值仍可能在某些 ambiguous query 上保留过多实体。

### 改动

保留固定 `δ_floor`：

```text
keep score >= δ_floor
if frontier size > B:
    keep top-B
```

`B` 先固定，再尝试由 entropy/seed ambiguity 自适应。

### 价值

可提供 deterministic latency cap，并避免 query-specific combinatorial explosion。

---

## P1-D：Hub-Aware Passage Reset / PPR

### 假设

高 df entity 对很多 passage 提供弱连接，会降低 context relevance。

### 改动

```text
w_e = a_e * idf(e) / L_e
idf(e)=log((|P|+1)/(df(e)+1))+1
```

可只在 passage prior 使用，不改 Stage 1，便于隔离效果。

### 风险

某些真正关键实体本身很常见（国家、疾病类别等），过强 IDF 可能伤 recall。需要 capped IDF 或 learned scalar。

---

## P1-E：Vectorized Passage Prior

### 问题

当前上游实现对 passage × activated entity 做 Python loop 和 `str.count`。

### 改动

offline 保存 sparse count matrix `N`：

```text
N[p,e] = NER span occurrence count
```

online：

```text
w[e] = activation[e] / level[e]
entity_mass = log1p(N) @ w
passage_prior = λ * dense_sim + log1p(entity_mass)
```

### 已做 microbenchmark

合成 20k passages / 10k entities / 64 active entities：

- Python nested membership：~0.153 s；
- CSR matvec：~0.00008 s；
- max abs diff = 0；
- ~1900× microbenchmark speedup。

真实 `str.count` 更慢，但真实系统还有 embedding/PPR 等开销，因此不能把 1900× 外推成端到端速度。

### 预期

这是“低风险高收益”的工程改动，建议最先落地。

---

## P1-F：Passage Adjacency Boundary Fix + Ablation

### 问题

公开实现无条件连接全局连续 passage，但正文没有这类边。

### 三个版本

```text
A no passage-passage edges
B within-document adjacency only
C current global sequential adjacency
```

### 可能结果

- 若 B > A：说明局部文档连续性是有效结构，应写进方法；
- 若 C > B：需警惕 benchmark chunk ordering leakage / 偶然共线；
- 若 A≈B≈C：删除复杂度和解释负担。

---

## P2-A：True Sparse Frontier Backend

### 问题

当前 vectorized 实现每 hop densify 全长 E/S 向量，且 per-entity top-k 仍 Python loop。

### 改法

用 edge list / CSR：

```text
active entity indices
→ gather incident sentence edges
→ segmented top-k by source entity
→ scatter-add weighted sentence mass
→ gather S→E edges
→ scatter-reduce entity mass
→ threshold/top-B
```

### 指标

```text
latency vs |E|, |S|, nnz, frontier size
peak GPU memory
activated frontier size
BFS-equivalence tests
```

---

## P2-B：Local Push PPR

### 假设

PPR 的有效 mass 大部分集中在 activated entity 附近，没必要每 query 扫全图。

### 改法

- 从 activated entities + dense top-L passages 建局部子图；
- push residual，直到 `r(v) < ε deg(v)`；
- boundary residual 超阈值时扩图；
- 以 full-graph PPR 为 reference。

### 成功标准

```text
retrieval latency -50% or better on 10M+ token corpus
Recall@5 loss <0.5pt
top-20 Kendall/Spearman high correlation
```

### 论文潜力

如果成立，它把 LinearRAG 的“线性全图复杂度”进一步推进为“查询局部复杂度”，研究价值明显高于单纯代码重构。

---

## P2-C：Learned Query-Time Calibration（谨慎）

可以训练一个很小的 calibration model 输入：

```text
seed margin
frontier entropy
entity degree stats
query length/type
sentence similarity distribution
```

输出：

```text
threshold
frontier budget
PPR damping
passage similarity weight
```

但这会引入训练数据和 overfitting 风险。建议只有在 P1 的手工机制有清楚规律后再做，不宜一开始就用 learned policy 掩盖问题。

---

## 5. 推荐的“最小可发表”组合

如果只选一个研究扩展，我会优先：

> **Calibrated Sparse LinearRAG：context-conditioned seed + degree-normalized bridging + local PPR**

它保留原论文最核心的 relation-free 优势，同时正面解决三个残余瓶颈：

```text
错误 seed
→ hub propagation noise
→ full-graph retrieval cost
```

但最终能否成为论文贡献，取决于是否在原始 chunking、re-chunking、不同 domain NER 下都稳定，而不是只在 2Wiki 上调出增益。
