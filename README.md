# 经验工厂 (Experience Factory)

AI 驱动的个人工作经验积累系统。解决"工作时间长了记性差、更新简历需要大量回忆整理"的痛点——不仅仅是记录，而是 AI 主动引导你把零散的工作记忆自动加工成结构化、可复用的经验资产。

## 核心链路

```
你说一句话 → 自动保存为原始记录 → AI 管道加工 → 结构化经验卡片 → 技能图谱
                     ↑                                      ↓
               可随时编辑补充 ←←←←← 原始记录 ←←←← 卡片可追溯来源
```

## 快速开始

### 环境要求

- Python 3.12+
- Node.js 20+
- [uv](https://docs.astral.sh/uv/)（Python 包管理）

### 安装与运行

```bash
# 1. 克隆仓库
git clone git@github.com:liwj-caiji/worker_helper.git
cd worker_helper

# 2. 安装 Python 依赖
uv sync --extra dev

# 3. 配置 LLM API Key
cp .env.example .env
# 编辑 .env，填入你的 LLM_API_KEY（支持 Claude / OpenAI）

# 4. 启动后端（http://localhost:8000）
uv run uvicorn backend.main:app --reload

# 5. 另一个终端，安装前端依赖并启动（http://localhost:5173）
cd frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:5173` 即可使用。

### 运行测试

```bash
uv run python -m pytest backend/tests/ -v
```

## 功能

### MVP 已实现

| 功能 | 说明 |
|---|---|
| 教练对话 | AI 主动引导你回顾工作，自然对话即可记录 |
| 碎片快记 | 侧边栏快速输入，想到什么记什么 |
| AI 加工管道 | 自动提取要点、量化成果、打技能标签、评分 |
| 经验卡片浏览 | 列表 + 搜索 + 按技能筛选 |
| 原始记录管理 | 查看/编辑原始输入，编辑后自动重新加工 |
| 定时提醒弹窗 | 可配置时间，PWA 通知 |
| LLM 可配置 | 设置页面切换模型，不影响功能 |

### 后续迭代

- 专项复盘模板
- 语音输入
- 简历/面试材料生成
- 能力图谱可视化
- 多用户支持
- Electron 桌面打包

## 技术栈

| 层 | 选型 |
|---|---|
| 后端 | Python + FastAPI |
| AI | LLM Provider 抽象层（默认 Claude，可切换 OpenAI 等） |
| 数据库 | SQLite（SQLAlchemy ORM） |
| 定时任务 | APScheduler |
| 前端 | Vue 3 + Vite + Tailwind CSS |
| 包管理 | uv |

## 项目结构

```
worker_helper/
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库引擎
│   ├── models.py            # ORM 模型
│   ├── schemas.py           # Pydantic 模型
│   ├── llm/                 # LLM 抽象层（Provider → Claude/OpenAI）
│   ├── services/
│   │   ├── pipeline.py      # AI 加工管道（提取→量化→归类→评分）
│   │   ├── coach.py         # 教练对话逻辑
│   │   └── reminder.py      # 定时提醒调度器
│   ├── routers/
│   │   ├── records.py       # 原始记录 API
│   │   ├── cards.py         # 经验卡片 API
│   │   ├── coach.py         # 教练对话 API
│   │   └── settings.py      # 配置 API
│   └── tests/               # 24 个测试用例
├── frontend/
│   └── src/
│       ├── views/           # 6 个页面
│       ├── components/      # 9 个组件
│       ├── api/             # API 客户端
│       ├── router/          # Vue Router
│       └── store/           # Pinia 状态管理
├── docs/superpowers/
│   ├── specs/               # 设计文档
│   └── plans/               # 实施计划
├── pyproject.toml
└── .env.example
```

## License

MIT
