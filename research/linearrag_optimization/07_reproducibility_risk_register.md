# LinearRAG 可复现性与有效性风险登记表

| ID | 风险 | 证据/来源 | 对结论影响 | 优先动作 | Gate |
|---|---|---|---|---|---|
| R1 | BFS 与 vectorized 算法语义不一致 | 当前公开代码 + issue #26 | 高：速度/准确率无法同时解释 | differential tests；统一 tier/aggregation | P0 |
| R2 | first-hop tier off-by-one | 当前公开代码静态分析 | 高：直接改变 Eq.(7) passage bonus | `L=hop+1`；回归测试 | P0 |
| R3 | 多路径到同一 entity 的 score 语义不同 | BFS vs vectorized 代码 | 高：activated entity / passage prior 改变 | 冻结 max/sum 规则 | P0 |
| R4 | duplicate seed aggregation 不一致 | sparse coalesce / scatter / dict 行为 | 中 | seed max aggregation | P0 |
| R5 | benchmark chunking 与原始 split 不同 | issue #25；作者回复解释 re-chunking | 高：任务难度和 gold co-location 改变 | 双 chunking 报告 | P0 |
| R6 | passage adjacency 未在正文说明 | `add_adjacent_passage_edges()` | 高：可能是隐藏增益/泄漏 | no/within-doc/global 三组 ablation | P0 |
| R7 | adjacency 可能跨文档边界 | 依赖 global passage index | 高 | 保存 document_id/local_idx | P0 |
| R8 | Medical 默认 NER 可能大量 fallback | issue 讨论；作者改用 SciSpacy | 高：graph stage 贡献被高估/误解 | 报 fallback rate；domain NER | P0 |
| R9 | Appendix threshold 文本与图/代码不一致 | E.2 写 δ=4；图约 0.2–0.8；run.sh 0.1/0.4/0.5 | 中 | 以 run manifest 为准，报告 exact params | P0 |
| R10 | damping 正文常见值与 config 默认不同 | paper Eq.(6) 0.85；config default 0.5 | 中 | dataset run manifest | P0 |
| R11 | passage edge binary vs weighted 实现差异 | paper C binary；code count-normalized edge | 中/高 | binary vs weighted ablation | P1 |
| R12 | passage score 每 query 重复字符串计数 | current code | 中：效率；可能 substring 错计 | offline span count sparse matrix | P1 |
| R13 | full argsort dense passages 不必要 | current code | 低/中：效率 | no-sort vector；fallback argpartition | P1 |
| R14 | vectorized path 每 hop densify | current code | 高（大图效率） | true sparse frontier backend | P2 |
| R15 | E→S 与 S→E 双份 sparse storage | current code | 中（memory） | CSR/CSC view 或单 edge index | P2 |
| R16 | full-graph PPR 随全图线性 | paper + code | 中/高（超大规模） | local push + residual fallback | P2 |
| R17 | GPT-based evaluator 版本漂移 | 论文 Table 4 虽多 evaluator，但 API model 可变化 | 中 | freeze model id/date/prompt；加 EM/F1 | P0 |
| R18 | 只有平均 accuracy，缺少 variance | 主表多为点估计 | 中 | bootstrap CI / repeated generation | P1 |

## 1. 风险分组

### 语义正确性风险

`R1–R4` 是最危险的，因为它们会导致“相同方法不同实现”产生不同结果。任何优化前必须解决。

### 数据/任务定义风险

`R5–R8` 决定我们到底在解决哪个任务。尤其 chunking 与 query NER fallback 会改变 multi-hop 的实际难度。

### 论文—代码配置风险

`R9–R11` 不一定是 bug，但如果不记录 exact run config，复现者会得到不同实验对象。

### 工程效率风险

`R12–R16` 是最容易形成实质加速的部分，其中 passage sparse matvec 属于低风险 exact optimization；local PPR 属于有研究空间的 approximate optimization。

### 评测风险

`R17–R18` 影响结论稳定性。论文已经用多个 evaluator 做 robustness，这是优点；进一步最好加 deterministic lexical metrics 和置信区间。

---

## 2. 建议的每次实验 manifest

```json
{
  "git_commit": "...",
  "dataset": "2wikimultihop",
  "dataset_hash": "...",
  "chunking": {
    "source": "original|fixed_token",
    "token_size": 1000,
    "overlap": 100,
    "hash": "..."
  },
  "ner_model": "en_core_web_trf",
  "embedding_model": "all-mpnet-base-v2",
  "retrieval_backend": "reference|bfs|vectorized",
  "max_iterations": 3,
  "threshold": 0.4,
  "top_k_sentence": 1,
  "passage_ratio": 0.05,
  "damping": 0.5,
  "passage_adjacency": "none|within_doc|global",
  "edge_weighting": "binary|count_normalized",
  "generator": "...",
  "evaluator": "...",
  "fallback_rate": 0.0
}
```

没有这个 manifest，不建议比较两个 accuracy 数字。
