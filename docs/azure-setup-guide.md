# Azure 部署配置指南

> **时间节点：M4（内测部署）前完成**
> **操作人：Juanjuan**

## 前置条件
- Azure 账号已登录：[portal.azure.com](https://portal.azure.com)

## 步骤

### 1. 创建资源组
- 搜索「资源组」→ 创建
- **名称：** `rg-weekend-buddy`
- **区域：** East Asia（香港）

### 2. 创建 Container Apps 环境
- 搜索「Container Apps Environment」→ 创建
- 放在 `rg-weekend-buddy` 资源组下
- 选默认配置即可

### 3. 创建 PostgreSQL
- 搜索「Azure Database for PostgreSQL - Flexible Server」→ 创建
- **资源组：** `rg-weekend-buddy`
- **规格：** B1ms（最小，~¥150/月）
- **数据库名：** `weekend_buddy`
- 记下连接字符串，填入 `.env` 的 `DATABASE_URL`

### 4. 创建 Redis
- 搜索「Azure Cache for Redis」→ 创建
- **资源组：** `rg-weekend-buddy`
- **规格：** Basic C0（~¥100/月）
- 记下连接字符串，填入 `.env` 的 `REDIS_URL`

### 5. 部署应用（由开发完成）
- SuperCrew001 会通过 GitHub Actions 自动部署到 Container Apps
- Juanjuan 无需操作

## 预估月成本
| 服务 | 规格 | 月费 |
|------|------|------|
| Container Apps | 按需 | ~¥50 |
| PostgreSQL | B1ms | ~¥150 |
| Redis | Basic C0 | ~¥100 |
| **合计** | | **~¥300** |

## 需要填入 `.env` 的值
```
DATABASE_URL=<PostgreSQL 连接字符串>
REDIS_URL=<Redis 连接字符串>
```
