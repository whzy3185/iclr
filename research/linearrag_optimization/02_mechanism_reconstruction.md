# LinearRAG 机制重构：从论文公式到可实现数据流

## 1. 为什么要重构一遍

论文的公式很简洁，但真正做优化需要明确：每个向量的维度是什么、哪些值是 query-independent、哪些值每个 hop 更新、threshold 在哪里应用、PPR reset 如何归一化、以及“hierarchical level”到底是 seed=0 还是 seed=1。

本笔记给出一个实现无关的 reference semantics。后续任何 BFS / sparse matrix / CUDA kernel 都应该先和这个 reference 对齐，再谈速度。

---

## 2. Offline state

定义：

- passages `P = {p_1,...,p_m}`；
- sentences `S = {s_1,...,s_n}`；
- entities `E = {e_1,...,e_r}`。

两个核心 incidence matrices：

```text
C ∈ {0,1}^{m×r}   passage × entity
M ∈ {0,1}^{n×r}   sentence × entity
```

理想情况下还需要以下元数据：

```text
entity_text[e]
sentence_text[s]
passage_text[p]
entity_degree_sentence[e] = Σ_s M[s,e]
entity_degree_passage[e]  = Σ_p C[p,e]
sentence_degree[s]        = Σ_e M[s,e]
passage_document_id[p]
passage_local_index[p]
```

最后两项非常重要：如果要保留相邻 passage 边，必须知道“是否属于同一原文档”，不能只依赖全局编号相邻。

---

## 3. Query initialization

### 3.1 Paper reference

query NER 得到 mentions `q_e`。每个 mention 取一个 entity nearest neighbor：

```text
seed(q_e) = argmax_e sim(q_e, e)
```

并把相似度写入 activation `a^0`。

### 3.2 建议的明确聚合规则

多个 query mentions 可能映射到同一个 entity。reference semantics 必须规定是：

- max；
- sum；
- noisy-or；
- last-write。

我建议 **max**，因为它与论文的 `MAX` persistence 更一致，也避免 query 中重复 mention 人为提高 seed mass：

```text
a^0[e] = max_{q_e→e} sim(q_e,e)
```

公开实现的 BFS / vectorized 路径在 duplicate seed 上存在不同的数据结构行为，因此应加单元测试。

### 3.3 Context-conditioned seed extension

对 candidate entity `e`，再取其若干关联句子的 full-query relevance：

```text
ctx(q,e) = max_{s:M[s,e]=1} sim(q,s)
seed_score = α sim(q_e,e) + (1-α) ctx(q,e)
```

如果 top1-top2 margin 足够大只保留一个；否则保留 top-m，让 Stage 1 再消歧。

---

## 4. Stage 1：semantic bridging

### 4.1 Literal matrix form

论文 Eq. (5)：

```text
z^t = M a^{t-1}
\tilde z^t = σ_q ⊙ z^t
b^t = M^T \tilde z^t
a^t = max(b^t, a^{t-1})
```

`σ_q[s] = sim(q, s)`。

### 4.2 一个必须澄清的问题：full diffusion 还是 frontier expansion

如果每一轮都用 `a^{t-1}` 的全部已有质量，旧路径会持续重复传播；如果使用“本轮新激活 frontier”，则更像 BFS。

两者不是同一个算法：

```text
full diffusion:     current = all accumulated activations
frontier expansion: current = newly activated/updated entities only
```

公开实现更接近 frontier expansion，并额外使用 `used sentences` 和 per-entity top-k sentence。论文展示公式却更像 full matrix update。

建议把 reference implementation 显式拆成三种模式并做 ablation：

- `literal_eq5`；
- `frontier_no_dedup`；
- `frontier_sentence_dedup_topk`（更接近当前代码）。

### 4.3 Fixed threshold 的准确定义

论文的“fixed threshold”应解释为：**不同 hop 使用同一个阈值**，而不是“所有数据集都用同一个阈值”。公开 `run.sh` 明显针对数据集设置 0.1/0.4/0.5 等不同值。

因此优化时要区分：

- `hop-invariant threshold`：论文支持；
- `dataset-invariant threshold`：论文没有证明；
- `query-calibrated threshold`：尚未验证。

### 4.4 Degree-normalized propagation

为了抑制 hub，我们可以只改变 query-time operator：

```text
b = D_e^{-1} M^T diag(σ) M a
```

或者：

```text
b = D_e^{-1/2} M^T D_s^{-1/2} diag(σ) D_s^{-1/2} M D_e^{-1/2} a
```

这不改变离线 graph，也不需要新增模型。

### 4.5 Frontier budget

建议：

```text
candidate = {e : score[e] >= δ_floor}
if |candidate| <= B:
    keep all
else:
    keep top-B by score
```

`B` 可由 query ambiguity 决定，但先从固定 B 做 clean ablation。

---

## 5. Hop/level 语义

论文 Eq. (7) 里有 `L_e`，直观上 seed 是第 1 层，第一跳桥接实体是第 2 层：

```text
hop index:   seed  first bridge  second bridge
0-based hop: 0     1             2
L_e:         1     2             3
```

因此统一规则应为：

```text
L_e = first_activation_hop + 1
```

这个细节不能被视为“只是日志”。它直接出现在 passage score 的分母里。我们的最小回归例子展示：如果第一跳误用 `L=1`，该实体对 passage 的贡献正好放大 2 倍，并可造成排序翻转。

---

## 6. Stage 2：passage initialization

论文 Eq. (7) 可拆成：

```text
DensePrior[p] = λ sim(q,p)
EntityPrior[p] = log(1 + Σ_e a[e] * f(count(p,e), L_e))
Init[p] = W_p * (DensePrior[p] + EntityPrior[p])
```

这里最适合做稀疏向量化。

若定义 entity query weight：

```text
w[e] = a[e] / L_e
```

以及 binary contain `C`，最简单的 entity mass 是：

```text
mass = C w
```

若需要 occurrence count，可将 `C` 从 binary incidence 改成 count matrix `N`，仍然可做 SpMV：

```text
mass = log1p(N) w
```

完全不需要：

```text
for every passage:
    for every activated entity:
        passage_text.count(entity_text)
```

这也是本分支 microbenchmark 的对象。

---

## 7. Hub-aware passage prior

令：

```text
df[e] = number of passages containing e
idf[e] = log((|P|+1)/(df[e]+1)) + 1
```

一个保守扩展是：

```text
w[e] = a[e] * idf[e] / L_e
```

更强的扩展可以用 BM25-like saturation 处理 occurrence count，但第一步不建议同时改太多自由度。

必要 ablation：

- no hub correction；
- sentence-degree only；
- passage-IDF only；
- both。

---

## 8. PPR reference semantics

建立 passage–entity bipartite adjacency：

```text
A = [[0, C],
     [C^T, 0]]
```

按 row degree 得到 transition `T`。reset vector `r` 包含 passage init 和 entity activation，并归一化。

标准 personalized PageRank：

```text
x_{k+1} = (1-d) r + d T^T x_k
```

直到 L1 residual 小于 tolerance。

需要记录：

- damping `d`；
- edge 是否 binary / count-normalized；
- reset 是否先归一化；
- dangling nodes 怎么处理；
- iteration tolerance / max iterations。

论文正文写 `d typically 0.85`，公开 config 默认是 0.5；这未必是错误，但复现实验必须把真实值写入 manifest。

---

## 9. Local PPR 变体

第一阶段已得到 `E_a`。可构造：

```text
P_local = passages incident to E_a
          ∪ top-L dense passages
E_local = entities incident to P_local
```

在局部子图上跑 PPR，若局部边界 mass 太高再扩一圈/回退全图。

好处：

- query 相关的计算规模；
- 易于批处理；
- 可以把全图 PPR 作为 gold/reference，测 rank correlation、recall loss 和速度。

这是一个比“再换 embedding model”更有潜在论文贡献的方向，因为它进一步推进了 LinearRAG 的 all-stage scalability 论点。

---

## 10. Reference invariants

建议所有后续实现都自动检查：

```text
I1: duplicate query mentions do not produce path-dependent seed mass
I2: BFS and vectorized modes match activated entity IDs under reference semantics
I3: first_activation_hop is identical across implementations
I4: passage prior vectors match within numerical tolerance
I5: PPR rank correlation > 0.999 on small exact graphs
I6: no passage-passage edge crosses document boundary
I7: entity fallback rate is logged per dataset/query type
I8: changing implementation backend does not require retuning semantic hyperparameters
```

如果 I8 不成立，所谓“vectorized implementation”实际上已经变成不同算法，应该用不同方法名和独立超参，而不是当作纯加速后端。
