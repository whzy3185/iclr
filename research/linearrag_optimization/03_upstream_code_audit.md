# LinearRAG 公开实现审计：论文—代码映射、差异与高价值修复点

> 审计对象：作者公开仓库 `DEEP-PolyU/LinearRAG`，读取时间 2026-09-10。  
> 本文不假设 issue 报告一定正确；把它们作为复现风险线索，并结合当前代码做静态分析。

## 1. 代码结构映射

核心文件：

```text
src/LinearRAG.py       indexing, entity activation, passage scoring, PPR
src/config.py          default hyperparameters
src/ner.py             spaCy/scispaCy NER
src/embedding_store.py embedding persistence via parquet
scripts/run.sh          dataset-specific settings
run.py                  dataset loading and end-to-end runner
```

论文的两个矩阵在实现里并未直接长期保存为 `M/C` 文件：

- sentence–entity 关系先保存为 dict；vectorized 模式 retrieval 开始时再构造 PyTorch sparse tensors；
- passage–entity 关系进入 igraph，用于 PPR；
- passage、entity、sentence embedding 分别存 parquet。

---

## 2. P0：BFS 与 vectorized retrieval 并不等价

这是我认为最优先的问题。

### 2.1 上游公开现象

Issue #26（2026-06-02）报告：MuSiQue 使用 paper/BFS 参数时，`use_vectorized_retrieval=True` 的结果显著低于 BFS，且 retrieval 约 5.4 s/query。这个 issue 截至本次审计时仍是 open。

这说明 matrix path 不能简单当作 BFS 的等价加速。

### 2.2 代码差异 A：first-hop tier off-by-one

BFS 路径：

```text
seed tier = 1
first propagated entity tier = iteration + 1 = 2
```

vectorized 路径：

```text
seed tier = 0
first propagated entity tier = iteration = 1
```

`calculate_passage_scores()` 后面使用：

```text
entity_bonus ∝ entity_score / tier
```

虽然 seed 的 `tier=0` 会被 special-case 到 denominator 1，但第一跳没有 special case，因此 vectorized 第一跳实体相对 BFS 被放大约 2×。

这会直接改变 passage initialization，而不是仅改变日志。

本分支有 `tier_consistency_regression.py` 构造了一个可翻转 passage ranking 的最小例子。

### 2.3 代码差异 B：多路径聚合方式不同

BFS：

- 对每个 current entity 独立取 top-k sentences；
- 对每条 entity→sentence→next-entity 路径计算 `entity_score * sentence_score`；
- `entity_weights[next] += score` 会累积；
- 但 `new_entities[next] = (...)` 和最终 `actived_entities` 保存的是最后一次写入的单个 path score。

vectorized：

- 先把所有 current entity 对某 sentence 的贡献求和成 `sentence_activation`；
- 再乘 sentence similarity；
- 通过 `S2E` 一次性把所有路径求和；
- `actived_entities` 保存的是聚合后的 summed score。

因此后续 passage bonus 读到的 activated entity score 语义根本不同。

### 2.4 代码差异 C：duplicate seed 行为也不一致

如果两个 query mentions 都映射到同一 entity：

- sparse COO `coalesce()` 可能把 duplicate seed score 相加；
- dense `scatter_` 会后写覆盖；
- BFS dict 又会去重/覆盖。

同一函数内部就存在两个 seed accumulator 语义。

### 修复建议

先写一个 50–100 个随机小图的 differential test：

```text
reference implementation
vs BFS
vs vectorized CPU
vs vectorized CUDA
```

逐 hop 比较：

```text
frontier entity IDs
entity scores
first activation hop
used sentence IDs
passage prior
PPR top-k
```

在完全一致之前，不要用不同 backend 分别调参来“追结果”，否则会把算法差异伪装成 hyperparameter sensitivity。

---

## 3. P0：公开代码的图结构与正文描述有额外差异

### 3.1 实现添加了 passage-passage adjacent edges

`index()` 在 entity-passage edges 之后无条件调用：

```text
add_adjacent_passage_edges()
```

该函数从 passage text 的数字前缀读取全局 index，然后把 `i` 和 `i+1` 的 passage 相连。

但正文 Tri-Graph 明确强调两类边：

- entity–sentence；
- entity–passage。

正文没有描述 passage–passage chain。

这件事非常值得单独 ablate，因为：

1. 它可能是在重新切 chunk 后恢复局部连续性，确实有效；
2. 也可能跨 document boundary 把不相关 passage 相连；
3. 它会让“仅靠 aligned entities 连接跨 passage 信息”的机制解释变得不纯。

建议引入显式 `document_id/local_chunk_idx`：

```text
no adjacency
within-document adjacency
current global sequential adjacency
```

三组对照。

### 3.2 P–E 边不是正文的 binary C

代码 `add_entity_to_passage_edges()` 使用：

```text
edge_weight = entity_occurrence_count / total_entity_occurrence_in_passage
```

而正文 Sec. 3.1 的 contain matrix `C` 是 binary indicator。

这可能是合理实现细节，但论文的“binary graph construction”与 PPR 实际权重需要更明确。建议复现实验把 binary/count-normalized 两者拆开。

---

## 4. P0：chunking 是主要可复现性变量

Issue #25 提出作者发布的 chunks 与原 benchmark split 数量/结构不同。作者在回复中解释：

- 原数据按 title/topic boundary 分段过于理想；
- 他们将原 chunks 合并，再按固定 token length 重切，以模拟真实长文档；
- 所有 baseline 使用相同 re-chunking，因此作者认为比较公平。

这段解释是合理的，但仍然意味着 **chunking 是方法效果的一部分**，不能只作为隐藏预处理。

建议后续报告完整 2×3 matrix：

```text
chunk source:
  original benchmark chunks
  merged + fixed-token re-chunk

method:
  Vanilla RAG
  LinearRAG
  strongest GraphRAG baseline(s)
```

并报告：

- average chunk tokens；
- gold evidence co-location rate（一个 chunk 是否已经包含多跳所需的多条证据）；
- number of chunks；
- NER entities/chunk；
- P–E degree distribution。

否则很难判断收益来自 graph retrieval 还是 chunk granularity。

---

## 5. P0/P1：NER fallback 必须可观测

`retrieve()` 在 query NER 为空时直接 dense fallback。

Issue #25 的讨论中，有复现者指出 Medical 上默认 spaCy 可能造成极高 fallback；作者回复目前 Medical 使用 `en_core_sci_scibert`，用于改善 biomedical NER。

这提示一个重要点：**LinearRAG 的 graph path 使用率本身就是核心指标。**

每个 dataset 应至少报告：

```text
query_ner_empty_rate
seed_match_below_margin_rate
mean_seed_count
fallback_dense_rate
mean_activated_entity_count
mean_hops_before_stop
```

如果一个数据集 80–90% query 都 fallback，那么那个数据集上的 end-to-end 结果不能强力支持 graph stage 的有效性。

---

## 6. P1：passage initialization 目前有明显 Python 热点

`calculate_passage_scores()`：

1. 先对所有 passage 计算 dense similarity 并完整排序；
2. 对每个 passage；
3. 再遍历每个 activated entity；
4. 用 `passage_text_lower.count(entity_lower)` 重新数 occurrence。

这有三个问题。

### 6.1 已有 incidence/count 信息却重复扫文本

index 阶段已经知道 passage 包含哪些 entity。应该直接保存 count sparse matrix：

```text
N[p,e] = occurrence_count
```

然后：

```text
entity_weight[e] = a[e] / L_e
bonus_mass = log1p(N) @ entity_weight
```

一次 SpMV 即可。

本分支 microbenchmark 在 20k passages / 10k entities / 64 active entities 上，稀疏 matvec 与一个“比真实 str.count 更有利”的 Python membership baseline 数值完全一致，最小计时约快 1900×。这不是端到端速度预测，但足以说明优化价值。

### 6.2 `str.count` 不是可靠的 entity occurrence 计数

它可能：

- 对 substring 产生 false count；
- 忽略 NER span 的边界定义；
- 每个 query 重新做本来可以 offline 固定的工作。

应该在 NER/index 阶段保存 span-derived count。

### 6.3 dense passage retrieval 不需要 full sort

Stage 2 初始化只需要每个 passage 的 similarity vector，并不需要按 similarity 完整排序。当前 `dense_passage_retrieval()` 做 `argsort` 全排序后又遍历全部 passage，存在无必要 `O(P log P)`。

建议拆成：

```text
compute_passage_similarity_vector()  # no sort
fallback_dense_topk()                # argpartition/topk only when needed
```

---

## 7. P2：所谓 vectorized path 仍大量 densify

`calculate_entity_scores_vectorized()` 每 hop 会：

- sparse entity vector → `.to_dense()`；
- sparse mm 得到 sentence activation 后转 dense；
- next entity scores 也是 dense；
- per active entity 还用 Python loop 做 sparse row indexing + top-k。

这会在大 `|E|,|S|` 下让“激活向量本身很稀疏”的优势打折。

更好的 backend 可以是：

- CSR adjacency + frontier gather；
- segmented top-k / top-k per source entity；
- scatter-reduce 到 sentence/entity；
- 保持 frontier COO，不构造全长 dense score；
- 或者用 PyTorch Geometric / torch_scatter 风格的 edge-index kernel。

另一个小点：代码同时保存 E→S 和 S→E 两份 sparse tensor，实际上后者是前者 transpose，可考虑只持有一种主结构和必要的 CSR/CSC views，避免重复 edge storage。

---

## 8. P2：全图 PPR 可以考虑局部化

`run_ppr()` 对完整 igraph 执行 personalized PageRank。论文把其复杂度描述为随边数线性，这在 1M 节点级仍能做到 ~0.1 s 是不错的，但如果 corpus 继续扩大，query-local computation 更有吸引力。

可以把 activated entities 的 incident passages + dense top-L 作为局部 seed neighborhood，做 push-based approximate PPR：

```text
local PPR first
if boundary residual > ε:
    expand one ring
if still high:
    fallback full PPR
```

这样有明确的 quality/speed trade-off，可形成比纯工程重写更强的研究故事。

---

## 9. 其他实现级问题

### `SpacyNER.batch_ner()` 的 batch size

当前：

```text
batch_size = len(passage_list) // max_workers
```

当 passages 数少于 workers 时可能得到 0。应 `max(1, ...)`。

### `question_ner()` lowercases query entity，而 corpus entity 保留原 casing

因为最终是 embedding matching，不一定错误。但建议 canonicalization 显式化：Unicode normalize、casefold、alias table、punctuation normalization；并把 raw/canonical text 都保存，便于复现。

### EmbeddingStore 每次 upsert 重写整个 parquet

增量 corpus 很大时 append/update 成本会变高。可以考虑：

- shard parquet；
- memmap embeddings + sqlite/arrow metadata；
- append-only manifest。

这不影响算法 accuracy，但影响论文强调的 growing-corpus scalability。

---

## 10. 优先修复顺序

```text
P0.1 differential semantics test (reference/BFS/vectorized)
P0.2 fix hop/tier + multi-path aggregation semantics
P0.3 expose and ablate passage adjacency
P0.4 chunking + NER fallback manifest
P1.1 vectorize passage prior from stored sparse count matrix
P1.2 context-conditioned seed selection
P1.3 degree/IDF hub correction
P1.4 fixed floor + frontier budget
P2.1 sparse frontier backend without densify
P2.2 local approximate PPR
P2.3 sharded incremental embedding/index store
```

这个顺序的原则是：先确保“同一算法不同 backend 的结果一致”，再优化模型；否则每个性能变化都可能只是实现语义漂移。
