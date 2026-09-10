# LinearRAG 研读与优化工作区

> 研究对象：**LinearRAG: Linear Graph Retrieval Augmented Generation on Large-scale Corpora**, ICLR 2026。  
> 阅读重点：论文正文第 1–10 页；附录仅在涉及可复现性、参数、扩展实验和 FAQ 时补充。  
> 本目录的目标不是复述论文，而是把论文的核心机制还原成可检验假设，并给出按风险/收益排序的优化路线与最小原型实验。

## 结论先行

LinearRAG 最值得保留的不是“GraphRAG”这个标签，而是一个非常清楚的工程/建模取舍：**离线阶段拒绝显式关系抽取，把实体—句子和实体—段落的共现结构作为无损索引；在线阶段再用查询语义决定哪些连接有用。** 这等价于把“容易犯事实错误的关系建模”从离线索引移到查询时的软传播与 LLM 阅读阶段。

我认为下一步最有潜力的方向不是重新引入 LLM 关系抽取，而是做 **Query-Calibrated LinearRAG**：保持 relation-free 的静态二部图，但让查询时的种子选择、传播归一化、剪枝预算和 PPR reset 更稳健、更一致、更稀疏。

优先级建议：

1. **P0：先解决实现语义与可复现性问题。** BFS 与 vectorized retrieval 当前并不语义等价；上游公开 issue 已报告 MuSiQue 上矩阵版本显著掉点。代码中还存在 hop/tier 记账差异、路径聚合语义差异、全局 passage adjacency 与论文图定义不一致等值得先审计的问题。
2. **P1：做 hub-aware、context-aware 的查询时权重。** 对高频实体进行 degree normalization / IDF correction；对歧义 query entity 用“实体表面相似度 + query→候选上下文相似度”做种子重排。
3. **P1：把固定阈值升级为“固定语义底线 + 自适应 frontier budget”。** 论文已经证明随 hop 衰减阈值并不好，因此不建议简单做 distance-decay；更合理的是保留固定阈值，只在候选爆炸时执行 top-B/quantile 截断。
4. **P1/P2：把 passage initialization 真正向量化。** 上游实现对“所有 passage × 所有 activated entity”逐项字符串计数；已有 contain matrix 后完全可以改成稀疏矩阵乘法。
5. **P2：做 local-push PPR / query-induced subgraph。** 当前每个 query 在完整 passage–entity 图上跑 PPR，复杂度仍是全图线性。LinearRAG 已经有强局部激活信号，可以进一步把第二阶段限制在激活实体附近并给出误差界/回退机制。

## 本分支产物

研究文档：

- `01_paper_notes_pages_1_10.md`：逐页、逐模块阅读正文 1–10 页。
- `02_mechanism_reconstruction.md`：把 Tri-Graph、Eq. (3)–(7) 和实际数据流重新写成可实现形式。
- `03_upstream_code_audit.md`：论文与公开代码的映射、差异、潜在 bug 和性能热点。
- `04_optimization_roadmap.md`：按 P0/P1/P2 排序的优化方向、收益假设、失败条件。
- `05_experiment_plan.md`：真实 benchmark 的受控实验设计与统计/效率指标。
- `06_personal_reflections.md`：对这篇论文真正“新”的地方、边界和后续研究形态的个人判断。
- `07_reproducibility_risk_register.md`：chunking、NER、fallback、评测、参数和实现一致性的风险登记表。
- `08_patch_plan.md`：如果要在上游 LinearRAG 代码上落地，建议的补丁顺序和接口变化。

代码原型见：

- `experiments/linearrag_optimization/`

目前做了三类最小实验：

- **hop/tier 一致性回归**：展示第一跳实体被错误记成 level 1 时，Eq. (7) 风格的 passage bonus 会被放大 2 倍，并可翻转一个构造例子的 passage 排序。
- **歧义种子消解 demo**：展示 surface-only 最近邻可能选错 homonym，而加入 query→候选上下文相似度后可以纠正。
- **hub-noise synthetic benchmark**：在一个专门制造高频 hub 的 relation-free 图中，raw sum propagation 会激活约 289 个实体，而 degree-normalized 版本只保留 4 个 gold-chain 实体；在该构造下 top-5 passage recall 本身没有提高，所以它目前只支持“降噪/控搜索空间”的机制假设，不支持真实数据集 accuracy 提升的结论。
- **passage bonus 向量化 microbenchmark**：20k passages、10k entities、64 activated entities 的合成条件下，CSR sparse matvec 与保守的 Python nested membership baseline 数值完全一致，在本机最小计时约有 ~1900× 差距。这个数不是端到端加速，只说明此热点很值得改写。

## 重要边界

这些原型实验不使用 HotpotQA / 2Wiki / MuSiQue / Medical 的真实数据，也没有调用论文中的生成/evaluator LLM。因此：

- 可以用于发现实现错误、验证机制方向、排除明显坏想法；
- **不能**作为“LinearRAG 已被我们提高 X%”的证据；
- 真正论文级结论必须回到统一 chunking、统一 embedding、统一 generator、统一 evaluator 的 benchmark 上做多 seed / 多数据集验证。

## 外部材料使用说明

除附件论文外，我还阅读了作者公开仓库 `DEEP-PolyU/LinearRAG` 的当前 `src/LinearRAG.py`、`config.py`、`ner.py`、`embedding_store.py`、`scripts/run.sh`，以及截至 2026-09-10 仍公开的相关 issue。代码审计文档会明确区分“论文陈述”“上游实现事实”“本分支推断/假设”。
