# 🗿 Polyglot Code Rosetta

> **Your Self-Evolving Personal Syntax Knowledge Base.**
> 一个懂你思维、零延迟的跨语言代码语法速查与知识管理中枢。

---

## 📖 项目简介 (Introduction)

在日常的 Data Science 和 Quant Finance 工作中，我们经常需要在 Python (Pandas)、R (Base) 和 SQL 之间反复横跳。虽然现有的大模型 (如 ChatGPT/DeepSeek) 可以回答语法问题，但每次提问都需要经历“打开网页 -> 输入上下文 -> 等待流式输出 -> 复制”的漫长过程。

**Polyglot Rosetta** 旨在解决这一痛点。它采用 **Local-First (本地优先)** 架构，将数据操作的核心概念（如“合并”、“透视”、“填补缺失值”）作为中枢，一键映射出对应的 Python、R 和 SQL 原生写法。通过本地 JSON 数据库，实现**毫秒级零延迟检索**；并通过接入大模型 API，赋予了知识库**自我进化**的能力。

---

## ✨ 核心特性 (Key Features)

* **⚡️ 零延迟模糊检索 (Blazing Fast Fuzzy Search)**
  * 内置跨字段全局检索引擎。无论是输入中文概念（如“合并”）、功能标签（如“left join”），还是直接输入某一种语言的残缺代码（如 `pd.merge` 或 `isna`），都能瞬间定位到包含三种语言的完整对照卡片。
* **🧠 AI 驱动的知识增强 (AI-Augmented Generation)**
  * 告别繁琐的手动录入。只需在侧边栏输入一个不懂的“中文概念”，后台将自动唤醒 DeepSeek 大模型，瞬间生成 Python、R (Base) 和 SQL 的高频标准写法及参数解析，并无缝写入本地数据库。
* **🛠️ 沉浸式知识管理 (CRUD & Inline Management)**
  * **内联编辑 (Inline Editing):** 发现标签不够精准？直接展开卡片修改并保存，状态即刻同步。
  * **安全防误删 (Safe Deletion):** 采用现代化气泡弹出交互 (Popover)，二次确认机制彻底杜绝误删手滑。
* **🛡️ 隐私与安全双重保障 (Privacy & Security First)**
  * 数据库完全存储在本地 `snippets.json`，高度定制化且无需联网即可查询。
  * API Key 采用严格的 `.env` 环境变量隔离，配合 `.gitignore`，确保开源分享时绝不泄漏个人凭证。

---

## 🛠️ 技术栈 (Tech Stack)

* **前端交互**: `Streamlit` (极简响应式 UI)
* **核心算法**: `thefuzz` (Levenshtein 距离模糊匹配)
* **后端驱动**: `Python 3.10+` + `subprocess` (子进程调度)
* **数据持久化**: 本地 `JSON` (轻量级文档型存储)
* **AI 大脑**: `DeepSeek-V3 API` (Prompt Engineering 强制结构化输出)

---

## 🚀 快速开始 (Quick Start)

### 1. 克隆项目与环境准备
确保你的电脑已安装 Python 及 pip。下载项目后，在终端运行：
```bash
pip install streamlit thefuzz python-dotenv requests
```

### 2. 配置环境变量 (至关重要)
在项目根目录新建一个名为 `.env` 的文件，填入你的大模型 API Key（参考 `.env.example`）：
```text
DEEPSEEK_API_KEY=sk-你的真实API_KEY
```

### 3. 一键启动
* **开发者模式**: 在终端运行 `streamlit run app.py`。
* **沉浸模式**: 直接双击项目根目录下的 `Start_Rosetta.bat`，即可在后台静默唤醒环境并弹出浏览器界面。

---

## 📂 目录结构 (Folder Structure)

```text
Project_rosetta/
├── Catcher/
│   └── generator.py       # 后端自动化数据抓取与大模型交互引擎
├── Search/
│   └── snippets.json      # 属于你自己的高价值代码知识库
├── .env                   # 本地环境变量 (不参与 Git 追踪)
├── .env.example           # 环境变量配置模板
├── .gitignore             # Git 忽略配置
├── app.py                 # Streamlit 前端渲染与搜索引擎主程序
├── Start_Rosetta.bat      # Windows 一键启动批处理脚本
└── README.md              # 项目说明文档
```

---

## 🔮 未来规划 (Roadmap)

本项目目前处于稳定可用状态，未来计划引入以下工程化升级：
- [ ] **数据验证**: 引入 `Pydantic` 拦截大模型异常格式输出，提升数据库健壮性。
- [ ] **高并发处理**: 使用 `asyncio` 重构 `generator.py`，支持批量概念的一键并发生成。
- [ ] **语义检索引擎**: 从字符级 Fuzzy Matching 升级为基于 ChromaDB 的本地 Vector Search。
- [ ] **日志监控**: 接入标准 `logging` 模块，沉淀系统运行状态。

---

*“Code is read much more often than it is written.”* *构建这个工具不仅是为了加速代码编写，更是为了沉淀我们思考数据的维度。*