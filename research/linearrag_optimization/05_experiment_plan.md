# LinearRAG 优化真实实验计划

## 1. 总原则

先复现，再优化；先 retrieval mechanism，再 generation；先固定 evaluation contract，再看结果。

建议把实验拆成四层：

```text
L0 correctness / differential tests
L1 retrieval-only experiments
L2 end-to-end QA
L3 scaling / robustness
```

---

## 2. L0：Correctness Gate

### 2.1 小图 differential suite

随机生成 100–1000 个小 Tri-Graph：

- 5–50 entities；
- 5–100 sentences；
- 3–30 passages；
- 随机 seed / query-sentence score；
- 包含 duplicate seeds、shared sentences、cycles、hub entities。

对比：

```text
reference CPU
upstream BFS
fixed vectorized CPU
fixed vectorized CUDA
```

Gate：所有核心 state 在 tolerance 内一致。

### 2.2 Hand-crafted regression cases

必须覆盖：

- first-hop tier；
- duplicate query entity；
- one sentence selected by two active entities；
- next entity reachable by multiple paths；
- threshold exactly equal boundary；
- empty NER；
- document boundary adjacency。

如果 L0 不通过，不进入 accuracy 比较。

---

## 3. 数据和 chunking matrix

数据：

- HotpotQA；
- 2WikiMultiHopQA；
- MuSiQue；
- Medical / GraphRAG-Bench subset。

每个数据至少两种 chunking：

```text
C0 original benchmark chunks
C1 author-style merged + fixed-token re-chunk
```

若资源允许再加：

```text
C2 fixed 256 tokens
C3 fixed 512 tokens
C4 fixed 1000 tokens
```

每个 chunking 保存 manifest：

```json
{
  "num_passages": 0,
  "mean_tokens": 0,
  "p95_tokens": 0,
  "gold_colocation_rate": 0,
  "mean_entities": 0,
  "mean_sentences": 0,
  "sha256": "..."
}
```

---

## 4. L1：Retrieval-only factorial design

### 4.1 Baseline

冻结一个可复现的 reference LinearRAG：

```text
seed = surface top1
bridge = raw / fixed threshold
passage prior = current reference
PPR = full graph
adjacency = explicitly specified
```

### 4.2 单因素优化

分别开启：

```text
A context seed
B degree normalization
C frontier budget
D passage IDF
E within-document adjacency
F vectorized passage prior (should be exact, not accuracy-changing)
G local PPR
```

### 4.3 组合

只组合通过单因素 gate 的模块：

```text
A+B
B+C
B+D
A+B+C+D
A+B+C+D+G
```

不要一开始跑所有 2^7 组合。

---

## 5. Retrieval metrics

主指标：

```text
Evidence Recall@k
Context Relevance / Precision@k
Gold supporting passage Recall@k (where available)
MRR / nDCG (if graded labels available)
```

机制指标：

```text
query NER empty rate
fallback dense rate
seed top1-top2 margin
seed correctness (人工小样本或 gold entity 可导出时)
activated entities per query
frontier size per hop
hops before stop
hub-degree of activated entities
PPR support size / residual
```

效率：

```text
p50/p95 retrieval latency
peak CPU RSS
peak GPU memory
index size on disk
indexing wall time
query-time FLOP/proxy counters
```

---

## 6. L2：End-to-end QA

为了避免 generator 噪声掩盖 retrieval mechanism，建议先在 frozen retrieved passages 上跑同一个 generator。

至少报告：

- Contain-Acc（与论文对齐）；
- GPT-Acc（与论文对齐，但记录 evaluator version/prompt）；
- EM/F1（对 Hotpot/2Wiki/MuSiQue 更标准）；
- answer length；
- abstention/error rate。

每个主要实验最好至少 3 个 retrieval/random seed（若 retrieval 本身确定，则 generation temperature seed 多次），但统计单位要区分 query-level 与 stochastic generation draws。

---

## 7. L3：Robustness axes

### 7.1 NER backend

```text
en_core_web_trf
lighter spaCy model
SciSpacy on Medical
optional domain NER
```

看优化是否只是补某个 NER 的缺陷。

### 7.2 Embedding backend

至少覆盖论文 Appendix 的两到三种 embedding；context-seed 和 hub correction 不应只在一个 embedding 上有效。

### 7.3 Corpus scale

合成/ATLAS-Wiki 子集：

```text
1M / 5M / 10M / 50M tokens (按资源调整)
```

重点画：

```text
latency vs graph nnz
memory vs graph nnz
local PPR visited edges vs full graph edges
```

### 7.4 Query complexity

按 gold hop 数或问题类型分层：

```text
1-hop / 2-hop / 3-4-hop
attribute query
entity-free/abstract query
ambiguous entity query
```

---

## 8. Hyperparameter discipline

要避免“每个 variant 单独调到最好”造成不公平。

建议：

1. baseline 参数按作者公开设置冻结；
2. 新模块只在一个 dev split 调自己的新增参数；
3. 不允许改 baseline 原参数来配合新模块，除非另做 joint-tuning 表；
4. 最终在 held-out split 报告；
5. 对 threshold/frontier budget 画二维 sensitivity，而不是只报最佳点。

特别注意：论文说 fixed threshold 优于 decaying threshold，但公开 `run.sh` 确实对不同 dataset 使用不同 threshold。不要误写成“一个 δ 全数据集通用”。

---

## 9. 判断标准：什么时候该放弃某个优化

### Context seed

如果只在手工 homonym case 有效，benchmark seed accuracy/QA 没改善且 latency 增加明显，就不要放主方法。

### Degree normalization

如果 relevance 上升但 evidence recall 明显下降，说明 normalization 太强。先做 capped correction，而不是继续调 threshold 掩盖。

### Frontier budget

若几乎从不触发，说明不是主要瓶颈；若频繁触发且伤 recall，说明应该解决上游 hub 而不是硬截断。

### IDF PPR

若 Medical/常见实体问题掉点，考虑 capped IDF 或只对极高 df percentile 实体启用。

### Local PPR

若为了保持 recall 必须访问 >70–80% 全图，则研究价值有限，可能只保留为工程 optional mode。

---

## 10. 推荐首轮实验顺序

```text
Day/Run 1: differential correctness suite
Day/Run 2: passage-prior vectorization exact-equivalence + speed
Day/Run 3: adjacency ablation + fallback instrumentation
Day/Run 4: degree normalization retrieval-only on 2Wiki + MuSiQue
Day/Run 5: context seed on ambiguous-query subset
Day/Run 6: combine A+B on all 4 datasets
Day/Run 7: local PPR scaling benchmark
Day/Run 8: full end-to-end generation only for surviving variants
```

这样能尽早杀掉无效思路，把昂贵 LLM generation 留到最后。
