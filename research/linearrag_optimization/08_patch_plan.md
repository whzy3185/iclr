# 上游落地补丁计划（建议，不直接修改作者仓库）

## Patch 0：测试脚手架

新增：

```text
tests/test_retrieval_equivalence.py
tests/fixtures/tiny_trigraphs.py
```

先把 reference semantics 冻结。

---

## Patch 1：统一 activation state

定义结构：

```python
ActivationState(
    score: Tensor/ndarray,
    first_hop: int,
    predecessor_sentence: optional,
)
```

统一规则：

```text
seed first_hop = 0
level = first_hop + 1
multiple incoming paths: score reducer explicitly MAX or SUM
seed duplicates: MAX
```

BFS/vectorized 都调用相同 reducer。

---

## Patch 2：把句子选择语义独立成函数

当前 vectorized path 的“按 entity top-k sentence + union + aggregate”很难验证。建议定义：

```text
select_sentences(frontier, similarity, top_k, used_mask)
```

返回 edge-level selections，而不是只返回 sentence set。这样能保留“哪个 source entity 选中了这条 sentence”的信息，避免共享 sentence 时无意改变聚合语义。

---

## Patch 3：保存 count sparse matrix

index 阶段从 NER spans 直接得到：

```text
M_binary[s,e]
N_count[p,e]
```

保存为 `.npz` / torch sparse / parquet edge table。

在线 passage score：

```text
entity_weight = activated_score / level
mass = log1p(N_count) @ entity_weight
prior = passage_ratio * dense_sim + log1p(mass)
```

移除所有 `passage_text.count(entity_text)`。

---

## Patch 4：拆 dense similarity API

```text
passage_similarity_vector(query_embedding)   # O(Pd), no sorting
dense_topk(query_embedding, k)               # argpartition / torch.topk
```

graph path 使用前者；fallback 使用后者。

---

## Patch 5：显式 passage document boundary

dataset loader 需要返回：

```text
passage_id
document_id
local_chunk_index
text
```

adjacency 只允许：

```text
same document_id && abs(local_idx_i-local_idx_j)==1
```

并提供配置：

```text
passage_adjacency = none | within_document
```

不再用全局数字前缀猜。

---

## Patch 6：Context seed optional mode

增加：

```text
seed_candidate_k
seed_context_alpha
seed_margin_threshold
```

仅在 top1-top2 surface margin 小时触发邻接句 context scoring，控制额外成本。

输出日志：

```text
ambiguous_seed_queries
multi_seed_queries
mean_seed_margin
```

---

## Patch 7：Degree normalization

offline 预计算：

```text
sentence_entity_degree[e]
passage_entity_df[e]
```

在线可选：

```text
bridge_normalization = none | entity_degree | symmetric
passage_hub_correction = none | idf
```

默认仍 `none`，先做 ablation。

---

## Patch 8：Sparse frontier backend

不要把它叫“vectorized”就默认等价。完成 Patch 0–2 后，再用：

- CSR/edge index；
- segmented top-k；
- scatter add/max；
- sparse frontier tensors。

每次 CI 在 CPU 小图上和 reference diff。

---

## Patch 9：Local PPR experimental mode

```text
ppr_backend = full | local_push
local_dense_seed_k
local_epsilon
local_max_expansions
```

日志必须记录：

```text
visited_nodes
visited_edges
boundary_residual
fallback_to_full_ppr
rank_overlap_with_full (debug/eval only)
```

---

## Patch 10：Reproducibility manifest

每次 run 自动写：

```text
config.json
dataset_manifest.json
retrieval_diagnostics.jsonl
timing.json
```

其中 dataset manifest 必须包括 chunking 和 hash。把 issue #25/#26 这类问题转成自动可见信息，而不是依赖复现者猜。

---

## 推荐 PR 拆分

```text
PR1 correctness tests + tier fix
PR2 exact passage-score vectorization
PR3 boundary-aware adjacency + diagnostics
PR4 context seed / degree normalization experiments
PR5 true sparse backend
PR6 local PPR
```

不要把 PR1–PR6 合成一个巨大改动，否则任何准确率变化都无法归因。
