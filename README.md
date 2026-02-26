# LifelightMemory Lab（心光 App 4.0 Memory 能力公开抽象版）

[![Backend CI](https://github.com/xiaosen3333/LifelightMemory-Lab/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/xiaosen3333/LifelightMemory-Lab/actions/workflows/backend-ci.yml)

[English README](README.en.md)

> 公司项目无法开源，这里是同栈的复刻/练手版本/抽象模块。  
> 本仓库用于公开展示后端与运维工程能力，不包含任何公司敏感实现。

本项目对应心光 App 4.0 的核心功能 Memory（记忆藤蔓），目标是让系统真正懂用户：从用户日记和对话中提取记忆事实，进行阶段性总结，并生成可视化记忆藤蔓与记忆洞察报告，让用户直观感知自己的变化。

## 这个仓库的目的

用于求职场景展示我的后端与运维能力：

- FastAPI 服务建模与接口设计
- 结构化存储 + 向量检索（Postgres + Qdrant）
- Docker Compose 一键拉起完整系统
- GitHub Actions 质量门禁（lint/test/build）
- 可执行部署脚本（健康检查 + 自动失败退出）

## 4.0 实战亮点（公司项目可公开指标）

以下指标来自我负责的公司项目 4.0 版本 Memory 能力建设，数据按可公开口径整理：

- 负责心光 4.0 核心能力 Memory（记忆藤蔓）建设，打通“日记/会话 -> 事实抽取 -> 画像生成 -> 用户反馈闭环”全链路。
- 4.0 上线首周（2025-09-13~2025-09-19）Memory 主路径渗透率达 `88.56%`（`6044/6825`，`chat_session` 去重用户口径），成为核心使用路径。
- 为实现记忆事实可视化，设计“记忆藤蔓”结构并设计用户记忆洞察报告。
- 在 Memory 服务口径下，D7 活跃留存从 `1.30%` 提升到 `2.01%`（`+0.71pp`）；D7 日记口径从 `0.77%` 提升到 `0.97%`（`+0.20pp`）。
- 基于 `user_profiles` 反馈数据，4.0 新推出的用户记忆报告显式满意度好评率达 `90.84%`（`23396/(23396+2358)`），后续月度稳定在 `92%+`。
- 支撑大规模数据与在线服务：`chat_session` 约 `190万+`、`chat_session_messages` 约 `600万+`、`user_profiles` 约 `44万+`、`user_profiles_facts` 约 `198万+`。
- 工程侧具备稳定性设计：流式接口、异步后台任务、Redis 队列（去重/重试/可见性）、画像一致性校验与自动化清理机制。

## 业务截图（4张）

### 1）记忆藤蔓主视图

![记忆藤蔓主视图](docs/showcase/screenshots/01-memory-vine-timeline.png)

### 2）记忆主题可视化（主题选择）

![记忆主题可视化](docs/showcase/screenshots/02-memory-theme-selector.png)

### 3）阶段性记忆洞察卡片

![阶段性记忆洞察卡片](docs/showcase/screenshots/03-memory-insight-card.png)

### 4）记忆洞察报告（雷达图 + 心路历程）

![记忆洞察报告](docs/showcase/screenshots/04-memory-insight-radar.png)

## 系统能力

- `POST /v1/memory/ingest`：写入用户记忆文本
- `POST /v1/memory/search`：按用户范围进行语义检索，自动词法降级
- `GET /v1/health`：返回 API、DB、Redis、Qdrant 健康状态

## 我负责的内容

- 架构设计：分层、数据模型、检索与降级策略
- 代码实现：FastAPI + SQLModel + Qdrant client
- 工程化：Makefile、测试、lint、GitHub CI
- 运维能力：容器编排、环境变量管理、部署脚本与健康检查

## 架构图

```mermaid
flowchart LR
    A["Client"] --> B["FastAPI Router"]
    B --> C["Memory Service"]
    C --> D["Postgres (SQLModel)"]
    C --> E["Qdrant Vector Store"]
    B --> F["Health Service"]
    F --> D
    F --> G["Redis"]
    F --> E
```

## 可公开边界说明

下列内容在公司环境中存在，但本仓库不包含：

- 私有业务规则与线上数据结构细节
- 公司内部模型配置、Prompt、风控策略
- 生产网络拓扑与密钥体系
- 真实用户数据与日志

本仓库复刻的是工程方法与技术栈，不是生产代码拷贝。

## 快速开始

### 1）本地 Python 运行

```bash
git clone https://github.com/xiaosen3333/LifelightMemory-Lab.git
cd LifelightMemory-Lab
cp .env.example .env
make install
make run
```

API 文档：`http://127.0.0.1:8000/docs`

### 2）Docker Compose 运行

```bash
cp .env.example .env
docker compose up --build -d
curl http://127.0.0.1:8000/v1/health
```

## API 示例

```bash
# Ingest
curl -X POST 'http://127.0.0.1:8000/v1/memory/ingest' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: dev-api-key' \
  -d '{"user_id":"u-1001","content":"I practiced backend system design today.","language":"en-US"}'

# Search
curl -X POST 'http://127.0.0.1:8000/v1/memory/search' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: dev-api-key' \
  -d '{"user_id":"u-1001","query":"system design","limit":5}'
```

## 工程化与运维信号

- `Makefile`：一键 lint/test/run/up/down
- `docker-compose.yml`：app + postgres + redis + qdrant
- `scripts/deploy_standalone.sh`：部署 + 健康检查
- `.github/workflows/backend-ci.yml`：lint + tests + docker build
- `CONTRIBUTING.md`：commit 规范 + PR 检查清单

## 目录结构

```text
LifelightMemory-Lab/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   └── services/
├── tests/
├── scripts/
├── docs/
├── .github/workflows/
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── README.en.md
```

## 与公司项目能力映射

- 多路由 + 记忆处理核心：映射到 `api + services` 分层
- 向量检索 + 降级策略：映射到 `vector_store + lexical fallback`
- 部署与健康治理：映射到 `docker-compose + deploy script + health endpoint`
