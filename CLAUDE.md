# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. 项目概述

AI 驱动的个人工作经验积累工具。用户通过对话或快记输入工作内容，后端 AI 管道自动提炼为结构化经验卡片并关联技能图谱。

## 2. 技术栈

| 层 | 选型 | 版本 |
|---|---|---|
| 语言 | Python | ≥3.12 |
| Web 框架 | FastAPI | ≥0.115 |
| ORM | SQLAlchemy | ≥2.0.35 |
| 数据库 | SQLite (aiosqlite) | ≥0.20 |
| 计划任务 | APScheduler | ≥3.10 |
| 配置管理 | pydantic-settings | ≥2.5 |
| AI SDK | anthropic / openai | ≥0.34 / ≥1.51 |
| 测试 | pytest + httpx | ≥8.3 / ≥0.27 |
| 前端框架 | Vue 3 | ^3.5 |
| 构建工具 | Vite | ^8.1 |
| 样式 | Tailwind CSS | ^4.3 |
| 状态管理 | Pinia | ^3.0 |
| 路由 | Vue Router | ^4.6 |
| HTTP 客户端 | Axios | ^1.18 |

## 3. 指令

```bash
# 全部后端测试
uv run python -m pytest backend/tests/ -v

# 单测文件
uv run python -m pytest backend/tests/test_pipeline.py -v

# 单测用例
uv run python -m pytest backend/tests/test_pipeline.py::test_process_record_creates_card -v

# 后端开发服务器 (:8000)
uv run uvicorn backend.main:app --reload

# 前端开发服务器 (:5173，/api 代理到 :8000)
cd frontend && npm run dev

# 前端生产构建
cd frontend && npm run build
```

## 4. 项目架构

核心数据流向：

```
用户输入（教练对话 / 快记）
  → RawRecord（raw_records 表）
  → process_record() 管道：LLM 提取 → 评分 → 打标签
  → ExperienceCard（experience_cards 表，source_record_id 关联原始记录）
  → SkillNode 创建或计数递增
```

**三层实体关系：** RawRecord ←(1:1)→ ExperienceCard ←(N:M via JSON tags)→ SkillNode。编辑 RawRecord 后重新执行管道，upsert 同一张卡片而非新建。

**LLM 可替换：** `backend/llm/base.py` 定义 `LLMProvider` 抽象类（`chat(system_prompt, user_message) -> str`），`factory.py` 单例工厂根据 `settings.llm_provider` 实例化（claude / openai）。切换模型只需改 `.env` 或调设置接口，管道代码不受影响。`llm_api_key` 使用 `SecretStr`，取值需调用 `.get_secret_value()`。

**配置：** `backend/config.py` 通过 pydantic-settings 自动读取 `.env`，启动时加载。

**数据库：** SQLite + SQLAlchemy，`check_same_thread=False`。`Base.metadata.create_all()` 在 FastAPI startup 事件中执行。测试通过 `conftest.py` 的 autouse fixture 按用例重建表（drop → create → yield → drop）。

**API 路由：**

| 前缀 | 文件 | 职责 |
|---|---|---|
| `/api/records` | `routers/records.py` | 原始记录 CRUD，创建/更新触发加工管道 |
| `/api/cards` | `routers/cards.py` | 经验卡片列表（搜索/技能筛选）+ 详情 + 更新 |
| `/api/coach` | `routers/coach.py` | POST `/chat`，保存记录并返回 AI 教练回复 |
| `/api/settings` | `routers/settings.py` | LLM 配置读写、提醒配置读写、提醒状态轮询 |

**前端：** Vue 3 SPA，Vite 开发代理 `/api` → `localhost:8000`。Pinia store 管理侧边栏快记和提醒弹窗状态。`App.vue` 每 60 秒轮询 `/api/settings/reminder/status` 触发弹窗。

**注意：** `ExperienceCardOut.metadata_` 字段使用 `serialization_alias="metadata"` 而非 `alias`，因为 SQLAlchemy Base 已占用 `metadata` 属性名。
