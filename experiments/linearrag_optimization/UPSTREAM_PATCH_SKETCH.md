# Mapping prototypes to the upstream LinearRAG implementation

本文件只做“如何映射”的草图，不复制作者代码。

## `calculate_entity_scores*`

建议统一输出：

```text
scores_by_entity_id
first_activation_hop_by_entity_id
frontier_history
used_sentence_ids
```

不要让 BFS 用“last path score”，vectorized 用“sum score”。

## `calculate_passage_scores`

当前 nested passage×entity 逻辑建议替换成：

```text
activated_weight[e] = score[e] / (first_hop[e] + 1)
entity_mass[p] = sparse_count_matrix[p,:] @ activated_weight
passage_score[p] = passage_ratio * dense_similarity[p] + log1p(entity_mass[p])
```

attribute-query fallback 如果保留，应在这个 vector 上做额外 sparse/keyword feature，而不是回到文本双重循环。

## `dense_passage_retrieval`

拆成：

```text
similarity_vector()   # graph retrieval initialization
topk()                # no-entity fallback only
```

## `_precompute_sparse_matrices`

若长期保留 PyTorch backend：

- 避免每次 `retrieve()` 重建；
- index 后持久化 edge index/CSR；
- 不必同时 materialize 完全重复的 E→S 和 S→E COO；
- query hop 中避免 `.to_dense()` 全长向量。

## `add_adjacent_passage_edges`

改成显式 document boundaries，并默认关闭直到 ablation 证明它是方法必要组成。
