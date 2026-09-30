# 真实学习资料场景验证基准 (Study Library Validation Benchmark)

本目录用于对自适应多级 RAG 架构（Adaptive Multi-Tier RAG）在真实个人学习资料库（如 `E:\me\Documents\学习资料`）下的工程表现进行量化回归测试与验收。

---

## 1. 验证目标

验证系统在脱离合成数据（Synthetic Data）后，面对真实杂乱个人资料时的核心能力：
1. **跨书定位效率**：能否在 50+ 本书的个人知识库中，1 秒内雷达定位目标文献；
2. **快查心流保护**：确切语法、配置、参数快查是否能在 1 轮内（< 1.0s）流式返回，不触发昂贵迟钝的树状 Agent 导航；
3. **沉浸式研读加速**：在针对单本书连续追问（$N \ge 2$）时，能否自动懒升级到 GPU 显存 KV Cache，获得亚秒级全书注意力推理；
4. **无目录容错**：面对没有目录的课件 PPT 与零散笔记，是否具备无目录退化保护，拒绝盲目顺序翻页；
5. **多模态图表理解**：面对复杂架构图、时序图与数学公式页，能否按需切出原页高清图像送入 Vision-LLM 原汁原味解读。

---

## 2. 场景数据集定义 (`study_library_scenarios.json`)

| 场景 ID | 场景名称 | 模拟真实场景 | 预期触发路由 | 核心合格指标 |
| :--- | :--- | :--- | :--- | :--- |
| **SCENARIO-01** | `cross_document_radar_search` | 跨 50 本书搜索“哪几本讲了 epoll LT 与 ET” | `Tier1_FTS_Macro_Filter` | 单轮直出（0 Agent 循环），延迟 < 1.0s，Top-3 命中率 100% |
| **SCENARIO-02** | `fast_syntax_param_lookup` | 查 Go `sync.Pool` 的具体 GC 回收阶段 | `Tier1_Small_To_Big` | 命中段落自动展开为小节，延迟 < 0.8s，原文引用字符 100% 匹配 |
| **SCENARIO-03** | `deep_single_book_study` | 研读 800 页大部头，连续深层追问 3+ 轮 | `Tier2_Lazy_KV_Cache` | 第 2 轮自动转热缓存，后续响应 < 0.5s，跨章节对比无遗漏 |
| **SCENARIO-04** | `slides_flat_notes_without_toc` | 查询无目录的微服务课件 PPT 第 28 页 | `Tier1_Layout_Window_Fallback` | 目录为空时不挂起、不死锁，平滑走布局聚类窗口 |
| **SCENARIO-05** | `multimodal_diagram_formula` | 解读第 17 页的分布式事务时序架构图 | `Tier4_Multimodal_Page_Dispatch` | 自动渲染 PDF 高清原页图送入多模态模型，图表信息无丢失 |

---

## 3. 测试断言与自动化核验

本基准通过 `tests/validation/test_study_library_scenarios.py` 驱动测试：
1. **Schema 结构与契约检验**：保证每个测试用例均具有确定性的指标阈值；
2. **路由决策契约**：根据用户查询意图与会话状态，断言路由器输出正确的 Tier 级别；
3. **Quote-then-Answer 强核验**：凡属于事实类回答，必须携带原文字符串，断言其在原文档中物理存在。
