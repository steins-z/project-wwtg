# Azure 资源配置指南

**负责人：** Juanjuan  
**时间节点：** M4/M5 阶段（内测部署前）  
**预估费用：** < 300 元/月

---

## 需要创建的资源

### 1. 资源组 (Resource Group)
- **名称建议：** `rg-wwtg-prod`
- **区域：** East Asia 或 China East 2（看哪个延迟低）
- 操作：Azure Portal → 资源组 → 创建

### 2. Azure Container Apps
- **用途：** 跑 FastAPI 后端
- **配置：**
  - 环境名：`wwtg-env`
  - 容器应用名：`wwtg-api`
  - 2 replicas（最小 0，按需扩缩）
  - CPU: 0.5 核 / 内存: 1GB（MVP 够用）
- 操作：Azure Portal → Container Apps → 创建

### 3. Azure Database for PostgreSQL
- **用途：** 用户数据、会话、方案、埋点
- **配置：**
  - 服务器名：`wwtg-pg`
  - 版本：PostgreSQL 16
  - SKU：Burstable B1ms（最便宜的，MVP 够用）
  - 存储：32GB
  - 数据库名：`wwtg`
  - 用户名/密码：自定义（记下来，配到 .env）
- 操作：Azure Portal → Azure Database for PostgreSQL → 灵活服务器 → 创建

### 4. Azure Cache for Redis
- **用途：** 会话缓存、POI 数据缓存、限流
- **配置：**
  - 名称：`wwtg-redis`
  - SKU：Basic C0（250MB，MVP 够用）
- 操作：Azure Portal → Azure Cache for Redis → 创建

---

## 创建完成后需要做的

1. **记录连接信息**（不要发群里，直接配到服务器 .env）：
   - PostgreSQL 连接串：`postgresql+asyncpg://<user>:<password>@<host>:5432/wwtg`
   - Redis 连接串：`rediss://<password>@<host>:6380/0`（注意 Azure Redis 用 SSL，端口 6380）

2. **网络配置**：
   - PostgreSQL 防火墙：允许 Container Apps 子网访问
   - Redis：允许 Container Apps 访问

3. **Container Apps 环境变量**：
   - 把 `.env.example` 里的所有变量配到 Container Apps 的环境变量中

---

## 暂时不需要（后续迭代）

- 自定义域名 + SSL（Azure Container Apps 自带免费 SSL）
- CDN
- 监控告警（先用 Azure 自带的 Log Analytics）

---

**有问题找：** SuperCrew001（技术）/ pm-Octopus（产品）
