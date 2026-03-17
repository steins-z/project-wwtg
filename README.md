# 周末去呀 🎉

AI 帮你 30 秒搞定周末出行方案。微信小程序 MVP。

## 项目结构

```
├── backend/           # FastAPI 后端
│   ├── app/           # 主应用代码
│   │   ├── services/  # LLM / 天气 / 地图 / 爬虫 / 埋点
│   │   ├── api/       # API 路由
│   │   └── models/    # 数据模型
│   ├── tests/         # 59 个测试
│   └── .env.example   # 环境变量模板
├── miniprogram/       # 微信小程序前端
├── docs/              # PRD、技术设计、竞品分析等
└── docker-compose.yml # 一键启动（API + Redis + PostgreSQL）
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/steins-z/project-wwtg.git
cd project-wwtg
git checkout feat/wwtg/dev-m5
```

### 2. 配置 API Key

```bash
cd backend
cp .env.example .env
```

打开 `backend/.env`，替换以下值：

| 变量 | 说明 | 去哪拿 |
|------|------|--------|
| `LLM_API_KEY` | DeepSeek API Key | [platform.deepseek.com](https://platform.deepseek.com) |
| `WX_APP_ID` | 小程序 AppID | [mp.weixin.qq.com](https://mp.weixin.qq.com) → 开发管理 |
| `WX_APP_SECRET` | 小程序 AppSecret | 同上 |
| `AMAP_API_KEY` | 高德地图 Key | [lbs.amap.com](https://lbs.amap.com) → 控制台 → 应用管理 |

> ⚠️ **不填 `LLM_API_KEY` 也能启动**，会走 mock 模式返回示例方案。

### 3. 启动后端（Docker 方式，推荐）

```bash
cd ..  # 回到项目根目录
docker-compose up --build
```

启动后：
- API 地址：`http://localhost:8000`
- 健康检查：`http://localhost:8000/health`
- 包含 Redis + PostgreSQL，不用单独装

### 3b. 启动后端（本地开发方式）

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

> 本地模式需要自己跑 Redis 和 PostgreSQL。

### 4. 启动小程序

1. 下载 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. 打开开发者工具 → 导入项目 → 选 `miniprogram/` 目录
3. 填入你的 **AppID**（在 `miniprogram/project.config.json` 的 `appid` 字段替换）
4. 开发者工具里即可预览

> 小程序默认有 mock 模式，不连后端也能看 UI 效果。

### 5. 运行测试

```bash
cd backend
pytest  # 59 个测试
```

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | FastAPI + Python 3.11+ |
| LLM | DeepSeek V3（OpenAI 兼容接口） |
| 数据库 | PostgreSQL + Redis |
| 天气/地图 | 高德开放平台 API |
| 数据源 | 小红书爬虫（Playwright） |
| 前端 | 微信小程序原生 |
| 部署 | Docker Compose |

## 功能

- 💬 对话式交互，告诉 AI 你在哪、几个人、想怎么玩
- 📋 30 秒生成 2 个差异化方案（一动一静）
- 🌤️ 实时天气 + 穿衣建议
- 🗺️ 一键导航到每个站点
- 📕 标注数据来源（小红书热门 vs AI 推荐）
- 🔄 不喜欢？换一批，不会重复推荐
- 📊 关键行为埋点（方案生成/选择/拒绝/详情查看/导航点击）

## 支持城市

MVP 阶段：**苏州、上海、杭州**
