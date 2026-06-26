# 问题记录

开发测试过程中发现的问题及解决方法。

---

## 问题列表

| # | 日期 | 问题 | 状态 |
|---|------|------|------|
| 1 | 2026-06-25 | 教练对话回复延迟 ~60s | ✅ 已解决 |

---

### 问题 1: 教练对话回复延迟约 60 秒

**日期:** 2026-06-25

**现象:** 用户在教练对话中输入工作内容后，等待约 1 分钟才收到 AI 回复。

**根因分析:**

1. **串行 3 次 LLM 调用** — 教练端点 (`POST /api/coach/chat`) 串行执行了 `process_record()`（提取 + 评分，2 次调用）和 `get_coach_response()`（对话生成，1 次调用），共 3 次 LLM 请求阻塞返回。
2. **DeepSeek V4 Pro 默认开启思考链** — 每次调用生成大量 `reasoning_content`（推理 token），额外增加延迟。实测单次调用：禁用前 5.7s / 256 tokens，禁用后 1.9s / 20 tokens。

**解决方案:**

1. `backend/routers/coach.py` — `process_record()` 改为后台线程异步执行，教练回复只需 1 次 LLM 调用即可返回
2. `backend/llm/openai_provider.py` — 新增 `disable_thinking` 参数，通过 `extra_body={"thinking": {"type": "disabled"}}` 禁用思考链
3. `backend/llm/factory.py` — DeepSeek 提供商默认启用 `disable_thinking=True`

**最终效果:** 端到端延迟从 ~60s 降至 ~2s。
