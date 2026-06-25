# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. 项目概述

AI 驱动的个人工作经验积累工具。用户通过对话或快记输入工作内容，后端 AI 管道自动提炼为结构化经验卡片并关联技能图谱。

## 2. 技术栈

| 层 | 选型 |
|---|---|
| 后端 | Python 3.12+ / FastAPI / SQLAlchemy / SQLite |
| 前端 | Vue 3 / Vite / Pinia |
| AI | LLM Provider 抽象层（默认 Claude，可切换 OpenAI） |
| 包管理 | uv |
| 测试 | pytest |

## 3. 指令

```bash
# 全部后端测试
uv run python -m pytest backend/tests/ -v

# 单测文件 / 单测用例
uv run python -m pytest backend/tests/test_pipeline.py -v
uv run python -m pytest backend/tests/test_pipeline.py::test_process_record_creates_card -v

# 后端开发服务器 (:8000)
uv run uvicorn backend.main:app --reload

# 前端开发服务器 (:5173，/api 代理到 :8000)
cd frontend && npm run dev
```

## 4. 项目架构

**数据流：** 用户输入 → RawRecord → `process_record()` AI 管道 → ExperienceCard → SkillNode。

**实体关系：** RawRecord ← 1:1 → ExperienceCard ← N:M(tags) → SkillNode。编辑原始记录后重新执行管道，upsert 同一张卡片而非新建。

**LLM 切换：** 修改 `.env` 中 `LLM_PROVIDER` 为 `claude` 或 `openai`（或调用 `PUT /api/settings/llm`）。`factory.py` 单例工厂按配置实例化，`reset_provider()` 在配置变更时重建。

**API 路由：** `/api/records`（原始记录 CRUD）、`/api/cards`（经验卡片列表/搜索）、`/api/coach`（教练对话）、`/api/settings`（LLM/提醒配置）。

**前端：** SPA，`/api` 代理到后端。`App.vue` 定时轮询提醒状态触发弹窗。
