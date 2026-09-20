# Codex F1 review closure — continue existing work

继续 `codex/f0-semantic-temporal-20260909`，已审核 checkpoint 为 `742c2a84819e122429cfa5b5973c173c734714b3`。若有更晚工作，记录实际 HEAD，不回退、不覆盖、不重抓数据。

先 `git status --short`、`git fetch origin main`；读取本文件及 `research/iclr_fit_validation/round63_f1_checkpoint_audit_and_review_closure.md`。本任务只补当前 F1 校准的诊断与可操作性，不替换科研问题、路线或 corpus。复用全部已存 Q0/Q1 分数。

## 1. 修诊断，不重算模型

- 重新计算 tokenizer 配对输入的 query/document 原始与实际保留 token 数；使用实际推理时的文本规范化、tokenizer、special tokens、padding mask 和 max_length。用 sequence_ids 或经过验证的等价方法分开两段。原长恰等于512不算截断；两段单独小于512但合计超长必须能检测。旧评分不变，生成 v2 诊断而非覆盖旧文件。
- 分开 dense_rank 与 reranker_rank，后者从已存分数降序排列并固定 tie-break。明确当前 rank_change_mean_abs 原本是 dense 顺序。导出两种排序诊断与小型 summary，避免仅提交多 MB 单行 JSON。
- duplicate 检查统一处理已知标题前缀；日期差从记录计算，不硬编码 -354。
- 回归测试调用真实 production matcher，并与小图 exhaustive oracle 比较。补错误注入测试，不只重复记录字段自身的公式。

## 2. 产出真正可填写的评审包

保持24个 calibration seeds；96个 certification seeds不用于调试或标注。

保留现有三类材料：seed、单篇证据、block。新增 Q0/Q1 质量对比池：每 seed 取 Q0 reranker top10、Q1 reranker top10、原展示8篇文献的并集，按(seed,paper)去重，上限672条，报告实际数量。仅排序已存分数，不调用模型。

先批准中性的 scientific-need 文本，再做两版检索结果的相关性判断，避免把 Q1 当作相关性的定义。保留 DIRECT_RELEVANCE / TRANSFER_ONLY / OFF_TOPIC / UNCLEAR；TRANSFER 不自动计入直接相关。全部目标字段初始为 null。

输出一个离线 `review.html`（或仓库已有等价工具）：能看原文、填选项、保存并导入进度、导出 JSONL。评审端不得包含模型分数、候选来自Q0还是Q1、旧标签、来源ID或私有映射；映射仅留在独立工程文件。只看4个slots不等于认证8/12个，更不等于已经审核通过。seed审核与来源事实核对可有自己的非盲页面，不能混入单篇相关性盲评界面。

对 source-only Q2 修复提出 `Q2_REPAIR_PROPOSALS.jsonl`，记录源文依据、拟保留背景、拟删除的focal solution/results、范围是否改变、信息不足项及 approval=null。不得仅为提升匹配数量而泛化问题。AI建议必须标 `AI_PROVISIONAL`，不能计成人工标签，不能提前展示给独立标注者。不推测新的科学空白。

## 3. 有界验收与停止

测试：token边界；dense/reranker排序；真实matcher；前缀重复；评审导出无私有字段；导出/导入 roundtrip；完整分母/null保留；source spans与原文对应；calibration/certification隔离。人类输入未提供时不执行Q2评分、不生成认证结论。未知时间不阻塞评审页面完成，但继续禁止历史洁净主张。

交付到 `experiments/idea_collapse/f1_calibration/review_closure/`：
`DIAGNOSTICS_V2_SUMMARY.json`、`REVIEW_POOL_MANIFEST.json`、`review.html`、空标注模板、`Q2_REPAIR_PROPOSALS.jsonl`、测试日志及 `REVIEW_CLOSURE_REPORT.md`。记录输入/输出hash、原checkpoint、所有失败与变更。提供一个可由人实际打开并填写的入口，而不只是更多状态文件。

全任务新的模型 forward calls=0；tokenizer与CPU派生计算允许。不得运行ARS、proposal generation、baseline、P0/P1；不得调用付费API，不自动填写人工标签，不改门槛。

每阶段小步commit，完成push并验证远端。返回：
BRANCH / FINAL_COMMIT / DIAGNOSTIC_FIXES / REVIEW_POOL_PAIRS / REVIEW_ENTRY / Q2_PROPOSALS / HUMAN_LABELS_IMPORTED / NEW_MODEL_FORWARD_CALLS=0 / TESTS / STATUS=AWAITING_CALIBRATION_DECISIONS。

完成即STOP。下一项科学进展是研究者的实际校准意见，不是自动进入96-case认证或继续全量评分。
